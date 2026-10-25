/* Move original controls after search initialization. No cloned forms or state. */
(() => {
  'use strict';
  const bar=document.querySelector('.tide-control-study__bar');
  const results=document.getElementById('results');
  const query=document.getElementById('event-search-form');
  if(!bar||!results||!query)return;
  const desktop=matchMedia('(min-width:75rem)');
  const shelf=document.body.dataset.controls==='filter-shelf';
  const intro=results.querySelector('.tide-control-study__intro');
  const context=results.querySelector('.tide-control-study__context');
  const filters=results.querySelector('.tide-control-study__disclosure');
  const body=filters.querySelector('.tide-control-study__filter-body');
  const date=body.querySelector('fieldset');
  const categories=body.querySelectorAll('fieldset')[1];
  const actions=body.querySelector('.tide-control-study__actions');
  const slots=[intro,query,context,filters].map(node=>({node,marker:document.createComment('Original Lineup control position')}));
  const inner=[date,categories,actions].map(node=>({node,marker:document.createComment('Original filter position')}));
  const visuallyHidden=[date.querySelector('legend'),date.querySelector('#date-hint'),categories.querySelector('.tide-field__hint')];
  let mounted=false,originalOpen=false,observer;

  function place(){
    if(desktop.matches===mounted)return;
    const active=document.activeElement;
    if(desktop.matches){
      originalOpen=filters.open;
      slots.forEach(({node,marker})=>{node.before(marker);bar.append(node);});
      date.classList.add('tide-control-study__dates');
      categories.classList.add('tide-control-study__categories');
      if(shelf){
        filters.open=originalOpen;
      }else{
        filters.hidden=true;
        inner.forEach(({node,marker})=>{node.before(marker);bar.append(node);});
      }
      visuallyHidden.forEach(node=>node.classList.add('tide-sr-only'));
      bar.hidden=false;
      document.body.classList.add('tide-control-study--mounted');
      observer=new ResizeObserver(()=>{
        document.documentElement.style.setProperty('--tide-control-study-bar-height',bar.getBoundingClientRect().height+'px');
      });
      observer.observe(bar);
      mounted=true;
    }else{
      observer.disconnect();
      if(!shelf)inner.forEach(({node,marker})=>marker.replaceWith(node));
      slots.forEach(({node,marker})=>marker.replaceWith(node));
      filters.hidden=false;filters.open=originalOpen;
      date.classList.remove('tide-control-study__dates');
      categories.classList.remove('tide-control-study__categories');
      visuallyHidden.forEach(node=>node.classList.remove('tide-sr-only'));
      bar.hidden=true;
      document.body.classList.remove('tide-control-study--mounted');
      document.documentElement.style.removeProperty('--tide-control-study-bar-height');
      mounted=false;
    }
    const target=active===bar?query.querySelector('input'):filters.contains(active)&&!filters.open?filters.querySelector('summary'):active;
    if(target?.isConnected&&target!==document.body)target.focus({preventScroll:true});
  }
  document.addEventListener('invalid',event=>{
    if(mounted&&filters.contains(event.target))filters.open=true;
  },true);
  desktop.addEventListener('change',place);place();
})();
