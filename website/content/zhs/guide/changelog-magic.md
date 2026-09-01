---
title: Magic 版本记录
description: Sigilora Magic 字体的版本历史与兼容性说明。
---

# 万智牌（Magic: The Gathering）

**Sigilora Magic** 字体的版本历史与兼容性说明。

Sigilora Magic 以全量字体族 `Sigilora Magic`（默认、阴影、扁平三种样式，通过 `ss01` / `ss02` 切换）和 Lite 字体族 `Sigilora Magic Lite`（仅默认样式）发布。当前版本覆盖 114 个符号——法术力、混血、非瑞、其他、特殊与忠诚计数器——采用 COLRv0。

字体版本遵循 SemVer：**Major** 表示删除 ligature、改变既有文本映射或移除字形；**Minor** 表示新增符号或兼容别名；**Patch** 为视觉修正。

## 已知问题

- 在 WebKit 浏览器（macOS 与 iOS 的 Safari）中，输入包含 ASCII 连字符后跟字母的 ligature——`[-X]` 与 `[-N]`——不会渲染，这是 WebKit 的文本整形行为。Chrome 与 Firefox 不受影响。详见[已知限制](/docs/guide/known-limitations)。

## Sigilora Magic 1.2.1

- 扁平模式的前景色跟随文字颜色：数字法术力符号（含 `{X}`/`{Y}`/`{Z}`）、横置符号、混血法术力的外框及其数字半、雪境的外框。

## Sigilora Magic 1.2.0

- 暗色模式支持。

## Sigilora Magic 1.1.0

- 增加 `{½}` ligature。
- 支持 `[+N]` / `[-N]` 忠诚计数器渲染。

## Sigilora Magic 1.0.1

- 调整扁平 `{W}` 配色。

## Sigilora Magic 1.0.0

- 增加忠诚计数器符号。

## Sigilora Magic 0.6.0

- 为 `{S}` 增加扁平样式。

## Sigilora Magic 0.5.0

- 补全扁平符号样式。

## Sigilora Magic 0.4.1

- 修复阴影渲染。

## Sigilora Magic 0.4.0

- 增加阴影样式图标。

## Sigilora Magic 0.3.0

- 补全图标集。

## Sigilora Magic 0.2.0

- 支持一个符号多个 ligature。

## Sigilora Magic 0.1.0

- 创建 Magic 符号字体。
