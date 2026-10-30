/* The map and current native pages must ship from one build and one source. */
const {test,before,after}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs/promises');
const path=require('node:path');
const crypto=require('node:crypto');
const {createPreviewServer}=require('../../../tools/serve.cjs');
const root=path.resolve(__dirname,'..');
let server,base;
before(async()=>{server=createPreviewServer();await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));base='http://127.0.0.1:'+server.address().port;});
after(async()=>{server.closeAllConnections();await new Promise(resolve=>server.close(resolve));});
const request=route=>fetch(base+route);
test('all 73 current routes share one build and only venues loads the registered map',async()=>{
 const routes=JSON.parse(await fs.readFile(path.join(root,'data/pages.json'),'utf8'));
 const events=JSON.parse(await fs.readFile(path.join(root,'data/events.json'),'utf8'));
 const names=[...Object.keys(routes),...events.map(e=>e.id)];assert.equal(names.length,73);
 for(const name of names){
  const response=await request('/events/app/'+name+'.html');assert.equal(response.status,200,name);
  const html=await response.text();assert.equal((html.match(/<script\b/g)||[]).length,name==='venues'?1:0,name);
  assert.doesNotMatch(html,/map-snapshot|consumer-lab|\/maps\/events|htmx|hx-boost/);
 }
});
test('every map mode resolves current resources and modules with the correct MIME type',async()=>{
 for(const prefix of ['app','themes/bumble-dark','themes/tide-light']){
  const route='/events/'+prefix+'/venues.html';const html=await (await request(route)).text();
  for(const [,ref] of html.matchAll(/(?:href|src)="([^"]+)"/g)){
   if(/^(#|https?:|mailto:|tel:)/.test(ref))continue;
   assert.equal((await request(new URL(ref,base+route).pathname)).status,200,ref);
  }
 }
 for(const name of ['venue-map.mjs','vendor/maplibre-6.16.0/maplibre-gl.mjs','vendor/maplibre-6.16.0/maplibre-gl-shared.mjs','vendor/maplibre-6.16.0/maplibre-gl-worker.mjs']){
  const response=await request('/events/runtime/map/'+name);assert.equal(response.status,200);assert.match(response.headers.get('content-type'),/javascript/);
 }
});
test('pinned MapLibre bytes and the approved dark style are preserved',async()=>{
 const manifest=JSON.parse(await fs.readFile(path.join(root,'data/map-dependencies.json'),'utf8'));
 assert.equal(manifest.maplibreVersion,'6.16.0');
 for(const [name,hash] of Object.entries(manifest.files))assert.equal(crypto.createHash('sha256').update(await fs.readFile(path.join(root,'src/map',name))).digest('hex'),hash,name);
 const style=await (await request('/events/runtime/map/maps/quiet-dark.json')).json();
 assert.equal(style.sources.openmaptiles.url,'https://tiles.openfreemap.org/planet');
 assert.equal(style.layers.find(l=>l.id==='background').paint['background-color'],'#15191b');
 assert.ok(style.layers.some(l=>l.type==='symbol'));assert.ok(style.layers.every(l=>!l.layout?.['icon-image']));
});
test('exact venue IDs use demonstration positions and current responsive card destinations',async()=>{
 const data=await (await request('/events/runtime/map/maps/venues.json')).json();
 const html=await (await request('/events/app/venues.html')).text();
 const venues=JSON.parse(await fs.readFile(path.join(root,'data/venues.json'),'utf8'));
 assert.deepEqual(data.venues.map(v=>v.id).sort(),venues.map(v=>v.id).sort());
 assert.match(data.coordinatePolicy,/not a verified business location/);
 for(const v of data.venues){assert.equal(v.demonstration,true);assert.match(html,new RegExp('id="map-'+v.id+'"'));assert.match(html,new RegExp('href="'+v.id+'\\.html"'));}
 assert.match(html,/View Sister and its 9 events/);assert.match(html,/tide-venue__select/);assert.match(html,/tide-venue__open/);
});
test('one footer belongs to the venue list and no caption reserves map height',async()=>{
 const html=await (await request('/events/app/venues.html')).text();
 assert.match(html,/data-lineup-venue-workspace="fixed"/);assert.equal((html.match(/<footer\b/g)||[]).length,1);
 const list=/<section[^>]+id="venue-list"([\s\S]*?)<\/section>/.exec(html)?.[1];assert.ok(list);
 assert.match(list,/<footer class="tide-app__site-footer">/);assert.match(list,/href="help.html"/);assert.doesNotMatch(html,/Illustrative venue locations\./);
 assert.match(html,/tide-venue-map__actions/);
});
