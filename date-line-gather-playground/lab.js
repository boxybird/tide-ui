'use strict';
const preview=document.querySelector('#event-preview'),form=document.querySelector('#motion-controls'),returnButton=document.querySelector('#return-list'),fullSize=document.querySelector('#full-size');
let currentRoute='';
function options(){const d=new FormData(form);return {strength:d.get('strength'),slow:d.get('slow')==='on',photo:d.get('photo')};}
function updateLink(){const o=options();fullSize.href='app.html?strength='+o.strength+'&pace='+(o.slow?'slow':'normal')+'&photo='+o.photo+currentRoute;}
function send(type,extra={}){preview.contentWindow.postMessage({channel:'date-line-motion',type,...extra},location.origin);}
form.addEventListener('change',()=>{send('configure',{options:options()});updateLink();});preview.addEventListener('load',()=>send('configure',{options:options()}));
returnButton.addEventListener('click',()=>send('close'));document.querySelector('#rehearse').addEventListener('click',()=>send('rehearse'));
addEventListener('message',event=>{if(event.origin!==location.origin||event.source!==preview.contentWindow||event.data?.channel!=='date-line-motion'||event.data.type!=='state')return;const d=event.data;document.documentElement.dataset.previewStrength=d.strength;document.documentElement.dataset.previewView=d.event?'event':'list';currentRoute=d.event?'#event='+d.event:'';returnButton.disabled=!d.event;document.querySelector('#preview-state').textContent=d.event?'THE EVENT':'THE LIST';document.querySelector('#support-status').textContent=d.reduced?'Reduced motion · direct navigation':d.supported?'Native View Transitions · '+d.duration+'ms':'Direct navigation · API unavailable';updateLink();});
