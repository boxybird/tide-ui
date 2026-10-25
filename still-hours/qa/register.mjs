/* Record the user's actual feedback and this completed collection. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const research=path.join(path.dirname(root),'research');
const file=path.join(research,'design-sets.json');
const registry=JSON.parse(fs.readFileSync(file,'utf8'));
const studies=JSON.parse(fs.readFileSync(path.join(root,'studies.json'),'utf8'));
const quiet=registry.sets.find(s=>s.name==='Quiet Studies');
if(quiet){
  quiet.status='Completed and reviewed by the user. User likes the subtle differences across the six; no individual favorite specified.';
  quiet.feedback='User: "I really like these" and says the subtle differences are exactly what was asked for. Requests another dark family, distinct from this family, with six subtle variations within itself. No numbered favorite specified.';
}
const newSet={name:'Still Hours',description:'A second dark static HTML/CSS family: warm charcoal, serif-first hierarchy, a date rail, continuous ruled cards and outlined price/action row. Six subtle optical refinements within one distinctive composition.',status:'Completed and browser-reviewed; awaiting user review. No favorite assumed.',kind:'static_html',started:'2026-10-21',completed:'2026-10-21',source:'Quiet Studies / Ink After Dark concept, with the same event content and workshop photo.',comparison:'../still-hours/index.html',archive:'../still-hours/still-hours.zip',options:studies.map(s=>({number:Number(s.id),name:s.name,file:`../still-hours/${s.id}-${s.slug}.html`,fonts:s.font})),preferred_options:[],feedback:'User requested a second set of six dark refinements. The six should differ subtly from one another while being clearly distinctive from the original six.'};
const existing=registry.sets.findIndex(s=>s.name==='Still Hours');
if(existing>=0)registry.sets[existing]=newSet;else registry.sets.push(newSet);
registry.preferences.current_constraint='Two named families of six static HTML/CSS refinements of Ink After Dark: Quiet Studies and Still Hours. Preserve the original six. The second family should be clearly distinctive from the first while keeping its own six variations subtle. Keep dark aesthetics, deliberate type/spacing/hierarchy and browser-reviewed mobile list/detail pairs. No browser JavaScript or full app.';
fs.writeFileSync(file,JSON.stringify(registry,null,2)+'\n');
const notes=path.join(research,'source-notes.txt');
const marker='2026-10-21 — Still Hours (twelfth set)';
if(!fs.readFileSync(notes,'utf8').includes(marker))fs.appendFileSync(notes,`\n\nPREFERENCE UPDATE: User likes Quiet Studies as a whole, especially the subtle differences. No individual numbered preference was given.\n\n${marker}\nUser requested another coherent dark family, with six small internal variations and a clear family-level difference from Quiet Studies. Delivered still-hours/index.html, six pair pages, twelve phone frames, local assets, design notes and still-hours.zip; preview port4176. Original collection unchanged.\nNew family uses warm charcoal, Fraunces/Lora/Literata serif names, a date rail, continuous ruled full-width entries, fine CSS diagonal texture and an outlined action beside price. The exact same workshop photo and event content support direct comparisons.\nPrimary type references inspected: https://github.com/undercasetype/Fraunces (variable axes), https://cyreal.org/fonts/lora/ (calligraphic construction), https://www.typetogether.com/fonts/literata (screen-reading origins). Typefaces provided by official Fontsource npm packages, self-hosted with OFL licenses. Existing local Radix icon exports reused. No new photographic assets generated.\nAll12 phone frames checked at390x844 and320/430 widths, six event openings at390x667, gallery at1440/960/768/436/320. No text clipping or horizontal overflow. Content-anchored94% scrim ensures predictable first-text contrast on short screens.42 targeted text checks, minimum7.10:1.20 HTML documents, zero browser scripts,7 local fonts,61 ZIP entries, CRC clean. Notes/evidence under still-hours/qa and design-qa.md. No user favorite assumed.\n`);
console.log('Recorded Quiet Studies feedback and Still Hours as set twelve.');
