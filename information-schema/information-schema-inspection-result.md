---
title: INSPECTION_RESULT
summary: 了解 TiDB 系统表 `INSPECTION_RESULT`。
---

# INSPECTION_RESULT

TiDB 内置了一些诊断规则，用于检测系统中的故障以及隐患。

该诊断功能可以帮助用户快速发现问题，减少用户的重复性手动工作。可使用 `select * from information_schema.inspection_result` 语句来触发内部诊断。

诊断结果表 `information_schema.inspection_result` 的表结构如下：

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC inspection_result;
```

```sql
+----------------+--------------+------+------+---------+-------+
| Field          | Type         | Null | Key  | Default | Extra |
+----------------+--------------+------+------+---------+-------+
| RULE           | varchar(64)  | YES  |      | NULL    |       |
| ITEM           | varchar(64)  | YES  |      | NULL    |       |
| TYPE           | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE       | varchar(64)  | YES  |      | NULL    |       |
| STATUS_ADDRESS | varchar(64)  | YES  |      | NULL    |       |
| VALUE          | varchar(64)  | YES  |      | NULL    |       |
| REFERENCE      | varchar(64)  | YES  |      | NULL    |       |
| SEVERITY       | varchar(64)  | YES  |      | NULL    |       |
| DETAILS        | varchar(256) | YES  |      | NULL    |       |
+----------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

字段解释：

* `RULE`：诊断规则名称，目前实现了以下规则：
    * `config`：配置一致性以及合理性检测。如果同一个配置在不同实例不一致，会生成 `warning` 诊断结果。
    * `version`：版本一致性检测。如果同一类型的实例版本不同，会生成 `critical` 诊断结果。
    * `node-load`：服务器负载检测。如果当前系统负载太高，会生成对应的 `warning` 诊断结果。
    * `critical-error`：系统各个模块定义了严重的错误，如果某一个严重错误在对应时间段内超过阈值，会生成 `warning` 诊断结果。
    * `threshold-check`：诊断系统会对一些关键指标进行阈值判断，如果超过阈值会生成对应的诊断信息。
* `ITEM`：每一个规则会对不同的项进行诊断，该字段表示对应规则下面的具体诊断项。
* `TYPE`：诊断的实例类型，可取值为 `tidb`，`pd` 和 `tikv`。
* `INSTANCE`：诊断的具体实例地址。
* `STATUS_ADDRESS`：实例的 HTTP API 服务地址。
* `VALUE`：针对这个诊断项得到的值。
* `REFERENCE`：针对这个诊断项的参考值（阈值）。如果 `VALUE` 超过阈值，就会产生对应的诊断信息。
* `SEVERITY`：严重程度，取值为 `warning` 或 `critical`。
* `DETAILS`：诊断的详细信息，可能包含进一步调查的 SQL 或文档链接。

## 诊断示例

对当前时间的集群进行诊断。

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.inspection_result\G
```

```sql
***************************[ 1. row ]***************************
RULE      | config
ITEM      | log.slow-threshold
TYPE      | tidb
INSTANCE  | 172.16.5.40:4000
VALUE     | 0
REFERENCE | not 0
SEVERITY  | warning
DETAILS   | slow-threshold = 0 will record every query to slow log, it may affect performance
***************************[ 2. row ]***************************
RULE      | version
ITEM      | git_hash
TYPE      | tidb
INSTANCE  |
VALUE     | inconsistent
REFERENCE | consistent
SEVERITY  | critical
DETAILS   | the cluster has 2 different tidb version, execute the sql to see more detail: select * from information_schema.cluster_info where type='tidb'
***************************[ 3. row ]***************************
RULE      | threshold-check
ITEM      | storage-write-duration
TYPE      | tikv
INSTANCE  | 172.16.5.40:23151
VALUE     | 130.417
REFERENCE | < 0.100
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:23151 tikv storage-write-duration was too slow
***************************[ 4. row ]***************************
RULE      | threshold-check
ITEM      | rocksdb-write-duration
TYPE      | tikv
INSTANCE  | 172.16.5.40:20151
VALUE     | 108.105
REFERENCE | < 0.100
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:20151 tikv rocksdb-write-duration was too slow
```

上述诊断结果发现了以下几个问题：

* 第一行表示 TiDB 的 `log.slow-threshold` 配置值为 `0`，可能会影响性能。
* 第二行表示集群中有 2 个不同的 TiDB 版本
* 第三、四行表示 TiKV 的写入延迟太大，期望时间是不超过 0.1s, 但实际值远超预期。

诊断集群在时间段 "2020-03-26 00:03:00", "2020-03-26 00:08:00" 的问题。指定时间范围需要使用 `/*+ time_range() */` 的 SQL Hint，参考下面的查询示例：

{{< copyable "sql" >}}

```sql
select /*+ time_range("2020-03-26 00:03:00", "2020-03-26 00:08:00") */ * from information_schema.inspection_result\G
```

```sql
***************************[ 1. row ]***************************
RULE      | critical-error
ITEM      | server-down
TYPE      | tidb
INSTANCE  | 172.16.5.40:4009
VALUE     |
REFERENCE |
SEVERITY  | critical
DETAILS   | tidb 172.16.5.40:4009 restarted at time '2020/03/26 00:05:45.670'
***************************[ 2. row ]***************************
RULE      | threshold-check
ITEM      | get-token-duration
TYPE      | tidb
INSTANCE  | 172.16.5.40:10089
VALUE     | 0.234
REFERENCE | < 0.001
SEVERITY  | warning
DETAILS   | max duration of 172.16.5.40:10089 tidb get-token-duration is too slow
```

上面的诊断结果发现了以下问题：

* 第一行表示 172.16.5.40:4009 TiDB 实例在 `2020/03/26 00:05:45.670` 发生了重启。
* 第二行表示 172.16.5.40:10089 TiDB 实例的最大的 `get-token-duration` 时间为 0.234s, 期望时间是小于 0.001s。

也可以指定条件，比如只查询 `critical` 严重级别的诊断结果：

{{< copyable "sql" >}}

```sql
select * from information_schema.inspection_result where severity='critical';
```

只查询 `critical-error` 规则的诊断结果:

{{< copyable "sql" >}}

```sql
select * from information_schema.inspection_result where rule='critical-error';
```

## 诊断规则介绍

诊断模块内部包含一系列的规则，这些规则会通过查询已有的监控表和集群信息表，对结果和阈值进行对比。如果结果超过阈值将生成 `warning` 或 `critical` 的结果，并在 `details` 列中提供相应信息。

可以通过查询 `inspection_rules` 系统表查询已有的诊断规则:

{{< copyable "sql" >}}

```sql
select * from information_schema.inspection_rules where type='inspection';
```

```sql
+-----------------+------------+---------+
| NAME            | TYPE       | COMMENT |
+-----------------+------------+---------+
| config          | inspection |         |
| version         | inspection |         |
| node-load       | inspection |         |
| critical-error  | inspection |         |
| threshold-check | inspection |         |
+-----------------+------------+---------+
```

### `config` 诊断规则

`config` 诊断规则通过查询 `CLUSTER_CONFIG` 系统表，执行以下两个诊断规则：

* 检测相同组件的配置值是否一致，并非所有配置项都会有一致性检查，下面是一致性检查的白名单：

    ```go
    // TiDB 配置一致性检查白名单
    port
    status.status-port
    host
    path
    advertise-address
    status.status-port
    log.file.filename
    log.slow-query-file
    tmp-storage-path

    // PD 配置一致性检查白名单
    advertise-client-urls
    advertise-peer-urls
    client-urls
    data-dir
    log-file
    log.file.filename
    metric.job
    name
    peer-urls

    // TiKV 配置一致性检查白名单
    server.addr
    server.advertise-addr
    server.status-addr
    log-file
    raftstore.raftdb-path
    storage.data-dir
    storage.block-cache.capacity
    ```

* 检测以下配置项的值是否符合预期。

    |  组件  | 配置项 | 预期值 |
    |  :----  | :----  |  :----  |
    | TiDB | log.slow-threshold | 大于 0 |
    | TiKV | raftstore.sync-log | true |

### version 诊断规则

`version` 诊断规则通过查询 `CLUSTER_INFO` 系统表，检测相同组件的版本 hash 是否一致。示例如下：

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.inspection_result WHERE rule='version'\G
```

```sql
***************************[ 1. row ]***************************
RULE      | version
ITEM      | git_hash
TYPE      | tidb
INSTANCE  |
VALUE     | inconsistent
REFERENCE | consistent
SEVERITY  | critical
DETAILS   | the cluster has 2 different tidb versions, execute the sql to see more detail: SELECT * FROM information_schema.cluster_info WHERE type='tidb'
```

### `critical-error` 诊断规则

`critical-error` 诊断规则执行以下两个诊断规则：

* 通过查询 [metrics schema](/metrics-schema.md) 数据库中相关的监控系统表，检测集群是否有出现以下比较严重的错误：

    |  组件  | 错误名字 | 相关监控表 | 错误说明 |
    |  ----  | ----  |  ----  |  ----  |
    | TiDB | panic-count | tidb_panic_count_total_count | TiDB 出现 panic 错误 |
    | TiDB | binlog-error | tidb_binlog_error_total_count | TiDB 写 binlog 时出现的错误 |
    | TiKV | critical-error | tikv_critical_error_total_coun | TiKV 的 critical error |
    | TiKV | scheduler-is-busy       | tikv_scheduler_is_busy_total_count | TiKV 的 scheduler 太忙，会导致 TiKV 临时不可用 |
    | TiKV | coprocessor-is-busy | tikv_coprocessor_is_busy_total_count | TiKV 的 coprocessor 太忙 |
    | TiKV | channel-is-full | tikv_channel_full_total_count | TiKV 出现 channel full 的错误 |
    | TiKV | tikv_engine_write_stall | tikv_engine_write_stall | TiKV 出现写入 stall 的错误 |

* 通过查询 `metrics_schema.up` 监控表和 `CLUSTER_LOG` 系统表，检查是否有组件发生重启。

### `threshold-check` 诊断规则

`threshold-check` 诊断规则通过查询 [metrics schema](/metrics-schema.md) 数据库中相关的监控系统表，检测集群中以下指标是否超出阈值：

|  组件  | 监控指标 | 相关监控表 | 预期值 |  说明  |
|  :----  | :----  |  :----  |  :----  |  :----  |
| TiDB | tso-duration              | pd_tso_wait_duration                | 小于 50 ms  |  获取事务 TSO 时间戳的等待耗时 |
| TiDB | get-token-duration        | tidb_get_token_duration             | 小于 1 ms   |  查询获取 token 的耗时，相关的 TiDB 配置参数是 token-limit  |
| TiDB | load-schema-duration      | tidb_load_schema_duration           | 小于 1 s    |  TiDB 更新表元信息的耗时 |
| TiKV | scheduler-cmd-duration    | tikv_scheduler_command_duration     | 小于 0.1 s  |  TiKV 执行 KV cmd 请求的耗时 |
| TiKV | handle-snapshot-duration  | tikv_handle_snapshot_duration       | 小于 30 s   |  TiKV 处理 snapshot 的耗时 |
| TiKV | storage-write-duration    | tikv_storage_async_request_duration | 小于 0.1 s  |  TiKV 写入的延迟 |
| TiKV | storage-snapshot-duration | tikv_storage_async_request_duration | 小于 50 ms  |  TiKV 获取 snapshot 的耗时 |
| TiKV | rocksdb-write-duration    | tikv_engine_write_duration          | 小于 100 ms |  TiKV RocksDB 的写入延迟 |
| TiKV | rocksdb-get-duration | tikv_engine_max_get_duration | 小于 50 ms |  TiKV RocksDB 的读取延迟 |
| TiKV | rocksdb-seek-duration | tikv_engine_max_seek_duration | 小于 50 ms |  TiKV RocksDB 执行 seek 的延迟 |
| TiKV | scheduler-pending-cmd-coun | tikv_scheduler_pending_commands  | 小于 1000 | TiKV 中被阻塞的命令数量  |
| TiKV | index-block-cache-hit | tikv_block_index_cache_hit | 大于 0.95 | TiKV 中 index block 缓存的命中率 |
| TiKV | filter-block-cache-hit | tikv_block_filter_cache_hit | 大于 0.95 | TiKV 中 filter block 缓存的命中率 |
| TiKV | data-block-cache-hit | tikv_block_data_cache_hit | 大于 0.80 | TiKV 中 data block 缓存的命中率 |
| TiKV | leader-score-balance | pd_scheduler_store_status  | 小于 0.05 | 检测各个 TiKV 实例的 leader score 是否均衡，期望实例间的差异小于 5% |
| TiKV | region-score-balance | pd_scheduler_store_status  | 小于 0.05 | 检测各个 TiKV 实例的 Region score 是否均衡，期望实例间的差异小于 5% |
| TiKV | store-available-balance | pd_scheduler_store_status  | 小于 0.2 | 检测各个 TiKV 实例的存储可用空间大小是否均衡，期望实例间的差异小于 20% |
| TiKV | region-count | pd_scheduler_store_status  | 小于 20000 | 检测各个 TiKV 实例的 Region 数量，期望单个实例的 Region 数量小于 20000 |
| PD | region-health | pd_region_health | 小于 100  | 检测集群中处于调度中间状态的 Region 数量，期望总数小于 100 |

另外还会检测 TiKV 实例的以下 thread cpu usage 是否过高:

* scheduler-worker-cpu
* coprocessor-normal-cpu
* coprocessor-high-cpu
* coprocessor-low-cpu
* grpc-cpu
* raftstore-cpu
* apply-cpu
* storage-readpool-normal-cpu
* storage-readpool-high-cpu
* storage-readpool-low-cpu
* split-check-cpu

TiDB 内置的诊断规则还在不断的完善改进中，如果你也想到了一些诊断规则，非常欢迎在 [tidb repository](https://github.com/pingcap/tidb) 下提 PR 或 Issue。
