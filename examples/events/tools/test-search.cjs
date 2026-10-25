const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const core=require('../src/runtime/js/search-core.js');
const manifest=JSON.parse(fs.readFileSync(path.join(__dirname,'../consumer-manifest.json'),'utf8'));
const cards=JSON.parse(fs.readFileSync(path.resolve(__dirname,'..',manifest.dataHome.events),'utf8'));
const state=query=>core.read(new URLSearchParams(query));
const matching=query=>cards.filter(card=>core.matches(card,state(query)));
let checks=0;function test(fn){fn();checks++;}
test(()=>assert.equal(cards.length,54));
test(()=>assert.equal(matching('').length,54));
test(()=>assert.equal(matching('venue=sunshine-theater').length,6));
test(()=>assert.equal(matching('venue=sunshine-theater&category=music').length,6));
test(()=>assert.equal(matching('venue=sunshine-theater&category=workshop').length,0));
test(()=>assert.equal(matching('venue=sunshine-theater&q=ink').length,0));
test(()=>assert.equal(matching('q=ink').length>0,true));
test(()=>assert.equal(matching('venue=sunshine-theater&q=Signal').length,1));
test(()=>assert.equal(matching('venue=sunshine-theater&from=2026-11-01').length,4));
test(()=>assert.equal(matching('venue=sunshine-theater&from=2026-10-30&to=2026-10-30').length,1));
test(()=>assert.equal(matching('venue=sunshine-theater&from=2026-12-01').length,0));
test(()=>assert.equal(core.serialize(state('venue=sunshine-theater&q=Signal')),'venue=sunshine-theater&q=Signal'));
test(()=>assert.equal(core.read(new URLSearchParams(),'sunshine-theater').venue,'sunshine-theater'));
test(()=>assert.equal(core.active(state('venue=sunshine-theater')),false));
test(()=>assert.equal(core.read(new URLSearchParams('venue=unknown')).venue,''));
test(()=>assert.equal(core.validRange(state('venue=sunshine-theater&from=2026-11-20&to=2026-11-01')),false));
console.log(`${checks} venue scope/search assertions passed.`);

