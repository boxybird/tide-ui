import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root = path.dirname(fileURLToPath(import.meta.url));
const body = name => fs.readFileSync(path.join(root, 'reference', name), 'utf8')
  .match(/<body[^>]*>([\s\S]*?)<\/body>/i)[1]
  .replaceAll('../assets/', 'assets/')
  .replaceAll('href="baseline-event.html"', 'href="#event=ink"')
  .replaceAll('href="baseline-list.html"', 'href="#"')
  .replace('href="../baseline.html" target="_top"', 'href="#"');
const list = body('baseline-list.html');
const event = body('baseline-event.html');
fs.writeFileSync(path.join(root, 'app.html'), [
  '<!doctype html><html lang="en"><head>',
  '<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">',
  '<meta name="theme-color" content="#111517"><title>Burque — this weekend</title>',
  '<link rel="preload" href="assets/fonts/manrope-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>',
  '<link rel="preload" href="assets/images/ink-after-dark.png" as="image">',
  '<link rel="stylesheet" href="fonts.css"><link rel="stylesheet" href="screens.css">',
  '<link rel="stylesheet" href="themes.css"><link rel="stylesheet" href="cards.css">',
  '<link rel="stylesheet" href="motion.css"><link rel="stylesheet" href="experiments.css"><link rel="stylesheet" href="micro.css"><script src="micro.js" defer></script><script src="app.js" defer></script>',
  '</head><body class="screen list-screen" data-study="01" data-layout="line">',
  '<div id="app">' + list + '</div>',
  '<template id="list-template">' + list + '</template>',
  '<template id="event-template">' + event + '</template>',
  '<div class="save-feedback" role="status" aria-live="polite" aria-atomic="true"></div>',
  '<noscript><p class="script-note">Enable JavaScript to try this motion study.</p></noscript>',
  '</body></html>'
].join('\n'));
console.log('Built app.html from the preserved Date Line frame copies.');
