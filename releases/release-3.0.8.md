---
title: TiDB 3.0.8 Release Notes
---

# TiDB 3.0.8 Release Notes

发版日期：2019 年 12 月 31 日

TiDB 版本：3.0.8

TiDB Ansible 版本：3.0.8

## TiDB

+ SQL 优化器
    - 修复 SQL Binding 因为 cache 更新不及时，导致绑定计划错误的问题 [#13891](https://github.com/pingcap/tidb/pull/13891)
    - 修复当 SQL 包含符号列表（类似于 "?, ?, ?" 这样的占位符）时，SQL Binding 可能失效的问题 [#14004](https://github.com/pingcap/tidb/pull/14004)
    - 修复 SQL Binding 由于原 SQL 以 `;` 结尾而不能创建/删除的问题 [#14113](https://github.com/pingcap/tidb/pull/14113)
    - 修复 `PhysicalUnionScan` 算子没有正确设置统计信息，导致查询计划可能选错的问题 [#14133](https://github.com/pingcap/tidb/pull/14133)
    - 移除 `minAutoAnalyzeRatio` 约束使自动 analyze 更及时 [#14015](https://github.com/pingcap/tidb/pull/14015)
+ SQL 执行引擎
    - 修复 `INSERT/REPLACE/UPDATE ... SET ... = DEFAULT` 语法会报错的问题，修复 `DEFAULT` 表达式与虚拟生成列配合使用会报错的问题 [#13682](https://github.com/pingcap/tidb/pull/13682)
    - 修复 `INSERT` 语句在进行字符串类型到浮点类型转换时，可能会报错的问题 [#14011](https://github.com/pingcap/tidb/pull/14011)
    - 修复 `HashAgg` Executor 并发值未被正确初始化，导致聚合操作执行在一些情况下效率低的问题 [#13811](https://github.com/pingcap/tidb/pull/13811)
    - 修复 group by item 被括号包含时执行报错的问题 [#13658](https://github.com/pingcap/tidb/pull/13658)
    - 修复 TiDB 没有正确计算 group by item，导致某些情况下 OUTER JOIN 执行会报错的问题 [#14014](https://github.com/pingcap/tidb/pull/14014)
    - 修复向 Range 分区表写入超过 Range 外的数据时，报错信息不准确的问题 [#14107](https://github.com/pingcap/tidb/pull/14107)
    - 鉴于 MySQL 8 即将废弃 `PadCharToFullLength`，revert PR [#10124](https://github.com/pingcap/tidb/pull/10124) 并撤销 `PadCharToFullLength` 的效果，以避免一些特殊情况下查询结果不符合预期 [#14157](https://github.com/pingcap/tidb/pull/14157)
    - 修复 `ExplainExec` 中没有保证 `close()` 的调用而导致 `EXPLAIN ANALYZE` 时造成 goroutine 泄露的问题 [#14226](https://github.com/pingcap/tidb/pull/14226)
+ DDL
    - 优化 "change column"/"modify column" 的输出的报错信息，让人更容易理解 [#13796](https://github.com/pingcap/tidb/pull/13796)
    - 新增 `SPLIT PARTITION TABLE` 语法，支持分区表切分 Region 功能 [#13929](https://github.com/pingcap/tidb/pull/13929)
    - 修复创建索引时，没有正确检查长度，导致索引长度超过 3072 字节没有报错的问题 [#13779](https://github.com/pingcap/tidb/pull/13779)
    - 修复由于分区表添加索引时若花费时间过长，可能导致输出 `GC life time is shorter than transaction duration` 报错信息的问题 [#14132](https://github.com/pingcap/tidb/pull/14132)
    - 修复在 `DROP COLUMN`/`MODIFY COLUMN`/`CHANGE COLUMN` 时没有检查外键导致执行 `SELECT * FROM information_schema.KEY_COLUMN_USAGE` 语句时发生 panic 的问题 [#14105](https://github.com/pingcap/tidb/pull/14105)
+ Server
    - Statement Summary 功能改进：
        - 新增大量的 SQL 指标字段，便于对 SQL 进行更详细的统计分析 [#14151](https://github.com/pingcap/tidb/pull/14151)，[#14168](https://github.com/pingcap/tidb/pull/14168)
        - 新增 `stmt-summary.refresh-interval` 参数用于控制定期将 `events_statements_summary_by_digest` 表中过期的数据移到  `events_statements_summary_by_digest_history` 表，默认间隔时间：30min [#14161](https://github.com/pingcap/tidb/pull/14161)
        - 新增 `events_statements_summary_by_digest_history` 表，保存从 `events_statements_summary_by_digest` 中过期的数据 [#14166](https://github.com/pingcap/tidb/pull/14166)
    - 修复执行 RBAC 相关的内部 SQL 时，错误输出 binlog 的问题 [#13890](https://github.com/pingcap/tidb/pull/13890)
    - 新增 `server-version` 配置项来控制修改 TiDB server 版本的功能 [#13906](https://github.com/pingcap/tidb/pull/13906)
    - 新增通过 HTTP 接口恢复 TiDB binlog 写入功能 [#13892](https://github.com/pingcap/tidb/pull/13892)
    - 将 `GRANT roles TO user` 所需要的权限由 `GrantPriv` 修改为 `ROLE_ADMIN` 或 `SUPER`，以与 MySQL 保持一致 [#13932](https://github.com/pingcap/tidb/pull/13932)
    - 当 `GRANT` 语句未指定 database 名时，TiDB 行为由使用当前 database 改为报错 `No database selected`，与 MySQL 保持兼容 [#13784](https://github.com/pingcap/tidb/pull/13784)
    - 修改 `REVOKE` 语句执行权限从 `SuperPriv` 改成用户只需要有对应 Schema 的权限，就可以执行 `REVOKE` 语句，与 MySQL 保持一致 [#13306](https://github.com/pingcap/tidb/pull/13306)
    - 修复 `GRANT ALL` 语法在没有 `WITH GRANT OPTION` 时，错误地将 `GrantPriv` 授权给目标用户的问题 [#13943](https://github.com/pingcap/tidb/pull/13943)
    - 修复 `LoadDataInfo` 中调用 `addRecord` 报错时，报错信息不包含导致 `LOAD DATA` 语句行为不正确信息的问题 [#13980](https://github.com/pingcap/tidb/pull/13980)
    - 修复因查询中多个 SQL 语句共用同一个 `StartTime` 导致输出错误的慢查询信息的问题 [#13898](https://github.com/pingcap/tidb/pull/13898)
    - 修复 `batchClient` 处理大事务时可能造成内存泄露的问题 [#14032](https://github.com/pingcap/tidb/pull/14032)
    - 修复 `system_time_zone` 固定显示为 `CST` 的问题，现在 TiDB 的 `system_time_zone` 会从 `mysql.tidb` 表中的 `systemTZ` 获取 [#14086](https://github.com/pingcap/tidb/pull/14086)
    - 修复 `GRANT ALL` 语法授予权限不完整（例如 `Lock_tables_priv`）的问题 [#14092](https://github.com/pingcap/tidb/pull/14092)
    - 修复 `Priv_create_user` 权限不能 `CREATE ROLE` 和 `DROP ROLE`的问题 [#14088](https://github.com/pingcap/tidb/pull/14088)
    - 将 `ErrInvalidFieldSize` 的错误码从 `1105(Unknow Error)` 改成 `3013` [#13737](https://github.com/pingcap/tidb/pull/13737)
    - 新增 `SHUTDOWN` 命令用于停止 TiDB Server，并新增 `ShutdownPriv` 权限 [#14104](https://github.com/pingcap/tidb/pull/14104)
    - 修复 `DROP ROLE` 语句的原子性问题，避免语句执行失败时，一些 ROLE 仍然被非预期地删除 [#14130](https://github.com/pingcap/tidb/pull/14130)
    - 修复 3.0 以下版本升级到 3.0 时，`tidb_enable_window_function` 在 `SHOW VARIABLE` 语句的查询结果错误输出 1 的问题，修复后输出 0 [#14131](https://github.com/pingcap/tidb/pull/14131)
    - 修复 TiKV 节点下线时，由于 `gcworker` 持续重试导致可能出现 goroutine 泄露的问题 [#14106](https://github.com/pingcap/tidb/pull/14106)
    - 在慢日志中记录 Binlog 的 `Prewrite` 的时间，提升问题追查的易用性 [#14138](https://github.com/pingcap/tidb/pull/14138)
    - `tidb_enable_table_partition` 变量支持 GLOBAL SCOPE 作用域 [#14091](https://github.com/pingcap/tidb/pull/14091)
    - 修复新增权限时未正确将新增的权限赋予对应的用户导致用户权限可能缺失或者被误添加的问题 [#14178](https://github.com/pingcap/tidb/pull/14178)
    - 修复当 TiKV 链接断开时，由于 `rpcClient` 不会关闭而导致 `CheckStreamTimeoutLoop` goroutine 会泄露的问题 [#14227](https://github.com/pingcap/tidb/pull/14227)
    - 支持基于证书的身份验证（[使用文档](/certificate-authentication.md)）[#13955](https://github.com/pingcap/tidb/pull/13955)
+ Transaction
    - 创建新集群时，`tidb_txn_mode` 变量的默认值由 `""` 改为 `"pessimistic"` [#14171](https://github.com/pingcap/tidb/pull/14171)
    - 修复悲观事务模式，事务重试时单条语句的等锁时间没有被重置导致等锁时间过长的问题 [#13990](https://github.com/pingcap/tidb/pull/13990)
    - 修复悲观事务模式，因对没有修改的数据未加锁导致可能读到不正确数据的问题 [#14050](https://github.com/pingcap/tidb/pull/14050)
    - 修复 mocktikv 中 prewrite 时，没有区分事务类型，导致重复的 insert value 约束检查 [#14175](https://github.com/pingcap/tidb/pull/14175)
    - 修复 `session.TxnState` 状态为 `Invalid` 时，事务没有被正确处理导致 panic 的问题 [#13988](https://github.com/pingcap/tidb/pull/13988)
    - 修复 mocktikv 中 `ErrConfclit` 结构未包含 `ConflictCommitTS` 的问题 [#14080](https://github.com/pingcap/tidb/pull/14080)
    - 修复 TiDB 在 Resolve Lock 之后，没有正确处理锁超时检查导致事务卡住的问题 [#14083](https://github.com/pingcap/tidb/pull/14083)
+ Monitor
    - `LockKeys` 新增 `pessimistic_lock_keys_duration` 监控 [#14194](https://github.com/pingcap/tidb/pull/14194)

## TiKV

+ Coprocessor
    - 修改 Coprocessor 遇到错误时输出日志的级别从 `error` 改成 `warn` [#6051](https://github.com/tikv/tikv/pull/6051)
    - 修改统计信息采样数据的更新行为从直接更行改成先删除再插入，更新行为与 tidb-server 保持一致 [#6069](https://github.com/tikv/tikv/pull/6096)
+ Raftstore
    - 修复因重复向 `peerfsm` 发送 destory 消息，`peerfsm` 被多次销毁导致 panic 的问题 [#6297](https://github.com/tikv/tikv/pull/6297)
    - `split-region-on-table` 默认值由 `true` 改成 `false`，默认关闭按 table 切分 Region 的功能 [#6253](https://github.com/tikv/tikv/pull/6253)
+ Engine
    - 修复极端条件下因 RocksDB 迭代器错误未正确处理导致可能返回空数据的问题 [#6326](https://github.com/tikv/tikv/pull/6326)
+ 事务
    - 修复悲观锁因锁未被正确清理导致 Key 无法写入数据，且出现 GC 卡住的问题 [#6354](https://github.com/tikv/tikv/pull/6354)
    - 优化悲观锁等锁机制，提升锁冲突严重场景的性能 [#6296](https://github.com/tikv/tikv/pull/6296)
+ 将内存分配库的默认值由 `tikv_alloc/default` 改成 `jemalloc` [#6206](https://github.com/tikv/tikv/pull/6206)

## PD

- Client
    - 新增通过 `context` 创建新 client，创建新 client 时可设置超时时间 [#1994](https://github.com/pingcap/pd/pull/1994)
    - 新增创建 `KeepAlive` 连接功能 [#2035](https://github.com/pingcap/pd/pull/2035)
- 优化`/api/v1/regions` API 的性能 [#1986](https://github.com/pingcap/pd/pull/1986)
- 修复删除 `tombstone` 状态的 Store 可能会导致 panic 的隐患 [#2038](https://github.com/pingcap/pd/pull/2038)
- 修复从磁盘加载 Region 信息时错误的将范围有重叠的 Region 删除的问题 [#2011](https://github.com/pingcap/pd/issues/2011)，[#2040](https://github.com/pingcap/pd/pull/2040)
- 将 etcd 版本从 3.4.0 升级到 3.4.3 稳定版本，注意升级后只能通过 pd-recover 工具降级 [#2058](https://github.com/pingcap/pd/pull/2058)

## Tools

+ TiDB Binlog
    - 修复 Pump 由于没有收到 DDL 的 commit binlog 导致 binlog 被忽略的问题 [#853](https://github.com/pingcap/tidb-binlog/pull/853)

## TiDB Ansible

- 回滚被精简的配置项 [#1053](https://github.com/pingcap/tidb-ansible/pull/1053)
- 优化滚动升级时 TiDB 版本检查的逻辑 [#1056](https://github.com/pingcap/tidb-ansible/pull/1056)
- TiSpark 版本升级到 2.1.8 [#1061](https://github.com/pingcap/tidb-ansible/pull/1061)
- 修复 Grafana 监控上 PD 页面 Role 监控项显示不正确的问题 [#1065](https://github.com/pingcap/tidb-ansible/pull/1065)
- 优化 Grafana 监控上 TiKV Detail 页面上 `Thread Voluntary Context Switches` 和 `Thread Nonvoluntary Context Switches` 监控项 [#1071](https://github.com/pingcap/tidb-ansible/pull/1071)
