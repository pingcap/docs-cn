---
title: TiDB OOM 故障排查
summary: 了解如何定位、排查 TiDB Out Of Memory (OOM) 问题。
---

# TiDB OOM 故障排查

本文总结了 TiDB Out Of Memory (OOM) 常见问题的解决思路。在遇到相关错误时，你可以参考本文档来排查错误原因并进行处理。

TiDB OOM ，需要区分以下两种情况。

- OS 层面 oom-killer kill tidb-server。该场景更多是 OS 容量规划问题和 TiUP resource limit 配置问题、或者是否有混布情况，导致 TiDB 作为受害者被 oom-killer killed。
- DB 层面 SQL 失败由于 'Out of Memory Quota'。该场景更多是 DB 内的内存使用控制行为。

针对上述的第一种情况，报错可能如下：

- 操作系统日志:  dmesg -T | grep tidb-server 结果中有问题发生附近时间点的 OOM-killer 的日志。

针对上述的第二种情况，报错可能如下：

- tidb.log show
    - Alerm:  [WARN] [memory_usage_alarm.go:139] ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"]
    - 重启相关日志：[INFO] [printer.go:33] ["Welcome to TiDB."]

- SQL 返回：ERROR 1105 (HY000): Out Of Memory Quota![conn_id=54] 。注意：此报错为配置了 tidb_mem_quota_query 后的正常行为。

针对两种情况，一些共同的症状：

- 客户端报错：SQL error, errno = 2013, state = 'HY000': Lost connection to MySQL server during query
- Grafana 上的监控，看是否有因内存超阈发生过重启：
    - TiDB --> Server --> Memory Usage 达到某一阈值的锯齿形
    - TiDB --> Server --> Events OPM 显示 ‘server kill’
    - TiDB --> Server --> Uptime 显示掉零重启
    - TiDB-Runtime --> Memory Usage , 看到 estimate-inuse 在持续升高
    - TiDB --> Server --> Memory Usage, process/heapInuse 在持续升高

## 排查方向

1. 首先需要确认 OOM 的出发点，是上述情况一 还是情况二。
2. OS 层面，检查资源配置、混布的影响。
3. DB 层面，常见情况包括:
    - TiDB 处理较大的数据流量，如大查询，大写入，数据导入等
    - TiDB 的高并发场景，多条 SQL 并发消耗资源或者算子并发高
    - TiDB 内存泄露，资源不释放

## 需要收集的诊断信息

1. 操作系统上的内存相关配置
    - TiUP 上的配置：resource_control.memory_limit
    - 操作系统的配置：
      - cat /proc/meminfo
      - Sys config:
        - vm.overcommit_memory
        - sysctl -a| grep oom
    - 是否 NUMA and number of nodes:  numactl --hardware ; numactl --show

2. DB 层的内存相关配置
    - tidb version
    - tidb_mem_quota_query, memory-usage-alarm-ratio, mem-quota-query
    - oom-action
    - tidb_enable_rate_limit_action
    - Server-memory-quota
    - Oom-use-tmp-storage, tmp-storage-path, tmp-storage-quota
    - tidb_analyze_version

3. TiDB 内存的日常使用情况，checked by TiDB --> Server --> Memory Usage

4. SQL with Top memory consumption：

    - SQL dashboard 中 SQL 语句分析/慢查询，查看内存用量
    - information_schema 的 SLOW_QUERY/CLUSTER_SLOW_QUERY
    - 各个 TiDB 节点的 tidb_slow_query.log
    - 设置了 memory-quota-query 的，在 tidb.log 中 grep "expensive_query"  看 mem_max 字段，特别是当 SQL 是 unsuccessful 的，只能通过 log 里的 expensive query 来排查。
    - SQL 的 explain analyze or explain 看算子层的内存消耗
    - SELECT * FROM information_schema.processlist; See column MEM

5. 内存使用率高的时候 TiDB 的 Profile 信息： curl -G http://{TiDBIP}:10080/debug/zip?seconds=10" > profile.zip

6. tmp 目录下的 dump 文件，该文件的路径会在 tidb.log 中打印出来。例如：
    ["tidb-server has the risk of OOM. Running SQLs and heap profile will be recorded in record path"] ["is server-memory-quota set"=false] ["system memory total"=14388137984] ["system memory usage"=11897434112] ["tidb-server memory usage"=11223572312] [memory-usage-alarm-ratio=0.8] ["record path"="/tmp/0_tidb/MC4wLjAuMDo0MDAwLzAuMC4wLjA6MTAwODA=/tmp-storage/record"]

## 常见原因和解决办法

### 系统配置不合理

检查操作系统的内存配置使用是否合理、OOM killer 配置是否符合预期。
    - 注意：为使 dmesg 能抓到 OOM killer 信息, 需确保 sysconfig vm.overcommit_memory=1。
DB 参数配置
    - 详见 TiDB 内存控制文档，了解如何限制一条 SQL 或者 一个 TiDB instance 的内存使用总量，以及 memory-usage-alarm-ratio、流量控制、数据落盘等机制。
    - 注意在设置了流量控制 tidb_enable_rate_limit_action 后，它会改变了 oom-cancel 的表现时间。因为它会首先尝试在内存阈值范围内，逐一停下线程。在只剩一个线程的时候才触发 cancel。

业务的形态：了解负载形态，平时 session 的并发度，单个 session 所使用的内存的预期，以准备好对应的容量配置。

### Go 内存释放时间

目前 TiDB TiUP 在 run_tidb.sh 中已经包含了 GODEBUG=madvdontneed=1 环境变量，表示 GC 时立即将内存返还给操作系统。请检查您的 TiUP 版本是否过旧；新版本的 TiUP 包含这个配置。

### 统计信息的收集和加载过程需要使用内存

TiDB 节点启动后需要加载统计信息到内存中。TiDB 从 v6.1.0 开始引入了 tidb_stats_cache_mem_quota 对统计信息内存使用进行了改善。

统计信息的收集过程会消耗内存。

- 可以使用指定采样率、指定只收集特定列的统计信息、减少 analyze 并发度的方式减少内存使用。
- TiDB 从 v6.1.0 开始引入了统计信息收集的内存限制，可以使用 tidb_mem_quota_analyze 变量来控制 TiDB 更新统计信息时的最大总内存占用。

更多信息详见于  Doc: 统计信息简介

### 大查询 SQL，在 TiDB 节点上消耗太多内存

一些场景如：

- SQL 的执行计划不优，比如由于缺少合适的索引、统计信息过期、优化器的 bug 等原因，导致了 SQL 的执行计划选错，或者出现了巨大的中间结果集累积在内存中。需要考虑添加合适的索引、使用执行算子的数据落盘功能 、以及检查表之间的关联方式以让筛选性好的表优先 join、加 hint 方式以做调优。
- 一些算子和函数不支持下推到存储层，所以需要先拉取数据到 TiDB 层。
- SQL 上存在扫描、聚合内容过大的情况 ,并且执行计划中可见算子 HashAgg。HashAgg是多线程并发执行，执行速度较快，但会消耗较多内存。 可以尝试使用 hint stream_agg 替代。
- 调整控制一次读取的 Region 数量，减少因并发高导致的内存问题。对应系统变量：tidb_distsql_scan_concurrency /tidb_index_serial_scan_concurrency/tidb_executor_concurrency。

### 大事务或大写入，在 TiDB 节点上消耗太多内存

需要提前进行内存的容量规划，这是因为：执行事务时 TiDB 进程的内存消耗相对于事务大小会存在一定程度的放大，最大可能达到提交事务大小的 2 到 3 倍以上。

针对单条大事务，也可通过拆分的方式调小事务尺寸。

### Prepare statment 使用过量

例如：客户端不断 prepare stmt 但未 deallocate prepare stmt 导致的内存持续上涨,最终导致 TiDB oom。

原因是：prepare statment 占用的内存要在 session 关闭后才会释放。这一点在长连接下尤需注意。

解决办法：可以调整 session 的 生命周期、连接池的 lift time 时长或者 SQL 重置策略，也可使用系统变量 max_prepared_stmt_count 进行限制。

### 客户端 OOM 问题

观察 grafana TiDB Details --> Server --> Client Data Traffic, 趋势和速度，看是否存在网路阻塞。

客户端错误 JDBC 配置参数导致的应用 OOM，流式读取的一个相关参数(defaultFetchSize)配置有误，造成数据在客户端大量缓存