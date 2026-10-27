/* Local static preview of generated outputs. No dependencies or build service. */
const http=require('node:http');
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const root=path.resolve(__dirname,'../build');
const port=Number(process.env.PORT||4187);
const types={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.md':'text/plain; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.jpeg':'image/jpeg','.webp':'image/webp','.woff2':'font/woff2'};
http.createServer((req,res)=>{
  let url,pathname;try{url=new URL(req.url,'http://localhost');pathname=decodeURIComponent(url.pathname);}catch{res.writeHead(400);res.end('Bad request');return;}
  if(pathname==='/favicon.ico'){res.writeHead(204);res.end();return;}
  if(pathname==='/'){res.writeHead(302,{Location:'/site/index.html'});res.end();return;}
  // Preserve the last shared preview entry while users switch to stable URLs.
  if(pathname.startsWith('/app-release-1.1.0/')){res.writeHead(302,{Location:'/events/'+pathname.slice('/app-release-1.1.0/'.length)+url.search+url.hash});res.end();return;}
  let file=path.resolve(root,'.'+pathname);
  if(!file.startsWith(root+path.sep)){res.writeHead(403);res.end('Forbidden');return;}
  if(fs.existsSync(file)&&fs.statSync(file).isDirectory())file=path.join(file,'index.html');
  fs.readFile(file,(error,data)=>{
    if(error){res.writeHead(404);res.end('Not found. Run npm run build first.');return;}
    // Keep editable documents/styles fresh. Local fonts can be reused across
    // refreshes; a content validator handles revalidation after their fresh day.
    const font=path.extname(file)==='.woff2';
    const headers={'Content-Type':types[path.extname(file)]||'application/octet-stream','Cache-Control':font?'public, max-age=86400':'no-cache','X-Content-Type-Options':'nosniff'};
    if(font){
      headers.ETag='"'+crypto.createHash('sha256').update(data).digest('hex')+'"';
      if(req.headers['if-none-match']===headers.ETag){res.writeHead(304,headers);res.end();return;}
    }
    res.writeHead(200,headers);res.end(data);
  });
}).listen(port,'127.0.0.1',()=>console.log(`Tide UI: http://127.0.0.1:${port}/site/index.html | Events: /events/app/index.html`));
