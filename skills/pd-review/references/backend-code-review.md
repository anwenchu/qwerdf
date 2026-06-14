# Backend Code Review

当 diff 涉及 Java、Spring Boot、Controller / Service / Repository、SQL、迁移、数据模型、权限或后端 API 时读取。

## Java / Spring Boot

- Controller 只处理协议、参数校验和响应映射；业务规则放在 service，持久化细节放在 repository / mapper。
- DTO 校验、权限校验、异常映射和错误码必须与 `tech/api-contract.md` 一致；不要把内部异常、堆栈或数据库错误直接回给前端。
- 检查 `@Transactional` 位置、传播行为、只读事务、部分成功和异常被捕获后事务是否仍能正确回滚。
- 资源使用要可关闭：流、文件、连接、锁、线程池、定时任务和外部 client 不应泄漏。
- 日志要包含定位所需业务 ID / trace 信息，但不得记录 token、密码、密钥、完整敏感对象或过量 payload。

## 数据模型 / SQL

- 唯一约束、外键、索引、非空、默认值、状态字段、软删除和业务校验必须一致。
- 迁移要兼容已有数据：新增非空列要有默认或回填策略，删除 / 改名字段要有灰度和回滚说明。
- 查询必须有稳定排序和分页；避免无界查询、N+1、重复查询、全表扫描和缺失索引的过滤条件。
- 并发写入要检查唯一键冲突、乐观 / 悲观锁、重复请求、幂等键和最终状态。

## API / 契约

- path、method、request、response、错误结构、状态码、分页结构和状态枚举必须匹配契约。
- 权限失败、资源不存在、参数错误和业务冲突应有可区分错误码；不要全部映射为 500 或通用错误。
- API client / mock / integration-map 中的字段命名和真实后端 DTO 命名必须一致。

## 测试切片

- Controller 测试覆盖参数校验、权限、错误映射和 response contract。
- Service 测试覆盖业务分支、事务失败、幂等、重复执行、并发或回滚路径。
- Repository / integration 测试覆盖约束、分页、排序、迁移兼容和真实 SQL 行为。
