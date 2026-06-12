---
name: pd-blueprint
description: >-
   PRD 到产品设计输入和 UI 页面蓝图工作流，把 PRD、竞品 URL、截图、产品想法或已有 spec 拆成 product-brief、用户流程、页面地图、页面规格和组件清单；不接入外部变更生命周期。Use when the user mentions $pd-blueprint、pd-blueprint、产品蓝图、产品设计输入、PRD转UI、页面蓝图、UI蓝图、从 PRD 生成页面设计输入、从竞品参考整理页面结构。
---

# $pd-blueprint — 产品设计输入与页面蓝图

Codex Product Delivery Skill：把 PRD、竞品参考或产品想法转成可进入 UI 方向探索、Figma 设计和前端实现的设计输入。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Product Delivery Artifact Contracts](../qwerdf-common/artifact-contracts.md) 中 `product-brief.md`、`ui-flows.md`、`ui-pages.md`、`ui-screens.md`、`ui-components.md` 的模板。
3. 优先读取输出目录中的 `prd.md`、`requirements.md`、`user-stories.md`、`acceptance-criteria.md`、`open-questions.md`。
4. 读取用户提供的 PRD、竞品 URL、截图、产品说明、设计偏好或已有 spec。
5. 如果用户未指定输出目录，使用 `pd-work/<name>/`。

## 边界

- 不要求先执行外部探索或变更初始化流程。
- 不创建外部变更目录。
- 不修改 `.state.yaml`。
- 不进 Figma。
- 不写代码。
- 不生成技术方案。
- 竞品只提炼交互模式、信息架构和体验取舍，不照抄视觉、文案或受保护资产。
- 竞品或截图中的业务模块、导航标签、资产类型、活动入口、copy trading、品牌术语等，只有在 PRD / requirements / 用户明确说明中出现时才能进入产品范围。

## 蓝图质量规则

- 每个页面先写清楚主体、目标用户和页面唯一任务，再写页面结构。
- 页面结构必须服务业务信息，不用无意义编号、装饰性分区或模板化 dashboard 区块。
- 文案按用户能识别的动作命名，不用系统实现术语替代用户语言。
- `empty` 和 `error` 状态必须给出下一步动作，不能只是情绪化提示。
- 竞品模式要写取舍：为什么适合本产品、哪些前提不适用、哪些地方不能照搬。
- 先写产品事实锁，再写参考拆解；页面、导航、组件和状态必须从产品事实锁推导，不能从参考图直接搬运。
- 参考材料只能贡献视觉密度、布局节奏、信息分组、反馈方式、交互动效等抽象模式；不能贡献产品能力、交易品类、tab 名称、品牌文案或业务对象。
- 如果参考图与 PRD / product-brief 冲突，把冲突项写入 `参考使用边界` 或 `不应照搬`，不要写进 `ui-pages.md`、`ui-screens.md` 或 `ui-components.md`。

## 流程

1. 判断输入是否足够生成产品设计输入；缺少目标用户、核心场景、MVP 范围或关键约束时，先列出缺口并提问，不写半成品文件。
2. 从 PRD、requirements、用户说明和已有 spec 中抽取产品事实锁：产品名称、目标用户、核心场景、支持的业务对象、MVP 范围、非目标范围。
3. 对竞品、截图或设计参考做参考拆解：只保留可借鉴的视觉 / 交互模式；把产品范围外的模块、导航、资产、文案、品牌和业务前提列为不得带入。
4. 先生成 `product-brief.md`，明确产品事实源、产品目标、目标用户、核心场景、MVP 范围、成功指标、约束、竞品模式、参考使用边界、风险和开放问题。
5. 基于 `product-brief.md` 生成 UI 页面蓝图：
   - `ui-flows.md`
   - `ui-pages.md`
   - `ui-screens.md`
   - `ui-components.md`
6. 每个页面必须覆盖 `default`、`loading`、`empty`、`error`、`permission` 状态。
7. 输出摘要必须列出产物目录、已写文件、仍需用户确认的问题，并提示下一步使用 `$pd-figma`。

## 输出摘要

```text
产品设计输入与 UI 页面蓝图完成: <name>
目录: <output-dir>
文件:
  - product-brief.md
  - ui-flows.md
  - ui-pages.md
  - ui-screens.md
  - ui-components.md
待确认:
  - <如无则写“无”>

下一步: 用 $pd-figma <name> 基于产品设计输入和页面蓝图选择 UI 方向并生成 Figma 设计
```
