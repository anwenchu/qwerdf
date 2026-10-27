---
name: pd-figma
description: >-
  产品设计输入、UI 设计系统和页面蓝图到 Figma 工作流，在 Figma 中展示候选 UI 方向供比较，选定后深化并交付；已有明确方向时沿用，不强制重选；不接入外部变更生命周期。Use when the user mentions $pd-figma、pd-figma、Figma设计、UI转Figma、生成Figma设计、页面蓝图转Figma、UI设计系统、把页面蓝图写到 Figma。
---

# $pd-figma — Figma 设计交付

Codex Product Delivery Skill：把产品设计输入和 UI 页面蓝图转成可评审、可交付给前端的 Figma 设计。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Product Delivery Artifact Contracts](../qwerdf-common/artifact-contracts.md) 中 `ui/ui-design-system.md`、`ui/ui-directions.md` 和 `ui/figma-handoff.md` 的模板。
3. 读取 [UI Design System Rules](../qwerdf-common/ui-design-system.md)、[UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)、[UI Patterns](../qwerdf-common/ui-patterns.md) 和 [UI Review Rules](../qwerdf-common/ui-review-rules.md)。
4. 读取输出目录中的 `product/product-brief.md`、`ui/ui-design-system.md`、`ui/ui-flows.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md`；如已有 `ui/ui-directions.md` / `ui/figma-handoff.md`，复用其中的有效候选、已定方向及文件 / frame 链接，续作只补未完成部分。
5. 如果用户未指定目录，默认查找 `pd-work/<name>/`。
6. 如需要调用 Product Design，先按 Product Design 的 `get-context` 规则确认设计 brief。
7. 如需要调用 Figma，必须先加载 Figma 对应技能：`figma-use`；创建或更新页面时同时遵守 `figma-generate-design`；用户要求或授权新建文件时加载 `figma-create-new-file`。

## 边界

- 不要求外部变更目录。
- 不修改 `.state.yaml`。
- 不写前端代码。
- 不生成技术方案、API 契约或数据库设计。
- 开始时从用户输入、当前会话和已有产物定位目标 Figma 文件及页面；缺失时尽早询问目标或是否新建，不到概念板做完才告知。用户已授权新建时按对应 Figma 技能执行；仅要求本地预览时不追问写入目标。
- 外部 Figma 写入前必须说明目标文件、页面和动作范围。
- 候选预览与正式深化的边界统一按下方 Gate 1 执行；方向未选定不阻断候选写入。
- 不得新增 `product/product-brief.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md` 中不存在的产品模块、导航、资产类型、页面或业务对象。
- 设计参考只能影响视觉风格、布局密度、组件形态和微交互，不能覆盖产品事实源或带入参考产品的业务语义。
- 不能绕过 `ui/ui-design-system.md` 直接按截图或竞品生成页面；页面级差异必须写成 `Page Overrides`。

## Gate 1：在 Figma 比较并选择 UI 方向

1. 先读取或形成 `ui/ui-design-system.md`：明确 `MASTER` 的产品类型、信息密度、颜色、字体、间距、圆角、按钮层级、表单、表格、列表、空态、错误态、加载态、移动端布局和可访问性规则。
2. 先判断是否需要探索方向。用户已选定、已委托你选定、要求沿用现有设计，或只修改局部页面时，记录依据后直接进入相应深化 / 修改，不强制重做三套。需要比较方向时，基于产品设计输入、设计系统和页面蓝图复用或补齐 `ui/ui-directions.md`，不重做已有效的本地候选。
3. 先写 `产品事实锁定`、`设计系统事实源` 和 `参考使用边界`：列出页面范围、支持的业务对象、明确不展示内容，以及参考图中不得带入的模块 / 文案 / 资产。
4. 每个方向都先写短设计计划：颜色、字体、布局、标志性元素、适用受众、页面气质和 design system 取舍。
5. 需要探索时默认给出 3 个有明显取舍的方向；数量和范围遵循用户要求。信息密度、导航结构、视觉风格、组件策略和风险不能只是换名字。
6. 每个方向都必须保持相同的产品范围；方向之间只能改变呈现方式，不能改变产品能力、页面清单或导航语义。
7. 自检每个方向是否像通用模板，是否误带入参考产品的业务模块；如果只是换色、换名或带入范围外内容，先重写再给用户。
8. 用户要求 Figma 设计或在 Figma 中比较、且目标与写入范围已明确时，先把候选的代表性页面写到独立探索页 / frames，标明“候选，待选择”，再请用户比较；不因尚未选择而只交本地概念板。优先使用可编辑 frame；使用概念板图片时说明它是图片预览，不能冒充可编辑 UI。用户明确要求仅本地预览、暂不写入或选定后再写时，遵循该要求。
9. 候选共用产品事实锁和已确认设计约束，待定风格仅记录为提案，不覆盖正式页面、已确认的 MASTER 或发布组件。按 Gate 2 的适用步骤写入并执行 Gate 3 截图 QA；在 `ui/ui-directions.md` 记录文件 / frame 链接、预览类型与实际写入状态。目标、权限或工具缺失时明确记为未写入 / 写入失败，不把本地文件称为 Figma 交付。
10. 候选可查看后给出推荐及理由，等待用户选择或修订（已有选择或委托选定的授权则沿用），再深化选定方向并生成正式 handoff。候选预览不等于正式定稿；尚待选择时下一步是方向评审，不进入 `$pd-plan`。

## Figma 视觉硬规则

按本次页面、组件与平台选取适用约束；尺寸与批准 variant 来自 MASTER / Page Overrides。严重性、例外和交接条件统一遵循 [UI Review Rules](../qwerdf-common/ui-review-rules.md)，不把默认像素值或内容自适应高度当成阻断。

- 字体必须来自 `ui/ui-design-system.md` 的 `MASTER` 语义层级；`MASTER` 缺少标题、正文、表格、数字、按钮或移动端字号时，先补齐设计系统或回到 `$pd-blueprint` / `$pd-figma`，不能临场随意定字号。
- 不得靠手动缩小字体来掩盖容器不够、字段过多或信息密度失控；先调整布局、列宽、换行、截断、tooltip、字段分组、摘要 / 详情层级或密度策略。
- 中文、英文、数字、金额、百分比、状态 badge 和按钮文本必须检查基线、行高和垂直对齐；同一语义层级不得混用字号、字重或行高。
- 移动端 frame 遵循 `MASTER` 的安全边距和平台安全区规则；固定顶部 / 底部 / 浮层必须为内容预留避让空间。
- 间距来自 `MASTER` 的 spacing scale；不为修复单处任意使用非系统值，必要差异记录理由与影响范围。
- 列表、表格、卡片、详情、记录流和数据看板必须先定义信息优先级；同类数据使用同一模板、同一对齐、同一分隔和同一格式。
- 字段过多时使用分组、摘要、详情、tooltip、展开区或二级页面；移动表格统一按 [共享布局规则](../qwerdf-common/ui-quality-checklist.md#2-布局间距与内容边界) 选择，不另列强制转换策略。
- SaaS / CRM / 管理后台 / 操作台类产品默认保持克制、高密度、可扫描和稳定布局；不得把操作型产品做成低密度营销页。

## Gate 2：写入 Figma

写入前确认：

- 目标 Figma 文件 URL / file key / frame 已明确。
- 本次要创建或更新的页面范围已明确。
- 本轮是候选探索还是选定方向的深化 / 修改；正式深化时方向已有明确依据，候选探索遵循 Gate 1。
- 是否已有设计系统；如有，优先复用组件、变量、样式。
- 已读取 `ui/ui-design-system.md` 的 `MASTER`；正式深化先确认受影响设计约束，page-level override 只包含必要差异，候选提案不改写已确认规则。
- 如目标包含图片，遵守 Figma `figma-generate-design` 的截图 / imageHash 迁移规则。
- 已对照 `product/product-brief.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md` 检查本轮候选或选定方向，没有新增范围外页面、导航或业务模块。

写入顺序：

1. 先读取或发现现有 Figma 设计系统、Code Connect、相邻页面和可复用组件。
2. 复用已有设计系统变量；正式深化时才确认新增颜色、字体、间距、圆角、阴影并记录到 `MASTER` 或 `Page Overrides`。候选差异只作用于探索 frames，记录于方向提案。
3. 建立或复用本次需要的基础组件：Button、Input、Select、Tabs、Badge、Table、Card、Modal、Drawer、EmptyState、Toast；候选不发布为正式组件。
4. 按本轮范围创建候选预览或选定方向的高保真页面，保留已有正式设计。
5. 覆盖关键页面适用的 default、loading、empty、error、permission 等状态；共用组件可集中展示状态并由页面引用，静态公开页不强制创造异步或权限状态。
6. 检查界面文案：按钮写动作结果；错误恢复与空态说明按 [共享质量清单](../qwerdf-common/ui-quality-checklist.md#4-适用的状态与交互) 判断，不为文案补造业务动作。
7. 每个 section 或页面完成后用 Figma 截图验证，修复明显错位、裁切、重叠、占位文案，并检查是否误引入参考产品的导航 / tab / 业务文案。
8. 对同一页面族、组件族、响应式断点和相似 frame 做同类问题扫描；用户指出的问题不能只修一个 frame。
9. 候选阶段更新 `ui/ui-directions.md` 的实际写入及 QA 结果；正式交付时更新 `ui/figma-handoff.md`，记录 Figma URL、frames、产品范围校验、设计系统、page-level override、状态页、截图 QA、同类问题扫描和前端注意事项。

## Gate 3：交付前截图级视觉 QA

写入或修改 Figma 后，必须执行截图级视觉 QA；不能只靠文字检查或图层描述声称“已修复”。

1. 获取本次创建或修改的每个目标 frame 截图；如果同一页面有桌面 / 平板 / 移动端断点，每个断点都要截图。
2. 对照 `ui/ui-design-system.md` 和 `ui-quality-checklist.md` 检查适用的可读性、操作、状态、布局与一致性；按 `ui-review-rules.md` 判断影响和严重性，不另维护零容忍缺陷清单。
3. 对用户指出的问题，先复述问题类别，再定位影响范围：同页面、同组件、同断点、相似列表 / 表格 / 卡片 / 表单都要检查。
4. P0/P1 修复后重新截图；必要证据缺失时记录待确认，不以自述代替验证。P2/P3 可记录 owner、验证方式、复查入口后继续，不要求无限返工到所有建议清零。
5. 输出摘要列出已检查 frame、视口 / 断点、截图证据、阻断与残余风险、同类问题扫描范围和待确认项。

## 输出摘要

```text
Figma 设计进度: <name；候选预览 / 选定方向深化 / 正式交付 / 阻断>
目录: <output-dir>
文件:
  - ui/ui-design-system.md
  - ui/ui-directions.md
  - ui/figma-handoff.md（正式交付时）
Figma: <url 或 待配置 / 待授权 / 失败原因>
实际写入: <文件 / frame 链接及可编辑或图片预览；未写入时说明原因>
验证:
  - 截图级视觉 QA: <已检查 frames / 视口 / 证据>
  - 阻断与残余风险: <无 P0/P1 / 待修复 / 证据缺口；P2/P3>
  - 同类问题扫描: <范围 / 结果>
  - 待人工确认: <无 / 列表>

下一步: <候选阶段请用户选方向；正式交付后用 $pd-ui-review，必要证据充分且无未解决 P0/P1 后再进入 $pd-plan>
```
