---
name: pd-vet
description: >-
  产品想法验证工作流，把一句话 idea、竞品 URL、截图、市场观察或粗略产品想法拆成用户问题、竞品参考、MVP 假设和验证问题，并给出进入 PRD、继续调研或暂停建议；不接入外部变更生命周期。Use when the user mentions $pd-vet、pd-vet、想法验证、idea验证、产品想法验证、创业想法验证、从想法开始、验证产品机会。
---

# $pd-vet — 想法验证

Codex Product Delivery Skill：把早期 idea 转成可判断是否值得写 PRD 的产品机会判断。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Product Delivery Artifact Contracts](../qwerdf-common/artifact-contracts.md) 中 `product/idea-brief.md`、`product/user-problem.md`、`product/competitor-notes.md`、`product/mvp-hypothesis.md`、`product/validation-questions.md` 的模板。
3. 读取用户提供的一句话 idea、竞品 URL、截图、市场观察、用户反馈或产品背景。
4. 如果用户未指定输出目录，使用 `pd-work/<name>/`。

## 边界

- 不写 PRD 定稿；PRD 交给 `$pd-prd`。
- 不进 Figma。
- 不写代码。
- 不做技术方案。
- 竞品只提炼问题、流程、定位和交互模式，不照抄视觉、文案或受保护资产。

## 流程

1. 先判断 idea 是否有足够上下文；缺少目标用户、痛点或使用场景时，先提问。
2. 生成 `product/idea-brief.md`，把原始想法整理成目标、用户、问题、价值和初步判断。
3. 生成 `product/user-problem.md`，明确用户画像、当前做法、问题强度和 Jobs To Be Done。
4. 生成 `product/competitor-notes.md`，提炼竞品/替代方案的可借鉴模式和不应照搬点。
5. 生成 `product/mvp-hypothesis.md`，列出核心假设、MVP 范围和最大风险。
6. 生成 `product/validation-questions.md`，给出需要访谈、调研或原型验证的问题。
7. 输出建议：进入 PRD、继续调研或暂停；说明理由。

## 输出摘要

```text
想法验证完成: <name>
目录: <output-dir>
文件:
  - product/idea-brief.md
  - product/user-problem.md
  - product/competitor-notes.md
  - product/mvp-hypothesis.md
  - product/validation-questions.md
建议: <进入 PRD / 继续调研 / 暂停>

下一步: 用 $pd-prd <name> 基于验证结果生成 PRD
```
