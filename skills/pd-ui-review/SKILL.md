---
name: pd-ui-review
description: >-
  独立 UI 设计质量审查工作流，基于 PRD、设计系统、Figma、截图或本地页面审查视觉与交互质量，输出 ui/ui-review-report.md 与 P0/P1/P2/P3 findings；默认只审查，不改设计稿、不改代码、不提交。Use when the user mentions $pd-ui-review、pd-ui-review、UI review、设计稿 review、Figma review、视觉审查、页面看起来不对、样式不统一、字体不统一、遮挡、重叠、突兀、不整齐、对齐问题、间距问题、移动端溢出、布局不专业、字段层级不清、卡片模板不一致、截图审查。
---

# $pd-ui-review — UI 设计质量审查

以当前证据找出影响用户任务的视觉 / 交互问题。默认只审查，不改设计、不改代码、不提交；不替代 `$pd-review` 的代码审查，也不进入 `$pd-git`。

## 读取

1. 定位当前 `SKILL.md` 目录为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage ui-review`，提取工作目录、执行规范、安全、产品事实边界及报告模板。工具需要 Python 3.10+；不可用时手动读取 [共享流程](../qwerdf-common/product-delivery-flow.md) 的相应章节和 [报告模板](../qwerdf-common/artifact-contracts.md) 中 `ui/ui-review-report.md`，记录人工读取即可。
2. 读取 [UI Review Rules](../qwerdf-common/ui-review-rules.md) 和 [UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md)。严重性、三层审查适用性、不能交付条件和同类问题扫描统一遵循共享规则。
3. 按本次范围读取已有产品事实、`ui/ui-design-system.md`、页面规格、组件清单、相关 `ui/figma-handoff.md` 或 `tech/frontend/frontend-acceptance.md`。需核对设计决策时读取 [Design System Rules](../qwerdf-common/ui-design-system.md)；需选择页面模式时读取 [UI Patterns](../qwerdf-common/ui-patterns.md)，不默认通读全部上游与工程文件。
4. 视觉检查读取 [Visual Defects](references/visual-defects.md)；Figma 对象另读 [Figma Review](references/figma-review.md)，截图 / 本地页面另读 [Screenshot Review](references/screenshot-review.md)。按对象选择，不全量加载专项参考。

## 流程

1. 确定页面 / frame / URL、版本、视口、状态和审查范围；缺少项目材料不妨碍有限的截图观察，但不能推断业务规则。未指定目录时用 `pd-work/<name>/`。
2. 获取当前截图证据、必要节点 / 运行度量。访问 Figma 前加载对应 Figma 技能；本地页面可使用浏览器 / Playwright。只有文字观察或修复说明时，不声称亲眼看到截图。
3. 对照设计系统与本轮验收点，记录机器扫描、视觉扫描、模板扫描的已检查项、不适用理由和未验证项。放大关键区域检查；机器无报错不能代替视觉判断。
4. 对发现的问题执行有边界的同类问题扫描。用户要求全稿时按页面清单逐页记录，未覆盖部分保持未审查。
5. 按共享规则输出 P0/P1/P2/P3 findings，保留真正影响操作、阅读、反馈、范围或设计系统一致性的约束；不因默认像素值、批准变体或风格偏好误拦。
6. 写入 `ui/ui-review-report.md`，区分阻断、证据缺口和残余风险。设计稿归 `$pd-figma`，实现偏差归 `$pd-fe`，事实源 / 设计系统问题归 `$pd-blueprint` / `$pd-plan`；归属不明写待确认。实现修复按 [共享交接规则](../qwerdf-common/ui-review-rules.md#6-ui-finding-修复交接) 引用原 finding，不要求审查时预填工程 slice 或复制报告。未经授权不修改这些产物。
7. 复查修复时按相同范围重新获取可比证据，逐项关闭 finding；旧结论不能覆盖当前问题。无 P0/P1 且必要证据充分时，可在本轮范围内建议继续，P2/P3 记录 owner、验证与复查入口。

## 输出摘要

```text
UI Review 完成: <name>
目录: <output-dir>
文件: ui/ui-review-report.md
范围: <本轮页面 / 状态 / 视口；未覆盖范围>
结论: <有阻断 / 证据不足 / 本轮范围可继续，附残余建议>
下一步: <对应归属或待确认项，不建议提交>
```
