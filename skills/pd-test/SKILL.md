---
name: pd-test
description: >-
  个人测试验证工作流，基于 PRD、技术方案、前后端实现和联调结果制定并执行 unit、integration、e2e、visual/UI regression、regression、manual acceptance 测试，输出测试计划、用例、报告和回归说明。Use when the user mentions $pd-test、pd-test、测试验证、生成测试计划、执行测试、回归测试、验收测试。
---

# $pd-test — 测试验证

个人辅助 Skill：按风险选择并执行足够的测试验证。

## 读取

1. 读取 [个人 Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `test-plan.md`、`test-cases.md`、`test-report.md`、`regression-notes.md` 的模板。
3. 读取 `prd.md`、`acceptance-criteria.md`、`tech-plan.md`、`integration-report.md`、`frontend-acceptance.md` 和实现记录。
4. 识别项目已有测试框架和 `package.json` / 构建工具 / 测试命令。
5. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 优先使用项目已有测试框架和脚本。
- 不引入新测试框架，除非用户明确要求。
- 不大范围修复业务代码；发现问题时记录并回到 `$pd-fe` 或 `$pd-be`。
- 未执行的测试必须单独列出原因和风险，不得合并写成通过。

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

1. 生成 `test-plan.md`，按风险选择 unit、integration、e2e、visual/UI regression、regression、manual acceptance。
2. 生成 `test-cases.md`。
3. 执行项目可用的最小测试、构建或浏览器验证。
4. 写入 `test-report.md`，记录命令、结果和证据。
5. 失败、跳过或无法执行的验证必须写入 `test-report.md` 的未执行 / 未覆盖部分。
6. 写入 `regression-notes.md`，说明覆盖范围、未覆盖范围和残余风险。

## 输出摘要

```text
测试验证完成: <name>
目录: <output-dir>
文件:
  - test-plan.md
  - test-cases.md
  - test-report.md
  - regression-notes.md
结论: <通过 / 未通过 / 有残余风险>
下一步: 用 $pd-review 做 Code Review
```
