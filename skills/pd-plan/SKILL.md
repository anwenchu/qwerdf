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
4. 读取 `product/prd.md`、`product/requirements.md`、`product/product-brief.md`、`ui/ui-design-system.md`、`ui/ui-screens.md`、`ui/ui-components.md`、`ui/figma-handoff.md`。
5. 扫描现有代码库的前端、后端、API client、路由、数据模型、权限和测试结构。
6. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 不写代码。
- 不提交代码。
- 不改 PRD 或 Figma。
- 不让 `$pd-fe` 或 `$pd-be` 单方面处理 `contract` 类型任务。
- 发现需求不清时，停止并提示回到 `$pd-prd`、`$pd-blueprint` 或 `$pd-figma`。
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
- 依赖状态只允许 `ready`、`not-required`、`blocked`、`unknown`、`mock-only`；只有 `ready` / `not-required` 允许进入 `$pd-fe` / `$pd-be`，`mock-only` 只能作为阻断信号。
- 本地真实服务、官方本地容器或测试环境真实服务可算 `ready`；mock server、stub client、fake adapter、contract simulator 必须标为 `mock-only` 并阻断交付，不得作为设计、开发、联调或测试通过证据。
- 只要涉及 DDL、DML、数据修复、初始化数据、权限 / 配置数据、索引、迁移、回填或不可逆数据操作，必须在 `tech/backend/sql-execution-plan.md` 逐条记录 SQL / migration 文件、执行环境、执行时机、执行顺序、验证方式、回滚方案和风险。
- 不允许只在 `tech/backend/data-model.md` 或 `tech/risk-plan.md` 泛泛描述数据变更；需要执行的 SQL 必须进入 `tech/backend/sql-execution-plan.md`，供 `$pd-test` 和 `$pd-release` 读取。
- `$pd-plan` 完成时，所有 `contract` slice 必须已经由当前技术设计产物证明并标记为 `done`；不能把 `pending` / `blocked` 的 `contract` slice 留给 `$pd-fe` 或 `$pd-be`。
- 工程初始化、目录结构落地、依赖安装、Spring Boot / Vite 脚手架、环境变量模板文件、Flyway 迁移文件、真实 API client 等需要改代码或文件的动作，必须拆成 `frontend`、`backend`、`shared-frontend` 或 `shared-backend` slice；mock server、mock adapter、stub client、fake repository、fake data source、contract simulator 不得写入技术实现任务，只能作为阻断原因记录。
- `并行标记` 只表达调度属性，只允许 `parallel-safe`、`serial`、`stage-gate`；禁止写入任务 ID，禁止出现 `blocked-by XXX`、`blocks XXX`、`blocked-by SYNC-001` 等依赖内容。
- `blocked-by` 和 `blocks` 是独立依赖列，不属于并行标记；所有任务 ID 依赖只能写入这两列，`-` 表示无依赖且不得和任务 ID 混用。
- 依赖必须双向闭环：如果 `A.blocked-by` 包含 `B`，则 `B.blocks` 必须包含 `A`；如果 `B.blocks` 包含 `A`，则 `A.blocked-by` 必须包含 `B`。
- `frontend` / `backend` 开发任务默认依赖具体的 `C-*`、`FE-*`、`BE-*` 前置任务；不要为了流程整齐让所有后续开发都依赖 `SYNC-*`。
- 只有后续开发必须基于“已通过真实前后端联调的契约、字段、数据、错误码或端到端行为”时，才允许开发任务在 `blocked-by` 中依赖 `SYNC-*`。
- 如果 `SYNC-*` 只是验证建议，不应阻塞开发任务；应写入“验证”列或任务说明中的并行建议。
- 如果 `SYNC-*` 是阶段门，必须在任务描述、验证列或并行建议中说明理由，例如：`依赖配置域真实 API 差异关闭后才能进入任务域真实 API 开发`。
- `SYNC-*` 的 `blocked-by` 应包含它要联调的所有前后端实现任务；`blocks` 只应包含确实需要联调结果作为阶段门的后续任务；验证列必须说明联调范围和通过条件。
- 每个 `frontend` / `backend` / `shared-*` slice 的验证列必须引用对应依赖准备状态，例如 `依赖准备：JDK ready、DB ready、Dify API ready`；若依赖是 `unknown` / `blocked` / `mock-only`，该 slice 不得交付给开发，验证列也不得把 mock / stub / fake / fixture / simulator 作为通过证据。
- 前端 UI slice 的验证列必须包含 UI 质量验收要求，例如设计系统一致性、桌面 / 移动端、无横向溢出、文本不重叠、loading / empty / error / permission / saving 状态、表单错误或截图 / 浏览器证据。
- 首次上线 / 空仓库场景使用以下模式：
  - `C-001`: `contract` / `done` / 确认工程基线契约，验证指向 `tech/tech-plan.md`、`tech/api-contract.md`、`tech/backend/data-model.md`、`tech/integration-map.md`。
  - `FE-001`: `frontend` / `pending` / 创建前端工程骨架并验证构建。
  - `BE-001`: `backend` / `pending` / 创建后端工程骨架并验证健康检查。
- 如果某个契约仍无法确认，停止输出并说明缺口；不要生成看似可执行但会阻塞实现阶段的 `tech/task-slices.md`。

## 流程

1. 先确认 PRD、产品设计输入、`ui/ui-design-system.md`、UI 蓝图和 Figma handoff 足够支撑工程设计。
2. 对照产品事实源和 `ui/ui-design-system.md` 检查 Figma handoff：若发现范围外页面、导航、资产类型、业务模块、交易品类、参考产品文案或设计系统漂移，写入冲突说明并停止。
3. 产出 `tech/tech-plan.md`，明确范围、非目标、现有系统影响、实施顺序和风险。
4. 分别产出 `tech/frontend/frontend-design.md` 和 `tech/backend/backend-design.md`；前端设计必须包含 UI 设计系统约束、响应式、可访问性、表单校验、错误映射、空态和 UI 验收方式。
5. 产出 `tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md` 和 `tech/frontend/frontend-state-api.md`，把 Figma / UI 蓝图 / design system 映射到前端组件、路由、状态、API client、page override 和状态覆盖。
6. 产出 `tech/api-contract.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md` 和 `tech/integration-map.md`，串通前端字段、后端字段、状态、错误码、权限、分页、真实依赖和 SQL / migration 执行要求；不得产出 mock 契约、mock 数据结构或 mock 实现方案。
7. 产出 `tech/dependency-readiness.md`，扫描并列出 JDK、Node、包管理器、数据库、缓存 / 队列、下游 HTTP 服务、SDK / 开源框架、环境变量 / 凭证、SQL / migration 等本次开发依赖；每项必须写适用 slice、真实资源 / 地址、验证命令、状态、证据、阻断原因和下一步。
8. 产出 `tech/task-slices.md`，每个 slice 必须包含优先级、类型、状态、并行标记、依赖、阻塞关系、依赖准备引用和验证方式。
9. 对 `tech/task-slices.md` 和 `tech/dependency-readiness.md` 做 handoff 自检；若发现问题，先修正再输出最终技术设计结果：
   - 检查“并行标记”列是否合法，是否误写了 `blocked-by`、`blocks` 或任务 ID。
   - 检查所有 `blocked-by` / `blocks` 是否双向一致，不允许单边声明。
   - 检查所有被 `SYNC-*` 阻塞的 `frontend` / `backend` 任务是否有明确阶段门理由。
   - 检查是否存在开发任务被 `SYNC-*` 阻塞，但实际只依赖某个 `C-*`、`FE-*` 或 `BE-*` 的情况；若是，改为依赖具体 slice 或写入“验证”列。
   - 检查 `SYNC-*` 的 `blocked-by` 是否覆盖它要联调的所有前后端实现任务，`blocks` 是否只包含真实阶段门后续任务，验证列是否说明联调范围和通过条件。
   - 检查所有 `contract` slice 是否为 `done`，且没有把代码实现动作误归为 `contract`。
   - 检查前端 UI slice 是否包含 UI 质量验收要求；不得只写“实现页面”而缺少设计系统、状态、响应式或浏览器验证。
   - 检查是否生成 `tech/backend/sql-execution-plan.md`；涉及 SQL / migration 时执行清单、顺序、验证、回滚和风险不得为空；不涉及时必须明确写“不涉及”。
   - 检查是否生成 `tech/dependency-readiness.md`；所有开发必需依赖必须为 `ready` / `not-required`，不得用 `mock-only` 作为 ready 证据。
   - 检查每个开发 slice 的验证列是否引用对应依赖准备项；存在 `unknown` / `blocked` / `mock-only` 时，不得提示进入 `$pd-fe` / `$pd-be`，只输出阻断和下一步依赖准备。
   - 检查技术实现任务、验证方式和开发说明中是否出现 mock client / mock server / stub / fake / fixture / simulator；出现时必须改为真实依赖方案或阻断说明。
10. 产出 `tech/risk-plan.md`。
11. 输出摘要必须根据 `tech/dependency-readiness.md` 决定下一步：全部开发必需依赖为 `ready` / `not-required` 时才提示可并行执行 `$pd-fe` 和 `$pd-be`；否则提示先完成依赖准备。

## 输出摘要

```text
技术设计完成: <name>
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

下一步: <依赖全部 ready / not-required 时并行使用 $pd-fe 和 $pd-be；否则先完成 tech/dependency-readiness.md 中的阻断依赖>
```
