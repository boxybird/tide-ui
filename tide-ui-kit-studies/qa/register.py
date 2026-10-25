from pathlib import Path
import json,re
root=Path('tide-ui-kit-studies');q=root/'qa'
def read(path):
 try:return path.read_text(encoding='utf-8-sig')
 except UnicodeDecodeError:return path.read_text(encoding='cp1252')
# Body markup is invariant; only the stylesheet links, metadata and asset rebasing differ.
checks={}
for skin in ['tide','mist','slate','deep']:
 folder=root if skin=='tide' else root/skin;parts={}
 for f in Path('date-line-ui-kit/frames').glob('*.html'):
  def body(p):return re.sub(r'(?:\.\./)*assets/','ASSETS/',re.search(r'<body[^>]*>([\s\S]*)</body>',read(p))[1])
  parts[f.name]=body(f)==body(folder/'frames'/f.name)
 checks[skin]=parts
(q/'fixture-lock.json').write_text(json.dumps(checks,indent=2)+'\n',encoding='utf-8')
p=Path('research/favorite-design.json');d=json.loads(read(p));d['status']='Favorite layout foundation; Tide is the current favorite UI kit appearance';d['ui_kit_preference']={'name':'Tide','selected':'2026-10-22','status':'Current favorite UI kit appearance','source':'../date-line-kit-variations/tide/index.html','current_studies':'../tide-ui-kit-studies/index.html','preferences':['Square edges','Named semantic color roles for easy palette swaps','No colored left-hand borders on callouts or announcements'],'new_palette_favorite':None};p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=Path('research/design-sets.json');d=json.loads(read(p));d['updated']='2026-10-22'
for x in d['sets']:
 if x.get('name')=='Date Line Appearance Studies':x['preferred_options']=[2];x['status']='Tide is the user-selected favorite UI kit appearance. Its callout stripes were removed at the user’s request.'
if not any(x.get('name')=='Tide Palette Studies' for x in d['sets']):d['sets'].append({'name':'Tide Palette Studies','date':'2026-10-22','path':'tide-ui-kit-studies/index.html','url':'http://127.0.0.1:4184/','description':'Tide favorite retained, all callout stripes removed. Three palette-only variants preserve square corners and complete kit inventory.','baseline':'Tide','options':[{'number':1,'name':'Mist','style':'Cool light mode with dark teal actions'},{'number':2,'name':'Slate','style':'Quieter charcoal and blue-gray'},{'number':3,'name':'Deep','style':'Darker blue with cyan accents'}],'status':'New variations; no replacement favorite chosen.'})
d['preferences']['current_constraint']='Tide is the favorite UI kit appearance. Preserve square edges, flat surfaces, type/spacing/targets, full component/screen inventory and sidebar comparison. Remove colored left borders from every future callout. Explore semantic palette swaps including light mode.'
d['preferences']['selected_direction']['appearance']='Tide';d['preferences']['selected_direction']['next']='Compare Mist, Slate and Deep while retaining Tide as the favorite baseline; use uniform neutral callout outlines.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=Path('AGENTS.md');s=read(p);s=s.replace('# Burque Events — current design direction','# Burque Events — current design direction\n\nCurrent UI kit favorite (2026-10-22): **Tide**. Keep its square edges and complete Foundations / Components / Screens / Coverage inventory. Use semantic palette roles. The user explicitly dislikes colored left borders on announcements/callouts: remove them rather than adding a replacement colored ornament. Latest palette studies: tide-ui-kit-studies/ (port4184), Tide + Mist (light), Slate and Deep. No new palette favorite chosen.');s=s.replace('No new favorite chosen.','Tide was subsequently selected as the favorite UI kit appearance.');p.write_text(s,encoding='utf-8')
p=Path('research/source-notes.txt');s=read(p);s+='\n2026-10-22 — User selects Tide as favorite UI kit appearance, especially square edges. Requests light mode and more Tide iterations; dislikes colored left callout borders. Tide Palette Studies: same semantic roles, fixed structure/radii, Mist light mode + Slate + Deep. Uniform neutral callout borders in every new kit and existing Tide at port4183. Preview port4184.\n';p.write_text(s,encoding='utf-8')
p=Path('date-line-kit-variations/AGENTS.md');s=read(p);s+='\n- Follow-up user selection: Tide is the favorite. Explicit scoped update: its callout stripes are removed in skin.css and the generator. New palette studies continue separately in tide-ui-kit-studies/ on port4184. Other appearances remain archived unchanged.\n';p.write_text(s,encoding='utf-8')
p=Path('date-line-kit-variations/design-qa.md');s=read(p);s+='\n## Subsequent user-requested change\n\n2026-10-22: Tide was selected as favorite. Its colored left callout stripes were removed with a neutral uniform outline; body text position and geometry remain identical. Earlier Tide status captures retain the pre-change appearance for historical comparison. Current before/after evidence and QA: ../tide-ui-kit-studies/design-qa.md. Other kit styles were not changed.\n';p.write_text(s,encoding='utf-8')
print('All frame bodies preserved:',all(all(x.values()) for x in checks.values()))
