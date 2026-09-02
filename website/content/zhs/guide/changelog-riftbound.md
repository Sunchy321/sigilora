---
title: 符文战场版本记录
description: Sigilora Riftbound（符文战场）字体的版本历史与兼容性说明。
---

# 符文战场

**Sigilora Riftbound** 字体的版本历史与兼容性说明。

Sigilora Riftbound 以 `Sigilora Riftbound`（默认样式）与精简版 `Sigilora Riftbound Lite` 两个字体族发布。当前版本包含 22 个符号——休眠、might、六个域符文、任意与数字 0–12——使用 COLRv1（任意的彩虹使用渐变）。反色（单色白）样式通过 `ss01` 特性切换。

字体版本遵循 SemVer：**Major** 表示删除 ligature、改变既有文本映射或移除字形；**Minor** 表示新增符号或兼容别名；**Patch** 为视觉修正。

## Sigilora Riftbound 0.3.0

- 新增字体的 COLRv0 回退 flavor：字形、ligature 与版本完全一致。不支持 COLRv1 的引擎——Safari/WebKit、原生 CoreText、Windows 10 DirectWrite、Android 13 及以下——在 Web 端通过游戏 CSS 自动获得该 flavor（或安装随附的 `… V0` 桌面字体），符号正常渲染而非空白。
- v0 flavor 中，唯一需要 COLRv1 的字形 `[A]` 任意的彩虹渐变改用专门的 `currentColor`（文字色）图形；其余字形——域符文、数字与反色样式——本就是平涂或单色，保持不变。

## Sigilora Riftbound 0.2.0

- 新增 Riftbound 符号集：`[E]` 休眠、`[M]` 🧍、域符文 `[R]` `[G]` `[B]` `[O]` `[P]` `[Y]`、`[A]` 任意、数字 `[0]`–`[12]`。
- 符文为无外圆的裸域色图形；`[A]` 彩虹使用 COLRv1 渐变。
- COLRv1，反色（单色白）样式通过 `ss01` 切换。
