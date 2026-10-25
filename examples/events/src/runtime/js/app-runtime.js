/* App-only shared browser services. No kit components or rendering live here. */
const TideApp = (() => {
  'use strict';
  const queries = Object.freeze({
    desktop: '(min-width: 75rem)',
    drawer: '(width < 75rem)',
    split: '(min-width: 60rem)',
    phone: '(width < 48rem)',
    reducedMotion: '(prefers-reduced-motion: reduce)'
  });
  const mediaQueries = new Map();

  function media(name) {
    if (!Object.hasOwn(queries, name)) throw new Error('Unknown app media query: ' + name);
    if (!mediaQueries.has(name)) mediaQueries.set(name, matchMedia(queries[name]));
    return mediaQueries.get(name);
  }

  // Keep the existing key strings: accepted preview links and session state
  // survive source cleanup. Storage remains optional on restricted/file URLs.
  const keys = Object.freeze({
    appliedReturn: 'tide:app-release-1.1.0:applied',
    rail: stateKey => 'tide:margin-filters:' + stateKey,
    photo: stateKey => 'tide:reading-widths:photo:' + stateKey,
    navigation: directory => 'tide:event-navigation:' + directory
  });
  const storage = Object.freeze({
    get(key) { try { return sessionStorage.getItem(key); } catch { return null; } },
    set(key, value) { try { sessionStorage.setItem(key, value); } catch {} },
    remove(key) { try { sessionStorage.removeItem(key); } catch {} }
  });

  function appliedState() {
    return TideSearch.read(new URLSearchParams(location.search), document.body.dataset.venueScope || '');
  }

  function formState(form) {
    return TideSearch.read(new URLSearchParams(new FormData(form)));
  }

  function destination(href, state) {
    const url = new URL(href, location.href);
    url.search = TideSearch.serialize(state);
    return url;
  }

  function eventCount(number, qualifier = '') {
    return number + (qualifier ? ' ' + qualifier : '') + (number === 1 ? ' event' : ' events');
  }

  function primaryClick(event) {
    return event.button === 0 && !event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey;
  }

  return Object.freeze({ media, keys, storage, appliedState, formState, destination, eventCount, primaryClick });
})();

if (typeof module !== 'undefined' && module.exports) module.exports = TideApp;
