import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const studies=JSON.parse(fs.readFileSync(path.join(root,'studies.json'),'utf8'));
const hex=c=>[1,3,5].map(i=>parseInt(c.slice(i,i+2),16));
const lin=n=>{n/=255;return n<=.04045?n/12.92:((n+.055)/1.055)**2.4;};
const lum=c=>{const [r,g,b]=Array.isArray(c)?c:hex(c);return .2126*lin(r)+.7152*lin(g)+.0722*lin(b);};
const ratio=(a,b)=>{const [light,dark]=[lum(a),lum(b)].sort((a,b)=>b-a);return (light+.05)/(dark+.05);};
// A white photographic pixel behind the first line, ignoring the additional
// photo-shade layer. The content-anchored scrim alone contributes 94% warm ink.
const worst=[22,21,18].map(n=>255*.06+n*.94);
const results=studies.map(s=>{
  const checks={primary:ratio(s.text,s.panel),secondary:ratio(s.muted,s.panel),label:ratio(s.label,s.panel),accent:ratio(s.accent,s.panel),tertiary:ratio(s.tertiary,s.bg),photoEyebrowWorstWhite:ratio(s.accent,worst),photoSecondaryWorstWhite:ratio(s.muted,worst)};
  return {study:s.id,name:s.name,checks,pass:Object.values(checks).every(n=>n>=4.5)};
});
fs.writeFileSync(path.join(root,'qa/contrast-results.json'),JSON.stringify(results,null,2));
console.log(results.map(s=>`${s.study} ${s.name}: ${s.pass?'PASS':'FAIL'}; minimum ${Math.min(...Object.values(s.checks)).toFixed(2)}:1`).join('\n'));
if(results.some(s=>!s.pass))process.exitCode=1;
