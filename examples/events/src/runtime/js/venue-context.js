/* Host composition only. Venue identity is an exact context, not a keyword. */
(() => {
  'use strict';
  const params=new URLSearchParams(location.search);
  const scope=params.get('venue')||document.body.dataset.venueScope;
  if(scope==='sunshine-theater'){
    document.body.dataset.venueScope=scope;
    document.getElementById('venue-scope').value=scope;
    const intro=document.querySelector('.tide-slide-study__intro');
    intro.querySelector('.tide-eyebrow').textContent='Venue · Downtown Albuquerque';
    intro.querySelector('#results-title').textContent='Sunshine Theater';
    intro.querySelector('p:not(.tide-eyebrow)').textContent='120 Central Ave SW · Albuquerque';
    document.querySelector('.tide-feed-study__kicker').textContent='Sunshine Theater';
    const home=document.querySelector('.tide-app__nav a[href="index.html"]');home?.removeAttribute('aria-current');
    const venueLink=document.querySelector('.tide-app__nav a[href="sunshine-theater.html"]');venueLink?.setAttribute('aria-current',document.body.classList.contains('tide-app-release--profile')?'page':'location');
    const links=document.createElement('div');links.className='tide-app-release__context';
    const information=document.createElement('a');information.className='tide-link';information.href=document.body.classList.contains('tide-app-release--profile')?'#venue-information':'sunshine-theater.html';information.textContent='Venue details';
    const all=document.createElement('a');all.className='tide-link';all.href='index.html';all.textContent='All events';links.append(information,all);intro.append(links);
    document.querySelector('[for="event-query"]').textContent='Search this venue’s events';
    document.getElementById('event-query').placeholder='An artist, a show…';
    document.getElementById('event-search-form').action='sunshine-theater.html';
    document.querySelectorAll('.tide-app__clear,.tide-app__all-events,.tide-app__filter-actions > a,#empty-results a').forEach(a=>a.href='sunshine-theater.html');
    document.querySelector('.tide-filter-panel__description').textContent='Narrow events at Sunshine Theater. Reset all keeps this venue selected.';
  }
  const results=document.getElementById('results');
  if(params.has('inspect')&&matchMedia('(width >= 60rem)').matches){
    document.addEventListener('DOMContentLoaded',()=>requestAnimationFrame(()=>{
      const card=results.querySelector('.tide-event-card--in-view');if(!card)return;
      const summary=results.querySelector('.tide-slide-study__summary').getBoundingClientRect().height;
      const group=card.closest('.tide-event-group').querySelector('header').getBoundingClientRect().height;
      const top=card.getBoundingClientRect().top-results.getBoundingClientRect().top+results.scrollTop-summary-group;
      results.scrollTo({top:Math.max(0,top),behavior:'instant'});
    }),{once:true});
  }
})();
