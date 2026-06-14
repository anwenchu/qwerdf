# Codex Product Delivery 规则

本文件是所有 `$pd-*` skill 的共享规则源。它们是独立的开源 Codex Product Delivery Skills，不绑定任何外部变更生命周期，不参与外部研发流程状态流转。

产品和设计阶段模板见 [artifact-contracts.md](artifact-contracts.md)。工程阶段模板见 [engineering-contracts.md](engineering-contracts.md)。
UI 设计系统和质量规则见 [ui-design-system.md](ui-design-system.md)、[ui-quality-checklist.md](ui-quality-checklist.md)、[ui-patterns.md](ui-patterns.md)、[ui-review-rules.md](ui-review-rules.md)。

## 1. 交付链路

```text
$pd-vet -> $pd-prd -> $pd-blueprint -> $pd-figma -> $pd-plan -> $pd-fe + $pd-be -> $pd-sync -> $pd-test -> $pd-review -> $pd-git -> $pd-release
```

| 阶段 | 负责 Skill | 必要产物 |
| --- | --- | --- |
| 想法验证 | `$pd-vet` | `product/idea-brief.md`、`product/user-problem.md`、`product/competitor-notes.md`、`product/mvp-hypothesis.md`、`product/validation-questions.md` |
| PRD 生成 | `$pd-prd` | `product/prd.md`、`product/requirements.md`、`product/user-stories.md`、`product/acceptance-criteria.md`、`product/open-questions.md` |
| 产品设计输入 | `$pd-blueprint` | `product/product-brief.md` |
| UI 页面蓝图 | `$pd-blueprint` | `ui/ui-design-system.md`、`ui/ui-flows.md`、`ui/ui-pages.md`、`ui/ui-screens.md`、`ui/ui-components.md` |
| Figma 设计交付 | `$pd-figma` | `ui/ui-design-system.md`、`ui/ui-directions.md`、`ui/figma-handoff.md` |
| 技术设计 | `$pd-plan` | `tech/tech-plan.md`、`tech/frontend/frontend-design.md`、`tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md`、`tech/frontend/frontend-state-api.md`、`tech/backend/backend-design.md`、`tech/api-contract.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md`、`tech/integration-map.md`、`tech/task-slices.md`、`tech/risk-plan.md` |
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
  tech/
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
- 修改 skill 描述、触发词或阶段边界后，检查 `evals/trigger-queries.json`，确保 should-trigger 和 should-not-trigger 样例仍然成立。

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
- `$pd-plan` 必须把 `ui/ui-design-system.md` 和 `ui/figma-handoff.md` 转成前端技术约束：组件复用、状态覆盖、响应式、可访问性、表单校验、错误映射、空态和 UI 验收方式。
- `$pd-fe` 必须读取 `ui/ui-design-system.md` 和 UI 质量清单后实现；完成后在 `tech/frontend/frontend-acceptance.md` 记录桌面 / 移动端、无横向溢出、文本不重叠、按钮 / 表单状态、loading / empty / error / permission / saving 状态和证据。
- `$pd-review` 涉及 UI diff 时必须执行 UI Review：检查设计系统一致性、产品类型匹配、信息层级、响应式、可访问性、状态覆盖、表单 / 表格 / 图表质量，并按 P0/P1/P2/P3 输出带证据的 finding。
- SaaS / CRM / 管理后台 / 操作台类产品默认采用克制、密集、可扫描、效率优先的界面方向；不要把 landing page hero、过度卡片化、装饰性插画或大面积氛围图带入操作型产品，除非 PRD 明确要求营销页面。

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

- `$pd-plan` 完成前，不允许进入 `$pd-fe` 或 `$pd-be`。
- `$pd-fe` 和 `$pd-be` 必须基于同一份 `tech/task-slices.md`、`tech/api-contract.md` 和 `tech/integration-map.md`。
- `$pd-fe` 必须基于同一份 `ui/ui-design-system.md`、`ui/figma-handoff.md` 和 `tech/frontend/frontend-design.md`；设计系统缺失、冲突或未转成前端约束时，先回到 `$pd-figma` 或 `$pd-plan`。
- `$pd-plan` 必须产出 `tech/backend/sql-execution-plan.md`：涉及 DDL、DML、数据修复、初始化数据、权限 / 配置数据、索引、迁移或回填时逐条列出；不涉及时也必须明确写“无 SQL 执行项 / 不涉及”。
- `$pd-fe` 和 `$pd-be` 每次只能执行一个 task slice。
- 并行执行时，`$pd-fe` 和 `$pd-be` 只能更新自己负责的 slice 状态。
- `contract` 类型任务只能由 `$pd-plan` 处理，不能由 `$pd-fe` 或 `$pd-be` 单方面修改。
- `$pd-plan` 交付给 `$pd-fe` / `$pd-be` 前，必须把自己创建的 `contract` slice 处理到 `done`，或停止交付并说明缺少的产品 / 设计 / 契约输入；不得把 `pending` / `blocked` 的 `contract` slice 作为实现阶段前置条件交给 `$pd-fe` / `$pd-be`。
- 所有本次相关 `frontend`、`backend`、`shared-frontend`、`shared-backend` slice 完成前，不进入 `$pd-sync` 之后的阶段；缺失实现只允许回到 `$pd-fe` / `$pd-be`。
- `$pd-fe` / `$pd-be` 完成后，下一步只能是继续实现剩余 slice，或在前后端相关 slice 都完成后进入 `$pd-sync`；不得建议直接 `$pd-git`、提交或 PR。
- `$pd-sync` 发现契约不一致时，不得直接修代码，必须先生成 `sync/plan-revision.md` 并回到 `$pd-plan`；发现实现问题时回到 `$pd-fe` / `$pd-be`。
- `$pd-sync` 没有明确通过，或未明确标记“不适用并说明原因”时，不进入 `$pd-test` 之后的阶段。
- `$pd-test` 必须读取 `$pd-sync` 的 `sync/integration-report.md`；联调未通过或缺失时，不得把测试结论写成“通过”，不得进入 `$pd-review` 或 `$pd-git`。
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

`contract` 表示同时影响前后端的契约类任务，例如 API 字段、错误码、权限、状态枚举、数据模型、分页结构、mock 数据结构。

### SYNC Slice 建模规则

- `frontend` / `backend` 开发任务默认依赖具体的 `C-*`、`FE-*`、`BE-*` 前置任务，不要为了流程整齐统一依赖 `SYNC-*`。
- 只有当后续开发必须基于“已通过真实前后端联调的契约、字段、数据、错误码或端到端行为”时，开发任务才允许在 `blocked-by` 中依赖 `SYNC-*`。
- 如果 `SYNC-*` 只是验证建议，不应阻塞开发任务；应写入“验证”列或任务说明中的并行建议，不要写入 `blocked-by`。
- 如果 `SYNC-*` 是阶段门，必须在任务描述、验证列或并行建议中说明理由，例如：`依赖配置域真实 API 差异关闭后才能进入任务域真实 API 开发`。
- `SYNC-*` 的 `blocked-by` 应包含它要联调的所有前后端实现任务。
- `SYNC-*` 的 `blocks` 只应包含确实需要联调结果作为阶段门的后续任务。
- `SYNC-*` 不应替代具体技术依赖；如果后续任务只需要某个后端或前端 slice，就依赖对应 `BE-*` / `FE-*`。
- `SYNC-*` 的验证列必须说明联调范围和通过条件。

### Contract Slice 交付规则

- `contract` slice 是 `$pd-plan` 的设计 / 契约确认项，不是代码实现项。它的验证证据应指向 `tech/api-contract.md`、`tech/backend/data-model.md`、`tech/integration-map.md`、`tech/frontend/frontend-state-api.md`、`tech/tech-plan.md` 等技术设计产物。
- `$pd-plan` 输出完成时，`tech/task-slices.md` 中不得存在 `pending`、`in_progress` 或 `blocked` 状态的 `contract` slice。若契约无法完成，`$pd-plan` 必须停止并提示回到上游 skill 或补充信息。
- 不要把工程初始化、目录创建、依赖安装、Spring Boot / Vite 脚手架、`.env.example`、数据库迁移文件、mock server / API client 等需要改代码或文件的实现动作写成 `contract` slice。按实际归属拆成 `frontend`、`backend`、`shared-frontend` 或 `shared-backend`。
- 如果某个实现动作依赖共享契约，使用“两段式”切片：一个 `contract` slice 标记为 `done` 以确认契约，一个或多个实现 slice 保持 `pending` 由 `$pd-fe` / `$pd-be` 执行。
- `$pd-fe` / `$pd-be` 选择 slice 时，只能执行自身类型且所有 `blocked-by` 已为 `done` 的 slice；若发现唯一阻塞是未完成 `contract` slice，应报告 `$pd-plan` handoff 问题，而不是自行修改契约。

## 9. Review 严重级别

`$pd-review` 输出的问题必须使用：

```text
P0: 阻断发布
P1: 必须修复
P2: 建议修复
P3: 可选优化
```

UI 严重级别按同一套 P0/P1/P2/P3 处理：

- `P0`: 核心 UI 流程不可用、关键页面白屏、主操作被遮挡、移动端核心流程无法操作。
- `P1`: 关键状态缺失、严重设计系统漂移、移动端严重横向溢出、表单错误无法定位、图表或视觉层级误导主流程。
- `P2`: 边界状态缺失、局部响应式问题、非核心信息层级不清、可维护性下降或测试 / 截图证据不足。
- `P3`: 不阻断的命名、局部间距、文案一致性或轻量视觉修正。

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
