---
name: pd-ui-review
description: >-
  独立 UI 设计质量审查工作流，基于 PRD、product-brief、ui-design-system、Figma handoff、Figma URL、页面截图、本地页面 URL 或 frontend-acceptance 审查设计稿和前端视觉表现，输出 ui/ui-review-report.md 与 P0/P1/P2/P3 findings；默认只审查，不改设计稿、不改代码、不提交。Use when the user mentions $pd-ui-review、pd-ui-review、UI review、设计稿 review、Figma review、视觉审查、页面看起来不对、样式不统一、字体不统一、遮挡、重叠、突兀、不整齐、对齐问题、间距问题、移动端溢出、截图审查。
---

# $pd-ui-review — UI 设计质量审查

Codex Product Delivery Skill：专门审查设计稿、Figma handoff、页面截图和前端 UI 展示质量，输出可执行的视觉 / 交互 findings。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Product Delivery Artifact Contracts](../qwerdf-common/artifact-contracts.md) 中 `ui/ui-review-report.md` 的模板。
3. 读取 [UI Design System Rules](../qwerdf-common/ui-design-system.md)、[UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)、[UI Patterns](../qwerdf-common/ui-patterns.md) 和 [UI Review Rules](../qwerdf-common/ui-review-rules.md)。
4. 读取当前项目的 `product/product-brief.md`、`product/prd.md`、`ui/ui-design-system.md`、`ui/ui-flows.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md`、`ui/ui-directions.md`、`ui/figma-handoff.md`；缺失时记录证据缺口。
5. 如审查前端实现，读取 `tech/frontend/frontend-design.md`、`tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-acceptance.md` 和相关截图 / 浏览器证据。
6. 如用户提供 Figma URL，按 Figma skill 规则读取 Figma context / screenshot；如提供本地页面 URL，允许用浏览器截图或 Playwright 证据审查；如只提供截图，基于截图、产品事实源和设计系统审查，证据不足处标记“待确认”。
7. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 渐进式 references

- 审查任何 UI 视觉问题时读取 [Visual Defects](references/visual-defects.md)。
- 审查 Figma URL、frame、design system 或 handoff 时读取 [Figma Review](references/figma-review.md)。
- 审查截图、本地页面 URL、响应式或浏览器证据时读取 [Screenshot Review](references/screenshot-review.md)。

## 边界

- 默认只审查，不修改设计稿、不改代码、不提交。
- 不替代 `$pd-review` 的代码级 Code Review；`$pd-review` 可读取 `ui/ui-review-report.md` 作为 UI 证据。
- 不把截图或参考图当产品事实源；页面、导航、业务模块和关键文案必须来自 PRD、product-brief、UI 蓝图或用户明确确认。
- 不越权修改 `ui/ui-design-system.md`、Figma handoff、PRD 或技术方案；发现事实源问题时把归属指向 `$pd-blueprint`、`$pd-figma` 或 `$pd-plan`。
- 不使用“丑”“不高级”“不美观”作为 finding；必须指出页面 / frame / 区域、具体问题、影响、建议、证据和归属。
- 没有视觉证据时，只审查文档完整性、设计系统一致性和验收证据缺口；不得臆测具体遮挡、重叠或溢出。
- 不进入 `$pd-git`，不作为提交放行结论。

## 审查维度

1. 产品与设计系统一致性：`MASTER`、Page Overrides、产品范围、页面模式、信息密度和管理后台 / SaaS / CRM 的克制高密度方向。
2. 基础视觉质量：风格、字体族、字号、字重、行高、颜色 token、圆角、阴影、边框、分割线、icon 风格和结构性图标。
3. 遮挡、重叠和布局破损：fixed header / footer / side nav、modal / drawer / popover / toast、z-index、文本溢出、移动端挤压和横向滚动。
4. 信息层级和突兀感：主操作、标题 / 说明 / 表单 / 表格层级、过大标题、过亮颜色、过重阴影、过多装饰和后台系统营销化。
5. 交互状态：hover、active、focus、disabled、loading、success、error、destructive action、icon-only label / tooltip。
6. 响应式和移动端：按 375px、768px、1024px、1440px 思考或验证；移动端不得横向溢出，固定底部按钮 / toast 不得遮挡关键操作。
7. 可访问性：对比度、非颜色唯一表达、label、键盘焦点、aria label、heading 层级和 reduced motion。
8. 产品类型适配：数据密集页、表单页、列表 / 表格页、卡片页、详情页、导航和移动端 frame 必须按对应模式审查，不用一套营销页审美覆盖所有产品。

## 不能交付条件

出现以下任一情况时，结论必须写为“不能进入下一阶段”或“证据不足，不能放行”，不得只写“已修复”：

- 关键 Figma frame、用户截图或本地页面 URL 没有截图 / 视觉证据。
- 用户指出的问题只修了单个 frame，未检查同页面、同组件族、同断点或相似页面。
- 截图仍存在遮挡、重叠、文本 / 容器溢出、移动端安全边距不足或页面级横向溢出。
- 同语义字体层级不一致，或通过随意缩小字号掩盖布局问题。
- `MASTER` 与 Page Overrides 冲突，且没有上游确认。
- 设计系统冲突、范围漂移或关键状态缺失仍未归属。
- 只有主观判断，没有 frame、截图、视口、状态、文件或产物段落证据。

## 严重性

- `P0`: 视觉 / 布局问题导致核心流程不可用，例如主按钮被遮挡、页面白屏、移动端无法提交、关键表单不可操作。
- `P1`: 主流程明显受损，例如关键错误态缺失、严重横向溢出、设计系统大面积漂移、信息层级误导用户。
- `P2`: 影响体验或专业度，例如局部遮挡、字体 / 间距不统一、卡片不齐、状态不完整、移动端次要区域破版。
- `P3`: 轻量视觉优化，例如局部文案、轻微间距、非阻断对齐建议。

## 流程

1. 识别审查对象：Figma 设计稿、截图、前端页面 URL、figma-handoff、frontend-acceptance，或组合输入。
2. 读取产品事实源和 `ui/ui-design-system.md`；先建立产品范围、设计系统 `MASTER` 和 Page Overrides。
3. 收集视觉证据：Figma screenshot、用户截图、浏览器截图、视口尺寸、frontend-acceptance 记录或产物段落。无法获取时记录证据缺口。
4. 执行同类问题扫描：如果发现字体、间距、遮挡、溢出、状态缺失或组件漂移，检查同页面、同组件族、同断点、相似列表 / 表格 / 卡片 / 表单是否复现。
5. 分层审查：先找 P0 / P1 阻断，再找 P2 / P3 专业度和一致性问题。
6. 每个 finding 指向具体页面 / frame / 区域 / 截图位置 / 视口 / 状态 / 产物段落，并给出影响、建议、证据和归属。
7. 归属规则：设计稿问题回 `$pd-figma`；实现展示问题回 `$pd-fe`；设计系统或页面范围事实源问题回 `$pd-blueprint` / `$pd-plan`；证据不足写“待人工确认”。
8. 写入或更新 `ui/ui-review-report.md`，记录截图证据、同类问题扫描、不能交付检查和是否建议进入下一阶段。
9. 输出摘要，不建议 `$pd-git`。

## 用户截图问题修复闭环

当用户用截图指出“字体不统一、遮挡、重叠、突兀、不整齐、对齐错位、间距混乱、移动端溢出”等问题时：

1. 先复述为可检查类别，例如 `typography drift`、`occlusion`、`overflow`、`alignment drift`、`density mismatch`。
2. 定位影响范围：具体 frame / 页面 / 区域 / 视口 / 状态，并列出需要扫描的相似 frame 或组件族。
3. 如果用户要求只审查，输出 findings 和归属；如果用户要求修复，必须回到 `$pd-figma` 或 `$pd-fe` 执行，修复后重新截图。
4. 修复完成前，不能只写“已处理”；必须有截图证据、零容忍 checklist 结果、同类问题扫描结果和待人工确认项。

## 输出摘要

```text
UI Review 完成: <name>
目录: <output-dir>
文件:
  - ui/ui-review-report.md
结论: <无阻断 / 有 P0 / 有 P1 / 有建议项 / 证据不足>
下一步: <回到 $pd-figma / $pd-fe / $pd-plan / $pd-blueprint / 待人工确认>
```
