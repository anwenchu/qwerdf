---
name: pd-sync
description: >-
  前后端联调工作流，基于前端实现、后端实现、api-contract 和 integration-map 检查接口、字段、状态码、错误结构、权限、分页、状态页、mock 与真实接口一致性；发现契约问题时生成 plan-revision，不直接修代码。Use when the user mentions $pd-sync、pd-sync、前后端联调、接口联调、API联调、mock切真实接口。
---

# $pd-sync — 前后端联调

Codex Product Delivery Skill：验证前后端实现是否符合统一契约。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `sync/integration-plan.md`、`sync/integration-report.md`、`sync/api-mismatch.md`、`sync/plan-revision.md` 的模板。
3. 读取 `tech/task-slices.md`、`tech/api-contract.md`、`tech/integration-map.md`、`tech/frontend/frontend-state-api.md`、`tech/frontend/frontend-implementation-log.md`、`tech/backend/backend-implementation-log.md`。
4. 识别本地前端、后端启动方式和环境配置。
5. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 不直接修前端代码。
- 不直接修后端代码。
- 不修改 API 契约或数据模型。
- 发现契约不一致时，必须生成 `sync/plan-revision.md` 并回到 `$pd-plan`。
- 无法启动或连接环境时，仍需写入 `sync/integration-report.md`，说明未执行项、原因和后续验证方式。
- 未明确通过联调时，不得建议进入 `$pd-test`、`$pd-review`、`$pd-git` 或提交 / PR。
- 相关 `frontend`、`backend`、`shared-frontend`、`shared-backend` slice 未全部为 `done` 时，不得执行联调；必须在 `sync/integration-report.md` 记录缺失实现并提示回到 `$pd-fe` / `$pd-be`。

## 联调决策树

```text
目标页面 / API
├─ 静态页面或纯前端 mock 可验证？
│  ├─ 是：先读取代码定位入口，再用浏览器验证渲染和交互
│  └─ 否：进入动态应用验证
└─ 动态应用验证
   ├─ 前后端服务已运行？
   │  ├─ 否：按项目脚本启动或记录无法启动原因
   │  └─ 是：打开页面，等待应用稳定，再检查 DOM、网络、日志和截图
   └─ 先侦察后操作：确认 selector / API / 状态，再执行交互断言
```

## 流程

1. 先检查 `tech/task-slices.md`：本次相关 `frontend`、`backend`、`shared-frontend`、`shared-backend` slice 必须全部为 `done`，并且前端 / 后端实现记录必须存在。
2. 如果存在未完成实现 slice，写入 `sync/integration-report.md` 的实现前置状态，列出缺失 slice、当前状态和应回到的 `$pd-fe` / `$pd-be`；停止联调，不启动环境，不进入 `$pd-test`。
3. 生成 `sync/integration-plan.md`，列出联调场景、前端入口、API、数据准备和预期。
4. 启动或连接可用的前后端环境。
5. 检查 path、method、request、response、状态码、错误结构、权限、分页、状态页、mock 和真实接口切换。
6. 对每个场景记录证据：命令输出、请求 / 响应摘要、截图、日志位置或未执行原因。
7. 写入 `sync/integration-report.md`。
8. 如发现实现问题但契约正确，记录到报告并提示回到 `$pd-fe` 或 `$pd-be`。
9. 如发现契约问题，写入 `sync/api-mismatch.md` 和 `sync/plan-revision.md`，停止并提示回到 `$pd-plan`。

## 输出摘要

```text
联调完成: <name>
目录: <output-dir>
文件:
  - sync/integration-plan.md
  - sync/integration-report.md
  - sync/api-mismatch.md
  - sync/plan-revision.md
结论: <通过 / 需前端修复 / 需后端修复 / 需回到 pd-plan>
下一步: <通过则用 $pd-test 做全链路验证；否则回到对应修复阶段>
```
