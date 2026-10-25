/* A private app-layout adapter. Reuse original nodes, forms and listeners. */
(() => {
  'use strict';
  const rail = document.querySelector('.tide-study__tools');
  const actions = document.querySelector('.tide-app__filter-actions');
  const query = document.getElementById('event-search-form');
  if (!rail || !actions || !query) return;
  const filters = actions.closest('details');
  const desktop = matchMedia('(min-width: 75rem)');
  const marker = document.createComment('Original filter action position');
  let scroller, dock, observer;

  function place() {
    if (desktop.matches === Boolean(scroller)) return;
    const active = document.activeElement;
    const focusedScroller = active === scroller;
    if (desktop.matches) {
      const priorTop = rail.scrollTop;
      scroller = document.createElement('div');
      scroller.className = 'tide-shell__filter-scroll';
      scroller.tabIndex = 0;
      scroller.setAttribute('role', 'region');
      scroller.setAttribute('aria-label', 'Filter options');
      dock = document.createElement('div');
      dock.className = 'tide-shell__action-dock';
      while (rail.firstChild) scroller.append(rail.firstChild);
      rail.append(scroller, dock);
      actions.before(marker);
      dock.append(actions);
      rail.classList.add('tide-shell__rail');
      scroller.scrollTop = priorTop;
      if (document.body.classList.contains('tide-shell--pinned-search')) {
        const measure = () => scroller?.style.setProperty('--tide-shell-search-height', query.getBoundingClientRect().height+'px');
        observer = new ResizeObserver(measure);
        observer.observe(query);
        measure();
      }
    } else {
      observer?.disconnect();
      marker.replaceWith(actions);
      while (scroller.firstChild) rail.insertBefore(scroller.firstChild, scroller);
      scroller.remove();
      dock.remove();
      rail.classList.remove('tide-shell__rail');
      scroller = dock = null;
    }
    const target = !desktop.matches && (focusedScroller || (filters.contains(active) && !filters.open))
      ? filters.querySelector('summary') : active;
    if (target?.isConnected && target !== document.body) target.focus({preventScroll: true});
  }
  desktop.addEventListener('change', place);
  place();
})();
