# Screenshot Review Reference

用于 `$pd-ui-review` 审查用户截图、本地页面 URL、浏览器截图和前端 UI 验收证据。

## 证据采集

- 本地页面 URL：优先用浏览器或 Playwright 在 375px、768px、1024px、1440px 视口截图，并记录 URL、视口、状态和时间。
- 用户截图：记录截图文件名、可见页面、可见状态、可见区域；不可见的 hover / focus / hidden content 标为待确认。
- `frontend-acceptance.md`：检查是否记录桌面 / 移动端、无横向溢出、无文本重叠、状态覆盖和 console / network 证据。
- 多页面或多断点修改：每个被修改页面 / frame / 断点都需要截图；只提供一个局部截图时，未覆盖区域不得写为已通过。

## 截图专项检查

- 页面级横向溢出：移动端 body 或主容器是否超出视口；表格是否用了局部滚动容器或降级卡片。
- 遮挡：固定导航、底部按钮、toast、弹窗、抽屉、popover 是否遮住关键字段、主按钮、错误提示或列表操作。
- 文本：标题、按钮、表格、badge、错误提示是否换行、截断、tooltip 或完整展示；长数字和英文是否撑破布局。
- 对齐：左边缘、表单 label/input、按钮组、卡片网格、表格表头/内容是否成列。
- 视觉一致性：字体、颜色、圆角、阴影、icon、按钮尺寸是否符合设计系统。
- 状态：截图是否能证明 default / loading / empty / error / permission / saving / disabled 等关键状态。
- 可访问性：焦点是否可见，icon-only 操作是否有 label / tooltip，颜色是否不是唯一信息表达。

## 同类问题扫描

- 发现一个遮挡问题时，检查同类 fixed header / footer / side nav / bottom action / toast / modal / drawer。
- 发现一个字体层级问题时，检查同页面 headings、tabs、filters、buttons、table cells、badges、empty / error 文案。
- 发现一个溢出问题时，检查长中文、长英文、数字、金额、状态标签、面包屑、按钮文案和表格列。
- 发现一个移动端问题时，至少检查 375px，并尽量补 768px / 1024px / 1440px 对比。
- 发现一个列表 / 表格 / 卡片问题时，检查同类数据模板、对齐、分隔、行高 / 卡片高度和移动端降级。

## 不能放行

- 没有截图证据，却声称视觉通过。
- 截图仍显示遮挡、重叠、页面级横向溢出、固定栏遮挡关键操作或文本撑破容器。
- only desktop default 状态通过，但移动端、错误态、空态、加载态或权限态是主流程风险。
- 用户指出问题后，没有给出相似页面 / 组件 / 断点的扫描结果。

## 证据不足写法

- “当前截图只覆盖桌面 default 状态，无法判断移动端横向溢出、hover/focus、loading/error/permission 状态；标为待确认，不作为已通过。”
- “截图看不到 Figma frame 或 design system 来源，无法判断是设计稿问题还是实现偏差；归属待确认。”
