/* Desktop browsing composition: relocate the original controls into the rail,
   preserve GET navigation and measure the permanent summary for month jumps. */
(() => {
  'use strict';
  const results=document.getElementById('results');
  const query=document.getElementById('event-search-form');
  const rail=document.getElementById('lineup-filters');
  if(!results||!query||!rail)return;
  const desktop=TideApp.media('desktop');
  const reduced=TideApp.media('reducedMotion');
  const trigger=results.querySelector('.tide-app__filter-toggle');
  const close=rail.querySelector('.tide-app__filter-close');
  const intro=results.querySelector('.tide-app__intro');
  const filters=results.querySelector('.tide-app__filters');
  const actions=results.querySelector('.tide-app__filter-actions');
  const summary=results.querySelector('.tide-lineup__summary');
  const badge=summary.querySelector('.tide-app__applied-filters');
  const controls=[intro,query,results.querySelector('.tide-app__filter-row'),filters];
  const slots=controls.map(node=>({node,marker:document.createComment('Lineup original control position')}));
  const actionMarker=document.createComment('Lineup original Apply position');
  const railMarker=document.createComment('Lineup original rail position');
  const resultsMarker=document.createComment('Lineup original results position');
  const storageKey=TideApp.keys.rail(document.body.dataset.stateKey);
  let desiredOpen=false,mounted=false,originalOpen=false,browser,clip,scroller,dock,observer,lastRailFocus;
  desiredOpen=TideApp.storage.get(storageKey)==='open';
  if(new URLSearchParams(location.search).get('preview-filters')==='open'){
    desiredOpen=true;
    TideApp.storage.set(storageKey,'open');
  }
  const count=TideSearch.refinementCount(TideApp.appliedState());
  badge.textContent='Filters · '+count;

  function returnIntro(){
    if(!mounted||desiredOpen)return;
    slots[0].marker.after(intro);intro.classList.add('tide-sr-only');
  }
  function finish(){
    if(!mounted)return;
    returnIntro();browser.classList.remove('tide-app__browse--instant');
  }
  function setOpen(next,{focus=false,persist=true,immediate=false}={}){
    desiredOpen=next;
    if(persist)TideApp.storage.set(storageKey,next?'open':'closed');
    if(!mounted)return;
    if(!next&&(rail.contains(document.activeElement)||focus))trigger.focus({preventScroll:true});
    if(immediate)browser.classList.add('tide-app__browse--instant');
    if(next){intro.classList.remove('tide-sr-only');scroller.prepend(intro);}
    clip.inert=!next;clip.setAttribute('aria-hidden',String(!next));
    browser.classList.toggle('tide-app__browse--filters-open',next);
    trigger.setAttribute('aria-expanded',String(next));
    const label=(next?'Hide':'Show')+' search and filters'+(count?' · '+count+' applied':'');
    trigger.setAttribute('aria-label',label);trigger.title=label;
    if(next&&focus){
      const target=lastRailFocus?.isConnected&&rail.contains(lastRailFocus)?lastRailFocus:document.getElementById('event-query');
      target.focus({preventScroll:true});
    }
    if(immediate||reduced.matches){returnIntro();requestAnimationFrame(finish);}
  }
  function measure(){
    if(!mounted)return;
    const height=summary.getBoundingClientRect().height;
    results.style.setProperty('--tide-lineup-summary-height',height+'px');
  }
  trigger.addEventListener('click',()=>setOpen(!desiredOpen,{focus:true}));
  close.addEventListener('click',()=>setOpen(false,{focus:true}));
  rail.addEventListener('focusin',event=>{if(event.target!==close&&event.target!==rail)lastRailFocus=event.target;});
  document.addEventListener('keydown',event=>{if(mounted&&desiredOpen&&browser.contains(event.target)&&event.key==='Escape'){event.preventDefault();setOpen(false,{focus:true});}});
  document.addEventListener('invalid',event=>{
    if(mounted&&rail.contains(event.target)){filters.open=true;setOpen(true,{immediate:true});}
  },true);
  function place(){
    if(desktop.matches===mounted)return;
    const active=document.activeElement;
    if(desktop.matches){
      const listOffset=results.scrollTop;originalOpen=filters.open;
      browser=document.createElement('div');browser.className='tide-app__browse';
      clip=document.createElement('div');clip.className='tide-app__filter-clip';
      rail.before(railMarker,browser);results.before(resultsMarker);
      clip.append(rail);
      browser.append(clip,results);
      scroller=document.createElement('div');scroller.className='tide-filter-panel__body';
      scroller.tabIndex=0;scroller.setAttribute('role','region');scroller.setAttribute('aria-label','Filter options');
      dock=document.createElement('div');dock.className='tide-filter-panel__footer';
      controls.forEach((node,index)=>{node.before(slots[index].marker);scroller.append(node);});
      actions.before(actionMarker);dock.append(actions);rail.append(scroller,dock);
      rail.classList.add('tide-filter-panel','tide-filter-panel--rail');rail.hidden=false;close.hidden=false;trigger.hidden=false;badge.hidden=!count;filters.open=true;
      mounted=true;document.body.classList.add('tide-app--desktop');
      browser.addEventListener('transitionend',event=>{if(event.target===browser&&event.propertyName==='grid-template-columns')finish();});
      setOpen(desiredOpen,{persist:false,immediate:true});
      observer=new ResizeObserver(measure);observer.observe(summary);measure();
      results.scrollTo({top:listOffset,behavior:'instant'});
    }else{
      const hadRailFocus=rail.contains(active);const hadLauncherFocus=active===trigger;const focusedScroller=active===scroller;
      observer?.disconnect();clip.inert=false;clip.removeAttribute('aria-hidden');
      actionMarker.replaceWith(actions);
      slots.forEach(({node,marker})=>marker.replaceWith(node));
      intro.classList.remove('tide-sr-only');filters.open=originalOpen;
      scroller.remove();dock.remove();railMarker.replaceWith(rail);resultsMarker.replaceWith(results);browser.remove();
      rail.classList.remove('tide-filter-panel','tide-filter-panel--rail');rail.hidden=true;close.hidden=true;trigger.hidden=true;badge.hidden=true;
      results.style.removeProperty('--tide-lineup-summary-height');
      document.body.classList.remove('tide-app--desktop');mounted=false;
      browser=clip=scroller=dock=null;
      const target=hadLauncherFocus||focusedScroller||active===close||active===rail||hadRailFocus&&filters.contains(active)&&!filters.open?filters.querySelector('summary'):active;
      if(target?.isConnected&&target!==document.body)target.focus({preventScroll:true});
    }
  }
  reduced.addEventListener('change',()=>{if(mounted&&reduced.matches)finish();});
  desktop.addEventListener('change',place);place();
})();
