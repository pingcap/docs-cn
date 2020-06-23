---
title: TiDB 4.0.2 Release Notes
category: Releases
---

# TiDB 4.0.2 Release Notes

发版日期：2020 年 6 月 30 日

TiDB 版本：4.0.2

## 兼容性

+ TiDB
    - 移除慢查询日志和 stateemnt summary 表中的敏感信息。[#18130](https://github.com/pingcap/tidb/pull/18130)
    - 禁止在 sequence 缓存中出现负数。[#18103](https://github.com/pingcap/tidb/pull/18103)
    - `CLUSTER_INFO` 表中不再显示 tombstone 状态的 TiKV 和 TiFlash 结点。[#17953](https://github.com/pingcap/tidb/pull/17953)
    - 诊断规则 `current-load` 变更为 `node-check`。[#17660](https://github.com/pingcap/tidb/pull/17660)

+ TiFlash
    - 提升从旧版本升级时的兼容性. [#786](https://github.com/pingcap/tics/pull/786)

## 新功能

+ TiDB
    - 支持在 `INSERT` 语句中使用 `MEMORY_QUOTA()` hint。[#18101](https://github.com/pingcap/tidb/pull/18101)
    - 支持基于 TLS 证书 SAN 属性的登录认证。[#17698](https://github.com/pingcap/tidb/pull/17698)
    - `REGEXP()` 函数支持 collation。[#17581](https://github.com/pingcap/tidb/pull/17581)
    - 支持会话和全局变量 `sql_select_limit`。[#17604](https://github.com/pingcap/tidb/pull/17604)
    - 支持新增分区时自动分裂 region 的功能。[#17665](https://github.com/pingcap/tidb/pull/17665)
    - 支持函数 `IF()`/`BITXOR()`/`BITNEG()`/`JSON_LENGTH()` 下推到 TiFlash Coprocessor 上执行。[#17651](https://github.com/pingcap/tidb/pull/17651), [#17592](https://github.com/pingcap/tidb/pull/17592)
    - 支持聚合函数 `APPROX_COUNT_DISTINCT()`，用于快速计算 `COUNT(DISTINCT)` 的近似值。[#18120](https://github.com/pingcap/tidb/pull/18120)
    - TiFlash 支持了 collation，支持相应的函数下推。[#17705](https://github.com/pingcap/tidb/pull/17705)
    - `INFORMATION_SCHEMA.INSPECTION_RESULT` 表新增 `STATUS_ADDRESS` 列，用于展示结点的 status 地址。[#17695](https://github.com/pingcap/tidb/pull/17695)
    - `MYSQL.BIND_INFO` 表新增 `SOURCE` 列，用于展示 binding 的创建方式。[#17587](https://github.com/pingcap/tidb/pull/17587)
    - `PERFORMANCE_SCHEMA.EVENTS_STATEMENTS_SUMMARY_BY_DIGEST` 表新增 `PLAN_IN_CACHE` 和 `PLAN_CACHE_HITS` 列，用于展示 plan cache 的使用情况。[#17493](https://github.com/pingcap/tidb/pull/17493)
    - 新增配置项 `enable-collect-execution-info` 和会话级变量 `tidb_enable_collect_execution_info` 用于控制是否在记录 SQL 的运行时信息并打印到慢查询日志中。[#18073](https://github.com/pingcap/tidb/pull/18073), [#18072](https://github.com/pingcap/tidb/pull/18072)
    - 新增全局变量 `tidb_slow_log_masking`，用于控制是否脱敏慢查询日志中的用户数据。[#17694](https://github.com/pingcap/tidb/pull/17694)
    - 增加对 TiKV 配置项 `storage.block-cache.capacity` 的诊断规则。[#17671](https://github.com/pingcap/tidb/pull/17671)

+ TiKV



+ PD



+ TiFlash
    - Coprocessor 支持新的聚合函数 `APPROX_COUNT_DISTINCT`. [#798](https://github.com/pingcap/tics/pull/798)
    - 存储引擎中的粗糙索引默认开启. [#777](https://github.com/pingcap/tics/pull/777)
    - 支持运行在 ARM 架构. [#769](https://github.com/pingcap/tics/pull/769)
    - 降低 delta index 的内存使用量. [#787](https://github.com/pingcap/tics/pull/787)
    - 使用更高效的 delta index update 算法. [#794](https://github.com/pingcap/tics/pull/794)
    - Coprocessor 支持 `JSON_LENGTH` 函数下推. [#742](https://github.com/pingcap/tics/pull/742)


+ Tools


## Improvements

+ TiDB
    - 降低当集群中 CM-Skech 占用过多内存时，golang 内存分配带来的查询延迟。[#17545](https://github.com/pingcap/tidb/pull/17545)
    - 缩短 TiKV 故障恢复时集群 QPS 的恢复时间。[#17681](https://github.com/pingcap/tidb/pull/17681)
    - 为 partition 表上的查询支持聚合函数下推到 TiKV 或者 TiFlash coprocessor。[#17655](https://github.com/pingcap/tidb/pull/17655)
    - 提升索引上等值条件的行数估算准确度。[#17611](https://github.com/pingcap/tidb/pull/17611)

## Bug 修复

+ TiDB
    - Fix the incorrect execution plan in plan cache after `tidb_isolation_read_engines` is changed. [#17570](https://github.com/pingcap/tidb/pull/17570)
    - Fix the occasionally runtime error in executing the `EXPLAIN FOR CONNECTION` statement. [#18124](https://github.com/pingcap/tidb/pull/18124)
    - Fix the incorrect result of session variable `last_plan_from_cache`. [#18111](https://github.com/pingcap/tidb/pull/18111)
    - Fix the runtime error in executing `UNIX_TIMESTAMP()` function from plan cache. [#18002](https://github.com/pingcap/tidb/pull/18002), [#17673](https://github.com/pingcap/tidb/pull/17673)
    - Fix the runtime error when the child of `HashJoin` executor returns `NULL` column. [#17937](https://github.com/pingcap/tidb/pull/17937)
    - Fix the runtime error caused by parallelly executing "DROP DATABASE" and other DDL on the same database. [#17659](https://github.com/pingcap/tidb/pull/17659)
    - Fix the incorrect result of function `COERCIBILITY()` on user variable. [#17890](https://github.com/pingcap/tidb/pull/17890)
    - Fix occasionally hang in the `IndexMergeJoin` executor. [#18091](https://github.com/pingcap/tidb/pull/18091)
    - Fix hang in the `IndexMergeJoin` executor when out of memory quota and query cancelling is triggered. [#17654](https://github.com/pingcap/tidb/pull/17654)
    - Fix over counting memory usage of the `Insert` and `Replace` executor. [#18062](https://github.com/pingcap/tidb/pull/18062)
    - Fix stoping replicating data to TiFlash storage when `DROP DATABASE` and `DROP TABLE` of the same database running concurrently. [#17901](https://github.com/pingcap/tidb/pull/17901)
    - Fix the `BACKUP`/`RESTORE` failure between TiDB and object storage. [#17844](https://github.com/pingcap/tidb/pull/17844)
    - Fix the incorrect error message of privelege check failure when access denied. [#17724](https://github.com/pingcap/tidb/pull/17724)
    - Discard the query feedbacks generated from the `DELETE`/`UPDATE` statements. [#17843](https://github.com/pingcap/tidb/pull/17843)
    - Forbid altering `AUTO_RANDOM_BASE` for a table without `AUTO_RANDOM` property. [#17828](https://github.com/pingcap/tidb/pull/17828)
    - Fix the issue that some system tables can not be access when setting `tidb_isolation_read_engines` without `tidb`. [#17719](https://github.com/pingcap/tidb/pull/17719)
    - Fix the incorrect result of JSON comparison on large integer and float values. [#17717](https://github.com/pingcap/tidb/pull/17717)
    - Fix the incorrect decimal property for the result of `COUNT()` function. [#17704](https://github.com/pingcap/tidb/pull/17704)
    - Fix the incorrect result of `HEX()` function when the type of input parameter is binary string. [#17620](https://github.com/pingcap/tidb/pull/17620)
    - Fix returning empty result when querying `INFORMATION_SCHEMA.INSPECTION_SUMMARY` table without filter condition. [#17697](https://github.com/pingcap/tidb/pull/17697)
    - Fix `ALTER USER` with hash string result in rehashed password issue. [#17646](https://github.com/pingcap/tidb/pull/17646)
    - Support collation for `ENUM` and `SET` values. [#17701](https://github.com/pingcap/tidb/pull/17701)
    - Fix the pre-split region timeout constraint not work issue on `CREATE TABLE`. [#17619](https://github.com/pingcap/tidb/pull/17619)
    - Fix an issue that may break the atomicity of DDL job: when a DDL job is retried, the schema is unexpectedly updated. [#17608](https://github.com/pingcap/tidb/pull/17608)
    - Fix the incorrect result for `FIELD()` function when the argument contains column. [#17562](https://github.com/pingcap/tidb/pull/17562)
    - Fix the occasionally not work issue on `max_execution_time` hint. [#17536](https://github.com/pingcap/tidb/pull/17536)
    - Fix the redundant concurrency information in the result of `EXPLAIN ANALYZE`. [#17350](https://github.com/pingcap/tidb/pull/17350)
    - Fix the incompatible behavior of `%h` on function `STR_TO_DATE`. [#17498](https://github.com/pingcap/tidb/pull/17498)
    - Fix the infinite follower/learner retry issue when `tidb_replica_read` is set to `follower` and there is a network partition between the leader and follower/learner. [#17443](https://github.com/pingcap/tidb/pull/17443)
    - Fix the issue that TiDB sends too much pings to PD follower occasionally. [#17947](https://github.com/pingcap/tidb/pull/17947)
    - Fix the issue that old versioned range partition table can not be loaded to TiDB 4.0.0. [#17983](https://github.com/pingcap/tidb/pull/17983)
    - Fix the SQL command timeout issue when multiple region requests failed at the same time by assigning different `Backoffer` for each region. [#17585](https://github.com/pingcap/tidb/pull/17585)
    - Fix the incompatible behavior on parsing datetime delimiters. [#17501](https://github.com/pingcap/tidb/pull/17501)
    - Fix the issue that TiKV request occasionally send to TiFlash server. [#18105](https://github.com/pingcap/tidb/pull/18105)

+ TiKV



+ PD



+ TiFlash
    - 修正 proxy 遇到 region not found 时可能的 panic 的问题. [#807](https://github.com/pingcap/tics/pull/807)
    - 修正 schema 同步遇到 I/O exception 时可能无法继续同步的问题. [#791](https://github.com/pingcap/tics/pull/791)


+ Tools
