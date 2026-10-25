/* Workbench-only composition adapter. Shared search initializes first.
   Move the original control nodes; preserve their form bindings and listeners. */
(() => {
  'use strict';
  const rail = document.querySelector('.tide-study__tools');
  const results = document.getElementById('results');
  if (!rail || !results || !document.getElementById('event-search-form')) return;
  const desktop = matchMedia('(min-width: 75rem)');
  const controls = [...results.children].filter(node =>
    ['tide-app__intro','tide-app__search','tide-app__filter-row','tide-app__filters']
      .some(name => node.classList.contains(name)));
  const slots = controls.map(node => ({node, marker:document.createComment('Workbench control position')}));
  const filters = results.querySelector('.tide-app__filters');
  let originalOpen = false;
  let mounted = false;

  function place() {
    if (desktop.matches === mounted) return;
    const active = document.activeElement;
    const listTop = results.scrollTop;
    if (desktop.matches) {
      originalOpen = filters.open;
      slots.forEach(({node,marker}) => { node.before(marker); rail.append(node); });
      rail.hidden = false;
      filters.open = true;
      mounted = true;
      // The shared navigation helper restored this before controls moved.
      // Keep that offset in the final feed geometry, without smooth scrolling.
      results.scrollTo({top:listTop, behavior:'instant'});
    } else {
      slots.forEach(({node,marker}) => marker.replaceWith(node));
      filters.open = originalOpen;
      rail.hidden = true;
      mounted = false;
    }
    if (controls.some(node => node === active || node.contains(active))) active.focus({preventScroll:true});
  }
  // The moved date fields no longer bubble invalid events through #results.
  // Native validation still needs to reveal a deliberately closed disclosure.
  document.addEventListener('invalid', event => {
    if (mounted && rail.contains(event.target)) filters.open = true;
  }, true);
  desktop.addEventListener('change', place);
  place();
})();
