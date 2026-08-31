**NEVER make design decisions on your own. Always ask the user before deciding.**

**NEVER revert design decisions previously made without the user's explicit request.**

## Project Overview

Sigilora is a symbol font project for game text. It uses OpenType ligatures to turn established game-community text representations into color symbols rendered inline within a line of text via COLR/CPAL.

The core value is that symbols keep their text identity: the original content stays copyable, searchable, and storable, and it degrades back to the game's existing text representation when the font is not loaded.

Sigilora is a neutral project published independently of the current website; the website is just one consumer.

## Architecture Reference

Use `docs/project-architecture.md` and `docs/project-architecture.zh-CN.md` as the stable reference for project boundaries, repository structure, versioning, and deferred decisions.

When a new requirement changes those stable boundaries, update both language versions of the architecture doc together and confirm with the user.

## Repository Structure

```text
sigilora/
├── pyproject.toml
├── src/sigilora_build/       # Python build and validation logic
├── fonts/<game>/             # canonical source data per game
├── packages/fonts/           # @sigilora/fonts publish directory
├── website/                  # Nuxt official site, docs and playground
└── tests/                    # font structure, mapping and shaping validation
```

Fixed responsibilities (do not change):

- The Python toolchain generates and validates fonts.
- `packages/fonts/` is only responsible for npm consumer artifacts.
- The official site consumes fonts through published artifacts and does not own font sources.

## Key Design Conventions

- Fonts are split per game. Never merge games into one font file.
- Prefer each game's mature native symbol text representation; matching text converts through the standard `liga` feature by default.
- The COLR version is a per-font build property, not a project-wide constraint: COLRv0 for flat color layers; COLRv1 for fonts like PTCG that need gradients, opacity, or complex transforms.
- The current build backend is `nanoemoji`, internal to `sigilora_build` and never exposed to npm consumers or the official site.
- Normalized SVGs and mappings under `fonts/<game>/` are the long-term source data; build tool configuration is not a public contract.

## npm Distribution (@sigilora/fonts)

- All game fonts ship in a single npm package; each game has its own CSS, WOFF2, and metadata entry.
- The npm package contains only consumer artifacts, type declarations, and license information — no SVG sources, Python build code, or test code.
- Two-layer versioning:
  - npm package version: Major = incompatible export-path or public machine-interface changes; Minor = a new game font; Patch = an update to any existing font artifact.
  - Font SemVer: Major = removed ligatures, changed existing mappings, or removed glyphs; Minor = new symbols, ligatures, or compatible aliases; Patch = visual fixes that do not change mappings, outline optimization, or metadata fixes.
  - A font Major upgrade does not require the npm package to upgrade Major in sync; consumers judge compatibility through font metadata.

## GitHub Release

- Each release creates a GitHub Release aligned with the npm package version and a git tag.
- Assets: `Sigilora-Fonts-<package-version>.zip`, per-game `Sigilora-<Game>-<font-version>.zip`, and `SHA256SUMS`.
- Desktop ZIPs carry TTF and license information; web artifacts live in the npm WOFF2.

## Blocking Validation Before Release

1. OpenType, TTF, and WOFF2 file structures are valid
2. All declared ligatures shape correctly through HarfBuzz
3. Mappings have no duplicates, no missing SVGs, and no unreferenced glyphs
4. COLR/CPAL tables match the font's declared v0 or v1
5. TTF and WOFF2 agree on glyphs, mappings, and font internal version

Pixel-level snapshots are not a release blocker initially; visual checks go through the public specimen.

## Website

- Nuxt 4; a public site, documentation, and an interactive specimen/playground.
- i18n: `@nuxtjs/i18n`, `no_prefix` routing, initial language from browser language + Cookie, `setLocale` on change, Nuxt UI locale synced with the site language.
- Reuse the behavior pattern only; do not depend on the website's `@tcg-cards/*` configuration or UI packages.
- UI copy via `vue-i18n`; guides, font documentation, and version history as per-language Nuxt Content Markdown.

## Licensing Boundary

- Each game must record asset source and license basis.
- Never assume ordinary commercial-use licenses permit: converting graphics into glyphs, distributing with the font binary, installing/embedding/redistributing, or re-licensing under OFL.
- Until per-asset audits finish, do not declare all fonts as OFL.

## Deferred Items

Do not complete these designs on your own; confirm them before entering their implementation phase:

1. `@sigilora/fonts` root manifest schema and stability policy
2. Website script protocol for reading the manifest and generating font configuration
3. Per-asset license audits and the final license mix
4. Timing for a dedicated Sigilora GitHub organization
5. Build backends other than nanoemoji
6. Pixel-level visual regression tests

## Commit Messages

Use Conventional Commits, matching the current website repository's convention. `fix` commits must describe the problem that was solved, not how it was fixed.
