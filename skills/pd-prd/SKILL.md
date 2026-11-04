---
name: pd-prd
description: >-
   PRD 生成工作流，把已验证 idea、用户问题、MVP 假设、竞品参考、访谈记录或粗略需求整理成正式 PRD、需求清单、用户故事、验收标准和开放问题。Use when the user mentions $pd-prd、pd-prd、生成PRD、写PRD、产品需求文档、从想法生成PRD、从验证结果生成PRD。
---

# $pd-prd — PRD 生成

把已验证的产品机会和需求材料整理成可进入产品设计输入和页面蓝图阶段的 PRD。

## 读取

通用产物维护与恢复按 [生命周期规则](../qwerdf-common/artifact-lifecycle.md) 执行；下列上下文工具已提取其工作规则，手动回退时也须读取该部分。

1. 定位当前 `SKILL.md` 的目录作为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage prd`。仅加载 [共享规则](../qwerdf-common/product-delivery-flow.md) 的产品相关章节及 [产物模板](../qwerdf-common/artifact-contracts.md) 的PRD 主模板，不通读 UI、工程、SQL 或发布内容。
2. 读取 [需求质量与交接检查](references/requirements-quality.md)。工具需要 Python 3.10+ 且无第三方依赖；不可运行时手动读取共享规则的默认工作目录、执行规范正文、产品事实 Gate、安全与意外最小化、外部生命周期边界及PRD 主模板，并做等价人工核对。记录未执行机械检查，不因环境限制阻断已完成业务核对的交接。
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

1. 判断输入是否足够生成 PRD；先按 [共享规模与拆分规则](../qwerdf-common/artifact-lifecycle.md#规模预算与任务拆分) 评估本轮范围和产物，过大先在现有需求总览拆成可独立验收单元，再展开本阶段正文，不为每个单元复制全套阶段模板；缺少目标用户、核心场景、MVP 范围或关键业务规则时，先列出缺口并提问。
2. 生成 `product/prd.md`，覆盖背景、目标、用户角色、核心场景、功能范围、非目标范围、业务规则、用户流程、验收标准、假设与风险、开放问题；记录事实来源及确认状态，不编造指标、访谈或用户决定。新编号建议 SRC / REQ / AC / Q；已有稳定编号（如 R1）和等价标题沿用。
3. 在同一 PRD 的功能范围保留需求编号、来源与业务结果；用户故事只有需要补充角色 / 动作 / 价值时才写，不另生成清单。
4. 在 PRD 验收章节维护 AC → 需求的唯一主索引，写清前置、操作和可观察结果；审阅适用异常、权限、重复 / 边界及业务状态，不强制矩阵。长说明可引用主题详情，但主索引中的编号、关联与简短结果保留，避免合法引用被误判不存在。
5. 在 PRD 开放问题章节记录影响、是否阻断、状态及确认方；没有则写“无”。必要业务 / 契约未决仍阻断受影响交接，不用精简文档掩盖缺口。

6. 运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" validate --stage prd --root "<output-dir>"`。`BLOCKED` 要修正明确的引用矛盾或澄清业务阻断；`REVIEW` 按提示人工核对原格式及内容，记录结论；`PASS` 仅表示未检出机械问题。退出码 0 也可能是 `REVIEW`，不能单凭退出码宣称通过。不为消除提示重排用户格式或补写无关历史材料。
7. 按需求质量参考完成读者自审，确认来源真实性、范围合理性、规则与验收语义一致。机械检查通过或等价人工核对完成，且业务自审无未解决阻断项时，才建议 `$pd-blueprint`；摘要区分脚本结果、人工结论和未决问题。

## 输出摘要

```text
PRD 生成完成: <name>
目录: <output-dir>
文件:
  - product/prd.md
待确认:
  - <如无则写“无”>
验证: <机械检查结果 / 未执行原因；业务自审缺口；阻断问题>

下一步: <无阻断则用 $pd-blueprint；否则继续澄清或修订受影响需求>
```
