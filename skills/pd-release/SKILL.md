---
name: pd-release
description: >-
  个人上线文档工作流，基于 PRD、技术方案、实现记录、联调报告、测试报告、Code Review 和提交说明生成通用 Markdown 上线计划、上线检查清单、回滚方案和 release notes；不接平台、不执行部署。Use when the user mentions $pd-release、pd-release、上线文档、发布计划、上线计划、回滚方案、release notes。
---

# $pd-release — 上线文档

个人辅助 Skill：生成上线前材料，不执行真实部署。

## 读取

1. 读取 [个人 Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `release-plan.md`、`release-checklist.md`、`rollback-plan.md`、`release-notes.md` 的模板。
3. 必须读取 `test-report.md` 和 `code-review.md`。
4. 读取 PRD、技术方案、实现记录、联调报告和提交说明。
5. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 不接 GitHub Release、GitLab、GitOps、Lark 或其他平台。
- 不执行部署。
- 不 push。
- 缺少 `test-report.md` 或 `code-review.md` 时，不得声称可以上线。
- 存在 P0/P1、失败测试、未解释的契约差异或缺少回滚路径时，结论必须写成有阻断风险。
- 不生成平台专属发布命令，除非用户另行要求设计新的部署 skill。

## 发布状态采集

生成上线材料前先确认：

1. 目标环境、发布范围和是否用户可见。
2. 关联 commit / PR / MR 是否明确；如不明确，写成待确认。
3. 测试报告、联调报告、Code Review 是否有阻断项。
4. 回滚路径是否真实可执行，是否涉及数据迁移或不可逆操作。
5. 监控、日志、告警、人工验收点和上线窗口是否明确。

## 流程

1. 采集发布状态，检查测试报告、联调报告和 Code Review 是否存在，确认无 P0/P1、失败测试和契约阻断。
2. 生成 `release-plan.md`。
3. 生成 `release-checklist.md`。
4. 生成 `rollback-plan.md`。
5. 生成 `release-notes.md`。
6. 输出上线风险、回滚触发条件和人工确认项。

## 输出摘要

```text
上线文档完成: <name>
目录: <output-dir>
文件:
  - release-plan.md
  - release-checklist.md
  - rollback-plan.md
  - release-notes.md
结论: <可进入上线审批 / 缺少验证 / 有阻断风险>
```
