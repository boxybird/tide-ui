/* Shared, DOM-independent search rules. Dates compare as local ISO calendar dates. */
const TideSearch = (() => {
  'use strict';
  const categories = ['music', 'comedy', 'workshop'];

  function normalize(value) {
    return String(value).normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLocaleLowerCase('en-US').replace(/[^\p{L}\p{N}]+/gu, ' ').trim();
  }

  function date(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value || '')) return '';
    const parsed = new Date(value + 'T12:00:00Z');
    return Number.isFinite(parsed.getTime()) && parsed.toISOString().slice(0, 10) === value ? value : '';
  }

  function read(params, defaultVenue = '') {
    return {
      venue: (params.get('venue') || defaultVenue) === 'sunshine-theater' ? 'sunshine-theater' : '',
      q: (params.get('q') || '').trim().replace(/\s+/g, ' ').slice(0, 160),
      from: date(params.get('from')),
      to: date(params.get('to')),
      categories: categories.filter(category => params.getAll('category').includes(category))
    };
  }

  function validRange(state) {
    return !state.from || !state.to || state.from <= state.to;
  }

  function active(state) {
    return Boolean(state.q || state.from || state.to || state.categories.length);
  }

  function serialize(state) {
    const params = new URLSearchParams();
    if (state.venue) params.set('venue', state.venue);
    if (state.q) params.set('q', state.q);
    if (state.from) params.set('from', state.from);
    if (state.to) params.set('to', state.to);
    for (const category of state.categories) params.append('category', category);
    return params.toString();
  }

  function matches(event, state) {
    if (!validRange(state)) return false;
    if (state.venue && event.venue !== state.venue) return false;
    if (state.from && event.date < state.from) return false;
    if (state.to && event.date > state.to) return false;
    if (state.categories.length && !state.categories.includes(event.category.toLowerCase())) return false;
    const words = normalize(state.q).split(' ').filter(Boolean);
    const text = normalize(event.search);
    return words.every(word => text.includes(word));
  }

  return Object.freeze({ normalize, read, validRange, active, serialize, matches });
})();

// The same rules are exercised against the committed fixture in Node's test runner.
if (typeof module !== 'undefined' && module.exports) module.exports = TideSearch;
