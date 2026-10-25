/* Local search over the 54 existing HTML cards. GET navigation keeps refresh,
   browser Back and shareable URLs native; event links retain the applied query. */
(() => {
  'use strict';
  const form = document.getElementById('event-search-form');
  if (!form) return; // Saved remains the separately disclosed sample shortlist.
  const results = document.getElementById('results');
  const filters = results.querySelector('.tide-app__filters');
  const from = document.getElementById('event-from');
  const to = document.getElementById('event-to');
  const error = document.getElementById('date-error');
  const query = document.getElementById('event-query');
  const choices = [...results.querySelectorAll('input[name="category"]')];
  const cards = [...results.querySelectorAll('.tide-event-card')];
  const state = TideSearch.read(new URLSearchParams(location.search), document.body.dataset.venueScope || '');
  const active = TideSearch.active(state);
  const encoded = TideSearch.serialize(state);

  function restoreControls() {
    query.value = state.q;
    from.value = state.from;
    to.value = state.to;
    choices.forEach(choice => { choice.checked = state.categories.includes(choice.value); });
    validateDates();
  }
  restoreControls();
  // Browsers may restore unsubmitted form drafts after deferred scripts run.
  // The applied URL remains the source of truth on reload and history traversal.
  window.addEventListener('pageshow', () => requestAnimationFrame(restoreControls));

  function validateDates() {
    const invalid = Boolean(from.value && to.value && from.value > to.value);
    to.setCustomValidity(invalid ? 'Choose an end date on or after the start date.' : '');
    to.setAttribute('aria-invalid', String(invalid));
    error.hidden = !invalid;
    return !invalid;
  }
  from.addEventListener('input', validateDates);
  to.addEventListener('input', validateDates);
  results.addEventListener('invalid', () => { filters.open = true; }, true);
  if (!validateDates()) filters.open = true;

  form.addEventListener('submit', event => {
    event.preventDefault();
    if (!validateDates()) {
      filters.open = true;
      to.reportValidity();
      return;
    }
    const next = new URL(form.action, location.href);
    next.search = TideSearch.serialize(TideSearch.read(new URLSearchParams(new FormData(form))));
    location.assign(next.href);
  });

  const visible = cards.filter(card => {
    card.hidden = !TideSearch.matches(card.dataset, state);
    const link = card.querySelector('.tide-event-card__link');
    const url = new URL(link.getAttribute('href'), location.href);
    url.search = encoded;
    link.href = url.href;
    return !card.hidden;
  });

  function count(number) { return number + (number === 1 ? ' event' : ' events'); }
  const countLabel = count(visible.length) + (state.q ? ' for “' + state.q + '”' : '');
  document.getElementById('result-count').textContent = countLabel;
  if (!document.body.classList.contains('tide-app--event') && active) {
    document.title = countLabel + ' · Burque';
  }

  const groups = [...results.querySelectorAll('.tide-event-group')];
  groups.forEach(group => {
    const total = group.querySelectorAll('.tide-event-card:not([hidden])').length;
    group.hidden = total === 0;
    group.querySelector('.tide-event-group__count').textContent = count(total);
  });
  const months = groups.filter(group => !group.hidden);
  results.querySelectorAll('.tide-event-group__nav').forEach(nav => {
    nav.hidden = months.length < 2;
    nav.querySelectorAll('a').forEach(link => {
      link.hidden = !months.some(group => '#' + group.id === link.getAttribute('href'));
    });
  });

  const filterCount = Number(Boolean(state.from || state.to)) + state.categories.length;
  const summary = filters.querySelector('summary');
  summary.firstChild.textContent = filterCount ? 'Filters · ' + filterCount + ' ' : 'Filters ';
  results.querySelector('.tide-app__clear').hidden = !active;
  if (active) results.querySelector('.tide-app__all-events').hidden = false;
  document.getElementById('filter-badge').hidden = active;

  function dateLabel(value) {
    // Explicit UTC prevents a date-only filter from shifting to the previous day.
    return new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' })
      .format(new Date(value + 'T12:00:00Z'));
  }
  document.getElementById('date-summary').textContent = state.from && state.to
    ? state.from === state.to ? dateLabel(state.from) : dateLabel(state.from) + ' – ' + dateLabel(state.to)
    : state.from ? 'From ' + dateLabel(state.from)
    : state.to ? 'Through ' + dateLabel(state.to) : state.venue ? 'Oct 30–Nov 27, 2026' : 'Oct 23–Nov 29, 2026';

  const empty = document.getElementById('empty-results');
  empty.hidden = visible.length > 0;
  if (!TideSearch.validRange(state)) {
    empty.querySelector('h2').textContent = 'Check your dates.';
    empty.querySelector('p').textContent = 'The end date needs to be on or after the start date.';
  }

  const preview = document.getElementById('event-detail');
  const placeholder = document.getElementById('preview-state');
  const previewSkip = document.querySelector('.tide-app__skip--detail');

  function contextLinks(detail) {
    if (!active && !state.venue) return;
    const destination = new URL(state.venue ? 'sunshine-theater.html' : 'search.html', location.href);
    destination.search = encoded;
    detail.querySelectorAll('a[aria-label="Back to all events"], a.tide-back-link').forEach(link => {
      link.href = destination.href;
      if (link.hasAttribute('aria-label')) link.setAttribute('aria-label', state.venue ? 'Back to venue' : 'Back to results');
      else link.lastChild.textContent = state.venue ? 'Back to venue' : 'Back to results';
    });
  }
  contextLinks(preview);

  function markPreview(card) {
    cards.forEach(item => {
      item.classList.toggle('tide-event-card--in-view', item === card);
      item.querySelector('.tide-event-card__status').hidden = item !== card;
    });
  }

  function showPlaceholder(title, description) {
    preview.hidden = true;
    placeholder.hidden = false;
    document.getElementById('preview-state-title').textContent = title;
    document.getElementById('preview-state-description').textContent = description;
    if (previewSkip) previewSkip.href = '#preview-state';
    markPreview(null);
  }

  if (document.body.classList.contains('tide-app--venue')) { markPreview(null); return; }

  // A real event URL always owns its detail. Filtering submits to search.html,
  // where the preview instead follows the first matching result when needed.
  if (document.body.classList.contains('tide-app--event')) return;
  if (!visible.length) {
    showPlaceholder('Another evening awaits.', 'Widen your search to find something happening nearby.');
    return;
  }
  const selected = visible.find(card => card.classList.contains('tide-event-card--in-view'));
  if (selected) return;

  showPlaceholder('Finding your evening…', 'Loading the first matching event.');
  results.dataset.previewLoading = 'true';
  placeholder.setAttribute('aria-busy', 'true');
  function previewReady() {
    results.dataset.previewLoading = 'false';
    placeholder.removeAttribute('aria-busy');
    window.dispatchEvent(new Event('tide:preview-ready'));
  }
  const first = visible[0];
  const url = new URL(first.querySelector('.tide-event-card__link').href);
  url.search = '';
  // Fetch only another local static HTML page. No API or client router is needed.
  fetch(url.href).then(response => {
    if (!response.ok) throw new Error('Preview unavailable');
    return response.text();
  }).then(html => {
    const source = new DOMParser().parseFromString(html, 'text/html').getElementById('event-detail');
    if (!source) throw new Error('Preview unavailable');
    const detail = document.importNode(source, true);
    // Standalone H1/H2/H3 headings become H2/H3/H4 in the split preview.
    detail.querySelectorAll('h1,h2,h3').forEach(heading => {
      const replacement = document.createElement('h' + (Number(heading.tagName.slice(1)) + 1));
      for (const attr of heading.attributes) replacement.setAttribute(attr.name, attr.value);
      replacement.append(...heading.childNodes);
      heading.replaceWith(replacement);
    });
    contextLinks(detail);
    preview.replaceWith(detail);
    placeholder.hidden = true;
    if (previewSkip) previewSkip.href = '#event-detail';
    markPreview(first);
    previewReady();
  }).catch(() => {
    showPlaceholder('Choose an evening.', 'Open a result to see the full event.');
    previewReady();
  });
})();
