/* Progressive desktop composition: original controls, original GET state. */
(() => {
  'use strict';
  const results=document.getElementById('results');
  const query=document.getElementById('event-search-form');
  const editor=document.getElementById('refine-editor');
  if(!results||!query||!editor)return;
  const desktop=matchMedia('(min-width: 75rem)');
  const variant=document.body.dataset.refine;
  if(variant==='pocket'&&!('showPopover' in HTMLElement.prototype))return;
  if(variant==='focus'&&!('showModal' in HTMLDialogElement.prototype))return;
  const intro=results.querySelector('.tide-refine-study__intro');
  const summary=results.querySelector('.tide-refine-study__summary');
  const context=results.querySelector('.tide-refine-study__context');
  const filters=results.querySelector('.tide-app__filters');
  const fields=filters.querySelector('.tide-refine-study__fields');
  const quick=results.querySelector('.tide-refine-study__quick');
  const trigger=summary.querySelector('.tide-refine-study__trigger');
  const close=editor.querySelector('.tide-refine-study__close');
  const body=editor.querySelector('.tide-refine-study__editor-body');
  const from=document.getElementById('event-from');
  const to=document.getElementById('event-to');
  let originalOpen=filters.open;
  const moves=[query,context,fields,quick].map(node=>{const marker=document.createComment('filter-space-original');node.before(marker);return {node,marker};});
  let mounted=false,editing=false,hiddenNodes=[],listOffset=0,observer;
  const categories=[...fields.querySelectorAll('input[name="category"]:checked')].map(input=>input.parentElement.textContent.trim());
  const count=Number(Boolean(from.value||to.value))+categories.length;
  const baseLabel={pocket:'Filters',focus:'Search & filter',refine:'Refine'}[variant];
  trigger.textContent=baseLabel+(count?' · '+count:'');
  const applied=document.createElement('span');applied.className='tide-caption tide-refine-study__applied';
  applied.textContent=categories.join(' · ');

  function positionPocket(){
    if(!mounted)return;
    const headingHeight=summary.getBoundingClientRect().height;
    if(headingHeight>0)results.style.setProperty('--tide-refine-study-heading-height',headingHeight+'px');
    if(variant!=='pocket')return;
    const rect=results.getBoundingClientRect();
    const button=trigger.getBoundingClientRect();
    editor.style.setProperty('--tide-refine-study-left',rect.left+'px');
    editor.style.setProperty('--tide-refine-study-width',rect.width+'px');
    editor.style.setProperty('--tide-refine-study-top',button.bottom+'px');
  }
  function exit(refocus=true){
    if(variant==='pocket') {if(editor.matches(':popover-open'))editor.hidePopover();}
    else if(variant==='focus') {if(editor.open)editor.close();}
    else if(editing){
      editor.hidden=true;
      hiddenNodes.forEach(({node,hidden})=>{node.hidden=hidden;});hiddenNodes=[];
      document.body.classList.remove('tide-refine-study--editing');
      results.scrollTo({top:listOffset,behavior:'instant'});
    }
    editing=false;trigger.setAttribute('aria-expanded','false');
    if(refocus&&mounted)trigger.focus({preventScroll:true});
  }
  function open(){
    if(!mounted)return;
    if(variant==='pocket')return; // Declarative popovertarget retains native light dismiss.
    if(variant==='focus')editor.showModal();
    else{
      listOffset=results.scrollTop;
      hiddenNodes=[...results.children].filter(node=>node!==editor).map(node=>({node,hidden:node.hidden}));
      hiddenNodes.forEach(({node})=>{node.hidden=true;});
      editor.hidden=false;document.body.classList.add('tide-refine-study--editing');
      results.scrollTo({top:0,behavior:'instant'});
    }
    editing=true;trigger.setAttribute('aria-expanded','true');
    document.getElementById('event-query').focus({preventScroll:true});
  }
  trigger.addEventListener('click',open);
  close.addEventListener('click',()=>exit());
  editor.addEventListener('toggle',event=>{
    if(variant!=='pocket')return;
    const expanded=event.newState==='open';trigger.setAttribute('aria-expanded',String(expanded));
    if(expanded)close.focus({preventScroll:true});
  });
  if(variant==='focus')editor.addEventListener('close',()=>{editing=false;trigger.setAttribute('aria-expanded','false');if(mounted)trigger.focus({preventScroll:true});});
  editor.addEventListener('keydown',event=>{if(variant==='refine'&&event.key==='Escape'){event.preventDefault();exit();}});
  // The existing month helper predates the persistent list heading. Account for
  // that heading here, while preserving native links and the prior helper below desktop.
  results.addEventListener('click',event=>{
    const link=event.target.closest?.('a.tide-event-group__jump');
    if(!mounted||!link||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    const url=new URL(link.href);
    if(url.origin!==location.origin||url.pathname!==location.pathname)return;
    const group=document.getElementById(decodeURIComponent(url.hash.slice(1)));
    if(!group||!results.contains(group))return;
    event.preventDefault();
    const top=group.getBoundingClientRect().top-results.getBoundingClientRect().top+results.scrollTop-results.clientTop-summary.getBoundingClientRect().height;
    group.querySelector('.tide-event-group__title')?.focus({preventScroll:true});
    results.scrollTo({top:Math.max(0,top),behavior:'auto'});
  },true);
  // A search submitted outside Pocket must reveal an invalid date before native focus.
  query.addEventListener('click',event=>{
    if(variant==='pocket'&&event.target.closest('button[type="submit"]')&&!to.validity.valid){positionPocket();editor.showPopover();}
  });
  document.addEventListener('invalid',event=>{
    if(!mounted||!editor.contains(event.target))return;
    if(variant==='pocket'&&!editor.matches(':popover-open'))editor.showPopover();
    if(variant==='focus'&&!editor.open)open();
    if(variant==='refine'&&!editing)open();
  },true);
  function place(){
    if(desktop.matches===mounted)return;
    if(desktop.matches){
      mounted=true;
      originalOpen=filters.open;
      intro.classList.add('tide-sr-only');filters.hidden=true;trigger.hidden=false;
      if(categories.length)context.append(applied);
      summary.after(quick,context);
      if(variant==='pocket'){quick.hidden=false;quick.append(query);}
      else body.append(query);
      body.append(fields);
      if(variant!=='refine')editor.hidden=false;
      document.body.classList.add('tide-refine-study--mounted');
      observer=new ResizeObserver(positionPocket);observer.observe(results);observer.observe(summary);
      positionPocket();
    }else{
      const active=document.activeElement;const inEditor=editor.contains(active);const wasTrigger=active===trigger;
      exit(false);observer?.disconnect();mounted=false;
      moves.forEach(({node,marker})=>marker.after(node));
      applied.remove();
      intro.classList.remove('tide-sr-only');filters.hidden=false;filters.open=originalOpen;
      trigger.hidden=true;quick.hidden=true;editor.hidden=true;
      document.body.classList.remove('tide-refine-study--mounted');
      ['--tide-refine-study-left','--tide-refine-study-width','--tide-refine-study-top'].forEach(name=>editor.style.removeProperty(name));
      results.style.removeProperty('--tide-refine-study-heading-height');
      if(inEditor&&fields.contains(active)&&!filters.open)filters.querySelector('summary').focus({preventScroll:true});
      else if(wasTrigger||inEditor&&active===close)filters.querySelector('summary').focus({preventScroll:true});
      else if(active?.isConnected)active.focus({preventScroll:true});
    }
  }
  desktop.addEventListener('change',place);window.addEventListener('resize',positionPocket);place();
})();
