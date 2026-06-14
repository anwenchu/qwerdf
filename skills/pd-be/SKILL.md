---
name: pd-be
description: >-
  后端开发实现工作流，基于 pd-plan 的 backend-design、api-contract、data-model、sql-execution-plan、integration-map 和 task-slices，每次只实现一个 backend 或 shared-backend 任务切片，并做最小后端验证；涉及 migration / SQL 时回填 SQL 执行计划。Use when the user mentions $pd-be、pd-be、后端开发、后端实现、实现后端 slice、按技术方案写后端、实现数据库迁移。
---

# $pd-be — 后端开发实现

Codex Product Delivery Skill：按技术设计执行一个后端 task slice。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中所有 `backend-*` 模板。
3. 读取 `tech/backend/backend-design.md`、`tech/api-contract.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md`、`tech/integration-map.md`、`tech/task-slices.md`。
4. 识别后端项目结构：服务入口、路由 / controller、service、repository、数据模型、权限、错误码、测试命令。
5. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 每次只执行一个 `backend` 或 `shared-backend` slice。
- 只更新自己负责的 slice 状态，不修改前端 slice。
- 不修改前端页面、组件、路由、样式。
- 不处理 `contract` 类型任务；发现契约问题时阻塞并记录，不单方面改契约。
- 如果后端 slice 的唯一阻塞是 `pending` / `blocked` 的 `contract` slice，视为 `$pd-plan` handoff 问题：停止实现并建议回到 `$pd-plan` 修订；不要把工程初始化误判为后端不可执行。
- 如果所有 `contract` slice 已为 `done`，且当前后端 slice 是项目初始化 / 后端骨架创建，允许从空仓库直接执行该后端 slice。
- 不引入新的后端框架或存储方案，除非用户明确要求。
- 如果实现涉及 migration、DDL、DML、初始化数据、数据修复、权限 / 配置数据或回填脚本，必须更新 `tech/backend/sql-execution-plan.md` 的实际 SQL / Migration 文件、执行环境、执行时机、验证方式和回滚方案；不得只把 SQL 文件写入代码库而不记录交接清单。
- 未完成本 slice 的最小验证时，不把 slice 状态更新为 `done`。
- 本阶段完成后不得建议直接提交、PR 或进入 `$pd-git`；只能继续后端 slice、等待 / 触发前端实现，或在相关实现完成后进入 `$pd-sync`。

## 流程

1. 从 `tech/task-slices.md` 选择一个可执行的后端 slice；没有明确 slice 时先让用户选择。可执行定义：类型为 `backend` / `shared-backend`，状态为 `pending`，且 `blocked-by` 为空或引用的 slice 全部为 `done`。
2. 若没有可执行后端 slice，先检查是否存在未完成 `contract` slice 阻塞实现；存在时报告 `$pd-plan` handoff 问题，不修改契约，不写后端代码。
3. 将 slice 状态更新为 `in_progress`。
4. 按现有项目模式实现接口、服务逻辑、数据模型、权限校验、错误码、migration / SQL 或后端测试。
5. 执行项目已有的最小后端检查、测试或构建命令。
6. 如果本 slice 新增或修改 SQL / migration，回填 `tech/backend/sql-execution-plan.md` 并在实现记录中引用 SQL ID。
7. 写入 `tech/backend/backend-implementation-log.md`、`tech/backend/backend-changed-files.md`、`tech/backend/backend-dev-notes.md`。
8. 成功后将该 slice 状态更新为 `done`；阻塞时更新为 `blocked` 并说明原因、证据和建议回到的 skill。

## 输出摘要

```text
后端 slice 完成: <slice-id>
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
