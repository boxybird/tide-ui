/* One original GET form and one live count/reset/apply set at every width.
   The same nodes move between the mobile flyout and existing desktop dock.
   Native details and original submit controls remain the no-script fallback. */
(() => {
  'use strict';
  const dialog=document.getElementById('responsive-filters');
  const form=document.getElementById('event-search-form');
  if(!dialog||!form||typeof dialog.showModal!=='function'||typeof TideSearch==='undefined')return;
  const small=TideApp.media('drawer'),phone=TideApp.media('phone');
  const reduced=TideApp.media('reducedMotion');
  const results=document.getElementById('results');
  const intro=results.querySelector('.tide-app__intro');
  const context=results.querySelector('.tide-app__filter-row');
  const summary=results.querySelector('.tide-lineup__summary');
  const badge=summary.querySelector('.tide-app__applied-filters');
  const filters=results.querySelector('.tide-app__filters');
  const fields=filters.querySelector('.tide-app__filter-form');
  const actions=fields.querySelector('.tide-app__filter-actions');
  const apply=actions.querySelector('button[type="submit"]');
  const launcher=document.querySelector('.tide-filter-drawer__trigger');
  const query=document.getElementById('event-query');
  const nav=document.querySelector('.tide-app__nav');
  const body=dialog.querySelector('.tide-filter-panel__body');
  const footer=dialog.querySelector('.tide-filter-panel__footer');
  const title=dialog.querySelector('.tide-filter-panel__title');
  const close=dialog.querySelector('[data-filter-close]');
  const reset=dialog.querySelector('[data-filter-reset]');
  const counter=dialog.querySelector('.tide-filter-panel__count');
  const statusRow=counter.parentElement;
  const fallbackClear=actions.querySelector('a');
  const controls=[query,...fields.querySelectorAll('input')];
  const from=document.getElementById('event-from'),to=document.getElementById('event-to');
  const cards=[...results.querySelectorAll('.tide-event-card')];
  const slots=[form,context,launcher,fields,apply].map(node=>({node,marker:document.createComment('Browse first: original position')}));
  const applyText=apply.textContent,wasSecondary=apply.classList.contains('tide-button--secondary');
  const applied=TideApp.appliedState();
  const appliedCount=TideSearch.refinementCount(applied);
  const returnKey=TideApp.keys.appliedReturn;
  let mounted=false,desktopMounted=false,snapshot=null,committing=false,closing=false,exitAnimation=null;
  const gutterProperty='--tide-app-scrollbar-gutter';
  let gutterObserver=null,gutterFrame=0,pendingGutter=0,lastGutter=null;

  function watchGutter(){
    if(gutterObserver||typeof ResizeObserver!=='function')return;
    gutterObserver=new ResizeObserver(entries=>{
      if(!desktopMounted||small.matches)return;
      const entry=entries.find(item=>item.target===results);
      if(!entry)return;
      const style=getComputedStyle(results);
      const insets=['paddingInlineStart','paddingInlineEnd','borderInlineStartWidth','borderInlineEndWidth']
        .reduce((total,key)=>total+(parseFloat(style[key])||0),0);
      // This horizontal-writing-mode composition has one unfragmented list.
      // Box sizes retain subpixel precision; subtract padding/borders so only
      // the native scrollbar's occupied space remains. Overlay bars add zero.
      const border=entry.borderBoxSize?.[0]?.inlineSize??results.offsetWidth;
      const content=entry.contentBoxSize?.[0]?.inlineSize??entry.contentRect.width;
      pendingGutter=Math.round(Math.max(0,border-content-insets)*1000)/1000;
      if(!Number.isFinite(pendingGutter)||gutterFrame||lastGutter!==null&&Math.abs(pendingGutter-lastGutter)<0.01)return;
      // Writing outside observer delivery avoids a resize-delivery loop.
      gutterFrame=requestAnimationFrame(()=>{
        gutterFrame=0;
        if(!desktopMounted||small.matches)return;
        if(lastGutter!==null&&Math.abs(pendingGutter-lastGutter)<0.01)return;
        lastGutter=pendingGutter;
        document.body.style.setProperty(gutterProperty,lastGutter+'px');
      });
    });
    gutterObserver.observe(results);
  }
  function stopWatchingGutter(){
    gutterObserver?.disconnect();gutterObserver=null;
    cancelAnimationFrame(gutterFrame);gutterFrame=0;lastGutter=null;
    document.body.style.removeProperty(gutterProperty);
  }

  function clearViewport(){
    dialog.style.removeProperty('--tide-filter-drawer-viewport-height');
    dialog.style.removeProperty('--tide-filter-drawer-viewport-top');
  }
  function syncViewport(){
    const viewport=window.visualViewport;
    if(!mounted||!dialog.open||!viewport||viewport.scale!==1)return;
    // A software keyboard may resize only the visual viewport. Do not constrain
    // pinch zoom; keep native zoom/panning behavior when scale differs from one.
    dialog.style.setProperty('--tide-filter-drawer-viewport-height',viewport.height+'px');
    dialog.style.setProperty('--tide-filter-drawer-viewport-top',viewport.offsetTop+'px');
  }

  function values(){return controls.map(input=>({value:input.value,checked:input.checked}));}
  function restore(){
    if(!snapshot)return;
    controls.forEach((input,index)=>{input.value=snapshot[index].value;input.checked=snapshot[index].checked;});
    to.dispatchEvent(new Event('input',{bubbles:true}));
  }
  function state(){return TideApp.formState(form);}
  function update(){
    if(!mounted&&!desktopMounted)return;
    const next=state(),valid=TideSearch.validRange(next);
    const total=valid?cards.filter(card=>TideSearch.matches(card.dataset,next)).length:0;
    counter.textContent=valid?TideApp.eventCount(total,'matching'):'Check the date range';
    apply.textContent=valid?'Show '+TideApp.eventCount(total):'Check dates';
    reset.disabled=!TideSearch.active(next);
  }
  function mountDesktop(){
    if(small.matches||desktopMounted)return;
    const dock=document.querySelector('.tide-filter-panel__footer');
    if(!dock)return;
    // The desktop rail composition owns the dock. Restore these children
    // before it removes that dock at the next breakpoint.
    dock.prepend(statusRow);
    apply.classList.add('tide-button--full');
    apply.classList.remove('tide-button--secondary');
    fallbackClear.classList.add('tide-app__legacy-clear');
    desktopMounted=true;update();watchGutter();
  }
  function unmountDesktop(){
    if(!desktopMounted)return;
    stopWatchingGutter();
    footer.prepend(statusRow);
    apply.classList.remove('tide-button--full');
    apply.classList.toggle('tide-button--secondary',wasSecondary);
    fallbackClear.classList.remove('tide-app__legacy-clear');
    desktopMounted=false;
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
    launcher.classList.toggle('tide-filter-drawer__trigger--applied',TideSearch.active(applied));
    launcher.setAttribute('aria-label','Search and filters'+(appliedCount?' · '+appliedCount+' applied':''));
  }
  function mount(){
    if(mounted||!small.matches)return;
    slots.forEach(({node,marker})=>node.before(marker));
    body.append(form,fields);footer.append(apply);nav.prepend(launcher);
    summary.after(context);
    if(!document.body.classList.contains('tide-app--venue'))intro.classList.add('tide-sr-only');
    context.classList.add('tide-filter-drawer__context');context.hidden=!TideSearch.active(applied);
    form.classList.add('tide-filter-drawer__query');
    fields.classList.add('tide-app__filter-fields');
    apply.classList.add('tide-button--full');apply.classList.remove('tide-button--secondary');
    actions.hidden=true;filters.hidden=true;launcher.hidden=false;
    const names={music:'Music',comedy:'Comedy',workshop:'Workshops'};
    badge.hidden=!appliedCount;badge.textContent=applied.categories.map(category=>names[category]).join(' · ')||'Dates set';
    mounted=true;document.body.classList.add('tide-app--drawer');label();update();
  }
  function unmount(){
    if(!mounted)return;
    const active=document.activeElement,wasOpen=dialog.open;
    closing=false;exitAnimation?.cancel();exitAnimation=null;
    if(wasOpen){committing=false;restore();dialog.close('resize');}
    clearViewport();
    // Restore outer wrappers first, then their original children.
    slots.forEach(({node,marker})=>marker.replaceWith(node));
    intro.classList.remove('tide-sr-only');context.classList.remove('tide-filter-drawer__context');context.hidden=false;
    form.classList.remove('tide-filter-drawer__query');
    fields.classList.remove('tide-app__filter-fields');
    apply.classList.remove('tide-button--full');apply.classList.toggle('tide-button--secondary',wasSecondary);apply.textContent=applyText;
    actions.hidden=false;filters.hidden=false;launcher.hidden=true;
    launcher.classList.add('tide-button--icon');launcher.classList.remove('tide-filter-drawer__trigger--applied');
    launcher.setAttribute('aria-expanded','false');badge.hidden=true;badge.textContent='Filters · '+appliedCount;
    mounted=false;document.body.classList.remove('tide-app--drawer');
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
  // Listen to the controls themselves: fields are associated with the form
  // but can live outside it, and both compositions move these same nodes.
  controls.forEach(input=>{input.addEventListener('input',update);input.addEventListener('change',update);});
  dialog.addEventListener('keydown',event=>{
    // A native search input otherwise consumes the first Escape to clear text.
    if(event.key==='Escape'){event.preventDefault();dismiss();return;}
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
    const next=TideApp.destination(form.action,state());
    TideApp.storage.set(returnKey,next.href);
    dialog.close('apply');
  },true);
  small.addEventListener('change',()=>{
    if(!small.matches){unmount();requestAnimationFrame(mountDesktop);}
    else{unmountDesktop();requestAnimationFrame(mount);}
  });
  phone.addEventListener('change',label);
  window.visualViewport?.addEventListener('resize',syncViewport);
  window.visualViewport?.addEventListener('scroll',syncViewport);
  document.addEventListener('DOMContentLoaded',()=>{mount();mountDesktop();},{once:true});
  window.addEventListener('pageshow',()=>{
    if(small.matches)requestAnimationFrame(()=>{mount();launcher.setAttribute('aria-expanded',String(dialog.open));update();});
    else requestAnimationFrame(()=>{mountDesktop();update();});
    const returned=TideApp.storage.get(returnKey)===location.href;
    if(returned)TideApp.storage.remove(returnKey);
    if(returned&&small.matches)requestAnimationFrame(()=>{
      const count=document.getElementById('result-count');count.tabIndex=-1;count.focus({preventScroll:true});
      summary.scrollIntoView({block:'start',behavior:'instant'});
    });
  });
})();
