# Backend Code Review

当 diff 涉及 Java、Spring Boot、Controller / Service / Repository、SQL、迁移、数据模型、权限或后端 API 时读取。

Java 审查必读公共规范的 [结构与可维护性](../../qwerdf-common/java-coding-rules.md#结构与可维护性) 和 [任务完成前自查](../../qwerdf-common/java-coding-rules.md#任务完成前自查)，其余语言与框架章节按改动核对。沿实际代码与调用路径独立核查，不因任务条目写了“已自查”或测试通过就放行；命名 / 格式服从当前仓库配置，不重复维护另一份规则，也不把风格建议升级为业务阻断。

## Java / Spring Boot

- Controller 只处理协议、参数校验和响应映射；业务规则放在 service，持久化细节放在 repository / mapper。
- DTO 校验、权限校验、异常映射和错误码必须与 `tech/api-contract.md` 一致；不要把内部异常、堆栈或数据库错误直接回给前端。
- 检查 `@Transactional` 位置、传播行为、只读事务、部分成功和异常被捕获后事务是否仍能正确回滚。
- 资源使用要可关闭：流、文件、连接、锁、线程池、定时任务和外部 client 不应泄漏。
- 日志要包含定位所需业务 ID / trace 信息，但不得记录 token、密码、密钥、完整敏感对象或过量 payload。

## 数据模型 / SQL

- Java 持久化选型、业务 SQL 归属、Mapper / XML 绑定及事务边界，以及数据约束、业务唯一性与查询边界，统一按 [共享持久化规则](../../qwerdf-common/java-coding-rules.md#spring-事务与持久化涉及数据库时) 核对；本处不另设 ORM、排序、分页或唯一约束的判断标准。
- SQL / 迁移按项目当前阶段与已确认兼容目标审查；需要迁移时核对已有数据、回填和回滚，不在明确无需旧版本兼容的开发项目强加灰度、双写或历史迁移。写文件不等于执行 SQL。
- 并发写入要检查唯一键冲突、乐观 / 悲观锁、重复请求、幂等键和最终状态。

## API / 契约

- path、method、request、response、错误结构、状态码、分页结构和状态枚举必须匹配契约。
- 权限失败、资源不存在、参数错误和业务冲突应有可区分错误码；不要全部映射为 500 或通用错误。
- API client、integration-map 和真实后端 DTO 字段命名必须一致；生产路径不得用模拟替代应有能力；测试替身与合成 fixture 按 [共享验证分层](../../qwerdf-common/product-delivery-flow.md#验证分层与独立预期) 核对证明边界。

## 测试切片

以下按本轮改动实际触及的行为与风险核对覆盖，不要求每个小改动补齐各层全套用例；执行频率、证据复用与必要回归沿用入口已加载的共享验证规则。

- Controller 测试覆盖参数校验、权限、错误映射和 response contract。
- Service 测试覆盖业务分支、事务失败、幂等、重复执行、并发或回滚路径。
- Repository / integration 按实际范围检查字段投影、映射、约束与查询行为；需证明真实 SQL / 事务代理时调用实际 Repository / Mapper / Spring 代理及数据库，不能靠手工补全对象证明映射正确。迁移兼容按本项目真实要求核对。
