/* Isolated desktop composition. Original controls and GET navigation stay owned
   by the shared app. Only the column geometry and disclosure state live here. */
(() => {
  'use strict';
  const results=document.getElementById('results');
  const query=document.getElementById('event-search-form');
  const rail=document.getElementById('lineup-filters');
  if(!results||!query||!rail)return;
  const desktop=matchMedia('(min-width: 75rem)');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const trigger=results.querySelector('.tide-slide-study__trigger');
  const close=rail.querySelector('.tide-slide-study__close');
  const intro=results.querySelector('.tide-slide-study__intro');
  const filters=results.querySelector('.tide-app__filters');
  const actions=results.querySelector('.tide-app__filter-actions');
  const summary=results.querySelector('.tide-slide-study__summary');
  const badge=summary.querySelector('.tide-slide-study__applied');
  const controls=[intro,query,results.querySelector('.tide-app__filter-row'),filters];
  const slots=controls.map(node=>({node,marker:document.createComment('Lineup original control position')}));
  const actionMarker=document.createComment('Lineup original Apply position');
  const railMarker=document.createComment('Lineup original rail position');
  const resultsMarker=document.createComment('Lineup original results position');
  const storageKey='tide:margin-filters:'+document.body.dataset.width;
  let desiredOpen=false,mounted=false,originalOpen=false,browser,clip,scroller,dock,observer,lastRailFocus;
  try{desiredOpen=sessionStorage.getItem(storageKey)==='open';}catch{}
  if(new URLSearchParams(location.search).get('preview-filters')==='open'){
    desiredOpen=true;
    try{sessionStorage.setItem(storageKey,'open');}catch{}
  }
  const count=Number(Boolean(document.getElementById('event-from').value||document.getElementById('event-to').value))+filters.querySelectorAll('input[name="category"]:checked').length;
  badge.textContent='Filters · '+count;

  function returnIntro(){
    if(!mounted||desiredOpen)return;
    slots[0].marker.after(intro);intro.classList.add('tide-sr-only');
  }
  function finish(){
    if(!mounted)return;
    returnIntro();browser.classList.remove('tide-slide-study__browser--instant');
  }
  function setOpen(next,{focus=false,persist=true,immediate=false}={}){
    desiredOpen=next;
    if(persist)try{sessionStorage.setItem(storageKey,next?'open':'closed');}catch{}
    if(!mounted)return;
    if(!next&&(rail.contains(document.activeElement)||focus))trigger.focus({preventScroll:true});
    if(immediate)browser.classList.add('tide-slide-study__browser--instant');
    if(next){intro.classList.remove('tide-sr-only');scroller.prepend(intro);}
    clip.inert=!next;clip.setAttribute('aria-hidden',String(!next));
    browser.classList.toggle('tide-slide-study__browser--open',next);
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
    results.style.setProperty('--tide-slide-study-heading-height',height+'px');
  }
  trigger.addEventListener('click',()=>setOpen(!desiredOpen,{focus:true}));
  close.addEventListener('click',()=>setOpen(false,{focus:true}));
  rail.addEventListener('focusin',event=>{if(event.target!==close&&event.target!==rail)lastRailFocus=event.target;});
  document.addEventListener('keydown',event=>{if(mounted&&desiredOpen&&browser.contains(event.target)&&event.key==='Escape'){event.preventDefault();setOpen(false,{focus:true});}});
  document.addEventListener('invalid',event=>{
    if(mounted&&rail.contains(event.target)){filters.open=true;setOpen(true,{immediate:true});}
  },true);
  results.addEventListener('click',event=>{
    const link=event.target.closest?.('a.tide-event-group__jump');
    if(!mounted||!link||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    const url=new URL(link.href);
    if(url.origin!==location.origin||url.pathname!==location.pathname)return;
    const group=document.getElementById(decodeURIComponent(url.hash.slice(1)));
    if(!group||!results.contains(group))return;
    event.preventDefault();
    const top=group.getBoundingClientRect().top-results.getBoundingClientRect().top+results.scrollTop-results.clientTop-summary.getBoundingClientRect().height;
    group.querySelector('.tide-event-group__title')?.focus({preventScroll:true});
    results.scrollTo({top:Math.max(0,top),behavior:'auto'});
  }); // Runs after the shared helper, which also cancels any pending event navigation.
  function place(){
    if(desktop.matches===mounted)return;
    const active=document.activeElement;
    if(desktop.matches){
      const listOffset=results.scrollTop;originalOpen=filters.open;
      browser=document.createElement('div');browser.className='tide-slide-study__browser';
      clip=document.createElement('div');clip.className='tide-slide-study__rail-clip';
      rail.before(railMarker,browser);results.before(resultsMarker);
      clip.append(rail);
      if(document.body.dataset.slide==='left')browser.append(clip,results);else browser.append(results,clip);
      scroller=document.createElement('div');scroller.className='tide-filter-panel__body';
      scroller.tabIndex=0;scroller.setAttribute('role','region');scroller.setAttribute('aria-label','Filter options');
      dock=document.createElement('div');dock.className='tide-filter-panel__footer';
      controls.forEach((node,index)=>{node.before(slots[index].marker);scroller.append(node);});
      actions.before(actionMarker);dock.append(actions);rail.append(scroller,dock);
      rail.classList.add('tide-filter-panel','tide-filter-panel--rail');rail.hidden=false;close.hidden=false;trigger.hidden=false;badge.hidden=!count;filters.open=true;
      mounted=true;document.body.classList.add('tide-slide-study--mounted');
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
      results.style.removeProperty('--tide-slide-study-heading-height');
      document.body.classList.remove('tide-slide-study--mounted');mounted=false;
      browser=clip=scroller=dock=null;
      const target=hadLauncherFocus||focusedScroller||active===close||active===rail||hadRailFocus&&filters.contains(active)&&!filters.open?filters.querySelector('summary'):active;
      if(target?.isConnected&&target!==document.body)target.focus({preventScroll:true});
    }
  }
  reduced.addEventListener('change',()=>{if(mounted&&reduced.matches)finish();});
  desktop.addEventListener('change',place);place();
})();
