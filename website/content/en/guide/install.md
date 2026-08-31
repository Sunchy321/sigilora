---
title: Installation
description: How to use Sigilora fonts in your web project.
---

# Installation

Sigilora fonts are distributed as the npm package `@sigilora/fonts`.

## Quick start

Install the package:

```bash
npm install @sigilora/fonts
```

Import the CSS for your game:

```js
import '@sigilora/fonts/magic.css'
```

Then apply the font family:

```css
.sigilora-magic {
  font-family: 'Sigilora Magic', serif;
}
```

Matching text such as `{W}{U}{B}{R}{G}` is converted to color symbols automatically through the standard `liga` feature.

## Font families

- **Sigilora Magic** — the full font with all styles. Switch styles with `font-feature-settings: 'ss01'` (shadow) or `'ss02'` (flat).
- **Sigilora Magic Lite** — the default style only; smaller.

> See also: [npm package](/docs/guide/install-npm) · [desktop](/docs/guide/install-desktop)
