---
name: pd-figma
description: >-
  个人产品设计输入和 UI 页面蓝图到 Figma 工作流，先基于 product-brief、ui-flows、ui-pages、ui-screens、ui-components 生成 3 个 UI 方向并等待用户选择，再写入或整理 Figma 设计交付；不接入外部变更生命周期。Use when the user mentions $pd-figma、pd-figma、Figma设计、UI转Figma、生成Figma设计、页面蓝图转Figma、把页面蓝图写到 Figma。
---

# $pd-figma — Figma 设计交付

个人辅助 Skill：把产品设计输入和 UI 页面蓝图转成可评审、可交付给前端的 Figma 设计。

## 读取

1. 读取 [个人 Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Product Delivery Artifact Contracts](../qwerdf-common/artifact-contracts.md) 中 `ui-directions.md` 和 `figma-handoff.md` 的模板。
3. 读取输出目录中的 `product-brief.md`、`ui-flows.md`、`ui-pages.md`、`ui-screens.md`、`ui-components.md`。
4. 如果用户未指定目录，默认查找 `pd-work/<name>/`。
5. 如需要调用 Product Design，先按 Product Design 的 `get-context` 规则确认设计 brief。
6. 如需要调用 Figma，必须先加载 Figma 对应技能：`figma-use`；创建或更新页面时同时遵守 `figma-generate-design`。

## 边界

- 不要求外部变更目录。
- 不修改 `.state.yaml`。
- 不写前端代码。
- 不生成技术方案、API 契约或数据库设计。
- 无目标 Figma 文件或 frame 时停止询问。
- 外部 Figma 写入前必须说明目标文件、页面和动作范围。
- 用户未选定 UI 方向前，不得写入 Figma。

## Gate 1：生成并确认 UI 方向

1. 基于 `product-brief.md` 和页面蓝图生成 `ui-directions.md`。
2. 每个方向都先写短设计计划：颜色、字体、布局、标志性元素、适用受众和页面气质。
3. 必须给出 3 个互相有明显取舍的方向：信息密度、导航结构、视觉风格、组件策略和风险不能只是换名字。
4. 自检每个方向是否像通用模板；如果只是换色或换名，先重写再给用户。
5. 给出推荐方向和理由，但必须等待用户明确选择方向 A / B / C，或提供修订后的方向。
6. 用户没有选择时停止，不调用 Figma。

## Gate 2：写入 Figma

写入前确认：

- 目标 Figma 文件 URL / file key / frame 已明确。
- 本次要创建或更新的页面范围已明确。
- UI 方向已选定。
- 是否已有设计系统；如有，优先复用组件、变量、样式。
- 如目标包含图片，遵守 Figma `figma-generate-design` 的截图 / imageHash 迁移规则。

写入顺序：

1. 先读取或发现现有 Figma 设计系统、Code Connect、相邻页面和可复用组件。
2. 建立或复用设计系统变量：颜色、字体、间距、圆角、阴影。
3. 建立或复用基础组件：Button、Input、Select、Tabs、Badge、Table、Card、Modal、Drawer、EmptyState、Toast。
4. 按页面逐个创建高保真页面。
5. 为关键页面创建状态页：default、loading、empty、error、permission。
6. 检查界面文案：按钮写动作结果，错误说明发生了什么和如何修复，空态引导用户下一步。
7. 每个 section 或页面完成后用 Figma 截图验证，修复明显错位、裁切、重叠、占位文案。
8. 写入 `figma-handoff.md`，记录 Figma URL、frames、设计系统、状态页、截图 QA 和前端注意事项。

## 输出摘要

```text
Figma 设计完成: <name>
目录: <output-dir>
文件:
  - ui-directions.md
  - figma-handoff.md
Figma: <url 或 待配置 / 待授权 / 失败原因>
验证:
  - <截图检查 / 待人工确认>

下一步: 用 $pd-plan <name> 基于 PRD、页面蓝图和 Figma handoff 生成前后端技术设计
```
