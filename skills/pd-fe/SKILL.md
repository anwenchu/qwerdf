---
name: pd-fe
description: >-
  前端开发实现工作流，基于 pd-plan 的 frontend-design、ui-design-system、api-contract、dependency-readiness、integration-map 和 task-slices，按本端顺序实现前端任务切片，每个切片执行真实依赖 gate、最小前端与 UI 质量验证。Use when the user mentions $pd-fe、pd-fe、前端开发、前端实现、实现前端 slice、按技术方案写前端、前端UI验收、真实依赖阻断。
---

# $pd-fe — 前端开发实现

按技术设计逐片实现，每个迭代闭合一个前端 task slice。

## 读取

先按 [生命周期规则](../qwerdf-common/artifact-lifecycle.md) 读取续作入口并核对权威任务；以下材料按当前任务 / finding 读取相关有效段落与必要证据，引用失效或有新冲突再扩查，不重复通读全部历史；仅适用时读取数据模型、SQL 或 UI 材料，不要求无关文件。

1. 定位本 `SKILL.md` 目录为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage fe`，只加载本阶段共享规则和模板（Python 3.10+，无第三方依赖）。不可运行时，按 [共享流程](../qwerdf-common/product-delivery-flow.md) 对应章节与下列模板手动读取；不通读无关阶段。
2. 上述输出已包含 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `frontend-*` 模板及 [共享业务进度摘要](../qwerdf-common/engineering-contracts.md#业务进度摘要)。任务选择、blocked 恢复和汇报按 [共享业务推进规则](../qwerdf-common/product-delivery-flow.md#业务推进阻断恢复与进度汇报) 执行。
   API 接入与任务范围按 [技术设计依据与范围规则](../qwerdf-common/technical-design-rules.md) 核对；关键参数 / 字段语义需猜测时回 `$pd-plan` 补证，不自行扩展契约或产品能力。
3. 读取 [UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)、[UI Patterns](../qwerdf-common/ui-patterns.md) 和 [UI Design System Rules](../qwerdf-common/ui-design-system.md)。
4. 读取 `tech/tech-plan.md`、`tech/frontend/frontend-design.md`、`tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md`、`tech/frontend/frontend-state-api.md`、`tech/api-contract.md`、`tech/dependency-readiness.md`、`tech/integration-map.md`、`tech/task-slices.md`、`ui/ui-design-system.md`、`ui/figma-handoff.md`，以及其中关联的未决项 / 设计检查记录。
   必须补读 Figma 原稿时，先加载当前环境中对应的 Figma 设计转代码技能并遵守其工具前置要求，连接选择与有效 session 按 [共享复用规则](../qwerdf-common/product-delivery-flow.md#figma-连接与会话复用) 执行，不因加载规范重新核查其他账号。已有材料不足时保留证据缺口，不用猜测或重复授权替代。
5. 如存在，读取 `sync/integration-report.md`、`sync/api-mismatch.md`、`test/test-report.md`、`test/code-review.md`、`ui/ui-review-report.md` 中归属 `$pd-fe` 的 findings。
6. 识别前端项目结构：`package.json`、路由、页面目录、组件目录、状态管理、API client、样式体系、测试命令。
7. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 只实现已授权且归属前端清单的任务，不改对端代码或状态、不单方面处理 contract、不引入未经要求的新框架。任务权威源、顺序、blocked 恢复与连续执行停止条件沿用已加载的共享规则；一片是迭代单位，不是批量授权的结束点。
- 开始或重开前按 [设计交接规则](../qwerdf-common/technical-design-rules.md#3-交付应足以让实现者执行) 核对当前结论与决定性缺口；有依据且属于既有契约 / 本片的工程遗漏直接补齐，需改契约或范围回 `$pd-plan / $pd-figma`，真正业务取舍才问用户。只检查不启动开发。
- 依赖按当前动作用途判断，不等待对端业务实现或 SYNC；顺序 / 输入说明冲突回 `$pd-plan` 校正受影响记录，其他具备条件的本端任务继续。真正编码缺输入仍阻断；验证受限的可继续范围、真实状态与 done 标准按共享规则，禁止模拟替代或虚报通过。
- 缺陷修复按共享联调与验收交接规则：有契约 / 设计依据、实现证据及本端已有 slice 的 implementation-defect 才可重开；无覆盖或需改上游则回 `$pd-plan / $pd-figma`。空仓库可执行设计已交接且输入齐备的工程初始化。
- 涉及 UI 时使用已确认的设计系统、Figma handoff 和前端设计；不改上游事实源掩盖偏差。独立 UI finding 按 [修复交接](../qwerdf-common/ui-review-rules.md#6-ui-finding-修复交接) 核对证据和归属，不因旧报告缺工程字段拒绝修复。

## 前端实现 Quick Reference

优先检查高影响问题，再处理低影响优化：

1. 数据 waterfalls：独立请求并行，便宜同步判断放在 await 前，避免串行加载。
2. Bundle：避免无边界 barrel import，重组件按需加载，第三方脚本延后。
3. Server / client 边界：只把必要数据传到 client，避免重复序列化和共享可变请求状态。
4. 状态与重渲染：派生状态优先 render 中计算，昂贵计算才 memo，事件逻辑不要塞进 effect。
5. 组件架构：避免用多个 boolean prop 表达模式，优先明确 variant、组合组件或 provider。
6. 可访问性与响应式：键盘焦点、语义结构、移动端无横向溢出和 reduced motion 不可跳过。
7. UI 质量：本次目标平台布局、文本不重叠、设计系统一致性及适用状态的证据进入 `frontend-acceptance.md`；状态适用性按 [共享质量清单](../qwerdf-common/ui-quality-checklist.md#4-适用的状态与交互)，不适用写明理由。
8. 管理后台 / SaaS / CRM / 操作台：优先信息密度、扫描效率、稳定布局和可重复操作；不要把页面改成营销 hero、大面积装饰或低密度展示卡片。

## 流程

1. 读取续作入口、权威任务及本端顺序，按 [共享仓库、分支与版本规则](../qwerdf-common/technical-design-rules.md#仓库分支与二方包版本) 核对实际目标及版本记录，再核对当前授权、设计交接与关联 finding。来源 / 状态冲突先按共享规则校正，视图滞后不能冒充任务缺失。
2. 按权威源中的本端顺序继续首个可执行的未完成任务，或有证据且已获准的缺陷修复。核查实际前置、全部原阻断及当前依赖用途；未 ready 只停止受影响动作。连续授权下转其他具备条件的任务，不以局部阻断全局停工。
3. 在权威源更新本任务为 in_progress 并刷新视图；blocked 的解除及仅验证受限时保留 blocked 续作严格按共享规则，不修改他人状态，不直接跳到 done。
4. 实现页面、组件、状态、真实 API client、权限 / 错误映射和必要接线，按适用平台验证布局、状态及设计系统一致性，证据记入 `frontend-acceptance.md`。缺必要原稿或运行环境时注明影响，不猜设计或用样例代替真实页面验收。
5. 扫描本片实际生产调用及测试路径，检查是否仍有 mock / stub / fake / fixture-only / simulator 或未接入真实 client；命名只是线索，按实际行为确认，发现不能以模拟结果交付。
6. 执行项目已有的最小高价值检查 / 构建 / 测试；修复须覆盖原 finding。受限、失败与通过分别记录，不重复跑无变化的全套检查，不跳过必要安全与依赖约束。
7. 原位更新本端实现记录、路径清单和仍有效注意事项；只留必要增量证据。代码 / 接线及原最小验证均完成后才将权威条目标 done 并刷新视图；否则注明剩余代码与验证缺口，不用“外部受阻”掩盖未实现。
8. 按共享业务进度摘要回填目标、实现 / 接线、验证、剩余与阻断；连续授权下回步骤 2。结束前核对原授权及所有剩余任务，只有满足共享停止条件才结束；不直接进入提交阶段。

## 输出摘要

```text
前端 slice / 缺陷修复状态: <slice-id；完成 / 阻断 / 未执行，按实际证据填写>
业务推进: <按共享业务进度摘要填写目标、实现与接线、验证、剩余与阻断；不估算整体百分比>
目录: <output-dir>
文件:
  - tech/task-slices.md（注明权威源；按既有来源更新本端状态与派生视图，顺序沿用 plan）
  - tech/frontend/frontend-implementation-log.md
  - tech/frontend/frontend-changed-files.md
  - tech/frontend/frontend-dev-notes.md
  - tech/frontend/frontend-acceptance.md
验证:
  - <命令 / 结果>
本端任务: <从已确认的权威源列 done / in_progress / pending / blocked 的计数与 ID；视图滞后须注明>
继续或结束: <连续授权下继续执行下一项；仅符合共享结束条件时给出剩余项与停止依据，不宣称未完成范围已完成>
```
