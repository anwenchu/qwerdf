---
name: pd-plan
description: >-
  个人技术设计工作流，基于 PRD、产品设计输入、UI 蓝图、Figma handoff 和现有代码库产出前端设计、后端设计、API 契约、数据模型、前后端一致性映射、任务切片和风险方案。Use when the user mentions $pd-plan、pd-plan、技术设计、技术方案、前后端设计、接口契约、任务切片。
---

# $pd-plan — 技术设计

个人辅助 Skill：把产品和设计产物串成前后端一致、可并行开发的工程方案。

## 读取

1. 读取 [个人 Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `tech-plan.md`、`frontend-design.md`、`frontend-component-map.md`、`frontend-route-map.md`、`frontend-state-api.md`、`backend-design.md`、`api-contract.md`、`data-model.md`、`integration-map.md`、`task-slices.md`、`risk-plan.md` 的模板。
3. 读取 `prd.md`、`requirements.md`、`product-brief.md`、`ui-screens.md`、`ui-components.md`、`figma-handoff.md`。
4. 扫描现有代码库的前端、后端、API client、路由、数据模型、权限和测试结构。
5. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 不写代码。
- 不提交代码。
- 不改 PRD 或 Figma。
- 不让 `$pd-fe` 或 `$pd-be` 单方面处理 `contract` 类型任务。
- 发现需求不清时，停止并提示回到 `$pd-prd`、`$pd-blueprint` 或 `$pd-figma`。

## 规则优先级

| 优先级 | 类别 | 设计重点 |
| --- | --- | --- |
| 1 | 契约一致性 | API、字段、状态、权限、错误码、分页和 mock 必须先对齐 |
| 2 | 数据与权限 | 数据模型、可见性、幂等、事务和越权风险必须可验证 |
| 3 | 前端架构 | 路由、组件、状态、API client 和设计还原路径要可落地 |
| 4 | 后端架构 | controller / service / repository 边界、错误处理和观测要清楚 |
| 5 | 性能与可维护性 | 避免不必要 waterfalls、重复请求、过宽 bundle、布尔 prop 膨胀和隐式耦合 |
| 6 | 发布风险 | 回滚、灰度、监控、测试缺口和人工确认项必须被记录 |

## 流程

1. 先确认 PRD、产品设计输入、UI 蓝图和 Figma handoff 足够支撑工程设计。
2. 产出 `tech-plan.md`，明确范围、非目标、现有系统影响、实施顺序和风险。
3. 分别产出 `frontend-design.md` 和 `backend-design.md`。
4. 产出 `frontend-component-map.md`、`frontend-route-map.md` 和 `frontend-state-api.md`，把 Figma / UI 蓝图映射到前端组件、路由、状态和 API client。
5. 产出 `api-contract.md`、`data-model.md` 和 `integration-map.md`，串通前端字段、后端字段、状态、错误码、权限、分页和 mock。
6. 产出 `task-slices.md`，每个 slice 必须包含优先级、类型、状态、并行标记、依赖、阻塞关系和验证方式。
7. 产出 `risk-plan.md`。
8. 输出摘要必须提示可并行执行 `$pd-fe` 和 `$pd-be`。

## 输出摘要

```text
技术设计完成: <name>
目录: <output-dir>
文件:
  - tech-plan.md
  - frontend-design.md
  - frontend-component-map.md
  - frontend-route-map.md
  - frontend-state-api.md
  - backend-design.md
  - api-contract.md
  - data-model.md
  - integration-map.md
  - task-slices.md
  - risk-plan.md

下一步: 并行使用 $pd-fe 和 $pd-be 按 task-slices.md 执行开发切片
```
