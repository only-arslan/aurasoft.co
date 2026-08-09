#!/usr/bin/env python3
"""Publish the privacy policy page at /privacy."""
import importlib.util, time, json, sys

spec = importlib.util.spec_from_file_location(
    "e", "/home/user/aurasoft.co/scripts/site/enrich_pages.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

h, p, sep, eyebrow, cols, card = m.h, m.p, m.sep, m.eyebrow, m.cols, m.card


def ul(items):
    li = "".join(f"<li>{i}</li>" for i in items)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{li}</ul>\n<!-- /wp:list -->'


EMAIL = "[YOUR CONTACT EMAIL]"

CONTENT = "\n\n".join([
    eyebrow("Legal · last updated 9 August 2026"),
    h("Privacy Policy", 1),
    p("This policy explains what information Aurasoft collects when you use our "
      "mobile games and applications, how we use it, and the choices you have.",
      "aura-lead"),
    p("Aurasoft is a game and software studio operating in Australia and Pakistan. "
      "In this policy, &quot;we&quot;, &quot;us&quot; and &quot;our&quot; mean Aurasoft; "
      "&quot;apps&quot; means the mobile games and applications we publish."),
    sep(),

    h("Information we collect"),
    h("Information you give us", 3),
    p("Most of our apps can be used without giving us any personal information. If you "
      "contact us for support, we receive your email address and whatever you choose to "
      "include in your message."),

    h("Information collected automatically", 3),
    p("When you use our apps, certain information is collected automatically by the app "
      "and by the third-party services described below:"),
    ul([
        "<strong>Device information</strong> — device model, operating system version, "
        "language and region settings",
        "<strong>Advertising identifier</strong> — your Google Advertising ID (Android) "
        "or Identifier for Advertisers (iOS), used to serve and measure advertising",
        "<strong>Usage data</strong> — in-app events such as levels started and "
        "completed, session length and feature use",
        "<strong>Diagnostic data</strong> — crash reports and performance data, which "
        "may include device state at the time of a crash",
        "<strong>Approximate location</strong> — inferred from your IP address at "
        "country or region level. We do not collect precise GPS location.",
    ]),
    p("We do not ask for or collect your name, postal address, phone number, or payment "
      "card details. Purchases, where offered, are handled entirely by Google Play or "
      "the Apple App Store, and we never receive your payment details."),
    sep(),

    h("Third-party services"),
    p("Our apps use services provided by other companies. These services collect and "
      "process data under their own privacy policies:"),
    cols(
        card("Google AdMob",
             "Serves advertising in our apps and measures its performance. AdMob may "
             "use your advertising identifier to show relevant ads.", "cyan"),
        card("Google Play Services",
             "Provides core platform functionality on Android, including sign-in, "
             "crash reporting and app distribution.", "violet"),
        card("Analytics",
             "Aggregated usage analytics that help us understand which parts of a game "
             "people play and where they get stuck.", "magenta"),
    ),
    p("You can read Google's privacy policy at "
      "<a href=\"https://policies.google.com/privacy\" rel=\"noopener\" "
      "target=\"_blank\">policies.google.com/privacy</a> and Apple's at "
      "<a href=\"https://www.apple.com/legal/privacy/\" rel=\"noopener\" "
      "target=\"_blank\">apple.com/legal/privacy</a>."),
    sep(),

    h("How we use information"),
    ul([
        "To operate our apps and keep them working correctly",
        "To display advertising, which is how most of our games are funded",
        "To diagnose crashes and fix bugs",
        "To understand which features are used, so we can improve them",
        "To respond to support requests you send us",
    ]),
    p("We do not sell your personal information, and we do not share it with third "
      "parties except the service providers described above."),
    sep(),

    h("Advertising and your choices"),
    p("Our games are supported by advertising. You have direct control over how that "
      "advertising uses your data:"),
    ul([
        "<strong>Android</strong> — Settings → Google → Ads, where you can delete or "
        "reset your advertising ID and opt out of personalised advertising",
        "<strong>iOS</strong> — Settings → Privacy &amp; Security → Tracking, where you "
        "can turn off app tracking requests entirely",
    ]),
    p("Turning off personalised advertising does not remove ads from our games; it "
      "means the ads you see are less relevant to you."),
    sep(),

    h("Children's privacy"),
    p("Our apps are not directed at children under 13, and we do not knowingly collect "
      "personal information from children under 13. Where an app is listed as suitable "
      "for a general audience that includes children, we configure advertising to serve "
      "non-personalised ads only, in line with Google Play's Families policy."),
    p("If you believe a child has provided us with personal information, contact us and "
      "we will delete it."),
    sep(),

    h("Data retention and security"),
    p("We keep diagnostic and usage data only as long as it is useful for the purposes "
      "described above, and support correspondence for as long as needed to resolve "
      "your enquiry. Data held by third-party services is retained under their own "
      "policies."),
    p("We take reasonable technical and organisational measures to protect information, "
      "though no method of transmission or storage is completely secure."),
    sep(),

    h("Your rights"),
    p("Depending on where you live, you may have the right to access the personal "
      "information we hold about you, ask us to correct or delete it, object to certain "
      "processing, or withdraw consent. This includes rights under the Australian "
      "Privacy Principles, the EU and UK GDPR, and the California Consumer Privacy Act."),
    p("To exercise any of these rights, contact us using the details below. We will "
      "respond within the time required by the applicable law."),
    sep(),

    h("International transfers"),
    p("We operate in Australia and Pakistan, and the services we use process data in "
      "other countries including the United States. Where information is transferred "
      "internationally, we rely on the safeguards offered by those service providers."),
    sep(),

    h("Changes to this policy"),
    p("We may update this policy as our apps change or the law requires. The date at the "
      "top of this page shows when it was last revised. Material changes will be "
      "reflected here before they take effect."),
    sep(),

    h("Contact us"),
    p("Questions about this policy, or about the information we hold, can be sent to:"),
    p(f"<strong>{EMAIL}</strong>"),
    p("Aurasoft — Australia &amp; Pakistan"),
])


def main():
    for attempt in range(5):
        try:
            r = m.call("wp_add_page", {
                "title": "Privacy Policy",
                "slug": "privacy",
                "content": CONTENT,
                "status": "publish",
            })
            if "error" in r:
                print("  FAIL:", r["error"].get("message")); return
            obj = json.loads(r["result"]["content"][0]["text"])
            print(f"  OK  Privacy Policy  id={obj.get('id')}  /{obj.get('slug')}/")
            return
        except Exception as exc:
            if attempt == 4:
                print("  FAIL:", exc)
            else:
                time.sleep(2 ** attempt)


if __name__ == "__main__":
    main()
