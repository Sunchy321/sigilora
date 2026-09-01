---
title: 安装
description: 如何在 Web 项目中使用 Sigilora 字体。
---

# 安装

Sigilora 字体通过 npm 包 `@sigilora/fonts` 分发。每个游戏都有独立的 CSS、WOFF2 与字体族。

## 快速开始

安装包：

```bash
npm install @sigilora/fonts
```

导入对应游戏的 CSS 并应用其字体族。以 Magic 为例：

```js
import '@sigilora/fonts/magic.css'
```

```css
.sigilora-magic {
  font-family: 'Sigilora Magic', serif;
}
```

以 Lorcana 为例：

```js
import '@sigilora/fonts/lorcana.css'
```

```css
.sigilora-lorcana {
  font-family: 'Sigilora Lorcana', serif;
}
```

以符文战场（Riftbound）为例：

```js
import '@sigilora/fonts/riftbound.css'
```

```css
.sigilora-riftbound {
  font-family: 'Sigilora Riftbound', serif;
}
```

匹配的游戏文本会通过标准 `liga` 特性自动转换为彩色符号——例如 Magic 中的 `{W}{U}{B}{R}{G}`、Lorcana 中的 `{S}{W}{L}{I}`，或符文战场中的 `[R][M]`。

## 支持的游戏

- **万智牌（Magic: The Gathering）** —— 导入 `@sigilora/fonts/magic.css`，字体族 `Sigilora Magic`。符号如 `{W}`、`{U}`、`{B}`、`{R}`、`{G}`、`{T}`、`[+1]`……
- **洛卡纳（Lorcana）** —— 导入 `@sigilora/fonts/lorcana.css`，字体族 `Sigilora Lorcana`。符号如 `{S}`、`{W}`、`{L}`、`{M}`、`{I}`、`{C}`、`{E}`……
- **符文战场（Riftbound）** —— 导入 `@sigilora/fonts/riftbound.css`，字体族 `Sigilora Riftbound`。符号如 `[E]`、`[M]`、`[R]`、`[A]`、`[2]`……

## 字体族

每个游戏提供两个字体族：

- **Sigilora <Game>** —— 全量字体。Magic 另有阴影与扁平样式，用 `font-feature-settings: 'ss01'`（阴影）或 `'ss02'`（扁平）切换；符文战场另有反色样式，用 `'ss01'` 切换。
- **Sigilora <Game> Lite** —— 仅默认样式，体积更小。

> 另见：[npm 包](/docs/guide/install-npm) · [桌面安装](/docs/guide/install-desktop) · [已知限制](/docs/guide/known-limitations)
