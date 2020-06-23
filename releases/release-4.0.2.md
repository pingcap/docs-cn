---
title: TiDB 4.0.2 Release Notes
category: Releases
---

# TiDB 4.0.2 Release Notes

发版日期：2020 年 6 月 30 日

TiDB 版本：4.0.2

## 兼容性

+ TiDB
    - Remove sensitive information in slow query log and statement summary table. [#18130](https://github.com/pingcap/tidb/pull/18130)
    - Forbid negative value in the sequence cache. [#18103](https://github.com/pingcap/tidb/pull/18103)
    - Remove tombstone TiKV and TiFlash servers from the `CLUSTER_INFO` table. [#17953](https://github.com/pingcap/tidb/pull/17953)
    - Change diagnos rule `current-load` to `node-check`. [#17660](https://github.com/pingcap/tidb/pull/17660)

+ TiFlash
    - 提升从旧版本升级时的兼容性. [#786](https://github.com/pingcap/tics/pull/786)

## 新功能

+ TiDB
    - Support the `MEMORY_QUOTA()` hint in `INSERT` statements. [#18101](https://github.com/pingcap/tidb/pull/18101)
    - Support authentication based on TLS certificate SAN field [#17698](https://github.com/pingcap/tidb/pull/17698)
    - Support collation for the `REGEXP()` function. [#17581](https://github.com/pingcap/tidb/pull/17581)
    - Support the `sql_select_limit` session and global vairable. [#17604](https://github.com/pingcap/tidb/pull/17604)
    - Support spliting the region for the newly added partition by default. [#17665](https://github.com/pingcap/tidb/pull/17665)
    - Support pushing the `IF()`/`BITXOR()`/`BITNEG()`/`JSON_LENGTH()` functions to the TiFlash Coprocessor. [#17651](https://github.com/pingcap/tidb/pull/17651), [#17592](https://github.com/pingcap/tidb/pull/17592)
    - Support a new aggregate function `APPROX_COUNT_DISTINCT()` to calculate the approximate result of `COUNT(DISTINCT)`. [#18120](https://github.com/pingcap/tidb/pull/18120)
    - Support collation in TiFlash, enable push collation related functions to tiflash. [#17705](https://github.com/pingcap/tidb/pull/17705)
    - Add the `STATUS_ADDRESS` column in the `INFORMATION_SCHEMA.INSPECTION_RESULT` table to indicate the status address of servers. [#17695](https://github.com/pingcap/tidb/pull/17695)
    - Add the `SOURCE` column in the `MYSQL.BIND_INFO` table to indicate the how the bindings are created. [#17587](https://github.com/pingcap/tidb/pull/17587)
    - Add the `PLAN_IN_CACHE` and `PLAN_CACHE_HITS` columns in `PERFORMANCE_SCHEMA.EVENTS_STATEMENTS_SUMMARY_BY_DIGEST` table to indicate the plan cache usage of sql statements. [#17493](https://github.com/pingcap/tidb/pull/17493)
    - Add the config `enable-collect-execution-info` and session variable `tidb_enable_collect_execution_info` to control whether to collect execution information of each operator and record it in the slow query log. [#18073](https://github.com/pingcap/tidb/pull/18073), [#18072](https://github.com/pingcap/tidb/pull/18072)
    - Add the global variable `tidb_slow_log_masking` to control whether to desensitize the query in slow query log. [#17694](https://github.com/pingcap/tidb/pull/17694)
    - Add config check for `storage.block-cache.capacity` of TiKV config in `INFORMATION_SCHEMA.INSPECTION_RESULT`. [#17671](https://github.com/pingcap/tidb/pull/17671)

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
    - Reduce the query latency caused by golang memory allocation when there are lots of memory consumed by CM-Sketch. [#17545](https://github.com/pingcap/tidb/pull/17545)
    - Reduce the QPS recover duration when a TiKV server is in the failure recovere progress. [#17681](https://github.com/pingcap/tidb/pull/17681)
    - Support pushing aggregate functions to TiKV/TiFlash coprocessor on partition table. [#17655](https://github.com/pingcap/tidb/pull/17655)
    - Improve row count estimation for index equal condition. [#17611](https://github.com/pingcap/tidb/pull/17611)

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
