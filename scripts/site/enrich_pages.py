#!/usr/bin/env python3
"""Rebuild the key pages with real block layout — columns, groups, buttons."""
import json, os, subprocess

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
    h("Where to buy"),
    p("Most of our packs are on itch.io. <em>Store link goes here.</em>"),
    btn("Browse the store", "#"),
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


def get_page(pid):
    r = call("wp_get_page", {"id": pid})
    return json.loads(r["result"]["content"][0]["text"])


def main():
    # Home and Assets get full rebuilds.
    for pid, content, name in ((9, HOME, "Home"), (12, ASSETS, "Assets")):
        r = call("wp_update_page", {"id": pid, "content": content})
        ok = "error" not in r
        print(f"  {'OK  ' if ok else 'FAIL'} {name}"
              + ("" if ok else f" — {r['error'].get('message')}"))

    # Services keeps its written detail; we replace the tail with laid-out blocks.
    cur = get_page(11)
    body = cur.get("content", {})
    body = body.get("raw") or body.get("rendered") or ""
    cut = body.find("<!-- wp:separator -->\n<hr class=\"wp-block-separator\"/>\n<!-- /wp:separator -->\n\n<!-- wp:heading -->\n<h2>How we work</h2>")
    if cut == -1:
        cut = body.find("How we work")
        cut = body.rfind("<!-- wp:separator -->", 0, cut) if cut > 0 else -1
    if cut > 0:
        r = call("wp_update_page", {"id": 11, "content": body[:cut] + SERVICES_TAIL})
        print(f"  {'OK  ' if 'error' not in r else 'FAIL'} Services")
    else:
        print("  SKIP Services — could not locate the tail to replace")


if __name__ == "__main__":
    main()
