---
name: pd-be
description: >-
  后端开发实现工作流，基于 pd-plan 的 backend-design、api-contract、dependency-readiness、data-model、sql-execution-plan、integration-map 和 task-slices，按本端顺序实现后端任务切片，每个切片执行真实依赖 gate 和最小后端验证；涉及 migration / SQL 时回填 SQL 执行计划。Use when the user mentions $pd-be、pd-be、后端开发、后端实现、实现后端 slice、按技术方案写后端、实现数据库迁移、真实依赖阻断。
---

# $pd-be — 后端开发实现

按技术设计逐片实现，每个迭代闭合一个后端 task slice。

## 读取

先按 [生命周期规则](../qwerdf-common/artifact-lifecycle.md) 读取续作入口并核对权威任务；以下材料按当前任务 / finding 读取相关有效段落与必要证据，引用失效或有新冲突再扩查，不重复通读全部历史；仅适用时读取数据模型、SQL 或 UI 材料，不要求无关文件。

1. 定位本 `SKILL.md` 目录为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage be`，只加载本阶段共享规则和模板（Python 3.10+，无第三方依赖）。不可运行时，按 [共享流程](../qwerdf-common/product-delivery-flow.md) 对应章节与下列模板手动读取；不通读无关阶段。
2. 上述输出已包含 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `backend-*` 模板及 [共享业务进度摘要](../qwerdf-common/engineering-contracts.md#业务进度摘要)。任务选择、blocked 恢复和汇报按 [共享业务推进规则](../qwerdf-common/product-delivery-flow.md#业务推进阻断恢复与进度汇报) 执行。
   关键接入与范围按 [技术设计依据与范围规则](../qwerdf-common/technical-design-rules.md) 核对；需要猜服务、方法、参数来源或字段语义时回 `$pd-plan` 补证，不静默发明契约或新增范围。
3. 读取 `tech/tech-plan.md`、`tech/backend/backend-design.md`、`tech/api-contract.md`、`tech/dependency-readiness.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md`、`tech/integration-map.md`、`tech/task-slices.md`，以及其中关联的未决项 / 设计检查记录。
4. 如存在，读取 `sync/integration-report.md`、`sync/api-mismatch.md`、`test/test-report.md`、`test/code-review.md` 中归属 `$pd-be` 的 findings。
5. 识别后端项目结构：服务入口、路由 / controller、service、repository、数据模型、权限、错误码、测试命令。
   涉及 Java 时按 [共享 Java 编码规则](../qwerdf-common/java-coding-rules.md) 的适用章节实现；不将规范建议扩成新任务或另一套阶段门。
6. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 只实现已授权且归属后端清单的任务，不改对端代码或状态、不单方面处理 contract、不引入未经要求的新框架或存储方案。任务权威源、顺序、blocked 恢复与连续执行停止条件沿用已加载的共享规则；一片是迭代单位，不是批量授权的结束点。
- 开始或重开前按 [设计交接规则](../qwerdf-common/technical-design-rules.md#3-交付应足以让实现者执行) 核对当前结论与决定性缺口；有依据且属于既有契约 / 本片的工程遗漏直接补齐，需改契约或范围回 `$pd-plan`，真正业务取舍才问用户。只检查不启动开发。
- 依赖按当前动作用途判断，不等待对端业务实现或 SYNC；顺序 / 输入说明冲突回 `$pd-plan` 校正受影响记录，其他具备条件的本端任务继续。真正编码缺输入仍阻断；验证受限的可继续范围、真实状态与 done 标准按共享规则，禁止模拟替代或虚报通过。
- 缺陷修复按共享联调与验收交接规则：有契约 / 设计依据、实现证据及本端已有 slice 的 implementation-defect 才可重开；无覆盖或需改上游则回 `$pd-plan`。空仓库可执行设计已交接且输入齐备的工程初始化。
- 涉及 Java 时按公共 Java 规则实现，持久化方式、MyBatis / XML、事务、行锁及缓存边界不得省略；涉及 SQL / migration 时回填原执行计划，不执行未获准的 SQL。

## 流程

1. 读取续作入口、权威任务及本端顺序，按 [共享仓库、分支与版本规则](../qwerdf-common/technical-design-rules.md#仓库分支与二方包版本) 核对实际目标及版本记录，再核对当前授权、设计交接与关联 finding。来源 / 状态冲突先按共享规则校正，视图滞后不能冒充任务缺失。
2. 按权威源中的本端顺序继续首个可执行的未完成任务，或有证据且已获准的缺陷修复。核查实际前置、全部原阻断及当前依赖用途；未 ready 只停止受影响动作。连续授权下转其他具备条件的任务，不以局部阻断全局停工。
3. 在权威源更新本任务为 in_progress 并刷新视图；blocked 的解除及仅验证受限时保留 blocked 续作严格按共享规则，不修改他人状态，不直接跳到 done。
4. 实现接口、服务、持久化、权限、错误码、事务、真实下游调用和必要接线；SQL / migration 文件进入原执行计划并引用 SQL ID。
5. 扫描本片实际生产调用及测试路径，检查是否仍有 mock / stub / fake / fixture-only / simulator 或未接入真实 client；命名只是线索，按实际行为确认，发现不能以模拟结果交付。
6. 执行项目已有的最小高价值检查 / 构建 / 测试；修复须覆盖原 finding。受限、失败与通过分别记录，不重复跑无变化的全套检查，不跳过必要安全与依赖约束。
7. 原位更新本端实现记录、路径清单和仍有效注意事项；只留必要增量证据。代码 / 接线及原最小验证均完成后才将权威条目标 done 并刷新视图；否则注明剩余代码与验证缺口，不用“外部受阻”掩盖未实现。
8. 按共享业务进度摘要回填目标、实现 / 接线、验证、剩余与阻断；连续授权下回步骤 2。结束前核对原授权及所有剩余任务，只有满足共享停止条件才结束；不直接进入提交阶段。

## 输出摘要

```text
后端 slice / 缺陷修复状态: <slice-id；完成 / 阻断 / 未执行，按实际证据填写>
业务推进: <按共享业务进度摘要填写目标、实现与接线、验证、剩余与阻断；不估算整体百分比>
目录: <output-dir>
文件:
  - tech/task-slices.md（注明权威源；按既有来源更新本端状态与派生视图，顺序沿用 plan）
  - tech/backend/backend-implementation-log.md
  - tech/backend/backend-changed-files.md
  - tech/backend/backend-dev-notes.md
  - tech/backend/sql-execution-plan.md <如本 slice 涉及 SQL / migration>
验证:
  - <命令 / 结果>
本端任务: <从已确认的权威源列 done / in_progress / pending / blocked 的计数与 ID；视图滞后须注明>
继续或结束: <连续授权下继续执行下一项；仅符合共享结束条件时给出剩余项与停止依据，不宣称未完成范围已完成>
```
