// Behavioral checks for the optional helper; no browser or third-party packages.
const test = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname,'../js/event-navigation.js'),'utf8');

function setup({desktop=true,reduced=false,blockedStorage=false}={}) {
  const handlers={},frames=new Map(),store=new Map(),navigations=[],scrolls=[];
  let sequence=0;
  const results={scrollTop:350,addEventListener:(name,fn)=>{handlers['results:'+name]=fn;},contains:target=>target?.inside===true,scrollTo:options=>{results.scrollTop=options.top;}};
  const location={href:'http://127.0.0.1:4186/the-late-set.html#attendance',origin:'http://127.0.0.1:4186',pathname:'/the-late-set.html',assign:url=>navigations.push(url)};
  const history={state:null,replaceState:state=>{history.state=state;}};
  const window={scrollY:800,scrollTo:options=>{scrolls.push(options);if(options.behavior==='instant')window.scrollY=options.top;},addEventListener:(name,fn)=>{handlers[name]=fn;}};
  const context={window,document:{querySelector:()=>results},location,history,URL,Date,performance:{now:()=>0,getEntriesByType:()=>[{type:'navigate'}]},matchMedia:q=>({matches:q.includes('min-width')?desktop:reduced}),requestAnimationFrame:fn=>{frames.set(++sequence,fn);return sequence;},cancelAnimationFrame:id=>frames.delete(id),sessionStorage:{getItem:key=>{if(blockedStorage)throw Error('Disabled');return store.get(key)||null;},setItem:(key,value)=>{if(blockedStorage)throw Error('Disabled');store.set(key,value);},removeItem:key=>store.delete(key)}};
  vm.runInNewContext(source,context);
  function click(slug='ink-after-dark',extra={}) {
    const link={href:location.origin+'/'+slug+'.html',target:'',hasAttribute:()=>false};
    const event={target:{inside:true,closest:()=>link},button:0,defaultPrevented:false,preventDefault(){this.defaultPrevented=true;},...extra};
    handlers['results:click'](event);return event;
  }
  function frame(y,time=16) {
    window.scrollY=y;const fn=frames.values().next().value;frames.clear();if(fn)fn(time);
  }
  return {click,frame,window,results,history,handlers,navigations,scrolls,store,frames};
}

test('scrolled event selection waits for the CSS-driven return to top',()=>{
  const app=setup();assert.equal(app.click().defaultPrevented,true);
  assert.equal(app.scrolls[0].behavior,'auto');assert.equal(app.navigations.length,0);
  app.frame(420);assert.equal(app.navigations.length,0);
  app.frame(0,32);assert.equal(app.navigations[0],'http://127.0.0.1:4186/ink-after-dark.html');
  assert.equal(app.history.state.tideEventReturn.top,800);
  assert.equal(JSON.parse([...app.store.values()][0]).top,350);
});
test('modified clicks keep native new-tab navigation',()=>{
  const app=setup();assert.equal(app.click('ink-after-dark',{ctrlKey:true}).defaultPrevented,false);
  assert.equal(app.scrolls.length,0);assert.equal(app.history.state,null);
});
test('mobile and reduced-motion users have no delayed navigation',()=>{
  for(const options of [{desktop:false},{reduced:true}]) {
    const app=setup(options);assert.equal(app.click().defaultPrevented,false);assert.equal(app.scrolls.length,0);
  }
});
test('disabled session storage cannot block event navigation',()=>{
  const app=setup({blockedStorage:true});app.click();app.frame(0);
  assert.equal(app.navigations.length,1);
});
test('Escape cancels pending navigation and its scheduled frame',()=>{
  const app=setup();app.click();app.handlers.keydown({key:'Escape',target:{}});app.frame(0);
  assert.equal(app.navigations.length,0);assert.equal(app.frames.size,0);
});
test('the latest selection wins while the original return point is preserved',()=>{
  const app=setup();app.click();app.window.scrollY=200;app.click('desert-frequencies');app.frame(0);
  assert.equal(app.navigations[0],'http://127.0.0.1:4186/desert-frequencies.html');
  assert.equal(app.history.state.tideEventReturn.top,800);
});
test('Back restores the prior reading position and list scroll',()=>{
  const app=setup();app.click();app.frame(0);app.results.scrollTop=0;
  app.handlers.pageshow({persisted:true});app.frame(0);
  assert.equal(app.window.scrollY,800);assert.equal(app.results.scrollTop,350);
});
