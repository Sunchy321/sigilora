# tests

Font structure, mapping, and shaping validation.

Blocking validation that must pass before release:

1. OpenType, TTF, and WOFF2 file structures are valid
2. All declared ligatures shape correctly through HarfBuzz
3. Mappings have no duplicates, no missing SVGs, and no unreferenced glyphs
4. COLR/CPAL tables match the font's declared v0 or v1
5. TTF and WOFF2 agree on glyphs, mappings, and font internal version
