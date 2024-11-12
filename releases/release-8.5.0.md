---
title: TiDB 8.5.0 Release Notes
summary: 了解 TiDB 8.5.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 8.5.0 Release Notes

<EmailSubscriptionWrapper />

发版日期：2024 年 5 月 24 日

TiDB 版本：8.5.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v8.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v8.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v8.5.0#version-list)

TiDB 8.5.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 8.1.0 版本），8.5.0 版本包含 [8.2.0-DMR](/releases/release-8.2.0.md)、[8.3.0-DMR](/releases/release-8.3.0.md), 和 [8.4.0-DMR] 中已发布的新功能、提升改进和错误修复。当你从 8.1.x 升级到 8.5.0 时，可以下载 [TiDB Release Notes PDF](https://download.pingcap.org/tidb-v8.1-to-v8.5-zh-release-notes.pdf) 查看两个 LTS 版本之间的所有 Release Notes。下表列出了从 8.1.0 到 8.5.0 的一些关键特性：

<!--Highlights table: ToDo-->

## 功能详情

### 可扩展性

* Schema 缓存内存上限功能成为正式功能（GA），减少了大规模数据场景的内存占用 [#50959](https://github.com/pingcap/tidb/issues/50959) @[tiancaiamao](https://github.com/tiancaiamao) @[wjhuang2016](https://github.com/wjhuang2016) @[gmhdbjd](https://github.com/gmhdbjd) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--1976-->

    在一些 SaaS 场景下，当表的数据量达到几十万甚至上百万时，schema meta 会占用较多的内存。开启该功能后，系统将使用 LRU 算法缓存和淘汰相应 schema meta 信息，有效减少内存占用。从 v8.4 开始，该功能默认开启，默认值为 512MiB，用户可通过参数 [tidb_schema_cache_size](/system-variables#tidb_schema_cache_size-new-in-v800)，按需调整。

    更多信息，请参考[用户文档](链接)。

* Use the Active PD Follower feature to enhance the scalability of PD's Region information query service (General Availability) [#7431](https://github.com/tikv/pd/issues/7431) @[okJiang](https://github.com/okJiang)

    In a TiDB cluster with a large number of Regions, the PD leader might experience high CPU load due to the increased overhead of handling heartbeats and scheduling tasks. If the cluster has many TiDB instances, and there is a high concurrency of requests for Region information, the CPU pressure on the PD leader increases further and might cause PD services to become unavailable.

    To ensure high availability and also enhance the scalability of PD's Region information query service. You can enable the Active PD Follower feature by setting the system variable [`pd_enable_follower_handle_region`](/system-variables.md#pd_enable_follower_handle_region-new-in-v760) to `ON`. After this feature is enabled, TiDB evenly distributes Region information requests to all PD servers, and PD followers can also handle Region requests, thereby reducing the CPU pressure on the PD leader.

    For more information, see [documentation](/tune-region-performance.md#use-the-active-pd-follower-feature-to-enhance-the-scalability-of-pds-region-information-query-service)

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 建库，建表加速功能成为正式功能（GA），大大节省了数据迁移，集群初始化的时间 [#50052](https://github.com/pingcap/tidb/issues/50052) @[D3Hunter](https://github.com/D3Hunter) @[gmhdbjd](https://github.com/gmhdbjd) tw@Oreoxmt <!--1977-->

    v8.0.0 引入了系统变量 [tidb_enable_fast_create_table](/system-variables#tidb_enable_fast_create_table-new-in-v800)，用于提升批量建库、建表的性能。在数据迁移，初始化集群环境时，可快速创建百万规模的表，大大减少耗时。

    更多信息，请参考[用户文档](链接)。

### 稳定性

* Enabling rate limiter can protect PD from being crash under a large number of sudden requests and improve the stability of PD [#5739](https://github.com/tikv/pd/issues/5739) @[rleungx](https://github.com/rleungx)

    You can adjust the rate limiter configuration through pd-ctl.

    For more information, see [Documentation](/stable/pd-control.md).

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

* 外键的功能成为正式功能（GA） [#36982](https://github.com/pingcap/tidb/issues/36982) @[YangKeao](https://github.com/YangKeao) @[crazycs520](https://github.com/crazycs520) tw@lilin90 <!--1894-->

    TiDB 的外键功能现已 GA，支持通过使用外键约束提升数据一致性和完整性保障。用户可以轻松创建表间的外键关联，实现级联更新和删除操作，使得数据管理更加便捷。这一功能为复杂数据关联的应用场景提供了更好的支持。

    更多信息，请参考[用户文档](链接)。

* 引入 ADMIN ALTER DDL JOBS 的语法，支持在线修改 DDL 任务参数 [#57229](hhttps://github.com/pingcap/tidb/issues/57229) @[fzzf678](https://github.com/fzzf678) @[tangenta](https://github.com/tangenta) tw@hfxsd <!--2016-->

    从 V8.3 版本开始，支持在 Session 级别设置变量 [tidb_ddl_reorg_batch_size](/system-variables#tidb_ddl_reorg_batch_size) 和  [tidb_ddl_reorg_worker_cnt](/system-variables#tidb_ddl_reorg_worker_cnt) ，因此通过 Global 设置这 2 个变量已不再影响所有运行中的 DDL 任务。如需更改这些变量的值，需要先取消 DDL 任务，调整变量取值后再重新提交。

    因此，从 V8.5 版本起，引入了 `ADMIN ALTER DDL JOBS` 语法，允许对指定的 DDL 任务在线调整变量值，以便灵活平衡资源消耗与性能，并将变更限定于单个任务，使影响范围更加可控。例如：

    - `ADMIN ALTER DDL JOBS job_id THREAD = 8;` — 在线调整该 DDL 任务的 `tidb_ddl_reorg_worker_cnt`
    - `ADMIN ALTER DDL JOBS job_id BATCH_SIZE = 256;` — 在线调整该 DDL 任务的 `tidb_ddl_reorg_batch_size`
    - `ADMIN ALTER DDL JOBS job_id MAX_WRITE_SPEED = '200MiB';` — 在线调整写入每个 TiKV 节点的索引数据流量大小

  更多信息，请参考[用户文档](链接)。

### 数据库管理

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* BR supports client-side encryption of log backup data (GA) [#56433](https://github.com/pingcap/tidb/issues/56433) @[Tristan1900](https://github.com/Tristan1900) tw@qiancai <!--1998-->

    TiDB v8.4.0 introduced an experimental feature to encrypt, on the client side, log backup data. Starting from v8.5.0, this feature is now Generally Avaialble. Before uploading log backup data to your backup storage, you can encrypt the backup data to ensure its security via one of the following methods:

    - Encrypt using a custom fixed key
    - Encrypt using a master key stored on a local disk
    - Encrypt using a master key managed by a Key Management Service (KMS)

  For more information, see [documentation](/br/br-pitr-manual.md#encrypt-the-log-backup-data).

### 数据迁移

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接) **tw@xxx** <!--1234-->

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v8.4.0 升级至当前版本 (v8.5.0) 所需兼容性变更信息。如果从 v8.3.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

### MySQL 兼容性

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|tidb_ddl_reorg_max_write_speed | Newly added |Used to control the speed at which TiDB writes index data to a single TiKV node. For example, setting the value to 200 MiB limits the maximum write speed to 200 MiB/s. |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 配置参数

| 配置文件或组件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|  |  |  |  |
|  |  |  |  |
|  |  |  |  |

### 系统表

### 其他

## 离线包变更

## 移除功能

## 废弃功能

以下为计划将在未来版本中废弃的功能：

* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入)，用于控制是否启用优先队列来优化自动收集统计信息任务的排序。在未来版本中，优先队列将成为自动收集统计信息任务的唯一排序方式，系统变量 [`tidb_enable_auto_analyze_priority_queue`](/system-variables.md#tidb_enable_auto_analyze_priority_queue-从-v800-版本开始引入) 将被废弃。
* TiDB 在 v7.5.0 引入了系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入)，用于设置 TiDB 使用异步方式合并分区统计信息，以避免 OOM 问题。在未来版本中，分区统计信息将统一使用异步方式进行合并，系统变量 [`tidb_enable_async_merge_global_stats`](/system-variables.md#tidb_enable_async_merge_global_stats-从-v750-版本开始引入) 将被废弃。
* 计划在后续版本重新设计[执行计划绑定的自动演进](/sql-plan-management.md#自动演进绑定-baseline-evolution)，相关的变量和行为会发生变化。
* TiDB 在 v8.0.0 引入了系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入)，用于控制 TiDB 是否支持并行 HashAgg 进行落盘。在未来版本中，系统变量 [`tidb_enable_parallel_hashagg_spill`](/system-variables.md#tidb_enable_parallel_hashagg_spill-从-v800-版本开始引入) 将被废弃。
* TiDB Lightning 参数 [`conflict.max-record-rows`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 计划在未来版本中废弃，并在后续版本中删除。该参数将由 [`conflict.threshold`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 替代，即记录的冲突记录数和单个导入任务允许出现的冲突记录数的上限数保持一致。
* 从 v6.3.0 开始，分区表默认使用[动态裁剪模式](/partitioned-table.md#动态裁剪模式)，相比静态裁剪模式，动态裁剪模式支持 IndexJoin、Plan Cache 等特性，性能表现更好。在未来版本中，静态裁剪模式将被废弃。

## 改进提升

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## 错误修复

+ TiDB

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiKV

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ PD

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ TiFlash

    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
    - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

+ Tools

    + Backup & Restore (BR)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiCDC

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Data Migration (DM)

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiDB Lightning

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

    + TiUP

        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)
        - note [#Issue-number](issue-link) @[Contributor-GitHub-ID](id-link)

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [Contributor-GitHub-ID](id-link)