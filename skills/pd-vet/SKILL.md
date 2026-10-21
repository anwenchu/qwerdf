---
name: pd-vet
description: >-
  产品想法验证工作流，把一句话 idea、竞品 URL、截图、市场观察或粗略产品想法拆成用户问题、竞品参考、MVP 假设和验证问题，并给出进入 PRD、继续调研或暂停建议；不接入外部变更生命周期。Use when the user mentions $pd-vet、pd-vet、想法验证、idea验证、产品想法验证、创业想法验证、从想法开始、验证产品机会。
---

# $pd-vet — 想法验证

Codex Product Delivery Skill：把早期 idea 转成可判断是否值得写 PRD 的产品机会判断。

## 读取

1. 先定位当前 `SKILL.md` 的目录作为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage vet`。仅加载 [共享规则](../qwerdf-common/product-delivery-flow.md) 的产品相关章节及 [产物模板](../qwerdf-common/artifact-contracts.md) 的本阶段片段；不通读工程、测试、SQL 和发布内容。
2. 读取 [产品机会判断](references/opportunity-review.md)。工具需要 Python 3.10+ 且无第三方依赖；不可运行时手动读取共享规则的默认工作目录、执行规范正文、产品事实 Gate、安全与意外最小化、外部生命周期边界及五个本阶段模板，做等价人工核对并记录未执行机械检查。
3. 读取用户提供的一句话 idea、竞品 URL、截图、市场观察、用户反馈或产品背景。
4. 如果用户未指定输出目录，使用 `pd-work/<name>/`。

## 边界

- 不写 PRD 定稿；PRD 交给 `$pd-prd`。
- 不进 Figma。
- 不写代码。
- 不做技术方案。
- 竞品只提炼问题、流程、定位和交互模式，不照抄视觉、文案或受保护资产。
- 用户指定格式时遵循其格式；工具不支持的结构人工核对同等完整性要求并记录，不声称机械通过。

## 流程

1. 先判断 idea 是否有足够上下文；缺少目标用户、痛点或使用场景时，先提问。
2. 生成 `product/idea-brief.md`，把原始想法整理成目标、用户、问题、价值和初步判断。
3. 生成 `product/user-problem.md`，明确用户画像、当前做法、问题强度和 Jobs To Be Done。
4. 生成 `product/competitor-notes.md`，提炼竞品/替代方案的可借鉴模式和不应照搬点。
5. 生成 `product/mvp-hypothesis.md`，列出核心假设、MVP 范围和最大风险。
6. 生成 `product/validation-questions.md`，给出需要访谈、调研或原型验证的问题。
7. 输出建议：进入 PRD、继续调研或暂停；说明理由，并区分事实、假设和未提供证据。进入 PRD 不代表已验证商业价值。
8. 运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" validate --stage vet --root "<output-dir>"`；`REVIEW` 提示人工核对未识别的材料与决定，`PASS` 仅代表未检出机械问题。退出码 0 不等于材料已通过；不编造证据来消除提示。
9. 结合机会判断做业务自审。机械检查通过或等价人工核对完成，且建议进入 PRD、无阻断需求定义的问题时才指向 `$pd-prd`；环境限制本身不阻断交接。摘要保留实际缺口及核对方式。

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
验证: <材料检查结果 / 未执行原因；尚未验证的假设>

下一步: <满足条件则用 $pd-prd；否则继续调研或暂停，并列出需验证的问题>
```
