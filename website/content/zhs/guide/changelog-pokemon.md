---
title: 宝可梦卡牌版本记录
description: Sigilora Pokemon（宝可梦卡牌）字体的版本历史与兼容性说明。
---

# 宝可梦卡牌

**Sigilora Pokemon** 字体的版本历史与兼容性说明。

Sigilora Pokemon 以全量 `Sigilora Pokemon`（default / orb / flat 三种样式）与精简版 `Sigilora Pokemon Lite`（仅默认样式）两个字体族发布。当前版本包含 11 个宝可梦卡牌基本能量符号，使用 COLRv1。每个能量通过标准 `liga` 特性，从能量单字母的方括号或花括号两种拼写之一转换——例如草属性为 `[G]` 与 `{G}`。字母沿用社区 EssentiarumTCG 约定（图标重建即提取自该字体）：C 无色、D 恶、F 斗、G 草、L 雷、M 钢、N 龙、P 超、R 火、W 水、Y 妖。

字体版本遵循 SemVer：**Major** 表示删除 ligature、改变既有文本映射或移除字形；**Minor** 表示新增符号或兼容别名；**Patch** 为视觉修正。

## Sigilora Pokemon 0.3.0

- 全量字体新增 COLRv0 回退 flavor：字形、ligature 与版本完全一致。不支持 COLRv1 的引擎——Safari/WebKit、原生 CoreText、Windows 10 DirectWrite、Android 13 及以下——在 Web 端通过游戏 CSS 自动获得（或安装随附的 `… V0` 桌面字体），符号正常渲染而非空白。
- 在该 v0 回退中，`orb`（`ss01`）样式改用 `flat` 样式的图形，因此无 COLRv1 的环境下光泽能量球渲染为平面圆徽。默认的文字色裸符号与 flat 盘面保持不变。
- Lite（仅默认样式）现直接以 COLRv0 构建——裸 `currentColor` 符号不需要 COLRv1——因此没有 v1/回退之分，任何引擎都能渲染。

## Sigilora Pokemon 0.2.0

- 为每个能量新增两种样式：`orb`（`ss01`，带光泽的能量球）与 `flat`（`ss02`，平面圆徽，盘面填充字体官方基色）。
- `default` 样式改为无外圆的裸能量符号、随文字颜色（`currentColor`），便于行内嵌入。default / orb / flat 共享同一能量轮廓（取自其 `[X]`/`{X}` 拼写渲染的字形）。

## Sigilora Pokemon 0.1.0

- 新增宝可梦卡牌基本能量符号集：`[G]`/`{G}` 草、`[R]`/`{R}` 火、`[W]`/`{W}` 水、`[L]`/`{L}` 雷、`[P]`/`{P}` 超、`[F]`/`{F}` 斗、`[D]`/`{D}` 恶、`[M]`/`{M}` 钢、`[Y]`/`{Y}` 妖、`[N]`/`{N}` 龙、`[C]`/`{C}` 无色。
- 每个能量同时注册方括号（`[G]`）与花括号（`{G}`）拼写，使两种既有游戏文本写法都能匹配。
- COLRv1，单一默认样式；暂不提供样式集变体。
