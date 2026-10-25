/* Lineup headings persist at every width. Other studies retain desktop-only composition.
   Existing counts, IDs, links and status nodes stay owned by search. */
(() => {
  'use strict';
  const results = document.getElementById('results');
  const total = document.getElementById('result-count');
  if (!results || !total || !document.getElementById('event-search-form')) return;
  const desktop = matchMedia('(min-width: 75rem)');
  const variant = document.body.dataset.feedStudy;
  const totalText = total.textContent;
  const months = [...results.querySelectorAll('.tide-feed-study__month-title')].map(title => ({
    title, original:title.firstChild, text:title.firstChild.textContent,
    count:title.querySelector('.tide-feed-study__month-count')
  }));
  let mounted=false, observer;
  function span(className,text) {
    const node=document.createElement('span');node.className=className;node.textContent=text;return node;
  }
  function place() {
    const shouldCompose=variant==='lineup'||desktop.matches;
    if (shouldCompose===mounted) return;
    if (shouldCompose) {
      const match=totalText.match(/^(\d+\s+events?)(.*)$/s);
      if (match) {
        total.replaceChildren(span('tide-feed-study__total-label',match[1]));
        if(match[2]) total.append(span('tide-feed-study__query',match[2]));
      }
      months.forEach(item => {
        const match=item.text.match(/^(.*?)\s+(\d{4})\s*$/);
        if(!match)return;
        item.name=span('tide-feed-study__month-name',match[1]);
        item.year=span('tide-feed-study__year',match[2]);
        item.original.replaceWith(item.name,document.createTextNode(' '),item.year,document.createTextNode(' '));
        if(variant==='calendar')item.count.classList.add('tide-badge');
        if(variant==='month-index') {
          item.index=span('tide-feed-study__month-index',item.title.closest('.tide-event-group').id.split('-').pop());
          item.index.setAttribute('aria-hidden','true');item.title.before(item.index);
        }
      });
      observer=new ResizeObserver(() => {
        const height=Math.max(0,...months.map(item=>item.title.parentElement.getBoundingClientRect().height));
        results.style.setProperty('--tide-feed-study-heading-height',height+'px');
      });
      months.forEach(item=>observer.observe(item.title.parentElement));
      mounted=true;
    } else {
      observer?.disconnect();total.textContent=totalText;
      months.forEach(item=>{
        if(!item.name)return;
        item.name.nextSibling?.remove();item.year.nextSibling?.remove();item.year.remove();item.name.replaceWith(item.original);
        item.index?.remove();item.count.classList.remove('tide-badge');
      });
      results.style.removeProperty('--tide-feed-study-heading-height');mounted=false;
    }
  }
  desktop.addEventListener('change',place);place();
})();
