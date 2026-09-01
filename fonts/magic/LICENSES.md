# LICENSES — Magic: The Gathering

This file records the asset sources and license basis for `fonts/magic/`.

## 1. Base symbol SVGs (default style)

- Location: `fonts/magic/raw/default/` (84 symbols)
- Source: Scryfall (`https://svgs.scryfall.io/card-symbols/...`)
- License: these are graphical renderings of Wizards of the Coast (WotC) card symbols, governed by the WotC Fan Content Policy. Neither Scryfall nor WotC grants the right to convert the graphics into glyphs, distribute them with a font binary, or re-license them (e.g., under OFL).

## 2. Style variants (original work layered on the base)

- Location: generated at build time from `fonts/magic/raw/default/` and `fonts/magic/raw/components/`; special cases kept as files under `fonts/magic/raw/static/`
- Source: original work by the project author, layered on top of the base Scryfall SVGs. The raw Scryfall files contain no shadows; the shadow style, the flat recoloring, and the special-case shadows for `100`, `1000000`, `half-white`, `half-red` and the snow flat are the author's own additions.
- License: the added layers are original work; the base glyphs underneath remain WotC/Scryfall IP.

## 3. Composition parts (components)

- Location: `fonts/magic/raw/components/` (19 parts)
- Source: not part of Scryfall's card-symbol set; the project's own decomposition parts for composing hybrid, phyrexian, loyalty-counter, and other symbols.
- License: original building blocks, combined with the Scryfall base glyphs.

## 4. Loyalty-counter glyph outlines

- Location: `fonts/magic/raw/loyalty_glyphs.json` — the digit/sign glyph outlines (`0-9`, `+`, `−`, `X`, `N`) used to build the loyalty counters.
- Source: original work by the project author, extracted as pure SVG geometry. No external commercial font is required at build time.
- License: the outlines are treated as the project's own layered work (see THIRD_PARTY_NOTICES.md); the loyalty counter presentation is based on the existing Magic: The Gathering depiction.
