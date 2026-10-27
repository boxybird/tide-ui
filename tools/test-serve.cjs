/* HTTP integration tests for local Node tooling; never shipped to browsers. */
const {test}=require('node:test');
const assert=require('node:assert/strict');
const http=require('node:http');
const fs=require('node:fs/promises');
const os=require('node:os');
const path=require('node:path');
const {gunzipSync,brotliDecompressSync}=require('node:zlib');
const {createPreviewServer}=require('./serve.cjs');

test('native preview HTTP contracts',async t=>{
  const root=await fs.mkdtemp(path.join(os.tmpdir(),'tide-preview-'));
  const original=Buffer.from('<!doctype html><p>Unchanged UI and native HTML.</p>'.repeat(80));
  await fs.writeFile(path.join(root,'page.html'),original);
  await fs.writeFile(path.join(root,'style.css'),'body { color: inherit; }'.repeat(80));
  const binary=Buffer.from([0,1,2,255,127]);
  await fs.writeFile(path.join(root,'photo.webp'),binary);
  await fs.writeFile(path.join(root,'font.woff2'),binary);
  const server=createPreviewServer(root);
  await new Promise((resolve,reject)=>{server.once('error',reject);server.listen(0,'127.0.0.1',resolve);});
  t.after(async()=>{await new Promise(resolve=>server.close(resolve));await fs.rm(root,{recursive:true,force:true});});
  function request(url='/page.html',headers={},method='GET'){
    return new Promise((resolve,reject)=>{
      const req=http.request({hostname:'127.0.0.1',port:server.address().port,path:url,headers,method},res=>{
        const chunks=[];res.on('data',chunk=>chunks.push(chunk));res.on('end',()=>resolve({status:res.statusCode,headers:res.headers,body:Buffer.concat(chunks)}));
      });req.on('error',reject);req.end();
    });
  }
  await t.test('Brotli and gzip preserve the exact document bytes',async()=>{
    for(const [name,decode] of [['br',brotliDecompressSync],['gzip',gunzipSync]]){
      const response=await request('/page.html',{'Accept-Encoding':name});
      assert.equal(response.status,200);assert.equal(response.headers['content-encoding'],name);
      assert.equal(response.headers.vary,'Accept-Encoding');assert.deepEqual(decode(response.body),original);
      assert.ok(response.body.length<original.length/2);
    }
    assert.deepEqual((await request()).body,original);
  });
  await t.test('negotiation respects quality, refusal and identity',async()=>{
    for(const [accept,encoding] of [['br;q=0.2, gzip;q=1','gzip'],['br;q=0,gzip;q=0',undefined],['gzip;q=0.5,identity;q=1',undefined],['*;q=1','br']]){
      assert.equal((await request('/page.html',{'Accept-Encoding':accept})).headers['content-encoding'],encoding);
    }
    assert.equal((await request('/page.html',{'Accept-Encoding':'br;q=0,gzip;q=0,identity;q=0'})).status,406);
  });
  await t.test('validators are representation-specific and support weak/list matching',async()=>{
    const plain=await request(),compressed=await request('/page.html',{'Accept-Encoding':'gzip'});
    assert.notEqual(plain.headers.etag,compressed.headers.etag);
    const hit=await request('/page.html',{'If-None-Match':'"old", W/'+plain.headers.etag});
    assert.equal(hit.status,304);assert.equal(hit.body.length,0);
    assert.equal((await request('/page.html',{'If-None-Match':plain.headers.etag,'Accept-Encoding':'gzip'})).status,200);
    assert.equal((await request('/page.html',{'If-Modified-Since':plain.headers['last-modified']})).status,304);
    assert.equal((await request('/page.html',{'If-None-Match':'"miss"','If-Modified-Since':plain.headers['last-modified']})).status,200);
  });
  await t.test('CSS and binary assets revalidate; only fonts have a freshness lifetime',async()=>{
    for(const file of ['/style.css','/photo.webp','/font.woff2']){
      const response=await request(file,{'Accept-Encoding':'br,gzip'});
      assert.equal(response.headers['cache-control'],file.endsWith('woff2')?'public, max-age=86400':'no-cache');
      assert.equal((await request(file,{'Accept-Encoding':'br,gzip','If-None-Match':response.headers.etag})).status,304);
      if(file!='/style.css'){assert.equal(response.headers['content-encoding'],undefined);assert.deepEqual(response.body,binary);}
    }
  });
  await t.test('HEAD has the same representation headers with no body',async()=>{
    const get=await request('/page.html',{'Accept-Encoding':'br'}),head=await request('/page.html',{'Accept-Encoding':'br'},'HEAD');
    assert.equal(head.status,200);assert.equal(head.body.length,0);
    for(const key of ['etag','content-length','content-encoding','content-type'])assert.equal(head.headers[key],get.headers[key]);
  });
  await t.test('source edits invalidate compressed and uncompressed validators immediately',async()=>{
    const before=await request('/page.html',{'Accept-Encoding':'gzip'});
    const changed=Buffer.concat([original,Buffer.from('<p>Fresh edit.</p>')]);
    await fs.writeFile(path.join(root,'page.html'),changed);
    const after=await request('/page.html',{'Accept-Encoding':'gzip','If-None-Match':before.headers.etag});
    assert.equal(after.status,200);assert.notEqual(after.headers.etag,before.headers.etag);assert.deepEqual(gunzipSync(after.body),changed);
  });
});
