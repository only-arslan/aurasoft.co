# Aurasoft — brand and visual direction

Neon, dark-first. The look a game studio can wear without it feeling costume.

## The idea

Neon works when it's **restrained**. A dark, near-black canvas with a small
number of saturated accents reads as premium and deliberate. The same colours
sprayed everywhere read as a 2003 gaming-clan page.

So: deep dark backgrounds, generous space, one dominant accent (cyan), a second
for contrast (magenta), and glow used to draw the eye to exactly one thing per
screen.

## Palette

### Backgrounds

| Token | Hex | Use |
|---|---|---|
| `--bg-void` | `#07070E` | page background, deepest layer |
| `--bg-base` | `#0B0B16` | main sections |
| `--bg-surface` | `#141426` | cards, panels |
| `--bg-elevated` | `#1C1C33` | hover states, raised elements |

### Neon accents

| Token | Hex | Use |
|---|---|---|
| `--neon-cyan` | `#00F0FF` | **primary** — links, key CTAs, active states |
| `--neon-magenta` | `#FF2E88` | **secondary** — highlights, second CTA, hover |
| `--neon-violet` | `#A24DFF` | bridges cyan and magenta in gradients |
| `--neon-lime` | `#B6FF3C` | sparingly — "in development" tags, success |

### Text

| Token | Hex | Use |
|---|---|---|
| `--text-hi` | `#F4F4FA` | headings, body |
| `--text-mid` | `#A8A8C0` | secondary text, descriptions |
| `--text-low` | `#6E6E8A` | meta, captions, disabled |

### Signature gradient

`linear-gradient(135deg, #00F0FF 0%, #A24DFF 50%, #FF2E88 100%)`

For hero headline accents, section dividers, button fills. Use it once or twice
per page — it stops being a signature if it's on everything.

## Rules that keep it from looking cheap

**Never set body text in neon.** Neon is for headings, accents and edges.
Long-form text is `--text-hi`; anything else is a headache to read.

**One glow per viewport.** Glow marks the single most important element on
screen. Two competing glows means neither wins.

**Glow with shadow, not colour:**
```css
box-shadow: 0 0 20px rgba(0, 240, 255, 0.35), 0 0 60px rgba(0, 240, 255, 0.15);
```

**Keep saturation off large areas.** Neon belongs on borders, text, small fills
and thin rules — never a full-width saturated block.

**Contrast is not optional.** `#00F0FF` on `#0B0B16` is roughly 13:1 — excellent.
`#00F0FF` on white would be about 1.6:1 and illegible. This palette only works
dark; don't port it to a light theme.

## Typography

**Headings:** a geometric or slightly technical sans — Space Grotesk, Chakra
Petch, Rajdhani or Orbitron. Tight tracking, heavy weight, often uppercase for
short labels.

**Body:** something plain and readable — Inter, DM Sans, or system UI. Body text
should not be doing the personality work; the headings and colour do that.

**Scale:** big jumps. Hero at 3.5–5rem, section headings 2–2.5rem, body 1rem–1.125rem.
Timid type undercuts the whole look.

## Imagery

Game key art and asset renders are the visual content — the design should frame
them, not compete. Dark surrounds make screenshots pop with no extra work.

For screenshots and pack art, a 1px `--neon-cyan` border at ~40% opacity plus a
soft glow on hover ties them into the system.

Avoid stock photos of people at laptops. A studio that makes its own art should
never show stock.

## Applying it in The7

The7 sets most of this under **Theme Options**:

- **General → Colors** — accent colour `#00F0FF`, secondary `#FF2E88`
- **General → Background** — page background `#0B0B16`
- **Typography** — heading and body fonts, plus the scale above
- **Header → Style** — transparent over the hero, solid `#0B0B16` on scroll
- **Buttons** — primary filled cyan with dark text; secondary outlined cyan
  with cyan text

Anything The7 can't reach goes in **Theme Options → Custom CSS**, using the
tokens above as CSS variables so there's one place to change them.

## Accessibility

- Body text stays at `--text-hi` on dark — comfortably above 4.5:1
- Never rely on colour alone for state; pair with an icon or label
- Glow is decorative only — never the sole indicator that something is focused
- Keep visible focus rings; a cyan outline suits the theme and is genuinely useful
