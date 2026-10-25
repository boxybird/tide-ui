/* Optional build-time authoring. Every delivered frame is plain HTML/CSS. */
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.dirname(fileURLToPath(import.meta.url));
const previous=path.join(path.dirname(root),'refinements');
const studies=JSON.parse(fs.readFileSync(path.join(root,'studies.json'),'utf8'));
for(const dir of ['frames','assets/fonts','assets/images','assets/icons','licenses','qa'])fs.mkdirSync(path.join(root,dir),{recursive:true});
const specs=[
  ['fraunces','Fraunces','100 900','full'],
  ['lora','Lora','400 700','wght'],
  ['literata','Literata','200 900','standard'],
  ['dm-sans','DM Sans','100 1000','wght'],
  ['instrument-sans','Instrument Sans','400 700','wght'],
  ['ibm-plex-sans','IBM Plex Sans','100 700','wght'],
  ['source-sans-3','Source Sans 3','200 900','wght']
];
let fonts='/* Local Latin variable fonts, with their original OFL licenses. */\n';
for(const [slug,family,weight,axis] of specs){
  const file=`${slug}-latin-${axis}-normal.woff2`;
  const pkg=path.join(root,'tooling/node_modules/@fontsource-variable',slug);
  const source=fs.existsSync(pkg)?path.join(pkg,'files',file):path.join(previous,'assets/fonts',file);
  const destination=path.join(root,'assets/fonts',file);
  if(fs.existsSync(source))fs.copyFileSync(source,destination);
  if(!fs.existsSync(destination))throw new Error(`Missing local font: ${file}`);
  const license=fs.existsSync(pkg)?path.join(pkg,'LICENSE'):path.join(previous,'licenses',`${slug}-OFL.txt`);
  if(fs.existsSync(license))fs.copyFileSync(license,path.join(root,'licenses',`${slug}-OFL.txt`));
  fonts+=`@font-face { font-family: '${family}'; font-style: normal; font-weight: ${weight}; font-display: swap; src: url('assets/fonts/${file}') format('woff2'); }\n`;
}
fs.writeFileSync(path.join(root,'fonts.css'),fonts);
fs.writeFileSync(path.join(root,'themes.css'),'/* Semantic optical refinements. Shared anatomy lives in screens.css. */\n@layer themes {\n'+studies.map(s=>`/* ${s.id} ${s.name} — ${s.font} */
[data-study="${s.id}"] {
  --font-title: '${s.family}'; --font-body: '${s.secondary}';
  --surface-base: ${s.bg}; --surface-panel: ${s.panel};
  --text-primary: ${s.text}; --text-secondary: ${s.muted};
  --text-label: ${s.label}; --text-tertiary: ${s.tertiary};
  --accent: ${s.accent}; --line-subtle: ${s.line};
  --inset: ${s.inset}px; --card-pad: ${s.pad}px; --body-size: ${s.body}px;
  --header-size: ${s.header}px; --card-title-size: ${s.card}px; --detail-title-size: ${s.detail}px;
  --detail-leading: ${s.leading}px; --title-weight: ${s.weight};
  --title-tracking: ${s.tracking}; --detail-tracking: ${s.detailTracking}; --softness: ${s.soft};
}`).join('\n\n')+'\n}\n');
const icon=(name,prefix='../')=>`<img class="icon" src="${prefix}assets/icons/${name}.svg" width="20" height="20" alt="" aria-hidden="true">`;
const head=(title,s,kind)=>{
  const font=specs.find(f=>f[1]===s.family);
  return `<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="${s.bg}"><title>${s.id} ${s.name} — ${title} · Burque</title><link rel="preload" href="../assets/fonts/${font[0]}-latin-${font[3]}-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="../fonts.css"><link rel="stylesheet" href="../screens.css"><link rel="stylesheet" href="../themes.css"></head><body class="screen ${kind}-screen" data-study="${s.id}">`;
};
const events=[
  {name:'Desert Frequencies',category:'Music',venue:'Sister',day:23,weekday:'Fri',fullDay:'Friday',time:'8:00 PM',hour:'20:00',price:'$18'},
  {name:'The Late Set',category:'Comedy',venue:'Dry Heat',day:23,weekday:'Fri',fullDay:'Friday',time:'9:30 PM',hour:'21:30',price:'$15'},
  {name:'Ink After Dark',category:'Workshop',venue:'Barelas Print Studio',day:24,weekday:'Sat',fullDay:'Saturday',time:'6:00 PM',hour:'18:00',price:'$32'}
];
function list(s){return head('event list',s,'list')+`
<div class="list-content">
  <header class="list-header">
    <div class="brand-row"><a class="brand" href="../${s.id}-${s.slug}.html" target="_top" aria-label="Burque design study">BURQUE<span aria-hidden="true">.</span></a><span class="saved-label">${icon('BookmarkIcon')}Saved</span></div>
    <div class="weekend-heading"><h1 class="serif">This weekend.</h1><div class="context-row"><span>Albuquerque</span><time datetime="2026-10-23">Oct 23–24, 2026</time></div></div>
  </header>
  <main class="event-list" aria-label="This weekend in Albuquerque">
    ${events.map((e,i)=>`<article class="event-card" aria-labelledby="event-title-${i}">
      ${i===2?`<a class="card-hit-area" href="${s.id}-event.html" aria-label="View Ink After Dark"><span class="sr-only">View Ink After Dark</span></a>`:''}
      <time class="date-rail" datetime="2026-10-${e.day}" aria-label="${e.fullDay}, October ${e.day}, 2026"><span class="day serif" aria-hidden="true">${e.day}</span><span class="weekday" aria-hidden="true">${e.weekday}</span></time>
      <div class="card-content"><div class="card-heading-row"><span class="category">${e.category}</span><span class="save-mark" aria-hidden="true">${icon('BookmarkIcon')}</span></div><h2 class="card-title" id="event-title-${i}">${e.name}</h2><p class="venue">${e.venue}</p><div class="card-meta"><time datetime="2026-10-${e.day}T${e.hour}:00-06:00">${e.time}</time><span class="price">${e.price}</span></div></div>
    </article>`).join('\n')}
  </main>
  <footer class="list-footer">Concept events<span aria-hidden="true">·</span>Demo details</footer>
</div></body></html>\n`;}
const detailContent=fs.readFileSync(path.join(root,'detail-content.inc'),'utf8');
function event(s){return head('Ink After Dark',s,'event')+`
<main>
  <section class="event-hero" aria-labelledby="event-title">
    <img class="hero-photo" src="../assets/images/ink-after-dark.png" width="1024" height="1536" alt="Hands rolling ink at a shared printmaking table, surrounded by prints, tools, and a coffee mug." fetchpriority="high"><div class="photo-shade" aria-hidden="true"></div>
    <header class="event-toolbar"><a class="toolbar-back" href="${s.id}-list.html">${icon('ArrowLeftIcon')}<span>Events</span></a><span class="save-preview" aria-label="Save event, visual preview">${icon('BookmarkIcon')}</span></header>
    <div class="hero-content">
      <div class="event-intro"><span class="category">Workshop <span aria-hidden="true">/</span> 21+</span><h1 id="event-title"><span>Ink After</span> Dark</h1><p class="subtitle">A printmaking social.</p></div>
      <dl class="event-facts"><div><dt class="fact-label">Saturday</dt><dd><time datetime="2026-10-24">October 24, 2026</time></dd></div><div><dt class="fact-label">2 hours</dt><dd><time datetime="2026-10-24T18:00:00-06:00">6:00–8:00 PM</time></dd></div></dl>
      <p class="venue-fact"><span class="fact-label">Where</span><span>Barelas Print Studio</span></p>
      <div class="admission-action"><p class="admission"><strong>$32</strong><span>per person</span></p><a class="primary-action" href="#event-details"><span>Plan this evening</span>${icon('ArrowRightIcon')}</a></div>
      <p class="materials">Materials included</p>
      <a class="detail-cue" href="#event-details"><span>More about the workshop</span>${icon('ArrowDownIcon')}</a>
    </div>
  </section>
  ${detailContent.replace('01-list.html',`${s.id}-list.html`)}
</main></body></html>\n`;}
const rootIcon=name=>icon(name,'');
function pair(s){return `<section class="study" id="study-${s.id}" aria-labelledby="study-title-${s.id}">
  <div class="study-heading"><div><span class="study-index">STILL HOURS / ${s.id}</span><h2 id="study-title-${s.id}">${s.name}</h2><p>${s.title}</p></div><a class="standalone-link" href="${s.id}-${s.slug}.html">Open pair ${rootIcon('ExternalLinkIcon')}</a></div>
  <div class="frame-pair"><figure><figcaption><span>THE LIST</span><a href="frames/${s.id}-list.html" target="_blank" rel="noopener">Open HTML ${rootIcon('ExternalLinkIcon')}</a></figcaption><iframe src="frames/${s.id}-list.html" title="${s.id} ${s.name} event list" width="390" height="844" loading="lazy"></iframe></figure><figure><figcaption><span>INK AFTER DARK</span><a href="frames/${s.id}-event.html" target="_blank" rel="noopener">Open HTML ${rootIcon('ExternalLinkIcon')}</a></figcaption><iframe src="frames/${s.id}-event.html" title="${s.id} ${s.name} opened event" width="390" height="844" loading="lazy"></iframe></figure></div>
  <div class="study-caption"><p>${s.note}</p><dl><div><dt>Type</dt><dd>${s.font}</dd></div><div><dt>Shared edge</dt><dd>${s.inset}px inset · 4px spacing base</dd></div><div><dt>Titles</dt><dd>${s.card} / ${s.detail}px</dd></div></dl></div>
</section>`;}
const galleryHead=title=>`<!doctype html>\n<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${title} · Burque</title><meta name="description" content="Still Hours: a second family of six subtle dark HTML/CSS refinements of Ink After Dark."><link rel="preload" href="assets/fonts/dm-sans-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin><link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="gallery.css"></head><body class="gallery">`;
const nav=studies.map(s=>`<a href="#study-${s.id}"><span>${s.id}</span>${s.name}</a>`).join('');
fs.writeFileSync(path.join(root,'index.html'),galleryHead('Still Hours — six dark refinements')+`
<a class="skip-link" href="#studies">Skip to the six studies</a>
<aside class="gallery-rail"><a class="gallery-wordmark" href="#top">BURQUE<span>.</span></a><p>STILL HOURS / SET TWO</p><nav aria-label="Six studies">${nav}</nav><div class="rail-footer"><a href="design-notes.html">Design notes</a><a href="still-hours.zip" download>Download all six ${rootIcon('ArrowDownIcon')}</a></div></aside>
<main class="gallery-main"><header class="gallery-intro" id="top"><span class="collection-label">BURQUE / STILL HOURS</span><h1>The same evening.<br>A different cadence.</h1><p>A second family of six quiet refinements.<br>Warm charcoal, softer serifs, and a date-led rhythm.</p><div class="comparison-note"><span>Same photo &amp; content</span><span>390 × 844px frames</span><span>Pure HTML &amp; CSS</span></div></header><div id="studies">${studies.map(pair).join('\n')}</div><footer class="collection-footer"><p>One new direction. Six close readings.</p><a href="design-notes.html">Read the design decisions ${rootIcon('ArrowRightIcon')}</a><a href="#top">Back to the first impression</a></footer></main></body></html>\n`);
for(const s of studies){
  fs.writeFileSync(path.join(root,'frames',`${s.id}-list.html`),list(s));
  fs.writeFileSync(path.join(root,'frames',`${s.id}-event.html`),event(s));
  fs.writeFileSync(path.join(root,`${s.id}-${s.slug}.html`),galleryHead(`${s.id} ${s.name}`)+`<main class="single-main"><nav class="single-nav"><a href="index.html#study-${s.id}">${rootIcon('ArrowLeftIcon')}All six studies</a><span>${s.id} / 06</span><a href="design-notes.html">Design notes</a></nav>${pair(s)}</main></body></html>\n`);
}
console.log('Built six Still Hours pairs, twelve static phone frames, and the comparison gallery.');
