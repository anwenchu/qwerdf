---
name: pd-git
description: >-
   Git 提交与 PR/MR 准备工作流，基于当前 git diff、实现记录、联调报告、测试报告、Code Review 和 commit readiness gate 生成 commit summary、commit message 和 PR/MR description；只有用户明确要求且 gate 全部通过时才可执行 git add、git commit，默认不 push。Use when the user mentions $pd-git、pd-git、提交代码、准备提交、生成PR描述、生成MR描述、commit message。
---

# $pd-git — 提交与 PR/MR 准备

Codex Product Delivery Skill：整理提交范围和 PR/MR 文案。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Engineering Artifact Contracts](../qwerdf-common/engineering-contracts.md) 中 `release/commit-summary.md` 和 `release/pr-description.md` 的模板。
3. 读取实现记录、联调报告、测试报告、Code Review、`.gitignore`、当前 git diff 和 git status。
4. 如果用户未指定目录，默认使用 `pd-work/<name>/`。

## 边界

- 默认只准备文案。
- 用户明确要求时才执行 `git add` 和 `git commit`。
- 执行 `git add` 前必须展示 planned files，并排除明显无关文件。
- 默认不 push，除非用户明确要求。
- 不修改业务代码。
- 有未解决 P0/P1、联调未通过、测试未通过、测试未执行、未解释的契约差异或提交范围风险时，不得执行 `git add` / `git commit`；只能生成阻断说明和风险说明。
- 不把 `.env`、密钥、token、私有证书、临时日志或无关生成物加入 planned files。
- 不用 `git add -A`、`git add .` 或通配符扩大提交范围；提交时只 add 已展示并确认的 planned files。
- 不 force-add 被 `.gitignore` / `.git/info/exclude` 忽略的文件，除非用户明确确认并说明为什么该文件必须提交。
- planned files 必须同时满足：与本次需求 / 实现记录 / 测试报告 / Code Review 相关、未被 ignore、不是生成噪声、不是秘密或本地配置。

## Git 状态采集

提交前先采集这些信号，再决定是否继续：

1. 当前分支、upstream 和 remote。
2. `git status --short` 的全部改动。
3. `git status --short --ignored` 或等价方式识别 ignored 文件。
4. staged / unstaged / untracked 文件分组。
5. `.gitignore`、`.git/info/exclude` 和必要时 `git check-ignore -v <path>` 的结果。
6. `git ls-files --others --exclude-standard` 中未被 ignore 的未跟踪文件。
7. 与本次 `pd-work/<name>`、实现记录、测试报告相关的文件。
8. 可能包含 secret、环境配置、构建产物、缓存、日志、截图、报告或无关改动的文件。

## 提交范围门禁

- Commit readiness gate 必须全部通过：相关实现 slice 已完成；`sync/integration-report.md` 明确通过或明确不适用并说明原因；`test/test-report.md` 明确通过且无未解释高风险缺口；`test/code-review.md` 无 P0/P1；提交范围检查无未解决漏提 / 多提风险。
- `release/commit-summary.md` 必须列出 planned files、excluded files、possible missing files、possible extra files 和 gitignore check。
- 漏提交检查：对照实现记录、测试报告、Code Review、需求产物和 git status，找出本次变更相关但未进入 planned files 的文件；有疑问时列为 possible missing files 并停止提交确认。
- 多提交检查：对照 planned files 和本次任务范围，找出无关格式化、IDE 配置、本地环境、缓存、构建产物、测试截图、临时报告、历史 benchmark run 等文件；列为 excluded files 或 possible extra files。
- `.gitignore` 检查：如果测试 / 构建产生的缓存、dist、coverage、日志、截图、临时报告没有被 ignore，记录风险并排除；不要为了让 status 干净而提交这些文件。
- staged 检查：如果已经存在 staged 文件，必须对照 planned files；staged 与 planned 不一致时先停止并说明差异，不继续提交。

## 流程

1. 采集 Git 状态，区分相关、无关、危险和待确认改动。
2. 检查 `.gitignore` / ignored / untracked 状态，识别应提交、应忽略、应排除和待确认文件。
3. 检查 commit readiness gate：实现 slice 完成、`sync/integration-report.md` 通过、`test/test-report.md` 通过、`test/code-review.md` 无 P0/P1。
4. 任一 gate 未通过时，写入 `release/commit-summary.md` 的阻断原因和下一步，不生成“可提交”口径，不执行 `git add` / `git commit`。
5. 写入 `release/commit-summary.md`，包含 readiness gates、git state、gitignore check、planned files、excluded files、possible missing files、possible extra files、commit message、summary、tests、known risks。
6. 写入 `release/pr-description.md`，包含 what changed、why、validation、risks、rollback。
7. 如用户明确要求提交，先展示 readiness gates、planned files、excluded files、possible missing / extra files 和 staged 差异；只有所有 gate 通过且确认无漏提 / 多提后，逐个 `git add <file>` 并执行 `git commit`。

## 输出摘要

```text
Git 提交准备完成: <name>
目录: <output-dir>
文件:
  - release/commit-summary.md
  - release/pr-description.md
提交: <未提交 / 已提交 commit sha>
下一步: 用 $pd-release 生成上线文档
```
