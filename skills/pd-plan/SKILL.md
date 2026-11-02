---
name: pd-plan
description: >-
  技术设计工作流，依据本轮确认需求和现有代码，为适用的前后端范围维护可落地设计、API 契约、依赖准备、数据与 SQL 方案、任务顺序及风险；涉及 UI 时对齐设计系统与 handoff。Use when the user mentions $pd-plan、pd-plan、技术设计、技术方案、前后端设计、接口契约、任务切片、依赖准备、SQL执行计划、数据库迁移计划、UI技术设计。
---

# $pd-plan — 技术设计

把产品和设计产物串成前后端一致、可并行开发的工程方案。

## 读取

下列项目材料只读取本轮适用的当前段落；缺少实际必需输入保留缺口，无关端、UI 或 SQL 不要求补造文件。

1. 定位本 `SKILL.md` 目录为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage plan`，仅前端 / 后端范围可加 `--area frontend` / `--area backend`，只加载适用共享规则和模板（Python 3.10+，无第三方依赖）。不可运行时，按 [共享流程](../qwerdf-common/product-delivery-flow.md) 对应章节与下列模板手动读取；不通读无关阶段。
2. 上述输出已包含 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `tech/tech-plan.md`、`tech/dependency-readiness.md`、`tech/frontend/frontend-design.md`、`tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md`、`tech/frontend/frontend-state-api.md`、`tech/backend/backend-design.md`、`tech/api-contract.md`、`tech/backend/data-model.md`、`tech/backend/sql-execution-plan.md`、`tech/integration-map.md`、`tech/task-slices.md`、`tech/risk-plan.md` 的模板；只采用本轮适用项。
3. 涉及 UI 时读取 [UI Design System Rules](../qwerdf-common/ui-design-system.md) 和 [UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)。
   技术依据、范围控制和交接判断读取 [技术设计依据与范围规则](../qwerdf-common/technical-design-rules.md)。
4. 按确认范围读取 `product/prd.md`、`product/requirements.md`、`product/product-brief.md`、`ui/ui-design-system.md`、`ui/ui-screens.md`、`ui/ui-components.md`、`ui/figma-handoff.md`。
   如确需访问 Figma 补证，加载对应操作技能并按 [共享连接规则](../qwerdf-common/product-delivery-flow.md#figma-连接与会话复用) 使用已有选择和有效会话；不将例行技术设计检查变成全部账号认证。
5. 先按本期业务链路限定扫描问题和停止边界，再读取相关前后端入口、API client、契约 / 提供方实现、路由、数据模型、权限、实际依赖版本 / 配置及测试结构；只读影响核查不自动扩成改造范围。
   涉及 Java 持久化设计时，按 [共享持久化规则](../qwerdf-common/java-coding-rules.md#spring-事务与持久化涉及数据库时) 明确数据访问方式、Mapper / XML 归属及事务边界，不把未确定的持久化选型留给实现阶段。
6. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 本阶段只设计 / 修订技术产物，不写业务代码、不提交、不改产品或 UI 事实源。只检查时只读报告，不因检查补造整套文件或启动开发。
- 依据、范围、工程漏项分类和交接条件统一按 [技术设计规则](../qwerdf-common/technical-design-rules.md)；关键服务、方法、参数来源及取值语义须有可定位依据，拟新增能力标为提案，决定性未知不能包装成设计完成。
- 适用产物与开发门禁沿用 context 中的共享规则。无 UI 不要求 Figma；涉及 UI 时必须核对产品事实、设计系统及 handoff，不能让参考增加范围。必要视觉证据缺口与独立 UI finding 保留。
- 任务权威源、动作粒度、各端顺序、完成标准、并行开发及联调验收交接，统一按 [Task Slice 规则](../qwerdf-common/product-delivery-flow.md#8-task-slice-规则)；不在本入口另维护一套枚举或例外。契约在设计交接中完成，未决字段不交给开发猜测。

## 流程

1. 先按 [共享仓库、分支与版本规则](../qwerdf-common/technical-design-rules.md#仓库分支与二方包版本) 确认本轮修改仓库和各自开发分支，再明确授权、验收范围、已有决定及需要修订的结论；二方包版本记录同源维护。判断前端、后端、UI、SQL 与联调适用性，将不适用项及依据记在 `tech/tech-plan.md`，不新建空文档。
2. 围绕确认的业务链路定向查源码、契约、实际依赖与测试；按共享分类规则补齐有依据的工程漏项，真正改变业务规则或范围才澄清。只读影响发现不自动纳入实施。
3. 原位维护 `tech/tech-plan.md` 与受影响的端设计、API 契约、数据模型和 integration-map。关键链路写清调用对象 / 方法、参数来源、数据语义、权限、状态变化、幂等 / 事务及失败恢复，关联证据并区分既有事实、提案和未决项。
4. 涉及 UI 时将设计系统和 handoff 转成组件、路由、状态 / API 映射及响应式、可访问性、错误处理与验收要求。缺失或冲突回相应产品 / 设计阶段，不用技术设计擅自补业务能力。
5. 涉及 Java 持久化时按 [公共 Java 规则](../qwerdf-common/java-coding-rules.md#spring-事务与持久化涉及数据库时) 定义 MyBatis Mapper / XML、事务与行锁边界。涉及 SQL / migration 时维护执行计划；不涉及按共享适用性规则说明。
6. 维护 `tech/dependency-readiness.md`：实际依赖、对应任务、编码 / 验证用途、真实资源、检查方式、状态与证据，区分已具备输入和后续验证限制。禁止模拟替代，不将待生成产物列为准备任务自己的输入。
7. 按共享任务规则确定唯一权威源，交付 `tech/task-slices.md` 的前后端有序清单 / 派生视图及联调验收范围。按独立可核验业务动作拆解，引用输入、归属、可观察结果、必要异常 / 安全要求及最小验证。优先闭合当前业务结果，必要准备单列；评估 [文档规模](../qwerdf-common/artifact-lifecycle.md) 后再决定是否拆分，不按 helper 或文件数量拆任务。
8. 交接自检：需求覆盖与既有代码证据；权威源及视图一致性；前后端各自顺序可执行、可按契约并行开发；必要准备有实际归属与产物；联调 / 测试范围及相关实现明确；本轮契约可落地且设计交接结论成立；各片最小验证与必要 UI / SQL / 安全约束不缺。已有任务只调整受影响范围，保留稳定 ID 或映射，不整表重置，不重写实现。
9. 在技术方案回填交接结论与风险，作废受影响的旧“完成”判断。分开汇报设计可交接性、编码输入就绪与未执行验证；不以文件齐全或依赖 ready 替代落地依据。仅检查不开发；已有后续开发授权且交接及对应动作 gate 满足才继续实现。

## 输出摘要

```text
技术设计状态: <本轮范围可交接 / 部分待补 / 阻断及依据>
目录与变更: <当前方案及实际更新的适用文档，不罗列空产物>
设计依据与未决项: <关键链路定位、决定性缺口和影响范围>
仓库、分支与版本: <引用 tech-plan 中已确认的记录，指出尚缺确认的部分；不另维护副本>
任务与顺序: <权威源、Markdown 视图同步情况；前 / 后端起始任务及可并行部分>
依赖与验证: <适用编码输入；待验证资源及尚未执行的检查>
范围核对: <本期改动、仅影响记录、待确认变化>
下一步: <遵循原授权；不把设计检查直接转成开发>
```
