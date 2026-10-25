import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const studies=JSON.parse(fs.readFileSync(path.join(root,'studies.json'),'utf8'));
const hex=c=>[1,3,5].map(i=>parseInt(c.slice(i,i+2),16));
const lin=n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;};
const lum=c=>{const [r,g,b]=Array.isArray(c)?c:hex(c);return .2126*lin(r)+.7152*lin(g)+.0722*lin(b);};
const ratio=(a,b)=>{const [light,dark]=[lum(a),lum(b)].sort((a,b)=>b-a);return (light+.05)/(dark+.05);};
const metrics=JSON.parse(fs.readFileSync(path.join(root,'qa/browser-metrics-390.json'),'utf8'));
const stops=[[0,.22],[.28,.03],[.38,.10],[.50,.80],[.62,.93],[.79,.98],[1,1]];
const alphaAt=y=>{for(let i=1;i<stops.length;i++){if(y<=stops[i][0]){const[a0,v0]=stops[i-1],[a1,v1]=stops[i];return v0+(v1-v0)*(y-a0)/(a1-a0);}}return 1;};
let failed=false;
const results=studies.map(s=>{
  const metric=metrics.find(m=>m.study===s.id&&m.kind.includes('event'));
  const alpha=alphaAt(metric.categoryY/metric.hero);
  // Conservative white photographic pixel under the first text line. The real
  // selected photo is darker. This checks the design’s scrim, not image luck.
  const worst=[8,12,14].map(n=>255*(1-alpha)+n*alpha);
  const checks={title:ratio(s.text,s.panel),secondary:ratio(s.muted,s.panel),label:ratio(s.label,s.panel),accent:ratio(s.accent,s.panel),action:ratio('#211a13',s.accent),photoEyebrowWorstWhite:ratio(s.accent,worst)};
  const pass=Object.values(checks).every(x=>x>=4.5);
  if(!pass)failed=true;
  return {study:s.id,name:s.name,checks,pass,photoScrimAlphaAtFirstText:alpha};
});
fs.writeFileSync(path.join(root,'qa/contrast-results.json'),JSON.stringify(results,null,2));
console.log(results.map(r=>`${r.study} ${r.name}: ${r.pass?'PASS':'FAIL'}; lowest ${Math.min(...Object.values(r.checks)).toFixed(2)}:1`).join('\n'));
if(failed)process.exitCode=1;
