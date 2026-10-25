'use strict';
const events = [
  {id:'desert',title:'Desert Frequencies',category:'Music',venue:'Sister',day:'23',weekday:'Friday',month:'October',date:'2026-10-23',start:'8:00',period:'PM',range:'8:00–11:30 PM',duration:'3½ hours',price:'$18',admission:'Three live sets',image:'concert.png',alt:'A guitarist on a warmly lit bar stage with audience heads in the foreground.',subtitle:'Three bands. One very good room.',heading:'A small room. A big sound.',intro:'Fuzzed-out guitars, slow-burning grooves, and a small room built for a loud night. Three fictional New Mexico bands bring desert-sized sound to an intimate downtown stage.',includes:['Three live sets','Standing room in an intimate venue','Full bar available'],schedule:[['7:00 PM','Doors & a drink'],['8:00 PM','Coyote Radio opens'],['9:00 PM','The Low Suns'],['10:00 PM','Mesa Static']],know:['21+ with photo ID. Standing room only; arrive early for a spot near the stage.','Re-entry is allowed. Earplugs are a good idea.'],cue:'More about the show'},
  {id:'late',title:'The Late Set',category:'Comedy',venue:'Dry Heat',day:'23',weekday:'Friday',month:'October',date:'2026-10-23',start:'9:30',period:'PM',range:'9:30–11:00 PM',duration:'90 minutes',price:'$15',admission:'Seated show',image:'comedy.png',alt:'A comedian with a microphone beside a stool and water glass on a small stage.',subtitle:'Sharp jokes. A small room. A late night.',heading:'Make a night of it.',intro:'A host, four local comics, and ninety minutes of very good stories about questionable decisions. A relaxed late-night showcase with a little room for the unexpected.',includes:['Seated 90-minute show','No two-drink minimum','First-come seating'],schedule:[['9:00 PM','Doors & first-come seating'],['9:30 PM','The host takes the mic'],['11:00 PM','That’s the show']],know:['21+ with photo ID. Adult material. Arrive 20–30 minutes early for your choice of seats.','Please keep phones silent during the show.'],cue:'More about the show'},
  {id:'ink',title:'Ink After Dark',category:'Workshop',venue:'Barelas Print Studio',day:'24',weekday:'Saturday',month:'October',date:'2026-10-24',start:'6:00',period:'PM',range:'6:00–8:00 PM',duration:'2 hours',price:'$32',admission:'Materials included',image:'ink-after-dark.png',alt:'Hands rolling ink at a shared printmaking table, surrounded by prints, tools, and a coffee mug.',subtitle:'A printmaking social.',cue:'More about the workshop'}
];
const app = document.querySelector('#app');
const root = document.documentElement;
const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
const params = new URLSearchParams(location.search);
const settings = {
  motion:'gather',
  strength:params.get('strength') === 'overdrive' ? 'overdrive' : 'expressive',
  slow:params.get('pace') === 'slow',
  photo:params.get('photo') === 'rough' ? 'rough' : 'original'
};
const partNames = ['surface','title','category','day','time'];
let current = null;
let listY = 0;
let savedOnly = false;
let active = null;
let navigation = 0;
let toastTimer;
const detailPositions = new Map();
let saved = new Set();
try { saved = new Set(JSON.parse(localStorage.getItem('burque-motion-saved') || '[]').filter(id => events.some(event => event.id === id))); } catch {}
const cachedImages = new Map();
function imageReady(file) {
  if (!cachedImages.has(file)) {
    const image = new Image();
    image.src = 'assets/images/' + file;
    cachedImages.set(file,image.decode().catch(() => {}));
  }
  return cachedImages.get(file);
}
function photoFor(event) { return settings.photo === 'rough' && event.id === 'ink' ? 'organizer-upload.png' : event.image; }
function applySettings() {
  root.dataset.motion = settings.motion;
  root.dataset.strength = settings.strength;
  const duration = settings.slow ? 2200 : (settings.strength === 'overdrive' ? 1000 : 720);
  root.style.setProperty('--travel-duration',duration + 'ms');
  root.dataset.duration = String(duration);
}
function inform() {
  if (parent !== window) parent.postMessage({channel:'date-line-motion',type:'state',event:current,supported:typeof document.startViewTransition === 'function',reduced:reducedMotion.matches,slow:settings.slow,motion:settings.motion,strength:settings.strength,photo:settings.photo,duration:root.dataset.duration},location.origin);
}
function clone(id) { return document.querySelector(id).content.cloneNode(true); }
function part(element,name) { element.dataset.part = name; return element; }
function icon(name) {
  const image = document.createElement('img');
  image.className = 'icon'; image.src = 'assets/icons/' + name + '.svg'; image.width = 20; image.height = 20; image.alt = ''; image.setAttribute('aria-hidden','true');
  return image;
}
function saveButton(event,round=false) {
  const button = document.createElement('button');
  button.type = 'button'; button.className = round ? 'round-control' : 'save-button';
  button.dataset.save = event.id;
  button.setAttribute('aria-label',(saved.has(event.id) ? 'Unsave ' : 'Save ') + event.title);
  button.setAttribute('aria-pressed',String(saved.has(event.id)));
  button.append(icon('BookmarkIcon'));
  return button;
}
function renderList() {
  const fragment = clone('#list-template');
  fragment.querySelectorAll('.event-card').forEach((card,index) => {
    const event = events[index];
    card.dataset.event = event.id;
    if (savedOnly && !saved.has(event.id)) { card.remove(); return; }
    let link = card.querySelector('.card-hit-area');
    if (!link) { link = document.createElement('a'); link.className = 'card-hit-area'; card.prepend(link); }
    link.href = '#event=' + event.id; link.setAttribute('aria-label','View ' + event.title); link.dataset.open = event.id;
    const surface = document.createElement('div');
    surface.className = 'card-surface'; surface.setAttribute('aria-hidden','true'); part(surface,'surface'); card.prepend(surface);
    const anchor = document.createElement('span'); anchor.className = 'return-anchor'; anchor.setAttribute('aria-hidden','true'); anchor.append(icon('ArrowLeftIcon')); card.append(anchor);
    part(card.querySelector('.card-title'),'title');
    part(card.querySelector('.category'),'category');
    part(card.querySelector('.venue'),'venue');
    part(card.querySelector('.date-day'),'day');
    part(card.querySelector('.date-small > span:first-child'),'weekday');
    part(card.querySelector('.date-small > span:last-child'),'month');
    part(card.querySelector('.price'),'price');
    const time = card.querySelector('.card-meta > time:not(.event-date)');
    time.innerHTML = '<span class="detail-part" data-part="time">' + event.start + '</span> ' + event.period;
    const slot = card.querySelector('.save-mark');
    slot.removeAttribute('aria-hidden'); slot.classList.add('save-slot'); slot.replaceChildren(saveButton(event));
  });
  const savedLabel = fragment.querySelector('.saved-label');
  const toggle = document.createElement('button');
  toggle.type = 'button'; toggle.className = 'saved-label'; toggle.dataset.savedFilter = '';
  toggle.setAttribute('aria-pressed',String(savedOnly));
  toggle.append(icon('BookmarkIcon'),document.createTextNode('Saved' + (saved.size ? ' (' + saved.size + ')' : '')));
  savedLabel.replaceWith(toggle);
  if (savedOnly && !saved.size) {
    const empty = document.createElement('section');
    empty.className = 'empty-saved';
    empty.innerHTML = '<h2>No saved evenings yet.</h2><p>Bookmark an event and it will be waiting here.</p><button type="button" data-show-all>Browse this weekend</button>';
    fragment.querySelector('.event-list').append(empty);
  }
  fragment.querySelector('.brand').removeAttribute('target');
  fragment.querySelector('.brand').setAttribute('aria-label','Burque events');
  app.replaceChildren(fragment);
  document.body.classList.replace('event-screen','list-screen');
  root.dataset.view = 'list'; document.title = 'Burque — this weekend'; current = null;
}
function renderEvent(event) {
  const fragment = clone('#event-template');
  const hero = fragment.querySelector('.event-hero');
  const surface = document.createElement('div');
  surface.className = 'hero-surface'; surface.setAttribute('aria-hidden','true'); part(surface,'surface');
  surface.append(fragment.querySelector('.hero-photo'),fragment.querySelector('.photo-shade'));
  hero.prepend(surface);
  const image = surface.querySelector('img');
  image.src = 'assets/images/' + photoFor(event);
  image.alt = photoFor(event) === 'organizer-upload.png' ? 'A crooked, flash-lit organizer snapshot with a large blank studio wall, blurred hands and a cluttered printmaking table.' : event.alt;
  // The wrapper is decorative for snapshots, but the photo keeps its own alt text.
  surface.removeAttribute('aria-hidden');
  image.addEventListener('error',() => surface.classList.add('image-failed'),{once:true});
  fragment.querySelector('.event-toolbar a').dataset.flight = '';
  const heading = part(fragment.querySelector('#event-title'),'title');
  fragment.querySelector('.hero-content').dataset.reveal = 'content';
  fragment.querySelector('.event-toolbar').dataset.reveal = 'toolbar';
  heading.textContent = event.title; heading.tabIndex = -1;
  const category = fragment.querySelector('.event-intro .category');
  category.innerHTML = '<span data-part="category">' + event.category + '</span> <span aria-hidden="true">/</span> 21+';
  // Keep the original category spacing around the slash, not around the shared word.
  category.querySelector('[data-part]').className = 'category-word';
  fragment.querySelector('.subtitle').textContent = event.subtitle;
  const rows = fragment.querySelectorAll('.event-facts > div');
  rows[0].querySelector('time').dateTime = event.date;
  rows[0].querySelector('time').innerHTML = '<span class="detail-part" data-part="weekday">' + event.weekday + ',</span> <span class="detail-part" data-part="month">' + event.month + '</span> <span class="detail-part" data-part="day">' + event.day + '</span><span class="fact-note">, 2026</span>';
  rows[1].querySelector('time').dateTime = event.date + 'T' + ({desert:'20:00',late:'21:30',ink:'18:00'})[event.id] + ':00-06:00';
  rows[1].querySelector('time').innerHTML = '<span class="detail-part" data-part="time">' + event.start + '</span>' + event.range.slice(event.start.length);
  rows[1].querySelector('.fact-note').textContent = '· ' + event.duration;
  rows[2].querySelector('dd').innerHTML = '<span class="detail-part" data-part="venue">' + event.venue + '</span><span class="fact-note place-note">Albuquerque</span>';
  part(fragment.querySelector('.admission strong'),'price').textContent = event.price;
  fragment.querySelector('.admission > span').textContent = event.admission;
  fragment.querySelector('.save-preview').replaceWith(saveButton(event,true));
  fragment.querySelector('.event-toolbar a').dataset.close = '';
  fragment.querySelector('.back-link').dataset.close = '';
  fragment.querySelector('.detail-cue > span').textContent = event.cue;
  if (event.id !== 'ink') {
    const details = fragment.querySelector('.full-details');
    details.querySelector(':scope > .category').textContent = event.category === 'Music' ? 'In the room' : 'After hours';
    details.querySelector('h2').textContent = event.heading;
    details.querySelector('.lead').textContent = event.intro;
    details.querySelector('.inclusions').replaceChildren(...event.includes.map(text => { const item = document.createElement('li'); item.append(icon('CheckIcon'),document.createTextNode(text)); return item; }));
    details.querySelector('.schedule').replaceChildren(...event.schedule.map(([time,text]) => { const row = document.createElement('div'); const dt = document.createElement('dt'); const dd = document.createElement('dd'); dt.textContent = time; dd.textContent = text; row.append(dt,dd); return row; }));
    const good = details.querySelectorAll('.detail-section')[2];
    good.querySelectorAll('p').forEach(p => p.remove());
    event.know.forEach(text => { const p = document.createElement('p'); p.textContent = text; good.append(p); });
    details.querySelector('.place').innerHTML = event.venue + '<br><span>Albuquerque, New Mexico</span>';
  }
  app.replaceChildren(fragment);
  document.body.classList.replace('list-screen','event-screen');
  root.dataset.view = 'event'; document.title = event.title + ' · Burque'; current = event.id;
}
function selectedParts(id) {
  const scope = current ? app.querySelector('.event-hero') : app.querySelector('[data-event="' + id + '"]');
  return scope ? [...scope.querySelectorAll('[data-part]')] : [];
}
function clearNames() { app.querySelectorAll('[data-part],[data-reveal],[data-flight],.return-anchor').forEach(element => element.style.removeProperty('view-transition-name')); }
function nameParts(id,allowed) {
  clearNames();
  const map = {};
  if (settings.motion === 'aperture') return map;
  if (settings.motion !== 'aperture') app.querySelectorAll('[data-reveal]').forEach(element => {
    const rect = element.getBoundingClientRect();
    if (rect.bottom > 0 && rect.top < innerHeight) element.style.viewTransitionName = 'event-' + element.dataset.reveal;
  });
  selectedParts(id).forEach(element => {
    const name = element.dataset.part;
    if (settings.motion === 'shutter' && !['surface','title'].includes(name)) return;
    if (!partNames.includes(name) || (settings.motion === 'aperture' && name === 'surface') || (allowed && !allowed.has(name))) return;
    const rect = element.getBoundingClientRect();
    if (!rect.width || !rect.height || rect.bottom <= 0 || rect.top >= innerHeight) return;
    element.style.viewTransitionName = 'event-' + name;
    map[name] = {x:rect.x,y:rect.y,width:rect.width,height:rect.height};
  });
  if (root.dataset.direction === 'close') {
    const flight = current ? app.querySelector('[data-close]') : app.querySelector('.is-returning .return-anchor');
    if (flight) { const r = flight.getBoundingClientRect(); if(r.bottom > 0 && r.top < innerHeight) { flight.style.viewTransitionName = 'return-control'; map.returnControl = {x:r.x,y:r.y,width:r.width,height:r.height}; } }
  }
  return map;
}
function getRoute() {
  const id = new URLSearchParams(location.hash.slice(1)).get('event');
  return events.some(event => event.id === id) ? id : null;
}
function syncBaseHistory() {
  if (!current) history.replaceState({...history.state,motionStudy:true,event:null,index:0,listY,savedOnly},'',location.pathname + location.search);
}
async function navigate(id,{historyMode='push',restoreY,focus=true}={}) {
  if (id === current && !active) return;
  const turn = ++navigation;
  const previous = active;
  if (previous) { previous.skipTransition(); await previous.updateCallbackDone.catch(() => {}); }
  if (turn !== navigation) return;
  if (id === current) { active = null; clearNames(); root.dataset.transitionPhase = 'idle'; inform(); return; }
  window.gatherFX?.reset();
  const source = current;
  const event = events.find(event => event.id === id);
  if (event) await imageReady(photoFor(event));
  if (turn !== navigation) return;
  if (!source) { listY = scrollY; if (historyMode !== 'none') syncBaseHistory(); }
  else detailPositions.set(source,scrollY);
  const sharedId = id || source;
  const sourceBox = (source ? app.querySelector('.event-hero') : app.querySelector('[data-event="' + sharedId + '"]'))?.getBoundingClientRect();
  let targetBox;
  applySettings();
  const sourceTitle = source && app.querySelector('[data-part="title"]')?.getBoundingClientRect();
  const titleVisible = !sourceTitle || (sourceTitle.bottom > 0 && sourceTitle.top < innerHeight);
  if (!titleVisible) clearNames();
  root.dataset.direction = id ? 'open' : 'close';
  const from = titleVisible ? nameParts(sharedId) : {};
  root.dataset.transitionKind = titleVisible ? settings.motion : 'dissolve';
  root.dataset.direction = id ? 'open' : 'close';
  root.dataset.transitionPhase = 'capturing';
  const commit = () => {
    if (event) renderEvent(event); else { renderList(); if(from.returnControl) app.querySelector('[data-event="' + sharedId + '"]')?.classList.add('is-returning'); }
    window.scrollTo({top:restoreY ?? (id ? 0 : listY),behavior:'instant'});
    targetBox = (id ? app.querySelector('.event-hero') : app.querySelector('[data-event="' + sharedId + '"]'))?.getBoundingClientRect();
    const to = nameParts(sharedId,new Set(Object.keys(from)));
    root.dataset.motionMap = JSON.stringify({from,to});
    if (historyMode === 'push') history.pushState({motionStudy:true,event:id,index:id ? 1 : 0,listY,savedOnly},'',id ? '#event=' + id : location.pathname + location.search);
    if (historyMode === 'replace') history.replaceState({motionStudy:true,event:id,index:0,listY,savedOnly},'',id ? '#event=' + id : location.pathname + location.search);
    if (focus) {
      const target = id ? app.querySelector('#event-title') : app.querySelector('[data-open="' + sharedId + '"]') || app.querySelector('.brand');
      target?.focus({preventScroll:true});
    }
    inform();
  };
  if (!document.startViewTransition || reducedMotion.matches || params.get('native') === 'off') {
    commit(); clearNames(); app.querySelectorAll('.is-returning').forEach(el => el.classList.remove('is-returning')); root.dataset.transitionPhase = 'idle'; root.dataset.transitionResult = 'direct'; return;
  }
  const customAnimations = [];
  const transition = document.startViewTransition(commit);
  active = transition;
  transition.ready.then(() => {
    if (turn !== navigation) return;
    root.dataset.transitionPhase = 'animating';
    root.dataset.transitionResult = 'native';
    const duration = Number(root.dataset.duration);
    const animate = (name,keyframes,extra={}) => {
      const animation = root.animate(keyframes,{duration,easing:'cubic-bezier(.22,.75,.18,1)',fill:'both',pseudoElement:name,...extra});
      customAnimations.push(animation);
      return animation;
    };
    // Each sketch animates the browser's actual transition snapshots.
    if (root.dataset.transitionKind !== 'dissolve' && settings.motion === 'aperture') {
      const origin = id ? sourceBox : targetBox;
      const x = Math.max(0,Math.min(innerWidth,(origin?.x || 0) + (origin?.width || innerWidth)/2));
      const y = Math.max(0,Math.min(innerHeight,(origin?.y || 0) + (origin?.height || innerHeight)/2));
      const radius = Math.hypot(Math.max(x,innerWidth-x),Math.max(y,innerHeight-y));
      const small = 'circle(24px at ' + x + 'px ' + y + 'px)';
      const full = 'circle(' + radius + 'px at ' + x + 'px ' + y + 'px)';
      animate(id ? '::view-transition-new(root)' : '::view-transition-old(root)',{clipPath:id ? [small,full] : [full,small]});
    }
    if (root.dataset.transitionKind !== 'dissolve' && settings.motion === 'shutter' && from.surface) {
      animate(id ? '::view-transition-new(event-surface)' : '::view-transition-old(event-surface)',{clipPath:id ? ['inset(0 100% 0 0)','inset(0 0% 0 0)'] : ['inset(0 0% 0 0)','inset(0 100% 0 0)']});
    }
    if (root.dataset.transitionKind !== 'dissolve' && settings.motion === 'gather' && from.surface) {
      animate('::view-transition-group(event-surface)',[{borderRadius:'0px'},{borderRadius:'18px',offset:.25},{borderRadius:'0px'}]);
      animate('::view-transition-old(root)',{scale:['1','.985']});
    }
    if (!id && from.returnControl) {
      const over = settings.strength === 'overdrive';
      animate('::view-transition-group(return-control)',[
        {translate:'0 0',rotate:'0deg',scale:'1'},
        {translate:(over ? '85px -90px' : '35px -40px'),rotate:over ? '-115deg' : '-35deg',scale:over ? '1.45' : '1.15',offset:.38},
        {translate:'-8px 10px',rotate:'10deg',scale:'.86',offset:.82},
        {translate:'0 0',rotate:'0deg',scale:'1'}
      ]);
    }
    // The day remains the date's visual anchor; other facts arrive together.
    if (settings.motion !== 'aperture' && from.day) {
      document.documentElement.animate(
        [{translate:'0 0'},{translate:'0 -44px',offset:.5},{translate:'0 0'}],
        {duration:Number(root.dataset.duration),easing:'ease-in-out',pseudoElement:'::view-transition-group(event-day)'}
      );
    }
    const animations = document.getAnimations().filter(animation => animation.effect?.pseudoElement?.startsWith('::view-transition'));
    root.dataset.animationCount = String(animations.length);
    root.dataset.animationNames = JSON.stringify([...new Set(animations.map(animation => animation.effect.pseudoElement))]);
    // Deterministic native-animation checkpoints for the saved visual QA only.
    const checkpoint = Number(params.get('checkpoint'));
    if (checkpoint > 0 && checkpoint < 1) {
      animations.forEach(animation => { animation.pause(); animation.currentTime = Number(root.dataset.duration) * checkpoint; });
      root.dataset.transitionPhase = 'paused';
      root.dataset.checkpoint = String(checkpoint);
      root.dataset.checkpointGeometry = JSON.stringify(partNames.map(name => {
        const style = getComputedStyle(root,'::view-transition-group(event-' + name + ')');
        return {name,transform:style.transform,translate:style.translate,width:style.width,height:style.height};
      }));
    }
  }).catch(() => { if (turn === navigation) root.dataset.transitionResult = 'skipped'; });
  try { await transition.finished; }
  finally {
    customAnimations.forEach(animation => animation.cancel());
    if (turn === navigation) { active = null; clearNames(); root.dataset.transitionPhase = 'idle'; if(!id) window.gatherFX?.land(sharedId); inform(); }
  }
}
function closeEvent() {
  if (!current) return;
  if (history.state?.motionStudy && history.state.index > 0) history.back();
  else navigate(null,{historyMode:'replace'});
}
function toast(message) {
  const output = document.querySelector('.save-feedback');
  output.textContent = message; clearTimeout(toastTimer);
  toastTimer = setTimeout(() => output.textContent = '',1800);
}
function toggleSave(id) {
  const before = new Set(saved);
  if (saved.has(id)) saved.delete(id); else saved.add(id);
  try { localStorage.setItem('burque-motion-saved',JSON.stringify([...saved])); }
  catch { saved = before; toast('Couldn’t save this event in this browser. Please try again.'); return; }
  const event = events.find(event => event.id === id);
  app.querySelectorAll('[data-save="' + id + '"]').forEach(button => {
    button.setAttribute('aria-pressed',String(saved.has(id)));
    button.setAttribute('aria-label',(saved.has(id) ? 'Unsave ' : 'Save ') + event.title);
  });
  if (!current) { const y = scrollY; renderList(); window.scrollTo({top:y,behavior:'instant'}); app.querySelector('[data-save="' + id + '"]')?.focus({preventScroll:true}); }
  window.gatherFX?.save(id,saved.has(id));
  toast(saved.has(id) ? 'Saved to your evenings.' : 'Removed from saved evenings.');
}
app.addEventListener('click',event => {
  const button = event.target.closest('a,button');
  if (!button || (event instanceof MouseEvent && (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey))) return;
  if (button.hasAttribute('data-save')) { event.preventDefault(); toggleSave(button.dataset.save); }
  else if (button.hasAttribute('data-open')) { event.preventDefault(); navigate(button.dataset.open); }
  else if (button.hasAttribute('data-close')) { event.preventDefault(); closeEvent(); }
  else if (button.hasAttribute('data-saved-filter') || button.hasAttribute('data-show-all') || button.classList.contains('brand')) {
    event.preventDefault(); active?.skipTransition(); savedOnly = button.hasAttribute('data-saved-filter') ? !savedOnly : false; listY = 0; renderList(); scrollTo({top:0,behavior:'instant'}); syncBaseHistory();
    app.querySelector('[data-saved-filter]')?.focus({preventScroll:true});
  } else if (button.hash === '#event-details') {
    event.preventDefault(); app.querySelector('#event-details').scrollIntoView({behavior:reducedMotion.matches ? 'instant' : 'smooth'}); app.querySelector('#event-details').focus({preventScroll:true});
  }
});
addEventListener('keydown',event => { if (event.key === 'Escape' && current) { event.preventDefault(); closeEvent(); } });
addEventListener('popstate',event => {
  const target = getRoute();
  if (!target && event.state?.motionStudy) { listY = event.state.listY || 0; savedOnly = !!event.state.savedOnly; }
  navigate(target,{historyMode:'none',restoreY:target ? detailPositions.get(target) || 0 : listY});
});
addEventListener('message',event => {
  if (event.origin !== location.origin || event.source !== parent || event.data?.channel !== 'date-line-motion') return;
  if (event.data.type === 'configure') {
    const value = event.data.options || {};
    settings.strength = value.strength === 'overdrive' ? 'overdrive' : 'expressive';
    settings.motion = 'gather';
    settings.slow = !!value.slow;
    const oldPhoto = settings.photo;
    settings.photo = value.photo === 'rough' ? 'rough' : 'original';
    active?.skipTransition(); applySettings();
    if (oldPhoto !== settings.photo && current === 'ink') { const y = scrollY; renderEvent(events.find(item => item.id === 'ink')); scrollTo({top:y,behavior:'instant'}); }
    inform();
  } else if (event.data.type === 'close') closeEvent();
  else if(event.data.type === 'rehearse') window.gatherFX?.rehearse();
});
reducedMotion.addEventListener('change',() => { if (reducedMotion.matches) active?.skipTransition(); inform(); });
history.scrollRestoration = 'manual';
const initial = getRoute();
applySettings();
if (initial) renderEvent(events.find(event => event.id === initial)); else renderList();
history.replaceState({motionStudy:true,event:initial,index:0,listY:0,savedOnly:false},'',location.href);
root.dataset.transitionPhase = 'idle';
document.fonts.ready.then(inform);
events.forEach(event => imageReady(event.image));
imageReady('organizer-upload.png');
inform();

