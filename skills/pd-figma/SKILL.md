---
name: pd-figma
description: >-
  产品设计输入、UI 设计系统和页面蓝图到 Figma 工作流，先基于 product-brief、ui-design-system、ui-flows、ui-pages、ui-screens、ui-components 生成 3 个 UI 方向并等待用户选择，再写入或整理 Figma 设计交付；不接入外部变更生命周期。Use when the user mentions $pd-figma、pd-figma、Figma设计、UI转Figma、生成Figma设计、页面蓝图转Figma、UI设计系统、把页面蓝图写到 Figma。
---

# $pd-figma — Figma 设计交付

Codex Product Delivery Skill：把产品设计输入和 UI 页面蓝图转成可评审、可交付给前端的 Figma 设计。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Product Delivery Artifact Contracts](../qwerdf-common/artifact-contracts.md) 中 `ui/ui-design-system.md`、`ui/ui-directions.md` 和 `ui/figma-handoff.md` 的模板。
3. 读取 [UI Design System Rules](../qwerdf-common/ui-design-system.md)、[UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)、[UI Patterns](../qwerdf-common/ui-patterns.md) 和 [UI Review Rules](../qwerdf-common/ui-review-rules.md)。
4. 读取输出目录中的 `product/product-brief.md`、`ui/ui-design-system.md`、`ui/ui-flows.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md`。
5. 如果用户未指定目录，默认查找 `pd-work/<name>/`。
6. 如需要调用 Product Design，先按 Product Design 的 `get-context` 规则确认设计 brief。
7. 如需要调用 Figma，必须先加载 Figma 对应技能：`figma-use`；创建或更新页面时同时遵守 `figma-generate-design`。

## 边界

- 不要求外部变更目录。
- 不修改 `.state.yaml`。
- 不写前端代码。
- 不生成技术方案、API 契约或数据库设计。
- 无目标 Figma 文件或 frame 时停止询问。
- 外部 Figma 写入前必须说明目标文件、页面和动作范围。
- 用户未选定 UI 方向前，不得写入 Figma。
- 不得新增 `product/product-brief.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md` 中不存在的产品模块、导航、资产类型、页面或业务对象。
- 设计参考只能影响视觉风格、布局密度、组件形态和微交互，不能覆盖产品事实源或带入参考产品的业务语义。
- 不能绕过 `ui/ui-design-system.md` 直接按截图或竞品生成页面；页面级差异必须写成 `Page Overrides`。

## Gate 1：生成并确认 UI 方向

1. 先读取或形成 `ui/ui-design-system.md`：明确 `MASTER` 的产品类型、信息密度、颜色、字体、间距、圆角、按钮层级、表单、表格、列表、空态、错误态、加载态、移动端布局和可访问性规则。
2. 基于 `product/product-brief.md`、`ui/ui-design-system.md` 和页面蓝图生成 `ui/ui-directions.md`。
3. 先写 `产品事实锁定`、`设计系统事实源` 和 `参考使用边界`：列出页面范围、支持的业务对象、明确不展示内容，以及参考图中不得带入的模块 / 文案 / 资产。
4. 每个方向都先写短设计计划：颜色、字体、布局、标志性元素、适用受众、页面气质和 design system 取舍。
5. 必须给出 3 个互相有明显取舍的方向：信息密度、导航结构、视觉风格、组件策略和风险不能只是换名字。
6. 每个方向都必须保持相同的产品范围；方向之间只能改变呈现方式，不能改变产品能力、页面清单或导航语义。
7. 自检每个方向是否像通用模板，是否误带入参考产品的业务模块；如果只是换色、换名或带入范围外内容，先重写再给用户。
8. 给出推荐方向和理由，但必须等待用户明确选择方向 A / B / C，或提供修订后的方向。
9. 用户没有选择时停止，不调用 Figma。

## Figma 视觉硬规则

- 字体必须来自 `ui/ui-design-system.md` 的 `MASTER` 语义层级；`MASTER` 缺少标题、正文、表格、数字、按钮或移动端字号时，先补齐设计系统或回到 `$pd-blueprint` / `$pd-figma`，不能临场随意定字号。
- 不得靠手动缩小字体来掩盖容器不够、字段过多或信息密度失控；先调整布局、列宽、换行、截断、tooltip、字段分组、摘要 / 详情层级或密度策略。
- 中文、英文、数字、金额、百分比、状态 badge 和按钮文本必须检查基线、行高和垂直对齐；同一语义层级不得混用字号、字重或行高。
- 移动端 frame 必须使用一致的侧向安全边距，默认 16px 或 `MASTER` 指定值；固定顶部 / 底部 / 浮层必须为内容预留避让空间。
- 间距必须来自 `MASTER` 的 spacing scale；不得在同一页面随机使用 7px、13px、19px 等非系统值，除非现有设计系统明确规定。
- 列表、表格、卡片、详情、记录流和数据看板必须先定义信息优先级；同类数据使用同一模板、同一对齐、同一分隔和同一格式。
- 字段过多时使用分组、摘要、详情、tooltip、展开区或二级页面；移动端表格必须降级为卡片 / 摘要 / 分组详情 / 局部横向滚动容器，不得造成页面级横向溢出。
- SaaS / CRM / 管理后台 / 操作台类产品默认保持克制、高密度、可扫描和稳定布局；不得把操作型产品做成低密度营销页。

## Gate 2：写入 Figma

写入前确认：

- 目标 Figma 文件 URL / file key / frame 已明确。
- 本次要创建或更新的页面范围已明确。
- UI 方向已选定。
- 是否已有设计系统；如有，优先复用组件、变量、样式。
- `ui/ui-design-system.md` 的 `MASTER` 已确认，且 page-level override 只包含必要差异。
- 如目标包含图片，遵守 Figma `figma-generate-design` 的截图 / imageHash 迁移规则。
- 已对照 `product/product-brief.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md` 检查选定 UI 方向，没有新增范围外页面、导航或业务模块。

写入顺序：

1. 先读取或发现现有 Figma 设计系统、Code Connect、相邻页面和可复用组件。
2. 建立或复用设计系统变量：颜色、字体、间距、圆角、阴影；同步记录到 `ui/ui-design-system.md` 的 `MASTER` 或 `Page Overrides`。
3. 建立或复用基础组件：Button、Input、Select、Tabs、Badge、Table、Card、Modal、Drawer、EmptyState、Toast。
4. 按页面逐个创建高保真页面。
5. 为关键页面创建状态页：default、loading、empty、error、permission。
6. 检查界面文案：按钮写动作结果，错误说明发生了什么和如何修复，空态引导用户下一步。
7. 每个 section 或页面完成后用 Figma 截图验证，修复明显错位、裁切、重叠、占位文案，并检查是否误引入参考产品的导航 / tab / 业务文案。
8. 对同一页面族、组件族、响应式断点和相似 frame 做同类问题扫描；用户指出的问题不能只修一个 frame。
9. 写入 `ui/figma-handoff.md`，记录 Figma URL、frames、产品范围校验、设计系统、page-level override、状态页、截图 QA、同类问题扫描和前端注意事项。

## Gate 3：交付前截图级视觉 QA

写入或修改 Figma 后，必须执行截图级视觉 QA；不能只靠文字检查或图层描述声称“已修复”。

1. 获取本次创建或修改的每个目标 frame 截图；如果同一页面有桌面 / 平板 / 移动端断点，每个断点都要截图。
2. 对照 `ui/ui-design-system.md`、`ui-quality-checklist.md` 和 `ui-review-rules.md` 检查低级视觉问题零容忍项：
   - 遮挡、重叠、文本或容器溢出。
   - 移动端安全边距不足、页面级横向溢出、固定栏遮挡关键内容。
   - 同语义字体层级不一致，或用缩小字体替代合理布局。
   - 圆角、阴影、边框、按钮、卡片 padding、表格密度随机漂移。
   - 行高 / 卡片高度随机，tabs、筛选、标题、列表内容和操作区明显错位。
   - 主次操作不清，default / loading / empty / error / permission 状态不一致。
   - 用 emoji 当结构性图标，或把操作型产品做成低密度营销页。
3. 对用户指出的问题，先复述问题类别，再定位影响范围：同页面、同组件、同断点、相似列表 / 表格 / 卡片 / 表单都要检查。
4. 发现问题时必须继续修复并重新截图，直到截图 QA 通过；无法修复时在 `ui/figma-handoff.md` 写明待人工确认项、原因、影响和下一步归属。
5. 输出摘要必须列出已检查 frame、视口 / 断点、截图证据、零容忍检查结果、同类问题扫描范围和待人工确认项。

## 输出摘要

```text
Figma 设计完成: <name>
目录: <output-dir>
文件:
  - ui/ui-design-system.md
  - ui/ui-directions.md
  - ui/figma-handoff.md
Figma: <url 或 待配置 / 待授权 / 失败原因>
验证:
  - 截图级视觉 QA: <已检查 frames / 视口 / 证据>
  - 低级视觉问题零容忍: <通过 / 待修复>
  - 同类问题扫描: <范围 / 结果>
  - 待人工确认: <无 / 列表>

下一步: 先用 $pd-ui-review <name> 做独立 UI 质量审查；P0/P1 清零后再用 $pd-plan 生成前后端技术设计
```
