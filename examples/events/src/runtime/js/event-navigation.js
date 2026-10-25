/* Optional enhancement for the desktop's real HTML event links.
   Let the existing CSS smooth scroll finish before navigating to the next page.
   No wheel interception, content swapping, framework or custom easing loop. */
(() => {
  'use strict';
  const results = document.querySelector('#results');
  if (!results) return;
  const desktop = TideApp.media('split');
  const reduceMotion = TideApp.media('reducedMotion');
  const storageKey = TideApp.keys.navigation(new URL('.', location.href).pathname);
  let pending = null;
  let frame = 0;
  let returnPosition = null;

  function restoreReturnPosition() {
    // A filtered preview may still be a short loading panel on browser Back.
    // Wait for its natural document height before restoring the reading point.
    if (!returnPosition || results.dataset?.previewLoading === 'true') return;
    const saved = returnPosition;
    returnPosition = null;
    requestAnimationFrame(() => {
      results.scrollTo({ top: saved.left, behavior: 'instant' });
      window.scrollTo({ top: saved.top, behavior: 'instant' });
    });
  }
  window.addEventListener('tide:preview-ready', restoreReturnPosition);

  function rememberReturnPosition() {
    try {
      history.replaceState({ ...history.state, tideEventReturn: {
        path: location.pathname, top: window.scrollY, left: results.scrollTop
      } }, '', location.href);
    } catch { /* A normal HTML link still works if history access is restricted. */ }
  }

  function rememberListPosition(url) {
    TideApp.storage.set(storageKey, JSON.stringify({
      path: url.pathname, top: results.scrollTop, at: Date.now()
    }));
  }

  function restoreListPosition() {
    if (!desktop.matches) return;
    try {
      const saved = JSON.parse(TideApp.storage.get(storageKey));
      if (!saved || saved.path !== location.pathname) return;
      TideApp.storage.remove(storageKey);
      if (Number.isFinite(saved.top) && Date.now() - saved.at < 60000) {
        results.scrollTo({ top: saved.top, behavior: 'instant' });
      }
    } catch { /* Keep native navigation usable when storage is unavailable. */ }
  }

  function stopPendingNavigation() {
    if (!pending) return;
    pending = null;
    cancelAnimationFrame(frame);
    window.scrollTo({ top: window.scrollY, behavior: 'instant' });
  }

  function finishNavigation() {
    if (!pending) return;
    const url = pending.url;
    pending = null;
    rememberListPosition(url);
    location.assign(url.href);
  }

  function waitForTop(now) {
    if (!pending) return;
    if (window.scrollY <= 1 || reduceMotion.matches || !desktop.matches || now - pending.started > 3000) {
      finishNavigation();
    } else {
      frame = requestAnimationFrame(waitForTop);
    }
  }

  results.addEventListener('click', event => {
    const link = event.target.closest?.('a.tide-event-card__link, a.tide-event-group__jump');
    if (!link || event.defaultPrevented || !TideApp.primaryClick(event) || link.hasAttribute('download') || (link.target && link.target !== '_self') || !desktop.matches) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin || new URL('.', url).pathname !== new URL('.', location.href).pathname) return;
    if (link.classList.contains('tide-event-group__jump')) {
      const group = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      if (!group || !results.contains(group) || url.pathname !== location.pathname) return;
      event.preventDefault();
      stopPendingNavigation();
      // One month-jump handler owns both tablet and desktop. The permanent
      // desktop summary adds its measured clearance only while mounted.
      const summary = document.body.classList.contains('tide-app--desktop')
        ? results.querySelector('.tide-lineup__summary').getBoundingClientRect().height : 0;
      const top = group.getBoundingClientRect().top - results.getBoundingClientRect().top + results.scrollTop - results.clientTop - summary;
      group.querySelector('.tide-event-group__title')?.focus({ preventScroll: true });
      results.scrollTo({ top: Math.max(0, top), behavior: 'auto' });
      return;
    }
    if (!pending) rememberReturnPosition();
    if (reduceMotion.matches || window.scrollY <= 1) {
      if (pending) stopPendingNavigation();
      rememberListPosition(url);
      return; // Browser follows the real href immediately.
    }
    event.preventDefault();
    pending = { url, started: performance.now() };
    cancelAnimationFrame(frame);
    // 'auto' deliberately reads scroll-behavior from the root CSS rule.
    window.scrollTo({ top: 0, behavior: 'auto' });
    frame = requestAnimationFrame(waitForTop);
  });

  // A deliberate new page-scroll gesture or Escape can interrupt the return.
  window.addEventListener('wheel', event => {
    returnPosition = null;
    if (!results.contains(event.target)) stopPendingNavigation();
  }, { passive: true });
  window.addEventListener('touchstart', event => {
    returnPosition = null;
    if (!results.contains(event.target)) stopPendingNavigation();
  }, { passive: true });
  window.addEventListener('keydown', event => {
    returnPosition = null;
    if (event.key === 'Escape' || (!results.contains(event.target) && ['PageDown','PageUp','Home','End','ArrowDown','ArrowUp',' '].includes(event.key))) stopPendingNavigation();
  });

  restoreListPosition();
  window.addEventListener('pageshow', event => {
    pending = null;
    cancelAnimationFrame(frame);
    const traversal = event.persisted || performance.getEntriesByType('navigation')[0]?.type === 'back_forward';
    const saved = history.state?.tideEventReturn;
    if (desktop.matches && traversal && saved?.path === location.pathname && Number.isFinite(saved.top) && Number.isFinite(saved.left)) {
      returnPosition = saved;
      restoreReturnPosition();
    } else {
      restoreListPosition();
    }
  });
})();
