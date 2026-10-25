/* One set of controls, two responsive placements. The approved desktop adapter
   remains untouched and takes ownership at75rem. Native details is the fallback. */
(() => {
  'use strict';
  const dialog=document.getElementById('responsive-filters');
  const form=document.getElementById('event-search-form');
  if(!dialog||!form||typeof dialog.showModal!=='function'||typeof TideSearch==='undefined')return;
  const small=matchMedia('(width < 75rem)');
  const filters=document.querySelector('.tide-app__filters');
  const fields=filters.querySelector('.tide-app__filter-form');
  const actions=fields.querySelector('.tide-app__filter-actions');
  const apply=actions.querySelector('button[type="submit"]');
  const launcher=document.querySelector('.tide-responsive-filters__trigger');
  const body=dialog.querySelector('.tide-responsive-filters__body');
  const footer=dialog.querySelector('.tide-responsive-filters__footer');
  const title=dialog.querySelector('.tide-responsive-filters__title');
  const close=dialog.querySelector('[data-filter-close]');
  const reset=dialog.querySelector('[data-filter-reset]');
  const counter=dialog.querySelector('.tide-responsive-filters__count');
  const description=dialog.querySelector('.tide-responsive-filters__description');
  const controls=[...fields.querySelectorAll('input')];
  const from=document.getElementById('event-from');
  const to=document.getElementById('event-to');
  const cards=[...document.querySelectorAll('#results .tide-event-card')];
  const fieldMarker=document.createComment('Original responsive filter content');
  const applyMarker=document.createComment('Original Apply location');
  const applyText=apply.textContent;
  const wasSecondary=apply.classList.contains('tide-button--secondary');
  const returnKey='tide:responsive-filters:applied';
  let mounted=false,snapshot=null,committing=false;

  function values(){return controls.map(input=>({value:input.value,checked:input.checked}));}
  function restore(){
    if(!snapshot)return;
    controls.forEach((input,index)=>{input.value=snapshot[index].value;input.checked=snapshot[index].checked;});
    to.dispatchEvent(new Event('input',{bubbles:true}));
  }
  function state(){return TideSearch.read(new URLSearchParams(new FormData(form)));}
  function update(){
    if(!mounted)return;
    const next=state();
    const valid=TideSearch.validRange(next);
    const total=valid?cards.filter(card=>TideSearch.matches(card.dataset,next)).length:0;
    counter.textContent=valid?total+' matching '+(total===1?'event':'events'):'Check the date range';
    apply.textContent=valid?'Show '+total+' '+(total===1?'event':'events'):'Check dates';
    reset.disabled=!next.from&&!next.to&&!next.categories.length;
  }
  function dismiss(){
    if(!dialog.open)return;
    committing=false;restore();dialog.close('cancel');
  }
  function open(){
    if(!mounted||dialog.open)return;
    committing=false;snapshot=values();update();
    const query=document.getElementById('event-query').value.trim();
    description.textContent=query?'Narrow results for “'+query+'”. Changes apply together.':'Choose dates and categories. Changes apply together.';
    dialog.showModal();launcher.setAttribute('aria-expanded','true');
    body.scrollTop=0;title.focus({preventScroll:true});
  }
  function mount(){
    if(mounted||!small.matches)return;
    fields.before(fieldMarker);apply.before(applyMarker);
    body.append(fields);footer.append(apply);
    fields.classList.add('tide-responsive-filters__fields');
    apply.classList.add('tide-responsive-filters__apply');
    apply.classList.remove('tide-button--secondary');
    actions.hidden=true;filters.hidden=true;launcher.hidden=false;mounted=true;
    const count=Number(Boolean(from.value||to.value))+controls.filter(input=>input.type==='checkbox'&&input.checked).length;
    launcher.querySelector('span').textContent=count?'Filters · '+count:'Filters';
    update();
  }
  function unmount(){
    if(!mounted)return;
    const active=document.activeElement;
    const wasOpen=dialog.open;
    if(wasOpen){committing=false;restore();dialog.close('resize');}
    fieldMarker.replaceWith(fields);applyMarker.replaceWith(apply);
    fields.classList.remove('tide-responsive-filters__fields');
    apply.classList.remove('tide-responsive-filters__apply');
    apply.classList.toggle('tide-button--secondary',wasSecondary);apply.textContent=applyText;
    actions.hidden=false;filters.hidden=false;launcher.hidden=true;
    launcher.setAttribute('aria-expanded','false');mounted=false;
    // The existing desktop adapter will mount after this resize listener.
    if(wasOpen||active===launcher)document.getElementById('results').focus({preventScroll:true});
  }

  launcher.addEventListener('click',open);
  close.addEventListener('click',dismiss);
  dialog.addEventListener('cancel',event=>{event.preventDefault();dismiss();});
  dialog.addEventListener('close',()=>{
    launcher.setAttribute('aria-expanded','false');
    if(mounted&&!committing)launcher.focus({preventScroll:true});
  });
  dialog.addEventListener('input',update);
  dialog.addEventListener('change',update);
  // Keep keyboard traversal in the task even in hosts that otherwise send Tab
  // from the last control to browser chrome. Native modal inertness does the rest.
  dialog.addEventListener('keydown',event=>{
    if(event.key!=='Tab')return;
    const stops=[...dialog.querySelectorAll('button,input,select,textarea,a[href],[tabindex="0"]')]
      .filter(node=>!node.disabled&&node.getClientRects().length);
    const first=stops[0],last=stops.at(-1),active=document.activeElement;
    if(event.shiftKey&&(active===first||active===title)){event.preventDefault();last?.focus();}
    else if(!event.shiftKey&&active===last){event.preventDefault();first?.focus();}
  });
  reset.addEventListener('click',()=>{
    from.value='';to.value='';controls.filter(input=>input.type==='checkbox').forEach(input=>{input.checked=false;});
    to.dispatchEvent(new Event('input',{bubbles:true}));update();
  });
  form.addEventListener('submit',()=>{
    if(!mounted||!dialog.open)return;
    committing=true;
    const next=new URL(form.action,location.href);next.search=TideSearch.serialize(state());
    try{sessionStorage.setItem(returnKey,next.href);}catch{}
    dialog.close('apply');
  },true);

  // Register before the unchanged desktop adapter: restore our nodes first when
  // entering desktop. When leaving desktop, mount after that adapter restores them.
  small.addEventListener('change',()=>{if(!small.matches)unmount();else requestAnimationFrame(mount);});
  // Deferred scripts capture the original nodes before DOMContentLoaded. Mount
  // afterward, so the desktop adapter always holds valid references on resize.
  document.addEventListener('DOMContentLoaded',mount,{once:true});
  window.addEventListener('pageshow',()=>{
    if(small.matches)requestAnimationFrame(mount);
    let returned=false;
    try{returned=sessionStorage.getItem(returnKey)===location.href;if(returned)sessionStorage.removeItem(returnKey);}catch{}
    if(returned&&small.matches)requestAnimationFrame(()=>{
      const count=document.getElementById('result-count');count.tabIndex=-1;count.focus({preventScroll:true});
      document.querySelector('.tide-slide-study__summary').scrollIntoView({block:'start',behavior:'instant'});
    });
  });
})();
