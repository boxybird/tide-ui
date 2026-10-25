/* The lineup hierarchy is shared at every width. Search owns the original
   counts and IDs; this helper composes their labels and measures sticky offsets. */
(() => {
  'use strict';
  const results = document.getElementById('results');
  const total = document.getElementById('result-count');
  if (!results || !total || !document.getElementById('event-search-form')) return;
  const months = [...results.querySelectorAll('.tide-lineup__month-title')];
  function span(className, text) {
    const node = document.createElement('span');
    node.className = className; node.textContent = text;
    return node;
  }
  const match = total.textContent.match(/^(\d+\s+events?)(.*)$/s);
  if (match) {
    total.replaceChildren(span('tide-lineup__total-label', match[1]));
    if (match[2]) total.append(span('tide-lineup__query', match[2]));
  }
  months.forEach(title => {
    const original = title.firstChild;
    const match = original.textContent.match(/^(.*?)\s+(\d{4})\s*$/);
    if (!match) return;
    original.replaceWith(span('tide-lineup__month-name', match[1]), document.createTextNode(' '), span('tide-lineup__year', match[2]), document.createTextNode(' '));
  });
  const observer = new ResizeObserver(() => {
    const height = Math.max(0, ...months.map(title => title.parentElement.getBoundingClientRect().height));
    results.style.setProperty('--tide-lineup-month-height', height + 'px');
  });
  months.forEach(title => observer.observe(title.parentElement));
})();
