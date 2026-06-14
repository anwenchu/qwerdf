# UI Design System Rules

本文件定义 Product Delivery 链路中的 UI 设计系统生成规则。它不是灵感库；只记录可被 `$pd-blueprint`、`$pd-figma`、`$pd-plan`、`$pd-fe` 和 `$pd-review` 共同执行和验证的设计约束。

## 1. 事实源

- 全局设计系统事实源写入 `ui/ui-design-system.md`。
- `ui/ui-design-system.md` 的 `MASTER` 是唯一事实源；页面级差异只能写在 `Page Overrides`，不得复制一份新的局部设计系统。
- `$pd-blueprint` 负责基于 PRD / product-brief 初建设计系统草案；`$pd-figma` 负责在生成或整理 Figma 前确认 / 补全；`$pd-plan`、`$pd-fe`、`$pd-review` 只读取和执行，不越权改写上游产品事实。
- 设计系统不能新增 PRD、product-brief 或 UI 蓝图中不存在的页面、业务模块、导航、资产类型、文案或产品能力。

## 2. 生成输入

生成或修订 `ui/ui-design-system.md` 时，必须先明确：

- 产品类型：SaaS、CRM、管理后台、操作台、数据看板、移动端工具、内容站、landing page 等。
- 用户角色：主要使用者、权限差异、重复使用频率。
- 核心任务：用户进入页面后最重要的 1 到 3 个任务。
- 信息密度：低 / 中 / 高，并说明原因。
- 视觉气质：用可执行词描述，例如克制、清晰、可信、扫描优先、交易密集；避免只写“高级感”“现代化”“好看”。
- 页面模式：表格列表、筛选列表、详情、表单、设置页、数据看板、工作台、移动单列、营销首屏等。
- 设计风险：范围漂移、信息过载、移动端拥挤、关键状态缺失、图表误导、参考产品误带入。

## 3. 产品类型默认策略

- SaaS / CRM / 管理后台 / 操作台：默认克制、密集、可扫描、效率优先；导航稳定，表格 / 筛选 / 批量操作可重复使用；避免营销页式 hero、过度卡片化、大面积装饰图和只为展示而存在的空白。
- 数据看板：优先指标可比性、时间范围、筛选条件、图例、单位和异常状态；图表服务决策，不用图表填充页面。
- 表单 / 设置页：优先分组、默认值、校验、错误恢复、保存反馈和危险操作确认；不要让用户在提交后才发现必填和格式错误。
- 移动端：优先单列、触控目标、底部关键动作、内容折叠和输入效率；桌面密集表格必须转换为卡片、分组列表或横向摘要。
- Landing page：只有 PRD 明确是获客 / 营销页面时才使用；首屏必须直接呈现产品 / 品牌 / offer，不得把业务产品误做成宣传首页。

## 4. MASTER 内容

`MASTER` 至少包含：

- Product type / user roles / core tasks / information density。
- Visual direction：页面气质、信息组织、禁止带入的参考元素。
- Navigation：全局导航、局部 tab、面包屑、返回路径。
- Layout：栅格、内容宽度、固定区、滚动区、响应式断点。
- Color tokens：主色、语义色、背景、边框、文本、图表色；说明使用场景和禁用场景。
- Typography：字号层级、标题 / 正文 / 数字 / 表格字号、行高、字重。
- Spacing：页面边距、组件间距、表格密度、表单行距。
- Radius / elevation：圆角、阴影、分隔线；默认卡片圆角不超过 8px，除非已有设计系统规定。
- Components：按钮、输入、选择器、表格、列表、卡片、抽屉、弹窗、toast、badge、tabs、空态、错误态、加载态。
- Interaction states：hover、focus、active、disabled、selected、loading、saving、success、error。
- Responsive / accessibility：移动端布局、键盘焦点、语义、对比度、文本溢出策略、reduced motion。

## 5. Page Overrides

页面级 override 只能记录必要差异：

- 页面目标不同导致的信息密度或布局差异。
- 特定页面需要的组件变体、图表规则、表格列密度、移动端转换方式。
- 特定状态的文案、权限、错误恢复或空态 CTA。

禁止在 page override 中重定义全局颜色、字体、圆角、按钮层级或导航模式，除非说明该页面为什么必须偏离 `MASTER`。

## 6. 设计系统门禁

- 没有 `ui/ui-design-system.md` 时，`$pd-figma` 必须先创建或补齐，再进入 Figma 写入。
- `$pd-plan` 输出前端技术设计时，必须把 `MASTER` 和 page override 转成前端约束：组件复用、状态、响应式、可访问性、表单校验、错误映射和验收方式。
- `$pd-fe` 实现时必须读取 `ui/ui-design-system.md`；发现设计系统缺失或与 Figma handoff 冲突时，记录阻塞并回到 `$pd-figma` 或 `$pd-plan`。
- `$pd-review` 对 UI diff 必须检查实现是否漂移：颜色、字体、间距、圆角、组件层级、状态、移动端和可访问性是否偏离设计系统。
