---
title: Installation
description: How to use Sigilora fonts in your web project.
---

# Installation

Sigilora fonts are distributed as the npm package `@sigilora/fonts`. Each game ships its own CSS, WOFF2, and font family.

## Quick start

Install the package:

```bash
npm install @sigilora/fonts
```

Import the CSS for your game and apply its font family. For Magic:

```js
import '@sigilora/fonts/magic.css'
```

```css
.sigilora-magic {
  font-family: 'Sigilora Magic', serif;
}
```

For Lorcana:

```js
import '@sigilora/fonts/lorcana.css'
```

```css
.sigilora-lorcana {
  font-family: 'Sigilora Lorcana', serif;
}
```

For Riftbound:

```js
import '@sigilora/fonts/riftbound.css'
```

```css
.sigilora-riftbound {
  font-family: 'Sigilora Riftbound', serif;
}
```

Matching game text is converted to color symbols automatically through the standard `liga` feature — for example `{W}{U}{B}{R}{G}` in Magic, `{S}{W}{L}{I}` in Lorcana, or `[R][M]` in Riftbound.

## Supported games

- **Magic: The Gathering** — import `@sigilora/fonts/magic.css`, font family `Sigilora Magic`. Symbols such as `{W}`, `{U}`, `{B}`, `{R}`, `{G}`, `{T}`, `[+1]`…
- **Lorcana** — import `@sigilora/fonts/lorcana.css`, font family `Sigilora Lorcana`. Symbols such as `{S}`, `{W}`, `{L}`, `{M}`, `{I}`, `{C}`, `{E}`…
- **Riftbound** — import `@sigilora/fonts/riftbound.css`, font family `Sigilora Riftbound`. Symbols such as `[E]`, `[M]`, `[R]`, `[A]`, `[2]`…

## Font families

Each game provides two families:

- **Sigilora <Game>** — the full font. Magic additionally ships shadow and flat styles, switched via `font-feature-settings: 'ss01'` (shadow) or `'ss02'` (flat). Riftbound ships an inverted (反色) style via `'ss01'`.
- **Sigilora <Game> Lite** — the default style only; smaller.

> See also: [npm package](/docs/guide/install-npm) · [desktop](/docs/guide/install-desktop) · [known limitations](/docs/guide/known-limitations)
