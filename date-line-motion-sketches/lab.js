'use strict';
const preview = document.querySelector('#event-preview');
const form = document.querySelector('#motion-controls');
const returnButton = document.querySelector('#return-list');
const fullSize = document.querySelector('#full-size');
const descriptions = {
  gather: 'A focused expansion. Title, day and start time carry the connection; supporting facts arrive together.',
  aperture: 'The complete event opens from the selected evening through a growing aperture. One continuous reveal.',
  shutter: 'The title travels as the photograph sweeps across the expanding card. Supporting details settle in together.'
};
let currentRoute = '';
function options() {
  const values = new FormData(form);
  return {motion:values.get('motion'),slow:values.get('slow') === 'on',photo:values.get('photo')};
}
function updateLink() {
  const value = options();
  fullSize.href = 'app.html?motion=' + value.motion + '&pace=' + (value.slow ? 'slow' : 'normal') + '&photo=' + value.photo + currentRoute;
}
function sendOptions() {
  preview.contentWindow.postMessage({channel:'date-line-motion',type:'configure',options:options()}, location.origin);
  document.querySelector('#motion-description').textContent = descriptions[options().motion];
  updateLink();
}
form.addEventListener('change',sendOptions);
preview.addEventListener('load',sendOptions);
returnButton.addEventListener('click',() => preview.contentWindow.postMessage({channel:'date-line-motion',type:'close'},location.origin));
window.addEventListener('message',event => {
  if (event.origin !== location.origin || event.source !== preview.contentWindow || event.data?.channel !== 'date-line-motion') return;
  const data = event.data;
  if (data.type === 'state') {
    document.documentElement.dataset.previewMotion = data.motion;
    document.documentElement.dataset.previewPhoto = data.photo;
    document.documentElement.dataset.previewDuration = data.duration;
    document.documentElement.dataset.previewView = data.event ? 'event' : 'list';
    currentRoute = data.event ? '#event=' + data.event : '';
    returnButton.disabled = !data.event;
    document.querySelector('#preview-state').textContent = data.event ? 'THE EVENT' : 'THE LIST';
    document.querySelector('#support-status').textContent = data.reduced ? 'Reduced motion is on · direct navigation' : data.supported ? 'Native View Transitions available · ' + (data.slow ? 'slow motion' : 'natural pace') : 'View Transitions unavailable · direct navigation';
    updateLink();
  }
});
