---
title: TiDB 4.0.2 Release Notes
---

# TiDB 4.0.2 Release Notes

发版日期：2020 年 7 月 1 日

TiDB 版本：4.0.2

## 兼容性

+ TiDB

    - 移除慢查询日志和 statement summary 表中的敏感信息 [#18130](https://github.com/pingcap/tidb/pull/18130)
    - 禁止在 sequence 缓存中出现负数 [#18103](https://github.com/pingcap/tidb/pull/18103)
    - `CLUSTER_INFO` 表中不再显示 tombstone 状态的 TiKV 和 TiFlash 节点 [#17953](https://github.com/pingcap/tidb/pull/17953)
    - 诊断规则 `current-load` 变更为 `node-check` [#17660](https://github.com/pingcap/tidb/pull/17660)

+ PD

    - 持久化 `store-limit` 配置项，弃用 `store-balance-rate` 配置 [#2557](https://github.com/pingcap/pd/pull/2557)

## 新更改

- TiDB 及 TiDB Dashboard 默认收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品 [#18180](https://github.com/pingcap/tidb/pull/18180)。若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)文档。

## 新功能

+ TiDB

    - 支持在 `INSERT` 语句中使用 `MEMORY_QUOTA()` hint [#18101](https://github.com/pingcap/tidb/pull/18101)
    - 支持基于 TLS 证书 SAN 属性的登录认证 [#17698](https://github.com/pingcap/tidb/pull/17698)
    - `REGEXP()` 函数支持 collation [#17581](https://github.com/pingcap/tidb/pull/17581)
    - 支持会话和全局变量 `sql_select_limit` [#17604](https://github.com/pingcap/tidb/pull/17604)
    - 支持新增分区时自动分裂 Region 的功能 [#17665](https://github.com/pingcap/tidb/pull/17665)
    - 支持函数 `IF()`/`BITXOR()`/`BITNEG()`/`JSON_LENGTH()` 下推到 TiFlash Coprocessor 上执行 [#17651](https://github.com/pingcap/tidb/pull/17651) [#17592](https://github.com/pingcap/tidb/pull/17592)
    - 支持聚合函数 `APPROX_COUNT_DISTINCT()`，用于快速计算 `COUNT(DISTINCT)` 的近似值 [#18120](https://github.com/pingcap/tidb/pull/18120)
    - TiFlash 支持了 collation，支持相应的函数下推 [#17705](https://github.com/pingcap/tidb/pull/17705)
    - `INFORMATION_SCHEMA.INSPECTION_RESULT` 表新增 `STATUS_ADDRESS` 列，用于展示节点的 status 地址 [#17695](https://github.com/pingcap/tidb/pull/17695)
    - `MYSQL.BIND_INFO` 表新增 `SOURCE` 列，用于展示 binding 的创建方式 [#17587](https://github.com/pingcap/tidb/pull/17587)
    - `PERFORMANCE_SCHEMA.EVENTS_STATEMENTS_SUMMARY_BY_DIGEST` 表新增 `PLAN_IN_CACHE` 和 `PLAN_CACHE_HITS` 列，用于展示 plan cache 的使用情况 [#17493](https://github.com/pingcap/tidb/pull/17493)
    - 新增配置项 `enable-collect-execution-info` 和会话级变量 `tidb_enable_collect_execution_info` 用于控制是否记录算子的执行信息并打印到慢查询日志中 [#18073](https://github.com/pingcap/tidb/pull/18073) [#18072](https://github.com/pingcap/tidb/pull/18072)
    - 新增全局变量 `tidb_slow_log_masking`，用于控制是否脱敏慢查询日志中的查询 [#17694](https://github.com/pingcap/tidb/pull/17694)
    - 增加对 TiKV 配置项 `storage.block-cache.capacity` 的诊断规则 [#17671](https://github.com/pingcap/tidb/pull/17671)
    - 新增 SQL 语法 `BACKUP`/`RESTORE` 来进行数据备份恢复 [#15274](https://github.com/pingcap/tidb/pull/15274)

+ TiKV

    - TiKV Control 支持 `encryption-meta` 命令 [#8103](https://github.com/tikv/tikv/pull/8103)
    - 增加 `RocksDB::WriteImpl` 相关的 perf context 监控 [#7991](https://github.com/tikv/tikv/pull/7991)

+ PD

    - 对 leader 执行 `remove-peer` 操作时，让这个 operator 不等待超时，立刻失败 [#2551](https://github.com/pingcap/pd/pull/2551)
    - 对 TiFlash 节点设置更合理的 store limit 配置默认值 [#2559](https://github.com/pingcap/pd/pull/2559)

+ TiFlash

    - Coprocessor 支持新的聚合函数 `APPROX_COUNT_DISTINCT`
    - 存储引擎中的粗糙索引默认开启
    - 支持运行在 ARM 架构
    - Coprocessor 支持 `JSON_LENGTH` 函数下推

+ TiCDC

    - 支持 Capture 节点扩容时迁移部分子任务到新加节点 [#665](https://github.com/pingcap/ticdc/pull/665)
    - Cli 中添加清理 TiCDC GC TTL 的功能 [#652](https://github.com/pingcap/ticdc/pull/652)
    - 在 MQ sink 中支持输出 Canal 协议 [#649](https://github.com/pingcap/ticdc/pull/649)

## 改进提升

+ TiDB

    - 降低当集群中 CM-Sketch 占用过多内存时，Golang 内存分配带来的查询延迟 [#17545](https://github.com/pingcap/tidb/pull/17545)
    - 缩短 TiKV 故障恢复时集群 QPS 的恢复时间 [#17681](https://github.com/pingcap/tidb/pull/17681)
    - 为 partition 表上的查询支持聚合函数下推到 TiKV 或者 TiFlash coprocessor [#17655](https://github.com/pingcap/tidb/pull/17655)
    - 提升索引上等值条件的行数估算准确度 [#17611](https://github.com/pingcap/tidb/pull/17611)

+ TiKV

    - 优化 PD client panic 日志信息 [#8093](https://github.com/tikv/tikv/pull/8093)
    - 重新加回 `process_cpu_seconds_total` 和 `process_start_time_seconds` 监控 [#8029](https://github.com/tikv/tikv/pull/8029)

+ TiFlash

    - 提升从旧版本升级时的兼容性
    - 降低 delta index 的内存使用量
    - 使用更高效的 delta index update 算法

+ Tools

    - Backup & Restore (BR)

        - 提升多表场景下的恢复数据性能 [#266](https://github.com/pingcap/br/pull/266)

## Bug 修复

+ TiDB

    - 修复 `tidb_isolation_read_engines` 更改后从 plan cache 中获取的执行计划不正确的问题 [#17570](https://github.com/pingcap/tidb/pull/17570)
    - 修复某些情况下 `EXPLAIN FOR CONNECTION` 返回运行时错误的问题 [#18124](https://github.com/pingcap/tidb/pull/18124)
    - 修复某些情况下 `last_plan_from_cache` 结果不正确的问题 [#18111](https://github.com/pingcap/tidb/pull/18111)
    - 修复执行 plan cache 中的 `UNIX_TIMESTAMP()` 时的运行时错误 [#18002](https://github.com/pingcap/tidb/pull/18002) [#17673](https://github.com/pingcap/tidb/pull/17673)
    - 修复 `HashJoin` 算子的孩子节点返回 `NULL` 类型的结果时，计算过程中的运行时错误 [#17937](https://github.com/pingcap/tidb/pull/17937)
    - 修复当在同一个数据库中并发执行 `DROP DATABASE` 语句和相关 DDL 语句时的运行错误 [#17659](https://github.com/pingcap/tidb/pull/17659)
    - 修复当 `COERCIBILITY()` 的输入参数是用户变量时结果不正确的问题 [#17890](https://github.com/pingcap/tidb/pull/17890)
    - 修复 `IndexMergeJoin` 算子偶尔卡住的问题 [#18091](https://github.com/pingcap/tidb/pull/18091)
    - 修复 `IndexMergeJoin` 算子触发 oom-action 后被取消执行时卡住的问题 [#17654](https://github.com/pingcap/tidb/pull/17654)
    - 修复 `Insert` 和 `Replace` 算子的内存统计过大的问题 [#18062](https://github.com/pingcap/tidb/pull/18062)
    - 修复在执行 `DROP DATABASE` 的同时对同一个数据库中的表 `DROP TABLE` 时，数据不再向 TiFlash 同步的问题 [#17901](https://github.com/pingcap/tidb/pull/17901)
    - 修复 TiDB 和对象存储服务之间 `BACKUP`/`RESTORE` 失败的问题 [#17844](https://github.com/pingcap/tidb/pull/17844)
    - 修复权限检查失败时的错误信息 [#17724](https://github.com/pingcap/tidb/pull/17724)
    - 修复 `DELETE`/`UPDATE` 语句的 feedback 被错误收集的问题 [#17843](https://github.com/pingcap/tidb/pull/17843)
    - 禁止更改非 `AUTO_RANDOM` 表的 `AUTO_RANDOM_BASE` 值 [#17828](https://github.com/pingcap/tidb/pull/17828)
    - 修复通过 `ALTER TABLE ... RENAME` 在数据库间移动表时，`AUTO_RANDOM` 列分配到错误结果的问题 [#18243](https://github.com/pingcap/tidb/pull/18243)
    - 修复系统变量 `tidb_isolation_read_engines` 的值中没有 `tidb` 时某些系统表无法访问的问题 [#17719](https://github.com/pingcap/tidb/pull/17719)
    - 修复 JSON 中大整数和浮点数比较的精度问题 [#17717](https://github.com/pingcap/tidb/pull/17717)
    - 修复 `COUNT()` 函数的返回类型中 `DECIMAL` 不正确的问题 [#17704](https://github.com/pingcap/tidb/pull/17704)
    - 修复 `HEX()` 函数的输入类型是二进制字符串时结果不正确的问题 [#17620](https://github.com/pingcap/tidb/pull/17620)
    - 修复查询 `INFORMATION_SCHEMA.INSPECTION_SUMMARY` 表没有指定过滤条件时返回结果为空的问题 [#17697](https://github.com/pingcap/tidb/pull/17697)
    - 修复 `ALTER USER` 语句使用哈希后的密码更新用户信息后，密码不符合预期的问题 [#17646](https://github.com/pingcap/tidb/pull/17646)
    - 为 `ENUM` 和 `SET` 类型支持 collation [#17701](https://github.com/pingcap/tidb/pull/17701)
    - 修复 `CREATE TABLE` 时预切分 Region 的超时机制不生效的问题 [#17619](https://github.com/pingcap/tidb/pull/17619)
    - 修复某些情况下 DDL 后台作业重试时，schema 未正确更新导致的 DDL 原子性问题 [#17608](https://github.com/pingcap/tidb/pull/17608)
    - 修复 `FIELD()` 函数的参数包含 column 时结果不正确的问题 [#17562](https://github.com/pingcap/tidb/pull/17562)
    - 修复某些情况下 `max_execution_time` hint 不生效的问题 [#17536](https://github.com/pingcap/tidb/pull/17536)
    - 修复某些情况下 `EXPLAIN ANALYZE` 的结果中并发信息被多次打印的问题 [#17350](https://github.com/pingcap/tidb/pull/17350)
    - 修复对 `STR_TO_DATE` 函数的 `%h` 解析和 MySQL 不兼容问题 [#17498](https://github.com/pingcap/tidb/pull/17498)
    - 修复 `tidb_replica_read` 设置成 `follower`，并且 Region 的 leader 和 follower/learner 之间出现网络分区后，TiDB 发送的 request 一直重试的问题 [#17443](https://github.com/pingcap/tidb/pull/17443)
    - 修复某些情况下 TiDB 一直 ping PD 的 follower 的问题 [#17947](https://github.com/pingcap/tidb/pull/17947)
    - 修复老版本的 range partition 表无法在 4.0 集群中加载的问题 [#17983](https://github.com/pingcap/tidb/pull/17983)
    - 修复当多个 Region 的请求同时超时时整个 SQL 语句超时的问题 [#17585](https://github.com/pingcap/tidb/pull/17585)
    - 修复解析日期类型的分隔符时和 MySQL 不兼容的问题 [#17501](https://github.com/pingcap/tidb/pull/17501)
    - 修复少数情况下发给 TiKV 的请求错发给 TiFlash 的问题 [#18105](https://github.com/pingcap/tidb/pull/18105)
    - 修复当前事务中主键被插入/删除但主键的锁却被另一事务清除可能造成结果不一致的问题 [#18250](https://github.com/pingcap/tidb/pull/18250)

+ TiKV

    - 修复 status server 的内存安全问题 [#8101](https://github.com/tikv/tikv/pull/8101)
    - 修复 json 数字比较的精度丢失问题 [#8087](https://github.com/tikv/tikv/pull/8087)
    - 修改错误的慢查询日志 [#8050](https://github.com/tikv/tikv/pull/8050)
    - 修复 merge 可能导致 peer 无法被移除的问题 [#8048](https://github.com/tikv/tikv/pull/8048)
    - 修复 `tikv-ctl recover-mvcc` 未清除无效的悲观锁 [#8047](https://github.com/tikv/tikv/pull/8047)
    - 修复一些遗漏的 Titan 监控 [#7997](https://github.com/tikv/tikv/pull/7997)
    - 修复向 TiCDC 返回 `duplicated error` 的问题 [#7887](https://github.com/tikv/tikv/pull/7887)

+ PD

    - 验证 `pd-server.dashboard-address` 配置项的正确性 [#2517](https://github.com/pingcap/pd/pull/2517)
    - 修复设置 `store-limit-mode` 为 `auto` 时可能引起 PD panic 的问题 [#2544](https://github.com/pingcap/pd/pull/2544)
    - 修复某些情况下热点不能识别的问题 [#2463](https://github.com/pingcap/pd/pull/2463)
    - 修复某些情况下 Placement Rules 会使 store 状态变更为 tombstone 的进程被阻塞的问题 [#2546](https://github.com/pingcap/pd/pull/2546)
    - 修复某些情况下从低版本升级后，PD 无法正常启动的问题 [#2564](https://github.com/pingcap/pd/pull/2564)

+ TiFlash

    - 修正 proxy 遇到 `region not found` 时可能的 panic 的问题
    - 修正 schema 同步遇到 I/O exception 时可能无法继续同步的问题
