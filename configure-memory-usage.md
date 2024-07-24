---
title: TiDB 内存控制文档
aliases: ['/docs-cn/dev/configure-memory-usage/','/docs-cn/dev/how-to/configure/memory-control/']
summary: TiDB 内存控制文档介绍了如何追踪和控制 SQL 查询过程中的内存使用情况，以及配置内存使用阈值和 tidb-server 实例的内存使用阈值。还介绍了使用 INFORMATION_SCHEMA 系统表查看内存使用情况，以及降低写入事务内存使用的方法。另外还介绍了流量控制和数据落盘的内存控制策略，以及通过设置环境变量 GOMEMLIMIT 缓解 OOM 问题。
---

# TiDB 内存控制文档

目前 TiDB 已经能够做到追踪单条 SQL 查询过程中的内存使用情况，当内存使用超过一定阈值后也能采取一些操作来预防 OOM 或者排查 OOM 原因。你可以使用系统变量 [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-从-v610-版本开始引入) 来控制查询超过内存限制后所采取的操作：

- 如果变量值为 `LOG`，那么当一条 SQL 的内存使用超过一定阈值（由 session 变量 `tidb_mem_quota_query` 控制）后，这条 SQL 会继续执行，但 TiDB 会在 log 文件中打印一条 LOG。
- 如果变量值为 `CANCEL`，那么当一条 SQL 的内存使用超过一定阈值后，TiDB 会立即中断这条 SQL 的执行，并给客户端返回一个错误，错误信息中会详细写明在这条 SQL 执行过程中占用内存的各个物理执行算子的内存使用情况。

## 如何配置一条 SQL 执行过程中的内存使用阈值

使用系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 来配置一条 SQL 执行过程中的内存使用阈值，单位为字节。例如：

配置整条 SQL 的内存使用阈值为 8GB：

{{< copyable "sql" >}}

```sql
SET tidb_mem_quota_query = 8 << 30;
```

配置整条 SQL 的内存使用阈值为 8MB：

{{< copyable "sql" >}}

```sql
SET tidb_mem_quota_query = 8 << 20;
```

配置整条 SQL 的内存使用阈值为 8KB：

{{< copyable "sql" >}}

```sql
SET tidb_mem_quota_query = 8 << 10;
```

## 如何配置 tidb-server 实例使用内存的阈值

自 v6.5.0 版本起，可以通过系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 设置 tidb-server 实例的内存使用阈值。

例如，配置 tidb-server 实例的内存使用总量，将其设置成为 32 GB：

{{< copyable "" >}}

```sql
SET GLOBAL tidb_server_memory_limit = "32GB";
```

设置该变量后，当 tidb-server 实例的内存用量达到 32 GB 时，TiDB 会依次终止正在执行的 SQL 操作中内存用量最大的 SQL 操作，直至 tidb-server 实例内存使用下降到 32 GB 以下。被强制终止的 SQL 操作会向客户端返回报错信息 `Out Of Memory Quota!`。

当前 `tidb_server_memory_limit` 所设的内存限制**不终止**以下 SQL 操作：

- DDL 操作
- 包含窗口函数和公共表表达式的 SQL 操作

> **警告：**
>
> + TiDB 在启动过程中不保证 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 限制生效。如果操作系统的空闲内存不足，TiDB 仍有可能出现 OOM。你需要确保 TiDB 实例有足够的可用内存。
> + 在内存控制过程中，TiDB 的整体内存使用量可能会略微超过 `tidb_server_memory_limit` 的限制。
> + `server-memory-quota` 配置项自 v6.5.0 起被废弃。为了保证兼容性，在升级到 v6.5.0 或更高版本的集群后，`tidb_server_memory_limit` 会继承配置项 `server-memory-quota` 的值。如果集群在升级至 v6.5.0 或更高版本前没有配置 `server-memory-quota`，`tidb_server_memory_limit` 会使用默认值，即 `80%`。

在 tidb-server 实例内存用量到达总内存的一定比例时（比例由系统变量 [`tidb_server_memory_limit_gc_trigger`](/system-variables.md#tidb_server_memory_limit_gc_trigger-从-v640-版本开始引入) 控制）, tidb-server 会尝试主动触发一次 Golang GC 以缓解内存压力。为了避免实例内存在阈值上下范围不断波动导致频繁 GC 进而带来的性能问题，该 GC 方式 1 分钟最多只会触发 1 次。

> **注意：**
>
> 在混合部署的情况下，`tidb_server_memory_limit` 为单个 tidb-server 实例的内存使用阈值，而不是整个物理机的总内存阈值。

## 使用 INFORMATION_SCHEMA 系统表查看当前 tidb-server 的内存用量

要查看当前实例或集群的内存使用情况，你可以查询系统表 [`INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE`](/information-schema/information-schema-memory-usage.md)。

要查看本实例或集群中内存相关的操作和执行依据，可以查询系统表 [`INFORMATION_SCHEMA.(CLUSTER_)MEMORY_USAGE_OPS_HISTORY`](/information-schema/information-schema-memory-usage-ops-history.md)。对于每个实例，该表保留最近 50 条记录。

## tidb-server 内存占用过高时的报警

当 tidb-server 实例的内存使用量超过内存阈值（默认为总内存量的 70%）且满足以下任一条件时，TiDB 将记录相关状态文件，并打印报警日志。

- 第一次内存使用量超过内存阈值。
- 内存使用量超过内存阈值，且距离上一次报警超过 60 秒。
- 内存使用量超过内存阈值，且 `(本次内存使用量 - 上次报警时内存使用量) / 总内存量 > 10%`。

你可以通过系统变量 [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) 修改触发该报警的内存使用比率，从而控制内存报警的阈值。

当触发 tidb-server 内存占用过高的报警时，TiDB 的报警行为如下：

- TiDB 将以下信息记录到 TiDB 日志文件 [`filename`](/tidb-configuration-file.md#filename) 所在目录中。

    - 当前正在执行的所有 SQL 语句中内存使用最高的 10 条语句和运行时间最长的 10 条语句的相关信息
    - goroutine 栈信息
    - 堆内存使用状态

- TiDB 将输出一条包含关键字 `tidb-server has the risk of OOM` 以及以下内存相关系统变量的日志。

    - [`tidb_mem_oom_action`](/system-variables.md#tidb_mem_oom_action-从-v610-版本开始引入)
    - [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)
    - [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入)
    - [`tidb_analyze_version`](/system-variables.md#tidb_analyze_version-从-v510-版本开始引入)
    - [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action)

为避免报警时产生的状态文件累积过多，目前 TiDB 默认只保留最近 5 次报警时所生成的状态文件。你可以通过配置系统变量 [`tidb_memory_usage_alarm_keep_record_num`](/system-variables.md#tidb_memory_usage_alarm_keep_record_num-从-v640-版本开始引入) 调整该次数。

下例通过构造一个占用大量内存的 SQL 语句触发报警，对该报警功能进行演示：

1. 配置报警比例为 `0.85`：

    {{< copyable "" >}}

    ```sql
    SET GLOBAL tidb_memory_usage_alarm_ratio = 0.85;
    ```

2. 创建单表 `CREATE TABLE t(a int);` 并插入 1000 行数据。

3. 执行 `select * from t t1 join t t2 join t t3 order by t1.a`。该 SQL 语句会输出 1000000000 条记录，占用巨大的内存，进而触发报警。

4. 检查 `tidb.log` 文件，其中会记录系统总内存、系统当前内存使用量、tidb-server 实例的内存使用量以及状态文件所在目录。

    ```
    [2022/10/11 16:39:02.281 +08:00] [WARN] [memoryusagealarm.go:212] ["tidb-server has the risk of OOM because of memory usage exceeds alarm ratio. Running SQLs and heap profile will be recorded in record path"] ["is tidb_server_memory_limit set"=false] ["system memory total"=33682427904] ["system memory usage"=22120655360] ["tidb-server memory usage"=21468556992] [memory-usage-alarm-ratio=0.85] ["record path"=/tiup/deploy/tidb-4000/log/oom_record]
    ```

    以上 Log 字段的含义如下：

    * `is tidb_server_memory_limit set`：表示系统变量 [`tidb_server_memory_limit`](/system-variables.md#tidb_server_memory_limit-从-v640-版本开始引入) 是否被设置
    * `system memory total`：表示当前系统的总内存
    * `system memory usage`：表示当前系统的内存使用量
    * `tidb-server memory usage`：表示 tidb-server 实例的内存使用量
    * `memory-usage-alarm-ratio`：表示系统变量 [`tidb_memory_usage_alarm_ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio) 的值
    * `record path`：表示状态文件存放的目录

5. 通过访问状态文件所在目录（该示例中的目录为 `/tiup/deploy/tidb-4000/log/oom_record`），可以看到标记了记录时间的 record 目录（例：`record2022-10-09T17:18:38+08:00`），其中包括 `goroutinue`、`heap`、`running_sql` 3 个文件，文件以记录状态文件的时间为后缀。这 3 个文件分别用来记录报警时的 goroutine 栈信息，堆内存使用状态，及正在运行的 SQL 信息。其中 `running_sql` 文件内容请参考 [`expensive-queries`](/identify-expensive-queries.md)。

## 如何降低 tidb-server 写入事务的内存使用

TiDB 采用的事务模型要求，所有待提交的事务写入操作需先在内存中进行缓存。在写入大的事务时，内存使用可能会增加并成为瓶颈。为了减少或避免大事务使用大量内存，你可以在满足各项限制条件的前提下通过调整 [`tidb_dml_type`](/system-variables.md#tidb_dml_type-从-v800-版本开始引入) 为 `"bulk"` 或使用[非事务 DML 语句](/non-transactional-dml.md)的方式来实现。

## tidb-server 其它内存控制策略

### 流量控制

- TiDB 支持对读数据算子的动态内存控制功能。读数据的算子默认启用 [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency) 所允许的最大线程数来读取数据。当单条 SQL 语句的内存使用每超过 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 一次，读数据的算子就会停止一个线程。
- 流控行为由参数 [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) 控制。
- 当流控被触发时，会在日志中打印一条包含关键字 `memory exceeds quota, destroy one token now` 的日志。

### 数据落盘

TiDB 支持对执行算子的数据落盘功能。当 SQL 的内存使用超过 Memory Quota 时，tidb-server 可以通过落盘执行算子的中间数据，缓解内存压力。支持落盘的算子有：Sort、MergeJoin、HashJoin、HashAgg。

- 落盘行为由参数 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)、[`tidb_enable_tmp_storage_on_oom`](/system-variables.md#tidb_enable_tmp_storage_on_oom)、[`tmp-storage-path`](/tidb-configuration-file.md#tmp-storage-path)、[`tmp-storage-quota`](/tidb-configuration-file.md#tmp-storage-quota) 共同控制。
- 当落盘被触发时，TiDB 会在日志中打印一条包含关键字 `memory exceeds quota, spill to disk now` 或 `memory exceeds quota, set aggregate mode to spill-mode` 的日志。
- Sort、MergeJoin、HashJoin 落盘是从 v4.0.0 版本开始引入的，非并行 HashAgg 的落盘是从 v5.2.0 版本开始引入的，并行 HashAgg 的落盘在 v8.0.0 版本以实验特性引入，在 v8.2.0 版本成为正式功能 (GA)。你可以通过系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) 控制是否启用支持落盘的并行 HashAgg 算法。该变量将在未来版本中废弃。TopN 的落盘在 v8.3.0 版本成为正式工能（GA）。
- 当包含 Sort、MergeJoin、HashJoin、 HashAgg 或 TopN 的 SQL 语句引起内存 OOM 时，TiDB 默认会触发落盘。

> **注意：**
>
> + HashAgg 落盘功能目前不支持 distinct 聚合函数。使用 distinct 函数且内存占用过大时，无法进行落盘。

本示例通过构造一个占用大量内存的 SQL 语句，对 HashAgg 落盘功能进行演示：

1. 将 SQL 语句的 Memory Quota 配置为 1GB（默认 1GB）：

    {{< copyable "sql" >}}

    ```sql
    SET tidb_mem_quota_query = 1 << 30;
    ```

2. 创建单表 `CREATE TABLE t(a int);` 并插入 256 行不同的数据。

3. 尝试执行以下 SQL 语句：

    {{< copyable "sql" >}}

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    该 SQL 语句占用大量内存，返回 Out of Memory Quota 错误。

    ```sql
    ERROR 1105 (HY000): Out Of Memory Quota![conn_id=3]
    ```

4. 执行相同的 SQL 语句，不再返回错误，可以执行成功。从详细的执行计划可以看出，HashAgg 使用了 600MB 的硬盘空间。

    {{< copyable "sql" >}}

    ```sql
    [tidb]> explain analyze select /*+ HASH_AGG() */ count(*) from t t1 join t t2 join t t3 group by t1.a, t2.a, t3.a;
    ```

    ```sql
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    | id                              | estRows     | actRows  | task      | access object | execution info                                                                                                                                                      | operator info                                                   | memory    | disk     |
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    | HashAgg_11                      | 204.80      | 16777216 | root      |               | time:1m37.4s, loops:16385                                                                                                                                           | group by:test.t.a, test.t.a, test.t.a, funcs:count(1)->Column#7 | 1.13 GB   | 600.0 MB |
    | └─HashJoin_12                   | 16777216.00 | 16777216 | root      |               | time:21.5s, loops:16385, build_hash_table:{total:267.2µs, fetch:228.9µs, build:38.2µs}, probe:{concurrency:1, total:35s, max:35s, probe:35s, fetch:962.2µs}         | CARTESIAN inner join                                            | 8.23 KB   | 4 KB     |
    |   ├─TableReader_21(Build)       | 256.00      | 256      | root      |               | time:87.2µs, loops:2, cop_task: {num: 1, max: 150µs, proc_keys: 0, rpc_num: 1, rpc_time: 145.1µs, copr_cache_hit_ratio: 0.00}                                       | data:TableFullScan_20                                           | 885 Bytes | N/A      |
    |   │ └─TableFullScan_20          | 256.00      | 256      | cop[tikv] | table:t3      | tikv_task:{time:23.2µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    |   └─HashJoin_14(Probe)          | 65536.00    | 65536    | root      |               | time:728.1µs, loops:65, build_hash_table:{total:307.5µs, fetch:277.6µs, build:29.9µs}, probe:{concurrency:1, total:34.3s, max:34.3s, probe:34.3s, fetch:278µs}      | CARTESIAN inner join                                            | 8.23 KB   | 4 KB     |
    |     ├─TableReader_19(Build)     | 256.00      | 256      | root      |               | time:126.2µs, loops:2, cop_task: {num: 1, max: 308.4µs, proc_keys: 0, rpc_num: 1, rpc_time: 295.3µs, copr_cache_hit_ratio: 0.00}                                    | data:TableFullScan_18                                           | 885 Bytes | N/A      |
    |     │ └─TableFullScan_18        | 256.00      | 256      | cop[tikv] | table:t2      | tikv_task:{time:79.2µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    |     └─TableReader_17(Probe)     | 256.00      | 256      | root      |               | time:211.1µs, loops:2, cop_task: {num: 1, max: 295.5µs, proc_keys: 0, rpc_num: 1, rpc_time: 279.7µs, copr_cache_hit_ratio: 0.00}                                    | data:TableFullScan_16                                           | 885 Bytes | N/A      |
    |       └─TableFullScan_16        | 256.00      | 256      | cop[tikv] | table:t1      | tikv_task:{time:71.4µs, loops:256}                                                                                                                                  | keep order:false, stats:pseudo                                  | N/A       | N/A      |
    +---------------------------------+-------------+----------+-----------+---------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------+-----------+----------+
    9 rows in set (1 min 37.428 sec)
    ```

## 其它

### 设置环境变量 `GOMEMLIMIT` 缓解 OOM 问题

Golang 自 Go 1.19 版本开始引入 [`GOMEMLIMIT`](https://pkg.go.dev/runtime@go1.19#hdr-Environment_Variables) 环境变量，该变量用来设置触发 Go GC 的内存上限。

对于 v6.1.3 <= TiDB < v6.5.0 的版本，你可以通过手动设置 Go `GOMEMLIMIT` 环境变量的方式来缓解一类 OOM 问题。该类 OOM 问题具有一个典型特征：观察 Grafana 监控，OOM 前的时刻，TiDB-Runtime > Memory Usage 面板中 **estimate-inuse** 立柱部分在整个立柱中仅仅占一半。如下图所示：

![normal OOM case example](/media/configure-memory-usage-oom-example.png)

为了验证 `GOMEMLIMIT` 在该类场景下的效果，以下通过一个对比实验进行说明：

- 在 TiDB v6.1.2 下，模拟负载在持续运行几分钟后，TiDB server 会发生 OOM（系统内存约 48 GiB）：

    ![v6.1.2 workload oom](/media/configure-memory-usage-612-oom.png)

- 在 TiDB v6.1.3 下，设置 `GOMEMLIMIT` 为 40000 MiB，模拟负载长期稳定运行、TiDB server 未发生 OOM 且进程最高内存用量稳定在 40.8 GiB 左右：

    ![v6.1.3 workload no oom with GOMEMLIMIT](/media/configure-memory-usage-613-no-oom.png)
