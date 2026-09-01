---
title: Riftbound changelog
description: Version history and compatibility notes for the Sigilora Riftbound font.
---

# Riftbound

Version history and compatibility notes for the **Sigilora Riftbound** font.

Sigilora Riftbound ships as the `Sigilora Riftbound` family (default style) and the lite `Sigilora Riftbound Lite` family. The current release covers 22 symbols — exhaust, might, six domain runes, any power, and the numbers 0–12 — using COLRv1 (the any-power rainbow uses a gradient). The inverted (反色, monochrome white) style is available via the `ss01` feature.

Font versions follow SemVer: a **Major** bump removes ligatures, changes existing text mappings, or removes glyphs; a **Minor** bump adds symbols or compatible aliases; a **Patch** is a visual fix.

## Sigilora Riftbound 0.2.0

- Add the Riftbound symbol set: `[E]` exhaust, `[M]` might, domain runes `[R]` `[G]` `[B]` `[O]` `[P]` `[Y]`, `[A]` any power, and `[0]`–`[12]` number symbols.
- Runes are bare domain-color glyphs (no outer circle); the `[A]` rainbow uses a COLRv1 gradient.
- COLRv1 with an inverted (反色, monochrome white) style switched via `ss01`.
