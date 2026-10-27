# Codex Product Delivery 规则

本文件是所有 `$pd-*` skill 的共享规则源。它们是独立的开源 Codex Product Delivery Skills，不绑定任何外部变更生命周期，不参与外部研发流程状态流转。

产品和设计阶段模板见 [artifact-contracts.md](artifact-contracts.md)。工程阶段模板见 [engineering-contracts.md](engineering-contracts.md)。
UI 设计系统和质量规则见 [ui-design-system.md](ui-design-system.md)、[ui-quality-checklist.md](ui-quality-checklist.md)、[ui-patterns.md](ui-patterns.md)、[ui-review-rules.md](ui-review-rules.md)。

## 1. 交付链路

```text
$pd-vet -> $pd-prd -> $pd-blueprint -> $pd-figma -> $pd-ui-review -> $pd-plan -> $pd-fe + $pd-be -> $pd-sync -> $pd-test -> $pd-review -> $pd-git -> $pd-release
```

| 阶段 | 负责 Skill | 必要产物 |
| --- | --- | --- |
| 想法验证 | `$pd-vet` | `product/idea-brief.md`、`product/user-problem.md`、`product/competitor-notes.md`、`product/mvp-hypothesis.md`、`product/validation-questions.md` |
| PRD 生成 | `$pd-prd` | `product/prd.md`、`product/requirements.md`、`product/user-stories.md`、`product/acceptance-criteria.md`、`product/open-questions.md` |
| 产品设计输入 | `$pd-blueprint` | `product/product-brief.md` |
| UI 页面蓝图 | `$pd-blueprint` | `ui/ui-design-system.md`、`ui/ui-flows.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md` |
| Figma 设计交付 | `$pd-figma` | `ui/ui-design-system.md`、`ui/ui-directions.md`、`ui/figma-handoff.md` |
| UI 设计质量审查 | `$pd-ui-review` | `ui/ui-review-report.md` |
| 技术设计 | `$pd-plan` | `tech/tech-plan.md`、`tech/dependency-readiness.md`、`tech/frontend/frontend-design.md`、`tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md`、`tech/frontend/frontend-state-api.md`、`tech/backend/backend-design.md`、`tech/api-contract.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md`、`tech/integration-map.md`、`tech/task-slices.md`、`tech/risk-plan.md` |
| 前端实现 | `$pd-fe` | `tech/frontend/frontend-implementation-log.md`、`tech/frontend/frontend-changed-files.md`、`tech/frontend/frontend-dev-notes.md`、`tech/frontend/frontend-acceptance.md` |
| 后端实现 | `$pd-be` | `tech/backend/backend-implementation-log.md`、`tech/backend/backend-changed-files.md`、`tech/backend/backend-dev-notes.md` |
| 前后端联调 | `$pd-sync` | `sync/integration-plan.md`、`sync/integration-report.md`、`sync/api-mismatch.md`、`sync/plan-revision.md` |
| 测试验证 | `$pd-test` | `test/test-plan.md`、`test/test-cases.md`、`test/test-report.md`、`test/regression-notes.md` |
| Code Review | `$pd-review` | `test/code-review.md` |
| Git 提交准备 | `$pd-git` | `release/commit-summary.md`、`release/pr-description.md` |
| 上线文档 | `$pd-release` | `release/release-plan.md`、`release/release-checklist.md`、`release/rollback-plan.md`、`release/release-notes.md` |

## 2. 默认工作目录

如果用户未指定输出目录，默认在当前工作区创建：

```text
pd-work/<name>/
  product/
  ui/
    ui-design-system.md
    ui-review-report.md
  tech/
    dependency-readiness.md
    frontend/
    backend/
  sync/
  test/
  release/
```

其中 `<name>` 优先来自用户提供的项目名 / 产品名；没有明确名称时，用简短 kebab-case 名称推导，例如 `ai-crm-dashboard`。

如果用户明确要求写到其他目录，使用用户指定目录，但保持同一组分目录和文件名。

新产物必须写入上面的 canonical path。读取上游产物时，先读取 canonical path；如果旧项目已经存在平铺文件，例如 `pd-work/<name>/prd.md`，可以作为 legacy fallback 读取，但后续写入和摘要都必须使用 canonical path。

## 3. Skill 执行规范

- 每个 `$pd-*` skill 只读取本阶段需要的公共模板和上游产物，避免一次性加载无关模板。
- 触发描述必须说明 “做什么” 和 “什么时候使用”，不要只罗列命令名。
- 产物必须可复用：写清输入来源、关键判断、未验证假设、验证证据和下一步。
- 缺少关键输入时先列出缺口并提问，不生成看似完整但依据不足的文件。
- 需要修改代码、设计、Git 或外部系统时，遵守对应 skill 的边界；没有明确授权时只做计划、报告或文案。
- 执行命令、浏览器验证或截图检查后，必须在对应报告中记录命令 / 方式、结果和证据位置。
- 当任务反复出现相同机械步骤时，优先把步骤沉淀为脚本或公共模板，而不是在多个 skill 中复制长指令。
- 修改 skill 描述、触发词或阶段边界后，检查 `evals/cases/trigger-queries.json`，确保 should-trigger 和 should-not-trigger 样例仍然成立。

### 产品事实与参考使用 Gate

- 产品事实源优先级：用户明确说明、PRD、需求清单、产品设计输入、UI 页面蓝图、现有代码 / 数据结构高于竞品、截图、Figma 参考和视觉样例。参考材料不能覆盖或扩展产品事实源。
- 设计前必须先建立产品事实锁：产品名称、目标用户、核心场景、支持的业务对象、页面 / 导航范围、明确不做的内容。
- 外部参考必须拆成两类：可借鉴的抽象视觉 / 交互模式，以及不得带入的业务语义 / 导航文案 / 产品模块 / 交易品类 / 品牌资产 / 受保护文案。
- 参考对象中出现但产品事实源未出现的功能、页面、tab、资产类型、合约类型、营销入口、社区 / 活动 / copy trading 等模块，默认视为参考禁区，只能写进“不得带入 / 不应照搬”，不能成为产品范围、页面结构、Figma frame、API 契约或任务切片。
- 如果无法判断某个参考元素是视觉风格还是产品能力，先提问；无人确认时按不带入处理。
- 设计输出必须能追溯：页面、组件、状态、导航和关键文案都要来自产品事实源或明确的用户确认；参考材料只贡献风格、布局密度、信息组织方式或微交互。
- Figma / 截图是表现层参考，不是需求来源。Figma handoff 与 PRD、product-brief 或 UI 蓝图冲突时，先记录冲突并停止，不把冲突内容下推到技术设计或实现。

### UI 设计系统与质量 Gate

- `ui/ui-design-system.md` 是 UI 设计系统事实源，`MASTER` 定义全局规则，`Page Overrides` 只记录必要页面差异。不得在页面规格、Figma handoff 或前端技术设计中复制出互相冲突的局部设计系统。
- `$pd-blueprint` 必须在产品设计输入阶段明确产品类型、用户角色、核心任务、信息密度、视觉气质、页面模式、导航结构、关键状态和设计风险，并生成设计系统草案。
- `$pd-figma` 在生成 UI 方向或写入 Figma 前必须读取或补齐 `ui/ui-design-system.md`；UI 方向只能改变呈现方式，不能改变产品范围。
- 候选先在 Figma 展示、用户选择后深化；已有方向或仅本地预览的处理统一见 [pd-figma 的方向交付流程](../pd-figma/SKILL.md#gate-1在-figma-比较并选择-ui-方向)。候选不等于正式 handoff，不据此进入技术设计。
- `$pd-figma` 创建或修改 Figma frame 后必须执行交付前截图级视觉 QA：每个目标 frame / 断点都要有截图证据，检查遮挡、重叠、溢出、字体、间距、安全区、状态和产品类型适配，并记录同类问题扫描。
- `$pd-figma` 不得只凭文字或图层描述声称已修复；用户指出的字体、间距、遮挡、重叠、突兀、不整齐或移动端溢出问题，必须修复后重新截图并检查相似 frame / 组件 / 断点。
- `$pd-ui-review` 是独立 UI 设计质量审查 gate，默认放在 `$pd-figma` 后、`$pd-plan` 前；也可在 `$pd-fe` 后用于视觉回归。它只输出 `ui/ui-review-report.md`，不改设计稿、不改代码、不提交。
- `$pd-ui-review` 必须审查产品事实源、`ui/ui-design-system.md` 的 `MASTER` / `Page Overrides`、Figma handoff、Figma frame、截图或本地页面 URL；发现 P0/P1 时必须把归属指向 `$pd-figma`、`$pd-fe`、`$pd-plan` 或 `$pd-blueprint`，不得泛泛评价“美观”。
- `$pd-ui-review` 的阻断、残余风险及授权后的修复交接统一遵循 [UI Review Rules](ui-review-rules.md)，不以交付阻断禁止修复原 finding。
- UI 审查适用性、严重性和交接条件统一见 [UI Review Rules](ui-review-rules.md)；检查项与默认尺寸见 [UI Quality Checklist](ui-quality-checklist.md)。截图不要求运行环境证据，不适用状态不强制生成，未覆盖范围不得宣称已验证。
- `$pd-plan` 必须把 `ui/ui-design-system.md` 和 `ui/figma-handoff.md` 转成前端技术约束：组件复用、状态覆盖、响应式、可访问性、表单校验、错误映射、空态和 UI 验收方式。
- `$pd-fe` 必须读取 `ui/ui-design-system.md` 和 UI 质量清单后实现；完成后在 `tech/frontend/frontend-acceptance.md` 记录本次平台、无横向溢出、文本不重叠及适用状态的检查证据；状态适用性统一遵循 [UI Quality Checklist](ui-quality-checklist.md#4-适用的状态与交互)，不适用写明理由。
- `$pd-review` 涉及 UI diff 时必须执行 UI Review：检查设计系统一致性、产品类型匹配、信息层级、响应式、可访问性、状态覆盖、表单 / 表格 / 图表质量，并按 P0/P1/P2/P3 输出带证据的 finding。
- SaaS / CRM / 管理后台 / 操作台类产品默认采用克制、密集、可扫描、效率优先的界面方向；不要把 landing page hero、过度卡片化、装饰性插画或大面积氛围图带入操作型产品，除非 PRD 明确要求营销页面。

### UI 职责边界

- `$pd-blueprint`：定义产品事实、页面范围、产品类型、信息密度、页面模式、关键状态和设计风险，生成 `ui/ui-design-system.md` 草案；不写 Figma 高保真。
- `$pd-figma`：确认 / 补齐 `MASTER`，生成 UI 方向，写入或整理 Figma，完成截图级视觉 QA 和 `ui/figma-handoff.md`；不改 PRD、技术方案或代码。
- `$pd-ui-review`：独立审查 Figma frame、handoff、截图和本地页面 UI 表现，输出 `ui/ui-review-report.md`；默认只审查，不改设计稿、不改代码、不提交。
- `$pd-plan`：把设计系统、handoff 和 UI Review 结论转成前端技术约束和 task slice；不擅自新增页面、导航或视觉风格。
- `$pd-fe`：按设计系统和技术设计实现，并在 `tech/frontend/frontend-acceptance.md` 记录桌面 / 移动端截图、状态、无横向溢出和无文本重叠证据；不修改上游设计事实源来掩盖实现偏差。
- `$pd-review`：做代码级和交付级审查，读取 `ui/ui-review-report.md` 和前端验收证据；发现 UI P0/P1 时阻断 `$pd-git`。

## 4. 安全与意外最小化

- Skill 内容不能包含与描述不符的隐藏行为、越权访问、数据外传、恶意脚本或误导性流程。
- 不把 token、cookie、密钥、敏感信息写入命令、日志、产物或 PR 描述。
- 涉及 Git、Figma、发布平台、外部 API、真实部署或写入外部系统时，先说明目标、范围和动作后再执行。
- 默认不执行 destructive、push、deploy、publish、sync-to-external 等高影响动作，除非用户明确要求并且对应 skill 允许。
- 读取外部或远程规则时记录来源；规则版本可能变化时，不把旧规则当作当前事实。

## 5. 外部 SKILL.md 内容模式

本仓库补充规则参考以下具体 `SKILL.md` 内容模式，而不只是参考仓库目录结构：

- Anthropic `skill-creator/SKILL.md`：触发描述要“偏主动”，正文用渐进式披露；长规则放 references / common，脚本可作为黑盒执行；改 skill 时用测试提示和反馈迭代。
- Anthropic `frontend-design/SKILL.md`：设计前先钉住主体、受众和页面任务；先写颜色、字体、布局、标志性元素的短计划，再自检是否模板化。
- Anthropic `webapp-testing/SKILL.md`：浏览器验证采用决策树，先确认静态 / 动态、服务是否运行，再侦察渲染态，最后执行交互；动态页面检查前等待稳定加载。
- Vercel `react-best-practices/SKILL.md` 和 `composition-patterns/SKILL.md`：把规则按优先级分组，先处理 waterfalls、bundle、server/client 数据、重渲染、组件架构等高影响问题。
- Vercel `vercel-optimize/SKILL.md`：先收集信号，再用确定性 gate 收窄调查范围；建议必须绑定证据、文件和版本，不做泛泛扫描。
- Vercel `web-design-guidelines/SKILL.md`：外部规则源可能变化时，先读取最新规则，再按指定文件 / 范围输出定位清晰的 findings。

## 6. 外部生命周期边界

这些 Skill 不做以下事情：

- 不创建外部变更目录。
- 不修改 `.state.yaml`。
- 不设置外部 artifact 状态。
- 不改变外部 change 生命周期状态。
- 不要求外部方案、任务拆分或实现流程作为前置或后置。
- 不把交付产物同步到 Apifox / Lark，除非用户单独明确要求。

## 7. 设计与工程 Gate

- 技术设计的关键链路依据、需求到改动的必要性及未决项交接，统一见 [技术设计依据与范围规则](technical-design-rules.md)。只读影响核查不代表授权扩大本期改动；设计是否明确与真实依赖是否 ready 分开判断。
- `$pd-plan` 完成前，不允许进入 `$pd-fe` 或 `$pd-be`。
- `$pd-fe` 和 `$pd-be` 必须基于同一份 `tech/task-slices.md`、`tech/api-contract.md` 和 `tech/integration-map.md`。
- `$pd-fe` 必须基于同一份 `ui/ui-design-system.md`、`ui/figma-handoff.md` 和 `tech/frontend/frontend-design.md`；设计系统缺失、冲突或未转成前端约束时，先回到 `$pd-figma` 或 `$pd-plan`。
- `$pd-plan` 前建议先执行 `$pd-ui-review`；如果尚未执行，`$pd-plan` 必须把 Figma 截图 QA 和 UI Review 缺失记为设计证据缺口，不得假装视觉质量已验收。
- 如果存在 `ui/ui-review-report.md` 且包含未解决 P0/P1，后续 `$pd-plan`、`$pd-fe`、`$pd-review` 必须阻断受影响范围的交付；P2/P3 必须作为残余风险读取。用户已授权的修复按 [UI finding 修复交接](ui-review-rules.md#6-ui-finding-修复交接) 执行，视觉问题不能靠代码提交流程绕过。
- `$pd-plan` 必须产出 `tech/backend/sql-execution-plan.md`：涉及 DDL、DML、数据修复、初始化数据、权限 / 配置数据、索引、迁移或回填时逐条列出；不涉及时也必须明确写“无 SQL 执行项 / 不涉及”。
- `$pd-plan` 必须产出 `tech/dependency-readiness.md`：JDK、Node、包管理器、数据库、缓存 / 队列、下游 HTTP 服务、SDK / 开源框架、环境变量 / 凭证、SQL / migration 等开发必需依赖都必须标明状态。
- 真实依赖 Gate：只有 `ready` / `not-required` 允许进入 `$pd-fe` / `$pd-be`；`unknown` / `blocked` / `mock-only` 必须阻断正式开发、联调通过和测试通过。
- 本地真实服务、官方本地容器或测试环境真实服务可算 `ready`；mock server、stub client、fake adapter、contract simulator 必须标为 `mock-only` 并阻断，不算 `ready`。
- 技术实现禁止使用任何 mock：不得规划、实现、提交或验收 mock client、mock server、stub adapter、fake repository、fake downstream、fixture-only 数据流或 contract simulator；发现只能使用 mock 时，必须记录为阻断或实现缺陷，不得继续交付。
- `$pd-fe` 和 `$pd-be` 每次只能执行一个 task slice；单个明确实现缺陷可按对应实现 skill 的修复模式处理，仍须有已有契约 / UI 设计证据及已有实现 slice。独立 UI finding 交给 `$pd-fe` 时统一遵循 [UI finding 修复交接](ui-review-rules.md#6-ui-finding-修复交接)，不另设来源白名单。
- 并行执行时，`$pd-fe` 和 `$pd-be` 只能更新自己负责的 slice 状态。
- `contract` 类型任务只能由 `$pd-plan` 处理，不能由 `$pd-fe` 或 `$pd-be` 单方面修改。
- `$pd-plan` 交付给 `$pd-fe` / `$pd-be` 前，必须把自己创建的 `contract` slice 处理到 `done`，或停止交付并说明缺少的产品 / 设计 / 契约输入；不得把 `pending` / `blocked` 的 `contract` slice 作为实现阶段前置条件交给 `$pd-fe` / `$pd-be`。
- 所有本次相关 `frontend`、`backend`、`shared-frontend`、`shared-backend` slice 完成前，不进入 `$pd-sync` 之后的阶段；缺失实现只允许回到 `$pd-fe` / `$pd-be`。
- `$pd-fe` / `$pd-be` 完成后，下一步只能是继续实现剩余 slice，或在前后端相关 slice 都完成后进入 `$pd-sync`；不得建议直接 `$pd-git`、提交或 PR。
- 开发进度不得依赖联调任务：任何 `frontend`、`backend`、`shared-frontend`、`shared-backend` slice 都不得 `blocked-by SYNC-*`；`SYNC-*` 也不得 `blocks` 任何开发任务。联调后发现的问题只能通过 `$pd-sync` 的 `implementation-defect` / `slice-missing` 路由回实现或计划阶段。
- `$pd-fe` / `$pd-be` 开始任何 slice 前必须检查 `tech/dependency-readiness.md` 中适用该 slice 的依赖；任一必需依赖不是 `ready` / `not-required` 时，必须停止、记录阻断原因，不得把 slice 标为 `done`。
- 前端实现依赖的是 API 契约、前端状态设计、UI 设计系统、前端运行环境和真实 API client 代码路径，不天然依赖后端实现进度。真实后端接口尚未成功返回数据时，前端仍可实现生产路径的真实 HTTP client、loading / empty / error / permission / service-unavailable 状态和 UI 验收；真实成功链路只能留到 `$pd-sync` 验证。
- `tech/dependency-readiness.md` 中“后端真实 API 可用性”默认适用 `SYNC-*` / `test`，不应直接适用 `FE-*`，除非该前端 slice 的目标就是“真实后端验收”。如果只是页面编码或 API client 编码，后端服务未完成不是前端开发阻断。
- 后端实现依赖的是 API 契约、后端设计、数据模型、SQL 执行计划、后端运行环境、真实下游依赖和后端代码路径，不天然依赖前端实现进度。真实前端页面尚未完成时，后端仍可实现接口、服务、权限、错误码、事务、migration、真实下游调用和后端测试；真实页面发起请求的端到端链路只能留到 `$pd-sync` 验证。
- `tech/dependency-readiness.md` 中“前端真实页面可用性”默认适用 `SYNC-*` / `test`，不应直接适用 `BE-*`，除非该后端 slice 的目标就是“真实前端回调 / 页面验收”。如果只是接口、服务或数据实现，前端页面未完成不是后端开发阻断。
- `$pd-fe` / `$pd-be` 不得把任何技术实现路径做成 mock client、stub adapter、fake repository、fake downstream、fixture-only 数据流、demo 数据路径或 contract simulator；需要模拟时只能作为阻断原因记录，不能落到代码或验证证据。
- `$pd-sync` 必须对每个阻断问题输出修复路由：`contract-mismatch` 回 `$pd-plan`，`implementation-defect` 回 `$pd-fe` / `$pd-be` 的缺陷修复模式，`slice-missing` 回 `$pd-plan` 补齐或修正 task slice，`environment-blocked` 留在 `$pd-sync` / 环境准备。
- `$pd-sync` 必须读取 `tech/dependency-readiness.md` 并执行 Mock 禁用检查；发现 `mock-only`、mock/stub/fake/fixture/simulator 或真实依赖未接入时，不得写“联调通过”，不得建议进入 `$pd-test`。
- `$pd-sync` 发现契约不一致时，不得直接修代码，必须生成 `sync/api-mismatch.md` 和 `sync/plan-revision.md` 并回到 `$pd-plan`。
- `$pd-sync` 发现契约正确但实现缺失或运行结果错误时，不得生成方案修订来掩盖实现缺陷；必须在 `sync/integration-report.md` 写明契约证据、实现证据、归属 slice 和下一步 `$pd-fe` / `$pd-be`。
- `$pd-sync` 发现契约正确但 `tech/task-slices.md` 没有任何前端 / 后端 slice 覆盖该实现时，视为 `slice-missing`，必须回 `$pd-plan` 修正切片；不得直接要求 `$pd-fe` / `$pd-be` 新造未计划任务。
- `$pd-sync` 没有明确通过，或未明确标记“不适用并说明原因”时，不进入 `$pd-test` 之后的阶段。
- `$pd-test` 必须读取 `$pd-sync` 的 `sync/integration-report.md`；联调未通过或缺失时，不得把测试结论写成“通过”，不得进入 `$pd-review` 或 `$pd-git`。
- `$pd-test` 必须读取 `tech/dependency-readiness.md` 和 `sync/integration-report.md` 的真实依赖验证；发现 `mock-only`、真实依赖未 ready 或 Mock 禁用检查未通过时，不得把测试结论写成通过。
- `$pd-test` 必须读取 `tech/backend/sql-execution-plan.md`；存在 SQL 执行项时，必须在 `test/test-report.md` 记录测试环境执行状态、验证证据和未执行风险。
- `$pd-test` 未执行验证、验证失败或存在未解释高风险缺口时，不得进入 `$pd-review` 或 `$pd-git`；只能写“未执行 / 失败 / 需人工验证 / 有残余风险”并回到对应修复阶段。
- `$pd-review` 必须在 `$pd-sync` 和 `$pd-test` 之后执行；发现 P0/P1、联调未通过、测试未通过或证据缺失时，不进入 `$pd-git`，先回到对应实现、联调、测试或方案 skill。
- `$pd-git` 只能在 commit readiness gate 全部通过后准备提交：相关实现 slice 已完成、`sync/integration-report.md` 明确通过或明确不适用、`test/test-report.md` 明确通过、`test/code-review.md` 无 P0/P1、提交范围检查无未解决漏提 / 多提风险。
- `$pd-release` 必须读取 `sync/integration-report.md`、`test/test-report.md`、`test/code-review.md` 和 `tech/backend/sql-execution-plan.md`；SQL 执行项未验证、执行顺序不清或回滚方案缺失时不得声称可以上线。

## 8. Task Slice 规则

`tech/task-slices.md` 的任务优先级：

```text
P0: 阻断主流程，必须先做
P1: 核心功能，必须做
P2: 增强或补充，可后做
```

任务类型：

```text
frontend
backend
contract
shared-frontend
shared-backend
sync
test
```

任务状态：

```text
pending
in_progress
done
blocked
```

并行标记只表达任务调度属性，不表达任务依赖：

```text
parallel-safe
serial
stage-gate
```

- `parallel-safe`：可与没有直接依赖关系的同阶段任务并行。
- `serial`：必须按 `blocked-by` / `blocks` 依赖顺序串行推进。
- `stage-gate`：阶段门或验收门，通常用于 `sync` / `test` / `review` 等门禁任务。
- “并行标记”列禁止出现任务 ID，禁止写入 `blocked-by XXX`、`blocks XXX`、`blocked-by SYNC-001` 等依赖内容。

依赖列是独立列，不属于并行标记：

```text
blocked-by
blocks
```

- 所有任务 ID 依赖只能写入 `blocked-by` 或 `blocks` 列。
- `-` 表示无依赖，不得和任务 ID 混用。
- 如果 `A.blocked-by` 包含 `B`，则 `B.blocks` 必须包含 `A`。
- 如果 `B.blocks` 包含 `A`，则 `A.blocked-by` 必须包含 `B`。
- 不允许只在 `blocks` 单边声明、但对方 `blocked-by` 缺失；也不允许只在 `blocked-by` 单边声明、但对方 `blocks` 缺失。
- 生成 `tech/task-slices.md` 后必须做依赖闭环自检，先修正单边依赖和错误列内容，再输出最终结果。

`contract` 表示同时影响前后端的契约类任务，例如 API 字段、错误码、权限、状态枚举、数据模型、分页结构和真实依赖边界；不得把 mock 数据结构作为契约交付。

### Frontend / Backend 双向依赖建模规则

- 前端实现任务默认不依赖后端实现任务。`FE-*` 应基于 `tech/api-contract.md`、`tech/frontend/frontend-state-api.md`、UI 设计系统、Figma handoff 和前端运行依赖实现页面、状态、真实 API client 和错误处理。
- 真实后端未完成、真实数据暂不可用或端到端链路未通过，是 `SYNC-*` / `test` 的阶段门，不是普通 `frontend` slice 的开发前置。
- `FE-* blocked-by BE-*` 只允许用于后端先产出前端编码必须消费的具体工程产物：OpenAPI generated client、共享 SDK、提交到仓库的 schema / type 文件、认证 / 权限中间件适配文件等。任务描述或验证列必须写明产物路径和原因。
- 如果前端只需要调用契约里的 API，或只是在等待真实后端成功响应，不允许让 `FE-*` 依赖 `BE-*`；应让 `FE-*` 与 `BE-*` 并行实现，并让二者共同阻塞对应 `SYNC-*`。
- 如果现有切片把前端实现绑到后端真实能力完成上，必须回 `$pd-plan` 修正：拆成前端实现先做、后端实现并行、真实联调验收后做。
- 前端不得用 mock 成功数据绕过后端未完成；后端未完成时只能验证真实 client 路径、失败态、空态、配置缺失态、服务不可用态和本地 UI / 构建 / 组件行为。
- 后端实现任务默认不依赖前端实现任务。`BE-*` 应基于 `tech/api-contract.md`、`tech/backend/backend-design.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md` 和真实依赖准备实现接口、服务、权限、错误码、事务、migration 和真实下游调用。
- 真实前端未完成、真实页面暂不可用或浏览器链路未通过，是 `SYNC-*` / `test` 的阶段门，不是普通 `backend` slice 的开发前置。
- `BE-* blocked-by FE-*` 只允许用于前端先产出后端编码必须消费的具体工程产物：共享 schema / type 包、提交到仓库的回调 payload fixture、必须用于后端测试的契约样例文件等。任务描述或验证列必须写明产物路径和原因。
- 如果后端只需要按契约实现 API，或只是在等待前端页面发起真实请求，不允许让 `BE-*` 依赖 `FE-*`；应让 `BE-*` 与 `FE-*` 并行实现，并让二者共同阻塞对应 `SYNC-*`。
- 如果现有切片把后端实现绑到前端页面完成上，必须回 `$pd-plan` 修正：拆成后端实现先做、前端实现并行、真实联调验收后做。
- 后端不得用 fake frontend request 或 fixture-only 成功路径冒充端到端通过；前端未完成时只能验证接口契约、service / repository、权限、错误码、真实下游、数据库和后端测试。

### SYNC Slice 建模规则

- `SYNC-*` 只能表示前后端真实联调阶段门，必须等待相关 `frontend`、`backend`、`shared-frontend`、`shared-backend` slice 全部 `done` 后执行。
- 开发任务不得依赖 SYNC-*：`frontend` / `backend` / `shared-*` slice 的 `blocked-by` 禁止包含 `SYNC-*`。
- `SYNC-*` 不得阻塞开发任务；`SYNC-*` 的 `blocks` 禁止包含 `FE-*`、`BE-*` 或 `shared-*`，只允许指向 `test` 或后续非开发门禁任务，或写 `-`。
- 联调发现的实现问题不预建为 `blocked-by SYNC-*` 的开发任务；由 `$pd-sync` 写成 `implementation-defect`，回 `$pd-fe` / `$pd-be` 缺陷修复模式。若没有已有实现 slice 覆盖，则写成 `slice-missing` 回 `$pd-plan`。
- `SYNC-*` 的 `blocked-by` 应包含它要联调的所有前后端实现任务。
- `SYNC-*` 不应替代具体技术依赖；如果开发任务只需要某个后端或前端 slice，就依赖对应 `BE-*` / `FE-*`，不是依赖 `SYNC-*`。
- `SYNC-*` 的验证列必须说明联调范围和通过条件。

### Contract Slice 交付规则

- `contract` slice 是 `$pd-plan` 的设计 / 契约确认项，不是代码实现项。它的验证证据应指向 `tech/api-contract.md`、`tech/backend/data-model.md`、`tech/integration-map.md`、`tech/frontend/frontend-state-api.md`、`tech/tech-plan.md` 等技术设计产物。
- `$pd-plan` 输出完成时，`tech/task-slices.md` 中不得存在 `pending`、`in_progress` 或 `blocked` 状态的 `contract` slice。若契约无法完成，`$pd-plan` 必须停止并提示回到上游 skill 或补充信息。
- 不要把工程初始化、目录创建、依赖安装、Spring Boot / Vite 脚手架、`.env.example`、数据库迁移文件、真实 API client 等需要改代码或文件的实现动作写成 `contract` slice。按实际归属拆成 `frontend`、`backend`、`shared-frontend` 或 `shared-backend`；mock server / mock client / stub / fake / simulator 只能作为阻断原因记录，不得成为实现动作。
- 如果某个实现动作依赖共享契约，使用“两段式”切片：一个 `contract` slice 标记为 `done` 以确认契约，一个或多个实现 slice 保持 `pending` 由 `$pd-fe` / `$pd-be` 执行。
- `$pd-fe` / `$pd-be` 选择 slice 时，只能执行自身类型且所有 `blocked-by` 已为 `done` 的 slice；若发现唯一阻塞是未完成 `contract` slice，应报告 `$pd-plan` handoff 问题，而不是自行修改契约。
- 缺陷修复例外：按对应实现 skill 核对原 finding 的 `implementation-defect` 分类、契约 / UI 设计证据、实现证据及已有实现 slice 后，可临时重开该 slice 或记录同 slice 修复，不需要先回 `$pd-plan` 新增 pending slice。独立 UI finding 到 `$pd-fe` 的交接沿用 [共享规则](ui-review-rules.md#6-ui-finding-修复交接)，不另枚举报告来源。
- 如果 finding 没有归属 slice、归属为 `slice-missing`，或需要新增 / 修改 API 契约、数据模型、状态枚举、权限规则、页面路由或任务范围，必须回 `$pd-plan`；实现 skill 不得自行扩展范围。

## 9. Review 严重级别

`$pd-review` 输出的问题必须使用：

```text
P0: 阻断发布
P1: 必须修复
P2: 建议修复
P3: 可选优化
```

UI 采用同一套 P0/P1/P2/P3，用户影响、证据不足及残余风险的判断统一见 [UI Review Rules](ui-review-rules.md)，不在各阶段重复维护定义。

## 10. Git 与发布边界

- `$pd-git` 默认只准备 commit / PR 文案。
- 用户明确要求时，`$pd-git` 可执行 `git add` 和 `git commit`。
- 执行 `git add` 前必须展示 planned files、excluded files、possible missing files、possible extra files 和 staged 差异，并排除明显无关文件。
- 提交前必须检查 `.gitignore` / ignored / untracked 状态；构建产物、缓存、日志、截图、临时报告和历史 benchmark run 默认不提交。
- 不使用 `git add -A`、`git add .` 或通配符扩大提交范围；只逐个 add 已确认的 planned files。
- staged 文件与 planned files 不一致时，不继续提交，先说明差异并等待确认。
- 有未解决 P0/P1、失败测试或未解释的契约差异时，不建议提交。
- 默认不 push，除非用户明确要求。
- `$pd-release` 只生成通用 Markdown 上线文档，不接平台、不部署。
