---
name: pd-prd
description: >-
   PRD 生成工作流，把已验证 idea、用户问题、MVP 假设、竞品参考、访谈记录或粗略需求整理成正式 PRD、需求清单、用户故事、验收标准和开放问题；不接入外部变更生命周期。Use when the user mentions $pd-prd、pd-prd、生成PRD、写PRD、产品需求文档、从想法生成PRD、从验证结果生成PRD。
---

# $pd-prd — PRD 生成

Codex Product Delivery Skill：把已验证的产品机会和需求材料整理成可进入产品设计输入和页面蓝图阶段的 PRD。

## 读取

1. 读取 [Codex Product Delivery 规则](../qwerdf-common/product-delivery-flow.md)。
2. 读取 [Product Delivery Artifact Contracts](../qwerdf-common/artifact-contracts.md) 中 `product/prd.md`、`product/requirements.md`、`product/user-stories.md`、`product/acceptance-criteria.md`、`product/open-questions.md` 的模板。
3. 优先读取输出目录中的 `product/idea-brief.md`、`product/user-problem.md`、`product/competitor-notes.md`、`product/mvp-hypothesis.md`、`product/validation-questions.md`。
4. 读取用户提供的访谈记录、竞品 URL、截图、产品背景、需求草稿或已有 spec。
5. 如果用户未指定输出目录，使用 `pd-work/<name>/`。

## 边界

- 不做 UI 页面蓝图；页面蓝图交给 `$pd-blueprint`。
- 不进 Figma。
- 不写代码。
- 不生成技术方案、API 契约或数据库设计。
- 不把未经验证的假设写成事实；必须标记假设、风险和待确认项。

## 流程

1. 判断输入是否足够生成 PRD；缺少目标用户、核心场景、MVP 范围或关键业务规则时，先列出缺口并提问。
2. 生成 `product/prd.md`，覆盖背景、目标、用户角色、核心场景、功能范围、非目标范围、业务规则、用户流程、验收标准、假设与风险、开放问题。
3. 生成 `product/requirements.md`，按需求 ID、优先级、来源和验收标准整理功能点。
4. 生成 `product/user-stories.md`，用用户角色、我想要、以便于、验收标准表达需求。
5. 生成 `product/acceptance-criteria.md`，明确功能、状态、边界和非目标验收。
6. 生成 `product/open-questions.md`，列出需要用户、业务、设计或技术确认的问题。
7. 输出摘要必须提示下一步使用 `$pd-blueprint`。

## 输出摘要

```text
PRD 生成完成: <name>
目录: <output-dir>
文件:
  - product/prd.md
  - product/requirements.md
  - product/user-stories.md
  - product/acceptance-criteria.md
  - product/open-questions.md
待确认:
  - <如无则写“无”>

下一步: 用 $pd-blueprint <name> 基于 PRD 生成产品设计输入和页面蓝图
```
