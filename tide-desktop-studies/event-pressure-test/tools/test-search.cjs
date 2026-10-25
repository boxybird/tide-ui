/* Behavioral assertions over the real authored fixtures and copied search core. */
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const root=path.resolve(__dirname,'..');
const search=require(path.join(root,'app/js/search-core.js'));
const events=JSON.parse(fs.readFileSync(path.join(root,'data/events.json'),'utf8'));
const run=q=>events.filter(e=>search.matches({date:e.date||'',endDate:e.endDate||e.date||'',category:e.category,search:e.title+' '+e.description+' '+e.venue},search.read(new URLSearchParams(q)))).map(e=>e.id).sort();
let checks=0;
function same(q,expected){assert.deepEqual(run(q),expected.sort(),q);checks++;}
same('',events.map(e=>e.id));
same('from=2026-11-01&to=2026-11-01',['across-months','all-day']);
same('from=2026-11-02&to=2026-11-02',['across-months','online-donation']);
same('from=2026-10-25&to=2026-10-25',['after-midnight','cancelled']);
same('from=2026-10-25&to=2026-10-25&category=workshop',['cancelled']);
same('from=2026-11-03&to=2026-11-03',['weekly-session']);
same('from=2026-11-04&to=2026-11-04',['rescheduled']);
same('from=2026-10-26&to=2026-10-26',[]);
same('from=2026-11-06&to=2026-11-06',['details-tba']);
same('q=found+sounds',['postponed']);
same('q=found+sounds&to=2026-12-01',[]);
same('q=record+shop&from=2026-01-01',[]);
same('from=2026-11-04&to=2026-11-01',[]);
same('q=zzzz-impossible-event',[]);
assert.equal(search.read(new URLSearchParams('from=2026-02-30')).from,'');checks++;
console.log(`${checks} date/search fixture assertions passed.`);
