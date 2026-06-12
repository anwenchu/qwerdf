---
name: pd-review
description: >-
   Code Review 工作流，基于 git diff、PRD、技术方案、前后端契约、联调报告和测试报告做结构化审查，按 P0/P1/P2/P3 输出需求一致性、方案一致性、契约一致性、错误处理、状态覆盖、安全、可维护性和测试缺口。Use when the user mentions $pd-review、pd-review、Code Review、代码审查、审查改动、review 当前实现。
---

# $pd-review — Code Review

Codex Product Delivery Skill：在提交前审查实现质量和交付风险。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `code-review.md` 的模板。
3. 读取 PRD、技术方案、API 契约、联调报告、测试报告、前后端实现记录和当前 git diff。
4. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 默认只审查，不修改代码。
- 不提交代码。
- 需要修复时，按问题归属回到 `$pd-fe`、`$pd-be` 或 `$pd-plan`。
- Findings 必须能定位到文件、区域、契约条目、测试证据或产物段落；证据不足时标记为待确认，不升级成确定问题。

## 审查类别优先级

| 优先级 | 类别 | 检查重点 |
| --- | --- | --- |
| 1 | 需求与契约 | 是否偏离 PRD、验收标准、API 契约、权限和状态规则 |
| 2 | 正确性 | 错误处理、边界条件、并发、幂等、数据一致性 |
| 3 | 安全与隐私 | 越权、敏感数据、日志泄露、输入校验 |
| 4 | 前端质量 | 状态覆盖、可访问性、响应式、重渲染、bundle 和组件 API |
| 5 | 后端质量 | 分层边界、事务、错误码、观测、资源使用 |
| 6 | 测试缺口 | 哪些验收标准、风险或回归路径未被验证 |

## 流程

1. 先列出 P0/P1/P2/P3 findings，按严重程度排序。
2. 覆盖需求一致性、技术方案一致性、前后端契约一致性、错误处理、状态覆盖、权限安全、可维护性、测试缺口。
3. 对每个 finding 标明影响、建议修复归属和验证建议。
4. 写入 `code-review.md`。
5. 无问题时明确说明未发现阻断问题，并列出残余风险。

## 输出摘要

```text
Code Review 完成: <name>
目录: <output-dir>
文件:
  - code-review.md
结论: <无阻断 / 有 P0 / 有 P1 / 有建议项>
下一步: 修复问题或用 $pd-git 准备提交
```
