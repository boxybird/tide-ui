/* Review fixture selection and mount timing only. Existing navigation owns the app. */
(() => {
  'use strict';
  const root=document.body;
  const desktop=matchMedia('(min-width:75rem)');
  const key='tide:reading-widths:photo:'+root.dataset.room;
  const modes=new Set(['original','rough','none']);
  const originals=new WeakMap();
  const asset=new URL('assets/organizer-upload.png',document.currentScript.src).href;
  let mode='rough';
  try { const stored=sessionStorage.getItem(key);if(modes.has(stored))mode=stored; } catch {}
  const requested=new URLSearchParams(location.search).get('photo');
  if(modes.has(requested))mode=requested;

  function applyPhoto() {
    try { sessionStorage.setItem(key,mode); } catch {}
    const title=document.getElementById('event-title');
    if(title?.textContent.trim()!=='Ink After Dark')return;
    const hero=title.closest('.tide-event-hero');
    const photo=hero?.querySelector('.tide-event-hero__photo');
    if(!photo)return;
    if(!originals.has(photo))originals.set(photo,{src:photo.getAttribute('src'),alt:photo.alt});
    const original=originals.get(photo);
    const figure=photo.closest('.tide-room-study__media');
    photo.hidden=mode==='none';
    if(figure)figure.hidden=mode==='none';
    photo.src=mode==='rough'?asset:original.src;
    photo.alt=mode==='rough'?'An imperfect organizer snapshot: a printmaking table below a large blank wall, softly focused and unevenly lit.':original.alt;
  }
  function ready() {
    root.classList.remove('tide-room-study--ready');
    if(desktop.matches)requestAnimationFrame(()=>requestAnimationFrame(()=>root.classList.add('tide-room-study--ready')));
  }
  window.addEventListener('message',event=>{
    if(event.origin!==location.origin||event.source!==parent||event.data?.type!=='tide:reading-widths:photo'||!modes.has(event.data.mode))return;
    mode=event.data.mode;applyPhoto();
  });
  window.addEventListener('tide:preview-ready',applyPhoto);
  desktop.addEventListener('change',ready);
  applyPhoto();ready();
})();
