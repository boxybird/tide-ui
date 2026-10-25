/* Optional enhancement for the desktop's real HTML event links.
   Let the existing CSS smooth scroll finish before navigating to the next page.
   No wheel interception, content swapping, framework or custom easing loop. */
(() => {
  'use strict';
  const results = document.querySelector('#results');
  if (!results) return;
  const desktop = matchMedia('(min-width: 60rem)');
  const reduceMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const storageKey = 'tide:event-navigation:' + new URL('.', location.href).pathname;
  let pending = null;
  let frame = 0;

  function rememberReturnPosition() {
    try {
      history.replaceState({ ...history.state, tideEventReturn: {
        path: location.pathname, top: window.scrollY, left: results.scrollTop
      } }, '', location.href);
    } catch { /* A normal HTML link still works if history access is restricted. */ }
  }

  function rememberListPosition(url) {
    try {
      sessionStorage.setItem(storageKey, JSON.stringify({
        path: url.pathname, top: results.scrollTop, at: Date.now()
      }));
    } catch { /* Storage is an optional enhancement, including on file: URLs. */ }
  }

  function restoreListPosition() {
    if (!desktop.matches) return;
    try {
      const saved = JSON.parse(sessionStorage.getItem(storageKey));
      if (!saved || saved.path !== location.pathname) return;
      sessionStorage.removeItem(storageKey);
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
    const link = event.target.closest?.('a.tide-event-card__link');
    if (!link || event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey || link.hasAttribute('download') || (link.target && link.target !== '_self') || !desktop.matches) return;
    const url = new URL(link.href);
    if (url.origin !== location.origin || new URL('.', url).pathname !== new URL('.', location.href).pathname) return;
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
    if (!results.contains(event.target)) stopPendingNavigation();
  }, { passive: true });
  window.addEventListener('touchstart', event => {
    if (!results.contains(event.target)) stopPendingNavigation();
  }, { passive: true });
  window.addEventListener('keydown', event => {
    if (event.key === 'Escape' || (!results.contains(event.target) && ['PageDown','PageUp','Home','End','ArrowDown','ArrowUp',' '].includes(event.key))) stopPendingNavigation();
  });

  restoreListPosition();
  window.addEventListener('pageshow', event => {
    pending = null;
    cancelAnimationFrame(frame);
    const traversal = event.persisted || performance.getEntriesByType('navigation')[0]?.type === 'back_forward';
    const saved = history.state?.tideEventReturn;
    if (desktop.matches && traversal && saved?.path === location.pathname && Number.isFinite(saved.top) && Number.isFinite(saved.left)) {
      requestAnimationFrame(() => {
        results.scrollTo({ top: saved.left, behavior: 'instant' });
        window.scrollTo({ top: saved.top, behavior: 'instant' });
      });
    } else {
      restoreListPosition();
    }
  });
})();
