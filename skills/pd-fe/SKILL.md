---
name: pd-fe
description: >-
  前端开发实现工作流，基于 pd-plan 的 frontend-design、ui-design-system、api-contract、integration-map 和 task-slices，每次只实现一个 frontend 或 shared-frontend 任务切片，并做最小前端与 UI 质量验证。Use when the user mentions $pd-fe、pd-fe、前端开发、前端实现、实现前端 slice、按技术方案写前端、前端UI验收。
---

# $pd-fe — 前端开发实现

Codex Product Delivery Skill：按技术设计执行一个前端 task slice。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中所有 `frontend-*` 模板。
3. 读取 [UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)、[UI Patterns](../qwerdf-common/ui-patterns.md) 和 [UI Design System Rules](../qwerdf-common/ui-design-system.md)。
4. 读取 `tech/frontend/frontend-design.md`、`tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md`、`tech/frontend/frontend-state-api.md`、`tech/api-contract.md`、`tech/integration-map.md`、`tech/task-slices.md`、`ui/ui-design-system.md`、`ui/figma-handoff.md`。
5. 如存在，读取 `sync/integration-report.md`、`sync/api-mismatch.md`、`test/test-report.md`、`test/code-review.md` 中归属 `$pd-fe` 的 findings。
6. 识别前端项目结构：`package.json`、路由、页面目录、组件目录、状态管理、API client、样式体系、测试命令。
7. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 每次只执行一个 `frontend` 或 `shared-frontend` slice。
- 可执行范围默认是一个 `pending` 前端 slice；例外是来自 `$pd-sync`、`$pd-test` 或 `$pd-review` 的单个 `implementation-defect`，且该 finding 必须给出契约 / UI 设计证据、实现证据和归属的已完成 `frontend` / `shared-frontend` slice。
- 只更新自己负责的 slice 状态，不修改后端 slice。
- 不修改后端接口、数据库、权限模型、后端服务逻辑。
- 不处理 `contract` 类型任务；发现契约问题时阻塞并记录，不单方面改契约。
- 如果前端 slice 的唯一阻塞是 `pending` / `blocked` 的 `contract` slice，视为 `$pd-plan` handoff 问题：停止实现并建议回到 `$pd-plan` 修订；不要把工程初始化误判为前端不可执行。
- 如果所有 `contract` slice 已为 `done`，且当前前端 slice 是项目初始化 / 前端骨架创建，允许从空仓库直接执行该前端 slice。
- 如果前端缺陷来自真实联调 / 测试 / review，且契约或 UI 设计事实源已存在、归属 slice 已存在但状态为 `done`，允许进入缺陷修复模式：临时重开该 slice 为 `in_progress` 或在实现记录中标明同 slice 修复，修复后重新验证并标回 `done`。
- 如果 finding 被标为 `slice-missing`、无法映射到已有前端 slice，或需要新增 / 修改 API 契约、页面范围、路由、UI 设计系统、Figma handoff 或任务范围，必须停止并回到 `$pd-plan` / `$pd-figma`；不得自行新造前端任务或改上游事实源。
- 不引入新 UI 框架，除非用户明确要求。
- 不绕过 `ui/ui-design-system.md` 自行重设颜色、字体、圆角、按钮层级、导航结构或页面模式；发现设计系统缺失或冲突时，先记录阻塞并回到 `$pd-figma` / `$pd-plan`。
- 未完成本 slice 的最小验证时，不把 slice 状态更新为 `done`。
- 本阶段完成后不得建议直接提交、PR 或进入 `$pd-git`；只能继续前端 slice、等待 / 触发后端实现，或在相关实现完成后进入 `$pd-sync`。

## 前端实现 Quick Reference

优先检查高影响问题，再处理低影响优化：

1. 数据 waterfalls：独立请求并行，便宜同步判断放在 await 前，避免串行加载。
2. Bundle：避免无边界 barrel import，重组件按需加载，第三方脚本延后。
3. Server / client 边界：只把必要数据传到 client，避免重复序列化和共享可变请求状态。
4. 状态与重渲染：派生状态优先 render 中计算，昂贵计算才 memo，事件逻辑不要塞进 effect。
5. 组件架构：避免用多个 boolean prop 表达模式，优先明确 variant、组合组件或 provider。
6. 可访问性与响应式：键盘焦点、语义结构、移动端无横向溢出和 reduced motion 不可跳过。
7. UI 质量：桌面 / 移动端布局、文本不重叠、按钮 / 表单状态、loading / empty / error / permission / saving 状态、设计系统一致性必须进入 `frontend-acceptance.md`。
8. 管理后台 / SaaS / CRM / 操作台：优先信息密度、扫描效率、稳定布局和可重复操作；不要把页面改成营销 hero、大面积装饰或低密度展示卡片。

## 流程

1. 先判断是否存在用户指定或报告中归属 `$pd-fe` 的缺陷修复项。
2. 若存在缺陷修复项，先验证它是否满足缺陷修复模式：分类为 `implementation-defect`，契约证据能在 `tech/api-contract.md` / `tech/integration-map.md` 找到或 UI 证据能在 `ui/ui-design-system.md` / `ui/figma-handoff.md` 找到，实现证据指向前端代码、浏览器截图、console、网络请求或测试结果，且能映射到已有 `frontend` / `shared-frontend` slice。
3. 合法缺陷修复项可重开归属 slice 为 `in_progress` 或在实现记录中写明同 slice 修复；不合法时停止并说明应回 `$pd-plan` / `$pd-figma` 的原因，尤其是 `slice-missing` 或上游事实源需要变更。
4. 如果不是缺陷修复模式，从 `tech/task-slices.md` 选择一个可执行的前端 slice；没有明确 slice 时先让用户选择。可执行定义：类型为 `frontend` / `shared-frontend`，状态为 `pending`，且 `blocked-by` 为空或引用的 slice 全部为 `done`。
5. 若没有可执行前端 slice，先检查是否存在未完成 `contract` slice 阻塞实现；存在时报告 `$pd-plan` handoff 问题，不修改契约，不写前端代码。若只有联调 / 测试 / review 缺陷但缺少归属 slice，报告 `slice-missing` 并回 `$pd-plan`。
6. 将目标 slice 状态更新为 `in_progress`。
7. 对照 `ui/ui-design-system.md`、`ui/figma-handoff.md` 和当前 slice 的验证列，确认本次 UI 质量验收点；缺失时记录为 `$pd-plan` handoff 缺口，不自行发明设计规则。
8. 按现有项目模式实现页面、组件、状态、API client、mock 切换或前端校验。
9. 执行项目已有的最小前端检查、测试或构建命令；缺陷修复必须至少复现或覆盖原 finding 的验证路径。
10. 做浏览器或组件级验收；至少检查桌面 / 移动端布局、无横向溢出、无文本重叠、按钮 / 表单状态、loading / empty / error / permission / saving 状态。没有可运行环境时，记录原因和人工验证项。
11. 写入 `tech/frontend/frontend-implementation-log.md`、`tech/frontend/frontend-changed-files.md`、`tech/frontend/frontend-dev-notes.md`、`tech/frontend/frontend-acceptance.md`；缺陷修复必须填写“修复来源”。
12. 成功后将该 slice 状态更新为 `done`；阻塞时更新为 `blocked` 并说明原因、证据和建议回到的 skill。

## 输出摘要

```text
前端 slice / 缺陷修复完成: <slice-id>
目录: <output-dir>
文件:
  - tech/frontend/frontend-implementation-log.md
  - tech/frontend/frontend-changed-files.md
  - tech/frontend/frontend-dev-notes.md
  - tech/frontend/frontend-acceptance.md
验证:
  - <命令 / 结果>
下一步: 继续 $pd-fe 处理下一个前端 slice，或等待 $pd-be 后执行 $pd-sync
```
