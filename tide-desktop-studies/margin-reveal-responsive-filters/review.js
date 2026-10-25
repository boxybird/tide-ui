/* Review only: actual responsive HTML viewports, scaled to the review surface. */
(() => {
  document.querySelectorAll('.tide-responsive-filters-review__viewport').forEach(frame=>{
    const width=Number(frame.dataset.width),height=Number(frame.dataset.height);
    frame.style.setProperty('--review-width',width);frame.style.setProperty('--review-height',height);
    const fit=()=>frame.style.setProperty('--review-scale',Math.min(1,frame.clientWidth/width));
    new ResizeObserver(fit).observe(frame);fit();
  });
})();
