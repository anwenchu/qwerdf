---
name: pd-fe
description: >-
  前端开发实现工作流，基于 pd-plan 的 frontend-design、api-contract、integration-map 和 task-slices，每次只实现一个 frontend 或 shared-frontend 任务切片，并做最小前端验证。Use when the user mentions $pd-fe、pd-fe、前端开发、前端实现、实现前端 slice、按技术方案写前端。
---

# $pd-fe — 前端开发实现

Codex Product Delivery Skill：按技术设计执行一个前端 task slice。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中所有 `frontend-*` 模板。
3. 读取 `frontend-design.md`、`frontend-component-map.md`、`frontend-route-map.md`、`frontend-state-api.md`、`api-contract.md`、`integration-map.md`、`task-slices.md`、`figma-handoff.md`。
4. 识别前端项目结构：`package.json`、路由、页面目录、组件目录、状态管理、API client、样式体系、测试命令。
5. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 每次只执行一个 `frontend` 或 `shared-frontend` slice。
- 只更新自己负责的 slice 状态，不修改后端 slice。
- 不修改后端接口、数据库、权限模型、后端服务逻辑。
- 不处理 `contract` 类型任务；发现契约问题时阻塞并记录，不单方面改契约。
- 不引入新 UI 框架，除非用户明确要求。
- 未完成本 slice 的最小验证时，不把 slice 状态更新为 `done`。

## 前端实现 Quick Reference

优先检查高影响问题，再处理低影响优化：

1. 数据 waterfalls：独立请求并行，便宜同步判断放在 await 前，避免串行加载。
2. Bundle：避免无边界 barrel import，重组件按需加载，第三方脚本延后。
3. Server / client 边界：只把必要数据传到 client，避免重复序列化和共享可变请求状态。
4. 状态与重渲染：派生状态优先 render 中计算，昂贵计算才 memo，事件逻辑不要塞进 effect。
5. 组件架构：避免用多个 boolean prop 表达模式，优先明确 variant、组合组件或 provider。
6. 可访问性与响应式：键盘焦点、语义结构、移动端无横向溢出和 reduced motion 不可跳过。

## 流程

1. 从 `task-slices.md` 选择一个可执行的前端 slice；没有明确 slice 时先让用户选择。
2. 将 slice 状态更新为 `in_progress`。
3. 按现有项目模式实现页面、组件、状态、API client、mock 切换或前端校验。
4. 执行项目已有的最小前端检查、测试或构建命令。
5. 做浏览器或组件级验收；如没有可运行环境，记录原因和人工验证项。
6. 写入 `frontend-implementation-log.md`、`frontend-changed-files.md`、`frontend-dev-notes.md`、`frontend-acceptance.md`。
7. 成功后将该 slice 状态更新为 `done`；阻塞时更新为 `blocked` 并说明原因、证据和建议回到的 skill。

## 输出摘要

```text
前端 slice 完成: <slice-id>
目录: <output-dir>
文件:
  - frontend-implementation-log.md
  - frontend-changed-files.md
  - frontend-dev-notes.md
  - frontend-acceptance.md
验证:
  - <命令 / 结果>
下一步: 继续 $pd-fe 处理下一个前端 slice，或等待 $pd-be 后执行 $pd-sync
```
