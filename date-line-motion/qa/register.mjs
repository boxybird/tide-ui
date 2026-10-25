import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const research = path.join(path.dirname(root),'research');
const registryPath = path.join(research,'design-sets.json');
const registry = JSON.parse(fs.readFileSync(registryPath,'utf8'));
const study = {
  name:'Date Line — Continuity',
  description:'An isolated HTML/CSS/vanilla-JavaScript prototype of native bidirectional View Transitions over the selected Date Line design.',
  status:'Completed and browser-reviewed; awaiting user motion preference. Date Line remains the overall favorite.',
  kind:'interactive_html',
  started:'2026-10-21',
  completed:'2026-10-21',
  source:'Quiet Assembly 01 Date Line; exact resting list and Ink After Dark opening retained.',
  comparison:'../date-line-motion/index.html',
  standalone:'../date-line-motion/app.html',
  archive:'../date-line-motion/date-line-continuity.zip',
  options:[
    {number:1,name:'Linked details',file:'../date-line-motion/app.html?motion=linked',changes:'Surface, title, category, date parts, start time, venue and price use named native snapshots.'},
    {number:2,name:'Title only',file:'../date-line-motion/app.html?motion=title',changes:'Only the title travels between views; remaining content dissolves.'},
    {number:3,name:'Soft dissolve',file:'../date-line-motion/app.html?motion=dissolve',changes:'Whole-view native crossfade for comparison.'}
  ],
  preferred_options:[],
  feedback:'User requests a prototype focused on the View Transition API, with title/date/time moving from the card into the individual event and back. Preserve all approved studies.',
  controls:'Slow motion at 2400ms; original or rough organizer photo. Controls live outside the phone.',
  validation:'390x844 resting list and Ink event are pixel equal to fresh source captures; actual native intermediate frames inspected; Back/Forward/Escape, scroll/focus return, direct links, saved state and direct fallback verified. See design-qa.md for console/tooling and device-test limits.'
};
const index = registry.sets.findIndex(set => set.name === study.name);
if (index < 0) registry.sets.push(study); else registry.sets[index] = study;
registry.preferences.current_constraint = 'Preserve Date Line and all practical studies. Explore native View Transition movement in the isolated date-line-motion prototype without changing the approved resting layout.';
registry.preferences.selected_direction.next = 'Iterate movement in Date Line — Continuity based on user feedback; preserve the Date Line visual baseline.';
fs.writeFileSync(registryPath,JSON.stringify(registry,null,2)+'\n');
const notes = '\n\n2026-10-21 — Date Line Continuity (fifteenth study)\nUser explicitly requested an interactive prototype focused on native View Transition movement from card title/date/time into full-screen event details and back. New isolated folder date-line-motion; preview4179. Earlier studies untouched, Date Line remains the favorite overall.\nThree comparison modes: Linked details, Title only, Soft dissolve; slow-motion and original/rough-photo controls outside the app. All three events open; Back/Forward/Escape, direct links, scroll/focus return and local saved state work. Natural480ms linked/title,280ms dissolve,2400ms slow. Title-off-screen return uses a dissolve. Native snapshots, not a FLIP substitute or glyph-outline interpolation.\nFresh390x844 source/implementation comparisons: zero changed pixels in both resting list and Ink opening. Intermediate native animations captured at elapsed-time checkpoints; title ghosting, photo layering, date/venue collisions, forward hash and short desktop preview cropping corrected.42 approved hash checks pass. No new assets generated; existing photos, texture, fonts and Radix SVGs reused.45-file portable archive, CRC clean. Primary implementation docs: MDN View Transition API/Using and view-transition-name, Chrome Developers same-document View Transitions.\nQA records empty standalone console and an apparent browser-tool iframe MutationObserver diagnostic in the workbench; page-error listener remains empty. Physical-device, additional-browser and OS media-emulation checks remain follow-ups. No motion mode has been selected as a new favorite.\n';
const sourceNotes = path.join(research,'source-notes.txt');
if (!fs.readFileSync(sourceNotes,'utf8').includes('Date Line Continuity (fifteenth study)')) fs.appendFileSync(sourceNotes,notes);
console.log('Recorded Continuity without changing the Date Line favorite.');
