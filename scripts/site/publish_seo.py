#!/usr/bin/env python3
import importlib.util, time, json

spec = importlib.util.spec_from_file_location(
    "e", "/home/user/aurasoft.co/scripts/site/enrich_pages.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

SEO = {
    9:  ("Aurasoft — Game & Software Studio | Australia & Pakistan",
         "Mobile games, custom software and game-ready 3D, 2D and UI assets from "
         "a studio working across Australia and Pakistan since 2018."),
    10: ("8 Free Android Games — Racing, Puzzle, Cards & Arcade | Aurasoft",
         "Play our full catalogue on Google Play: Pursuit 2, Bhabhi Thulla, "
         "Trivia Sports Quiz, Crypto Blast and more, built end to end by Aurasoft."),
    11: ("Game & App Development Services | Aurasoft",
         "Full-cycle mobile game development, custom software and art "
         "outsourcing from a studio that ships its own titles on Google Play."),
    12: ("Game Assets — 3D, 2D & UI Kits | Aurasoft",
         "Production-ready 3D models, 2D art and UI kits, made for our own games "
         "and sold on itch.io. Shipped in something real, not stock art."),
    13: ("About Aurasoft — Studio in Australia & Pakistan",
         "Founded in 2018, Aurasoft builds games, software and art assets across "
         "two countries and one team."),
    14: ("Contact Aurasoft",
         "Start a project or ask about our assets. Email arslan.aurasoft@gmail.com "
         "— we reply within one business day."),
    33: ("Privacy Policy | Aurasoft",
         "How Aurasoft collects and uses information in our mobile apps, "
         "including AdMob advertising, opt-out steps and your rights."),
}

NAMES = {9:"Home",10:"Games",11:"Services",12:"Assets",13:"About",14:"Contact",33:"Privacy"}

def write(pid, title, desc, tries=25):
    for a in range(1, tries+1):
        try:
            r = m.call("wp_update_page", {"id": pid, "meta": {
                "_genesis_title": title, "_genesis_description": desc}})
            if "error" in r:
                print(f"  FAIL {NAMES[pid]}: {r['error'].get('message')}", flush=True); return
            print(f"  OK   {NAMES[pid]} (attempt {a})", flush=True); return
        except Exception:
            if a == tries: print(f"  FAIL {NAMES[pid]}: gave up", flush=True)
            else: time.sleep(4)

for pid, (title, desc) in SEO.items():
    write(pid, title, desc)
    time.sleep(4)
