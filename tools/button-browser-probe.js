// Development-only, read-only Browser Use evaluation. Never shipped to a page.
// Evaluate this function on a generated button-states.html specimen.
() => {
  const failures = [];
  const px = value => Number(value.replace('px', ''));
  const cases = [...document.querySelectorAll('[data-button-case]')].map(element => {
    const style = getComputedStyle(element), bounds = element.getBoundingClientRect();
    const icon = element.querySelector('.tide-icon');
    return {
      case: element.dataset.buttonCase, width: bounds.width, height: bounds.height,
      padding: [style.paddingTop, style.paddingRight, style.paddingBottom, style.paddingLeft].map(px),
      fontSize: px(style.fontSize), lineHeight: px(style.lineHeight), weight: style.fontWeight,
      fontStyle: style.fontStyle, textTransform: style.textTransform, letterSpacing: style.letterSpacing,
      border: px(style.borderTopWidth), color: style.color, background: style.backgroundColor,
      disabled: element.matches(':disabled, [aria-disabled="true"]'),
      iconSize: icon ? [icon.getBoundingClientRect().width, icon.getBoundingClientRect().height] : null,
    };
  });
  const near = (actual, expected) => Math.abs(actual - expected) < .8;
  for (const item of cases) {
    if (item.fontSize !== 14 || item.lineHeight !== 22 || item.weight !== '550') failures.push(item.case+': typography');
    if (item.fontStyle !== 'normal' || item.textTransform !== 'none' || item.letterSpacing !== 'normal') failures.push(item.case+': inherited emphasis');
    if (!near(item.border, 1)) failures.push(item.case+': border reservation');
    if (item.iconSize && !item.iconSize.every(n => near(n, 18))) failures.push(item.case+': icon size');
    const iconOnly = /^(icon-|photo-)/.test(item.case);
    if (iconOnly) {
      const regular = ['icon-regular', 'icon-legacy-regular', 'photo-regular'].includes(item.case);
      if (!near(item.width, regular ? 48 : 44) || !near(item.height, regular ? 48 : 44)) failures.push(item.case+': icon target');
    } else {
      const compact = item.case === 'compact';
      const expected = compact ? [10,16,10,16] : [12,20,12,20];
      if (!item.padding.every((n,i) => near(n,expected[i]))) failures.push(item.case+': padding');
      if (item.height < (compact ? 44 : 48)-.8) failures.push(item.case+': target height');
    }
  }
  const byCase = name => cases.find(item => item.case === name);
  for (const variant of ['primary','secondary','quiet','icon','photo']) {
    const disabled = byCase(variant+'-disabled'), selectedDisabled = byCase(variant+'-pressed-disabled');
    if (!disabled || !selectedDisabled || disabled.color !== selectedDisabled.color || disabled.background !== selectedDisabled.background) failures.push(variant+': disabled precedence');
  }
  if (!near(byCase('body-context').width, byCase('reading-context').width)) failures.push('inherited context width');
  if (!near(byCase('body-context').width, byCase('emphasis-context').width)) failures.push('inherited emphasis width');
  if (document.documentElement.scrollWidth > innerWidth) failures.push('document overflow');
  if (document.scripts.length) failures.push('browser script dependency');
  return {theme:document.documentElement.dataset.theme,mode:document.documentElement.dataset.mode,viewport:[innerWidth,innerHeight],pass:!failures.length,failures,cases};
}
