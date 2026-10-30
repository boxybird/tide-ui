/* Local static preview only. Node is development tooling, never browser code. */
const http=require('node:http');
const fs=require('node:fs/promises');
const path=require('node:path');
const crypto=require('node:crypto');
const zlib=require('node:zlib');
const {promisify}=require('node:util');
const gzip=promisify(zlib.gzip),brotli=promisify(zlib.brotliCompress);
const types={'.mjs':'text/javascript; charset=utf-8','.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.json':'application/json; charset=utf-8','.md':'text/plain; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2'};
const textTypes=new Set(['.html','.css','.json','.md','.svg','.mjs']);

function encodingFor(header,compressible){
  if(!header)return 'identity';
  const weights=new Map(header.toLowerCase().split(',').map(item=>{
    const [name,...parameters]=item.trim().split(';');
    const q=parameters.find(p=>p.trim().startsWith('q='));
    const weight=q?Number(q.trim().slice(2)):1;
    return [name,Number.isFinite(weight)&&weight>=0&&weight<=1?weight:0];
  }));
  const weight=name=>weights.get(name)??weights.get('*')??0;
  const available=compressible?['br','gzip'].filter(name=>weight(name)>0):[];
  available.sort((a,b)=>weight(b)-weight(a));
  const identity=weights.get('identity')??(weights.get('*')===0?0:1);
  if(available.length&&(!weights.has('identity')||weight(available[0])>=identity))return available[0];
  return identity>0?'identity':null;
}

function createPreviewServer(root=path.resolve(__dirname,'../build')){
  root=path.resolve(root);
  return http.createServer(async(req,res)=>{
    if(!['GET','HEAD'].includes(req.method)){res.writeHead(405,{Allow:'GET, HEAD'});res.end();return;}
    let url,pathname;
    try{url=new URL(req.url,'http://localhost');pathname=decodeURIComponent(url.pathname);}catch{res.writeHead(400);res.end('Bad request');return;}
    if(pathname==='/favicon.ico'){res.writeHead(204);res.end();return;}
    if(pathname==='/'){res.writeHead(302,{Location:'/site/index.html'});res.end();return;}
    if(pathname.startsWith('/app-release-1.1.0/')){res.writeHead(302,{Location:'/events/'+pathname.slice('/app-release-1.1.0/'.length)+url.search+url.hash});res.end();return;}
    let file=path.resolve(root,'.'+pathname);
    if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end('Forbidden');return;}
    try{
      if((await fs.stat(file)).isDirectory())file=path.join(file,'index.html');
      // Resolve symlinks as well as URL paths before reading outside the build.
      if(!(await fs.realpath(file)).startsWith(root+path.sep)){res.writeHead(403);res.end('Forbidden');return;}
      const [data,stat]=await Promise.all([fs.readFile(file),fs.stat(file)]);
      const ext=path.extname(file).toLowerCase(),compressible=textTypes.has(ext)&&data.length>=512;
      const encoding=encodingFor(req.headers['accept-encoding'],compressible);
      if(!encoding){res.writeHead(406,{Vary:'Accept-Encoding'});res.end();return;}
      const payload=encoding==='br'?await brotli(data,{params:{[zlib.constants.BROTLI_PARAM_QUALITY]:4}}):encoding==='gzip'?await gzip(data):data;
      const headers={
        'Content-Type':types[ext]||'application/octet-stream',
        'Cache-Control':ext==='.woff2'?'public, max-age=86400':'no-cache',
        'X-Content-Type-Options':'nosniff',
        ETag:'"'+crypto.createHash('sha256').update(payload).digest('hex')+'"',
        'Last-Modified':stat.mtime.toUTCString(),
      };
      if(compressible)headers.Vary='Accept-Encoding';
      if(encoding!=='identity')headers['Content-Encoding']=encoding;
      const tags=req.headers['if-none-match'];
      const match=tags?tags.split(',').some(tag=>tag.trim()==='*'||tag.trim().replace(/^W\//,'')===headers.ETag):
        req.headers['if-modified-since']&&Date.parse(headers['Last-Modified'])<=Date.parse(req.headers['if-modified-since']);
      if(match){res.writeHead(304,headers);res.end();return;}
      headers['Content-Length']=payload.length;
      res.writeHead(200,headers);res.end(req.method==='HEAD'?undefined:payload);
    }catch(error){
      res.writeHead(error.code==='ENOENT'||error.code==='ENOTDIR'?404:500);
      res.end('Preview file unavailable. Run npm run build first.');
    }
  });
}

module.exports={createPreviewServer};
if(require.main===module){
  const port=Number(process.env.PORT||4187);
  createPreviewServer().listen(port,'127.0.0.1',()=>console.log(`Tide UI: http://127.0.0.1:${port}/site/index.html | Events: /events/app/index.html`));
}
