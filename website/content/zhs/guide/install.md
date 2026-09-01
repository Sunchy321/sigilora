---
title: 安装
description: 如何在 Web 项目中使用 Sigilora 字体。
---

# 安装

Sigilora 字体通过 npm 包 `@sigilora/fonts` 分发。

## 快速开始

安装包：

```bash
npm install @sigilora/fonts
```

导入对应游戏的 CSS：

```js
import '@sigilora/fonts/magic.css'
```

然后应用字体族：

```css
.sigilora-magic {
  font-family: 'Sigilora Magic', serif;
}
```

`{W}{U}{B}{R}{G}` 之类的匹配文本会通过标准 `liga` 特性自动转换为彩色符号。

## 字体族

- **Sigilora Magic** —— 全量字体，包含全部样式。用 `font-feature-settings: 'ss01'`（阴影）或 `'ss02'`（扁平）切换样式。
- **Sigilora Magic Lite** —— 仅默认样式，体积更小。

> 另见：[npm 包](/docs/guide/install-npm) · [桌面安装](/docs/guide/install-desktop) · [已知限制](/docs/guide/known-limitations)
