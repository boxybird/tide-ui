/* Runtime contracts without browser dependencies. Browser behavior is also
   exercised against the generated app and its preserved predecessor. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const manifest = JSON.parse(fs.readFileSync(path.join(root, 'consumer-manifest.json'), 'utf8'));
const source = name => fs.readFileSync(path.join(root, 'src/runtime/js', name + '.js'), 'utf8');
let checks = 0;
function test(name, run) { run(); checks++; }
function plain(value) { return JSON.parse(JSON.stringify(value)); }

function realm({ desktop = true, split = true, reducedMotion = false, scope = '', query = '' } = {}) {
  const stored = new Map(), media = new Map(), calls = { scroll: [], focus: [], cancelled: [], window: {} };
  const results = {
    scrollTop: 750, clientTop: 0, dataset: {},
    addEventListener(type, fn) { calls[type] = fn; },
    getBoundingClientRect() { return { top: 120 }; },
    contains(node) { return node === group; },
    querySelector() { return { getBoundingClientRect() { return { height: 96 }; } }; },
    scrollTo(options) { calls.scroll.push(options); }
  };
  const group = {
    getBoundingClientRect() { return { top: 1800 }; },
    querySelector() { return { focus(options) { calls.focus.push(options); } }; }
  };
  const context = vm.createContext({
    URL, URLSearchParams, Date, Map, Set, JSON, Number,
    FormData: class { constructor(items) { this.items = items; } [Symbol.iterator]() { return this.items[Symbol.iterator](); } },
    document: {
      body: { dataset: { venueScope: scope }, classList: { contains() { return desktop; } } },
      querySelector() { return results; }, getElementById(id) { return id === 'month-2026-11' ? group : null; }
    },
    location: { href: 'https://example.test/events/index.html' + query, search: query, pathname: '/events/index.html', origin: 'https://example.test', assign(url) { calls.assigned = url; } },
    history: { state: null, replaceState() {} }, performance: { now() { return 0; }, getEntriesByType() { return []; } },
    requestAnimationFrame() { return 1; }, cancelAnimationFrame(id) { calls.cancelled.push(id); },
    sessionStorage: { getItem(key) { return stored.get(key) ?? null; }, setItem(key, value) { stored.set(key, String(value)); }, removeItem(key) { stored.delete(key); } },
    matchMedia(query) {
      if (!media.has(query)) media.set(query, { matches: query.includes('reduced-motion') ? reducedMotion : query.includes('60rem') ? split : query.includes('75rem') ? desktop : false, addEventListener() {} });
      return media.get(query);
    },
    window: { scrollY: 0, addEventListener(type, fn) { calls.window[type] = fn; }, scrollTo() {} }
  });
  vm.runInContext(source('search-core'), context);
  vm.runInContext(source('app-runtime'), context);
  return { context, app: vm.runInContext('TideApp', context), search: vm.runInContext('TideSearch', context), calls, stored, media };
}

test('all registered scripts parse and have one source home', () => {
  const registered = manifest.behaviorHome.map(name => path.basename(name)).sort();
  assert.deepEqual(registered, fs.readdirSync(path.join(root, 'src/runtime/js')).filter(name => name.endsWith('.js')).sort());
  for (const name of registered) new vm.Script(source(name.slice(0, -3)), { filename: name });
});
test('storage remains optional when browser access throws', () => {
  const r = realm();
  Object.defineProperty(r.context, 'sessionStorage', { get() { throw new Error('Storage blocked'); } });
  assert.equal(r.app.storage.get('key'), null);
  assert.doesNotThrow(() => r.app.storage.set('key', 'value'));
  assert.doesNotThrow(() => r.app.storage.remove('key'));
});
test('storage preserves exact existing values and removals', () => {
  const { app } = realm();
  app.storage.set('key', 'open'); assert.equal(app.storage.get('key'), 'open');
  app.storage.remove('key'); assert.equal(app.storage.get('key'), null);
});
test('historical session keys remain compatible', () => {
  const { keys } = realm().app;
  assert.equal(keys.appliedReturn, 'tide:app-release-1.1.0:applied');
  assert.equal(keys.rail('app-release-1.1.0-bumble-dark'), 'tide:margin-filters:app-release-1.1.0-bumble-dark');
  assert.equal(keys.photo('margin-aligned'), 'tide:reading-widths:photo:margin-aligned');
  assert.equal(keys.navigation('/events/app/'), 'tide:event-navigation:/events/app/');
});
test('media queries retain their distinct layout thresholds', () => {
  const { app, media } = realm();
  for (const name of ['desktop', 'drawer', 'split', 'phone', 'reducedMotion']) app.media(name);
  assert.deepEqual([...media.keys()], ['(min-width: 75rem)', '(width < 75rem)', '(min-width: 60rem)', '(width < 48rem)', '(prefers-reduced-motion: reduce)']);
  assert.equal(app.media('desktop'), app.media('desktop'));
  assert.throws(() => app.media('unknown'), /Unknown app media query/);
});
test('URL scope and inclusive local dates retain normalized state', () => {
  const { app } = realm({ scope: 'sunshine-theater', query: '?q=%20Signal%20&from=2026-10-30&to=2026-10-30&category=music' });
  assert.deepEqual(plain(app.appliedState()), { venue: 'sunshine-theater', q: 'Signal', from: '2026-10-30', to: '2026-10-30', categories: ['music'] });
});
test('form serialization retains repeated categories and ignores invalid values', () => {
  const { app } = realm();
  const state = app.formState([['q', '  An   evening  '], ['category', 'workshop'], ['category', 'music'], ['category', 'unknown'], ['from', '2026-02-30'], ['venue', 'sunshine-theater']]);
  assert.equal(app.destination('search.html?old=1', state).href, 'https://example.test/events/search.html?venue=sunshine-theater&q=An+evening&category=music&category=workshop');
});
test('event labels preserve singular, plural and matching copy', () => {
  const { app } = realm();
  assert.equal(app.eventCount(0), '0 events'); assert.equal(app.eventCount(1), '1 event');
  assert.equal(app.eventCount(54), '54 events'); assert.equal(app.eventCount(1, 'matching'), '1 matching event');
});
test('refinement counts exclude venue and query and count a date range once', () => {
  const { search } = realm();
  const read = query => search.read(new URLSearchParams(query));
  assert.equal(search.refinementCount(read('venue=sunshine-theater&q=Signal')), 0);
  assert.equal(search.refinementCount(read('from=2026-10-30&to=2026-11-30')), 1);
  assert.equal(search.refinementCount(read('to=2026-11-30&category=music&category=comedy')), 3);
});

function navigation(options) {
  const r = realm(options);
  vm.runInContext(source('event-navigation'), r.context);
  return r;
}
function click(r, { href = 'https://example.test/events/index.html#month-2026-11', month = true, linkTarget = '', download = false, ...overrides } = {}) {
  const link = { href, target: linkTarget, hasAttribute() { return download; }, classList: { contains() { return month; } } };
  const event = { button: 0, defaultPrevented: false, metaKey: false, ctrlKey: false, shiftKey: false, altKey: false, target: { closest() { return link; } }, preventDefault() { this.defaultPrevented = true; }, ...overrides };
  r.calls.click(event);
  return event;
}
test('one desktop month jump accounts for the permanent summary', () => {
  const r = navigation(); assert.equal(click(r).defaultPrevented, true);
  assert.deepEqual(plain(r.calls.scroll), [{ top: 2334, behavior: 'auto' }]);
  assert.deepEqual(plain(r.calls.focus), [{ preventScroll: true }]);
});
test('tablet month jumps retain their original offset', () => {
  const r = navigation({ desktop: false }); click(r);
  assert.deepEqual(plain(r.calls.scroll), [{ top: 2430, behavior: 'auto' }]);
});
test('phone and modified month links stay native', () => {
  const phone = navigation({ desktop: false, split: false }); assert.equal(click(phone).defaultPrevented, false);
  for (const overrides of [{ ctrlKey: true }, { metaKey: true }, { shiftKey: true }, { altKey: true }, { button: 1 }, { defaultPrevented: true }]) {
    const r = navigation(); click(r, overrides); assert.equal(r.calls.scroll.length, 0);
  }
});
test('cross-origin and different-document month links stay native', () => {
  for (const href of ['https://other.test/events/index.html#month-2026-11', 'https://example.test/events/other.html#month-2026-11']) {
    const r = navigation(); assert.equal(click(r, { href }).defaultPrevented, false); assert.equal(r.calls.scroll.length, 0);
  }
});
test('a month jump still cancels pending smooth event navigation', () => {
  const r = navigation(); r.context.window.scrollY = 900;
  assert.equal(click(r, { href: 'https://example.test/events/ink-after-dark.html', month: false }).defaultPrevented, true);
  click(r); assert.ok(r.calls.cancelled.includes(1)); assert.equal(r.calls.assigned, undefined);
  assert.equal(r.calls.scroll.length, 1);
});
test('reduced motion keeps event navigation immediate and remembers the list', () => {
  const r = navigation({ reducedMotion: true }); r.context.window.scrollY = 900;
  assert.equal(click(r, { href: 'https://example.test/events/ink-after-dark.html', month: false }).defaultPrevented, false);
  assert.equal(JSON.parse(r.app.storage.get(r.app.keys.navigation('/events/'))).top, 750);
});
test('download and new-window event links retain browser behavior', () => {
  for (const extra of [{ download: true }, { linkTarget: '_blank' }]) {
    const r = navigation(); r.context.window.scrollY = 900;
    assert.equal(click(r, { href: 'https://example.test/events/ink-after-dark.html', month: false, ...extra }).defaultPrevented, false);
    assert.equal(r.calls.cancelled.length, 0);
  }
});
test('photo compatibility rejects foreign/invalid messages and restores originals', () => {
  const r = realm({ query: '?photo=none' });
  const photo = { src: 'original.png', alt: 'Original description', hidden: false, getAttribute() { return this.src; } };
  const hero = { querySelector() { return photo; } };
  const title = { textContent: 'Ink After Dark', closest() { return hero; } };
  r.context.document.currentScript = { src: 'https://example.test/events/runtime/js/preview.js' };
  r.context.document.getElementById = id => id === 'event-title' ? title : null;
  r.context.document.body.classList.add = () => {};
  r.context.document.body.classList.remove = () => {};
  r.context.parent = {};
  vm.runInContext(source('preview'), r.context);
  assert.equal(photo.hidden, true);
  const message = { origin: 'https://example.test', source: r.context.parent, data: { type: 'tide:reading-widths:photo', mode: 'original' } };
  r.calls.window.message({ ...message, origin: 'https://other.test' }); assert.equal(photo.hidden, true);
  r.calls.window.message({ ...message, source: {} }); assert.equal(photo.hidden, true);
  r.calls.window.message({ ...message, data: { ...message.data, mode: 'invalid' } }); assert.equal(photo.hidden, true);
  r.calls.window.message(message); assert.equal(photo.hidden, false); assert.equal(photo.src, 'original.png'); assert.equal(photo.alt, 'Original description');
  r.calls.window.message({ ...message, data: { ...message.data, mode: 'rough' } });
  assert.equal(photo.src, 'https://example.test/events/runtime/js/assets/organizer-upload.png');
  assert.match(photo.alt, /imperfect organizer snapshot/);
});
test('storage and breakpoint ownership cannot spread back into feature scripts', () => {
  for (const name of manifest.behaviorHome.filter(name => !name.endsWith('/app-runtime.js'))) {
    const text = fs.readFileSync(path.join(root, name), 'utf8');
    assert.doesNotMatch(text, /\bsessionStorage\b|\bmatchMedia\(/, name);
  }
  assert.doesNotMatch(source('rail'), /a\.tide-event-group__jump/);
});
console.log(`${checks} app runtime contracts passed.`);
