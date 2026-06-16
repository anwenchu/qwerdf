# Frontend Code Review

当 diff 涉及 TypeScript、React、API client、页面状态、CSS / 移动端布局或浏览器行为时读取。

## TypeScript

- 检查类型收窄是否真实覆盖 nullable / optional 字段；不要用 `as`、`!` 或宽泛 fallback 掩盖契约缺口。
- `any`、`unknown`、宽泛 record、字符串状态枚举必须有边界说明；DTO 类型要与 `tech/api-contract.md` 字段、分页、错误结构一致。
- 异步函数必须处理 reject、取消、重复触发和 stale response；不要让 Promise 错误只出现在 console。
- API client 的 request / response mapper 不得静默丢字段、改名或把后端错误映射成成功态。

## React

- 状态来源要单一：避免 props、URL、server data、local state 多处复制后失同步。
- `useEffect` 依赖必须能解释；避免把事件逻辑、派生状态或同步计算塞进 effect。
- 请求竞态要可控：快速切换筛选、分页、tab、弹窗关闭或路由离开时，不应把旧响应写回新状态。
- 受控表单要处理清空、默认值、校验失败、提交中、重复提交和服务端错误。
- 页面必须覆盖 loading / empty / error / permission / success 状态，且状态文案和操作符合产品事实源。

## UI / 交互

- 检查移动端布局、横向溢出、焦点可达、键盘操作、滚动容器、弹窗关闭、可访问标签和 reduced motion。
- 组件 props 复杂度过高、多个 boolean 模式组合、隐式 children 协议或重复渲染路径，可能导致可维护性 finding。
- 性能风险包括重复请求、数据 waterfalls、过度重渲染、无边界 memo、过大 bundle、同步阻塞计算和未清理订阅 / timer。

## API 契约与真实依赖

- 前端状态、字段命名、分页结构、状态枚举和错误码必须与 `tech/api-contract.md`、`tech/integration-map.md`、真实 API 行为一致。
- 技术实现禁止使用任何 mock；mock-only 分支、stub、fake、fixture-only 数据流或 simulator 一旦出现，必须作为阻断或缺陷处理，并能在 `sync/integration-report.md` 中被验证。

## 测试

- 前端测试至少覆盖关键交互、错误态、空态、权限态、表单失败、重复提交和核心响应式布局。
- 对复杂状态机或 API mapper，优先要求单测；对页面主流程，优先要求浏览器验证或 E2E。
