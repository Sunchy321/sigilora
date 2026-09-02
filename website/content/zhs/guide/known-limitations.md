---
title: 已知限制
description: 使用 Sigilora 字体时需要注意的浏览器相关行为。
---

# 已知限制

Sigilora 通过标准 OpenType `liga` 特性将 `[-X]` 之类的文本转换为彩色符号。大多数浏览器都能可靠地应用这些 ligature。颜色渲染取决于每个游戏的 COLR 版本，因此有两个浏览器相关行为值得注意：一个与颜色有关，一个与整形有关。

## COLRv1 支持与 Safari

Sigilora 字体以 COLR 存储彩色字形（v0 或 v1，视游戏而定）。COLRv0 被所有主流引擎支持，包括 Safari/WebKit 与 Apple 原生文本栈。COLRv1 被 Chromium 与 Firefox 支持，但 Safari/WebKit 不支持——WebKit 从未实现 COLRv1。

因此，使用 COLRv1 的游戏——宝可梦卡牌与符文战场的全量字体族，以及符文战场 Lite——还会附带一份同规格的 COLRv0 回退 flavor：字形、ligature 与字体版本完全一致，颜色以平涂填充与 `currentColor` 编码。游戏 CSS 会自动分流：在不支持 COLRv1 的引擎上得到 v0 flavor，支持 COLRv1 的引擎则得到完整 v1 flavor。无需任何配置。

宝可梦卡牌 Lite 是例外：它只含裸 `currentColor` 默认样式，不需要 COLRv1，因此直接以单个 COLRv0 字体构建，无需回退。

在 v0 flavor 中，需要 COLRv1 的效果按设计降级：

- 宝可梦 `orb`（`ss01`，光泽能量球）改用 `flat` 样式的图形，因此渲染为平面圆徽。默认的文字色裸符号与 flat 盘面不受影响。
- 符文战场 `[A]` 任意的彩虹渲染为单色文字色（`currentColor`）符文。域符文、数字与反色样式不受影响。

结果：在 Safari 及其他仅 v0 的环境——例如经 CoreText 渲染文本的原生 Apple 应用——光泽能量球与符文战场彩虹以对应的平涂/文字色形式呈现，而非空白。

## 连字符后跟字母的 ligature（WebKit）

在基于 WebKit 的浏览器中——macOS 与 iOS 的 Safari——输入序列包含 ASCII 连字符（`-`，U+002D）且**其后紧跟字母**的 `liga` 连字不会被应用。WebKit 会在该位置切开 shaping run，导致连字无法形成，相关文本渲染为空白。

对当前 Magic 字体而言，受影响的恰好是两个符号：`X` 和 `N` 的负忠诚计数器：

- `[-X]` 与 `[-N]` 在 Safari 中不渲染
- 其余负忠诚计数器（`[-1]` … `[-25]`）与正计数器（`[+X]`、`[+N]`、`[+1]` …）均正常
- Chrome 与 Firefox 能正确应用这些连字

这是 WebKit 的文本整形行为，不是字体缺陷。字体数据、ligature 映射与形状均有效；相同的字形在 HarfBuzz 与 CoreText 下都能正确整形。

目前尚未提供替代渲染。未来字体更新可以将替代减号字符——Unicode 减号（`−`，U+2212）或不间断连字符（`‑`，U+2011）——映射到同一输入字形，因为它们不会触发 WebKit 的这一行为，但当前字体并未映射这些字符。在此之前，`[-X]` 与 `[-N]` 只会在能正确应用连字的浏览器（Chrome、Firefox）中渲染。
