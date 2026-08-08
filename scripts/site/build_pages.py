#!/usr/bin/env python3
"""Create the aurasoft.co page set over the WordPress MCP endpoint."""
import json, os, urllib.request

URL = "https://aurasoft.co/wp-json/wp/v2/wpmcp/streamable"
TOKEN = os.environ["WP_MCP_TOKEN"]
_id = [100]


def call(tool, args):
    _id[0] += 1
    body = json.dumps({
        "jsonrpc": "2.0", "id": _id[0], "method": "tools/call",
        "params": {"name": tool, "arguments": args},
    }).encode()
    req = urllib.request.Request(URL, data=body, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json, text/event-stream",
    })
    with urllib.request.urlopen(req, timeout=90) as r:
        return json.loads(r.read())


def h(text, level=2):
    return (f'<!-- wp:heading {{"level":{level}}} -->\n'
            f'<h{level}>{text}</h{level}>\n<!-- /wp:heading -->')


def p(text):
    return f'<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->'


def lead(text):
    return ('<!-- wp:paragraph {"className":"lead"} -->\n'
            f'<p class="lead"><strong>{text}</strong></p>\n<!-- /wp:paragraph -->')


def ul(items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<!-- wp:list -->\n<ul>{li}</ul>\n<!-- /wp:list -->'


def sep():
    return '<!-- wp:separator -->\n<hr class="wp-block-separator"/>\n<!-- /wp:separator -->'


PAGES = [
    # ---------------------------------------------------------------- HOME
    dict(title="Home", slug="home", content="\n\n".join([
        h("We make games. And the tools to build them.", 1),
        lead("Aurasoft is a game and software studio working out of Australia and "
             "Pakistan. We ship mobile titles, build software for clients, and sell "
             "the 3D, 2D and UI assets we make along the way."),
        sep(),
        h("Three lines of work that feed each other"),
        p("The art we build for our own games becomes the packs we sell. The "
          "engineering that ships those games is what clients hire us for."),
        h("Games", 3),
        p("Android and iOS titles, built end to end — concept, art, code, release, "
          "and the long tail of updates after launch."),
        h("Software", 3),
        p("Apps and custom software for clients who need something built properly "
          "the first time. Same team, same standards."),
        h("Assets", 3),
        p("3D models, 2D art and UI kits — production-ready, made for real projects "
          "because they came out of ours."),
        sep(),
        h("Why studios work with us"),
        p("<strong>We ship.</strong> We are not consultants who have read about game "
          "development. We release our own titles and hit the same walls you do."),
        p("<strong>Two timezones, one team.</strong> Australia and Pakistan means "
          "work moves while you sleep — genuine coverage, not overnight ticket queues."),
        p("<strong>Art and code under one roof.</strong> No handoff gap between the "
          "people making assets and the people building the game. That gap is where "
          "projects die."),
        sep(),
        h("Got something you want built?"),
        p("Tell us what you are making. We will tell you straight whether we are the "
          "right studio for it."),
    ])),

    # --------------------------------------------------------------- GAMES
    dict(title="Games", slug="games", content="\n\n".join([
        h("Games we have made", 1),
        lead("Everything here we made ourselves — design, art, code, release."),
        p("Some are ours, some were built with partners. All of them shipped."),
        sep(),
        h("Titles"),
        p("<em>Game listings go here — key art, platforms and store links for each "
          "title. Unreleased work is worth showing too, marked as in development; "
          "work in progress signals momentum.</em>"),
        sep(),
        h("Built with"),
        p("Unity and Unreal for the games themselves, with Android Studio and Xcode "
          "for the native side — so builds behave on real devices, not just in the "
          "editor."),
    ])),

    # ------------------------------------------------------------ SERVICES
    dict(title="Services", slug="services", content="\n\n".join([
        h("What we build for clients", 1),
        lead("We take on client work in the same three areas we work in ourselves. "
             "Small enough to care, experienced enough to ship."),
        sep(),
        h("Game Development"),
        p("Full-cycle mobile game development, Android and iOS. We come in at any "
          "stage — a concept on a napkin, a prototype that stalled, or a live game "
          "that needs a team who can pick it up without breaking it."),
        ul(["Unity and Unreal",
            "Native tooling — Android Studio and Xcode, so builds behave on real devices",
            "Gameplay programming, systems design, level design",
            "Full art production — characters, environments, VFX, UI",
            "Store release, ASO, live-ops and post-launch updates"]),
        h("App &amp; Software Development"),
        p("Mobile apps and custom software. The same engineers who ship games under "
          "deadline — which tends to show in how the work holds up."),
        ul(["Native mobile apps — Android Studio and Xcode, Java for Android",
            "Backends, APIs, automation and tooling in Python",
            "Desktop and simulation work in Unity or Unreal where it fits better "
            "than a web stack",
            "Maintenance and support after launch"]),
        h("Art &amp; Asset Production"),
        p("Art production for studios who need more hands. Work to your style guide, "
          "in your pipeline, at your quality bar."),
        ul(["3D — characters, props, environments, game-ready and PBR textured",
            "2D — concept art, sprites, backgrounds, marketing art",
            "UI/UX — full interface kits, icons, HUD design",
            "Outsourcing at scale, or a single pack"]),
        sep(),
        h("How we work"),
        p("<strong>1. Talk</strong> — you tell us what you are making. We ask a lot "
          "of questions."),
        p("<strong>2. Scope</strong> — a real plan with real numbers. No surprise "
          "invoices."),
        p("<strong>3. Build</strong> — weekly builds you can actually play, not "
          "status reports."),
        p("<strong>4. Ship</strong> — release, then the support that makes launch "
          "stick."),
        sep(),
        h("Our toolchain"),
        p("Unity · Unreal · Android Studio · Xcode · Java · Python"),
    ])),

    # -------------------------------------------------------------- ASSETS
    dict(title="Assets", slug="assets", content="\n\n".join([
        h("Made for our games. Packaged for yours.", 1),
        lead("We build assets for our own games, then package the good ones up. "
             "Everything here has shipped in something real — that is the only "
             "quality bar that matters."),
        sep(),
        h("3D Assets"),
        p("Characters, props and environments. Game-ready topology, sane poly "
          "counts, PBR textures. Unity and Unreal ready."),
        h("2D Assets"),
        p("Sprites, tilesets, backgrounds and FX sheets. Layered sources included, "
          "so you can actually edit them."),
        h("UI Kits"),
        p("Complete interface sets — menus, HUDs, buttons, icons, popups. "
          "Consistent, scalable and drop-in."),
        sep(),
        h("Where to buy"),
        p("Most of our packs are on itch.io. <em>Store link goes here.</em>"),
    ])),

    # --------------------------------------------------------------- ABOUT
    dict(title="About", slug="about", content="\n\n".join([
        h("A studio in two places", 1),
        lead("Aurasoft started in 2018 and works across Australia and Pakistan."),
        p("We build our own games, take on client work we find interesting, and sell "
          "the art we make along the way."),
        p("The split is not an accident. It gives us close contact with clients in "
          "Australia and a strong production team in Pakistan — and between them, "
          "work that keeps moving around the clock."),
        sep(),
        h("What we care about"),
        p("Shipping over talking. Work that holds up after launch. Being straight "
          "with clients about what something will actually take."),
        sep(),
        h("The team"),
        p("<em>Team profiles go here — names, roles and photos.</em>"),
        h("Offices"),
        p("Australia · Pakistan"),
    ])),

    # ------------------------------------------------------------- CONTACT
    dict(title="Contact", slug="contact", content="\n\n".join([
        h("Tell us what you are building", 1),
        lead("Client project, asset question, or you just want to talk shop — we "
             "read everything and reply properly."),
        p("We reply within one business day. Both our timezones count."),
        sep(),
        h("Get in touch"),
        p("<em>Contact form goes here. Until then, add your email address and "
          "social links.</em>"),
        h("Find us"),
        p("Australia · Pakistan"),
    ])),
]


def main():
    created = {}
    for spec in PAGES:
        r = call("wp_add_page", {
            "title": spec["title"],
            "slug": spec["slug"],
            "content": spec["content"],
            "status": "publish",
        })
        if "error" in r:
            print(f"  FAIL  {spec['title']}: {r['error'].get('message')}")
            continue
        txt = r.get("result", {}).get("content", [{}])[0].get("text", "{}")
        try:
            obj = json.loads(txt)
            pid = obj.get("id")
            created[spec["slug"]] = pid
            print(f"  OK    {spec['title']:<10} id={pid}  /{spec['slug']}/")
        except Exception:
            print(f"  ?     {spec['title']}: {txt[:150]}")
    print("\n  created:", json.dumps(created))


if __name__ == "__main__":
    main()
