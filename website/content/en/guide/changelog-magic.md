---
title: Magic changelog
description: Version history and compatibility notes for the Sigilora Magic font.
---

# Magic: The Gathering

Version history and compatibility notes for the **Sigilora Magic** font.

Sigilora Magic ships as the full `Sigilora Magic` family (default, shadow, and flat styles, switched via `ss01` / `ss02`) and the lite `Sigilora Magic Lite` family (default style only). The current release covers 114 symbols — mana, hybrid, phyrexian, other, special, and loyalty counters — using COLRv0.

Font versions follow SemVer: a **Major** bump removes ligatures, changes existing text mappings, or removes glyphs; a **Minor** bump adds symbols or compatible aliases; a **Patch** is a visual fix.

## Known issues

- In WebKit browsers (Safari on macOS and iOS), ligatures whose input contains an ASCII hyphen followed by a letter — `[-X]` and `[-N]` — do not render, due to a WebKit text-shaping behavior. Chrome and Firefox are unaffected. See [known limitations](/docs/guide/known-limitations).

## Sigilora Magic 1.2.1

- Flat-mode foregrounds follow the text color: numeric-mana symbols (including `{X}`/`{Y}`/`{Z}`), the tap symbol, hybrid-mana frames and their numeric halves, and the snow frame.

## Sigilora Magic 1.2.0

- Dark-mode support.

## Sigilora Magic 1.1.0

- Add a ligature for `{½}`.
- Support `[+N]` / `[-N]` loyalty-counter rendering.

## Sigilora Magic 1.0.1

- Adjust the flat `{W}` color.

## Sigilora Magic 1.0.0

- Add loyalty-counter symbols.

## Sigilora Magic 0.6.0

- Add the flat style for `{S}`.

## Sigilora Magic 0.5.0

- Complete the flat symbol styles.

## Sigilora Magic 0.4.1

- Fix shadow rendering.

## Sigilora Magic 0.4.0

- Add shadow-style icons.

## Sigilora Magic 0.3.0

- Add the complete icon set.

## Sigilora Magic 0.2.0

- Support multiple ligatures per symbol.

## Sigilora Magic 0.1.0

- Create the Magic symbol font.
