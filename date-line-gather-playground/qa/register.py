from pathlib import Path
import json,hashlib
p=Path('research/design-sets.json');d=json.loads(p.read_text(encoding='utf-8-sig'))
for s in d['sets']:
 if s.get('name')=='Motion Sketches' or 'Motion Sketches' in s.get('name',''):
  s['latest_feedback']='User likes the studies and is leaning toward Gather. Explore richer, deliberately exaggerated microinteractions with real web research.'
if not any(s.get('name')=='Gather, amplified' for s in d['sets']):
 d['sets'].append({'name':'Gather, amplified','description':'Research-backed rich microinteraction extension of Gather, preserving the resting Date Line layout.','path':'date-line-gather-playground/index.html','url':'http://127.0.0.1:4181/','options':[{'number':1,'name':'Expressive'},{'number':2,'name':'Overdrive'}],'status':'New experiment; no intensity preference selected. Prior Gather remains preserved.'})
d['preferences']['current_constraint']='User is leaning toward Gather. Push rich and deliberately overdone microinteractions using inspected internet references; preserve Date Line and all prior studies.'
d['preferences']['selected_direction']['next']='Compare Expressive and Overdrive in Gather, amplified; retain Date Line as favorite visual foundation.'
p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
p=Path('research/favorite-design.json');d=json.loads(p.read_text());d['motion_preference']={'direction':'Gather','status':'Leaning preference, not a replacement for the Date Line layout favorite','date':'2026-10-21'};p.write_text(json.dumps(d,indent=2)+'\n')
p=Path('AGENTS.md');s=p.read_text();s+='\n- Latest user motion feedback: leaning toward Gather; explicitly requests research-backed, rich and deliberately exaggerated microinteractions. New preserved sibling: date-line-gather-playground/ (port4181), Expressive and Overdrive. Date Line remains the overall visual favorite.\n';p.write_text(s)
p=Path('date-line-gather-playground/package.json');d=json.loads(p.read_text());d['name']='burque-gather-amplified';p.write_text(json.dumps(d,indent=2)+'\n')
checks={name:hashlib.sha256((Path('date-line-motion-sketches')/name).read_bytes()).hexdigest()==hashlib.sha256((Path('date-line-gather-playground')/name).read_bytes()).hexdigest() for name in ['screens.css','themes.css','cards.css','fonts.css']}
Path('date-line-gather-playground/qa/preservation.json').write_text(json.dumps(checks,indent=2));print(checks)
