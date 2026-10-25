/* Host-only fixture states. Real HTML links are the fallback. No API, storage,
   PWA/offline service or user submissions are introduced by this study. */
(() => {
  'use strict';
  const results=document.getElementById('results');
  const feed=document.getElementById('pressure-feed');
  if(!results||!feed)return;
  const form=document.getElementById('event-search-form');
  const count=document.getElementById('result-count');
  const empty=document.getElementById('empty-results');
  const placeholder=document.getElementById('preview-state');
  const cards=[...feed.querySelectorAll('.tide-event-card')];
  const params=new URLSearchParams(location.search);
  let state=document.body.dataset.pressureState||'ready',busy=false;
  const isEvent=document.body.classList.contains('tide-app--event');
  const headingLevel=isEvent?1:2;
  const originalTitle=document.getElementById('event-title')?.textContent||'this event';
  const selected=cards.find(card=>card.classList.contains('tide-event-card--in-view'))||cards[0];
  const target=selected?.querySelector('.tide-event-card__link').href||'index.html';
  const loadingFeed=()=>state==='feed-loading'||state==='feed-failed';
  const status=document.createElement('p');status.className='tide-sr-only';status.setAttribute('role','status');status.setAttribute('aria-live','polite');status.setAttribute('aria-atomic','true');document.body.append(status);

  function element(tag,cls,text){const n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n;}
  function announce(text){status.textContent=text;}
  function appliedState(){return TideSearch.read(new URLSearchParams(location.search));}
  function countText(n){return n+' '+(n===1?'event':'events');}
  function action(label,href,kind){
    const a=element('a','tide-button tide-button--secondary',label);a.href=href;a.dataset.pressureRecover=kind;return a;
  }
  function showEmpty(title,description,link){
    empty.replaceChildren(element('h2','',title),element('p','',description));
    if(link)empty.append(link);
    empty.hidden=false;
  }
  function placeholderText(title,text){
    document.getElementById('event-detail').hidden=true;placeholder.hidden=false;
    document.getElementById('preview-state-title').textContent=title;
    document.getElementById('preview-state-description').textContent=text;
  }
  function syncDraft(){
    document.body.dataset.pressureState=state;
    window.dispatchEvent(new Event('pressure:state'));
  }
  function feedScene(){
    feed.hidden=true;results.setAttribute('aria-busy',String(state==='feed-loading'));
    count.textContent=state==='feed-loading'?'Loading events…':'Events unavailable';
    if(state==='feed-loading')showEmpty('Finding local events…','Your lineup is loading. We’ll show the results here as soon as they are ready.');
    else showEmpty('Events couldn’t load.','Your search choices are still here. Try loading the lineup again.',action('Try again','index.html','feed'));
    placeholderText('Your lineup comes first.','Choose an event once the results are available.');
    syncDraft();
  }
  function detailScene(){
    const detail=document.getElementById('event-detail');
    detail.hidden=false;placeholder.hidden=true;
    detail.setAttribute('aria-busy',String(state==='detail-loading'));
    const box=element('div','tide-empty tide-pressure__state');
    box.append(element('p','tide-eyebrow',state==='detail-loading'?'Opening event':'Event details unavailable'));
    const title=element('h'+headingLevel,'tide-pressure__state-title',state==='detail-loading'?'Opening this event…':'This event couldn’t load.');
    title.id='event-title';title.tabIndex=-1;box.append(title,element('p','',originalTitle));
    box.append(element('p','',state==='detail-loading'?'The lineup stays available while the event opens.':'Your lineup and filters are still here. Retry just this event.'));
    if(state==='detail-failed')box.append(action('Try again',target,'detail'));
    box.append(Object.assign(element('a','tide-link','Back to the lineup'),{href:'index.html'}));
    detail.replaceChildren(box);
    if(selected){selected.querySelector('.tide-event-card__status').textContent=state==='detail-loading'?'Opening…':'Couldn’t load';}
  }
  function cachedScene(){
    const wrapper=element('div','tide-pressure__feed-message');wrapper.id='pressure-feed-message';
    const note=element('div','tide-notice');note.append(element('strong','','Showing the last available copy'),element('p','','Updated at 9:10 AM. We couldn’t refresh it; event details may have changed.'),action('Try again','index.html','cached'));
    wrapper.append(note);feed.before(wrapper);
    const detail=document.getElementById('event-detail');
    const wrap=element('div','tide-pressure__detail-message');wrap.id='pressure-detail-message';
    const n=element('div','tide-notice');n.append(element('strong','','These details may be out of date.'),element('p','','Last checked today at 9:10 AM. Confirm current arrangements with the organizer before travelling.'));wrap.append(n);detail.prepend(wrap);
  }
  function initialize(){
    if(loadingFeed())feedScene();
    else if(state.startsWith('detail-'))detailScene();
    else if(state==='no-upcoming'&&!TideSearch.active(appliedState())){
      count.textContent='0 upcoming events';showEmpty('Nothing upcoming just yet.','There are no published events in this sample feed. There are no filters to clear.',Object.assign(element('a','tide-button tide-button--secondary','Check the lineup again'),{href:'no-upcoming.html'}));
      placeholderText('A little quiet today.','New events will appear here when there is something to browse.');syncDraft();
    }else if(state==='cached-copy')cachedScene();
    if(params.has('inspect')&&selected&&matchMedia('(width >= 60rem)').matches&&!loadingFeed()){
      // Case-review deep links expose the corresponding card in this bounded
      // list only. Ordinary navigation keeps the existing scroll restoration.
      const sticky=results.querySelector('.tide-slide-study__summary').getBoundingClientRect().height;
      const group=selected.closest('.tide-event-group').querySelector('header').getBoundingClientRect().height;
      const top=selected.getBoundingClientRect().top-results.getBoundingClientRect().top+results.scrollTop-sticky-group;
      results.scrollTo({top:Math.max(0,top),behavior:'instant'});
    }
    if(params.get('play')==='1'&&(state==='feed-loading'||state==='detail-loading'))setTimeout(()=>recover(state==='feed-loading'?'feed':'detail',null),1200);
  }
  async function recover(kind,trigger){
    if(busy)return;busy=true;
    trigger?.setAttribute('aria-disabled','true');
    try{
      if(kind==='feed'){
        state='feed-loading';feedScene();announce('Loading events.');
        await new Promise(resolve=>setTimeout(resolve,700));
        state='ready';feed.hidden=false;empty.hidden=cards.some(card=>!card.hidden);
        const total=cards.filter(card=>!card.hidden).length;count.textContent=countText(total);
        const detail=document.getElementById('event-detail');detail.hidden=false;placeholder.hidden=true;
        results.setAttribute('aria-busy','false');announce(countText(total)+' loaded.');
        if(trigger){count.tabIndex=-1;count.focus({preventScroll:true});}
        const url=new URL('index.html',location.href);url.search=TideSearch.serialize(appliedState());history.replaceState(history.state,'',url);
      }else{
        if(kind==='detail'){state='detail-loading';detailScene();}
        else document.getElementById('pressure-feed-message')?.setAttribute('aria-busy','true');
        announce('Loading event details.');
        const response=await fetch(target);if(!response.ok)throw new Error('Local sample unavailable');
        const doc=new DOMParser().parseFromString(await response.text(),'text/html');
        const source=doc.getElementById('event-detail');if(!source)throw new Error('Missing sample detail');
        const detail=document.importNode(source,true);
        if(!isEvent)detail.querySelectorAll('h1,h2,h3').forEach(h=>{const n=document.createElement('h'+(Number(h.tagName.slice(1))+1));for(const a of h.attributes)n.setAttribute(a.name,a.value);n.append(...h.childNodes);h.replaceWith(n);});
        document.getElementById('event-detail').replaceWith(detail);
        document.getElementById('pressure-feed-message')?.remove();state='ready';
        if(selected)selected.querySelector('.tide-event-card__status').textContent='In view';
        announce('Event details loaded.');
        if(trigger)detail.querySelector('#event-title')?.focus({preventScroll:true});
        const url=new URL(isEvent?target:'index.html',location.href);url.search=TideSearch.serialize(appliedState());history.replaceState(history.state,'',url);
      }
      syncDraft();document.getElementById('event-to').dispatchEvent(new Event('input',{bubbles:true}));
      window.dispatchEvent(new Event('tide:preview-ready'));
    }catch{
      if(kind==='feed'){state='feed-failed';feedScene();}
      else if(kind==='detail'){state='detail-failed';detailScene();}
      else{document.getElementById('pressure-feed-message')?.setAttribute('aria-busy','false');}
      announce('The sample could not load. Try again.');
    }finally{busy=false;}
  }
  document.addEventListener('click',event=>{
    const link=event.target.closest?.('[data-pressure-recover]');
    if(!link||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    event.preventDefault();recover(link.dataset.pressureRecover,link);
  });
  document.addEventListener('submit',event=>{if(loadingFeed()&&event.target===form){event.preventDefault();event.stopImmediatePropagation();announce('Load the events before applying the search.');}},true);
  document.addEventListener('DOMContentLoaded',()=>requestAnimationFrame(initialize),{once:true});
})();
