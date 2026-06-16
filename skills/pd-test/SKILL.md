---
name: pd-test
description: >-
  测试验证工作流，基于 PRD、技术方案、SQL 执行计划、前后端实现和联调结果制定并执行 unit、integration、e2e、visual/UI regression、regression、manual acceptance 测试，输出测试计划、用例、报告和回归说明；涉及 SQL / migration 时记录测试环境执行验证。Use when the user mentions $pd-test、pd-test、测试验证、生成测试计划、执行测试、回归测试、验收测试、SQL执行验证。
---

# $pd-test — 测试验证

Codex Product Delivery Skill：按风险选择并执行足够的测试验证。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `test/test-plan.md`、`test/test-cases.md`、`test/test-report.md`、`test/regression-notes.md` 的模板。
3. 读取 `product/prd.md`、`product/acceptance-criteria.md`、`tech/tech-plan.md`、`tech/dependency-readiness.md`、`tech/backend/sql-execution-plan.md`、`sync/integration-report.md`、`tech/frontend/frontend-acceptance.md` 和实现记录。
4. 识别项目已有测试框架和 `package.json` / 构建工具 / 测试命令。
5. 如当前目录是 git 仓库，读取 `.gitignore`、`git status --short` 和必要时的 ignored / untracked 状态。
6. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 优先使用项目已有测试框架和脚本。
- 不引入新测试框架，除非用户明确要求。
- 不大范围修复业务代码；发现问题时记录并回到 `$pd-fe` 或 `$pd-be`。
- 未执行的测试必须单独列出原因和风险，不得合并写成通过。
- 不执行 `git add`、`git commit` 或修改 `.gitignore`，除非用户明确要求；默认只记录 gitignore / 工作区风险。
- `sync/integration-report.md` 缺失、联调未通过或未明确“不适用并说明原因”时，不得把测试结论写成通过，不得建议进入 `$pd-review` 或 `$pd-git`。
- `tech/dependency-readiness.md` 缺失、必需依赖不是 `ready` / `not-required`、或联调报告存在 `mock-only` / Mock 禁用检查未通过时，不得把测试结论写成通过，不得建议进入 `$pd-review` 或 `$pd-git`。
- 测试通过证据必须来自真实依赖、真实 API、真实数据库或明确不需要外部依赖的代码路径；mock server、stub client、fake adapter、fixture-only 数据、测试替身或 simulator 不得作为任何测试通过证据。
- `tech/backend/sql-execution-plan.md` 缺失时，不得忽略 SQL 风险；必须在 `test/test-report.md` 标为证据缺口并建议回到 `$pd-plan`。
- 存在 SQL 执行项但未在测试环境执行或未验证时，不得把相关测试结论写成完全通过；必须记录未执行原因、风险和后续处理。

## 测试决策树

```text
验证目标
├─ 有确定业务验收标准？
│  ├─ 否：先回到 PRD / 蓝图补验收标准
│  └─ 是：继续
├─ 是代码逻辑、接口契约还是 UI 行为？
│  ├─ 代码逻辑：优先 unit / integration
│  ├─ 接口契约：优先 API integration / contract check
│  └─ UI 行为：优先浏览器验证，先侦察渲染态再执行操作
└─ 环境不可用？
   ├─ 是：记录未执行项、原因、风险和人工验证方式
   └─ 否：执行最小高价值测试并保存证据
```

## 流程

1. 先检查 `sync/integration-report.md`：联调必须通过，或明确“不适用”且说明原因；否则只生成测试阻断说明，并提示回到 `$pd-sync` / `$pd-fe` / `$pd-be` / `$pd-plan`。
2. 读取 `tech/dependency-readiness.md` 和 `sync/integration-report.md` 的“真实依赖验证” / “Mock 禁用检查”；任一必需依赖为 `unknown` / `blocked` / `mock-only` 或 Mock 禁用检查未通过时，只生成测试阻断说明。
3. 读取 `tech/backend/sql-execution-plan.md`：无 SQL 时记录“不涉及”；有 SQL 时把每条 SQL ID 纳入 `test/test-plan.md` 和 `test/test-report.md` 的验证范围。
4. 生成 `test/test-plan.md`，按风险选择 unit、integration、e2e、visual/UI regression、regression、manual acceptance，并包含真实依赖验证、Mock 禁用检查和 SQL 执行验证。
5. 生成 `test/test-cases.md`。
6. 执行项目可用的最小测试、构建、SQL / migration 测试环境执行或浏览器验证；integration / e2e / acceptance 必须连接真实依赖或真实本地容器。
7. 执行测试前后采集 `git status --short`；如测试、构建或浏览器验证产生新文件，判断它们是应提交产物、应忽略产物还是无关噪声。
8. 对照 `.gitignore` 和 `git ls-files --others --exclude-standard` 检查未跟踪但未忽略的构建产物、缓存、截图、日志、报告或临时文件；发现应忽略但未忽略的文件时写入风险，不把它们算作测试通过证据。
9. 写入 `test/test-report.md`，记录命令、结果、证据、联调前置状态、真实依赖验证、Mock 禁用检查、SQL 执行验证和 Git / ignore 检查：新增或变化文件、应提交候选、应排除候选、可能漏提交和可能多提交。
10. 失败、跳过或无法执行的验证必须写入 `test/test-report.md` 的未执行 / 未覆盖部分。
11. 写入 `test/regression-notes.md`，说明覆盖范围、未覆盖范围和残余风险。

## 输出摘要

```text
测试验证完成: <name>
目录: <output-dir>
文件:
  - test/test-plan.md
  - test/test-cases.md
  - test/test-report.md
  - test/regression-notes.md
结论: <通过 / 未通过 / 有残余风险>
下一步: <通过则用 $pd-review；否则回到 $pd-sync / $pd-fe / $pd-be / $pd-plan>
```
