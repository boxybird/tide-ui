/* Build-time only. The output contains no browser JavaScript. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
const root = path.dirname(fileURLToPath(import.meta.url));
const workspace = path.dirname(root);
const require = createRequire(path.join(workspace, 'burque-pocket/package.json'));
const React = require('react');
const { renderToStaticMarkup } = require('react-dom/server');
const icons = require('@radix-ui/react-icons');
for (const dir of ['assets/fonts', 'assets/images', 'assets/icons', 'licenses', 'frames', 'qa']) fs.mkdirSync(path.join(root, dir), { recursive: true });

const fontSpecs = [
  ['manrope', 'Manrope', '200 800'],
  ['source-sans-3', 'Source Sans 3', '200 900'],
  ['newsreader', 'Newsreader', '200 800'],
  ['dm-sans', 'DM Sans', '100 1000'],
  ['ibm-plex-sans', 'IBM Plex Sans', '100 700'],
  ['instrument-sans', 'Instrument Sans', '400 700'],
];
let faces = '/* Locally hosted Latin variable fonts. No third-party browser requests. */\n';
for (const [slug, family, weight] of fontSpecs) {
  const pkg = path.join(root, 'tooling/node_modules/@fontsource-variable', slug);
  const file = `${slug}-latin-${slug === 'newsreader' ? 'standard' : 'wght'}-normal.woff2`;
  fs.copyFileSync(path.join(pkg, 'files', file), path.join(root, 'assets/fonts', file));
  fs.copyFileSync(path.join(pkg, 'LICENSE'), path.join(root, 'licenses', `${slug}-OFL.txt`));
  faces += `@font-face { font-family: '${family}'; font-style: normal; font-weight: ${weight}; font-display: swap; src: url('assets/fonts/${file}') format('woff2'); }\n`;
}
const monoPkg = path.join(root, 'tooling/node_modules/@fontsource/ibm-plex-mono');
fs.copyFileSync(path.join(monoPkg, 'files/ibm-plex-mono-latin-400-normal.woff2'), path.join(root, 'assets/fonts/ibm-plex-mono-latin-400-normal.woff2'));
fs.copyFileSync(path.join(monoPkg, 'LICENSE'), path.join(root, 'licenses/ibm-plex-mono-OFL.txt'));
faces += "@font-face { font-family: 'IBM Plex Mono'; font-style: normal; font-weight: 400; font-display: swap; src: url('assets/fonts/ibm-plex-mono-latin-400-normal.woff2') format('woff2'); }\n";
fs.writeFileSync(path.join(root, 'fonts.css'), faces);
fs.copyFileSync(path.join(workspace, 'burque-pocket/public/images/workshop.png'), path.join(root, 'assets/images/ink-after-dark.png'));
fs.copyFileSync(path.join(workspace, 'burque-pocket/public/images/dots.png'), path.join(root, 'assets/images/quiet-dots.png'));
fs.copyFileSync(path.join(workspace, 'burque-pocket/node_modules/@radix-ui/react-icons/LICENSE'), path.join(root, 'licenses/radix-icons-MIT.txt'));
const iconNames = ['BookmarkIcon', 'Cross1Icon', 'ArrowRightIcon', 'ArrowDownIcon', 'ArrowLeftIcon', 'CalendarIcon', 'ClockIcon', 'SewingPinIcon', 'CheckIcon', 'ChevronDownIcon', 'ExternalLinkIcon'];
for (const name of iconNames) {
  const svg = renderToStaticMarkup(React.createElement(icons[name], { width: 24, height: 24, 'aria-hidden': true }));
  // SVG path data comes directly from the Radix icon package, not custom artwork.
  fs.writeFileSync(path.join(root, 'assets/icons', `${name}.svg`), svg.replaceAll('currentColor', '#f0f0ed'));
}

export const studies = [
  { id:'01', slug:'soft-focus', name:'Soft Focus', family:'Manrope', secondary:'Manrope', title:'A quieter, more deliberate baseline.', note:'Open counters, a medium title weight, and a warm neutral accent. A 24px content inset gives the type and the photo the same left edge.', font:'Manrope throughout', rhythm:'24px inset · 4px spacing base', scale:'24 / 36px titles', card:24, detail:36, inset:24, weight:580, bg:'#111517', panel:'#1a1f22', text:'#f0f1ed', muted:'#b8bfc6', accent:'#edbd8b', label:'#aab3ba', tracking:'-0.032em', detailTracking:'-0.04em', body:14, radius:12, density:'Balanced', spacing:'16px after the venue; 24px between major detail groups.' },
  { id:'02', slug:'humanist', name:'Humanist', family:'Source Sans 3', secondary:'Source Sans 3', title:'Softer reading, cleaner information.', note:'A humanist sans with clear numerals and a slightly larger optical size. The rhythm stays compact without tightening the line height.', font:'Source Sans 3 throughout', rhythm:'24px inset · 4px spacing base', scale:'26 / 38px titles', card:26, detail:38, inset:24, weight:570, bg:'#131617', panel:'#1b2021', text:'#f3f0e9', muted:'#bfc3bf', accent:'#e1c4a0', label:'#b3bab5', tracking:'-0.018em', detailTracking:'-0.025em', body:16, radius:10, density:'Easy reading', spacing:'26px titles optically match the smaller x-height; body text sits on a 20px line.' },
  { id:'03', slug:'warm-editorial', name:'Warm Editorial', family:'Newsreader', secondary:'DM Sans', title:'A small editorial inflection.', note:'A restrained serif for event names, paired with a quiet sans for everything practical. The original composition and photo still do the work.', font:'Newsreader + DM Sans', rhythm:'24px inset · 4px spacing base', scale:'28 / 40px titles', card:28, detail:40, inset:24, weight:480, bg:'#151514', panel:'#211f1c', text:'#f3efe6', muted:'#c0bcb3', accent:'#e8c394', label:'#b7afa1', tracking:'-0.012em', detailTracking:'-0.024em', body:14, radius:8, density:'Warm & editorial', spacing:'Serif titles get 32px lines and 20px of breathing room before the next information group.' },
  { id:'04', slug:'open-form', name:'Open Form', family:'DM Sans', secondary:'DM Sans', title:'Rounder forms, lighter touch.', note:'A generous x-height and softer shapes make a modest weight feel confident. A cool charcoal surface keeps the apricot accent understated.', font:'DM Sans throughout', rhythm:'24px inset · 4px spacing base', scale:'24 / 36px titles', card:24, detail:36, inset:24, weight:530, bg:'#101418', panel:'#1a2026', text:'#f1f1ef', muted:'#b7c0c9', accent:'#e8c2a5', label:'#aab7c3', tracking:'-0.025em', detailTracking:'-0.034em', body:14, radius:14, density:'Soft & open', spacing:'An even 24px card rhythm, 8px local gaps, and slightly rounder action corners.' },
  { id:'05', slug:'studio-notes', name:'Studio Notes', family:'IBM Plex Sans', secondary:'IBM Plex Sans', title:'Precise, with a little character.', note:'Plex gives the listings a studio noticeboard quality. Monospaced category labels add structure while the main reading stays proportional.', font:'IBM Plex Sans + Plex Mono', rhythm:'20px inset · 4px spacing base', scale:'25 / 36px titles', card:25, detail:36, inset:20, weight:550, bg:'#121616', panel:'#1b2221', text:'#eef1eb', muted:'#b6c1bb', accent:'#dcccaa', label:'#b0c0b6', tracking:'-0.02em', detailTracking:'-0.028em', body:14, radius:6, density:'Compact & precise', spacing:'20px edges and a measured 4px rule system; a monospaced label does not take over the body copy.' },
  { id:'06', slug:'quiet-air', name:'Quiet Air', family:'Instrument Sans', secondary:'Instrument Sans', title:'A little more room to settle in.', note:'Fewer heavy weights, more negative space, and a narrower accent range. The larger inset makes the image-led detail feel especially composed.', font:'Instrument Sans throughout', rhythm:'28px inset · 4px spacing base', scale:'24 / 36px titles', card:24, detail:36, inset:28, weight:530, bg:'#101214', panel:'#191d20', text:'#ecefea', muted:'#bac1c5', accent:'#e8cbb2', label:'#b0b9bd', tracking:'-0.025em', detailTracking:'-0.035em', body:14, radius:10, density:'Airy', spacing:'28px shared edges, 20px venue-to-metadata spacing, and 28px separation before the primary action.' },
];
const esc = s => String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('"','&quot;');
const icon = name => `<img class="icon" src="../assets/icons/${name}.svg" width="20" height="20" alt="" aria-hidden="true">`;
const rootIcon = name => `<img class="icon" src="assets/icons/${name}.svg" width="16" height="16" alt="" aria-hidden="true">`;
function head(title, pageClass, study, extra='') {
  const font = fontSpecs.find(f => f[1] === study.secondary) ?? fontSpecs[0];
  const preload = `../assets/fonts/${font[0]}-latin-wght-normal.woff2`;
  return `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="${study.bg}"><title>${title} · Burque</title><link rel="preload" href="${preload}" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="../fonts.css"><link rel="stylesheet" href="../screens.css"><link rel="stylesheet" href="../themes.css">${extra}</head><body class="${pageClass}" data-study="${study.id}">`;
}
const cardData = [
  {title:'Desert Frequencies',category:'Music',venue:'Sister',date:'Fri, Oct 23',time:'8:00 PM',price:'$18'},
  {title:'The Late Set',category:'Comedy',venue:'Dry Heat',date:'Fri, Oct 23',time:'9:30 PM',price:'$15'},
  {title:'Ink After Dark',category:'Workshop',venue:'Barelas Print Studio',date:'Sat, Oct 24',time:'6:00 PM',price:'$32'},
];
function list(study) {
  return head(`${study.id} ${study.name} — event list`, 'screen list-screen', study) + `
  <div class="list-content">
    <header class="list-header">
      <div class="brand-row"><a class="brand" href="../${study.id}-${study.slug}.html" target="_top" aria-label="Burque design study">BURQUE<span aria-hidden="true">.</span></a><span class="saved-label">${icon('BookmarkIcon')}Saved</span></div>
      <div class="context-row"><span class="location">Albuquerque</span><div class="date-context"><span>This weekend</span><time datetime="2026-10-23">Oct 23–24, 2026</time></div></div>
    </header>
    <main class="event-list" aria-label="This weekend in Albuquerque">
      ${cardData.map((e,i) => `<article class="event-card${i === 2 ? ' ink-card' : ''}" aria-labelledby="event-title-${i}">
        ${i===2 ? `<a class="card-hit-area" href="${study.id}-event.html" aria-label="View Ink After Dark"><span class="sr-only">View Ink After Dark</span></a>` : ''}<div class="card-heading-row"><span class="category">${e.category}</span><span class="save-mark" aria-hidden="true">${icon('BookmarkIcon')}</span></div>
        <h2 id="event-title-${i}" class="card-title">${e.title}</h2>
        <p class="venue">${e.venue}</p>
        <div class="card-meta"><time datetime="2026-10-${i===2?'24':'23'}">${e.date}</time><span class="meta-separator" aria-hidden="true"></span><span>${e.time}</span><span class="meta-separator" aria-hidden="true"></span><span class="price">${e.price}</span></div>
      </article>`).join('\n')}
    </main>
    <footer class="list-footer">Concept events<span aria-hidden="true">·</span>Demo details</footer>
  </div>
</body></html>\n`;
}
function event(study) {
  return head(`${study.id} ${study.name} — Ink After Dark`, 'screen event-screen', study) + `
  <main>
    <section class="event-hero" aria-labelledby="event-title">
      <img class="hero-photo" src="../assets/images/ink-after-dark.png" width="1024" height="1536" alt="Hands rolling ink at a shared printmaking table, surrounded by prints, tools, and a coffee mug." fetchpriority="high">
      <div class="photo-shade" aria-hidden="true"></div>
      <header class="event-toolbar"><a class="round-control" href="${study.id}-list.html" aria-label="Back to the event list">${icon('Cross1Icon')}</a><span class="round-control save-preview" aria-label="Save event, visual preview">${icon('BookmarkIcon')}</span></header>
      <div class="hero-content">
        <div class="event-intro"><span class="category">Workshop <span aria-hidden="true">/</span> 21+</span><h1 id="event-title">Ink After Dark</h1><p class="subtitle">A printmaking social.</p></div>
        <dl class="event-facts">
          <div><dt>${icon('CalendarIcon')}<span class="sr-only">Date</span></dt><dd><time datetime="2026-10-24">Saturday, October 24<span class="fact-note">, 2026</span></time></dd></div>
          <div><dt>${icon('ClockIcon')}<span class="sr-only">Time</span></dt><dd><time datetime="2026-10-24T18:00:00-06:00">6:00–8:00 PM</time><span class="fact-note">· 2 hours</span></dd></div>
          <div><dt>${icon('SewingPinIcon')}<span class="sr-only">Venue</span></dt><dd>Barelas Print Studio<span class="fact-note place-note">Albuquerque</span></dd></div>
        </dl>
        <div class="admission"><p><strong>$32</strong><span>per person</span></p><span>Materials included</span></div>
        <a class="primary-action" href="#event-details"><span>Plan this evening</span>${icon('ArrowRightIcon')}</a>
        <a class="detail-cue" href="#event-details"><span>More about the workshop</span>${icon('ArrowDownIcon')}</a>
      </div>
    </section>
    <article class="full-details" id="event-details" aria-labelledby="details-title" tabindex="-1">
      <span class="category">At the worktable</span><h2 id="details-title">A different kind of night out.</h2><p class="lead">Carve a simple block, pull your first print, and settle into an easygoing evening around a shared studio table. Make something imperfect and entirely yours.</p>
      <section class="detail-section"><h3>Your evening includes</h3><ul class="inclusions"><li>${icon('CheckIcon')}All materials and tools</li><li>${icon('CheckIcon')}Guidance from a local printmaker</li><li>${icon('CheckIcon')}One wine or alcohol-free pour</li><li>${icon('CheckIcon')}Your finished prints to take home</li></ul></section>
      <section class="detail-section"><h3>The evening, loosely planned</h3><dl class="schedule"><div><dt>6:00 PM</dt><dd>Meet the table &amp; choose a design</dd></div><div><dt>6:20 PM</dt><dd>Carve your block</dd></div><div><dt>7:00 PM</dt><dd>Ink, roll &amp; pull your first print</dd></div><div><dt>8:00 PM</dt><dd>Pack up your new masterpieces</dd></div></dl></section>
      <section class="detail-section"><h3>Good to know</h3><p>Beginners are welcome. Wear something you’d happily get ink on. Come on your own or bring a friend; everyone shares a worktable.</p><p>This is a 21+ evening. Arrive about 10 minutes early to get settled.</p></section>
      <section class="detail-section"><h3>Finding your way</h3><p class="place">Barelas Print Studio<br><span>Albuquerque, New Mexico</span></p><p>Ask the organizer about step-free access or other access needs before booking.</p></section>
      <p class="demo-disclosure">A fictional evening for a design study. Event details and photography are illustrative; this page does not make a reservation.</p>
      <a class="back-link" href="${study.id}-list.html">${icon('ArrowLeftIcon')}Back to the events</a>
    </article>
  </main>
</body></html>\n`;
}
function pair(study) {
  return `<section class="study" id="study-${study.id}" aria-labelledby="study-title-${study.id}" data-study="${study.id}">
    <div class="study-heading"><div><span class="study-index">REFINEMENT ${study.id}</span><h2 id="study-title-${study.id}">${study.name}</h2><p>${study.title}</p></div><a class="standalone-link" href="${study.id}-${study.slug}.html" aria-label="Open ${study.name} on its own">Open pair ${rootIcon('ExternalLinkIcon')}</a></div>
    <div class="frame-pair"><figure><figcaption><span>THE LIST</span><a href="frames/${study.id}-list.html" target="_blank" rel="noopener">Open HTML ${rootIcon('ExternalLinkIcon')}</a></figcaption><iframe src="frames/${study.id}-list.html" title="${study.id} ${study.name} event list" width="390" height="844" loading="lazy"></iframe></figure><figure><figcaption><span>INK AFTER DARK</span><a href="frames/${study.id}-event.html" target="_blank" rel="noopener">Open HTML ${rootIcon('ExternalLinkIcon')}</a></figcaption><iframe src="frames/${study.id}-event.html" title="${study.id} ${study.name} opened event" width="390" height="844" loading="lazy"></iframe></figure></div>
    <div class="study-caption"><p>${study.note}</p><dl><div><dt>Type</dt><dd>${study.font}</dd></div><div><dt>Rhythm</dt><dd>${study.rhythm}</dd></div><div><dt>Hierarchy</dt><dd>${study.scale}</dd></div></dl></div>
  </section>`;
}
const nav = studies.map(s => `<a href="#study-${s.id}"><span>${s.id}</span>${s.name}</a>`).join('');
const galleryHead = title => `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title}</title><meta name="description" content="Six considered HTML and CSS refinements of Burque’s Ink After Dark mobile event design."><link rel="preload" href="assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="gallery.css"></head><body class="gallery">`;
const intro = `<header class="gallery-intro" id="top"><span class="collection-label">BURQUE / QUIET STUDIES</span><h1>Ink After Dark,<br>refined.</h1><p>Six small shifts in type, space, and tone.<br>The same evening, considered more carefully.</p><div class="comparison-note"><span>Same photo &amp; content</span><span>390 × 844px frames</span><span>Pure HTML &amp; CSS</span></div></header>`;
fs.writeFileSync(path.join(root, 'index.html'), galleryHead('Burque — Six quiet refinements') + `<a class="skip-link" href="#studies">Skip to the six refinements</a><aside class="gallery-rail"><a class="gallery-wordmark" href="#top">BURQUE<span>.</span></a><p>THE REFINEMENT EDIT</p><nav aria-label="Refinements">${nav}</nav><div class="rail-footer"><a href="design-notes.html">Design notes</a><a href="quiet-studies.zip" download>Download all six ${rootIcon('ArrowDownIcon')}</a></div></aside><main class="gallery-main">${intro}<div id="studies">${studies.map(pair).join('\n')}</div><footer class="collection-footer"><p>Same content. Six typographic readings.</p><a href="design-notes.html">Read the design decisions ${rootIcon('ArrowRightIcon')}</a><a href="#top">Back to the first impression</a></footer></main></body></html>\n`);
for (const study of studies) {
  fs.writeFileSync(path.join(root, 'frames', `${study.id}-list.html`), list(study));
  fs.writeFileSync(path.join(root, 'frames', `${study.id}-event.html`), event(study));
  fs.writeFileSync(path.join(root, `${study.id}-${study.slug}.html`), galleryHead(`${study.id} ${study.name} — Burque`) + `<main class="single-main"><nav class="single-nav"><a href="index.html#study-${study.id}">${rootIcon('ArrowLeftIcon')}All six refinements</a><span>${study.id} / 06</span><a href="design-notes.html">Design notes</a></nav>${pair(study)}</main></body></html>\n`);
}
fs.writeFileSync(path.join(root, 'studies.json'), JSON.stringify(studies, null, 2));
console.log('Built six static pairs, twelve standalone frames, one comparison gallery, and local font/icon/image assets.');
