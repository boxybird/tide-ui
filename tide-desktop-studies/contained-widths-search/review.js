/* Review controls stay outside the product frames. All messages are same-origin. */
(() => {
  const search=document.getElementById('search-layout');
  const photo=document.getElementById('upload-sample');
  const frames=[...document.querySelectorAll('iframe')];
  function sendSearch(frame){frame.contentWindow.postMessage({type:'tide:contained-widths:search',layout:search.value},location.origin);}
  function sendPhoto(frame){frame.contentWindow.postMessage({type:'tide:reading-widths:photo',mode:photo.value},location.origin);}
  search.addEventListener('change',()=>frames.forEach(sendSearch));
  photo.addEventListener('change',()=>frames.forEach(sendPhoto));
  frames.forEach(frame=>{frame.addEventListener('load',()=>{sendSearch(frame);sendPhoto(frame);});sendSearch(frame);sendPhoto(frame);});
})();
