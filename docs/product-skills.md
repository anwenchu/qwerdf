# Product Skills：来源、改动与验证

## 本次范围

`pd-vet`、`pd-prd` 和 `pd-blueprint` 的产品输入衔接。保留技能名称、触发描述、安装方式、canonical 输出路径和 UI 规则；不重写 Figma、技术设计、实现或发布流程。旧编号与产物可继续使用，脚本不改写旧产物。

## 实际阅读的外部来源

2026-10-21 读取两个仓库的完整文件树，并固定以下版本进行相关文档和源码阅读。下面是与本次产品改动有关的阅读范围，不代表逐个阅读了与本任务无关的艺术资源、Office schema 或其他 SDK。

### agentskills/agentskills

版本：[`69ef37e9424c0a7ea9dd2293b559e43ec8176379`](https://github.com/agentskills/agentskills/tree/69ef37e9424c0a7ea9dd2293b559e43ec8176379)。

| 阅读文件 | 借鉴 / 判断 |
| --- | --- |
| [格式规范](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/specification.mdx) | 区分元数据、入口、按需资源；500 行是建议上限，不是“达到 500 行才拆分”。 |
| [编写实践](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/skill-creation/best-practices.mdx) | 根据真实工作选择规则；引用必须说明何时读取；确定性校验形成反馈闭环。 |
| [脚本设计](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/skill-creation/using-scripts.mdx) | 无交互输入、清晰错误、结构化输出、退出码；不把大段脚本源码载入执行上下文。 |
| [输出评估](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/skill-creation/evaluating-skills.mdx) | 检查实际产物、保留执行证据；机械断言与读者判断分开；比较旧版时保存快照。 |
| [触发描述优化](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/docs/skill-creation/optimizing-descriptions.mdx) | 正反例及相邻任务边界很重要；本次未发现需要改触发描述的证据，因此保持现有描述。 |
| [参考验证器源码](https://github.com/agentskills/agentskills/blob/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref/src/skills_ref/validator.py) | 检查元数据、命名、目录对应；它不验证 PRD 的业务状态。 |

### anthropics/skills

版本：[`dbd4588f9e1033efb41dad4bef2f7947c8993d44`](https://github.com/anthropics/skills/tree/dbd4588f9e1033efb41dad4bef2f7947c8993d44)。

| 阅读文件 | 借鉴 / 判断 |
| --- | --- |
| [skill-creator](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/SKILL.md) | 先理解意图，基于实际执行改进；保留已有技能标识，避免把单个例子硬编码为通用流程。 |
| [quick_validate.py](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/scripts/quick_validate.py) | 快速校验是文件格式检查，不能直接用作产品需求验收。 |
| [grader](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/agents/grader.md) | 有文件或标题不等于工作完成；通过结论需要实际证据，并检查断言是否过弱。 |
| [评估结构](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/skill-creator/references/schemas.md)（evals / grading 部分） | 每条判断记录结果与证据，不只有总体通过率。 |
| [文档共创](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/doc-coauthoring/SKILL.md) | 上下文收集、局部修订、读者视角检查；不照搬固定问题数量或强制逐段等待的节奏。 |
| [internal-comms](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/internal-comms/SKILL.md) | 入口识别类型，再读取相应参考，而非全部加载。 |
| [webapp-testing](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/webapp-testing/SKILL.md) | 工具按接口调用，保留运行与产物证据；本次不引入浏览器测试。 |
| [mcp-builder](https://github.com/anthropics/skills/blob/dbd4588f9e1033efb41dad4bef2f7947c8993d44/skills/mcp-builder/SKILL.md) | 按任务加载特定参考，校验可观测结果；不引入 MCP 实现流程。 |

这些仓库提供格式、组织和评估方法。以下来源 / 需求 / 验收追溯是 qwerdf 的本地产品规则，不是外部标准规定的 PRD schema；SRC / REQ / AC 仅为新编号建议，覆盖矩阵按需使用。未复制外部文档正文、实现代码或受限资产。

## 现状问题与对应修改

1. 产品入口短，但要求先读取完整 `product-delivery-flow.md`，会引入下游 SQL、真实依赖、提交和发布规则。新增 `context` 子命令按阶段提取原规则和模板，保持原文件为唯一来源，避免另建重复规则集。
2. 原 PRD 模板主要是章节标题，验收主要是 UI 状态勾选；不能检查来源、需求与验收是否对应。增加来源追溯、前置条件 / 事件 / 可观察结果；以验收表中的 AC → 需求关系为唯一权威关联，避免多处维护完整 AC 清单，复杂需求可加业务状态与边界矩阵。
3. 原机会判断和 PRD 摘要无条件提示下一阶段。改为按实际建议、材料检查、业务自审和未解决阻断项决定下一步。
4. 增加产品阶段参考，区分事实、假设、未提供证据、MVP 与后续范围；指标没有基线时不编数值。

## 工具接口

需要 Python 3.10+，不安装第三方包。以下命令在仓库根目录执行；已安装技能需用实际 skill 所在目录定位相对工具路径。

```bash
python3 skills/qwerdf-common/scripts/product_artifacts.py --help
python3 skills/qwerdf-common/scripts/product_artifacts.py context --stage prd
python3 skills/qwerdf-common/scripts/product_artifacts.py validate --stage prd --root pd-work/example --format json
```

- `context` 支持 `vet`、`prd`、`blueprint`；只输出相关片段（含共享安全与外部操作边界），不写文件。公共规则节名或模板缺失时明确失败，不静默跳过。
- `validate` 支持 `vet`、`prd`；只读产物。退出码 0 为未检出明确阻断（包含 `REVIEW`），1 为明确冲突或业务阻断，2 为参数或读取失败；自动化必须检查 JSON 的 `status` 或 `passed`，不能用退出码 0 代替通过。
- 优先 canonical path，缺失时可读取同名旧平铺文件，并在 JSON 中标记 `legacy_reads`。无法识别的结构提示人工核对，不强制迁移或补齐无关历史材料。
- Python 不可用或原格式不适配时，技能可手动读取所需章节并核对同等业务约束，记录方式、结论和未决项。人工核对完成且无业务阻断即可交接，不能伪报机械校验已通过。

## 验证边界

| 结果 | 条件与处理 |
| --- | --- |
| `BLOCKED` | 可识别结构中的重复编号、明确未知引用或矛盾关联、正式需求依赖未确认来源、已识别需求没有验收、明确未解决的阻断问题；修正或澄清后重跑。草稿可以保留未确认来源，但不能作为已确认需求交接。 |
| `REVIEW` | 缺文件 / 正文、未识别表格或关联、空字段、未识别章节、模糊结果、已有覆盖表的未说明项或无法判断的开放问题状态；人工核对实际内容和本次范围，不因格式问题强制重写。 |
| `PASS` | 未检出上述机械问题，JSON `passed` 为 true；仍需业务自审。非阻断问题确认人待定仅为提醒（`requires_review: false`），可保持 PASS。 |

旧的 R1 / S1 / A1 等稳定编号、中文紧邻引用、等价标题均兼容。需求清单与用户故事无需列全 AC，覆盖矩阵可省略；旧版反向清单仍可读取，但明确矛盾会报错。开放问题中的“无”只从实际可见声明读取，代码示例或注释不能覆盖尚未澄清的问题。

仍需产品审阅：用户是否真有该问题、来源是否真实、优先级及范围是否合理、AC 是否表达了正确权限或状态语义、不适用理由是否成立、指标是否可信。脚本不能判断“把成功 AC 填到权限列”这类语义伪覆盖；不能用机械 PASS 证明需求已确认。

运行 `python3 -m unittest discover -s scripts/tests -v` 检查工具行为。触发预检和 benchmark dry-run 都不代表模型真实执行通过；真实评估需要检查进程、产物和每条断言。耗时与 token 优化只有在实际运行对照后才能下结论；本次可直接比较的是声明读取路径下的文本字符数。

## 2026-10-21 首轮验证记录

- 修改前：仓库静态校验通过；触发预检 21/21。
- 首轮修改后：工具行为测试 33/33；仓库静态校验、触发预检 21/21、Python 编译、`git diff --check`、安装 dry-run 通过。仓库静态校验还执行全部 benchmark case 的布局 dry-run。
- “权限和撤回规则未确认”真实执行场景通过，并人工读回产物：只创建开放问题，将两项问题标为未解决阻断，没有擅自补规则或生成正式 PRD。
- 初次完整 PRD 执行达到 180 秒时限，未生成产物，不能算通过；日志出现连接流错误。延长时限后重跑通过（约 241 秒），生成五份产品产物；用当时的工具版本再次检查通过，并读回全部五份产物核对范围、来源和验收。案例包含 5 项需求、17 条 AC；未编造访谈或改善指标，保留非阻断效果验证问题。
- 两类真实场景各取得一次通过结果；没有执行旧技能 / 无技能对照，也没有重复采样，不能据此声称需求质量或执行成功率有统计提升。
- 旧 benchmark runner 把 `--ask-for-approval` 放在 `exec` 后，本机 CLI 不接受。验证时用 runner 已支持的自定义命令把该参数放在 `exec` 前；未修改全局配置或项目 runner。

## 复审修正与回归

- 兼容旧编号、中文紧邻引用及等价标题；非阻断问题确认人待定仅提醒。
- 不再从示例或注释中的“无”推断没有开放问题；无法识别正文问题状态时返回 REVIEW，交接前人工核对。
- 共享上下文恢复安全规则；工具不可用或格式不适配时，技能给出等价人工核对路径。
- 去掉需求清单、用户故事与覆盖表中完整 AC 清单的重复维护；覆盖矩阵可省略、裁剪维度或按风险分行，保留明确错误引用及矛盾检查。
- 完整 PRD benchmark 的断言显式要求 JSON `status == "PASS"`，防止把退出码 0 的 REVIEW 误算通过；用回归测试验证两者差异。
- 修正后：工具行为测试 53/53，包含原先复现的误判与关键约束反例；保存的 9 组复现材料重放均符合预期（7 组 PASS，示例 / 注释掩盖正文问题的 2 组 REVIEW）。此前真实模型生成的五份 PRD 产物用当前工具复查为 PASS。本轮未重新执行模型生成，不把产物重放当作新的模型评估。
- 仓库静态校验（含全部 benchmark 布局 dry-run）、触发预检 21/21、Python 编译、安装 dry-run、`git diff --check` 通过；对比首轮修改前快照，其他技能的原有文件内容保持不变。未提交或推送。

以下是产品阶段修正完成时的历史字符数记录，后续 UI 迭代可能改变这些值；不作为当前值。对比：旧版入口 + 完整共享流程 + 本阶段模板，对比当前入口 + 提取片段 + 新增阶段参考；蓝图两侧都计入原有三个 UI 参考，不计用户材料和对话历史。

| 阶段 | 修改前字符数 | 修改后字符数 | 减少 |
| --- | ---: | ---: | ---: |
| vet | 19,958 | 5,943 | 70.2% |
| prd | 19,651 | 7,787 | 60.4% |
| blueprint | 31,050 | 18,144 | 41.6% |

这是声明读取路径下的静态字符对比；没有把它当作实际 token、耗时或需求质量的提升比例。
