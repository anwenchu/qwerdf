---
name: pd-test
description: >-
  测试验证工作流，基于 PRD、技术方案、SQL 执行计划、前后端实现和联调结果制定并执行 unit、integration、e2e、visual/UI regression、regression、manual acceptance 测试，在一份报告中维护测试计划、用例、结果和回归范围；涉及 SQL / migration 时记录测试环境执行验证。Use when the user mentions $pd-test、pd-test、测试验证、生成测试计划、执行测试、回归测试、验收测试、SQL执行验证。
---

# $pd-test — 测试验证

按风险选择并执行足够的测试验证。

## 读取

默认从需求、方案、任务三份主文档的相关章节恢复上下文。下列旧分文件仅在已存在且是有效事实源、或确需独立消费时读取；同样内容已在主文档时不补建文件、不复制正文。真正缺失的契约 / 输入 / 证据仍保留缺口。

1. 定位本 `SKILL.md` 目录为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage test`，只加载本阶段共享规则和模板（Python 3.10+，无第三方依赖）。不可运行时，按 [共享流程](../qwerdf-common/product-delivery-flow.md) 对应章节与下列模板手动读取；不通读无关阶段。
2. 上述输出只含 `test/test-report.md`；计划、用例、结果和回归是同一报告的章节。
3. 读取 PRD 验收、技术方案、任务中的实现 / UI 检查证据和适用联调报告；SQL 需要独立执行清单时引用它，既有独立事实源按需读取。
   如本轮确需补读实时 Figma，先加载对应操作技能和 [共享连接规则](../qwerdf-common/product-delivery-flow.md#figma-连接与会话复用)，再补齐当前工具的连接参数、恢复已选连接及本任务会话；仅本地页面 / 截图验证不主动连接 Figma。
4. 识别项目已有测试框架和 `package.json` / 构建工具 / 测试命令。
5. 如当前目录是 git 仓库，读取 `.gitignore`、`git status --short` 和必要时的 ignored / untracked 状态。
6. 按 [共享目录规则](../qwerdf-common/product-delivery-flow.md#2-默认工作目录) 先确定本次独立任务根目录，以下阶段路径相对于该目录。

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
4. 在 `test/test-report.md` 的计划章节，按风险选择 unit、integration、e2e、visual/UI regression、regression、manual acceptance，并包含真实依赖验证、Mock 禁用检查和 SQL 执行验证。
5. 在同一报告记录必要验收用例、预期与验证方式，引用现有自动化用例，不复制全部测试代码。
6. 按 [共享验证规则](../qwerdf-common/product-delivery-flow.md#验证与审查) 核对已有证据的输入、产物及实际覆盖，复用仍有效结果，集中补验缺失或受变化影响的范围；核实验证入口，遵守同一循环的重跑依据及超时退出条件，不因进入测试阶段自动重跑全部开发检查。integration / e2e / acceptance 必须连接真实依赖或真实本地容器，原定回归与正式验收缺口仍须补齐。
7. 执行测试前后采集 `git status --short`；如测试、构建或浏览器验证产生新文件，判断它们是应提交产物、应忽略产物还是无关噪声。
8. 对照 `.gitignore` 和 `git ls-files --others --exclude-standard` 检查未跟踪但未忽略的构建产物、缓存、截图、日志、报告或临时文件；发现应忽略但未忽略的文件时写入风险，不把它们算作测试通过证据。
9. 写入 `test/test-report.md`，记录命令、结果、证据、联调前置状态、真实依赖验证、Mock 禁用检查、SQL 执行验证和 Git / ignore 检查：新增或变化文件、应提交候选、应排除候选、可能漏提交和可能多提交。
10. 失败、跳过或无法执行的验证必须写入 `test/test-report.md` 的未执行 / 未覆盖部分。
11. 在同一报告的回归章节说明覆盖、未覆盖及残余风险，不另生成三份伴随材料。

## 输出摘要

```text
测试验证完成: <name>
目录: <output-dir>
文件:
  - test/test-report.md
结论: <本轮执行范围、单项通过 / 未通过 / 未执行；整体通过与否及依据>
下一步: <可先做只读 $pd-review；整体缺口回对应阶段，不放行提交>
```
