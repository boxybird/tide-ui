/* Browse-first composition. One original GET form/control set, restored before
   the frozen desktop adapter takes over. Native details remains the fallback. */
(() => {
  'use strict';
  const dialog=document.getElementById('responsive-filters');
  const form=document.getElementById('event-search-form');
  if(!dialog||!form||typeof dialog.showModal!=='function'||typeof TideSearch==='undefined')return;
  const small=matchMedia('(width < 75rem)'),phone=matchMedia('(width < 48rem)');
  const reduced=matchMedia('(prefers-reduced-motion: reduce)');
  const results=document.getElementById('results');
  const intro=results.querySelector('.tide-slide-study__intro');
  const context=results.querySelector('.tide-app__filter-row');
  const summary=results.querySelector('.tide-slide-study__summary');
  const badge=summary.querySelector('.tide-slide-study__applied');
  const filters=results.querySelector('.tide-app__filters');
  const fields=filters.querySelector('.tide-app__filter-form');
  const actions=fields.querySelector('.tide-app__filter-actions');
  const apply=actions.querySelector('button[type="submit"]');
  const launcher=document.querySelector('.tide-responsive-filters__trigger');
  const query=document.getElementById('event-query');
  const querySubmit=form.querySelector('button[type="submit"]');
  const queryRow=form.querySelector('.tide-search-line');
  const nav=document.querySelector('.tide-app__nav');
  const body=dialog.querySelector('.tide-responsive-filters__body');
  const footer=dialog.querySelector('.tide-responsive-filters__footer');
  const title=dialog.querySelector('.tide-responsive-filters__title');
  const close=dialog.querySelector('[data-filter-close]');
  const reset=dialog.querySelector('[data-filter-reset]');
  const counter=dialog.querySelector('.tide-responsive-filters__count');
  const controls=[query,...fields.querySelectorAll('input')];
  const from=document.getElementById('event-from'),to=document.getElementById('event-to');
  const cards=[...results.querySelectorAll('.tide-event-card')];
  const slots=[form,context,launcher,fields,apply].map(node=>({node,marker:document.createComment('Browse first: original position')}));
  const applyText=apply.textContent,wasSecondary=apply.classList.contains('tide-button--secondary');
  const applied=TideSearch.read(new URLSearchParams(location.search));
  const appliedCount=Number(Boolean(applied.from||applied.to))+applied.categories.length;
  const returnKey='tide:browse-flyout:applied';
  let mounted=false,snapshot=null,committing=false,closing=false,exitAnimation=null;

  function clearViewport(){
    dialog.style.removeProperty('--tide-browse-flyout-viewport-height');
    dialog.style.removeProperty('--tide-browse-flyout-viewport-top');
  }
  function syncViewport(){
    const viewport=window.visualViewport;
    if(!mounted||!dialog.open||!viewport||viewport.scale!==1)return;
    // A software keyboard may resize only the visual viewport. Do not constrain
    // pinch zoom; keep native zoom/panning behavior when scale differs from one.
    dialog.style.setProperty('--tide-browse-flyout-viewport-height',viewport.height+'px');
    dialog.style.setProperty('--tide-browse-flyout-viewport-top',viewport.offsetTop+'px');
  }

  function values(){return controls.map(input=>({value:input.value,checked:input.checked}));}
  function restore(){
    if(!snapshot)return;
    controls.forEach((input,index)=>{input.value=snapshot[index].value;input.checked=snapshot[index].checked;});
    to.dispatchEvent(new Event('input',{bubbles:true}));
  }
  function state(){return TideSearch.read(new URLSearchParams(new FormData(form)));}
  function update(){
    if(!mounted)return;
    const next=state(),valid=TideSearch.validRange(next);
    const total=valid?cards.filter(card=>TideSearch.matches(card.dataset,next)).length:0;
    counter.textContent=valid?total+' matching '+(total===1?'event':'events'):'Check the date range';
    apply.textContent=valid?'Show '+total+' '+(total===1?'event':'events'):'Check dates';
    reset.disabled=!TideSearch.active(next);
  }
  function closePanel(){
    if(!dialog.open||closing)return;
    closing=true;
    const finish=()=>{if(closing){closing=false;exitAnimation=null;if(dialog.open)dialog.close('cancel');}};
    if(reduced.matches||!small.matches){finish();return;}
    exitAnimation=dialog.animate([{transform:'translateX(0)'},{transform:'translateX(-100%)'}],{duration:180,easing:'cubic-bezier(.4,0,1,1)'});
    exitAnimation.finished.then(finish,()=>{});
  }
  function dismiss(){if(!dialog.open||closing)return;committing=false;restore();closePanel();}
  function open(){
    if(!mounted||dialog.open)return;
    committing=false;snapshot=values();update();
    dialog.showModal();syncViewport();launcher.setAttribute('aria-expanded','true');
    body.scrollTop=0;title.focus({preventScroll:true});
  }
  function label(){
    if(!mounted)return;
    launcher.classList.toggle('tide-button--icon',phone.matches);
    launcher.classList.toggle('tide-browse-flyout__trigger--applied',TideSearch.active(applied));
    launcher.setAttribute('aria-label','Search and filters'+(appliedCount?' · '+appliedCount+' applied':''));
  }
  function mount(){
    if(mounted||!small.matches)return;
    slots.forEach(({node,marker})=>node.before(marker));
    body.append(form,fields);footer.append(apply);nav.prepend(launcher);
    summary.after(context);
    intro.classList.add('tide-sr-only');
    context.classList.add('tide-browse-flyout__context');context.hidden=!TideSearch.active(applied);
    form.classList.add('tide-browse-flyout__query');queryRow.classList.add('tide-browse-flyout__search-row');
    fields.classList.add('tide-responsive-filters__fields');
    apply.classList.add('tide-responsive-filters__apply');apply.classList.remove('tide-button--secondary');
    querySubmit.hidden=true;actions.hidden=true;filters.hidden=true;launcher.hidden=false;
    const names={music:'Music',comedy:'Comedy',workshop:'Workshops'};
    badge.hidden=!appliedCount;badge.textContent=applied.categories.map(category=>names[category]).join(' · ')||'Dates set';
    mounted=true;document.body.classList.add('tide-browse-flyout--mounted');label();update();
  }
  function unmount(){
    if(!mounted)return;
    const active=document.activeElement,wasOpen=dialog.open;
    closing=false;exitAnimation?.cancel();exitAnimation=null;
    if(wasOpen){committing=false;restore();dialog.close('resize');}
    clearViewport();
    // Restore outer wrappers first, then their original children.
    slots.forEach(({node,marker})=>marker.replaceWith(node));
    intro.classList.remove('tide-sr-only');context.classList.remove('tide-browse-flyout__context');context.hidden=false;
    form.classList.remove('tide-browse-flyout__query');queryRow.classList.remove('tide-browse-flyout__search-row');
    fields.classList.remove('tide-responsive-filters__fields');
    apply.classList.remove('tide-responsive-filters__apply');apply.classList.toggle('tide-button--secondary',wasSecondary);apply.textContent=applyText;
    querySubmit.hidden=false;actions.hidden=false;filters.hidden=false;launcher.hidden=true;
    launcher.classList.add('tide-button--icon');launcher.classList.remove('tide-browse-flyout__trigger--applied');
    launcher.setAttribute('aria-expanded','false');badge.hidden=true;badge.textContent='Filters · '+appliedCount;
    mounted=false;document.body.classList.remove('tide-browse-flyout--mounted');
    if(wasOpen||active===launcher)results.focus({preventScroll:true});
  }

  launcher.addEventListener('click',open);close.addEventListener('click',dismiss);
  dialog.addEventListener('cancel',event=>{event.preventDefault();dismiss();});
  dialog.addEventListener('click',event=>{
    if(event.target!==dialog)return;
    const r=dialog.getBoundingClientRect();
    if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dismiss();
  });
  dialog.addEventListener('close',()=>{clearViewport();launcher.setAttribute('aria-expanded','false');if(mounted&&!committing)launcher.focus({preventScroll:true});});
  dialog.addEventListener('input',update);dialog.addEventListener('change',update);
  dialog.addEventListener('keydown',event=>{
    if(event.key!=='Tab')return;
    const stops=[...dialog.querySelectorAll('button,input,select,textarea,a[href],[tabindex="0"]')].filter(node=>!node.disabled&&node.getClientRects().length);
    const first=stops[0],last=stops.at(-1),active=document.activeElement;
    if(event.shiftKey&&(active===first||active===title)){event.preventDefault();last?.focus();}
    else if(!event.shiftKey&&active===last){event.preventDefault();first?.focus();}
  });
  reset.addEventListener('click',()=>{
    query.value='';from.value='';to.value='';controls.filter(input=>input.type==='checkbox').forEach(input=>{input.checked=false;});
    to.dispatchEvent(new Event('input',{bubbles:true}));update();
  });
  form.addEventListener('submit',()=>{
    if(!mounted||!dialog.open)return;
    committing=true;closing=false;exitAnimation?.cancel();exitAnimation=null;
    const next=new URL(form.action,location.href);next.search=TideSearch.serialize(state());
    try{sessionStorage.setItem(returnKey,next.href);}catch{}
    dialog.close('apply');
  },true);
  small.addEventListener('change',()=>{if(!small.matches)unmount();else requestAnimationFrame(mount);});
  phone.addEventListener('change',label);
  window.visualViewport?.addEventListener('resize',syncViewport);
  window.visualViewport?.addEventListener('scroll',syncViewport);
  document.addEventListener('DOMContentLoaded',mount,{once:true});
  window.addEventListener('pageshow',()=>{
    if(small.matches)requestAnimationFrame(()=>{mount();launcher.setAttribute('aria-expanded',String(dialog.open));update();});
    let returned=false;
    try{returned=sessionStorage.getItem(returnKey)===location.href;if(returned)sessionStorage.removeItem(returnKey);}catch{}
    if(returned&&small.matches)requestAnimationFrame(()=>{
      const count=document.getElementById('result-count');count.tabIndex=-1;count.focus({preventScroll:true});
      summary.scrollIntoView({block:'start',behavior:'instant'});
    });
  });
})();
