---
title: Known Limitations
description: Browser-specific behavior to be aware of when using Sigilora fonts.
---

# Known Limitations

Sigilora converts text like `[-X]` into color symbols through the standard OpenType `liga` feature. Most browsers apply these ligatures reliably. There is one browser-specific shaping behavior to be aware of.

## Ligatures with a hyphen followed by a letter (WebKit)

In WebKit-based browsers — Safari on macOS and iOS — an OpenType `liga` ligature whose input sequence contains an ASCII hyphen-minus (`-`, U+002D) **immediately followed by a letter** is not applied. WebKit splits the shaping run at that position, so the ligature cannot be formed and the affected text renders as blank.

For the current Magic font this affects exactly two symbols: the negative loyalty counters for `X` and `N`:

- `[-X]` and `[-N]` do not render in Safari
- All other negative loyalty counters (`[-1]` … `[-25]`) and positive counters (`[+X]`, `[+N]`, `[+1]` …) render normally
- Chrome and Firefox apply these ligatures correctly

This is a WebKit text-shaping behavior, not a defect in the font. The font data, the ligature mappings, and the shapes are valid; the same glyphs shape correctly through HarfBuzz and CoreText.

No alternate rendering is currently provided. A future font update could map alternative minus characters — the Unicode MINUS SIGN (`−`, U+2212) or the NON-BREAKING HYPHEN (`‑`, U+2011) — to the same input glyph, since those do not trigger this WebKit behavior, but they are not mapped today. Until then, `[-X]` and `[-N]` render only in browsers that apply the ligature correctly (Chrome, Firefox).
