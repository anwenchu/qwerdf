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
- 移动端：优先单列、触控目标、底部关键动作、内容折叠和输入效率；表格策略遵循 [共享布局规则](ui-quality-checklist.md#2-布局间距与内容边界)，在 MASTER 记录本次选择与理由。
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
- Radius / elevation：圆角、阴影、分隔线；沿用已有系统或按产品任务选择，不为所有卡片设统一像素上限。
- Components：按钮、输入、选择器、表格、列表、卡片、抽屉、弹窗、toast、badge、tabs、空态、错误态、加载态。
- Interaction states：hover、focus、active、disabled、selected、loading、saving、success、error。
- Responsive / accessibility：移动端布局、键盘焦点、语义、对比度、文本溢出策略、reduced motion。

其中字体、间距和复杂信息展示必须可执行：

- Typography semantic levels：至少定义页面标题、分组标题、正文、辅助说明、表格文本、数字 / 金额、按钮、错误提示、移动端正文；每级包含字号、行高、字重和使用场景。
- 不得把“按需缩小字体”作为适配策略；字段过多时必须转为布局、换行、截断、tooltip、分组、摘要 / 详情或响应式降级策略。
- Spacing scale：定义页面边距、移动端安全边距、section gap、组件 padding、表单行距、表格行高、卡片 gap；默认使用 4 / 8 基础尺度或已有系统尺度。
- Safe area：固定 header、footer、bottom action、toast、floating action、drawer、modal 对内容的避让规则。
- Complex information patterns：列表、表格、卡片、详情、记录流、数据看板的信息优先级、格式化规则、列宽 / 行高策略、移动端降级方式和溢出处理。

## 5. Page Overrides

页面级 override 只能记录必要差异：

- 页面目标不同导致的信息密度或布局差异。
- 特定页面需要的组件变体、图表规则、表格列密度、移动端转换方式。
- 特定状态的文案、权限、错误恢复或空态 CTA。

禁止在 page override 中重定义全局颜色、字体、圆角、按钮层级或导航模式，除非说明该页面为什么必须偏离 `MASTER`。

## 6. 设计系统门禁

以下完整性要求只适用于本次涉及的页面、组件、平台和状态；小范围修订不强制补齐历史全套设计系统。不适用项说明理由，影响本次关键操作或验收的未知项才阻断受影响范围。严重性与交接条件统一见 [UI Review Rules](ui-review-rules.md)。

- 没有 `ui/ui-design-system.md` 时，`$pd-figma` 必须先创建或补齐，再进入 Figma 写入。
- `MASTER` 缺少本次高保真 frame 必需的字体、spacing scale、安全区、状态或信息展示约束时，先复用已有系统或补齐受影响部分；无法判断关键设计决策时回 `$pd-blueprint` 澄清，不为无关维度强制补全历史文档。
- `$pd-plan` 输出前端技术设计时，必须把 `MASTER` 和 page override 转成前端约束：组件复用、状态、响应式、可访问性、表单校验、错误映射和验收方式。
- `$pd-fe` 实现时必须读取 `ui/ui-design-system.md`；发现设计系统缺失或与 Figma handoff 冲突时，记录阻塞并回到 `$pd-figma` 或 `$pd-plan`。
- `$pd-review` 对 UI diff 必须检查实现是否漂移：颜色、字体、间距、圆角、组件层级、状态、移动端和可访问性是否偏离设计系统。
- `$pd-ui-review` 对 Figma frame、截图或本地页面 URL 必须用 `MASTER` / Page Overrides 判断字体、间距、安全区、状态和产品类型是否一致；没有截图证据时不得放行。

## 7. Token 与组件契约

- 先复用已有设计系统、Figma 变量、组件库及项目 token，不为借鉴外部目录重命名或重建一套。新设计建议区分基础值、语义角色与组件引用；小项目可直接使用语义 token，无需强制三层文件。
- 在 MASTER 记录本次使用的 token 名称、值 / 别名、主题 / 用途、来源与状态。来源可为已确认系统、节点 / CSS 测量、设计建议；截图估计只能标待核对，不把默认值或推断说成测量事实。空缺是否阻断取决于受影响的关键设计决策。
- 组件规则引用语义 token、允许 variant、关键状态与内容 / 交互约束；`ui/ui-components.md` 维护页面、业务输入 / 事件及复用关联，不复制 token 值。具体代码 API、props 类型和工程路径交 `$pd-plan`，不在蓝图阶段发明实现。
- Page Overrides 只写差异、理由、来源和影响范围，不复制 MASTER。代码已有 CSS / JSON token 时链接现有事实源；设计值与实现绑定的对应关系需可追溯，冲突由负责人协调，不双向手改多份值。
- CSS、JSON、组件索引或预览如需导出，标为派生产物并记录生成来源；不要求纯蓝图任务生成这些文件。检查显式未知引用、别名无法解析或循环、组件引用漂移；默认值、别名与人工判断各自标明。
- 风格 / 配色检索仅按产品类型、任务、品牌、信息密度与平台选取少量候选并说明取舍。中文输入可转换为检索关键词；零命中说明缺口，不静默套营销页或覆盖现有 MASTER。不内置或强制安装外部整套数据库。
