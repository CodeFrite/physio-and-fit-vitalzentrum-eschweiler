# physio & fit — Vitalzentrum Eschweiler

A rebuild of [vitalzentrum-eschweiler.de](https://vitalzentrum-eschweiler.de/) (currently a
GoDaddy Website Builder site). **Every word of the original German copy is kept verbatim** —
only the design, structure and interaction are new.

## Design direction

> **"Bewegung ist Medizin"** — clinical precision, delivered calm.

Their own method is *dosed* movement: the Milon circuit runs 11 minutes a round, 33 minutes a
session, 66–99 minutes a week; Rehasport is prescribed at 50 units over 18 months. The rooms
have forest murals printed on the walls and a ring light on the ceiling. The design is built
from that, not from generic "wellness".

| | |
|---|---|
| **Ground** | `#EEF1EA` pale birch-green light (dark: `#0B1310`) |
| **Ink** | `#122019` deep forest-black |
| **Moss** | `#4F6B57` rules, meta, quiet marks |
| **Puls** | `#6E960A` the brand lime, tuned to hold on a light ground |
| **Klinik** | `#1E3D55` the brand navy, authority marks only |

- **Archivo** (variable width, expanded caps) for display — engineered, signage-like
- **Source Serif 4** for the long German prose
- **IBM Plex Mono** for *every number on the site* — times, prices, durations, section
  markers. That is the dosage thread that ties the identity together.

Layout is a persistent left spine (a treatment-chart rule with a slow-breathing progress
marker) plus an asymmetric measure: a narrow mono rail for labels, a ~63ch serif column for
reading. The hero carries the **Zirkel** — a ring that completes one revolution every 11
seconds, the length of one Milon round.

## What changed beyond the visuals

- **Öffnungszeiten were recovered.** On the live site that page is empty; the hours only
  existed as pixels inside a JPEG. They are now real, selectable text — plus a live
  "open now" indicator in the header and today's column marked in the table.
- **Sixteen routes became ten.** `physiopraxis` absorbs `anwendungsbereiche`,
  `trainingsflaeche` absorbs the three training pages, `kurse` absorbs `kurse-vor-ort` and
  `reha-sport`, `karriere` absorbs both job pages, `kontakt` absorbs `oeffnungszeiten`.
  Every old address stays a valid deep link — it keeps its own title and description and
  scrolls to its section, so a printed flyer or a Google result still lands in the right
  place.
- **German and English**, with English at an `en/` prefix in the hash. The language is never
  stored — no cookie, no `localStorage` — so § 25 TTDSG never applies. Copy is duplicated in
  the DOM rather than swapped by script, so the page still works with JS off.
- A full-screen mobile menu, breadcrumbs, and per-page titles/descriptions (the site's own
  SEO strings).
- The six course descriptions became an accordion instead of one 9,000-character wall.
- The `Begriff: Erklärung` bullet lists became definition lists.
- The contact form composes a real mail draft (no backend); phone, e-mail and directions
  are one tap away throughout.
- Impressum and the full Datenschutzerklärung are carried over intact. The cookie notice is
  *not*: there is no analytics and no third-party embed, so its text ("um den
  Website-Traffic zu analysieren") would have been false. It is the only text block that
  left the site.
- **Fonts are self-hosted** (437 KB, latin + latin-ext). The page loads zero external
  resources, so no visitor IP reaches a third party and there is nothing to consent to.
- Light and dark themes with a real switch, not just `prefers-color-scheme` — and the choice
  is not stored either. `prefers-reduced-motion` honoured, visible focus states,
  keyboard-navigable menus.

## Layout

```
index.html              the deployable site (single file, hash-routed)
assets/fonts/           Archivo, Source Serif 4, IBM Plex Mono — self-hosted woff2
assets/img/             the masters as received from the old builder
assets/img/opt/         the shipped set — WebP + JPEG fallback, name-WIDTH.{webp,jpg}
docs/konzept.html       the client-facing case: IA, colour, type, legal, UX
src/*.html              the parts index.html is assembled from — edit these
build/assemble.py       src/*.html            -> index.html
build/gen-datenschutz.py  policy plain text   -> structured HTML
build/make-artifact.py  index.html            -> dist/ (images inlined, single file)
build/verify-text.py    asserts every original sentence survives verbatim
dist/vitalzentrum.html  single-file build for preview/sharing
```

## Build

```sh
python3 build/assemble.py        # rebuild index.html after editing src/
python3 build/make-artifact.py   # rebuild the single-file version
python3 -m http.server 8000      # then open http://localhost:8000
```

Deploy by uploading `index.html` and `assets/` to any static host.

## Verification

`build/verify-text.py` compares the rebuild against text scraped from the live site:

```
507 sentences checked, 0 content differences
286 Datenschutzerklärung lines checked, 0 differences
```

## Known gap

The **Anwendungsbereiche** page says "Hier erhalten Sie demnächst alle Informationen…" on the
live site too — there is no content to carry over yet.
