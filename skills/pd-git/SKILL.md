---
name: pd-git
description: >-
   Git 提交与 PR/MR 准备工作流，基于当前 git diff、实现记录、测试报告和 Code Review 生成 commit summary、commit message 和 PR/MR description；用户明确要求时可执行 git add、git commit，默认不 push。Use when the user mentions $pd-git、pd-git、提交代码、准备提交、生成PR描述、生成MR描述、commit message。
---

# $pd-git — 提交与 PR/MR 准备

Codex Product Delivery Skill：整理提交范围和 PR/MR 文案。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `commit-summary.md` 和 `pr-description.md` 的模板。
3. 读取实现记录、联调报告、测试报告、Code Review 和当前 git diff。
4. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 默认只准备文案。
- 用户明确要求时才执行 `git add` 和 `git commit`。
- 执行 `git add` 前必须展示 planned files，并排除明显无关文件。
- 默认不 push，除非用户明确要求。
- 不修改业务代码。
- 有未解决 P0/P1、失败测试或未解释的契约差异时，只能生成文案和风险说明，不建议提交。
- 不把 `.env`、密钥、token、私有证书、临时日志或无关生成物加入 planned files。

## Git 状态采集

提交前先采集这些信号，再决定是否继续：

1. 当前分支、upstream 和 remote。
2. `git status --short` 的全部改动。
3. staged / unstaged / untracked 文件分组。
4. 与本次 `pd-work/<name>/`、实现记录、测试报告相关的文件。
5. 可能包含 secret、环境配置、构建产物或无关改动的文件。

## 流程

1. 采集 Git 状态，区分相关、无关、危险和待确认改动。
2. 检查 `integration-report.md`、`test-report.md` 和 `code-review.md` 是否存在阻断项。
3. 写入 `commit-summary.md`，包含 planned files、excluded files、commit message、summary、tests、known risks。
4. 写入 `pr-description.md`，包含 what changed、why、validation、risks、rollback。
5. 如用户明确要求提交，先展示 planned files 和 excluded files，再执行 `git add` 和 `git commit`。

## 输出摘要

```text
Git 提交准备完成: <name>
目录: <output-dir>
文件:
  - commit-summary.md
  - pr-description.md
提交: <未提交 / 已提交 commit sha>
下一步: 用 $pd-release 生成上线文档
```
