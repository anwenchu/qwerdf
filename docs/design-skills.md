# Design Skills：借鉴、修正与验证

## 范围与事实源

本次修订 `pd-blueprint`、`pd-ui-review` 及共享设计规则、模板、相关 Figma QA 衔接和评估用例；复查修正覆盖 `pd-plan`、`pd-fe`、`pd-review` 的规则衔接。当前校验行为以「当前自动校验边界」为准，后面的执行记录保留当时的版本和结果。保留技能名称、触发边界、输出路径、产品事实优先级和默认只审查边界；不改真实 Figma、产品页面或工程实现，不提交或推送。

UI 审查适用性、证据、严重性和交接条件只在 `skills/qwerdf-common/ui-review-rules.md` 维护；检查项目和默认设计起点在 `ui-quality-checklist.md`；Token / 组件契约在 `ui-design-system.md`。专项参考仅补充取证方法，报告引用结果，不再重复制定另一套门禁。

## 外部阅读与采用边界

2026-10-21 按固定版本阅读相关目录、文档和实现。以下是本次相关范围，不表示逐个阅读了项目所有媒体、平台和部署文件。未复制外部实现、风格 CSV、品牌资产或模板正文；新增测试页面和截图为本仓库原创合成材料。

### nexu-io/open-design

版本：[`3b0df90f305c8279e748c292accf336d02b924ef`](https://github.com/nexu-io/open-design/tree/3b0df90f305c8279e748c292accf336d02b924ef)。

| 阅读范围 | 本地采用 / 不采用 |
| --- | --- |
| [设计系统说明](https://github.com/nexu-io/open-design/blob/3b0df90f305c8279e748c292accf336d02b924ef/docs/design-systems.md)、design-systems/README.md | 采用规范 / token / 组件间的可追溯关系、派生文件不竞争事实源；不搬其整套 package schema、目录和固定数量要求。 |
| [Token 契约](https://github.com/nexu-io/open-design/blob/3b0df90f305c8279e748c292accf336d02b924ef/apps/daemon/src/design-systems/token-contract.ts)、token-evidence.ts、contracts 的 token-schema.ts / derived-token-outputs.ts | 采用值与别名、来源定位、测量 / 推断 / 默认值区分；本地保留 Markdown 和已有系统链接，不强制实现多层 token 文件或导出工具。 |
| [组件索引提取](https://github.com/nexu-io/open-design/blob/3b0df90f305c8279e748c292accf336d02b924ef/packages/contracts/src/design-systems/components-manifest.ts) | 采用组件引用语义 token、显式未知引用与漂移检查；蓝图只写设计与业务约束，代码 props/API 留给技术设计。 |
| skills/design-brief、reference-design-contract 及 checklist、brand-extract | 采用从参考抽取约束、测量与建议分开；不搬封闭配色词表、固定九标题、强制字体、资产下载或自动品牌注册。 |
| [截图对照记录](https://github.com/nexu-io/open-design/blob/3b0df90f305c8279e748c292accf336d02b924ef/docs/design/chat-mirror/README.md)、measure.mjs、shoot-live.mjs | 采用可比较基线、字体 / 数据 / 动画条件和组件样例与真实宿主分开验证；不执行其向服务种数据的脚本。 |
| skills/design-review、contracts/critique.ts 及测试、daemon/critique/rollout.ts | design-review 是上游技能的目录入口，不能据此声称内置完整视觉审查。未引入评分剧场、多角色轮询或按分数自动交付。 |

### WAAMEngineer/ui-ux-pro-max-skill

版本：[`40034e6a200c4f7f3e4f42a77cfed713bf5680a3`](https://github.com/WAAMEngineer/ui-ux-pro-max-skill/tree/40034e6a200c4f7f3e4f42a77cfed713bf5680a3)。阅读 README、`.claude/skills/ui-ux-pro-max/SKILL.md`、搜索 / 生成 / 持久化实现，以及风格、配色、产品、规则、UX / Web、landing / typography 数据结构与相关行。

- [检索实现](https://github.com/WAAMEngineer/ui-ux-pro-max-skill/blob/40034e6a200c4f7f3e4f42a77cfed713bf5680a3/src/ui-ux-pro-max/scripts/core.py) 使用 BM25；该版本数据有 67 种风格、96 套配色、100 条行业规则。采用按产品、任务、品牌、密度与平台检索少量候选并说明取舍，不复制或强制安装整套数据库。
- 在隔离目录用生成器所需五个检索域的完整数据复现：中文“后台 数据表格 响应式”零命中，英文对应查询返回三个候选；中文“运营管理后台”生成通用分类 / Glassmorphism / Hero，英文 dashboard 查询也会保留默认 Hero section。检索建议不能替代业务判断，零命中不静默套模板。
- [生成与持久化实现](https://github.com/WAAMEngineer/ui-ux-pro-max-skill/blob/40034e6a200c4f7f3e4f42a77cfed713bf5680a3/src/ui-ux-pro-max/scripts/design_system.py) 的 MASTER + Overrides 思路本仓库已采用；不新增第二套目录，也不调用会覆写 MASTER 的外部持久化命令。
- 行业反模式用于判断适用性，不把“紫粉渐变”升级为跨产品禁色；品牌已确认的紫色和合理紧凑布局可沿用。固定视口、字号、间距等仍服从产品和平台约束。

## 具体修正

- P0/P1 按用户任务受损程度阻断受影响范围；P2/P3 记录 owner、验证方式、复查入口后可继续。证据不足与产品缺陷分开，不为消除提示盲目降级或编造事实。
- 视觉扫描、机器扫描、模板扫描如实记已检查 / 不适用 / 未验证；只有截图时运行检查不适用，无同类对象时模板扫描不适用，不能因此否定可见布局审查。必要视觉证据缺失仍不能声称通过。
- 默认尺寸为设计起点，批准的 MASTER / Page Overrides、局部滚动、内容自适应高度及组件变体不自动算缺陷。关键操作遮挡、不可恢复的金额裁切、错误反馈误导等仍需处理。
- 状态按业务适用性覆盖；共享组件维护一次，页面引用差异。公开静态页不制造 loading / permission，真实异步和失败路径也不能借不适用跳过。
- Token 的来源、状态、值 / 别名和组件引用纳入已有模板；已有 token 文件可链接，不重复抄值，不强制新增 JSON/CSS、组件库或实现 API。
- 截图对照记录版本、状态、主题、数据、视口、DPR / 缩放及字体条件；未知项限制相关判断，不妨碍观察可见缺陷。修复说明不覆盖当前同条件截图。
- `context --stage ui-review` 复用现有只读提取器，保留安全与产品事实边界，只取报告模板；按对象加载专项参考，不通读工程 / SQL / 发布内容。

## 评估与验证边界

原案例只有文字“截图证据”与关键词断言，未提供图片；构造明确写未运行、未看截图的报告仍可 19/19 通过。现在用两张真实浏览器截图替换这类输入，并增加批准紧凑布局与无图场景。

- `evals/fixtures/ui-review/source/` 是原创 HTML 和本地 Playwright 截图生成器；`images/` 是评估用 PNG 与尺寸、版本、主题、DPR、数据条件、声明字体和 SHA-256 基线。基线用于可重复取证，不证明字体名称已做底层加载检测。
- `evals/checks/ui_review.py` 仅用于固定 benchmark：检查图片存在 / 基线一致、报告引用、三层结果和案例结论 / finding 一致性。复用产品工具的 Markdown 读取逻辑，不向实际 skill 工作流添加报告格式校验器。用户原格式仍可人工核对。
- 自动断言不能证明模型看过图片或视觉判断正确；实际执行后还需检查看图工具记录，并按 case 的 `review_notes` 人工对照原图与报告。缺图、未执行或文字说明不能冒充视觉通过，也不以一个分数自动交付。
- 正常技能使用不要求安装 Playwright 或重建截图；维护 fixture 时才需本地浏览器。测试不访问真实 Figma、不操作用户页面、不使用生产数据。

维护命令见 [Development](development.md)。执行结果记录在下节；触发预检、布局 dry-run、自动断言和真实模型执行是不同验证层次。

## 当前自动校验边界

二次复查发现正则推断语义既漏检又误拒，现已删除具体视觉缺陷的同义词判分和“无损害”句式推断，不再逐词修补。脚本只服务固定 benchmark，范围标为 `report-structure-and-evidence`，不进入实际 skill 的交付链。

| 状态 / 退出码 | 含义 |
| --- | --- |
| PASS / 0 | 可机械判断的结构、引用和已知输入条件检查通过，且没有需要解析的非空 Findings 内容；不表示视觉质量通过。 |
| REVIEW / 2 | 非空 finding（包括无问题占位行）、列表 / 正文 / 子标题、未知格式、未选定或重复的状态 / 章节等需人工解释；`mechanical_checks_passed=true`，`automated_checks_passed=false`。拿不准不伪装成无问题，也不直接报成产品缺陷。 |
| FAIL / 1 | 存在明确材料问题或固定案例矛盾，如缺图 / 基线不一致、无运行对象却声称机器扫描已完成、无图却声称视觉 / 模板已检查、必要模板检查未完成或明确分级与案例冲突。 |

具体观察、损害程度、证据与核心任务的对应关系沿用案例 `review_notes` 人工对图核对；不新增另一份人工审批文件或评分体系。通用 runner 只把退出 0 计为自动通过，REVIEW 会显示未通过自动检查，但不应记作模型视觉判断错误；应分开报告结构检查、待复核项和人工结论。不要删除 finding 或改写合理的旧报告来凑 PASS。

保留的硬约束仅限确定内容：固定阻断案例明确只有 P2/P3 或空结果时不接受；固定正常对照中的明确 P0/P1 要检查冲突；截图、引用与采集状态要一致；截图不等于运行页面，文件哈希检查不算 UI 机器扫描。真实核心操作遮挡、不可恢复金额裁切和必要错误恢复仍按共享规则处理，没有改成可忽略建议。

空态反馈统一由 `ui-quality-checklist.md` 的条件表维护，蓝图及 Figma 文案步骤引用它；只读空态可解释无需动作，真实错误恢复和写操作反馈仍须覆盖。共享 `ui-review-rules.md` 明确自动结构检查不能替代视觉判断，未识别内容交审查者复核；这不要求实际 UI skill 的每份报告额外人工批准，也不新增全局格式门禁。

本轮验证与复查：

- 回归 102/102，包含本次“无法 / 无损害”正反例、列表 / 正文 / 子标题 / fenced 内容、未选择 / 重复结论、重复章节 / 检查层、真实不可执行扫描声明，以及合法的归属待确认。英文或新的句式不会触发词表扩充，统一保留人工解释。
- 保存的二次复查 8 个场景经真实 CLI 重放：2 个正常对照 PASS，5 个语义 / 选择不明确的报告 REVIEW，1 个无运行输入却声称扫描完成的报告 FAIL；退出码分别为 0 / 2 / 1。原先 4 份错误报告仍不会自动放行。
- 7 份历史真实模型报告重放均无机械错误，并按新边界返回 REVIEW；这是结构重检，不称作自动视觉验收，也不是新模型执行。已有人工对图结论和原始 runner 记录保留，不为凑 PASS 改写报告。
- 静态校验、触发预检 21/21、29 个案例布局 dry-run、Python 编译、安装 dry-run 和 git diff --check 通过。额外 skill-creator quick_validate 仍因环境缺少 PyYAML 未运行成功，未新增依赖。
- 只修改评估器、其测试、蓝图 / Figma 的空态引用、共享审查边界及两份维护文档；对比本轮开始快照，产品工具和模板、benchmark 输入、所有截图及其他原有改动保持不变。没有暂存、提交或推送。

证据在 `/private/tmp/qwerdf-ui-structural-fix-652cgz_w/`：`reproductions-after.json`、`cli-replays.json`、`first-reproductions-replay.json`、`saved-model-artifacts-replay.json` 与 `scope.json`。本轮没有重新执行模型或操作真实设计 / 产品；复查未发现所修边界内新的确定问题，未把机械检查外推为视觉完整性证明。

## 首轮验证记录

- 工具回归测试 72/72：包含原关键词假通过、缺图 / 图片变更、未看截图、证据引用别名、限定范围的加粗结论、带编号 finding、正常无 finding 写法、紧凑模式、不适用运行检查和非阻断 P2。
- 三个真实模型场景均退出 0 并生成报告，逐图 / 逐报告读回后符合预期：移动端提交文案遮挡判为 P1，不臆测完全无法点击；批准的 8px 边距、紫色品牌、自适应行高和静态 default 可继续；只有修复说明时保持证据不足，不编造视觉 finding。
- 初次机械判分为 1/3：两份报告因正常的加粗 / 标点、finding 编号、E1 引用和无 finding 说明被过窄断言误拒。已增加兼容及回归，用最终评估器重检原始三份产物，3/3 通过；保留原始运行日志，不将重检冒充新一轮模型执行。
- 真实执行证据在 `/private/tmp/qwerdf-ui-execution/20261021T080810Z/`，最终重检为 `/private/tmp/qwerdf-ui-final-recheck.json`。每个场景一次执行，没有旧技能 / 无技能对照，也没有统计成功率或视觉质量提升结论。CLI 文本日志不完整保留原生看图调用；此处人工核对基于真实输入图、派生局部图和报告内容，不把“已看图”自述当作程序证明。
- 仓库静态校验（含全部 benchmark 布局 dry-run）、触发预检 21/21、Python 编译、安装 dry-run 和 `git diff --check` 通过。系统 skill-creator 的额外 quick_validate 因环境缺少 PyYAML 未完成，未为此安装依赖；本仓库静态验证覆盖元数据、目录、引用和边界，行为证据如上。
- 原有产品阶段修改及无关工作区内容已与本轮前快照核对保留。没有修改真实设计或产品实现，没有提交或推送。

## 2026-10-21 第一次复查修正（历史记录）

本节的关键词判分实现与通过数是上轮快照，已由「当前自动校验边界」替代；不据此解释当前工具状态。

针对复查的 5 项 P2，只修复已有评估漏洞和共享规则衔接，不加入新的产品工作流校验器：

- 固定阻断案例要求 finding 观察同时指向核心对象及其缺陷。仅写无关辅助文字裁切，不能替代提交按钮遮挡、关键金额裁切或保存失败反馈缺失。断言支持不同描述和编号，仍不能证明模型真正理解图像；人工按图复查保留。
- Findings 解析限于结果章节；不能识别的实际问题表 / 分级记录进入 `review_required`，不会当作没有问题。无 finding 行同时需要明确空结果和无实际损害，不因“未发现恢复入口”跳过真实问题。这里的格式约定仅用于固定 benchmark，用户旧格式仍可等价人工核对。
- 紧凑目录有三条同类行，模板比较是该案例的必要检查；“未验证”或错误写成“不适用”不能通过。单一金额摘要没有同类对象时仍可不适用；截图的运行扫描仍可不适用。
- 删除 `pd-review` 的重复 UI 分级；UI 严重性及证据缺口读取 `ui-review-rules.md`。P0/P1 是受影响范围阻断，P2/P3 是残余风险。
- 状态适用性条件只在 `ui-quality-checklist.md` 维护；技术设计、前端实现、工程验收模板及前端 Code Review 引用它。静态页不强制造保存 / 权限态；实际异步、写入、错误恢复和权限差异仍须覆盖，必要检查未执行不能写成已验证。

新增两组正反视觉用例：

| 场景 | 输入与必要事实 | 预期 |
| --- | --- | --- |
| amount-clipped / amount-readable | 同一付款确认摘要、同一 28px 金额字号；仅容器容纳策略不同。产品明确该处是唯一金额来源，无 tooltip / 展开等恢复路径。 | 尾数裁切为 P1；完整可读版本可继续。不能从截图猜被裁掉的金额。 |
| save-error / save-error-feedback | 本地合成表单实际点击保存后，邮箱格式校验拒绝；capture.cjs 记录 rejected、原因及输入保留到 baseline.json。分别缺少或具备可见错误说明及改正指引。 | 必要反馈缺失为 P1；反馈完整版本可继续。不是实际服务接口失败，也不能只从默认画面没有红字推断错误态缺失。 |

新增 4 张 PNG 来自本地浏览器，两张原有 PNG 的 SHA-256 保持不变。采集器及状态记录只服务合成评估，不进入真实产品、实现路径或联调通过证据。

验证：工具回归 89/89、触发预检 21/21、仓库静态校验和 git diff --check 通过。先加入复现用例，原评估器出现 5 个失败断言（4 个测试方法，含未验证 / 不适用两个子例），再实施修正。保存的 4 份错误报告重放均不再自动通过，2 份正确对照仍通过；上轮 3 份真实报告用当前评估器重检仍通过。这些重放不是新模型执行。

复现修正前后证据：`/private/tmp/qwerdf-ui-audit-ek5e4676/results.json` 与 `after-fix.json`。本轮新增真实模型执行目录为 `/private/tmp/qwerdf-ui-fix-execution/20261021T083954Z/`。金额正常对照的“无 finding”行使用“当前样本未见裁切 / 可完整读取”表达，初版断言误拒；已补回归、接受可读性和“未见反馈妨碍理解”等等价无损害表达，同时保留“未发现恢复入口，金额被裁切”的拒绝反例。原始运行日志保留，不把重检冒充新的模型运行。


本轮真实执行完成后的读回：

- 4 份报告均人工对照原始截图及必要采集记录：金额裁切 / 失败反馈缺失各为 P1；金额完整 / 反馈完整各可在本轮静态范围继续。均区分静态结论与未验证行为，没有据此声称真实支付或保存接口通过。
- 原始 runner 为 1/4，不改写该记录：金额裁切场景已产出有效报告，但模型进程因容量错误退出 1；两份正常报告被执行时复制的旧版“无 finding”写法断言误拒。其他 3 个模型进程退出 0，均未超时。
- 最终评估器重检原始 4 份产物为 4/4，结果位于 `/private/tmp/qwerdf-ui-fix-final-recheck.json`；这是产物重检，不能改称原始执行 4/4 或新的模型运行。上轮 3 份真实报告仍通过；保存的 4 份错误报告均拒绝、2 份正确对照均通过。
- 89 项回归、静态校验、21/21 触发预检、29 个案例布局 dry-run、Python 编译、安装 dry-run 与 git diff --check 通过。安装仍为指向本仓库的 live symlink。系统 skill-creator quick_validate 仍因缺少 PyYAML 无法运行，未安装新依赖。
- 与本轮开始前快照逐文件核对：仅修改本次评估、UI 共享规则及消费方、设计维护文档；先前产品工具 / 模板、两张原有 PNG 和其他工作区修改保留。没有暂存、提交或推送。

这些是少量合成场景和确定性反例，未做无 skill 对照、重复采样或真实 Figma / 产品运行验收；自动断言仍不证明看图或完整理解，自述和分数不替代人工视觉复核。该次复查只验证了记录中的场景，后续新增反例与修正见当前边界说明。
