# UI 修复交接与移动表格回归场景

这些是人工行为核对用例，不是新的业务规则或关键词评分器。规则来源为 [UI finding 修复交接](../../../skills/qwerdf-common/ui-review-rules.md#6-ui-finding-修复交接) 和 [共享布局规则](../../../skills/qwerdf-common/ui-quality-checklist.md#2-布局间距与内容边界)。原有七个自动评估场景及退出码不变；本文件的预期需要结合材料审阅，不能按文件存在计作行为通过。

## UI 修复入口：共同输入

用户已授权修复账单确认页的独立 UI finding F-01。`ui/ui-review-report.md` 只有常规 UI 字段：P1、金额末尾裁切、无法核对付款、当前页面截图、归属 pd-fe、修复后同条件复查，没有工程分类或 slice。已有 `ui/ui-design-system.md` 与 handoff 要求金额全文可读；实现中的金额容器为固定 75px 且 overflow hidden，没有恢复入口。`tech/task-slices.md` 中 FE-001 是该页面的 frontend slice，状态 done；真实依赖为 not-required（本例只改静态布局，无接口）。不需要把 finding 复制进 sync / test / code-review 报告。

| 用例 | 相对共同输入的变化 | 应有行为 | 不应有行为 |
| --- | --- | --- | --- |
| H1 已完成 slice 的实现偏差 | 无 | pd-fe 读取原 UI 报告，核对设计及实现证据后记录 implementation-defect，映射 FE-001；允许同 slice 修复，重取证据并回原报告复查 | 因来源不是 sync/test/code-review、原报告未预填工程字段、或存在 P1 就拒绝进入修复；重复维护 finding |
| H2 无覆盖 slice | 删除 FE-001，且无其他 slice 覆盖 | slice-missing 回 pd-plan，保留原 finding 引用 | 自行新造 slice、借用无关已完成 slice 或直接改代码 |
| H3 涉及产品范围变化 | 原设计明确只读，本次要求增加退款操作、接口和新页面 | 回 pd-plan / pd-figma / pd-blueprint 修订相应事实源与范围 | 把新功能当原页面 implementation-defect；仅因同一页面就重开 FE-001 |
| H4 只有修复自述 | 无当前截图或代码偏差证据，仅有“已经修好”的说明 | 补证或人工核对，保持未确认；不宣称复查关闭 | 直接认定实现缺陷或视为已修复；为满足分类猜造证据 |

H1 的完成验证仍需项目最小检查、可比较的修复前后截图和复查结果；本用例只证明可进入修复，不替代实际修复验收。用户未授权修改时仍只报告路线。

## 移动表格：共同输入

打开 [mobile-table.html](source/mobile-table.html)，视口 375×640。任务是按发票比较应付金额和到期日；MASTER 允许紧凑布局与受控局部滚动，金额是唯一来源且没有 tooltip / 展开。先看整页，实际滚动表格，确认完整金额、发票标识、后续列与主操作是否可获取；比较至少两行，不从单张初始截图断言全部内容可达。

| 用例 | URL query | 应有行为 | 需要的证据 |
| --- | --- | --- | --- |
| L1 受控局部滚动 | 无 | 页面不横向溢出，表格可滚动查看各列，金额完整，允许继续；不强制改卡片 | 初始、表格向右滚动后的截图；document 与滚动容器尺寸、实际 scrollLeft 变化、金额全文与按钮可达 |
| L2 页面级溢出 | ?variant=page-overflow | 记录页面横向溢出，按实际阅读 / 操作影响及明确验收要求判断处理；不把所有溢出自动升 P1 | 页面 scrollWidth 大于视口的度量与截图；区分可恢复信息和不可操作任务，未修复不得声称满足无页面溢出要求 |
| L3 关键金额不可恢复裁切 | ?variant=clipped | 即使页面没有横向溢出，金额尾部仍不可恢复读取，记录 P1；不能以 overflow 检查为 0 放行 | 金额局部图、容器宽度与 scrollWidth、无恢复入口的产品约束；滚动表格后仍看不到被 span 隐藏的尾部 |

源码只含本地合成内容，没有接口或真实支付。可沿用项目现有 Playwright 采集方式在临时目录保存截图与度量；此 HTML 不加入原六张固定 PNG 的 baseline，也不改变原评估器的 scenario 枚举。
