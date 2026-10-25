'use strict';
(() => {
 const root=document.documentElement;
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 let engaged=null, rehearsalTimer;
 const strength=()=>root.dataset.strength==='overdrive' ? 2 : 1;
 const spring='linear(0,.45 12%,.87 25%,1.08 42%,.98 65%,1)';
 function reset(){
  clearTimeout(rehearsalTimer);
  document.querySelectorAll('.is-engaged,.is-pressed').forEach(el=>{el.classList.remove('is-engaged','is-pressed');el.style.removeProperty('translate');});
  engaged=null;
 }
 function engage(el){if(engaged===el)return;reset();engaged=el;el?.classList.add('is-engaged');root.dataset.microState=el?.matches('[data-close]')?'close-hover':'card-hover';}
 function pulse(el){if(!el||reduced.matches)return;el.animate([{opacity:.55,transform:'scale(.85)'},{opacity:.7,offset:.2},{opacity:0,transform:'scale('+ (1+strength()*.6) +')'}],{duration:600,easing:'ease-out',pseudoElement:'::after'});}
 document.addEventListener('pointermove',event=>{
  if(event.pointerType==='touch'||root.dataset.transitionPhase!=='idle')return;
  const el=event.target.closest('.event-card,.round-control');
  if(!el){if(engaged)reset();return;}engage(el);
  const r=el.getBoundingClientRect(); const x=(event.clientX-r.left)/r.width-.5,y=(event.clientY-r.top)/r.height-.5;
  el.style.setProperty('--hot-x',(x+.5)*100+'%');el.style.setProperty('--hot-y',(y+.5)*100+'%');
  if(el.matches('.round-control')&&!reduced.matches)el.style.translate=(x*12*strength())+'px '+(y*12*strength())+'px';
 });
 document.addEventListener('pointerout',event=>{if(!event.relatedTarget)reset();});
 document.addEventListener('focusin',event=>{if(root.dataset.transitionPhase!=='idle')return;const el=event.target.closest('.card-hit-area,.round-control');if(el)engage(el.closest('.event-card')||el);});
 document.addEventListener('focusout',()=>reset());
 document.addEventListener('pointerdown',event=>{const card=event.target.closest('.event-card');card?.classList.add('is-pressed');});
 document.addEventListener('pointerup',()=>document.querySelectorAll('.is-pressed').forEach(el=>el.classList.remove('is-pressed')));
 document.addEventListener('pointercancel',()=>reset());
 window.gatherFX={reset,
  land(id){const card=document.querySelector('[data-event="'+id+'"]'); if(!card)return;
   card.classList.remove('is-returning');
   if(reduced.matches)return;
   const marker=card.querySelector('.return-anchor');
   marker.animate([{opacity:1,scale:'1'},{opacity:0,scale:'.35'}],{duration:320,easing:'ease-in',fill:'none'});pulse(marker);
   card.animate([{translate:'0 0'},{translate:'0 '+(-5*strength())+'px',offset:.26},{translate:'0 3px',offset:.56},{translate:'0 0'}],{duration:580,easing:spring});
   card.animate([{opacity:1},{opacity:0}],{duration:850,easing:'ease-out',pseudoElement:'::after'});
   root.dataset.microState='landed';
  },
  save(id,isSaved){const button=document.querySelector('[data-save="'+id+'"]');if(!button||reduced.matches)return;const glyph=button.querySelector('.icon');
   glyph?.animate([{transform:'translateY(0) rotate(0) scale(1)'},{transform:'translateY(-'+(8*strength())+'px) rotate(-18deg) scale(1.3)',offset:.35},{transform:'translateY(2px) rotate(8deg) scale(.9)',offset:.68},{transform:'translateY(0) rotate(0) scale(1)'}],{duration:620,easing:spring});
   if(isSaved)pulse(button);root.dataset.microState=isSaved?'saved':'unsaved';
  },
  rehearse(){const el=root.dataset.view==='event'?document.querySelector('[data-close]'):document.querySelector('[data-event="ink"]');engage(el);rehearsalTimer=setTimeout(reset,2400);}
 };
})();

