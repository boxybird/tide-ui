// Development-only, read-only DOM measurement. Never import into a deliverable.
// Evaluate this function through Browser Use on a generated form-states.html.
() => {
  const px = value => Number(value.replace('px', ''));
  const failures = [];
  const near = (value, expected) => Math.abs(px(value) - expected) < 1;
  const assert = (condition, message) => { if (!condition) failures.push(message); };
  const type = s => ({ family:s.fontFamily, style:s.fontStyle, size:s.fontSize,
    leading:s.lineHeight, weight:s.fontWeight, tracking:s.letterSpacing, case:s.textTransform });
  const checkType = (s, size, leading, weight, name, nativeSelect=false) => {
    assert(s.fontFamily.includes('Manrope') && s.fontStyle === 'normal' &&
      s.letterSpacing === 'normal' && s.textTransform === 'none' &&
      near(s.fontSize,size) && (near(s.lineHeight,leading) || nativeSelect && s.lineHeight==='normal') && s.fontWeight === String(weight), name+': type');
  };
  const measurements = Array.from(document.querySelectorAll('[data-control-case]'), e => {
    const name=e.dataset.controlCase, s=getComputedStyle(e), r=e.getBoundingClientRect();
    const m={name, width:r.width, height:r.height, type:type(s), padding:s.padding,
      border:s.borderColor, borderWidth:s.borderWidth, background:s.backgroundColor, color:s.color};
    if (e.matches('.tide-field__control')) {
      const select=e.tagName==='SELECT', listbox=select && (e.hasAttribute('multiple') || Number(e.getAttribute('size')||1)>1);
      checkType(s,16,24,400,name,e.tagName==='SELECT');
      assert(e.tagName==='TEXTAREA' ? r.height>=119 : listbox ? r.height>=48 : Math.abs(r.height-48)<1,name+': field height');
      assert(near(s.paddingTop,11) && near(s.paddingBottom,11) && near(s.paddingInlineStart,16) && near(s.paddingInlineEnd,select&&!listbox?46:16),name+': field padding');
      if (select) {
        const icon=getComputedStyle(e.parentElement,'::after');
        m.indicator={content:icon.content, mask:icon.maskImage, width:icon.width, height:icon.height,
          inset:icon.marginInlineEnd, pointerEvents:icon.pointerEvents, direction:s.direction};
        assert(listbox ? s.appearance==='auto' && ['none','normal'].includes(icon.content) :
          s.appearance==='none' && icon.content==='""' && icon.maskImage.includes('ChevronDownIcon.svg') &&
          near(icon.width,18) && near(icon.height,18) && near(icon.marginInlineEnd,17) &&
          icon.pointerEvents==='none',name+': native select indicator');
      }
    }
    if (e.matches('.tide-choice')) {
      checkType(s,14,24,400,name);
      assert(r.height>=43,name+': choice target');
    }
    if (e.matches('.tide-chip, .tide-expandable__summary')) {
      const disclosure=e.matches('.tide-expandable__summary');
      checkType(s,14,disclosure?24:22,550,name);
      assert(r.height>=(disclosure?47:43),name+': target');
      assert(near(s.paddingTop,disclosure?11:10) && near(s.paddingBottom,disclosure?11:10) && near(s.paddingLeft,16) && near(s.paddingRight,16),name+': padding');
    }
    if (e.matches('.tide-choice, .tide-chip') && e.querySelector('input')) {
      const input=e.querySelector('input'), rect=input.getBoundingClientRect();
      m.input={checked:input.checked, disabled:input.matches(':disabled'), width:rect.width, height:rect.height};
      assert(Math.abs(rect.width-18)<1 && Math.abs(rect.height-18)<1,name+': native glyph');
    }
    if (e.matches('.tide-expandable__summary')) {
      const pseudo=getComputedStyle(e,'::after'), icon=e.querySelector('.tide-expandable__icon');
      m.indicator={fallback:pseudo.content, mask:pseudo.maskImage, transform:pseudo.transform,
        explicit:Boolean(icon), explicitTransform:icon ? getComputedStyle(icon).transform : null};
      assert(icon ? pseudo.content==='none' || pseudo.content==='normal' : pseudo.content==='""' && pseudo.maskImage.includes('ChevronDownIcon.svg'),name+': exactly one chevron');
      if (icon) assert(Math.abs(icon.getBoundingClientRect().width-18)<1,name+': explicit glyph');
    }
    if (e.matches('.tide-upload')) {
      const input=e.querySelector('input[type="file"]'), inputStyle=getComputedStyle(input), button=getComputedStyle(input,'::file-selector-button');
      checkType(inputStyle,14,22,400,name+' filename'); checkType(button,14,22,550,name+' selector');
      assert(near(button.minHeight,44) && near(button.paddingTop,10) && near(button.paddingLeft,16),name+': file button geometry');
      assert(near(s.paddingTop,16) && near(s.rowGap,12),name+': upload inset');
      m.file={type:type(inputStyle), buttonType:type(button), minHeight:button.minHeight,
        padding:button.padding, borderStyle:s.borderStyle, disabled:input.matches(':disabled')};
    }
    return m;
  });
  for (const [selector,size,leading,weight] of [
    ['.tide-field__label',14,20,500],['.tide-field__hint',12,20,400],
    ['.tide-field__error',12,20,400],['.tide-fieldset__legend',16,24,550]]) {
    for (const e of document.querySelectorAll(selector)) checkType(getComputedStyle(e),size,leading,weight,e.id||selector);
  }
  const byName=Object.fromEntries(measurements.map(m=>[m.name,m]));
  for (const prefix of ['alignment','rtl']) {
    const select=byName[prefix+'-select'], summary=byName[prefix+'-summary'];
    assert(Math.abs(select.height-summary.height)<1,prefix+': regular control height');
    assert(select.indicator.mask===summary.indicator.mask,prefix+': shared chevron');
  }
  for (const [a,b] of [['context-text','text'],['context-choice','choice'],['context-chip','chip'],['context-summary','summary']]) {
    assert(JSON.stringify(byName[a].type)===JSON.stringify(byName[b].type),a+': context isolation');
    assert(byName[a].padding===byName[b].padding,a+': context padding');
  }
  for (const [a,b] of [['invalid-disabled','disabled'],['chip-disabled-checked','chip-disabled'],['chip-invalid-disabled','chip-disabled'],['chip-fieldset-disabled','chip-disabled'],['chip-link-disabled','chip-disabled'],['choice-disabled-checked','choice-disabled'],['choice-invalid-disabled','choice-disabled'],['choice-fieldset-disabled','choice-disabled'],['upload-invalid-disabled','upload-disabled']]) {
    assert(['color','background','border'].every(p=>byName[a][p]===byName[b][p]),a+': disabled precedence');
  }
  assert(byName['upload-invalid'].file.borderStyle==='solid','invalid upload boundary');
  assert(byName['upload-invalid'].border===byName.invalid.border,'field/upload danger consistency');
  assert(byName['upload-invalid-disabled'].file.borderStyle==='dashed','disabled upload boundary');
  assert(!document.querySelector('[data-control-case="chip-link-disabled"]').hasAttribute('href'),'disabled link destination');
  for (const input of document.querySelectorAll('[required]')) {
    assert(!input.hasAttribute('aria-invalid'),'required authored invalid state');
    assert(!input.matches(':user-invalid'),'untouched native invalid state');
  }
  assert(document.documentElement.scrollWidth<=innerWidth+1,'document horizontal overflow');
  assert(document.scripts.length===0,'browser script boundary');
  return {theme:document.documentElement.dataset.theme,mode:document.documentElement.dataset.mode,
    viewport:[innerWidth,innerHeight], userInvalid:CSS.supports('selector(:user-invalid)'),
    overflow:document.documentElement.scrollWidth-innerWidth, count:measurements.length,failures,measurements};
}
