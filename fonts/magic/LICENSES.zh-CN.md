# LICENSES — Magic: The Gathering

此文件记录 `fonts/magic/` 的素材来源与许可依据。

## 1. 基础符号 SVG（default 样式）

- 位置：`fonts/magic/raw/default/`（84 个符号）
- 来源：Scryfall（`https://svgs.scryfall.io/card-symbols/...`）
- 许可：这些图形是 Wizards of the Coast（WotC）卡牌符号的图形表达，受 WotC Fan Content Policy 约束。Scryfall 与 WotC 均未授予将图形转为字形、随字体二进制分发或再授权（如 OFL）的权利。

## 2. 样式变体（叠加在基础符号上的原创工作）

- 位置：构建时从 `fonts/magic/raw/default/` 与 `fonts/magic/raw/components/` 生成；特殊例外以文件形式保留在 `fonts/magic/raw/static/`
- 来源：本项目作者的原创工作，叠加在基础 Scryfall SVG 之上。原始 Scryfall 文件不含阴影；阴影样式、平铺配色，以及 `100`、`1000000`、`half-white`、`half-red` 的特殊阴影和 snow 的平铺样式均为作者自行添加。
- 许可：叠加的图层为原创工作；其下的基础字形仍属 WotC/Scryfall 知识产权。

## 3. 合成零件（components）

- 位置：`fonts/magic/raw/components/`（19 个零件）
- 来源：不属于 Scryfall 卡牌符号集；为项目自行拆分的零件，用于合成混血、非瑞、忠诚计数器等符号。
- 许可：原创构建块，与 Scryfall 基础字形混用。

## 4. Plantin-Bold 字体（外部依赖，不入库）

- 用途：`compose.loyalty` 将忠诚计数器文本（"+1" 等）转为路径时使用的字体。
- 位置：`fonts/magic/external/Plantin-Bold.ttf`——不入库，需自行提供（见 `external/README.md`）。
- 许可：Monotype 的商业字体。其二进制不入库、不随字体或包分发。最终字体中嵌入的是由它渲染出的字形轮廓路径。
