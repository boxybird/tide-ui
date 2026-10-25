"""Build independent consumer pages from the immutable approved prototype.

Only this successor's app outputs are written. CSS extraction removes old panel
internals; all product data, structure and host geometry are retained.
"""
from pathlib import Path
import argparse
import re
import shutil
import sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[1]
STUDIES=ROOT.parent
WORKSPACE=STUDIES.parent
SOURCE=STUDIES/'margin-reveal-unified-search'
KIT=ROOT/'kit'
APP=ROOT/'app'
CHECK='--check' in sys.argv
sys.path.insert(0,str(KIT/'tools'))
from filter_panel import panel,header

def write(path,content):
    if CHECK:
        assert path.is_file() and path.read_text(encoding='utf-8')==content, 'Stale consumer output: '+str(path)
        return
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(content,encoding='utf-8',newline='\n')

def without_panel_rules(source):
    """Remove complete owned rules while preserving enclosing media/layers."""
    forbidden=('tide-shell__rail','tide-shell__filter-scroll','tide-shell__action-dock',
               'tide-slide-study__scroller','tide-browse-flyout__body',
               'tide-browse-flyout__search-row','tide-width-study__search-')
    output='';start=0
    while True:
        opening=source.find('{',start)
        if opening<0:return output+source[start:]
        depth=1;end=opening+1
        while depth:
            if source[end]=='{':depth+=1
            elif source[end]=='}':depth-=1
            end+=1
        prelude=source[start:opening]
        clean=re.sub(r'/\*.*?\*/','',prelude,flags=re.S).strip()
        body=source[opening+1:end-1]
        if clean.startswith('@'):
            output+=prelude+'{'+without_panel_rules(body)+'}'
        elif not any(word in clean for word in forbidden):
            output+=prelude+'{'+body+'}'
        elif ':where(' in clean:
            # Gutter alignment remains host-owned; the new footer is already flush.
            output+=prelude.replace(',\n      .tide-shell__action-dock','')+'{'+body+'}'
        start=end

def main():
    styles=[WORKSPACE/'tide-responsive-app/css/app.css',STUDIES/'css/studies.css',
      STUDIES/'workbench-widths/widths.css',STUDIES/'half-split-refinements/shell.css',
      STUDIES/'list-rhythm/list-rhythm.css',STUDIES/'lineup-sliding-filters/sliding-filters.css',
      STUDIES/'lineup-reading-widths/reading-widths.css',STUDIES/'contained-widths-search/widths-search.css',
      STUDIES/'contained-margin-filters/margin-filters.css',STUDIES/'margin-reveal-refined/desktop-filters.css',
      STUDIES/'margin-reveal-aligned/sidebar-alignment.css',STUDIES/'margin-reveal-browse-first/browse-flyout.css']
    css='/* Generated host compositions only. Shared panel internals come from kit 1.3.0. */\n'
    for source in styles:
        css+='\n/* Host input: '+str(source.relative_to(WORKSPACE)).replace('\\','/')+' */\n'+without_panel_rules(source.read_text(encoding='utf-8'))+'\n'
    css+='''
@layer tide.filter-host {
  @media (width >= 75rem) {
    .tide-feed-study {
      --tide-shell-panel-height: max(0px, calc(100dvh - var(--tide-shell-panel-top) - var(--tide-app-pane-gap) - var(--tide-unified-search-scrollbar-gutter, 0px)));
    }
    .tide-filter-host__legacy-clear { display: none; }
  }
  @media (width < 75rem) {
    html:has(.tide-browse-flyout__dialog[open]) { overflow: hidden; scrollbar-gutter: stable; }
    .tide-browse-flyout__dialog { max-inline-size: none; max-block-size: none; inset-block-end: auto; }
    .tide-filter-host__fields { padding-block: 0; gap: var(--tide-space-8); }
  }
}
'''
    write(APP/'css/host.css',css)
    scripts={
      'search-core.js':WORKSPACE/'tide-responsive-app/js/search-core.js',
      'event-search.js':WORKSPACE/'tide-responsive-app/js/event-search.js',
      'event-navigation.js':WORKSPACE/'tide-responsive-app/js/event-navigation.js',
      'headings.js':STUDIES/'list-rhythm/headings.js',
      'room.js':STUDIES/'lineup-reading-widths/room.js'}
    for name,source in scripts.items():write(APP/'js'/name,source.read_text(encoding='utf-8'))
    upload=STUDIES/'lineup-reading-widths/assets/organizer-upload.png'
    target=APP/'js/assets/organizer-upload.png'
    if CHECK:assert target.read_bytes()==upload.read_bytes(),'Organizer photo copy is stale'
    else:
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(upload,target)
    for name in ('comedy.png','concert.png'):
        source=WORKSPACE/'tide-responsive-app/assets/images'/name
        target=APP/'assets/images'/name
        if CHECK:assert target.read_bytes()==source.read_bytes(),'Event photo copy is stale: '+name
        else:
            target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    adapter=(STUDIES/'contained-margin-filters/slide-adapter.js').read_text(encoding='utf-8')
    adapter=adapter.replace("scroller.className='tide-shell__filter-scroll tide-slide-study__scroller'", "scroller.className='tide-filter-panel__body'")
    adapter=adapter.replace("dock.className='tide-shell__action-dock'", "dock.className='tide-filter-panel__footer'")
    adapter=adapter.replace("'tide-shell__rail'", "'tide-filter-panel','tide-filter-panel--rail'")
    write(APP/'js/rail.js',adapter)
    controller=(SOURCE/'unified-search.js').read_text(encoding='utf-8')
    replacements={
      'tide-responsive-filters__trigger':'tide-browse-flyout__trigger',
      'tide-responsive-filters__body':'tide-filter-panel__body',
      'tide-responsive-filters__footer':'tide-filter-panel__footer',
      'tide-responsive-filters__title':'tide-filter-panel__title',
      'tide-responsive-filters__count':'tide-filter-panel__count',
      'tide-shell__action-dock':'tide-filter-panel__footer',
      'tide-unified-search__legacy-clear':'tide-filter-host__legacy-clear',
      'tide-responsive-filters__fields':'tide-filter-host__fields',
      'tide-responsive-filters__apply':'tide-button--full',
      "const querySubmit=form.querySelector('button[type=\"submit\"]');":'',
      "const queryRow=form.querySelector('.tide-search-line');":'',
      "statusRow.classList.add('tide-unified-search__status-row');":'',
      "counter.classList.add('tide-unified-search__count');":'',
      "apply.classList.add('tide-unified-search__apply');":"apply.classList.add('tide-button--full');",
      "statusRow.classList.remove('tide-unified-search__status-row');":'',
      "counter.classList.remove('tide-unified-search__count');":'',
      "apply.classList.remove('tide-unified-search__apply');":"apply.classList.remove('tide-button--full');",
      'querySubmit.hidden=true;':'',
      "queryRow.classList.add('tide-browse-flyout__search-row');":'',
      "queryRow.classList.remove('tide-browse-flyout__search-row');":''}
    for old,new in replacements.items():controller=controller.replace(old,new)
    controller=controller.replace("if(event.key!=='Tab')return;", "// A native search input otherwise consumes the first Escape to clear text.\n    if(event.key==='Escape'){event.preventDefault();dismiss();return;}\n    if(event.key!=='Tab')return;")
    # Canonical one-column Field has no separate query submit to hide.
    write(APP/'js/filters.js',controller)
    dialog=panel(opening='<dialog class="tide-filter-panel tide-browse-flyout__dialog" id="responsive-filters" aria-labelledby="responsive-filter-title">',
                 closing='</dialog>',header=header(),reset_attributes=' disabled')
    count=0
    for source in (SOURCE/'demo').glob('*.html'):
        html=source.read_text(encoding='utf-8')
        # Replace the entire stylesheet/script set, not an override stack on old components.
        html=re.sub(r'\s*<link rel="stylesheet"[^>]*>','',html)
        html=re.sub(r'\s*<script\b.*?</script>','',html,flags=re.S)
        assets='<link rel="stylesheet" href="../kit/css/tide.css">\n<link rel="stylesheet" href="css/host.css">\n'
        assets+='\n'.join(f'<script src="js/{name}" defer></script>' for name in ['search-core.js','event-search.js','event-navigation.js','headings.js','filters.js','rail.js','room.js'])
        html=html.replace('</head>',assets+'\n</head>')
        html=html.replace('../../base/kit/','../kit/')
        html=html.replace('../../base/assets/','assets/')
        html=re.sub(r'<dialog\b.*?</dialog>',lambda m:dialog,html,flags=re.S)
        html=html.replace('tide-responsive-filters__trigger ','')
        html=re.sub(r'<div class="tide-search-line tide-width-study__search-row">(.*?)<button\b.*?</button></div>',r'<div class="tide-field">\1</div>',html,flags=re.S)
        write(APP/source.name,html);count+=1
    print(f'{count} independent app pages built; shared CSS and shell adopted.')

if __name__=='__main__':main()
