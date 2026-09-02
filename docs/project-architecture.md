# Sigilora Symbol Font Project Design

## 1. Background

Sigilora is a symbol font project aimed at game text. It uses OpenType ligatures to turn the text representations already established by game communities into color symbols, rendered inline within a line of text via COLR/CPAL.

The project's core value is not providing an ordinary icon font, but keeping symbols in their text identity:

- The original content can be copied, searched, and stored
- When the font is not loaded, it degrades to the game's existing text representation
- After the corresponding game font is loaded, the text representation automatically renders as color symbols
- Different games can keep their own established symbol syntax

Sigilora is a neutral project published independently of the current website. The website is just one consumer of it.

## 2. Goals

Sigilora aims to:

1. Provide embeddable, in-text color symbol fonts for games with mature symbol text representations
2. Let each game independently maintain its font content, COLR version, and font version
3. Reduce multi-game maintenance cost through a unified repository, build pipeline, and release entry point
4. Support web use, desktop installation, and a public online preview simultaneously
5. Let the website and other consumers integrate through stable release artifacts instead of depending on the font source repository

## 3. Non-Goals

The current design does not include the following:

- Establishing a unified cross-game symbol text syntax
- Merging all games' symbols into a single font file
- Requiring a page to load multiple game fonts in a single network request
- Creating a separate code repository per game
- Establishing a dedicated GitHub organization at the initial stage
- Implementing multiple switchable font build backends at the initial stage
- Defining the auto-configuration manifest protocol of the current website in this design
- Completing a per-asset license audit of third-party assets in this design

## 4. Project Identity and Naming

### 4.1 Overall Name

The overall project name is **Sigilora**.

The name keeps the modern root of `sigil` and derives it in a fantasy way, evoking the feeling of a symbol system or school of magic in a game world. The project accepts that a same-named use already exists on the internet and no longer changes the name.

### 4.2 Game Font Naming

All game fonts use a unified naming hierarchy:

- Font family: `Sigilora <Game>`
- PostScript/file identifier: uses a stable ASCII game identifier
- Web artifacts: per-game CSS and WOFF2
- Desktop artifacts: per-game TTF

The game display name and the stable game identifier should be separated. The display name is used for the font family and documentation; the stable identifier is used for directories, files, manifests, and export paths.

## 5. Repository and Project Boundaries

### 5.1 Independent Repository

Sigilora uses an independent repository. It is not placed in the website repository and is not a Git submodule of the website.

In the early stage, the independent repository may be hosted under an existing organization or personal account. A dedicated GitHub organization is established only when multiple Sigilora repositories, multiple maintainers, or independent permission management needs appear.

### 5.2 Website Integration Boundary

The website only consumes published Sigilora artifacts; it does not read or build font sources.

The website is allowed to detect and configure fonts through a script, but the script should rely on the machine-facing interface exposed by the npm package, not on the Sigilora repository directory structure. The specific structure of the root manifest is deferred to the integration design stage.

### 5.3 Repository Logical Structure

The Sigilora repository is font-engineering-centric rather than npm-package-centric or official-site-centric. Its main logical components include:

```text
sigilora/
├── pyproject.toml
├── src/sigilora_build/       # Python build and validation logic
├── fonts/<game>/             # canonical source data per game
├── packages/fonts/           # @sigilora/fonts publish directory
├── website/                  # Nuxt official site, docs and playground
└── tests/                    # font structure, mapping and shaping validation
```

The diagram above expresses component boundaries; the official site directory name may be adjusted to the final workspace convention when the independent repository is created, but the following responsibilities must not change:

- The Python toolchain is responsible for generating and validating fonts
- `packages/fonts/` is only responsible for npm consumer artifacts
- The official site consumes fonts through published artifacts and does not own font sources

## 6. Font Partitioning and Text Behavior

### 6.1 Per-Game Font Split

Each game produces an independent font file. A typical page usually uses only one game font, so cross-game merged fonts are not provided, and "compressing multiple fonts into one network request" is not a design goal.

Splitting per game:

- Isolates overlapping text representations between games
- Avoids unbounded growth of a single font
- Lets each game choose its COLR version independently
- Lets each game maintain its font version independently

### 6.2 Ligature Protocol

Each game font prefers the mature native symbol text representation already established in that game community; Sigilora does not invent a cross-game unified syntax.

As long as the corresponding Sigilora font is applied, matching text is converted to symbols by default through the standard `liga` feature. Code blocks or areas that should not be converted are handled by the consumer not applying the font, or by explicitly disabling ligatures.

Known browser limitation: in WebKit browsers (Safari on macOS and iOS), a `liga` ligature whose input contains an ASCII hyphen-minus (`-`, U+002D) immediately followed by a letter is not applied, because WebKit splits the shaping run at that position. For the Magic font this affects `[-X]` and `[-N]`. No alternate input characters are currently mapped for these two symbols. This is a shaping-engine behavior, not a font defect, and is not caught by HarfBuzz-based validation.

### 6.3 COLR Version

The COLR version is an independent build property of each font, not a project-wide global constraint:

- Fonts that currently need only flat color layers use COLRv0
- Fonts like PTCG that need gradients, opacity, or complex transforms can use COLRv1
- Fonts that do not need COLRv1 are not upgraded early just for a unified technology stack
- A COLRv1 font may additionally ship a COLRv0 fallback flavor: the same glyphs, ligatures, mappings, and font version encoded in COLRv0 (flat colors plus `currentColor`), so engines without COLRv1 — Safari/WebKit, native CoreText, Windows 10 DirectWrite, Android < 13 — render symbols instead of blank space. On the web the per-game CSS declares the v0 face first and the v1 face inside `@supports font-tech(color-COLRv1)`, so COLRv1-capable engines load the v1 flavor and everything else fails closed to v0. Desktop ZIPs distribute both flavors as separately named families (`… V0`).
- The COLR version is chosen per family, not per game: the full and Lite families of one game can differ. A family that only carries glyphs expressible in COLRv0 (flat fills and `currentColor`) can be built directly as COLRv0 — Pokémon TCG Lite does this — and then needs no `-v0` fallback. The fallback mechanism applies only to a family that is itself COLRv1.

## 7. Source Data and Build

### 7.1 Canonical Source Data

The canonical source data of each game includes:

- Normalized SVGs
- Ligature text mappings
- Glyph identifiers and display information
- Font internal version
- COLR target version
- Asset source and license records

Normalized SVGs and mapping data are the project's long-term source data. Build tool configuration is not a public contract.

### 7.2 Current Build Backend

`nanoemoji` is currently used to generate fonts. It exists as an internal build backend of `sigilora_build` and is not directly exposed to npm consumers or the official site.

The project only retains the architectural ability to replace the build backend; initially only the nanoemoji backend is implemented, and no plugin-style multi-builder system is built. Future migration to fontTools, a custom Python pipeline, or a UFO/fontmake workflow is acceptable as long as source data semantics, artifact contracts, and validation results stay consistent.

### 7.3 Build Artifacts

The same source data generates:

- WOFF2 for web use
- TTF for desktop installation
- CSS `@font-face` definitions
- Font and symbol metadata
- Data required by the specimen

Content-equivalent OTF files are not additionally generated for format symmetry.

## 8. npm Distribution and Versioning

### 8.1 Single-Package Distribution

All game fonts are published through one npm package:

```text
@sigilora/fonts
```

The package provides independent CSS, WOFF2, and metadata per game. Consumers import only the game entry they need, and the browser only requests the WOFF2 actually referenced. Including other small font files in the npm install is an acceptable maintenance cost.

The npm package contains only consumer artifacts, type declarations, and license information. It does not contain SVG sources, Python build implementations, or test code.

### 8.2 Two-Layer Version Model

The npm package version and the font version are independent of each other.

The npm package version only describes the release container and the public interface:

- Major: incompatible changes to export paths or public machine interfaces
- Minor: a new game font
- Patch: an update to any existing font artifact

Each game font maintains an independent SemVer in its OpenType metadata and its own metadata:

- Major: removed ligatures, changed existing text mappings, or removed glyphs
- Minor: new symbols, ligatures, or compatible aliases
- Patch: visual fixes that do not change mappings, outline optimization, or metadata fixes

A font Major upgrade does not require the npm package to upgrade Major in sync. Consumers need to judge the compatibility change of a specific game font through its font metadata.

### 8.3 Default Consumption

The default documentation recommends installing the npm package and self-hosting the fonts. An npm-supporting public CDN can be a convenience option, but it is not the default deployment method.

## 9. GitHub Release

Each release creates a GitHub Release aligned with the npm package version and a git tag.

The release includes:

- `Sigilora-Fonts-<package-version>.zip`: complete snapshot of all font files (TTF and WOFF2)
- `Sigilora-<Game>-<font-version>.zip`: independent download package per game font (TTF and WOFF2)
- `SHA256SUMS`: checksums of release assets

Each release re-attaches all games' independent ZIPs, even if some fonts did not change in that release. The font files are small, and a complete snapshot matters more than saving a little storage.

Release ZIPs contain both TTF and WOFF2 plus license information: TTF for desktop installation, WOFF2 for direct web self-hosting. COLRv1 fonts include their `-v0` fallback TTF and WOFF2 in the same ZIPs. Web consumption through npm still uses the per-game CSS and WOFF2 in the package. This practice matches common open-source font projects such as Noto Color Emoji, Material Symbols, and Font Awesome.

## 10. Validation and Quality Gates

The following blocking validation must be completed automatically before release:

1. OpenType, TTF, and WOFF2 file structures are valid
2. All declared ligatures shape correctly through HarfBuzz
3. Mappings have no duplicates, no missing SVGs, and no unreferenced glyphs
4. COLR/CPAL tables match the font's declared v0 or v1
5. TTF and WOFF2 agree on glyphs, mappings, and font internal version

The project also automatically generates a specimen page for each game, showing:

- Original text and ligature rendering results
- All symbols and the color palette
- Inline effects at multiple font sizes
- Copyable input text and usage code

Initially, cross-platform pixel-level snapshots are not used as a release blocker, because color font rendering is affected by browsers and operating systems. Structural, mapping, and shaping validation must block releases; visual checks are done through the public specimen.

## 11. Official Site and Documentation

### 11.1 Technical Direction

The Sigilora official site uses Nuxt 4. It is both a public site and documentation site, and an interactive specimen/playground for the fonts.

Core pages include at least:

- Project introduction and install entry
- Overview of supported games and font versions
- Per-game font details and complete symbol tables
- Real-time text input, font switching, and ligature preview
- CSS, npm, and desktop installation documentation
- Version history and compatibility notes

### 11.2 Multi-Language

The official site follows the dynamic i18n behavior pattern of the current project:

- Uses `@nuxtjs/i18n`
- Routing uses `no_prefix`
- Initial language is determined by browser language and Cookie
- `setLocale` is called dynamically when the user's language setting changes
- Nuxt UI locale is synced with the site language

Sigilora only reuses this behavior pattern; it does not depend on the `@tcg-cards/*` configuration or UI packages of the current repository.

The content division is as follows:

- Navigation, buttons, and playground interface copy use `vue-i18n`
- Guides, font documentation, and version history use per-language Nuxt Content Markdown

## 12. Licensing Boundary

Font graphics may come from redrawn originals, public sources, and purchased third-party drawings. Each game must record asset source and license basis.

This design does not assume that ordinary commercial-use licenses naturally allow:

- Converting graphics into font glyphs
- Publicly distributing them with the font binary
- Allowing users to install, embed, and redistribute the font
- Re-licensing under OFL or other licenses

The concrete asset audit and the final license mix are designed separately. Until the audit is complete, do not uniformly declare all fonts as OFL, and do not assume redistribution rights for third-party assets.

## 13. Deferred Items

The following items are explicitly deferred and do not block the current project boundaries from taking effect:

1. The fields, schema, and stability policy of the `@sigilora/fonts` root manifest
2. The script protocol for the website to automatically read the manifest and generate font configuration
3. Per-asset license audits and the final license mix for each game
4. The timing for establishing a dedicated Sigilora GitHub organization
5. Build backends other than nanoemoji
6. Pixel-level visual regression tests

These items must be confirmed separately before entering their corresponding implementation phase; implementers should not complete the design on their own.
