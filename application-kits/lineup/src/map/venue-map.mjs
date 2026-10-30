import {Map as LibreMap, Marker, LngLatBounds, AttributionControl, setWorkerUrl} from './vendor/maplibre-6.16.0/maplibre-gl.mjs';

// Lineup map enhancement over the current native venue markup.
const figure=document.querySelector('#venue-map');
const frame=figure?.querySelector('.tide-venue__map-frame');
const list=document.querySelector('#venue-list');
const points=[...figure.querySelectorAll('.tide-venue__point')];
const origins=points.map(point=>[point,point.parentElement]);
const status=document.createElement('p');
status.className='tide-caption tide-venue-map__status';status.setAttribute('role','status');status.setAttribute('aria-live','polite');
figure.append(status);
const settings=new URLSearchParams(location.search);
const motion=matchMedia('(prefers-reduced-motion: reduce)');
const storageKey='lineup-map:'+location.pathname;
let saved;
try{saved=JSON.parse(sessionStorage.getItem(storageKey)||'null');}catch{}
const selectedId=()=>{const match=/^#(?:map|venue)-(.+)$/.exec(location.hash);return match&&points.some(p=>p.id==='map-'+match[1])?match[1]:null;};
let map,venues=[],markers=[],ready=false,timer,observer;
const canvas=document.createElement('div');canvas.className='tide-venue-map__canvas';frame.append(canvas);
const tools=document.createElement('div');tools.className='tide-venue-map__tools';tools.hidden=true;tools.setAttribute('role','group');tools.setAttribute('aria-label','Map zoom');
function tool(label,text,run){const button=document.createElement('button');button.type='button';button.className='tide-photo-control';button.setAttribute('aria-label',label);button.textContent=text;button.addEventListener('click',run);tools.append(button);return button;}
tool('Zoom in','+',()=>map.zoomIn({duration:motion.matches?0:220}));
tool('Zoom out','−',()=>map.zoomOut({duration:motion.matches?0:220}));frame.append(tools);
const fit=document.createElement('button');fit.type='button';fit.className='tide-button tide-button--secondary tide-button--compact tide-venue-map__fit';fit.textContent='All venues';fit.hidden=true;frame.append(fit);
function bounds(){return venues.reduce((b,v)=>b.extend(v.coordinates),new LngLatBounds());}
function showAll(){map.fitBounds(bounds(),{padding:{top:82,right:60,bottom:70,left:60},maxZoom:14,duration:motion.matches?0:420});}
fit.addEventListener('click',showAll);
function visible(){return frame.getBoundingClientRect().width>0&&frame.getBoundingClientRect().height>0;}
function labelSides(){
  if(!ready)return;
  for(const venue of venues){const point=document.getElementById('map-'+venue.id);const xy=map.project(venue.coordinates);point.classList.toggle('tide-venue-map__label-left',xy.x>canvas.clientWidth*.52);}
}
function syncSelection(pan=false){
  const id=selectedId();
  for(const point of points){const active=point.id==='map-'+id;point.classList.toggle('tide-venue-map__selected',active);const link=point.querySelector('a');if(active)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');}
  for(const row of list.querySelectorAll('.tide-event-card')){for(const link of row.querySelectorAll('.tide-event-card__link')){if(row.id==='venue-'+id)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');}}
  if(ready&&visible()){
    map.resize();
    const venue=venues.find(v=>v.id===id);
    if(pan&&venue)map.easeTo({center:venue.coordinates,duration:motion.matches?0:440,essential:false});
    labelSides();
  }
  if(ready&&id){const venue=venues.find(v=>v.id===id);if(venue)status.textContent=venue.name+' selected.';}
}
function fail(message){
  clearTimeout(timer);ready=false;figure.classList.remove('tide-venue-map--ready');figure.dataset.mapState='fallback';figure.setAttribute('aria-label','Illustrated venue map');status.classList.remove('tide-sr-only');tools.hidden=true;fit.hidden=true;
  observer?.disconnect();if(map){map.remove();map=null;}
  for(const [point,parent] of origins){point.classList.remove('maplibregl-marker','maplibregl-marker-anchor-center','tide-venue-map__label-left');point.removeAttribute('style');parent.append(point);}
  canvas.remove();
  status.textContent=message+' The illustrated map and venue links remain available.';
}
window.addEventListener('hashchange',()=>requestAnimationFrame(()=>syncSelection(true)));
window.addEventListener('pagehide',()=>{
  if(!ready)return;
  try{sessionStorage.setItem(storageKey,JSON.stringify({hash:location.hash,center:map.getCenter().toArray(),zoom:map.getZoom(),listTop:list.scrollTop}));}catch{}
});
window.addEventListener('pageshow',()=>{if(ready)requestAnimationFrame(()=>{map.resize();syncSelection();});});
async function start(){
  if(settings.get('map')==='off'){fail('Interactive map is disabled for this test.');return;}
  figure.dataset.mapState='loading';status.textContent='Loading map…';
  try{
    const response=await fetch(new URL('./maps/venues.json', import.meta.url));if(!response.ok)throw new Error('Venue locations unavailable');
    venues=(await response.json()).venues;
    setWorkerUrl(new URL('./vendor/maplibre-6.16.0/maplibre-gl-worker.mjs', import.meta.url).href);
    map=new LibreMap({container:canvas,style:new URL(settings.get('map')==='fail'?'./maps/unavailable.json':'./maps/quiet-dark.json', import.meta.url).href,center:[-106.645,35.082],zoom:12.8,minZoom:10,maxZoom:18,attributionControl:false,cooperativeGestures:true,dragRotate:false,pitchWithRotate:false,touchPitch:false,renderWorldCopies:false,refreshExpiredTiles:true});
    map.touchZoomRotate.disableRotation();
    map.addControl(new AttributionControl({compact:false,customAttribution:'<a href="https://github.com/CartoDB/CartoDB-basemaps" target="_blank" rel="noopener" title="Dark Matter design derived from CARTO basemaps by Stamen and Paul Norman, CC BY 3.0; modified for Lineup">© CARTO</a>'}),'bottom-right');
    map.on('webglcontextlost',()=>fail('Interactive map rendering was interrupted.'));
    map.on('error',event=>{console.warn('Lineup map:',event.error?.message||'Map resource unavailable');if(!ready&&settings.get('map')==='fail')fail('Interactive map is unavailable.');});
    timer=setTimeout(()=>{if(!ready)fail('Interactive map could not load.');},18000);
    map.once('load',()=>{
      clearTimeout(timer);
      for(const venue of venues){const point=document.getElementById('map-'+venue.id);markers.push(new Marker({element:point,anchor:'center'}).setLngLat(venue.coordinates).addTo(map));}
      ready=true;figure.dataset.mapState='ready';figure.classList.add('tide-venue-map--ready');figure.setAttribute('aria-label','Venue map');status.classList.add('tide-sr-only');tools.hidden=false;fit.hidden=false;
      canvas.querySelector('canvas').setAttribute('aria-label','Interactive venue map. Use arrow keys to pan, plus and minus to zoom.');
      status.textContent='';
      let initialView=false;
      function applyInitialView(){
        if(!visible())return;
        map.resize();initialView=true;
        if(saved?.hash===location.hash){map.jumpTo({center:saved.center,zoom:saved.zoom});list.scrollTop=saved.listTop||0;}
        else{map.fitBounds(bounds(),{padding:{top:82,right:60,bottom:70,left:60},maxZoom:14,duration:0});const venue=venues.find(v=>v.id===selectedId());if(venue)map.jumpTo({center:venue.coordinates});}
      }
      applyInitialView();
      syncSelection();
      map.on('move',labelSides);
      let wasVisible=visible();
      observer=new ResizeObserver(()=>{if(!ready)return;const nowVisible=visible();if(nowVisible){map.resize();if(!initialView)applyInitialView();if(!wasVisible)syncSelection(true);labelSides();}wasVisible=nowVisible;});
      observer.observe(frame);
    });
  }catch(error){console.warn('Lineup map:',error.message);fail('Interactive map is unavailable.');}
}
syncSelection();start();
