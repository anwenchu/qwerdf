---
name: pd-test
description: >-
  测试验证工作流，基于 PRD、技术方案、SQL 执行计划、前后端实现和联调结果制定并执行 unit、integration、e2e、visual/UI regression、regression、manual acceptance 测试，输出测试计划、用例、报告和回归说明；涉及 SQL / migration 时记录测试环境执行验证。Use when the user mentions $pd-test、pd-test、测试验证、生成测试计划、执行测试、回归测试、验收测试、SQL执行验证。
---

# $pd-test — 测试验证

按风险选择并执行足够的测试验证。

## 读取

下列项目材料只读取本轮适用的当前段落；缺少实际必需输入保留缺口，无关端、UI 或 SQL 不要求补造文件。

1. 定位本 `SKILL.md` 目录为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage test`，只加载本阶段共享规则和模板（Python 3.10+，无第三方依赖）。不可运行时，按 [共享流程](../qwerdf-common/product-delivery-flow.md) 对应章节与下列模板手动读取；不通读无关阶段。
2. 上述输出已包含 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `test/test-plan.md`、`test/test-cases.md`、`test/test-report.md`、`test/regression-notes.md` 的模板；只采用本轮适用项。
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
- 执行时机、单项结果与整体通过按 [共享验证规则](../qwerdf-common/product-delivery-flow.md#验证与审查) 区分：联调 / 环境缺口不阻止独立、获准且输入齐备的测试，不得把部分通过说成整体通过。可提前做只读审查；提交仍须正式门禁。
- 测试通过证据来自真实代码及适用真实依赖；mock / stub / fake / fixture-only / 测试替身 / simulator 不作为通过证据。
- SQL 只在适用范围核对执行计划与授权。涉及 SQL 而计划缺失回 `$pd-plan` 补齐；无 SQL 可引用技术方案的“不涉及”依据。必要 SQL 未执行 / 未验证的用例保留未通过，不要求无 SQL 的路径引入数据库。

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

1. 核对本轮范围及联调适用性，读取已有 `sync/integration-report.md`；缺失 / 未通过先记录对整体验收的影响，继续识别不依赖该缺口的测试，不只生成阻断说明就结束。
2. 按每个用例实际消费的输入读取依赖准备与 Mock 禁用证据；输入缺失停止该用例，执行其余具备条件且获准的检查。缺失依赖清单需补证，不把状态未知的依赖当 ready。
3. 按技术方案判断 SQL 适用性；有 SQL 时读取执行计划，把相关 SQL ID 纳入计划 / 报告，无 SQL 引用不涉及依据。
4. 生成 `test/test-plan.md`，按风险选择 unit、integration、e2e、visual/UI regression、regression、manual acceptance，并包含真实依赖验证、Mock 禁用检查和 SQL 执行验证。
5. 生成 `test/test-cases.md`。
6. 执行项目可用的最小测试、构建、已获准的 SQL / migration 测试环境执行或浏览器验证；integration / e2e / acceptance 必须连接真实依赖或真实本地容器。
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
结论: <本轮执行范围、单项通过 / 未通过 / 未执行；整体通过与否及依据>
下一步: <可先做只读 $pd-review；整体缺口回对应阶段，不放行提交>
```
