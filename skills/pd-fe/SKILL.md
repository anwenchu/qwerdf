---
name: pd-fe
description: >-
  前端开发实现工作流，基于 pd-plan 的 frontend-design、ui-design-system、api-contract、dependency-readiness、integration-map 和 task-slices，逐个实现 frontend 或 shared-frontend 任务切片，每个切片执行真实依赖 gate、最小前端与 UI 质量验证。Use when the user mentions $pd-fe、pd-fe、前端开发、前端实现、实现前端 slice、按技术方案写前端、前端UI验收、真实依赖阻断。
---

# $pd-fe — 前端开发实现

Codex Product Delivery Skill：按技术设计逐片实现，每个迭代闭合一个前端 task slice。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `frontend-*` 模板及 [共享业务进度摘要](../qwerdf-common/engineering-contracts.md#业务进度摘要)。任务选择、blocked 恢复和汇报按 [共享业务推进规则](../qwerdf-common/product-delivery-flow.md#业务推进阻断恢复与进度汇报) 执行。
   API 接入与任务范围按 [技术设计依据与范围规则](../qwerdf-common/technical-design-rules.md) 核对；关键参数 / 字段语义需猜测时回 `$pd-plan` 补证，不自行扩展契约或产品能力。
3. 读取 [UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)、[UI Patterns](../qwerdf-common/ui-patterns.md) 和 [UI Design System Rules](../qwerdf-common/ui-design-system.md)。
4. 读取 `tech/tech-plan.md`、`tech/frontend/frontend-design.md`、`tech/frontend/frontend-component-map.md`、`tech/frontend/frontend-route-map.md`、`tech/frontend/frontend-state-api.md`、`tech/api-contract.md`、`tech/dependency-readiness.md`、`tech/integration-map.md`、`tech/task-slices.md`、`ui/ui-design-system.md`、`ui/figma-handoff.md`，以及其中关联的未决项 / 设计检查记录。
   必须补读 Figma 原稿时，先加载当前环境中对应的 Figma 设计转代码技能并遵守其工具前置要求，连接选择与有效 session 按 [共享复用规则](../qwerdf-common/product-delivery-flow.md#figma-连接与会话复用) 执行，不因加载规范重新核查其他账号。已有材料不足时保留证据缺口，不用猜测或重复授权替代。
5. 如存在，读取 `sync/integration-report.md`、`sync/api-mismatch.md`、`test/test-report.md`、`test/code-review.md`、`ui/ui-review-report.md` 中归属 `$pd-fe` 的 findings。
6. 识别前端项目结构：`package.json`、路由、页面目录、组件目录、状态管理、API client、样式体系、测试命令。
7. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 每个实现迭代只执行一个 `frontend` 或 `shared-frontend` slice；连续执行的授权与迭代边界沿用共享业务推进规则。
- 可执行范围默认是一个具备条件的本端 `pending` 或本轮继续处理的 `in_progress` slice；`blocked` 须先按共享规则核实恢复，不因状态标签永久停工；例外是联调、测试或审查中的单个 `implementation-defect`，且必须有契约 / UI 设计证据、实现证据和已有 `frontend` / `shared-frontend` slice。独立 UI 报告的读取、分类与重开条件统一见 [UI finding 修复交接](../qwerdf-common/ui-review-rules.md#6-ui-finding-修复交接)。
- 只更新自己负责的 slice 状态，不修改后端 slice。
- 不修改后端接口、数据库、权限模型、后端服务逻辑。
- 不处理 `contract` 类型任务；发现契约问题时阻塞并记录，不单方面改契约。
- 漏项先按 [共享分类规则](../qwerdf-common/technical-design-rules.md#工程漏项与业务决策分类) 定向补查：既有契约已明确、属于本端已有 slice 的工程遗漏直接补齐并验证；需修订契约 / 设计 / 任务覆盖时沿用上游回退，不自行改契约，也不把内部修订自动变成用户审批。身份与资金安全条件始终保留。
- 开始编码或重开缺陷 slice 前按 [共享交接规则](../qwerdf-common/technical-design-rules.md#3-交付应足以让实现者执行) 复核本轮设计范围与目标 slice；即使任务已标 `done`、依赖已 ready，本轮交接范围的设计仍有冲突 / 决定性缺口时也不得进入实现，须回 `$pd-plan`。用户只要求检查时，不启动开发。
- 如果前端 slice 的唯一阻塞是 `pending` / `blocked` 的 `contract` slice，视为 `$pd-plan` handoff 问题：停止实现并建议回到 `$pd-plan` 修订；不要把工程初始化误判为前端不可执行。
- 通过共享交接核查、本轮交接范围内所有 `contract` slice 已为 `done`，且当前前端 slice 是项目初始化 / 前端骨架创建时，允许从空仓库执行；仍须满足该 slice 的依赖 gate。
- 如果前端缺陷来自真实联调 / 测试 / review，且契约或 UI 设计事实源已存在、归属 slice 已存在但状态为 `done`，允许进入缺陷修复模式：临时重开该 slice 为 `in_progress` 或在实现记录中标明同 slice 修复，修复后重新验证并标回 `done`。
- 如果 finding 被标为 `slice-missing`、无法映射到已有前端 slice，或需要新增 / 修改 API 契约、页面范围、路由、UI 设计系统、Figma handoff 或任务范围，必须停止并回到 `$pd-plan` / `$pd-figma`；不得自行新造前端任务或改上游事实源。
- 开始目标 slice 前必须检查 `tech/dependency-readiness.md`：适用该 slice 的依赖只有 `ready` / `not-required` 才可进入开发；`unknown` / `blocked` / `mock-only` 必须停止并记录阻断，不得标 `done`。
- 开发进度不得依赖联调任务。若目标 `frontend` / `shared-frontend` slice 的 `blocked-by` 包含 `SYNC-*`，判定为 `$pd-plan` 依赖建模错误，报告 `over-constrained-slice` 并要求修正为“前端实现与后端实现并行，相关实现 slice 全部 `done` 后再执行 `SYNC-*`”；不要等待联调任务解锁开发。
- 前端开发不依赖后端业务实现进度。按 [共享并行开发规则](../qwerdf-common/product-delivery-flow.md#frontend--backend-并行开发规则) 区分本端工程前置、共享产物准备和联调验收；存在对端业务实现阻塞时记录 `over-constrained-slice` 回 `$pd-plan`，不等待对端完成，也不绕过真正的工程准备。
- 真实后端未完成不是前端编码阻断；前端可基于 `tech/api-contract.md`、`tech/frontend/frontend-state-api.md`、UI 设计系统和真实 API client 实现页面，并验证 loading / empty / error / permission / service-unavailable 状态。真实成功链路只能由 `$pd-sync` 验证，不得用 mock 成功数据冒充。
- 技术实现禁止使用任何 mock；不得实现或保留 mock API client、mock server、stub adapter、fake data source、fixture-only 数据流、Storybook / demo 数据路径或 contract simulator，发现时只能记录为阻断或 `implementation-defect`。
- 发现本 slice 的生产路径仍是 mock/stub/fake，或应有的真实 API client 未实现 / 未接入时，归类为依赖阻断或 `implementation-defect`，不得把 slice 标为 `done`；环境地址待填与本端完成条件统一按 [共享并行开发规则](../qwerdf-common/product-delivery-flow.md#frontend--backend-并行开发规则) 判断，不仅凭缺少部署地址判实现失败。
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
7. UI 质量：本次目标平台布局、文本不重叠、设计系统一致性及适用状态的证据进入 `frontend-acceptance.md`；状态适用性按 [共享质量清单](../qwerdf-common/ui-quality-checklist.md#4-适用的状态与交互)，不适用写明理由。
8. 管理后台 / SaaS / CRM / 操作台：优先信息密度、扫描效率、稳定布局和可重复操作；不要把页面改成营销 hero、大面积装饰或低密度展示卡片。

## 流程

1. 先按共享分类规则补查并区分工程漏项、契约缺口与业务未决，再按共享交接规则核对当前请求、设计交接结论和关联缺口记录；未通过时报告设计阻断，不写前端代码。通过后判断是否存在用户指定或报告中归属 `$pd-fe` 的缺陷修复项。
2. 若存在缺陷修复项，先验证它是否满足缺陷修复模式：分类为 `implementation-defect`，契约证据能在 `tech/api-contract.md` / `tech/integration-map.md` 找到或 UI 证据能在 `ui/ui-design-system.md` / `ui/figma-handoff.md` 找到，实现证据指向前端代码、浏览器截图、console、网络请求或测试结果，且能映射到已有 `frontend` / `shared-frontend` slice。独立 UI finding 按共享交接规则在此核对分类和映射，不因原报告没有工程字段而拒绝修复。
3. 合法缺陷修复项可重开归属 slice 为 `in_progress` 或在实现记录中写明同 slice 修复；不合法时停止并说明应回 `$pd-plan` / `$pd-figma` 的原因，尤其是 `slice-missing` 或上游事实源需要变更。
4. 如果不是缺陷修复模式，按共享业务推进规则，从 `tech/task-slices.md` 选择当前里程碑的下一个可执行前端 slice，优先继续本轮已开启且仍可执行的任务。类型为 `frontend` / `shared-frontend`，状态为 `pending`（含依证恢复的 blocked）或本轮有权继续的 `in_progress`，且 `blocked-by` 为空或引用的 slice 全部为 `done`；blocked 必须先核查所有原阻断及当前交接 / 依赖条件再恢复，不能直接改标签解锁。已有明确顺序时不要求用户重选；无法判断时再澄清。
5. 若没有可执行前端 slice，先检查是否存在未完成 `contract` slice 阻塞实现；存在时报告 `$pd-plan` handoff 问题，不修改契约，不写前端代码。若前端 slice 的阻塞来自 `SYNC-*`，报告 `over-constrained-slice`，要求 `$pd-plan` 删除开发任务对联调任务的依赖，并改成相关实现 slice 全部 `done` 后再执行 `SYNC-*`。若存在对端业务实现的阻塞，按共享并行开发规则记录 `over-constrained-slice`，回 `$pd-plan` 同步修正任务依赖、依赖清单和验证要求，不自行把共享产物准备当成对端整块业务实现的例外。若只有联调 / 测试 / review 缺陷但缺少归属 slice，报告 `slice-missing` 并回 `$pd-plan`。
6. 检查 `tech/dependency-readiness.md` 中适用目标 slice 的依赖状态；任一必需依赖为 `unknown` / `blocked` / `mock-only` 时，停止开发，保持 `pending` 或标 `blocked` 并写明依赖 ID、阻断原因和下一步，不进入 `in_progress`。
7. 将目标 slice 状态更新为 `in_progress`。
8. 对照 `ui/ui-design-system.md`、`ui/figma-handoff.md` 和当前 slice 的验证列，确认本次 UI 质量验收点；缺失时记录为 `$pd-plan` handoff 缺口，不自行发明设计规则。
9. 按现有项目模式实现页面、组件、状态、真实 API client、真实接口切换或前端校验；不得引入 mock client、mock server、stub、fake、fixture-only 数据或 simulator。
10. 扫描本 slice 是否残留 mock/stub/fake 命名、mock-only 配置、fixture-only 数据、Storybook / demo 数据路径或强制 mock 开关；发现后停止并记录为阻断或实现缺陷，不标 `done`。
11. 执行项目已有的最小前端检查、测试或构建命令；缺陷修复必须至少复现或覆盖原 finding 的验证路径。
12. 按当前 slice 的验收点做浏览器或组件级验收，检查目标平台布局、无横向溢出、无文本重叠、适用状态及设计系统一致性。状态引用共享质量清单；没有可运行环境时记录未验证项与影响，不用组件样例替代必要的真实页面验证。
13. 写入 `tech/frontend/frontend-implementation-log.md`、`tech/frontend/frontend-changed-files.md`、`tech/frontend/frontend-dev-notes.md`、`tech/frontend/frontend-acceptance.md`；缺陷修复必须填写“修复来源”，依赖阻断必须填写依赖 ID 和 `tech/dependency-readiness.md` 证据；`over-constrained-slice` 必须写明被过度阻塞的 `FE-*`、相关 `BE-*`、为什么不是前端开发依赖，以及建议回 `$pd-plan` 修正后的依赖形态。
14. 成功后将该 slice 状态更新为 `done`；阻塞时更新为 `blocked` 并说明原因、证据和建议回到的 skill。 每个迭代回填共享业务进度摘要；未实现、契约缺口和验证阻塞分别说明，不能以测试数或切片计数代替业务进展。

## 输出摘要

```text
前端 slice / 缺陷修复状态: <slice-id；完成 / 阻断 / 未执行，按实际证据填写>
业务推进: <按共享业务进度摘要填写目标、实现与接线、验证、剩余与阻断；不估算整体百分比>
目录: <output-dir>
文件:
  - tech/frontend/frontend-implementation-log.md
  - tech/frontend/frontend-changed-files.md
  - tech/frontend/frontend-dev-notes.md
  - tech/frontend/frontend-acceptance.md
验证:
  - <命令 / 结果>
下一步: <完成后继续前端 slice 或按门禁进入 $pd-sync；阻断时说明缺口及修复归属，不宣称完成>
```
