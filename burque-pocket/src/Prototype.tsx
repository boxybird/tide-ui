import { useEffect, useRef, useState, type CSSProperties } from 'react';
import { flushSync } from 'react-dom';
import { ArrowDownIcon, ArrowRightIcon, BookmarkIcon, BookmarkFilledIcon, Cross1Icon, CalendarIcon, ClockIcon, SewingPinIcon, CheckIcon } from '@radix-ui/react-icons';
import { BottomSheet, MobileScroll, useKeyboard, useMobileDevice } from './mobile';
import { events, type Event } from './events';

const fromHash = () => events.find(e => '#event/' + e.id === location.hash) ?? null;
export default function Prototype() {
  const { device } = useMobileDevice();
  const keyboard = useKeyboard();
  const [active, setActive] = useState<Event | null>(fromHash);
  const [transitionId, setTransitionId] = useState<string | null>(null);
  const [saved, setSaved] = useState<string[]>(() => { try { return JSON.parse(localStorage.getItem('pocket-nights-saved') || '[]'); } catch { return []; } });
  const [savedOnly, setSavedOnly] = useState(false);
  const [planOpen, setPlanOpen] = useState(false);
  const [notice, setNotice] = useState('');
  const app = useRef<HTMLDivElement>(null), detail = useRef<HTMLDivElement>(null);
  const pending = useRef(false), activeRef = useRef(active), returnId = useRef<string | null>(active?.id ?? null);
  const timer = useRef<number | undefined>(undefined);
  const height = device.geometry.screen.height - (device.platform === 'android' ? device.geometry.safeArea.bottom : 0);
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches || new URLSearchParams(location.search).get('motion') === 'off';
  const shared = (key: string, enabled: boolean): CSSProperties => ({ viewTransitionName: enabled ? `pocket-${key}` : 'none' });

  useEffect(() => { document.title = 'Burque — Pocket Nights'; events.forEach(e => { const img = new Image(); img.src = e.image; }); }, []);
  useEffect(() => { try { localStorage.setItem('pocket-nights-saved', JSON.stringify(saved)); } catch { /* Session saves remain available. */ } }, [saved]);
  useEffect(() => () => window.clearTimeout(timer.current), []);
  function announce(message: string) { setNotice(message); clearTimeout(timer.current); timer.current = window.setTimeout(() => setNotice(''), 3000); }
  function toggleSaved(e: Event) { const exists = saved.includes(e.id); setSaved(s => exists ? s.filter(id => id !== e.id) : [...s, e.id]); announce(exists ? 'Removed from your nights' : 'Saved to your nights'); }

  async function changeView(next: Event | null) {
    if (pending.current || activeRef.current?.id === next?.id) return;
    pending.current = true; keyboard.hide();
    const id = next?.id ?? activeRef.current?.id ?? null;
    if (next) returnId.current = next.id;
    flushSync(() => { setPlanOpen(false); setTransitionId(id); });
    const change = () => flushSync(() => { activeRef.current = next; setActive(next); });
    app.current?.setAttribute('data-transition-state', 'running');
    try {
      if ('startViewTransition' in document && !reduced()) {
        const transition = document.startViewTransition(change);
        try { await transition.ready; app.current?.setAttribute('data-transition-result', 'animated'); }
        catch { app.current?.setAttribute('data-transition-result', 'skipped'); }
        await transition.finished;
      } else { change(); app.current?.setAttribute('data-transition-result', 'immediate'); }
    } finally {
      flushSync(() => setTransitionId(null)); pending.current = false;
      app.current?.setAttribute('data-transition-state', 'idle');
      if (next) detail.current?.querySelector<HTMLButtonElement>('.close-detail')?.focus({ preventScroll: true });
      else app.current?.querySelector<HTMLButtonElement>(`[data-open="${returnId.current}"]`)?.focus({ preventScroll: true });
      // A browser Back/Forward action can arrive while the snapshots animate.
      if (fromHash()?.id !== activeRef.current?.id) queueMicrotask(() => { void changeView(fromHash()); });
    }
  }
  function openEvent(e: Event) { if (pending.current) return; history.pushState({ pocketEvent: true }, '', '#event/' + e.id); void changeView(e); }
  function closeEvent() { if (pending.current) return; if (history.state?.pocketEvent) history.back(); else { history.replaceState(null, '', location.pathname + location.search); void changeView(null); } }
  useEffect(() => { const onPop = () => { void changeView(fromHash()); }; window.addEventListener('popstate', onPop); return () => window.removeEventListener('popstate', onPop); });
  useEffect(() => {
    if (!active || planOpen) return;
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') { e.preventDefault(); closeEvent(); }
      if (e.key !== 'Tab') return;
      const controls = Array.from(detail.current?.querySelectorAll<HTMLElement>('button, a[href]') ?? []);
      const first = controls[0], last = controls[controls.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last?.focus(); }
      if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first?.focus(); }
    };
    document.addEventListener('keydown', onKey); return () => document.removeEventListener('keydown', onKey);
  });
  function moreDetails() { detail.current?.querySelector('.mobile-scroll')?.scrollTo({ top: height - 40, behavior: reduced() ? 'instant' : 'smooth' }); }
  function calendar(e: Event) {
    const esc = (s: string) => s.replace(/\\/g, '\\\\').replace(/\n/g, '\\n').replace(/,/g, '\\,').replace(/;/g, '\\;');
    const text = ['BEGIN:VCALENDAR','VERSION:2.0','PRODID:-//Burque//Pocket Nights Demo//EN','BEGIN:VEVENT',`UID:${e.id}-2026@burque.demo`,'DTSTAMP:20261020T180000Z',`DTSTART:${e.start}`,`DTEND:${e.end}`,`SUMMARY:${esc(e.title + ' (demo event)')}`,`LOCATION:${esc(e.arrival)}`,'DESCRIPTION:Fictional design event. No booking has been made.','END:VEVENT','END:VCALENDAR',''].join('\r\n');
    const url = URL.createObjectURL(new Blob([text], { type: 'text/calendar;charset=utf-8' }));
    const a = document.createElement('a'); a.href = url; a.download = `${e.id}-demo.ics`; a.click(); setTimeout(() => URL.revokeObjectURL(url), 1000); announce('Demo calendar event downloaded');
  }
  const visible = savedOnly ? events.filter(e => saved.includes(e.id)) : events;
  return <div ref={app} className="burque-app" style={{ '--screen-height': `${height}px`, '--safe-top': `${device.geometry.safeArea.top}px` } as CSSProperties}>
    <div className="list-layer" data-hidden={Boolean(active)} inert={Boolean(active)} aria-hidden={Boolean(active)}>
      <header className="browse-header"><span className="brand">BURQUE<span>.</span></span><button className={`saved-filter ${savedOnly ? 'is-active' : ''}`} aria-pressed={savedOnly} onClick={() => setSavedOnly(!savedOnly)}><BookmarkIcon />{savedOnly ? 'All nights' : 'Saved'}{saved.length > 0 && <span className="saved-count">{saved.length}</span>}</button><div className="browse-context"><span>Albuquerque</span><div>{savedOnly ? 'Your nights' : 'This weekend'}<small>Oct 23–24, 2026</small></div></div></header>
      <MobileScroll className="browse-scroll"><main aria-label={savedOnly ? 'Saved events' : 'This weekend’s events'}>
        {visible.map(e => <article className="event-card" key={e.id} style={shared('surface', transitionId === e.id && !active)}>
          <button className="card-open" data-open={e.id} aria-label={`Open ${e.title}`} onClick={() => openEvent(e)}><span className="category">{e.category}</span><h2 style={shared('title', transitionId === e.id && !active)}>{e.title}</h2><span className="card-venue" style={shared('venue', transitionId === e.id && !active)}>{e.venue}</span><span className="card-meta"><span style={shared('date', transitionId === e.id && !active)}>{e.shortDate}</span><span style={shared('time', transitionId === e.id && !active)}>{e.time}</span><span className="price" style={shared('price', transitionId === e.id && !active)}>{e.price}</span></span></button>
          <button className="card-save" aria-label={`${saved.includes(e.id) ? 'Unsave' : 'Save'} ${e.title}`} aria-pressed={saved.includes(e.id)} onClick={() => toggleSaved(e)}>{saved.includes(e.id) ? <BookmarkFilledIcon /> : <BookmarkIcon />}</button>
        </article>)}
        {!visible.length && <div className="empty-state"><BookmarkIcon /><h2>A good night to look forward to.</h2><p>Save an event and you’ll find it here.</p><button onClick={() => setSavedOnly(false)}>Explore this weekend <ArrowRightIcon /></button></div>}
        <p className="demo-note">Concept events · Demo details</p>
      </main></MobileScroll>
    </div>
    {active && <div className="detail-layer" ref={detail} role="dialog" aria-modal="true" aria-labelledby="detail-title" key={active.id}>
      <div className="detail-controls"><button className="round-control close-detail" onClick={closeEvent} aria-label="Close event"><Cross1Icon /></button><button className="round-control" aria-label={`${saved.includes(active.id) ? 'Unsave' : 'Save'} ${active.title}`} aria-pressed={saved.includes(active.id)} onClick={() => toggleSaved(active)}>{saved.includes(active.id) ? <BookmarkFilledIcon /> : <BookmarkIcon />}</button></div>
      <MobileScroll className="detail-scroll"><article>
        <section className="photo-hero" style={shared('surface', Boolean(transitionId))}>
          <img className="event-photo" src={active.image} alt={active.alt} fetchPriority="high" draggable={false} /><div className="photo-scrim" />
          <div className="hero-content"><span className="category">{active.category} · 21+</span><h1 id="detail-title" style={shared('title', Boolean(transitionId))}>{active.title}</h1><p className="hero-subtitle">{active.subtitle}</p>
            <div className="hero-meta"><div><CalendarIcon /><span style={shared('date', Boolean(transitionId))}>{active.shortDate}</span><span className="hero-year">2026</span></div><div><ClockIcon /><span style={shared('time', Boolean(transitionId))}>{active.time}</span><span className="duration">{active.id === 'ink' ? '– 8:00 PM' : active.id === 'late' ? '· 90 minutes' : '· Doors 7 PM'}</span></div><div><SewingPinIcon /><span style={shared('venue', Boolean(transitionId))}>{active.venue}</span></div><div className="hero-price"><span style={shared('price', Boolean(transitionId))}>{active.price}</span><span>per person · 21+</span></div></div>
            <button className="primary-action" onClick={() => setPlanOpen(true)}>Plan this evening <ArrowRightIcon /></button><button className="more-details" onClick={moreDetails}>More about {active.id === 'ink' ? 'the workshop' : 'the night'} <ArrowDownIcon /></button>
          </div>
        </section>
        <div className="event-story"><span className="eyebrow">A LITTLE MORE TO GO ON</span><h2>{active.id === 'ink' ? 'A different kind of night out.' : active.id === 'late' ? 'Make room for a late laugh.' : 'Come for the sound. Stay for the room.'}</h2><p>{active.intro}</p>
          <section className="story-section"><h3>{active.heading}</h3><ul className="inclusions">{active.lineup.map(item => <li key={item}><CheckIcon />{item}</li>)}</ul></section>
          <section className="story-section"><h3>The evening, loosely planned</h3><dl className="schedule">{active.schedule.map(([time, what]) => <div key={time}><dt>{time}</dt><dd>{what}</dd></div>)}</dl></section>
          <section className="story-section"><h3>Good to know</h3><p>{active.know}</p></section>
          <section className="story-section"><h3>Finding your way</h3><p className="arrival"><SewingPinIcon />{active.arrival}</p><p>{active.arrivalNote}</p></section>
          <section className="story-section ticket-summary"><div><span>YOUR EVENING</span><strong>{active.price}<small> per person</small></strong><p>{active.duration}</p></div><button className="primary-action" onClick={() => setPlanOpen(true)}>Plan this evening <ArrowRightIcon /></button><button className="calendar-action" onClick={() => calendar(active)}><CalendarIcon />Add to calendar</button></section>
          <p className="fiction-note">A little imagination, a lot of New Mexico. Event details, lineups, prices, and images are fictional demo content. No reservations or purchases are made here.</p>
        </div>
      </article></MobileScroll>
      <BottomSheet open={planOpen} onOpenChange={setPlanOpen} title="Make a little room for a good night." description="This is a concept event. Save the plan or try a demo calendar reminder."><div className="plan-content"><h3>{active.title}</h3><p>{active.date}<br />{active.duration}<br />{active.venue} · Albuquerque</p><strong>{active.price} per person · 21+</strong><p>{active.includes.join(' · ')}</p><button className="primary-action" onClick={() => { if (!saved.includes(active.id)) setSaved(s => [...s, active.id]); setPlanOpen(false); announce('Saved to your nights'); }}>{saved.includes(active.id) ? 'Keep this in my nights' : 'Save this evening'}<BookmarkIcon /></button><button className="calendar-action" onClick={() => calendar(active)}><CalendarIcon />Try a calendar reminder</button><small>No booking or payment. All event information is demo data.</small></div></BottomSheet>
    </div>}
    <div className={`toast ${notice ? 'visible' : ''}`} role="status">{notice}</div>
  </div>;
}
