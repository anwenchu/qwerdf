---
name: pd-sync
description: >-
  前后端联调工作流，基于前端实现、后端实现、api-contract 和 integration-map 检查接口、字段、状态码、错误结构、权限、分页、状态页、mock 与真实接口一致性；发现契约问题时生成 plan-revision，不直接修代码。Use when the user mentions $pd-sync、pd-sync、前后端联调、接口联调、API联调、mock切真实接口。
---

# $pd-sync — 前后端联调

Codex Product Delivery Skill：验证前后端实现是否符合统一契约。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `integration-plan.md`、`integration-report.md`、`api-mismatch.md`、`plan-revision.md` 的模板。
3. 读取 `api-contract.md`、`integration-map.md`、`frontend-state-api.md`、`frontend-implementation-log.md`、`backend-implementation-log.md`。
4. 识别本地前端、后端启动方式和环境配置。
5. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 不直接修前端代码。
- 不直接修后端代码。
- 不修改 API 契约或数据模型。
- 发现契约不一致时，必须生成 `plan-revision.md` 并回到 `$pd-plan`。
- 无法启动或连接环境时，仍需写入 `integration-report.md`，说明未执行项、原因和后续验证方式。

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

1. 生成 `integration-plan.md`，列出联调场景、前端入口、API、数据准备和预期。
2. 启动或连接可用的前后端环境。
3. 检查 path、method、request、response、状态码、错误结构、权限、分页、状态页、mock 和真实接口切换。
4. 对每个场景记录证据：命令输出、请求 / 响应摘要、截图、日志位置或未执行原因。
5. 写入 `integration-report.md`。
6. 如发现实现问题但契约正确，记录到报告并提示回到 `$pd-fe` 或 `$pd-be`。
7. 如发现契约问题，写入 `api-mismatch.md` 和 `plan-revision.md`，停止并提示回到 `$pd-plan`。

## 输出摘要

```text
联调完成: <name>
目录: <output-dir>
文件:
  - integration-plan.md
  - integration-report.md
  - api-mismatch.md
  - plan-revision.md
结论: <通过 / 需前端修复 / 需后端修复 / 需回到 pd-plan>
```
