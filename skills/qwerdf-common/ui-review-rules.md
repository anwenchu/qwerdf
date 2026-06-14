# UI Review Rules

本文件用于 `$pd-review` 的 UI 设计质量审查，也可供 `$pd-fe` 完成前自检。UI finding 必须有证据：文件 / 组件、Figma frame、截图、视口、状态、产物段落或测试结果。

## 1. 审查输入

涉及前端 UI、样式、组件、路由、页面、Figma handoff 或 `frontend-acceptance.md` 时，必须读取：

- `ui/ui-design-system.md`
- `ui/ui-screens.md`
- `ui/ui-components.md`
- `ui/figma-handoff.md`
- `tech/frontend/frontend-design.md`
- `tech/frontend/frontend-acceptance.md`
- 本文件和 `ui-quality-checklist.md`

缺少关键设计证据时，不能声称 UI 已通过；应写为证据缺口或残余风险。

## 2. 审查维度

- 设计系统一致性：颜色、字体、间距、圆角、阴影、按钮层级、组件变体是否符合 `MASTER`。
- 产品类型匹配：管理后台 / SaaS / CRM 是否保持克制、密集、可扫描；landing page 是否只在需求允许时出现。
- 信息层级：页面主任务、主按钮、状态、错误和危险操作是否清楚。
- 状态覆盖：default、loading、empty、error、permission、saving / submitting 是否可展示和可恢复。
- 响应式：桌面和移动端是否无横向溢出、无遮挡、无文本重叠。
- 可访问性：键盘焦点、label、aria、对比度、reduced motion。
- 表单 / 表格 / 图表：校验、排序、分页、单位、时间范围、空错态和批量操作是否完整。

## 3. 严重性

- `P0`: UI 导致核心流程不可用，例如主按钮不可见 / 被遮挡、移动端核心页面无法操作、提交状态卡死、关键页面白屏或无法启动。
- `P1`: 主流程可见但风险明显，例如关键状态缺失、权限 / 错误态误导用户、设计系统严重漂移、移动端严重横向溢出、表单错误无法定位、关键数据图表误导。
- `P2`: 边界状态、局部响应式、可维护性或体验风险，例如长文案溢出、非核心空态缺少下一步、表格密度不稳定、组件 props 过复杂、轻度可访问性缺口。
- `P3`: 不阻断的命名、局部间距、文案一致性、轻量重构或视觉微调建议。

不得把没有截图、文件、视口、状态或设计系统证据的主观判断升级为 `P0` / `P1`。

## 4. Finding 写法

每个 UI finding 必须包含：

- 级别：P0 / P1 / P2 / P3。
- 类别：UI / 设计系统 / 响应式 / 可访问性 / 状态覆盖 / 表单 / 表格 / 图表。
- 文件 / 行号或区域：组件路径、CSS 文件、页面路径、Figma frame 或验收清单条目。
- 问题：具体到状态、视口或交互。
- 影响：对用户任务、主流程、误操作、可访问性或维护成本的影响。
- 修复归属：通常为 `$pd-fe`；若设计系统或 Figma handoff 错，归 `$pd-figma` 或 `$pd-plan`。
- 验证方式：截图、Playwright / 浏览器 smoke、组件测试、视觉回归、移动端视口验证、键盘验证。

## 5. 防误报

- 不把“我更喜欢另一种风格”写成 finding；必须对照产品类型、设计系统或验收标准。
- 不要求后台系统采用营销页 hero、装饰卡片或大面积氛围图。
- 不因 Figma 没有逐像素一致就报错；只有影响信息层级、状态、可访问性或设计系统约束时才作为 finding。
- 不把 formatter、class 顺序、轻微像素差作为主要问题，除非导致真实布局或交互风险。
