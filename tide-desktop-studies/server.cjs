// Local study server. The approved app/kit is mounted read-only, never edited.
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const root = __dirname;
const base = fs.existsSync(path.join(root,'base')) ? path.join(root,'base') : path.resolve(root,'../tide-responsive-app');
const types = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.woff2':'font/woff2','.json':'application/json','.md':'text/plain; charset=utf-8','.zip':'application/zip'};
http.createServer((req,res) => {
  if (req.method !== 'GET' && req.method !== 'HEAD') { res.writeHead(405); res.end(); return; }
  let pathname;
  try { pathname=decodeURIComponent(new URL(req.url,'http://127.0.0.1').pathname); }
  catch { res.writeHead(400); res.end(); return; }
  if (pathname==='/favicon.ico') { res.writeHead(204); res.end(); return; }
  const mounted = pathname.startsWith('/base/');
  const parent = mounted ? base : root;
  const relative = mounted ? pathname.slice(6) : pathname==='/' ? 'index.html' : pathname.slice(1);
  const file=path.resolve(parent,relative);
  if (!file.startsWith(parent+path.sep)) { res.writeHead(403); res.end(); return; }
  fs.readFile(file,(error,data) => {
    if (error) { res.writeHead(404); res.end('Not found'); return; }
    res.writeHead(200,{'Content-Type':types[path.extname(file)] || 'application/octet-stream','Cache-Control':'no-cache','X-Content-Type-Options':'nosniff'});
    res.end(req.method==='HEAD' ? undefined : data);
  });
}).listen(4187,'127.0.0.1',()=>console.log('Wide Open desktop studies: http://127.0.0.1:4187/'));
