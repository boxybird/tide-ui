// Read-only development measurements for frames/kit-closeout.html. Never served.
() => {
  const failures=[],measurements=[],signatures={};
  const near=(value,n)=>Math.abs(value.replace('px','')*1-n)<.8;
  const check=(ok,message)=>{if(!ok) failures.push(message);};
  const type=e=>{const s=getComputedStyle(e);return [s.fontFamily,s.fontStyle,s.fontSize,s.lineHeight,s.fontWeight,s.letterSpacing,s.textTransform];};
  const checkType=(e,size,leading,weight,label)=>{
    if(!e){failures.push(label+': missing');return;}
    const t=type(e);
    check(t[0].includes('Manrope')&&t[1]==='normal'&&near(t[2],size)&&near(t[3],leading)&&t[4]===String(weight),label+': type');
  };
  const titles={organizer:[14,24,550],partner:[16,24,550],fallback:[28,36,580],hero:[36,40,580],details:[28,36,580],panel:[20,28,580],'venue-card':[20,28,580]};
  const slots={organizer:'.tide-organizer__title',partner:'.tide-partner__title',fallback:'.tide-fallback__title',hero:'.tide-event-hero__title',details:'.tide-event-details__title',panel:'.tide-panel__title','venue-card':'.tide-venue-card__title'};
  for(const e of document.querySelectorAll('[data-closeout]')) {
    const kind=e.dataset.closeout,hidden=Boolean(e.closest('[hidden]')),s=getComputedStyle(e),r=e.getBoundingClientRect();
    const label=(e.closest('.tide-doc-closeout')?'context:':'default:')+kind;
    measurements.push({kind,hidden,type:type(e),width:r.width,height:r.height,padding:s.padding});
    if(hidden){check(r.width===0&&r.height===0,'hidden '+kind);continue;}
    check(r.left>=-1&&r.right<=innerWidth+1,label+': bounds');
    if(kind==='nested') {
      const profile=e.querySelector('.tide-venue-profile'),heading=e.querySelector('section h3');
      check(near(getComputedStyle(profile).paddingLeft,0)&&near(getComputedStyle(profile).paddingTop,24),label+': flush padding');
      check(Math.abs(profile.querySelector('h3').getBoundingClientRect().left-heading.getBoundingClientRect().left)<1,label+': aligned leading edges');
      continue;
    }
    checkType(e,14,24,400,label);
    if(titles[kind])checkType(e.querySelector(slots[kind]),...titles[kind],label+' title');
    if(['organizer','partner','panel','header','venue'].includes(kind))check([s.paddingLeft,s.paddingRight,s.paddingTop,s.paddingBottom].every(v=>near(v,24)),label+': padding');
    if(kind==='partner') {checkType(e.querySelector('p'),12,20,400,label+' body');checkType(e.querySelector('.tide-partner__label'),12,20,550,label+' label');}
    if(kind==='hero') {checkType(e.querySelector('.tide-event-hero__admission strong'),22,28,500,label+' admission');check(near(getComputedStyle(e.querySelector('.tide-event-hero__facts dd')).columnGap,8),label+': fact gap');}
    if(kind==='details') {checkType(e.querySelector('.tide-event-details__section-title'),16,24,550,label+' section');checkType(e.querySelector('.tide-eyebrow'),11,16,500,label+' eyebrow');checkType(e.querySelector('.tide-disclosure'),12,20,400,label+' disclosure');}
    if(kind==='header')checkType(e.querySelector('.tide-brand'),19,28,450,label+' brand');
    const signature=JSON.stringify([type(e),...(slots[kind]?[type(e.querySelector(slots[kind]))]:[])]);
    if(signatures[kind])check(signatures[kind]===signature,label+': context equality');else signatures[kind]=signature;
  }
  check(document.documentElement.scrollWidth<=innerWidth,'document overflow');
  return {url:location.href,width:innerWidth,height:innerHeight,cases:measurements.length,failures,measurements};
};
