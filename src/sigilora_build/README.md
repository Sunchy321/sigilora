# sigilora_build

Python build and validation logic.

- Uses `nanoemoji` as the current internal build backend to generate fonts (WOFF2 / TTF / CSS).
- Owns the blocking release validation: OpenType structure, HarfBuzz shaping, mapping consistency, COLR/CPAL conformance, and TTF/WOFF2 consistency.
- Exists as an internal toolchain; it is never exposed to npm consumers or the official site.
