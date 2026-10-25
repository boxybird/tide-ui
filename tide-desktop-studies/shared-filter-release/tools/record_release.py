"""Record the successor in workspace discovery files, without touching baselines."""
from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
WORKSPACE=ROOT.parent.parent
kit=ROOT/'kit'
p=kit/'screen-map.json'
data=json.loads(p.read_text(encoding='utf-8'))
if not any(row['area']=='Shared search and filters' for row in data):
    data.insert(0,{'area':'Shared search and filters','coverage':'Optional header, scrolling body, pinned actions; clean, one/zero, invalid and applied specimens in all six modes. Host-tested GET, draft count, reset/cancel/clear, keyboard and resize.','status':'Included · Kit 1.3.0; independent consumer verified'})
    p.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
p=WORKSPACE/'research/favorite-design.json'
data=json.loads(p.read_text(encoding='utf-8'))
selected=data['ui_kit_preference']
selected['preserved_previous_kit']='../tide-responsive-app/kit/index.html'
selected['preserved_original_kit']='../tide-ui-kit/index.html'
selected.update({'current_kit':'../tide-desktop-studies/shared-filter-release/kit/index.html',
                 'css_entry':'../tide-desktop-studies/shared-filter-release/kit/css/tide.css',
                 'theme_source':'../tide-desktop-studies/shared-filter-release/kit/tokens/themes.json',
                 'version':'1.3.0',
                 'adoption_release':{'date':'2026-10-24','review':'../tide-desktop-studies/shared-filter-release/index.html','consumer':'../tide-desktop-studies/shared-filter-release/app/index.html','component':'tide-filter-panel','contract':'../tide-desktop-studies/shared-filter-release/kit/docs/SEARCH-FILTERS.md','status':'User-authorized additive release; approved prototype and frozen dependencies preserved'}})
p.write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=WORKSPACE/'AGENTS.md'
intro='''Current maintained successor (2026-10-24): **tide-desktop-studies/shared-filter-release/kit/**, kit **1.3.0**; local4187/shared-filter-release/index.html. The user explicitly requested shipping the shared filter patterns and testing in an independent app copy. `css/filter-panel.css` owns the optional header, scrolling body, pinned footer, status row/count and flush rail modifier. `templates/filter-panel.html` and `tools/filter_panel.py` supply canonical HTML. Existing controls, Badge, Result summary, errors and Empty are reused; all six theme/mode specimens share structure. Primitive/theme inputs and existing component CSS remain unchanged. The consumer at `shared-filter-release/app/` removes extracted private panel classes/styles. Matching, routing, modal focus/snapshot/resize and native scrollbar measurement remain host-owned. First Escape cancels even from a nonempty search field in the copy. Approved `margin-reveal-unified-search/`1.0.2 (72 files), prior kit1.2.1 (180), app1.3.1 (980), original foundation (176) and all earlier studies remain frozen. Do not overwrite or redirect them. Actual Chromium geometry matches desktop/tablet/phone; Firefox/Safari remain explicitly deferred. See the successor's AGENTS.md, docs/ADOPTION.md, kit/docs/SEARCH-FILTERS.md and qa evidence. Further maintained kit work belongs in this successor; older current-kit statements below describe preserved history.

'''
source=p.read_text(encoding='utf-8')
if not source.startswith('Current maintained successor (2026-10-24)'):
    p.write_text(intro+source,encoding='utf-8')
print('Maintained successor recorded; frozen source trees untouched.')
