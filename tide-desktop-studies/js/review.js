/* Fit real desktop viewport frames into the comparison page. Review only. */
(() => {
  const picker = document.getElementById('preview-size');
  const frames = [...document.querySelectorAll('.tide-study-review__viewport')];
  function fit() {
    const [width,height] = picker.value.split(',').map(Number);
    frames.forEach(frame => {
      const scale = Math.min(1, frame.clientWidth / width);
      frame.style.setProperty('--tide-study-preview-width', width+'px');
      frame.style.setProperty('--tide-study-preview-height', height+'px');
      frame.style.setProperty('--tide-study-preview-scale', String(scale));
    });
    document.querySelectorAll('.tide-study-review__dimensions').forEach(n => { n.textContent=width+' × '+height+' · live HTML'; });
  }
  const observer = new ResizeObserver(fit);
  frames.forEach(frame => observer.observe(frame));
  picker.addEventListener('change', fit);
  fit();
})();
