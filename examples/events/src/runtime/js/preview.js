/* Supported sample-photo/inspection hooks and post-mount transition readiness.
   Historical message and storage identifiers remain a compatibility contract. */
(() => {
  'use strict';
  const root=document.body;
  const desktop=TideApp.media('desktop');
  const key=TideApp.keys.photo(root.dataset.stateKey);
  const modes=new Set(['original','rough','none']);
  const originals=new WeakMap();
  const asset=new URL('assets/organizer-upload.png',document.currentScript.src).href;
  let mode='rough';
  const stored=TideApp.storage.get(key);if(modes.has(stored))mode=stored;
  const params=new URLSearchParams(location.search);
  const requested=params.get('photo');
  if(modes.has(requested))mode=requested;

  function applyPhoto() {
    TideApp.storage.set(key,mode);
    const title=document.getElementById('event-title');
    if(title?.textContent.trim()!=='Ink After Dark')return;
    const hero=title.closest('.tide-event-hero');
    const photo=hero?.querySelector('.tide-event-hero__photo');
    if(!photo)return;
    if(!originals.has(photo))originals.set(photo,{src:photo.getAttribute('src'),alt:photo.alt});
    const original=originals.get(photo);
    photo.hidden=mode==='none';
    photo.src=mode==='rough'?asset:original.src;
    photo.alt=mode==='rough'?'An imperfect organizer snapshot: a printmaking table below a large blank wall, softly focused and unevenly lit.':original.alt;
  }
  function ready() {
    root.classList.remove('tide-app--ready');
    if(desktop.matches)requestAnimationFrame(()=>requestAnimationFrame(()=>root.classList.add('tide-app--ready')));
  }
  window.addEventListener('message',event=>{
    if(event.origin!==location.origin||event.source!==parent||event.data?.type!=='tide:reading-widths:photo'||!modes.has(event.data.mode))return;
    mode=event.data.mode;applyPhoto();
  });
  window.addEventListener('tide:preview-ready',applyPhoto);
  desktop.addEventListener('change',ready);
  const results=document.getElementById('results');
  if(results&&params.has('inspect')&&TideApp.media('split').matches){
    document.addEventListener('DOMContentLoaded',()=>requestAnimationFrame(()=>{
      const card=results.querySelector('.tide-event-card--in-view');if(!card)return;
      const summary=results.querySelector('.tide-lineup__summary').getBoundingClientRect().height;
      const group=card.closest('.tide-event-group').querySelector('header').getBoundingClientRect().height;
      const top=card.getBoundingClientRect().top-results.getBoundingClientRect().top+results.scrollTop-summary-group;
      results.scrollTo({top:Math.max(0,top),behavior:'instant'});
    }),{once:true});
  }
  applyPhoto();ready();
})();
