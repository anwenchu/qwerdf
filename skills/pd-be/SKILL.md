---
name: pd-be
description: >-
  后端开发实现工作流，基于 pd-plan 的 backend-design、api-contract、dependency-readiness、data-model、sql-execution-plan、integration-map 和 task-slices，每次只实现一个 backend 或 shared-backend 任务切片，并做真实依赖 gate 和最小后端验证；涉及 migration / SQL 时回填 SQL 执行计划。Use when the user mentions $pd-be、pd-be、后端开发、后端实现、实现后端 slice、按技术方案写后端、实现数据库迁移、真实依赖阻断。
---

# $pd-be — 后端开发实现

Codex Product Delivery Skill：按技术设计执行一个后端 task slice。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中所有 `backend-*` 模板。
3. 读取 `tech/backend/backend-design.md`、`tech/api-contract.md`、`tech/dependency-readiness.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md`、`tech/integration-map.md`、`tech/task-slices.md`。
4. 如存在，读取 `sync/integration-report.md`、`sync/api-mismatch.md`、`test/test-report.md`、`test/code-review.md` 中归属 `$pd-be` 的 findings。
5. 识别后端项目结构：服务入口、路由 / controller、service、repository、数据模型、权限、错误码、测试命令。
6. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 每次只执行一个 `backend` 或 `shared-backend` slice。
- 可执行范围默认是一个 `pending` 后端 slice；例外是来自 `$pd-sync`、`$pd-test` 或 `$pd-review` 的单个 `implementation-defect`，且该 finding 必须给出契约证据、实现证据和归属的已完成 `backend` / `shared-backend` slice。
- 只更新自己负责的 slice 状态，不修改前端 slice。
- 不修改前端页面、组件、路由、样式。
- 不处理 `contract` 类型任务；发现契约问题时阻塞并记录，不单方面改契约。
- 如果后端 slice 的唯一阻塞是 `pending` / `blocked` 的 `contract` slice，视为 `$pd-plan` handoff 问题：停止实现并建议回到 `$pd-plan` 修订；不要把工程初始化误判为后端不可执行。
- 如果所有 `contract` slice 已为 `done`，且当前后端 slice 是项目初始化 / 后端骨架创建，允许从空仓库直接执行该后端 slice。
- 如果后端缺陷来自真实联调 / 测试 / review，且契约已存在、归属 slice 已存在但状态为 `done`，允许进入缺陷修复模式：临时重开该 slice 为 `in_progress` 或在实现记录中标明同 slice 修复，修复后重新验证并标回 `done`。
- 如果 finding 被标为 `slice-missing`、无法映射到已有后端 slice，或需要新增 / 修改 API 契约、数据模型、状态枚举、权限规则或任务范围，必须停止并回到 `$pd-plan`；不得自行新造后端任务或改契约。
- 开始目标 slice 前必须检查 `tech/dependency-readiness.md`：适用该 slice 的依赖只有 `ready` / `not-required` 才可进入开发；`unknown` / `blocked` / `mock-only` 必须停止并记录阻断，不得标 `done`。
- 技术实现禁止使用任何 mock；不得实现或保留 mock client、mock server、stub adapter、fake repository、fake downstream、仅返回 fixture 的实现、测试替身或 contract simulator，发现时只能记录为阻断或 `implementation-defect`。
- 发现现有后端实现仍是 mock/stub/fake 或只接入 mock 下游时，归类为依赖阻断或 `implementation-defect`，不得把 slice 标为 `done`。
- 不引入新的后端框架或存储方案，除非用户明确要求。
- 如果实现涉及 migration、DDL、DML、初始化数据、数据修复、权限 / 配置数据或回填脚本，必须更新 `tech/backend/sql-execution-plan.md` 的实际 SQL / Migration 文件、执行环境、执行时机、验证方式和回滚方案；不得只把 SQL 文件写入代码库而不记录交接清单。
- 未完成本 slice 的最小验证时，不把 slice 状态更新为 `done`。
- 本阶段完成后不得建议直接提交、PR 或进入 `$pd-git`；只能继续后端 slice、等待 / 触发前端实现，或在相关实现完成后进入 `$pd-sync`。

## 流程

1. 先判断是否存在用户指定或报告中归属 `$pd-be` 的缺陷修复项。
2. 若存在缺陷修复项，先验证它是否满足缺陷修复模式：分类为 `implementation-defect`，契约证据能在 `tech/api-contract.md` / `tech/integration-map.md` 找到，实现证据指向后端代码或运行结果，且能映射到已有 `backend` / `shared-backend` slice。
3. 合法缺陷修复项可重开归属 slice 为 `in_progress` 或在实现记录中写明同 slice 修复；不合法时停止并说明应回 `$pd-plan` 的原因，尤其是 `slice-missing` 或契约需要变更。
4. 如果不是缺陷修复模式，从 `tech/task-slices.md` 选择一个可执行的后端 slice；没有明确 slice 时先让用户选择。可执行定义：类型为 `backend` / `shared-backend`，状态为 `pending`，且 `blocked-by` 为空或引用的 slice 全部为 `done`。
5. 若没有可执行后端 slice，先检查是否存在未完成 `contract` slice 阻塞实现；存在时报告 `$pd-plan` handoff 问题，不修改契约，不写后端代码。若只有联调 / 测试 / review 缺陷但缺少归属 slice，报告 `slice-missing` 并回 `$pd-plan`。
6. 检查 `tech/dependency-readiness.md` 中适用目标 slice 的依赖状态；任一必需依赖为 `unknown` / `blocked` / `mock-only` 时，停止开发，保持 `pending` 或标 `blocked` 并写明依赖 ID、阻断原因和下一步，不进入 `in_progress`。
7. 将目标 slice 状态更新为 `in_progress`。
8. 按现有项目模式实现接口、服务逻辑、数据模型、权限校验、错误码、migration / SQL 或后端测试；涉及下游 HTTP / SDK 时必须接入真实 `RestClient` / `WebClient` / 官方 SDK / 真实 adapter。
9. 扫描本 slice 是否残留 mock/stub/fake 命名、mock-only 配置、fixture-only 返回、测试替身或 simulator；发现后停止并记录为阻断或实现缺陷，不标 `done`。
10. 执行项目已有的最小后端检查、测试或构建命令；缺陷修复必须至少复现或覆盖原 finding 的验证路径。
11. 如果本 slice 新增或修改 SQL / migration，回填 `tech/backend/sql-execution-plan.md` 并在实现记录中引用 SQL ID。
12. 写入 `tech/backend/backend-implementation-log.md`、`tech/backend/backend-changed-files.md`、`tech/backend/backend-dev-notes.md`；缺陷修复必须填写“修复来源”，依赖阻断必须填写依赖 ID 和 `tech/dependency-readiness.md` 证据。
13. 成功后将该 slice 状态更新为 `done`；阻塞时更新为 `blocked` 并说明原因、证据和建议回到的 skill。

## 输出摘要

```text
后端 slice / 缺陷修复完成: <slice-id>
目录: <output-dir>
文件:
  - tech/backend/backend-implementation-log.md
  - tech/backend/backend-changed-files.md
  - tech/backend/backend-dev-notes.md
  - tech/backend/sql-execution-plan.md <如本 slice 涉及 SQL / migration>
验证:
  - <命令 / 结果>
下一步: 继续 $pd-be 处理下一个后端 slice，或等待 $pd-fe 后执行 $pd-sync
```
