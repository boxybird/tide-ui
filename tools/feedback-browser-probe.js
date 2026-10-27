// Development-only read-only measurements; never served with the kit or site.
() => {
  const failures=[];
  const px=value=>Number(value.replace('px',''));
  const near=(value,n)=>Math.abs(px(value)-n)<1;
  const check=(pass,message)=>{if(!pass) failures.push(message);};
  const type=s=>({family:s.fontFamily,style:s.fontStyle,size:s.fontSize,leading:s.lineHeight,
    weight:s.fontWeight,tracking:s.letterSpacing,case:s.textTransform});
  const checkType=(e,size,leading,weight,name,title=false)=>{
    const s=getComputedStyle(e);
    check(s.fontFamily.includes('Manrope')&&s.fontStyle==='normal'&&near(s.fontSize,size)&&
      near(s.lineHeight,leading)&&s.fontWeight===String(weight)&&s.textTransform==='none'&&
      (title?near(s.letterSpacing,-.768):s.letterSpacing==='normal'),name+': type');
  };
  const inset=(s,block,inline)=>near(s.paddingTop,block)&&near(s.paddingBottom,block)&&
    near(s.paddingLeft,inline)&&near(s.paddingRight,inline);
  const measurements=Array.from(document.querySelectorAll('[data-feedback-case]'),e=>{
    const name=e.dataset.feedbackCase,s=getComputedStyle(e),r=e.getBoundingClientRect();
    const m={name,type:type(s),height:r.height,width:r.width,padding:s.padding,gap:s.gap,
      color:s.color,background:s.backgroundColor,border:s.borderColor,hidden:e.hasAttribute('hidden')};
    if(m.hidden) {check(s.display==='none'&&r.height===0&&r.width===0,name+': hidden');return m;}
    if(e.matches('.tide-badge')) {
      checkType(e,12,20,550,name);check(r.height>=23&&inset(s,1,8)&&near(s.columnGap,8),name+': badge geometry');
      check(e.tagName==='SPAN'&&!e.hasAttribute('tabindex')&&!e.hasAttribute('role'),name+': static badge');
      const icon=e.querySelector('.tide-icon');if(icon) check(Math.abs(icon.getBoundingClientRect().width-16)<1,name+': glyph');
    } else {
      checkType(e,14,24,400,name);
      if(e.matches('.tide-notice')) {
        check(inset(s,16,16)&&near(s.rowGap,8),name+': notice spacing');
        check([s.borderTopColor,s.borderRightColor,s.borderBottomColor,s.borderLeftColor].every(v=>v===s.borderTopColor)&&
          [s.borderTopWidth,s.borderRightWidth,s.borderBottomWidth,s.borderLeftWidth].every(v=>v===s.borderTopWidth),name+': uniform border');
        for(const title of e.querySelectorAll('.tide-notice__title')) checkType(title,14,24,550,name+' title');
        for(const strong of e.querySelectorAll(':scope > strong')) checkType(strong,14,24,550,name+' legacy title');
      }
      if(e.matches('.tide-toast')) {
        check(inset(s,16,16)&&near(s.gap,16)&&s.flexWrap==='wrap'&&r.height>=77,name+': toast spacing');
        for(const message of e.querySelectorAll('.tide-toast__message, :scope > span')) checkType(message,14,24,400,name+' message');
      }
      if(e.matches('.tide-empty')) {
        const compact=e.matches('.tide-empty--compact');
        check(inset(s,compact?24:48,compact?16:24)&&near(s.rowGap,16),name+': empty spacing');
        check(px(s.borderTopWidth)===0&&s.justifyItems==='start',name+': unframed empty');
        for(const title of e.querySelectorAll('.tide-empty__title')) checkType(title,24,32,580,name+' title',true);
        const icon=e.querySelector(':scope > .tide-icon');if(icon) check(Math.abs(icon.getBoundingClientRect().width-28)<1,name+': glyph');
      }
      for(const p of e.querySelectorAll('p')) checkType(p,14,24,400,name+' paragraph');
    }
    check(r.right<=innerWidth+1&&r.left>=-1,name+': bounds');
    return m;
  });
  const byName=Object.fromEntries(measurements.map(m=>[m.name,m]));
  for(const [a,b] of [['context-badge','badge-neutral'],['context-notice','notice-info'],['context-toast','toast-action'],['context-empty','empty-matches']]) {
    check(JSON.stringify(byName[a].type)===JSON.stringify(byName[b].type),a+': context type');
    check(byName[a].padding===byName[b].padding&&byName[a].gap===byName[b].gap,a+': context spacing');
  }
  for(const name of ['notice-error','notice-success','notice-long','notice-summary','context-notice'])
    check(byName[name].border===byName['notice-info'].border,name+': neutral boundary');
  for(const name of ['badge-success','badge-warning','badge-danger'])
    check(byName[name].padding===byName['badge-neutral'].padding,name+': status density');
  for(const link of document.querySelectorAll('.tide-notice__action, .tide-toast__action, .tide-empty__action')) {
    checkType(link,14,24,550,link.id||link.className);
    check(link.getBoundingClientRect().height>=43,'link target: '+link.textContent);
    if(link.getAttribute('aria-disabled')==='true') {
      check(!link.hasAttribute('href')&&getComputedStyle(link).textDecorationLine==='none','unavailable link');
    }
  }
  for(const [id,height,block,inline] of [['feedback-notice-button',48,12,20],['feedback-toast-button',44,10,16],['feedback-context-button',48,12,20]]) {
    const e=document.querySelector('#'+id),s=getComputedStyle(e);
    checkType(e,14,22,550,id);check(e.getBoundingClientRect().height>=height-1&&inset(s,block,inline),id+': button composition');
  }
  const summary=document.querySelector('#feedback-summary-title');checkType(summary,16,24,650,'error summary title');
  check(document.documentElement.scrollWidth<=innerWidth+1,'horizontal overflow');
  check(document.scripts.length===0,'browser scripts');
  return {theme:document.documentElement.dataset.theme,mode:document.documentElement.dataset.mode,
    viewport:[innerWidth,innerHeight],count:measurements.length,hidden:measurements.filter(m=>m.hidden).length,
    overflow:document.documentElement.scrollWidth-innerWidth,failures,measurements};
}
