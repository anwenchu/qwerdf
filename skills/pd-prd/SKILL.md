---
name: pd-prd
description: >-
   PRD 生成工作流，把已验证 idea、用户问题、MVP 假设、竞品参考、访谈记录或粗略需求整理成正式 PRD、需求清单、用户故事、验收标准和开放问题；不接入外部变更生命周期。Use when the user mentions $pd-prd、pd-prd、生成PRD、写PRD、产品需求文档、从想法生成PRD、从验证结果生成PRD。
---

# $pd-prd — PRD 生成

Codex Product Delivery Skill：把已验证的产品机会和需求材料整理成可进入产品设计输入和页面蓝图阶段的 PRD。

## 读取

1. 定位当前 `SKILL.md` 的目录作为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage prd`。仅加载 [共享规则](../qwerdf-common/product-delivery-flow.md) 的产品相关章节及 [产物模板](../qwerdf-common/artifact-contracts.md) 的五个 PRD 模板，不通读 UI、工程、SQL 或发布内容。
2. 读取 [需求质量与交接检查](references/requirements-quality.md)。工具需要 Python 3.10+ 且无第三方依赖；不可运行时手动读取共享规则的默认工作目录、执行规范正文、产品事实 Gate、安全与意外最小化、外部生命周期边界及五个 PRD 模板，并做等价人工核对。记录未执行机械检查，不因环境限制阻断已完成业务核对的交接。
3. 优先读取输出目录中的 `product/idea-brief.md`、`product/user-problem.md`、`product/competitor-notes.md`、`product/mvp-hypothesis.md`、`product/validation-questions.md`。
4. 读取用户提供的访谈记录、竞品 URL、截图、产品背景、需求草稿或已有 spec。
5. 如果用户未指定输出目录，使用 `pd-work/<name>/`。

## 边界

- 不做 UI 页面蓝图；页面蓝图交给 `$pd-blueprint`。
- 不进 Figma。
- 不写代码。
- 不生成技术方案、API 契约或数据库设计。
- 不把未经验证的假设写成事实；必须标记假设、风险和待确认项。
- 用户指定格式时遵循其格式；工具不支持的结构改为人工核对同等追溯与覆盖要求，记录不适用原因，不伪称机械通过。用户明确要草稿时可保留假设，但不得当成已确认需求交接。

## 流程

1. 判断输入是否足够生成 PRD；缺少目标用户、核心场景、MVP 范围或关键业务规则时，先列出缺口并提问。
2. 生成 `product/prd.md`，覆盖背景、目标、用户角色、核心场景、功能范围、非目标范围、业务规则、用户流程、验收标准、假设与风险、开放问题；记录事实来源及确认状态，不编造指标、访谈或用户决定。新编号建议 SRC / REQ / AC / Q；已有稳定编号（如 R1）和等价标题沿用。
3. 生成 `product/requirements.md`，整理功能点、优先级、已确认来源及预期业务结果；不重复列全验收编号。
4. 生成 `product/user-stories.md`，用用户角色、我想要、以便于和关联需求表达需求；无需另维护 AC 清单。
5. 生成 `product/acceptance-criteria.md`，以此处的 AC → 需求关系为验收关联的唯一权威记录，包含前置条件、操作 / 事件和可观察结果。审阅适用的正常结果、异常恢复、权限、边界重复及业务状态；覆盖矩阵可仅用于复杂或高风险需求，不逐项强制填表，不重复列全 AC，也不把 UI 状态当业务生命周期。
6. 生成 `product/open-questions.md`，记录问题、影响、是否阻断、状态及确认方；无问题明确写“无”。关键规则不清时阻断受影响需求；非阻断问题的确认人待定仅作跟踪提醒，不升级为业务阻断。
7. 运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" validate --stage prd --root "<output-dir>"`。`BLOCKED` 要修正明确的引用矛盾或澄清业务阻断；`REVIEW` 按提示人工核对原格式及内容，记录结论；`PASS` 仅表示未检出机械问题。退出码 0 也可能是 `REVIEW`，不能单凭退出码宣称通过。不为消除提示重排用户格式或补写无关历史材料。
8. 按需求质量参考完成读者自审，确认来源真实性、范围合理性、规则与验收语义一致。机械检查通过或等价人工核对完成，且业务自审无未解决阻断项时，才建议 `$pd-blueprint`；摘要区分脚本结果、人工结论和未决问题。

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
验证: <机械检查结果 / 未执行原因；业务自审缺口；阻断问题>

下一步: <无阻断则用 $pd-blueprint；否则继续澄清或修订受影响需求>
```
