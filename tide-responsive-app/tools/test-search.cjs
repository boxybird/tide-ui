const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const search = require('../js/search-core.js');
const events = JSON.parse(fs.readFileSync(path.join(__dirname, '../data/events.json'), 'utf8'))
  .map(event => ({ ...event, search: ['title','category','venue','subtitle','lead'].map(key => event[key]).join(' ') + (event.category === 'Workshop' ? ' workshops' : '') }));
const state = query => search.read(new URLSearchParams(query));
const find = query => events.filter(event => search.matches(event, state(query)));

test('empty search and cleared controls return all 48 events', () => {
  assert.equal(find('').length, 48);
  assert.equal(find('q=+++&from=&to=').length, 48);
  assert.equal(search.active(state('')), false);
});
test('title search returns one result, ignoring case and punctuation', () => {
  assert.deepEqual(find('q=INK-AFTER+DARK').map(event => event.slug), ['ink-after-dark']);
});
test('title, venue, category and description are searchable; terms combine', () => {
  assert(find('q=Sister').every(event => event.venue === 'Sister'));
  assert.equal(find('q=warm+amplifiers')[0].slug, 'desert-frequencies');
  assert.equal(find('q=workshops').length, events.filter(event => event.category === 'Workshop').length);
  assert.equal(search.normalize('CAFÉ, after-dark!'), 'cafe after dark');
});
test('dates include both boundaries and span October into November', () => {
  const result = find('from=2026-10-31&to=2026-11-01');
  assert(result.some(event => event.date === '2026-10-31'));
  assert(result.some(event => event.date === '2026-11-01'));
  assert(result.every(event => event.date >= '2026-10-31' && event.date <= '2026-11-01'));
});
test('either end of a range can be omitted', () => {
  assert.equal(find('to=2026-10-31').length, 16);
  assert.equal(find('from=2026-11-01').length, 32);
});
test('date and category can narrow to exactly one event', () => {
  assert.deepEqual(find('from=2026-11-01&to=2026-11-01&category=workshop').map(event => event.slug), ['first-sunday-print-exchange']);
});
test('categories combine with OR, then intersect with search and dates', () => {
  const result = find('category=music&category=comedy&from=2026-10-23&to=2026-10-23');
  assert.deepEqual(result.map(event => event.slug), ['desert-frequencies','the-late-set']);
  assert.equal(find('q=desert&category=workshop').length, 0);
});
test('unmatched search, excluded category and dates outside fixture return zero', () => {
  assert.equal(find('q=unfindablexyz').length, 0);
  assert.equal(find('q=ink+after+dark&category=music').length, 0);
  assert.equal(find('from=2026-12-01').length, 0);
});
test('invalid ranges are rejected; malformed dates and unknown parameters are ignored', () => {
  assert.equal(search.validRange(state('from=2026-11-01&to=2026-10-31')), false);
  assert.equal(find('from=2026-11-01&to=2026-10-31').length, 0);
  assert.equal(find('from=2026-02-30&to=invalid&category=unknown&sort=random').length, 48);
});
test('URLs round-trip Unicode, ampersands, dates and multiple categories', () => {
  const initial = state('q=caf%C3%A9+%26+print&from=2026-10-24&category=workshop&category=music&category=music');
  assert.deepEqual(state(search.serialize(initial)), initial);
  assert.equal(initial.categories.length, 2);
  assert.equal(search.serialize(initial).includes('%26'), true);
});
