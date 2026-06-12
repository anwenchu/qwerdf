---
name: pd-be
description: >-
  后端开发实现工作流，基于 pd-plan 的 backend-design、api-contract、data-model、integration-map 和 task-slices，每次只实现一个 backend 或 shared-backend 任务切片，并做最小后端验证。Use when the user mentions $pd-be、pd-be、后端开发、后端实现、实现后端 slice、按技术方案写后端。
---

# $pd-be — 后端开发实现

Codex Product Delivery Skill：按技术设计执行一个后端 task slice。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中所有 `backend-*` 模板。
3. 读取 `backend-design.md`、`api-contract.md`、`data-model.md`、`integration-map.md`、`task-slices.md`。
4. 识别后端项目结构：服务入口、路由 / controller、service、repository、数据模型、权限、错误码、测试命令。
5. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 每次只执行一个 `backend` 或 `shared-backend` slice。
- 只更新自己负责的 slice 状态，不修改前端 slice。
- 不修改前端页面、组件、路由、样式。
- 不处理 `contract` 类型任务；发现契约问题时阻塞并记录，不单方面改契约。
- 不引入新的后端框架或存储方案，除非用户明确要求。
- 未完成本 slice 的最小验证时，不把 slice 状态更新为 `done`。

## 流程

1. 从 `task-slices.md` 选择一个可执行的后端 slice；没有明确 slice 时先让用户选择。
2. 将 slice 状态更新为 `in_progress`。
3. 按现有项目模式实现接口、服务逻辑、数据模型、权限校验、错误码或后端测试。
4. 执行项目已有的最小后端检查、测试或构建命令。
5. 写入 `backend-implementation-log.md`、`backend-changed-files.md`、`backend-dev-notes.md`。
6. 成功后将该 slice 状态更新为 `done`；阻塞时更新为 `blocked` 并说明原因、证据和建议回到的 skill。

## 输出摘要

```text
后端 slice 完成: <slice-id>
目录: <output-dir>
文件:
  - backend-implementation-log.md
  - backend-changed-files.md
  - backend-dev-notes.md
验证:
  - <命令 / 结果>
下一步: 继续 $pd-be 处理下一个后端 slice，或等待 $pd-fe 后执行 $pd-sync
```
