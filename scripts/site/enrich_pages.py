#!/usr/bin/env python3
"""Rebuild the key pages with real block layout — columns, groups, buttons."""
import json, os, subprocess, time

URL = "https://aurasoft.co/wp-json/wp/v2/wpmcp/streamable"
TOKEN = os.environ["WP_MCP_TOKEN"]
_id = [500]


def call(tool, args):
    """Go through curl — Python's urllib does not honour this sandbox's proxy."""
    _id[0] += 1
    payload = json.dumps({"jsonrpc": "2.0", "id": _id[0], "method": "tools/call",
                          "params": {"name": tool, "arguments": args}})
    out = subprocess.run(
        ["curl", "-sS", "-m", "90", "-X", "POST", URL,
         "-H", f"Authorization: Bearer {TOKEN}",
         "-H", "Content-Type: application/json",
         "-H", "Accept: application/json, text/event-stream",
         "--data-binary", "@-"],
        input=payload, capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"curl failed: {out.stderr.strip()[:200]}")
    return json.loads(out.stdout)


# ---- block helpers -------------------------------------------------------

def h(t, lv=2, cls=""):
    c = f' {{"level":{lv},"className":"{cls}"}}' if cls else f' {{"level":{lv}}}'
    k = f' class="wp-block-heading {cls}"' if cls else ' class="wp-block-heading"'
    return f'<!-- wp:heading{c} -->\n<h{lv}{k}>{t}</h{lv}>\n<!-- /wp:heading -->'


def p(t, cls=""):
    if cls:
        return (f'<!-- wp:paragraph {{"className":"{cls}"}} -->\n'
                f'<p class="{cls}">{t}</p>\n<!-- /wp:paragraph -->')
    return f'<!-- wp:paragraph -->\n<p>{t}</p>\n<!-- /wp:paragraph -->'


def cols(*inner):
    body = "".join(
        f'<!-- wp:column -->\n<div class="wp-block-column">{c}</div>\n<!-- /wp:column -->'
        for c in inner)
    return (f'<!-- wp:columns -->\n<div class="wp-block-columns">{body}</div>\n'
            f'<!-- /wp:columns -->')


def card(title, text, hue):
    """A pillar/feature card. `hue` drives the accent via a class."""
    return (f'<!-- wp:group {{"className":"aura-card aura-{hue}"}} -->\n'
            f'<div class="wp-block-group aura-card aura-{hue}">'
            f'<!-- wp:heading {{"level":3}} -->\n<h3 class="wp-block-heading">{title}</h3>\n'
            f'<!-- /wp:heading -->'
            f'<!-- wp:paragraph -->\n<p>{text}</p>\n<!-- /wp:paragraph -->'
            f'</div>\n<!-- /wp:group -->')


def btn(label, href, style="fill"):
    cls = "aura-btn" if style == "fill" else "aura-btn aura-btn-ghost"
    return (f'<!-- wp:buttons -->\n<div class="wp-block-buttons">'
            f'<!-- wp:button {{"className":"{cls}"}} -->\n'
            f'<div class="wp-block-button {cls}">'
            f'<a class="wp-block-button__link wp-element-button" href="{href}">{label}</a>'
            f'</div>\n<!-- /wp:button --></div>\n<!-- /wp:buttons -->')


def btnrow(pairs):
    inner = "".join(
        f'<!-- wp:button {{"className":"aura-btn{"" if i == 0 else " aura-btn-ghost"}"}} -->\n'
        f'<div class="wp-block-button aura-btn{"" if i == 0 else " aura-btn-ghost"}">'
        f'<a class="wp-block-button__link wp-element-button" href="{href}">{label}</a>'
        f'</div>\n<!-- /wp:button -->'
        for i, (label, href) in enumerate(pairs))
    return (f'<!-- wp:buttons -->\n<div class="wp-block-buttons">{inner}</div>\n'
            f'<!-- /wp:buttons -->')


def sep():
    return ('<!-- wp:separator -->\n<hr class="wp-block-separator"/>\n'
            '<!-- /wp:separator -->')


def eyebrow(t):
    return p(t, "aura-eyebrow")


# ---- pages ---------------------------------------------------------------

# Storefronts. Keep these here rather than inline so a change is one edit.
ITCH_STUDIO = "https://auragamestudio.itch.io"
ITCH_DEV = "https://rehandev.itch.io"
PLAY_DEV = "https://play.google.com/store/apps/dev?id=6340776414296526480"

# Published titles. Add a row per game — the Play URL is derived from the
# package id, so only the human-facing copy needs writing.
GAMES_LIST = [
    ("com.aurasoft.CryptoPOP", "CryptoPOP",
     "A crypto-themed arcade popper. Match, chain and clear the board in quick "
     "rounds that get meaner the longer you last — and a high score that is never "
     "quite safe.",
     "cyan"),
]


def play_url(package):
    return f"https://play.google.com/store/apps/details?id={package}"


def game_cards():
    """One card per published title, falling back to a visible TODO for any
    game whose blurb has not been written yet — better an obvious gap than
    invented copy about a real product."""
    out = []
    for pkg, title, blurb, hue in GAMES_LIST:
        text = blurb or "<em>Description needed.</em>"
        out.append(card(title, text, hue))
    return cols(*out) if out else ""



HOME = "\n\n".join([
    eyebrow("Game &amp; software studio · Australia + Pakistan · est. 2018"),
    h("We make games. And the tools to build them.", 1),
    p("Aurasoft ships mobile titles, builds software for clients, and sells the 3D, "
      "2D and UI assets we make along the way. Three things, one craft.", "aura-lead"),
    btnrow([("Play our games", "/games/"), ("Browse assets", "/assets/")]),
    sep(),
    eyebrow("What we do"),
    h("Three lines of work that feed each other"),
    p("The art we build for our own games becomes the packs we sell. The engineering "
      "that ships those games is what clients hire us for."),
    cols(
        card("Games", "Android and iOS titles built end to end — concept, art, code, "
                      "release, and the long tail of updates after launch.", "cyan"),
        card("Software", "Native mobile and backend work from the same engineers who "
                         "ship games under deadline. It shows in how the work holds up.", "violet"),
        card("Assets", "3D models, 2D art and UI kits — production-ready, made for real "
                       "projects because they came out of ours.", "magenta"),
    ),
    sep(),
    eyebrow("Why us"),
    h("Why studios work with us"),
    cols(
        card("We ship", "We are not consultants who have read about game development. "
                        "We release our own titles and hit the same walls you do.", "cyan"),
        card("Two timezones", "Australia and Pakistan means work moves while you sleep — "
                              "genuine coverage, not overnight ticket queues.", "violet"),
        card("One roof", "No handoff gap between the people making assets and the people "
                         "building the game. That gap is where projects die.", "magenta"),
    ),
    sep(),
    h("Got something you want built?"),
    p("Tell us what you are making. We will tell you straight whether we are the right "
      "studio for it.", "aura-lead"),
    btn("Start a conversation", "/contact/"),
])

ASSETS = "\n\n".join([
    eyebrow("Asset store"),
    h("Made for our games. Packaged for yours.", 1),
    p("We build assets for our own games, then package the good ones up. Everything "
      "here has shipped in something real — that is the only quality bar that matters.",
      "aura-lead"),
    sep(),
    cols(
        card("3D Assets", "Characters, props and environments. Game-ready topology, sane "
                          "poly counts, PBR textures. Unity and Unreal ready.", "cyan"),
        card("2D Assets", "Sprites, tilesets, backgrounds and FX sheets. Layered sources "
                          "included, so you can actually edit them.", "violet"),
        card("UI Kits", "Complete interface sets — menus, HUDs, buttons, icons, popups. "
                        "Consistent, scalable and drop-in.", "magenta"),
    ),
    sep(),
    eyebrow("Where to buy"),
    h("Our itch.io stores"),
    p("Everything we release is on itch.io. Two storefronts — the studio's, and our "
      "lead developer's."),
    cols(
        card("Aura Game Studio", "The studio storefront — games and asset packs released "
                                 "under Aurasoft.", "cyan"),
        card("RehanDev", "Our lead developer's storefront, with additional tools and "
                         "packs.", "violet"),
    ),
    btnrow([("Aura Game Studio on itch.io", ITCH_STUDIO),
            ("RehanDev on itch.io", ITCH_DEV)]),
])

SERVICES_TAIL = "\n\n".join([
    sep(),
    eyebrow("Process"),
    h("How we work"),
    cols(
        card("1. Talk", "You tell us what you are making. We ask a lot of questions.", "cyan"),
        card("2. Scope", "A real plan with real numbers. No surprise invoices.", "violet"),
        card("3. Build", "Weekly builds you can actually play, not status reports.", "magenta"),
        card("4. Ship", "Release, then the support that makes launch stick.", "cyan"),
    ),
    sep(),
    eyebrow("Toolchain"),
    h("What we build with"),
    p("Unity · Unreal · Android Studio · Xcode · Java · Python", "aura-chips"),
    btn("Start a conversation", "/contact/"),
])


def ul(items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{li}</ul>\n<!-- /wp:list -->'


SERVICES = "\n\n".join([
    eyebrow("Client work"),
    h("What we build for clients", 1),
    p("We take on client work in the same three areas we work in ourselves. Small "
      "enough to care, experienced enough to ship.", "aura-lead"),
    sep(),
    h("Game Development"),
    p("Full-cycle mobile game development, Android and iOS. We come in at any stage — "
      "a concept on a napkin, a prototype that stalled, or a live game that needs a "
      "team who can pick it up without breaking it."),
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
        "Desktop and simulation work in Unity or Unreal where it fits better than a "
        "web stack",
        "Maintenance and support after launch"]),
    h("Art &amp; Asset Production"),
    p("Art production for studios who need more hands. Work to your style guide, in "
      "your pipeline, at your quality bar."),
    ul(["3D — characters, props, environments, game-ready and PBR textured",
        "2D — concept art, sprites, backgrounds, marketing art",
        "UI/UX — full interface kits, icons, HUD design",
        "Outsourcing at scale, or a single pack"]),
    SERVICES_TAIL,
])

GAMES = "\n\n".join([
    eyebrow("Shipped work"),
    h("Games we have made", 1),
    p("Everything here we made ourselves — design, art, code, release. Some are ours, "
      "some were built with partners. All of them shipped.", "aura-lead"),
    btnrow([("See all our games on Google Play", PLAY_DEV),
            ("Browse our itch.io store", ITCH_STUDIO)]),
    sep(),
    eyebrow("Where to play"),
    h("On the stores"),
    cols(
        card("Google Play", "Our Android catalogue lives on Google Play under the "
                            "Aurasoft developer profile.", "cyan"),
        card("itch.io", "Builds, prototypes and asset packs go up on itch.io, often "
                        "before they reach the app stores.", "violet"),
        card("iOS", "Selected titles ship to the App Store, built natively in Xcode "
                    "alongside the Android release.", "magenta"),
    ),
    sep(),
    eyebrow("Selected titles"),
    h("Featured games"),
    game_cards(),
    btnrow([("CryptoPOP on Google Play", play_url("com.aurasoft.CryptoPOP"))]),
    sep(),
    eyebrow("How they are built"),
    h("Built with"),
    p("Unity and Unreal for the games themselves, with Android Studio and Xcode for "
      "the native side — so builds behave on real devices, not just in the editor."),
    p("Unity · Unreal · Android Studio · Xcode · Java · Python", "aura-chips"),
    btn("Talk to us about a project", "/contact/"),
])

ABOUT = "\n\n".join([
    eyebrow("The studio"),
    h("A studio in two places", 1),
    p("Aurasoft started in 2018 and works across Australia and Pakistan. We build our "
      "own games, take on client work we find interesting, and sell the art we make "
      "along the way.", "aura-lead"),
    p("The split is not an accident. It gives us close contact with clients in "
      "Australia and a strong production team in Pakistan — and between them, work "
      "that keeps moving around the clock."),
    sep(),
    eyebrow("What we care about"),
    h("How we operate"),
    cols(
        card("Shipping over talking", "A released build beats a roadmap. We would "
                                      "rather show you something running.", "cyan"),
        card("Work that lasts", "Launch is the start of the job, not the end of it. We "
                                "build for the year after release.", "violet"),
        card("Straight answers", "We tell clients what something will actually take, "
                                 "including when the answer is inconvenient.", "magenta"),
    ),
    sep(),
    eyebrow("Where we are"),
    h("Offices"),
    cols(
        card("Australia", "Client-facing team, close to the timezone most of our "
                          "partners work in.", "cyan"),
        card("Pakistan", "Production team — engineering and art, at scale.", "violet"),
    ),
    sep(),
    h("The team"),
    p("<em>Team profiles go here — names, roles and photos.</em>"),
    btn("Work with us", "/contact/"),
])

CONTACT = "\n\n".join([
    eyebrow("Get in touch"),
    h("Tell us what you are building", 1),
    p("Client project, asset question, or you just want to talk shop — we read "
      "everything and reply properly.", "aura-lead"),
    p("We reply within one business day. Both our timezones count."),
    sep(),
    eyebrow("What is it about"),
    h("Three things people usually ask us"),
    cols(
        card("A game", "You have a concept, a stalled prototype, or a live title that "
                       "needs a team. Tell us where it is now.", "cyan"),
        card("Software", "An app or a custom build. The more you can say about scope, "
                         "the more useful our first reply will be.", "violet"),
        card("Assets", "A pack question, a licence question, or custom art production "
                       "for your pipeline.", "magenta"),
    ),
    sep(),
    h("Reach us"),
    p("<em>Contact form goes here. Until then, add your email address and social "
      "links.</em>"),
    p("Australia · Pakistan"),
])

# Page IDs on the live site, created by build_pages.py.
PAGES = (
    (9,  HOME,     "Home"),
    (10, GAMES,    "Games"),
    (11, SERVICES, "Services"),
    (12, ASSETS,   "Assets"),
    (13, ABOUT,    "About"),
    (14, CONTACT,  "Contact"),
)


def main():
    for pid, content, name in PAGES:
        # The proxy in front of this sandbox resets connections intermittently,
        # so each write gets a few attempts before it counts as a failure.
        for attempt in range(5):
            try:
                r = call("wp_update_page", {"id": pid, "content": content})
                ok = "error" not in r
                print(f"  {'OK  ' if ok else 'FAIL'} {name}"
                      + ("" if ok else f" — {r['error'].get('message')}"))
                break
            except Exception as exc:
                if attempt == 4:
                    print(f"  FAIL {name} — {exc}")
                else:
                    time.sleep(2 ** attempt)


if __name__ == "__main__":
    main()
