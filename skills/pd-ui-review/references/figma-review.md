# Figma Review Reference

用于 `$pd-ui-review` 审查 Figma URL、frame、Figma screenshot 和 `ui/figma-handoff.md`。

## 读取和证据

- 按 Figma skill 规则获取 frame context 和 screenshot；无法访问时记录授权 / URL / frame 缺口。
- 对照 `product/product-brief.md`、`ui/ui-pages.md`、`ui/ui-screens.md` 和 `ui/ui-components.md` 检查页面范围。
- 对照 `ui/ui-design-system.md` 检查 `MASTER`、Page Overrides、颜色、字体、间距、圆角、组件状态和响应式规则。
- finding 证据优先写 frame 名、页面名、组件名、截图位置和相关 handoff 段落。
- 审查 `$pd-figma` 交付时，检查 `ui/figma-handoff.md` 是否记录每个目标 frame / 断点的截图 QA、低级视觉问题零容忍结果和同类问题扫描。

## Figma 专项检查

- Design system：变量、文本样式、组件 variants 是否来自同一套系统；页面级差异是否写入 Page Overrides。
- Frame 完整性：default、loading、empty、error、permission 是否覆盖；主流程是否包含关键交互状态。
- 范围漂移：Figma 是否新增 PRD / product-brief / ui-pages 中没有的页面、导航、tab、业务模块、文案或参考产品能力。
- 基础视觉：对齐、间距、字体、颜色、阴影、圆角、icon 风格和按钮层级是否统一。
- 交付可实现性：组件状态、响应式说明、表格移动端降级、表单校验、错误恢复是否足够给 `$pd-plan` 和 `$pd-fe` 使用。
- 字体与间距：Typography semantic levels、spacing scale、移动端安全边距是否来自 `MASTER`；不得靠缩小字号解决布局问题。
- 复杂信息展示：列表、表格、卡片、详情、记录流和数据看板是否有信息优先级、稳定模板、格式化规则和移动端降级。

## 不能放行

- 关键 frame 没有 screenshot。
- 用户指出的问题没有扫描相似 frame / component family / responsive breakpoint。
- frame 截图仍有遮挡、重叠、文本溢出、移动端横向溢出或固定栏遮挡。
- `MASTER` 与 Page Overrides 冲突，且 handoff 未解释。
- 状态页缺 error / permission / loading 等主流程状态。

## 归属判断

- Figma frame 本身错位、状态缺失、设计系统漂移：归 `$pd-figma`。
- Figma 与产品事实源冲突：归 `$pd-blueprint` 或 `$pd-plan`，并标出冲突来源。
- Figma 正确但前端实现偏离：归 `$pd-fe`，证据需同时引用 Figma / handoff 和截图 / 页面。
