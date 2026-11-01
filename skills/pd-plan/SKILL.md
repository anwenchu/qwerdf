---
name: pd-plan
description: >-
  技术设计工作流，基于 PRD、产品设计输入、UI 设计系统、UI 蓝图、Figma handoff 和现有代码库产出前端设计、后端设计、API 契约、真实依赖准备清单、数据模型、SQL 执行计划、前后端一致性映射、任务切片和风险方案。Use when the user mentions $pd-plan、pd-plan、技术设计、技术方案、前后端设计、接口契约、任务切片、依赖准备、SQL执行计划、数据库迁移计划、UI技术设计。
---

# $pd-plan — 技术设计

Codex Product Delivery Skill：把产品和设计产物串成前后端一致、可并行开发的工程方案。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `tech/tech-plan.md`、`tech/dependency-readiness.md`、`tech/frontend/frontend-design.md`、`tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md`、`tech/frontend/frontend-state-api.md`、`tech/backend/backend-design.md`、`tech/api-contract.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md`、`tech/integration-map.md`、`tech/task-slices.md`、`tech/risk-plan.md` 的模板。
3. 读取 [UI Design System Rules](../qwerdf-common/ui-design-system.md) 和 [UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)。
   技术依据、范围控制和交接判断读取 [技术设计依据与范围规则](../qwerdf-common/technical-design-rules.md)。
4. 读取 `product/prd.md`、`product/requirements.md`、`product/product-brief.md`、`ui/ui-design-system.md`、`ui/ui-screens.md`、`ui/ui-components.md`、`ui/figma-handoff.md`。
5. 先按本期业务链路限定扫描问题和停止边界，再读取相关前后端入口、API client、契约 / 提供方实现、路由、数据模型、权限、实际依赖版本 / 配置及测试结构；只读影响核查不自动扩成改造范围。
   涉及 Java 持久化设计时，按 [共享持久化规则](../qwerdf-common/java-coding-rules.md#spring-事务与持久化涉及数据库时) 明确数据访问方式、Mapper / XML 归属及事务边界，不把未确定的持久化选型留给实现阶段。
6. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 不写代码。
- 不提交代码。
- 不改 PRD 或 Figma。
- 设计检查与实施交接按 [共享交接规则](../qwerdf-common/technical-design-rules.md#3-交付应足以让实现者执行) 执行：只要求检查时只读报告；已授权修订时同步更新旧结论及受影响任务，不能仅补缺口附件后继续沿用“设计完成”。
- 关键接入不明确或决定性依据缺失时，按共享技术设计规则报告草案 / 受影响部分待补，不仅凭文件齐全宣称完成；范围外发现不自动进入本期改动或 task slices。
- 不让 `$pd-fe` 或 `$pd-be` 单方面处理 `contract` 类型任务。
- 发现漏项或“不清楚”时，先按 [共享分类规则](../qwerdf-common/technical-design-rules.md#工程漏项与业务决策分类) 补查：范围内有依据的工程漏项在本阶段补齐设计，不重复问已确认业务要求；真正的业务未决 / 范围变化才定向澄清，必要时回 `$pd-prd`、`$pd-blueprint` 或 `$pd-figma`，不将内部技术修订当成新的用户审批。
- Figma handoff 是表现层输入，不是产品事实源；如果它新增了 PRD、product-brief 或 UI 蓝图中不存在的页面、导航、资产类型、业务模块或文案，先记录冲突并停止，不下推到技术设计。
- `ui/ui-design-system.md` 是 UI 事实源；如果缺失、与 Figma handoff 冲突或没有说明 `MASTER` / `Page Overrides`，先记录缺口并回到 `$pd-blueprint` / `$pd-figma`。

## 规则优先级

| 优先级 | 类别 | 设计重点 |
| --- | --- | --- |
| 1 | 契约一致性 | API、字段、状态、权限、错误码、分页和真实依赖必须先对齐；技术实现禁止使用任何 mock |
| 2 | 数据与权限 | 数据模型、可见性、幂等、事务和越权风险必须可验证 |
| 3 | 前端架构 | 路由、组件、状态、API client 和设计还原路径要可落地 |
| 4 | UI 工程约束 | 设计系统、状态覆盖、响应式、可访问性、表单校验、错误映射和空态必须进入前端设计 |
| 5 | 后端架构 | controller / service / repository 边界、错误处理和观测要清楚 |
| 6 | 性能与可维护性 | 避免不必要 waterfalls、重复请求、过宽 bundle、布尔 prop 膨胀和隐式耦合 |
| 7 | 真实依赖准备 | JDK、Node、数据库、下游 HTTP、SDK、环境变量、凭证和 SQL / migration 必须有 ready 证据 |
| 8 | 发布风险 | 回滚、灰度、监控、测试缺口和人工确认项必须被记录 |

## Task Slice 防呆

- `contract` slice 只用于确认 API 字段、错误码、权限、状态枚举、数据模型、分页结构和真实依赖边界等共享契约；不得把 mock 数据结构设计成实现契约。
- `tech/backend/sql-execution-plan.md` 是 SQL / migration 交接清单，`$pd-plan` 每次都必须产出；没有 SQL 执行项时也必须明确写“无 SQL 执行项 / 不涉及”。
- `tech/dependency-readiness.md` 是正式开发前置 gate，`$pd-plan` 每次都必须产出；没有外部依赖时也必须列出 JDK / Node / 包管理器 / 数据库等基础依赖为 `ready` 或 `not-required`。
- 依赖状态只允许 `ready`、`not-required`、`blocked`、`unknown`、`mock-only`；适用于目标 slice 的必需依赖只有 `ready` / `not-required` 才允许其进入 `$pd-fe` / `$pd-be`，`mock-only` 只能作为阻断信号。
- 本地真实服务、官方本地容器或测试环境真实服务可算 `ready`；mock server、stub client、fake adapter、contract simulator 必须标为 `mock-only` 并阻断交付，不得作为设计、开发、联调或测试通过证据。
- 只要涉及 DDL、DML、数据修复、初始化数据、权限 / 配置数据、索引、迁移、回填或不可逆数据操作，必须在 `tech/backend/sql-execution-plan.md` 逐条记录 SQL / migration 文件、执行环境、执行时机、执行顺序、验证方式、回滚方案和风险。
- 不允许只在 `tech/backend/data-model.md` 或 `tech/risk-plan.md` 泛泛描述数据变更；需要执行的 SQL 必须进入 `tech/backend/sql-execution-plan.md`，供 `$pd-test` 和 `$pd-release` 读取。
- `$pd-plan` 完成时，本轮交接范围内所有 `contract` slice 必须已经由当前技术设计产物证明并标记为 `done`；不能把 `pending` / `blocked` 的 `contract` slice 留给 `$pd-fe` 或 `$pd-be`。分期范围按共享交接规则确定。
- 工程初始化、目录结构落地、依赖安装、Spring Boot / Vite 脚手架、环境变量模板文件、Flyway 迁移文件、真实 API client 等需要改代码或文件的动作，必须拆成 `frontend`、`backend`、`shared-frontend` 或 `shared-backend` slice；mock server、mock adapter、stub client、fake repository、fake data source、contract simulator 不得写入技术实现任务，只能作为阻断原因记录。
- `并行标记` 只表达调度属性，只允许 `parallel-safe`、`serial`、`stage-gate`；禁止写入任务 ID，禁止出现 `blocked-by XXX`、`blocks XXX`、`blocked-by SYNC-001` 等依赖内容。
- `blocked-by` 和 `blocks` 是独立依赖列，不属于并行标记；所有任务 ID 依赖只能写入这两列，`-` 表示无依赖且不得和任务 ID 混用。
- 依赖必须双向闭环：如果 `A.blocked-by` 包含 `B`，则 `B.blocks` 必须包含 `A`；如果 `B.blocks` 包含 `A`，则 `A.blocked-by` 必须包含 `B`。
- 开发任务只关联已确认契约、本端真正的前置任务或必要工程准备产物；按共享并行规则建模，不为流程整齐增加对端或 `SYNC-*` 依赖。
- 前端实现默认依赖已确认契约、前端设计和本端真实工程前置；后端实现默认依赖已确认契约、后端设计和本端真实工程前置。两端业务实现并行，具体依赖与共享产物边界统一按 [Frontend / Backend 并行开发规则](../qwerdf-common/product-delivery-flow.md#frontend--backend-并行开发规则) 建模，不另设相互等待的例外。
- `SYNC-*` 是严格的联调阶段门，只能在相关 `frontend`、`backend`、`shared-frontend`、`shared-backend` 实现 slice 全部 `done` 后执行。
- 开发任务不得依赖 `SYNC-*`：任何 `frontend` / `backend` / `shared-*` slice 的 `blocked-by` 都禁止包含 `SYNC-*`；任何 `SYNC-*` 的 `blocks` 都禁止包含 `FE-*`、`BE-*` 或 `shared-*` 开发任务。
- 如果后续发现必须基于联调结果修代码，不要预先创建 `blocked-by SYNC-*` 的开发任务；应由 `$pd-sync` 输出 `implementation-defect`，再让 `$pd-fe` / `$pd-be` 以缺陷修复模式重开已有 slice，或以 `slice-missing` 回 `$pd-plan` 补齐切片。
- `SYNC-*` 的 `blocked-by` 必须包含它要联调的所有前后端实现任务；`blocks` 只允许指向 `test` 或后续非开发门禁任务，或写 `-`；验证列必须说明联调范围和通过条件。
- 每个 `frontend` / `backend` / `shared-*` slice 的验证列必须引用对应依赖准备状态，例如 `依赖准备：JDK ready、DB ready、Dify API ready`；若依赖是 `unknown` / `blocked` / `mock-only`，该 slice 不得交付给开发，验证列也不得把 mock / stub / fake / fixture / simulator 作为通过证据。
- 前端 UI slice 的验证列必须包含 UI 质量验收要求，例如设计系统一致性、目标平台、无横向溢出、文本不重叠、适用状态及截图 / 浏览器证据；状态按 [共享质量清单](../qwerdf-common/ui-quality-checklist.md#4-适用的状态与交互) 判断，不适用写明理由，不另列全量必检状态。
- 首次上线 / 空仓库场景使用以下模式：
  - `C-001`: `contract` / `done` / 确认工程基线契约，验证指向 `tech/tech-plan.md`、`tech/api-contract.md`、`tech/backend/data-model.md`、`tech/integration-map.md`。
  - `FE-001`: `frontend` / `pending` / 创建前端工程骨架并验证构建。
  - `BE-001`: `backend` / `pending` / 创建后端工程骨架并验证健康检查。
- 如果某个契约仍无法确认，停止受影响范围的正式交接并说明缺口，保留已确认的设计记录；不要生成看似可执行但缺少关键契约的任务，或把未决契约伪标为 `done`。

## 流程

仅检查已有设计时，按共享交接规则核查现有产物并输出发现及交接判断；以下产出步骤用于设计 / 修订，不因检查而重写文件或补造整套材料。

1. 先确认 PRD、产品设计输入、`ui/ui-design-system.md`、UI 蓝图和 Figma handoff 足够支撑工程设计。
2. 对照产品事实源和 `ui/ui-design-system.md` 检查 Figma handoff：若发现范围外页面、导航、资产类型、业务模块、交易品类、参考产品文案或设计系统漂移，写入冲突说明并停止。
3. 产出 `tech/tech-plan.md`，关联本期需求与必要技术前置，区分改动和影响核查范围；按共享规则记录关键结论依据、设计提案、未决项及其影响，再明确现有系统影响、实施顺序和风险。
4. 分别产出 `tech/frontend/frontend-design.md` 和 `tech/backend/backend-design.md`；前端设计必须包含 UI 设计系统约束、响应式、可访问性、表单校验、错误映射、空态和 UI 验收方式。
5. 产出 `tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md` 和 `tech/frontend/frontend-state-api.md`，把 Figma / UI 蓝图 / design system 映射到前端组件、路由、状态、API client、page override 和状态覆盖。
6. 产出 `tech/api-contract.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md` 和 `tech/integration-map.md`，串通前端字段、后端字段、状态、错误码、权限、分页、真实依赖和 SQL / migration 执行要求；关键服务接入、参数来源、取值语义、顺序和失败路径在对应设计段落写清并关联依据。区分既有能力与拟新增设计，不得产出 mock 契约、mock 数据结构或 mock 实现方案。
7. 产出 `tech/dependency-readiness.md`，扫描并列出 JDK、Node、包管理器、数据库、缓存 / 队列、下游 HTTP 服务、SDK / 开源框架、环境变量 / 凭证、SQL / migration 等本次开发依赖；每项必须写适用 slice、真实资源 / 地址、验证命令、状态、证据、阻断原因和下一步。
8. 按 [共享业务推进规则](../qwerdf-common/product-delivery-flow.md#业务推进阻断恢复与进度汇报) 在实施顺序中组织本期业务里程碑，再产出 `tech/task-slices.md`；任务说明引用对应里程碑 / 验收，每个 slice 保留优先级、类型、状态、并行标记、依赖、阻塞关系、依赖准备引用和验证方式，不用任务数量代替业务闭环。
9. 按共享交接规则核对本轮验收及关联设计，再对 `tech/task-slices.md` 和 `tech/dependency-readiness.md` 做 handoff 自检；若发现问题，先修正再输出最终技术设计结果（仅检查模式报告问题，不直接改文件）：
   - 先按共享技术设计规则走通本期关键链路，检查接口 / 数据映射的依据及决定性未决项；逐项核对任务、SQL 和依赖改动是否属于确认范围或必要前置。只读影响发现和未授权的一般建议不得变成本期任务。
   - 对开放问题按共享分类规则核对是否已补查、是否确需用户提供信息或决定业务取舍；有依据的工程漏项由设计补齐，不留给开发猜测。身份参数须串查采集、传递、下游实际消费与返回处理，不能只因新增字段就宣布缺口已闭合。
   - 检查“并行标记”列是否合法，是否误写了 `blocked-by`、`blocks` 或任务 ID。
   - 检查所有 `blocked-by` / `blocks` 是否双向一致，不允许单边声明。
   - 检查是否存在任何 `frontend` / `backend` / `shared-*` 开发任务 `blocked-by SYNC-*`；若存在，删除该依赖，改为并行实现并让相关实现任务共同阻塞 `SYNC-*`。
   - 检查是否存在任何 `SYNC-* blocks FE-* / BE-* / shared-*`；若存在，删除该反向开发阻塞，必要时把联调后修复写成 `$pd-sync` finding 路由规则，而不是预建开发任务。
   - 按共享并行规则检查 `FE-* blocked-by BE-*`、`BE-* blocked-by FE-*` 及任务实际类型，消除前后端业务实现之间的相互等待；真实后端未完成、真实前端未完成仅作为对应联调 / 测试前置。确需共享产物时拆出最小工程准备任务，并同步依赖清单与验证列，不能通过改名或保留环境阻断变相串行。
   - 检查 `SYNC-*` 的 `blocked-by` 是否覆盖它要联调的所有前后端实现任务，且这些实现任务在联调执行前必须为 `done`；`blocks` 是否只包含 `test` 或后续非开发门禁任务，验证列是否说明联调范围和通过条件。
   - 检查本轮交接范围内所有 `contract` slice 是否由当前设计支持且为 `done`，并且没有把代码实现动作误归为 `contract`。
   - 按共享业务推进规则核对里程碑是否可按已确认验收走通、必要安全与依赖是否随链路覆盖、任务顺序是否持续推进业务结果；决定性口径缺失不能留到开发后再解释，已有局部修复不强制重建全量里程碑。
   - 检查前端 UI slice 是否包含 UI 质量验收要求；不得只写“实现页面”而缺少设计系统、状态、响应式或浏览器验证。
   - 检查是否生成 `tech/backend/sql-execution-plan.md`；涉及 SQL / migration 时执行清单、顺序、验证、回滚和风险不得为空；不涉及时必须明确写“不涉及”。
   - 检查是否生成 `tech/dependency-readiness.md`；拟交接开发 slice 的必需依赖必须为 `ready` / `not-required`，不得用 `mock-only` 作为 ready 证据；后续验证 / 发布阶段的依赖不混作当前编码前置。
   - 检查每个开发 slice 的验证列是否引用对应依赖准备项；按共享并行规则逐个判断拟执行 slice 的必要依赖，只有该 slice 存在 `unknown` / `blocked` / `mock-only` 时才阻断其开发。消费者等待共享产物，不阻断条件已具备的产物准备任务或其他独立任务；但不能借此放过本轮交接范围内的决定性契约缺口。
   - 检查技术实现任务、验证方式和开发说明中是否出现 mock client / mock server / stub / fake / fixture / simulator；出现时必须改为真实依赖方案或阻断说明。
10. 产出 `tech/risk-plan.md`。
11. 在 `tech/tech-plan.md` 更新交接结论；仅检查时报告当前结论是否仍成立及需修订位置。摘要分别说明本轮设计是否可交接、适用依赖是否就绪和未执行验证，再决定下一步：只检查不启动开发；已授权后续开发时也须本轮约定设计范围可交接、目标 slice 必需依赖为 `ready` / `not-required` 才执行对应 `$pd-fe` / `$pd-be`，否则停在补设计或准备依赖，不伪称全部完成。

## 输出摘要

```text
技术设计状态: <name；本轮范围可交接 / 部分待补 / 阻断，说明依据>
目录: <output-dir>
文件:
  - tech/tech-plan.md
  - tech/dependency-readiness.md
  - tech/frontend/frontend-design.md
  - tech/frontend/frontend-component-map.md
  - tech/frontend/frontend-route-map.md
  - tech/frontend/frontend-state-api.md
  - tech/backend/backend-design.md
  - tech/api-contract.md
  - tech/backend/data-model.md
  - tech/backend/sql-execution-plan.md
  - tech/integration-map.md
  - tech/task-slices.md
  - tech/risk-plan.md

设计依据与未决项: <关键链路定位 / 决定性缺口及受影响范围>
依赖与验证状态: <适用 slice 的依赖准备引用；尚未执行的实现 / 运行验证>
范围核对: <本期改动；仅作影响记录的范围外发现；待确认变化>
下一步: <仅检查时报告修订建议；已有实现授权且设计与依赖 gate 通过才执行对应 slice，否则先补设计或准备依赖>
```
