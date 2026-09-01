# @sigilora/fonts

npm publish directory for consumer artifacts.

This directory is a **generated staging area** produced by `sigilora package <game>`; its per-game subdirectories are gitignored. Each game's package contains:

- `magic.css` — a single CSS declaring both `@font-face` entries (full and lite)
- `magic.woff2` — full font (all styles, `ssXX` switching)
- `magic-lite.woff2` — lite font (default style + ligatures)
- `magic.json` — font and symbol metadata

The root manifest schema and publish tooling are deferred (see the architecture doc, section 13).
