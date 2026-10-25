/* Same-origin review controls, never shown in the app frames. */
(() => {
  const select=document.getElementById('upload-sample');
  const frames=[...document.querySelectorAll('iframe')];
  function send(frame){frame.contentWindow.postMessage({type:'tide:reading-widths:photo',mode:select.value},location.origin);}
  select.addEventListener('change',()=>frames.forEach(send));
  frames.forEach(frame=>{frame.addEventListener('load',()=>send(frame));send(frame);});
})();
