// Development-only read-only listing measurements. Never served as browser code.
() => {
  const failures=[],px=v=>Number(v.replace('px','')),near=(v,n)=>Math.abs(px(v)-n)<1;
  const check=(pass,message)=>{if(!pass) failures.push(message);};
  const type=s=>({family:s.fontFamily,style:s.fontStyle,size:s.fontSize,leading:s.lineHeight,weight:s.fontWeight,tracking:s.letterSpacing,case:s.textTransform});
  const checkType=(e,size,leading,weight,label,tracking='normal',casing='none')=>{
    const s=getComputedStyle(e);
    check(s.fontFamily.includes('Manrope')&&s.fontStyle==='normal'&&near(s.fontSize,size)&&near(s.lineHeight,leading)&&s.fontWeight===String(weight)&&s.textTransform===casing&&
      (tracking==='normal'?s.letterSpacing==='normal':near(s.letterSpacing,tracking)),label+': type');
  };
  const nodes=document.querySelectorAll('[data-listing-card], [data-listing-date], [data-listing-result], [data-listing-group]');
  const measurements=Array.from(nodes,e=>{
    const kind=e.hasAttribute('data-listing-card')?'card':e.hasAttribute('data-listing-date')?'date':e.hasAttribute('data-listing-result')?'result':'group';
    const key=e.getAttribute('data-listing-'+kind),name=kind+':'+key,s=getComputedStyle(e),r=e.getBoundingClientRect();
    const m={kind,key,type:type(s),width:r.width,height:r.height,padding:s.padding,color:s.color,border:s.borderTopWidth,hidden:Boolean(e.closest('[hidden]'))};
    if(m.hidden) {check(r.height===0&&r.width===0,name+': hidden');return m;}
    checkType(e,14,24,400,name);
    check(r.right<=innerWidth+1&&r.left>=-1,name+': horizontal bounds');
    if(kind==='card') {
      check([s.paddingTop,s.paddingBottom,s.paddingLeft,s.paddingRight].every(v=>near(v,24)),name+': insets');
      const title=e.querySelector('.tide-event-card__title'),venue=e.querySelector('.tide-event-card__venue'),meta=e.querySelector('.tide-event-card__meta');
      checkType(title,24,32,580,name+' title',-.768);checkType(venue,14,24,400,name+' venue');
      checkType(e.querySelector('.tide-event-card__category'),12,20,550,name+' category',1.44,'uppercase');
      checkType(meta,14,24,400,name+' meta');checkType(e.querySelector('.tide-event-card__price'),14,24,550,name+' price');
      check(near(getComputedStyle(title).marginTop,8)&&near(getComputedStyle(venue).marginTop,4)&&near(getComputedStyle(meta).marginTop,16),name+': rhythm');
      check(near(getComputedStyle(meta).columnGap,16)&&near(getComputedStyle(meta).rowGap,12),name+': metadata gaps');
      const link=e.querySelector('.tide-event-card__link');
      if(link) {const box=link.getBoundingClientRect();check(Math.abs(box.width-r.width)<1&&Math.abs(box.height-r.height)<1,name+': cover geometry');}
      const action=e.querySelector('.tide-event-card__save');
      if(action) check(Number(getComputedStyle(action).zIndex)>Number(getComputedStyle(link).zIndex)&&action.getBoundingClientRect().width>=43,name+': independent action layer');
      m.titleType=type(getComputedStyle(title));m.metaType=type(getComputedStyle(meta));
    }
    if(kind==='date') {
      const day=e.querySelector('.tide-date__day'),parts=e.querySelector('.tide-date__parts');
      checkType(day,26,32,500,name+' day',-1.04);checkType(parts,12,16,400,name+' parts');
      check(near(s.columnGap,8)&&Math.abs(r.height-32)<1,name+': date geometry');
      check(e.tagName==='TIME'&&Boolean(e.getAttribute('datetime'))&&Boolean(e.getAttribute('aria-label'))&&day.getAttribute('aria-hidden')==='true'&&parts.getAttribute('aria-hidden')==='true',name+': native date label');
      m.dayWidth=day.getBoundingClientRect().width;m.partsWidth=parts.getBoundingClientRect().width;
    }
    if(kind==='result') {
      check(near(s.paddingTop,16)&&near(s.paddingBottom,16)&&near(s.paddingLeft,24)&&near(s.paddingRight,24)&&near(s.gap,12),name+': summary insets');
      checkType(e.querySelector('.tide-results__count'),14,24,400,name+' count');
      const order=e.querySelector('.tide-results__order');if(order) checkType(order,14,24,400,name+' order');
    }
    if(kind==='group') {
      const h=e.querySelector('.tide-event-group__header'),hs=getComputedStyle(h);
      check(near(hs.paddingTop,8)&&near(hs.paddingBottom,8)&&near(hs.paddingLeft,24)&&near(hs.paddingRight,24)&&near(hs.gap,12),name+': header insets');
      checkType(h.querySelector('.tide-event-group__title'),14,24,550,name+' title');
      checkType(h.querySelector('.tide-event-group__count'),12,20,400,name+' count');
      for(const jump of h.querySelectorAll('.tide-event-group__jump')) {checkType(jump,14,24,550,name+' jump');const box=jump.getBoundingClientRect();check(box.width>=43&&box.height>=43,name+': jump target');}
      check(e.matches('.tide-event-group--sticky')?hs.position==='sticky'&&near(hs.top,0):hs.position==='static',name+': sticky state');
    }
    return m;
  });
  const find=(kind,key)=>measurements.find(m=>m.kind===kind&&m.key===key);
  for(const [kind,a,b] of [['card','base','context-card'],['date','double','context-date'],['result','one','context'],['group','static','context']]) {
    const first=find(kind,a),other=find(kind,b);
    check(JSON.stringify(first.type)===JSON.stringify(other.type)&&first.padding===other.padding,kind+': context isolation');
  }
  const base=find('card','base'),selected=find('card','selected');check(Math.abs(base.height-selected.height)<1&&base.padding===selected.padding,'preview state geometry');
  const single=find('date','single'),double=find('date','double');check(Math.abs(single.dayWidth-double.dayWidth)<1&&Math.abs(single.partsWidth-double.partsWidth)<1,'date column alignment');
  const first=document.querySelector('#listing-calendar-first'),second=document.querySelector('#listing-calendar-second');
  check(px(getComputedStyle(first).borderTopWidth)===0&&px(getComputedStyle(second).borderTopWidth)>0,'visible sibling separators');
  check(!document.querySelector('#listing-unavailable .tide-event-card__link'),'unavailable detail navigation');
  check(document.scripts.length===0,'browser scripts');check(document.documentElement.scrollWidth<=innerWidth+1,'document overflow');
  return {theme:document.documentElement.dataset.theme,mode:document.documentElement.dataset.mode,viewport:[innerWidth,innerHeight],count:measurements.length,
    hidden:measurements.filter(m=>m.hidden).length,overflow:document.documentElement.scrollWidth-innerWidth,failures,measurements};
}
