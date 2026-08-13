#!/usr/bin/env python3
import importlib.util, time

spec = importlib.util.spec_from_file_location(
    "e", "/home/user/aurasoft.co/scripts/site/enrich_pages.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

# TSF appends " - Aurasoft" to every page, and " - {tagline}" on the front
# page — confirmed by probing the live <title> tag, not assumed. Titles here
# are written short so the appended half completes them instead of repeating
# brand text that is already coming.
TITLES = {
    9:  "",  # empty -> clean TSF default: "Aurasoft - Game & Software Studio — Australia & Pakistan"
    10: "8 Free Android Games — Racing, Puzzle, Cards & Arcade",
    11: "Game & App Development Services",
    12: "Game Assets — 3D, 2D & UI Kits",
    13: "Our Studio — Australia & Pakistan",
    14: "Contact Us",
    33: "Privacy Policy",
}

NAMES = {9:"Home",10:"Games",11:"Services",12:"Assets",13:"About",14:"Contact",33:"Privacy"}

def write(pid, title, tries=25):
    for a in range(1, tries+1):
        try:
            r = m.call("wp_update_page", {"id": pid, "meta": {"_genesis_title": title}})
            if "error" in r:
                print(f"  FAIL {NAMES[pid]}: {r['error'].get('message')}", flush=True); return
            print(f"  OK   {NAMES[pid]} (attempt {a})", flush=True); return
        except Exception:
            if a == tries: print(f"  FAIL {NAMES[pid]}: gave up", flush=True)
            else: time.sleep(4)

for pid, title in TITLES.items():
    if pid == 9:
        continue  # already set and verified
    write(pid, title)
    time.sleep(4)
