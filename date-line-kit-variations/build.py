from pathlib import Path
import shutil,re,json,hashlib
root=Path(__file__).parent
source=root.parent/'date-line-ui-kit'
themes={
 'original':{'name':'Date Line','caption':'Original · Warm peach on charcoal.','base':'#111517','panel':'#1a1f22','raised':'#232a2e','field':'#171d20','primary':'#f0f1ed','secondary':'#b8bfc6','label':'#aab3ba','tertiary':'#939da6','accent':'#edbd8b','onAccent':'#111517','subtle':'#343a3e','strong':'#4a5156','control':'#68747d','selected':'#312b25','selectedLine':'#9b8065','success':'#b3d2bb','successBg':'#1b2b24','successLine':'#527160','warning':'#e4c48f','warningBg':'#2d281f','warningLine':'#786446','danger':'#e6b1ad','dangerBg':'#302326','dangerLine':'#80575b','radii':[8,12,16,24,6,999],'heroAccent':'#edbd8b','texture':.24,'scheme':'dark'},
 'daybreak':{'name':'Daybreak','caption':'Daybreak · Plum on warm white.','base':'#f3f0f7','panel':'#fffaf4','raised':'#ffffff','field':'#ffffff','primary':'#242230','secondary':'#5b5668','label':'#655b71','tertiary':'#6d6379','accent':'#6541a5','onAccent':'#fffdf8','subtle':'#d5cedd','strong':'#b4aabd','control':'#82788e','selected':'#e8def6','selectedLine':'#9274ba','success':'#32664b','successBg':'#e7f0e9','successLine':'#86a891','warning':'#7a5420','warningBg':'#f4ecd8','warningLine':'#ac925e','danger':'#953d4e','dangerBg':'#f9e5e8','dangerLine':'#c48b99','radii':[8,12,16,24,6,999],'heroAccent':'#d5b9f5','texture':.035,'scheme':'light'},
 'tide':{'name':'Tide','caption':'Tide · Teal, ink and squared edges.','base':'#0f1720','panel':'#17232e','raised':'#22323d','field':'#111e29','primary':'#edf2ef','secondary':'#b2c5c7','label':'#a4bdc0','tertiary':'#96aaaf','accent':'#91d2c8','onAccent':'#0f2021','subtle':'#334751','strong':'#4a626e','control':'#66838e','selected':'#1d3a3b','selectedLine':'#5faeaa','success':'#b5d0b6','successBg':'#1c302a','successLine':'#597866','warning':'#e2c58f','warningBg':'#2e2b22','warningLine':'#86714b','danger':'#e2afb5','dangerBg':'#32272e','dangerLine':'#8b626f','radii':[2,2,4,2,2,2],'heroAccent':'#91d2c8','texture':.20,'scheme':'dark'},
 'lift':{'name':'Lift','caption':'Lift · Lavender, depth and soft light.','base':'#191720','panel':'#26232e','raised':'#322e3c','field':'#1f1c27','primary':'#f2edf6','secondary':'#c3baca','label':'#bdb0c8','tertiary':'#aa9fb4','accent':'#c5acf0','onAccent':'#241b31','subtle':'#41384d','strong':'#5f536f','control':'#7d708b','selected':'#3c304f','selectedLine':'#9f81c4','success':'#b8d5c3','successBg':'#26352e','successLine':'#6c8b77','warning':'#e6ca9c','warningBg':'#352e26','warningLine':'#917852','danger':'#e0b1c1','dangerBg':'#392a36','dangerLine':'#947087','radii':[10,12,16,24,6,999],'heroAccent':'#c5acf0','texture':.18,'scheme':'dark'}
}
(root/'skins.json').write_text(json.dumps(themes,indent=2)+'\n')
common_css='''
html { background:var(--skin-canvas); color-scheme:var(--skin-scheme); scroll-behavior:auto !important; }
body[data-study="01"] { --surface-base:var(--skin-canvas); --surface-panel:var(--skin-panel); --text-primary:var(--skin-primary); --text-secondary:var(--skin-secondary); --text-label:var(--skin-label); --text-tertiary:var(--skin-tertiary); --accent:var(--skin-accent); --line-subtle:var(--skin-subtle); --line-strong:var(--skin-strong); --action-radius:var(--skin-action-radius); --texture-opacity:var(--skin-texture); }
:root { --surface-raised:var(--skin-raised); --surface-field:var(--skin-field); --control-border:var(--skin-control); --radius-control:var(--skin-action-radius); --radius-panel:var(--skin-panel-radius); --success:var(--skin-success); --success-bg:var(--skin-success-bg); --warning:var(--skin-warning); --warning-bg:var(--skin-warning-bg); --danger:var(--skin-danger); --danger-bg:var(--skin-danger-bg); --selected-bg:var(--skin-selected); --selected-line:var(--skin-selected-line); --kit-switch-radius:var(--skin-field-radius); }
.btn:not(.secondary):not(.quiet):not(:disabled) { color:var(--skin-on-accent); }
.btn:not(.secondary):not(.quiet):not(:disabled) .icon { filter:var(--skin-action-icon); }
.btn.secondary .icon,.icon { filter:var(--skin-icon); }
.icon-btn.selected { background:var(--skin-selected); border-color:var(--skin-selected-line); }
.chip.selected,.chip:has(input:checked) { background:var(--skin-selected); border-color:var(--skin-selected-line); }
.field input:not([type=checkbox]):not([type=radio]):not([type=file]),.field select,.field textarea { border-radius:var(--skin-field-radius); }
.chip { border-radius:var(--skin-chip-radius); }
.icon-btn,.screen-study figcaption > a,.round-control { border-radius:var(--skin-icon-radius); }
.badge { border-radius:var(--skin-badge-radius); }
.badge.success { border-color:var(--skin-success-line); }
.badge.warning { border-color:var(--skin-warning-line); }
.badge.danger { border-color:var(--skin-danger-line); }
.notice,.upload-field,.swatch,input::file-selector-button { border-radius:var(--skin-field-radius); }
.toast-sample,.organizer { border-radius:var(--skin-action-radius); }
.doc-panel,.hero-card { border-radius:var(--skin-panel-radius); }
.skip-link { color:var(--skin-on-accent); }
/* The photograph is a distinct dark surface in every skin. Its crop, scrim and geometry stay fixed. */
.event-hero { --surface-base:#111517; --text-primary:#f0f1ed; --text-secondary:#b8bfc6; --text-label:#aab3ba; --text-tertiary:#939da6; --accent:var(--skin-hero-accent); color:var(--text-primary); }
.event-hero .icon { filter:none; }
.event-hero .primary-action { color:#211a27; }
.event-hero .primary-action .icon { filter:brightness(0); }
@media(prefers-contrast:more) { body[data-study="01"] { --texture-opacity:0; } }
'''
def css(t):
 keys={'canvas':'base','panel':'panel','raised':'raised','field':'field','primary':'primary','secondary':'secondary','label':'label','tertiary':'tertiary','accent':'accent','on-accent':'onAccent','subtle':'subtle','strong':'strong','control':'control','selected':'selected','selected-line':'selectedLine','success':'success','success-bg':'successBg','success-line':'successLine','warning':'warning','warning-bg':'warningBg','warning-line':'warningLine','danger':'danger','danger-bg':'dangerBg','danger-line':'dangerLine','hero-accent':'heroAccent'}
 values=''.join('--skin-'+k+':'+t[v]+';' for k,v in keys.items())
 values+='--skin-scheme:'+t['scheme']+';--skin-texture:'+str(t['texture'])+';'
 for name,val in zip(['field','action','panel','chip','badge','icon'],t['radii']): values+='--skin-'+name+'-radius:'+str(val)+'px;'
 values+='--skin-icon:'+('brightness(.18)' if t['scheme']=='light' else 'none')+';--skin-action-icon:'+('brightness(0) invert(1)' if t['scheme']=='light' else 'brightness(0)')+';'
 result='/* Paint-only skin. No type, spacing, sizing or component markup changes. */\n:root {'+values+'}\n'+common_css
 if t['name']=='Lift': result+='''
/* Elevation changes paint, never bounding boxes or layout spacing. */
.doc-panel,.hero-card,.organizer,.notice,.toast-sample { background:var(--surface-panel); box-shadow:inset 0 1px 0 #ffffff0d,0 2px 3px #0005,0 14px 28px #0003; }
.event-card { box-shadow:inset 0 1px 0 #ffffff0d,inset 0 -1px 0 #0005; }
.btn:not(.quiet):not(:disabled),.primary-action { box-shadow:inset 0 1px 0 #ffffff40,0 3px 0 #0004,0 8px 16px #0005; }
.btn.secondary,.icon-btn,.chip,.round-control { background:var(--surface-raised); box-shadow:inset 0 1px 0 #ffffff12,0 2px 3px #0005,0 5px 12px #0003; }
.icon-btn.selected,.chip.selected,.chip:has(input:checked) { background:var(--skin-selected); }
.field input:not([type=checkbox]):not([type=radio]):not([type=file]),.field select,.field textarea { box-shadow:inset 0 2px 6px #0005,inset 0 -1px 0 #ffffff08; }
.event-hero .round-control { background:#28232f; }
'''
 if t['name']=='Tide': result+='\n/* Callouts use a uniform neutral outline. Preserve the original text alignment. */\n.notice,.notice.error,.notice.success { border:1px solid var(--line-strong); padding-inline-start:calc(var(--space-4) + 2px); }\n'
 return result
files=list(source.glob('*.html'))+list((source/'frames').glob('*.html'))
# No generated screenshots, previous QA notes or mutation scripts are copied into the new deliverable.
for key,t in themes.items():
 folder=root if key=='original' else root/key;folder.mkdir(exist_ok=True);(folder/'frames').mkdir(exist_ok=True)
 if key!='original':(folder/'skin.css').write_text(css(t))
 tokens=json.loads((source/'tokens.json').read_text());tokens['skin']=t['name'];tokens['colors']={'Canvas':t['base'],'Card':t['panel'],'Raised':t['raised'],'Primary text':t['primary'],'Secondary text':t['secondary'],'Accent':t['accent']};tokens['semantic'].update({'field':t['field'],'controlBorder':t['control'],'success':t['success'],'warning':t['warning'],'danger':t['danger']});tokens['radius']={'field':t['radii'][0],'action':t['radii'][1],'documentationPanel':t['radii'][2]};tokens['texture']['opacity']=t['texture'];tokens['radius'].update({'filterChoice':t['radii'][3],'badge':t['radii'][4],'iconControl':t['radii'][5]});tokens['photoSurface']={'canvas':'#111517','accent':t['heroAccent']};tokens['elevation']='raised' if key=='lift' else 'flat';(folder/'tokens.json').write_text(json.dumps(tokens,indent=2)+'\n')
 for f in files:
  rel=f.relative_to(source);s=f.read_text(encoding='utf-8-sig');isframe=rel.parts[0]=='frames';depth=(1 if key!='original' else 0)+(1 if isframe else 0);prefix='../'*depth
  # All image/font/CSS assets share one source. Local page links stay inside each kit.
  s=re.sub(r'(?:\.\./)*assets/',prefix+'assets/',s)
  for name in ['fonts.css','screens.css','themes.css','cards.css','ui.css','gallery.css']:
   s=re.sub(r'href="(?:\.\./)*'+re.escape(name)+'"','href="'+prefix+name+'"',s)
  if key!='original':
   s=s.replace('href="README.md"','href="'+prefix+'README.md"').replace('href="screen-map.json"','href="'+prefix+'screen-map.json"')
   skinhref='../skin.css' if isframe else 'skin.css'
   s=s.replace('</head>','<link rel="stylesheet" href="'+skinhref+'"></head>')
   s=s.replace('name="theme-color" content="#111517"','name="theme-color" content="'+t['base']+'"')
  if rel.name=='index.html' and not isframe:
   switcher='<section class="kit-switcher" aria-label="Compare UI kit appearances"><p>Compare appearance</p>'
   for section in ['top','foundations','components','screens','coverage']:
    switcher+='<div class="skin-links" data-for="'+section+'">'
    for other,meta in themes.items():
     href=(('../' if key!='original' else '')+('index.html' if other=='original' else other+'/index.html')+'#'+section)
     switcher+='<a href="'+href+'"'+(' aria-current="true"' if key==other else '')+'>'+meta['name']+'</a>'
    switcher+='</div>'
   switcher+='<p class="skin-caption">'+t['caption']+'</p></section>'
   s=s.replace('</nav><p class="nav-foot">','</nav>'+switcher+'<p class="nav-foot">')
   s=s.replace('</head>','<link rel="stylesheet" href="'+prefix+'comparison.css"></head>')
   s=s.replace('<title>Date Line — UI kit</title>','<title>'+t['name']+' — Date Line UI kit</title>')
   s=s.replace('One peach primary action per task.','One primary accent per task.')
   s=s.replace('Radius: 8px fields, 12px actions, 16px documentation panels.','Radius: '+str(t['radii'][0])+'px fields, '+str(t['radii'][1])+'px actions, '+str(t['radii'][2])+'px documentation panels.')
   s=s.replace('Warm action. Cool surfaces. Three useful levels of depth.','Accent, canvas and three useful levels of depth.')
   if key!='original':
    old=['#111517','#1a1f22','#232a2e','#f0f1ed','#b8bfc6','#edbd8b'];new=[t[v] for v in ['base','panel','raised','primary','secondary','accent']]
    for a,b in zip(old,new):s=s.replace('background:'+a,'background:'+b).replace(a.upper()+'</code>',b.upper()+'</code>')
    s=s.replace('href="01-date-line.html">View the original','href="../01-date-line.html">View the original')
    s=s.replace('The originals stay exactly as you chose them.','The same components, in another appearance.').replace('Original list</a>','Themed list</a>').replace('Original full-screen event</a>','Themed full-screen event</a>').replace('These copies retain their original HTML, CSS and artwork. New screens below use the same foundations.','Every kit uses identical screen content, component structure, type sizes and spacing. Palette, corners and elevation are the variables.')
   s=s.replace('Date Line / UI kit 0.1 · Static HTML.','Date Line / Appearance studies · Static HTML.')
  (folder/rel).write_text(s,encoding='utf-8')
print('Built Date Line reference + Daybreak, Tide and Lift. Shared fixtures, assets and foundations.')
