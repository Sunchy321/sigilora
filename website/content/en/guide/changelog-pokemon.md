---
title: Pokémon TCG changelog
description: Version history and compatibility notes for the Sigilora Pokemon font.
---

# Pokémon TCG

Version history and compatibility notes for the **Sigilora Pokemon** font.

Sigilora Pokemon ships as the full `Sigilora Pokemon` family (default, orb, and flat styles) and the lite `Sigilora Pokemon Lite` family (the default style only). The current release covers the 11 Pokémon TCG basic energy symbols using COLRv1. Each energy converts through the standard `liga` feature from both a bracket and a brace spelling of the energy's single letter — `[G]` and `{G}` for Grass, for example. The letters follow the community EssentiarumTCG convention that the icon reconstruction was extracted from: C colorless, D darkness, F fighting, G grass, L lightning, M metal, N dragon, P psychic, R fire, W water, Y fairy.

Font versions follow SemVer: a **Major** bump removes ligatures, changes existing text mappings, or removes glyphs; a **Minor** bump adds symbols or compatible aliases; a **Patch** is a visual fix.

## Sigilora Pokemon 0.3.0

- Add a COLRv0 fallback flavor of the full font, identical in glyphs, ligatures, and version. Engines without COLRv1 — Safari/WebKit, native CoreText, Windows 10 DirectWrite, Android 13 and below — receive it automatically through the game CSS on the web (or by installing the bundled `… V0` desktop font), so symbols render instead of blank space.
- In that v0 fallback the `orb` (`ss01`) style is drawn from the `flat` style's art, so the glossy energy ball renders as the flat disc where COLRv1 is unavailable. The default text-color bare symbol and the flat badges are unchanged.
- The Lite family (default style only) is built as COLRv0 directly — its bare `currentColor` symbols need no COLRv1 — so it has no v1/fallback split and renders everywhere.

## Sigilora Pokemon 0.2.0

- Add two new styles per energy: `orb` (`ss01`, the glossy energy ball) and `flat` (`ss02`, a flat round badge filled with the font's official disc color).
- Change the `default` style to the bare energy symbol in the text color (`currentColor`, with no outer disc) for embedding in running text. The default, orb, and flat styles share one outline per energy, taken from the glyph its `[X]`/`{X}` spelling renders.

## Sigilora Pokemon 0.1.0

- Add the Pokémon TCG basic energy set: `[G]`/`{G}` Grass, `[R]`/`{R}` Fire, `[W]`/`{W}` Water, `[L]`/`{L}` Lightning, `[P]`/`{P}` Psychic, `[F]`/`{F}` Fighting, `[D]`/`{D}` Darkness, `[M]`/`{M}` Metal, `[Y]`/`{Y}` Fairy, `[N]`/`{N}` Dragon, `[C]`/`{C}` Colorless.
- Each energy is registered under both a bracket (`[G]`) and a brace (`{G}`) spelling so established game text is matched either way.
- COLRv1 with a single default style; no stylistic-set variants yet.
