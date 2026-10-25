/* Desktop-only layout comparison. Reuse the one real submit button and field. */
(() => {
  'use strict';
  const root=document.body;
  const button=document.querySelector('.tide-width-study__search-submit');
  if(!button)return;
  const desktop=matchMedia('(min-width:75rem)');
  const choices=new Set(['below','compact','inline']);
  const key='tide:contained-widths:search:'+root.dataset.width;
  let layout='below';
  try {const stored=sessionStorage.getItem(key);if(choices.has(stored))layout=stored;}catch{}
  const requested=new URLSearchParams(location.search).get('search-layout');
  if(choices.has(requested))layout=requested;
  function apply(){
    root.dataset.searchLayout=layout;
    button.classList.toggle('tide-button--icon',!desktop.matches||layout==='inline');
    root.classList.add('tide-width-study--enhanced');
    try {sessionStorage.setItem(key,layout);}catch{}
  }
  window.addEventListener('message',event=>{
    if(event.origin!==location.origin||event.source!==parent||event.data?.type!=='tide:contained-widths:search'||!choices.has(event.data.layout))return;
    layout=event.data.layout;apply();
  });
  desktop.addEventListener('change',apply);apply();
})();
