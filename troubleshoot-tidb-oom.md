---
title: TiDB OOM 故障排查
summary: 了解如何定位、排查 TiDB Out Of Memory (OOM) 问题。
---

# TiDB OOM 故障排查

本文总结了 TiDB Out Of Memory (OOM) 常见问题的解决思路。在遇到 OOM 问题时，你可以参考本文档来排查错误原因并进行处理。

## 整体排查思路

在排查 OOM 问题时，整体遵循以下排查思路：

1. 首先需要确认是否属于 OOM 问题。执行下面命令查看操作系统日志，如果结果中存在问题发生附近时间点的 OOM-killer 的日志，则可以确定是 OOM 问题。

    ```shell
    dmesg -T | grep tidb-server
    ```

2. 确认是 OOM 问题之后，可以进一步排查触发原因是由部署问题导致还是由数据库问题导致。

    - 如果是部署问题触发 OOM，需要排查资源配置、混合部署的影响。

    - 如果是数据库问题触发 OOM，常见原因有:
        - TiDB 处理较大的数据流量，如大查询、大写入、数据导入等
        - TiDB 的高并发场景，多条 SQL 并发消耗资源，或者算子并发高
        - TiDB 内存泄露，资源没有释放

## 常见故障现象

OOM 常见的故障现象包括（但不限于）：

- 客户端报错：`SQL error, errno = 2013, state = 'HY000': Lost connection to MySQL server during query`

- 查看 Grafana 监控，发现以下现象：
    - **TiDB** > **Server** > **Memory Usage** 达到某一阈值的锯齿形
    - **TiDB** > **Server** > **Uptime** 显示为掉零
    - **TiDB-Runtime** > **Memory Usage** 观察到 estimate-inuse 在持续升高
    - **TiDB** > **Server** > **Memory Usage** 观察到 process/heapInuse 在持续升高

- 查看 tidb.log，可发现如下日志条目：
    - OOM 相关的 Alerm: [WARN] [memory_usage_alarm.go:139] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"]。关于该日志的详细说明，请参考 [`memory-usage-alarm-ratio`](/system-variables.md#tidb_memory_usage_alarm_ratio)。
    - 重启相关的日志条目：[INFO] [printer.go:33] ["Welcome to TiDB."]

## 常见故障原因和解决方法

TiDB 出现 OOM 问题，一般从以下几个方面进行排查：

- 部署问题

- 数据库问题

- 客户端问题

以下章节分别进行介绍。

### 部署问题

如果是由于部署不当导致的 OOM 问题，常见的原因有：

- 操作系统内存容量规划偏小，导致内存不足

- TiUP [`resource_control`](/tiup/tiup-cluster-topology-reference.md#global) 配置不合理

- 有混合部署的情况（指 TiDB 和其他应用程序部署在同一台服务器上），导致 TiDB 作为受害者被 oom-killer killed

### 数据库问题

本节介绍由于数据库问题导致的 OOM 问题和解决办法。

> **说明：**
>
> 如果 SQL 返回 `ERROR 1105 (HY000): Out Of Memory Quota![conn_id=54]`，是由于配置了 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)，数据库的内存使用控制行为会出发该报错。此报错为正常行为，不是故障，可以忽略。

#### 执行 SQL 语句时在 TiDB 节点上消耗太多内存

可以根据以下不同的触发 OOM 的原因，采取相应的措施减少 SQL 的内存使用：

- 如果 OOM 是由于 SQL 的执行计划不优，比如由于缺少合适的索引、统计信息过期、优化器的 bug 等原因，导致选错了 SQL 的执行计划，进而出现巨大的中间结果集累积在内存中。这种情况下可以考虑采取以下措施：
    - 添加合适的索引
    - 使用算子的落盘功能
    - 调整表之间的 JOIN 顺序
    - 使用 hint 进行调优

- 一些算子和函数不支持下推到存储层，导致出现巨大的中间结果集累积。此时可能需要改写业务 SQL，或使用 hint 进行调优，来使用可下推的函数或算子。

- 执行计划中存在算子 HashAgg。HashAgg 是多线程并发执行，虽然执行速度较快，但会消耗较多内存。可以尝试使用 hint `stream_agg` 替代。

- 调小同时读取的 Region 的数量，或降低算子并发度，以避免因高并发导致的内存问题。对应的系统变量包括：
    - [`tidb_distsql_scan_concurrency`](/system-variables.md#tidb_distsql_scan_concurrency)、
    - [`tidb_index_serial_scan_concurrency`](/system-variables.md#tidb_index_serial_scan_concurrency)
    - [`tidb_executor_concurrency`](/system-variables.md#tidb_executor_concurrency-从-v50-版本开始引入)

- 问题发生时间附近，session 的并发度过高。此时可能需要添加节点进行扩容。

#### 大事务或大写入在 TiDB 节点上消耗太多内存

需要提前进行内存的容量规划，这是因为执行事务时 TiDB 进程的内存消耗相对于事务大小会存在一定程度的放大，最大可能达到提交事务大小的 2 倍到 3 倍以上。

针对单个大事务，也可通过拆分的方式调小事务大小。

#### 收集和加载统计信息的过程中消耗太多内存

TiDB 节点启动后需要加载统计信息到内存中。TiDB 从 v6.1.0 开始引入了 [`enable_tidb_stats_cache_mem_quota`](/tidb-configuration-file.md#enable-stats-cache-mem-quota-从-v610-版本开始引入) 对统计信息内存使用进行了改善。

统计信息的收集过程会消耗内存。可以通过以下方式控制内存使用量：

- 使用指定采样率、指定只收集特定列的统计信息、减少 analyze 并发度等手段减少内存使用。

- TiDB 从 v6.1.0 开始引入了统计信息收集的内存限制，可以使用系统变量 [`tidb_mem_quota_analyze`](/system-variables.md#tidb_mem_quota_analyze-从-v610-版本开始引入) 来控制 TiDB 更新统计信息时的最大总内存占用。

更多信息请参见[统计信息简介](/statistics.md)。

#### Prepared Statement 使用过量

客户端不断创建 Prepared Statement 但未执行 [`deallocate prepare stmt`](/sql-prepared-plan-cache.md#忽略-com_stmt_close-指令和-deallocate-prepare-语句) 导致的内存持续上涨，最终导致 TiDB OOM。

原因是由于 Prepared Statement 占用的内存要在 session 关闭后才会释放。这一点在长连接下尤需注意。

要解决该问题，可以考虑采取以下措施：

- 调整 session 的生命周期

- 调整连接池的 life time 时长

- 使用系统变量 [max_prepared_stmt_count](/system-variables.md#max_prepared_stmt_count) 进行限制

#### 系统变量配置不当

系统变量 [`tidb_enable_rate_limit_action`](/system-variables.md#tidb_enable_rate_limit_action) 在单条查询仅涉及读数据的情况下，对内存控制效果较好。

如果还存在额外的计算操作（如连接、聚合等），启动该变量可能会导致内存不受 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 控制，加剧 OOM 风险。

建议关闭该变量。从 TiDB v6.3.0 开始，该变量默认关闭。

### 客户端 OOM 问题

若客户端发生 OOM，则需要排查以下方面：

- 观察 **Grafana TiDB Details** > **Server** > **Client Data Traffic** 的趋势和速度，查看是否存在网路阻塞。

- 检查是否存在错误的 JDBC 配置参数导致的应用 OOM，例如流式读取的相关参数 `defaultFetchSize` 配置有误，会造成数据在客户端大量缓存。

## 处理 OOM 问题需要收集的诊断信息

为定位 OOM 故障，通常需要收集以下信息：

- 操作系统的内存相关配置
    - TiUP 上的配置：`resource_control.memory_limit`
    - 操作系统的配置：
        - 内存信息：`cat /proc/meminfo`
        - 相关内核参数：`vm.overcommit_memory`
    - NUMA 相关信息:
        - `numactl --hardware`
        - `numactl --show`

- 数据库的内存相关配置
    - tidb version
    - `tidb_mem_quota_query`、`memory-usage-alarm-ratio`、`mem-quota-query`
    - `oom-action`
    - `tidb_enable_rate_limit_action`
    - `server-memory-quota`
    - `oom-use-tmp-storage`、`tmp-storage-path`、`tmp-storage-quota`
    - `tidb_analyze_version`

- 在 Grafana 查看 TiDB 内存的日常使用情况: **TiDB** > **Server** > **Memory Usage**

- 查看内存消耗较多的 SQL 语句：

    - 可以从 SQL Dashboard 中查看 SQL 语句分析、慢查询，查看内存使用量
    - `information_schema` 的 `SLOW_QUERY`、`CLUSTER_SLOW_QUERY`
    - 各个 TiDB 节点的 tidb_slow_query.log
    - 在 tidb.log 中 grep "expensive_query" 查看对应的日志条目
    - 执行 `EXPLAIN ANALYZE` 查看算子的内存消耗
    - 执行 `SELECT * FROM information_schema.processlist;` 查看 SQL 对应的 `MEM` 列的值

- 执行以下命令，收集内存使用率高的时候 TiDB 的 Profile 信息：

    ```shell
    curl -G http://{TiDBIP}:10080/debug/zip?seconds=10" > profile.zip
    ```

- 在 tidb.log 中，grep 关键字 "tidb-server has the risk of OOM"，可以看到 TiDB Server 收集的告警文件路径，例如：

    ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is server-memory-quota set"=false] ["system memory total"=14388137984] ["system memory usage"=11897434112] ["tidb-server memory usage"=11223572312] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/0_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]

## 参考文档

- [TiDB 内存调优](/configure-memory-usage.md)

- [TiKV 内存调优](/tune-tikv-memory-performance.md)
