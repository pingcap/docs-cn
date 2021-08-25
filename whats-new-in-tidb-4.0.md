---
title: What's New in TiDB 4.0
summary: 了解 TiDB 4.0 版本的新特性。
---

# What's New in TiDB 4.0

随着 TiDB v4.0 于 2020 年 5 月 28 日正式发布，TiDB v4.0 在稳定性、易用性、性能、安全和功能方面进行了大量的改进。本文概括性地介绍改进的内容，用户可根据实际情况决定升级到 TiDB v4.0。本文仅总结 v4.0 中面向用户且最重要的改进事项，功能及错误修复的完整列表，请参阅 [Release Notes](/releases/release-notes.md#40)。

## 调度功能

+ 热点调度支持更多维度。热点调度在决策时，除了根据写入/读取流量作为调度依据外，新引入 key 的维度。可以很大程度改善原有单一维度决策造成的 CPU 资源利用率不均衡的问题。详情参阅：[调度](/tidb-scheduling.md)。

## 存储引擎

+ TiFlash 是 TiDB 为完善 Realtime HTAP 形态引入的关键组件，TiFlash 通过 Multi-Raft Learner 协议实时从 TiKV 复制数据，确保行存储引擎 TiKV 和列存储引擎 TiFlash 之间的数据强一致。TiKV、TiFlash 可按需部署在不同的机器，解决 HTAP 资源隔离的问题。详情参阅：[TiFlash](/tiflash/tiflash-overview.md)。
+ 4.0 版本中 TiKV 提供新的存储格式，提升宽表场景下编解码数据的效率。

## TiDB Dashboard

+ DBA 通过 [TiDB Dashboard](/dashboard/dashboard-intro.md) UI 可以快速了解集群的集群拓扑、配置信息、日志信息、硬件信息、操作系统信息、慢查询信息、SQL 访问信息、诊断报告信息等，帮助 DBA 通过 SQL 快速了解、分析系统的各项指标，具体信息如下：
    - Cluster Info，提供集群中所有组件，包括：TiDB、TiKV、PD、TiFlash 运行状态及其所在主机的运行状态。
    - Key Visualizer，系统可视化输出 TiDB 集群一段时间内的流量情况，用于 DBA 分析 TiDB 集群的使用模式和排查流量热点。
    - SQL Statements，记录当系统执行的所有 SQL 以及 SQL 相关的统计信息，包括：执行次数、执行时间汇总等，帮助用户快速分析系统的 SQL 执行状况，判断系统中有哪些热点 SQL 语句等。
    - Slow Queries，汇总集群中所有的慢查询语句，帮助用户快速定位慢查询语句。
    - Diagnostic Report，系统会周期性的自动对集群可能存在的问题进行诊断，并将诊断结果和一些集群相关的负载监控信息汇总成一个诊断报告。诊断报告是网页形式，通过浏览器保存后可离线浏览和传阅。
    - Log Search & Download，可视化搜索、查询集群的日志信息，帮忙 DBA 分析系统的问题，提升 DBA 运维的效率。

## 部署运维工具

TiUP 是 4.0 版本中新推出的包管理器的工具，主要用于管理 TiDB 生态内的所有的包，提供组件管理、Playground、Cluster、TUF、离线部署等功能，将安装、部署、运维 TiDB 工具化，提升 DBA 部署、运维 TiDB 的效率。详情参阅：[TiUP](/tiup/tiup-overview.md)。具体的功能如下：

- 组件管理功能，提供一键式组件信息查询、安装、升级、卸载等功能，方便 DBA 管理 TiDB 的所有组件。
- 集群管理功能 (Cluster)：提供一键式 TiDB 集群的部署、运维 TiDB 功能。包括：安装、部署、扩容、缩容、升级、配置变更、启动、停止、重启，查询集群状信息等，支持管理多个 TiDB 集群。
- 本地部署功能 (Playground): 提供快速在本地部署一个 TiDB 集群，快速体验、了解 TiDB 的基本功能，注意：此功能仅用于快速了解 TiDB，不适合上生产。
- 私有镜像管理 (Mirror): 当无法通过公网访问 TiUP 官方镜像时，TiUP 提供构建私有镜像的方案，帮助用户构建私有镜像及提供离线部署部署的功能。
- 性能测试功能 (Benchmark): 提供一键部署性能测试工具的功能，主要提供 TPC-C、TPC-H 两种性能测试的 workload 。

## 事务

+ 悲观事务正式 GA 并作为默认事务模式提供，支持 Read Committed 隔离级别以及 `SELECT FOR UPDATE NOWAIT` 语法。详情参阅：[悲观事务模型](/pessimistic-transaction.md)。
+ 支持大事务，最大事务限制由 100 MB 提升到了 10 GB，同时支持乐观事务和悲观事务。详情参阅：[事务限制](/transaction-overview.md#事务限制)。

## SQL 功能

- 在 SQL Plan Management 中引入了 SQL Bind 的自动捕获和演进，提升易用性和执行计划稳定性。详情参阅：[绑定执行计划](/sql-plan-management.md)。
- 新增 15 种 SQL Hint 用于控制优化器生成执行计划，和执行引擎执行查询时的行为。详情参阅：[SQL Hint](/optimizer-hints.md)。
- 支持 `SELECT INTO outfile` 语句，该语句用来将表数据导出到指定的文本文件中，配合上 `LOAD DATA`，可以方便的在数据库之间导入/导出数据。
- 支持自定义序列对象 Sequence，提供 `CACHE/NO_CACHE`、`CYCLE/NO_CYCLE` 选项定义序列的不同特性，满足序列生成的各种需求，用户可以通过 Sequence 替代第三方 ID 生成服务。详情参阅：[Sequence](/sql-statements/sql-statement-create-sequence.md)。
- 新增 `Flashback` 命令，支持恢复被 `Truncate` 的表。详情参阅：[`Flashback`](/sql-statements/sql-statement-flashback-table.md)。
- 新增查询数据时将 Join、Sort 中间结果写入本地磁盘，防止查询语句占用内存过多导致系统 OOM 的问题，提升系统的稳定性。
- 优化 `EXPLAIN` 和 `EXPLAIN ANALYZE` 的输出结果，显示更多的信息，提升排查问题的效率。详情参阅：[Explain Analyze](/sql-statements/sql-statement-explain-analyze.md)，[Explain](/sql-statements/sql-statement-explain.md)。
- 支持 Index Merge 功能，Index Merge 是一种新的表访问方式，当查询只涉及到单张表时，优化器会自动根据查询条件读取多个索引数据并对结果求并集，提升查询单张表时的性能。详情参阅：[Index Merge](/explain-overview.md#indexmerge-示例)。
- 支持 AutoRandom Key 作为 TiDB 在列属性上的扩展语法，AutoRandom 被设计用于解决自增主键列的写热点问题，为使用自增主键列的用户提供最低成本的 MySQL 迁移方案。详情参阅：[AutoRandom Key](/auto-random.md)。
- 新增集群拓扑、配置信息、日志信息、硬件信息、操作系统信息、慢查询信息等系统表等，帮助 DBA 通过 SQL 快速了解、分析系统的各项指标，详情参阅：[information_schema](/information-schema/information-schema.md)。具体信息如下：

    - 新增集群拓扑、配置、日志、硬件、操作系统等信息表，帮助 DBA 快速了集群配置、状态信息：

        - `cluster_info` 表，用于保存集群的拓扑信息。
        - `cluster_log` 表，用于保存系统的日志信息。
        - `cluster_hardware`，`cluster_systeminfo`，用于保存系统中服务器的硬件系统，操作系统信息等。

    - 新增慢查询、诊断结果、性能监控等系统表，帮助 DBA 快速分析系统的性能瓶颈：

        - `cluster_slow_query` 表，用于记录保存全局的慢查询信息。
        - `cluster_processlist` 表，用于记录保存全局的 processlist。
        - `inspection_result` 表，4.0 版本新增自动性能诊断的功能，帮助 DBA 自动分析系统的性能瓶颈并自动输出相关的性能分析报告，方便 DBA 定位常见的问题和异常项，提升 DBA 运维的效率。
        - `metrics_summary` 和 `metric_summary_by_label` 表，用于记录保存系统中的所有监控指标信息，DBA 可以通过 SQL 访问所有的监控指标并可以与历史的监控指标进行对比，方便 DBA 定位、分析异常现象。
        - `inspection_summary` 表，用于记录保存不同的数据链路或者访问链路上各种关键的监控指标，方便 DBA 定位、分析常见数据链路或者访问链路中的异常现象，例如：读数据、写数据链路。

## 字符集及排序规则

在 TiDB 4.0 的新集群中，支持大小写和口音不敏感的排序规则 `utf8mb4_general_ci` 及 `utf8_general_ci`，详情参阅：[字符集及排序规则](/character-set-and-collation.md)。

## 安全

+ 完善客户端与服务端，组件与组件之间的加密通信，确保连接安全性，保护接收与发送的任何数据不会被网络犯罪分子读取和修改。主要支持基于证书的登录认证、在线更新证书、校验 TLS 证书的 `CommonName` 属性等功能。详情参阅：[开启加密传输](/enable-tls-between-clients-and-servers.md)。
+ 透明数据加密 (Transparent Data Encryption)，简称 TDE，是 TiDB 推出的一个新特性，用来对整个数据库提供保护。数据库开启 TDE 加密功能后，对于连接到数据库的应用程序来说是完全透明的，它不需要对现有应用程序做任何改变。因为 TDE 的加密特性是基本于文件级别的，系统会在将数据写到磁盘之前加密，在读取到内存之前解密，确保数据的安全性。目前主要支持 AES128-CTR、AES192-CTR、AES256-CTR 三种加密算法，支持通过 AWS KMS 管理密钥等功能。详情参阅[静态加密](/encryption-at-rest.md)。

## 备份与恢复

快速备份恢复功能，用来快速的备份与恢复单个 TiDB 集群的数据，确保数据的可靠性，符合企业备份与恢复或者等保的要求。主要支持快速的全量备份与恢复、支持按照数据排序后区间范围备份与恢复数据。详情参阅：[快速备份与恢复工具](/br/backup-and-restore-tool.md)。

## 服务级别功能

+ 支持缓存 `Prepare`/`Execute` 请求的执行计划，提升 SQL 的执行效率。详情参阅：[缓存执行计划](/sql-prepare-plan-cache.md)。
+ 支持自适应线程池功能，精简线程池数量，优化请求处理调度方式，提升产品易用性，提升产品的性能。
+ Follower Read 功能是指在强一致性读的前提下使用 Region 的 follower 副本来承载数据读取的任务，从而提升 TiDB 集群的吞吐能力并降低 leader 负载。Follower Read 包含一系列将 TiKV 读取负载从 Region 的 leader 副本上 offload 到 follower 副本的负载均衡机制。TiKV 的 Follower Read 可以保证数据读取的一致性，可以为用户提供强一致的数据读取能力。详情参阅：[Follower Read](/follower-read.md)。

## TiCDC

TiCDC 支持通过拉取 TiKV 变更日志实现 TiDB 集群之间数据同步，支持数据的高可靠、服务的高可用能力，确保数据不会丢失。用户可以通过订阅的方式订阅数据的变更信息，系统会自动将数据推送到下游系统，当前仅支持 MySQL 协议的数据库（例如：MySQL、TiDB），Kafka 及 Pulsar 作为 TiCDC 的下游，同时用户也可以通过 TiCDC 提供的[开放数据协议](/ticdc/ticdc-open-protocol.md)自行扩展支持的下游系统。详情参阅：[TiCDC](/ticdc//ticdc-overview.md)。
