"""Generate complete Tide kits from the preserved component/screen inventory."""
from pathlib import Path
import json,re
from theme_engine import stylesheet,role_colors
root=Path(__file__).parent
source=root.parent/'date-line-ui-kit'
palettes=json.loads((root/'palettes.json').read_text(encoding='utf-8'))
files=list(source.glob('*.html'))+list((source/'frames').glob('*.html'))
for key,palette in palettes.items():
 folder=root if key=='tide' else root/key
 folder.mkdir(exist_ok=True);(folder/'frames').mkdir(exist_ok=True)
 (folder/'theme.css').write_text(stylesheet(palette),encoding='utf-8')
 tokens=json.loads((source/'tokens.json').read_text(encoding='utf-8'))
 tokens['family']='Tide';tokens['skin']=palette['name'];tokens['roles']=role_colors(palette)
 tokens['colors']={'Canvas':palette['base'],'Card':palette['panel'],'Raised':palette['raised'],'Primary text':palette['primary'],'Secondary text':palette['secondary'],'Accent':palette['accent']}
 tokens['semantic'].update({'field':palette['field'],'controlBorder':palette['control'],'success':palette['success'],'warning':palette['warning'],'danger':palette['danger']})
 tokens['radius']={'field':2,'action':2,'documentationPanel':4,'filterChoice':2,'badge':2,'iconControl':2}
 tokens['texture']['opacity']=palette['texture'];tokens['photoSurface']={'canvas':'#111517','accent':palette['heroAccent']};tokens['elevation']='flat';tokens['callouts']={'outline':'uniform neutral','statusCue':'Explicit wording; no left-hand stripe'}
 (folder/'tokens.json').write_text(json.dumps(tokens,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
 for file in files:
  rel=file.relative_to(source);isframe=rel.parts[0]=='frames';depth=(0 if key=='tide' else 1)+(1 if isframe else 0);prefix='../'*depth
  s=file.read_text(encoding='utf-8-sig')
  s=re.sub(r'(?:\.\./)*assets/',prefix+'assets/',s)
  for name in ['fonts.css','screens.css','themes.css','cards.css','ui.css','gallery.css']:
   s=re.sub(r'href="(?:\.\./)*'+re.escape(name)+'"','href="'+prefix+name+'"',s)
  if key!='tide':s=s.replace('href="README.md"','href="'+prefix+'README.md"').replace('href="screen-map.json"','href="'+prefix+'screen-map.json"')
  s=s.replace('</head>','<link rel="stylesheet" href="'+('../theme.css' if isframe else 'theme.css')+'"></head>')
  s=s.replace('name="theme-color" content="#111517"','name="theme-color" content="'+palette['base']+'"')
  if rel.name=='index.html' and not isframe:
   switcher='<section class="kit-switcher" aria-label="Compare Tide palettes"><p>Tide palette studies</p>'
   for section in ['top','foundations','components','screens','coverage']:
    switcher+='<div class="skin-links" data-for="'+section+'">'
    for other,meta in palettes.items():
     href=('../' if key!='tide' else '')+('index.html' if other=='tide' else other+'/index.html')+'#'+section
     switcher+='<a href="'+href+'"'+(' aria-current="true"' if key==other else '')+'>'+meta['name']+'</a>'
    switcher+='</div>'
   switcher+='<p class="skin-caption">'+palette['caption']+'</p></section>'
   s=s.replace('</nav><p class="nav-foot">','</nav>'+switcher+'<p class="nav-foot">')
   s=s.replace('</head>','<link rel="stylesheet" href="'+prefix+'comparison.css"></head>')
   s=s.replace('<title>Date Line — UI kit</title>','<title>Tide / '+palette['name']+' — UI kit</title>')
   s=s.replace('DATE LINE · UI KIT / 0.1','TIDE · PALETTE STUDIES').replace('Date Line / Interface library','Tide / Interface library')
   s=s.replace('One peach primary action per task.','One primary accent per task.')
   s=s.replace('Radius: 8px fields, 12px actions, 16px documentation panels.','Radius: 2px fields, 2px actions, 4px documentation panels.')
   s=s.replace('Warm action. Cool surfaces. Three useful levels of depth.','Semantic roles for surfaces, text, accents and status.')
   for old,new in zip(['#111517','#1a1f22','#232a2e','#f0f1ed','#b8bfc6','#edbd8b'],[palette[v] for v in ['base','panel','raised','primary','secondary','accent']]):
    s=s.replace('background:'+old,'background:'+new).replace(old.upper()+'</code>',new.upper()+'</code>')
   s=s.replace('The originals stay exactly as you chose them.','Tide is the starting point.').replace('Original list</a>','Event list</a>').replace('Original full-screen event</a>','Full-screen event</a>').replace('These copies retain their original HTML, CSS and artwork. New screens below use the same foundations.','Every palette shares the same components, typography, spacing and screen content. Callouts use a plain neutral outline, with no colored left edge.')
   s=s.replace('href="01-date-line.html">View the original','href="'+('../' if key!='tide' else '')+'01-date-line.html">View Tide reference')
   s=s.replace('Date Line / UI kit 0.1 · Static HTML.','Tide / Palette studies · Static HTML.')
  (folder/rel).write_text(s,encoding='utf-8')
print('Built Tide + Mist, Slate and Deep. Uniform callout outlines; shared square geometry.')
