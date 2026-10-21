---
name: pd-blueprint
description: >-
   PRD 到产品设计输入和 UI 页面蓝图工作流，把 PRD、竞品 URL、截图、产品想法或已有 spec 拆成 product-brief、UI 设计系统、用户流程、页面地图、页面规格和组件清单；不接入外部变更生命周期。Use when the user mentions $pd-blueprint、pd-blueprint、产品蓝图、产品设计输入、PRD转UI、页面蓝图、UI蓝图、UI设计系统、从 PRD 生成页面设计输入、从竞品参考整理页面结构。
---

# $pd-blueprint — 产品设计输入与页面蓝图

Codex Product Delivery Skill：把 PRD、竞品参考或产品想法转成可进入 UI 方向探索、Figma 设计和前端实现的设计输入。

## 读取

1. 定位当前 `SKILL.md` 的目录作为 `<skill-dir>`，运行 `python3 "<skill-dir>/../qwerdf-common/scripts/product_artifacts.py" context --stage blueprint`，按需提取 [共享规则](../qwerdf-common/product-delivery-flow.md) 和 [产物模板](../qwerdf-common/artifact-contracts.md)，不通读工程、SQL 和提交规则。工具需要 Python 3.10+ 且无第三方依赖；不可运行时手动读取默认工作目录、执行规范正文、产品事实 Gate、安全与意外最小化、外部生命周期边界、UI gate / 职责边界及本阶段六个模板。
2. 上游存在稳定需求 / 验收编号时沿用（包括 R1 等旧编号），在流程、页面和状态说明中保留关联。发现未解决阻断问题先回 `$pd-prd` 澄清受影响范围；旧版或自定义格式可按已有人工核对结论交接，不强制重编号、补表或依赖 Python，不替用户补出已确认规则，也不伪报机械通过。
3. 读取 [UI Design System Rules](../qwerdf-common/ui-design-system.md)、[UI Quality Checklist](../qwerdf-common/ui-quality-checklist.md) 和 [UI Patterns](../qwerdf-common/ui-patterns.md)。
4. 优先读取输出目录中的 `product/prd.md`、`product/requirements.md`、`product/user-stories.md`、`product/acceptance-criteria.md`、`product/open-questions.md`。
5. 读取用户提供的 PRD、竞品 URL、截图、产品说明、设计偏好或已有 spec。
6. 如果用户未指定输出目录，使用 `pd-work/<name>/`。

## 边界

- 不要求先执行外部探索或变更初始化流程。
- 不创建外部变更目录。
- 不修改 `.state.yaml`。
- 不进 Figma。
- 不写代码。
- 不生成技术方案。
- 竞品只提炼交互模式、信息架构和体验取舍，不照抄视觉、文案或受保护资产。
- 竞品或截图中的业务模块、导航标签、资产类型、活动入口、copy trading、品牌术语等，只有在 PRD / requirements / 用户明确说明中出现时才能进入产品范围。

## 蓝图质量规则

- 每个页面先写清楚主体、目标用户和页面唯一任务，再写页面结构。
- 产品设计输入必须包含产品类型、用户角色、核心任务、信息密度、视觉气质、页面模式、导航结构、关键状态和设计风险。
- `ui/ui-design-system.md` 必须包含 `MASTER` 和 `Page Overrides`；`MASTER` 是全局事实源，页面级只写必要差异。
- SaaS / CRM / 管理后台 / 操作台默认走克制、密集、可扫描、效率优先方向；避免营销页式 hero、过度卡片化、大面积装饰和只服务氛围的视觉。
- landing page 只有 PRD 明确要求获客、营销或活动页时才作为页面模式。
- 页面结构必须服务业务信息，不用无意义编号、装饰性分区或模板化 dashboard 区块。
- 文案按用户能识别的动作命名，不用系统实现术语替代用户语言。
- 状态反馈要求统一读取 [共享质量清单的条件表](../qwerdf-common/ui-quality-checklist.md#4-适用的状态与交互)，不为套模板补造业务动作。
- 竞品模式要写取舍：为什么适合本产品、哪些前提不适用、哪些地方不能照搬。
- 先写产品事实锁，再写参考拆解；页面、导航、组件和状态必须从产品事实锁推导，不能从参考图直接搬运。
- 参考材料只能贡献视觉密度、布局节奏、信息分组、反馈方式、交互动效等抽象模式；不能贡献产品能力、交易品类、tab 名称、品牌文案或业务对象。
- 如果参考图与 PRD / product-brief 冲突，把冲突项写入 `参考使用边界` 或 `不应照搬`，不要写进 `ui/ui-pages.md`、`ui/ui-screens.md` 或 `ui/ui-components.md`。

## 流程

1. 判断输入是否足够生成产品设计输入；缺少目标用户、核心场景、MVP 范围或关键约束时，先列出缺口并提问，不写半成品文件。
2. 从 PRD、requirements、用户说明和已有 spec 中抽取产品事实锁：产品名称、目标用户、核心场景、支持的业务对象、MVP 范围、非目标范围。
3. 对竞品、截图或设计参考做参考拆解：只保留可借鉴的视觉 / 交互模式；把产品范围外的模块、导航、资产、文案、品牌和业务前提列为不得带入。
4. 先生成 `product/product-brief.md`，明确产品事实源、产品目标、目标用户、核心场景、MVP 范围、成功指标、UI 方向输入、约束、竞品模式、参考使用边界、风险和开放问题。
5. 生成 `ui/ui-design-system.md` 草案，按共享设计系统规则记录本次 token 的值 / 别名、用途、来源与确认状态，关联组件 variant、关键状态和内容 / 交互约束；已有系统优先复用。`MASTER` 维护全局约束，`Page Overrides` 只写差异，不复制数值到页面和组件清单。不要求额外生成 CSS / JSON 或代码 API；不得用参考图扩展产品范围。
6. 基于 `product/product-brief.md` 和 `ui/ui-design-system.md` 生成 UI 页面蓝图：
   - `ui/ui-flows.md`
   - `ui/ui-pages.md`
   - `ui/ui-screens.md`
   - `ui/ui-components.md`
7. 按实际业务覆盖适用状态，异步、数据为空、失败恢复、权限和保存反馈不可遗漏；静态公开页不强制制造 loading / permission。共享组件状态可维护一次，页面引用并写差异；按产品实际平台 / 断点制定响应式要求。
8. 按共享质量清单自审来源、范围、token / 组件关联和关键状态。摘要列出文件、设计建议 / 待确认项及受影响范围；本轮无关键阻断时建议 `$pd-figma`，否则先澄清，不为凑模板改写无关历史材料。

## 输出摘要

```text
产品设计输入与 UI 页面蓝图完成: <name>
目录: <output-dir>
文件:
  - product/product-brief.md
  - ui/ui-design-system.md
  - ui/ui-flows.md
  - ui/ui-pages.md
  - ui/ui-screens.md
  - ui/ui-components.md
待确认:
  - <如无则写“无”>

下一步: <本轮无关键阻断则用 $pd-figma；否则先澄清受影响范围>
```
