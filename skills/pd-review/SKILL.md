---
name: pd-review
description: >-
   Code Review 工作流，基于 git diff、PRD、UI 设计系统、技术方案、前后端契约、联调报告、测试报告和 ui-review-report 做提交前结构化审查，并深入逐文件检查代码正确性、安全、性能、数据一致性、UI 质量、可维护性和测试质量，按 P0/P1/P2/P3 输出带证据、修复归属和验证建议的 findings。Use when the user mentions $pd-review、pd-review、Code Review、代码审查、代码级审查、提交前审查、审查改动、review 当前实现。
---

# $pd-review — Code Review

Codex Product Delivery Skill：在提交前审查实现质量和交付风险。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `test/code-review.md` 的模板。
3. 读取 `product/prd.md`、`product/requirements.md`、`product/acceptance-criteria.md`、`ui/ui-design-system.md`、`ui/ui-screens.md`、`ui/ui-components.md`、`ui/figma-handoff.md`、`ui/ui-review-report.md`（如存在）、`tech/tech-plan.md`、`tech/api-contract.md`、`tech/integration-map.md`、`tech/task-slices.md`、`sync/integration-report.md`、`test/test-report.md`、前后端实现记录、changed files、dev notes、当前 git diff 和 git status。
4. 如果当前目录是 git 仓库且存在 diff，先运行本 skill 自带脚本 `scripts/diff_triage.py`，将目标仓库的 `git diff --no-ext-diff --unified=80` 通过 stdin 传入；用输出决定审查顺序、风险标签和需要加载的 references。
5. 根据 diff 技术栈渐进式加载 references：
   - 任意代码级 review：读取 [Universal Code Quality](references/universal-code-quality.md)。
   - 涉及 TypeScript / React / 前端状态 / API client / CSS 布局：读取 [Frontend Code Review](references/frontend-code-review.md)。
   - 涉及 UI、样式、组件、页面、Figma handoff、frontend-acceptance 或响应式：读取 [UI Review Rules](../qwerdf-common/ui-review-rules.md) 和 [UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)。
   - 涉及 Java / Spring Boot / SQL / 数据模型 / 后端 API：读取 [Backend Code Review](references/backend-code-review.md)。
   - 涉及权限、输入、外部调用、日志、敏感字段、数据写入或性能敏感路径：读取 [Security & Performance Review](references/security-performance-review.md)。
6. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 默认只审查，不修改代码。
- 不提交代码。
- 需要修复时，按问题归属回到 `$pd-fe`、`$pd-be`、`$pd-plan`、`$pd-sync` 或 `$pd-test`。
- Findings 必须能定位到文件、区域、契约条目、测试证据或产物段落；证据不足时标记为待确认，不升级成确定问题。
- `sync/integration-report.md` 或 `test/test-report.md` 缺失、未通过或证据不足时，不得输出“可提交 / 可进入 $pd-git”；必须作为阻断或残余风险写入 Code Review。
- 不把格式化、import 顺序、简单 lint 或类型风格问题作为主要 finding，除非它们导致真实行为风险；这类问题优先交给 formatter、linter、typecheck。
- `$pd-review` 重点关注自动化工具难以发现的问题：业务语义、契约偏差、边界条件、权限、安全、并发、数据一致性、可维护性和测试有效性。
- UI diff 不只看视觉偏好；必须对照 `ui/ui-design-system.md`、产品类型、Figma handoff、frontend-acceptance、截图 / 浏览器证据和用户任务。
- `$pd-ui-review` 是独立设计稿 / 截图 / 页面视觉审查入口；如存在 `ui/ui-review-report.md`，必须把其中未解决 P0/P1 作为阻断或残余风险，不用代码级审查覆盖掉独立 UI finding。
- 如果 lint / typecheck / test 未执行或失败，按证据缺口或阻断项记录，不伪造通过。

## 审查类别优先级

| 优先级 | 类别 | 检查重点 |
| --- | --- | --- |
| 1 | 需求与契约 | 是否偏离 PRD、验收标准、API 契约、权限和状态规则 |
| 2 | 正确性 | 错误处理、边界条件、并发、幂等、数据一致性 |
| 3 | 安全与隐私 | 越权、敏感数据、日志泄露、输入校验 |
| 4 | UI 设计质量 | 设计系统一致性、产品类型匹配、信息层级、响应式、可访问性、状态覆盖 |
| 5 | 前端质量 | 状态覆盖、可访问性、响应式、重渲染、bundle 和组件 API |
| 6 | 后端质量 | 分层边界、事务、错误码、观测、资源使用 |
| 7 | 测试缺口 | 哪些验收标准、风险或回归路径未被验证 |

## 严重性分级

- `P0`: 会导致核心流程不可用、数据损坏、严重安全漏洞、不可恢复迁移问题，或提交后无法启动。
- `P1`: 会导致主流程错误、权限绕过、契约破坏、明显数据不一致，或关键测试缺失。
- `P2`: 边界场景错误、可维护性明显下降、性能风险、非核心流程体验问题，或测试覆盖不足。
- `P3`: 命名、结构、可读性、轻量重构建议，不阻断提交。
- 不允许把没有证据的猜测升级为 `P0` / `P1`；证据不足时标记为“待确认”或残余风险。

UI 严重性补充：

- `P0`: UI 导致核心流程不可用、关键页面白屏、主操作被遮挡、提交卡死或移动端核心流程无法操作。
- `P1`: 关键状态缺失、设计系统严重漂移、移动端严重横向溢出、表单错误无法定位、视觉层级误导主流程或图表口径误导。
- `P2`: 边界状态缺失、局部响应式问题、非核心信息层级不清、组件 API 复杂度升高、截图 / 浏览器证据不足。
- `P3`: 不阻断的局部间距、文案一致性、命名或轻量视觉调整。

## 产品范围漂移检查

- 对照 PRD、product-brief、UI 蓝图和 Figma handoff，检查实现或设计是否新增未授权页面、导航、tab、资产类型、业务模块、交易品类、活动入口或参考产品文案。
- 发现来自竞品 / 截图 / Figma 参考但不属于产品事实源的内容时，按需求一致性问题处理；影响主流程或对外可见时至少标为 P1。
- 不能用“参考图里有”作为产品范围证据；必须能指向 PRD、product-brief、requirements、用户明确确认或现有系统事实。

## 大 Diff 处理

- 先用 `scripts/diff_triage.py` 对 diff 做确定性分组，输出文件规模、风险标签、推荐 references 和 review order。
- 如果 diff 过大，先按模块、风险和入口分组，不要泛泛审查。
- 优先审查入口层、边界层、共享模块、数据写入、权限判断、外部调用、错误处理、迁移和测试断言。
- 对低风险纯样式、文案、生成文件或自动格式化改动，记录范围并抽样确认；不要让它们挤占核心风险审查。

## 审查流程

按四阶段推进：上下文收集、高层审查、代码 / UI 审查、结论决策；前置证据检查和报告写入是执行门禁，以下步骤是执行展开。

1. 上下文收集：读取 PRD、技术方案、API 契约、integration-map、task-slices、联调报告、测试报告、实现记录、changed files、git diff 和 git status；运行 `scripts/diff_triage.py` 生成 diff triage；识别 diff 触及的语言 / 框架并按需读取 references。
2. 前置证据检查：`sync/integration-report.md` 必须通过或明确不适用，`test/test-report.md` 必须通过且无未解释高风险缺口；缺失或未通过时先输出阻断 finding，并把下一步指向 `$pd-sync` 或 `$pd-test`，不进入 `$pd-git`。
3. 高层审查：判断范围是否正确、架构是否贴合方案、文件组织是否合理、契约是否一致、测试策略是否覆盖主风险。
4. UI 设计质量审查：涉及 UI diff 时，对照 `ui/ui-design-system.md`、Figma handoff、frontend-acceptance 和浏览器 / 截图证据，检查设计系统一致性、产品类型匹配、信息层级、响应式、可访问性、状态覆盖、表单 / 表格 / 图表质量。
5. 代码级审查：按文件和 diff 逐段检查正确性、安全、性能、数据一致性、错误处理、状态覆盖、复用、可维护性和测试质量；新增 helper / service / component 前必须搜索相邻模块和 shared 目录是否已有可复用能力。
6. 结论与决策：列出 `P0` / `P1` / `P2` / `P3` findings，按严重程度排序；每个 finding 标明文件 / 区域、影响、修复归属和验证建议。
7. 写入 `test/code-review.md`。
8. 无问题时明确说明“未发现阻断问题”，并列出残余风险、未覆盖范围和仍依赖的自动化 / 人工验证。

## 输出要求

- Findings 优先，按 `P0` / `P1` / `P2` / `P3` 排序。
- 每个 finding 必须有文件、区域、契约条目、测试证据或产物段落；不能只写泛泛建议。
- 每个 `P0` / `P1` 必须给出修复归属：`$pd-fe`、`$pd-be`、`$pd-plan`、`$pd-sync` 或 `$pd-test`。
- 每个 finding 必须给出验证建议，例如应补哪个单测、集成测试、E2E、浏览器验证或 API 测试。
- UI finding 必须给出设计系统 / Figma / 截图 / 视口 / 组件路径 / 验收清单证据；不能只写“看起来不美观”。
- 如果联调报告或测试报告缺失 / 失败，不得输出“可进入 $pd-git”。
- `test/code-review.md` 必须记录 diff triage 摘要：总文件数、增删行、风险标签、推荐 references 和优先审查文件。
- `test/code-review.md` 必须记录 UI Review 摘要；没有 UI diff 时写明“不适用”和依据。
- 没有发现问题时，也要说明未发现阻断问题，并列出残余风险和未覆盖范围。

## 输出摘要

```text
Code Review 完成: <name>
目录: <output-dir>
文件:
 - test/code-review.md
结论: <无阻断 / 有 P0 / 有 P1 / 有建议项>
下一步: <无阻断且联调 / 测试通过则用 $pd-git；否则回到 $pd-sync / $pd-test / 修复阶段>
```
