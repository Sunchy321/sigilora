---
title: Known Limitations
description: Browser-specific behavior to be aware of when using Sigilora fonts.
---

# Known Limitations

Sigilora converts text like `[-X]` into color symbols through the standard OpenType `liga` feature. Most browsers apply these ligatures reliably. Color rendering depends on each game's COLR version, so two browser-specific behaviors are worth knowing: one about color, one about shaping.

## COLRv1 support and Safari

Sigilora fonts store their color glyphs as COLR (v0 or v1 depending on the game). COLRv0 is supported by every major engine, including Safari/WebKit and the native Apple text stack. COLRv1 is supported by Chromium and Firefox but not by Safari/WebKit, which never implemented COLRv1.

Games that ship COLRv1 — the full Pokémon TCG and Riftbound families, and Riftbound Lite — therefore also ship a matching COLRv0 fallback flavor: the same glyphs, ligatures, and font version, with colors encoded as flat fills and `currentColor`. The game CSS serves this fallback automatically — on an engine without COLRv1 you get the v0 flavor, and where COLRv1 works you get the full v1 flavor. There is nothing to configure.

Pokémon TCG Lite is the exception: it carries only the bare `currentColor` default style, which needs no COLRv1, so it is built as a single COLRv0 font and needs no fallback.

In a v0 flavor the effects that need COLRv1 degrade by design:

- Pokémon `orb` (`ss01`, the glossy energy ball) is drawn from the `flat` style's art, so it renders as the flat badge. The default text-color bare symbol and the flat badges are unaffected.
- Riftbound `[A]` any-power rainbow renders as a single text-color (`currentColor`) rune. Domain runes, numbers, and the inverted style are unaffected.

The consequence: on Safari and other v0-only contexts — such as native Apple apps that render text through CoreText — glossy energy balls and the Riftbound rainbow appear as their flat/text-color equivalents instead of blank space.

## Ligatures with a hyphen followed by a letter (WebKit)

In WebKit-based browsers — Safari on macOS and iOS — an OpenType `liga` ligature whose input sequence contains an ASCII hyphen-minus (`-`, U+002D) **immediately followed by a letter** is not applied. WebKit splits the shaping run at that position, so the ligature cannot be formed and the affected text renders as blank.

For the current Magic font this affects exactly two symbols: the negative loyalty counters for `X` and `N`:

- `[-X]` and `[-N]` do not render in Safari
- All other negative loyalty counters (`[-1]` … `[-25]`) and positive counters (`[+X]`, `[+N]`, `[+1]` …) render normally
- Chrome and Firefox apply these ligatures correctly

This is a WebKit text-shaping behavior, not a defect in the font. The font data, the ligature mappings, and the shapes are valid; the same glyphs shape correctly through HarfBuzz and CoreText.

No alternate rendering is currently provided. A future font update could map alternative minus characters — the Unicode MINUS SIGN (`−`, U+2212) or the NON-BREAKING HYPHEN (`‑`, U+2011) — to the same input glyph, since those do not trigger this WebKit behavior, but they are not mapped today. Until then, `[-X]` and `[-N]` render only in browsers that apply the ligature correctly (Chrome, Firefox).
