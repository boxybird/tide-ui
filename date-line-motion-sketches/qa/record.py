from pathlib import Path
import json, hashlib
root = Path(__file__).resolve().parents[1]
workspace = root.parent
registry_file = workspace / "research/design-sets.json"
registry = json.loads(registry_file.read_text(encoding="utf-8"))
entry = {
    "name":"Date Line — Motion Sketches",
    "description":"Fast motion-only iteration reusing the existing prototype: Gather, Aperture and Shutter.",
    "kind":"interactive_html",
    "status":"Browser-reviewed; awaiting user preference. Date Line remains the favorite overall.",
    "started":"2026-10-21",
    "completed":"2026-10-21",
    "comparison":"../date-line-motion-sketches/index.html",
    "options":[{"number":i+1,"name":name,"file":"../date-line-motion-sketches/app.html?motion="+name.lower()} for i,name in enumerate(("Gather","Aperture","Shutter"))],
    "preferred_options":[],
    "feedback":"User wants faster iteration focused on a distinctive list-to-event transition using the native View Transition API, with micro feedback animations secondary.",
    "validation":"All three native openings/returns pass. List and all three event endpoints are pixel-identical to Date Line at390x844. No new assets or app features."
}
registry["sets"] = [item for item in registry["sets"] if item["name"] != entry["name"]] + [entry]
registry["preferences"]["selected_direction"]["next"] = "Choose a motion direction in Date Line — Motion Sketches, keeping the approved visual baseline unchanged."
registry["preferences"]["current_constraint"] = "Fast motion-only iterations; preserve Date Line and prior prototypes. Focus on list-to-event transition before adding app features or secondary microinteractions."
registry_file.write_text(json.dumps(registry,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
notes_file = workspace / "research/source-notes.txt"
notes = "\n\n2026-10-21 — Date Line Motion Sketches (sixteenth study)\nUser requests faster iteration focused on a distinctive native View Transition opening, with app construction and secondary microinteractions deferred. Reused the existing prototype in a preserved sibling folder on port4180. Gather carries title/date/time through an expansion; Aperture masks the complete event; Shutter reveals the photo plane while the title travels. All rest states fixed. No new assets or product features.\nThree native openings and returns, controls, narrow-phone aperture and direct fallback verified. Resting list and three event endpoints pixel-equal to fresh390x844 source captures. Intermediate frames inspected; an initially fragmented aperture was simplified to avoid competing text paths. Primary implementation reference: Chrome Developers same-document View Transitions documentation. All earlier collections remain preserved; no new favorite assumed.\n"
if "Motion Sketches (sixteenth study)" not in notes_file.read_text(encoding="utf-8"):
    with notes_file.open("a",encoding="utf-8") as file:
        file.write(notes)
checks = {}
for filename in ("screens.css","themes.css","cards.css","fonts.css"):
    checks[filename] = (root/filename).read_bytes() == (workspace/"quiet-assembly"/filename).read_bytes()
lock = json.loads((workspace/"date-line-in-practice/baseline-lock.json").read_text())
checks["approved_pairs"] = all(hashlib.sha256((workspace/"date-line-in-practice"/item[key]).read_bytes()).hexdigest() == item["sha256"] for item in lock["files"] for key in ("source","copy"))
assert all(checks.values()), checks
(root/"qa/preservation.json").write_text(json.dumps(checks,indent=2))
print(json.dumps(checks))
