# 合成依赖输入：同名类来源不明

本例仅为审查原始材料，不是真实项目的依赖状态。

应用的依赖解析结果包含两个制品，均声明 `sample.identity.UserMapper`：

| 制品 | 当前解析版本 | 声明位置 | 可见方法 |
| --- | --- | --- | --- |
| identity-storage | 2.4 | archive-a/sample/identity/UserMapper.java | findByOrgAndEmail(org, email) |
| identity-common | 2.4 | archive-b/sample/identity/UserMapper.java | findByOrgEmailAndSource(org, email, source) |

已知两个制品都进入打包清单；尚未提供打包排序、实际装载类来源、Mapper 注册位置或运行配置。仅检查 archive-a 并不能证明当前应用没有按 source 查询的能力；看到 archive-b 也不能证明实际正在使用其实现。没有足够证据断言必须升级版本、修改公共库或已经兼容。
