---
title: TiDB 7.5.0 Release Notes
summary: 了解 TiDB 7.5.0 版本的新功能、兼容性变更、改进提升，以及错误修复。
---

# TiDB 7.5.0 Release Notes

发版日期：2023 年 x 月 x 日

TiDB 版本：7.5.0

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v7.5/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v7.5/production-deployment-using-tiup) | [下载离线包](https://cn.pingcap.com/product-community/?version=v7.5.0#version-list)

TiDB 7.5.0 为长期支持版本 (Long-Term Support Release, LTS)。

相比于前一个 LTS（即 7.1.0 版本），7.5.0 版本包含 [7.2.0-DMR](/releases/release-7.2.0.md)、[7.3.0-DMR](/releases/release-7.3.0.md) 和 [7.4.0-DMR](/releases/release-7.4.0.md) 中已发布的新功能、提升改进和错误修复，并引入了以下关键特性：

## 功能详情

### 可扩展性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 性能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 稳定性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 高可用

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### SQL 功能

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据库管理

* BR 支持备份和恢复表统计信息 [#issue号](链接) @[Leavrth](https://github.com/Leavrth) <!--**tw@hfxsd** 1437-->

    BR 备份工具 从 v7.5.0 开始支持备份和恢复数据库统计信息，包括列、索引和表级别的统计信息。通过支持该功能，从备份中恢复的 TiDB 数据库不再需要手动运行统计信息收集任务或等待自动收集任务的完成，简化了数据库维护并提升高了恢复库的查询性能。可以通过 [`--ignore-stats=false`](/br/br-snapshot-manual.md#备份统计信息) 启用该功能。

    更多信息，请参考[用户文档](/br/br-snapshot-manual.md#备份统计信息)。

### 可观测性

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 安全

* 功能标题 [#issue号](链接) @[贡献者 GitHub ID](链接)

    功能描述（需要包含这个功能是什么、在什么场景下对用户有什么价值、怎么用）

    更多信息，请参考[用户文档](链接)。

### 数据迁移

* Data Migration (DM) 支持拦截不兼容（破坏数据一致性）的 DDL 变更 [#9692](https://github.com/pingcap/tiflow/issues/9692) @[GMHDBJD](https://github.com/GMHDBJD) <!--**tw@hfxsd** 1523-->

    在 v7.5.0 之前，使用 DM 的 Binlog Filter 功能只能迁移或过滤指定的 event，且颗粒度比较粗，例如只能过滤 ALTER 这种大颗粒度的 DDL Event，这种方式在某些业务场景会受限，如业务允许 Add Column，但是不允许 Drop Column，但之前的版本都会被 Alter 这个 Event 过滤。

    因此，在 v7.5.0 在原先基础上细化了支持的 DDL event，如新增 Modify Column（修改列数据类型），Drop column 等会导致数据丢失、数据被截断、精度损失等问题的细粒度 DDL event，用户可以按需配置，同时还支持拦截这些 DDL，并报错提示用户，用户可以及时介入手工处理，避免对下游的业务数据产生影响。

    更多信息，请参考[用户文档](https://github.com/pingcap/docs-cn/pull/15309)。

* 支持实时更新增量数据校验的 checkpoint [issue号](链接) @[lichunzhu](https://github.com/lichunzhu) <!--**tw@ran-huang** 1496-->

    在 v7.5.0 之前，你可以使用[增量数据校验功能](/dm/dm-continuous-data-validation.md)来判断 DM 同步到下游的数据是否与上游一致，并以此作为业务流量从上游数据库割接到 TiDB 的依据。然而，由于增量校验 checkpoint 受到较多限制，如同步延迟、不一致的数据等待重新校验等因素，需要每隔几分钟刷新一次校验后的 checkpoint。对于某些只有几十秒割接时间的业务场景来说，这是无法接受的。

    v7.5.0 引入实时更新增量数据校验的 checkpoint 后，你可以传入上游数据库填写的 binlog 位置。一旦增量校验程序在内存里校验到该 binlog 位置，会立即刷新 checkpoint，而不是每隔几分钟刷新 checkpoint。因此，你可以根据该立即返回的 checkpoint 快速进行割接操作。

    更多信息，请参考[用户文档](链接)。

## 兼容性变更

> **注意：**
>
> 以下为从 v7.4.0 升级至当前版本 (v7.5.0) 所需兼容性变更信息。如果从 v7.3.0 或之前版本升级到当前版本，可能也需要考虑和查看中间版本 Release Notes 中提到的兼容性变更信息。

### 行为变更

* 行为变更 1

* 行为变更 2

### MySQL 兼容性

* 兼容性 1

* 兼容性 2

### 系统变量

| 变量名  | 修改类型（包括新增/修改/删除）    | 描述 |
|--------|------------------------------|------|
|        |                              |      |
|        |                              |      |
|        |                              |      |
|        |                              |      |

### 配置文件参数

| 配置文件 | 配置项 | 修改类型 | 描述 |
| -------- | -------- | -------- | -------- |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |
|          |          |          |          |

### 其他

## 离线包变更

从 v7.5.0 开始，`TiDB-community-toolkit` 二进制软件包中移除了以下内容：

- `tikv-importer-{version}-linux-{arch}.tar.gz`
- `mydumper`

## 废弃功能

* [Mydumper](https://docs.pingcap.com/zh/tidb/v4.0/mydumper-overview) 在 v7.5.0 中废弃，其绝大部分功能已经被 [Dumpling](/dumpling-overview.md) 取代，强烈建议切换到 Dumpling。<!--**tw@Oreoxmt** 1593-->

* TiKV-importer 组件在 v7.5.0 中废弃，建议使用 [TiDB Lightning 物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)作为替代方案。<!--**tw@Oreoxmt** 1594-->

* [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 在 v7.5.0 废弃数据同步功能，强烈建议使用 [TiCDC](/ticdc/ticdc-overview.md) 来实现高效稳定的数据同步。尽管 TiDB Binlog 在 v7.5.0 仍支持 Point-in-Time Recovery (PITR) 场景，但是该组件在未来 LTS 版本中将被完全废弃，推荐使用 [PITR](/br/br-pitr-guide.md) 替代。<!--**tw@Oreoxmt** 1575-->

* 统计信息的[快速分析](https://docs.pingcap.com/zh/tidb/v7.4/system-variables#tidb_enable_fast_analyze)（实验特性）在 v7.5.0 中废弃。<!--**tw@Oreoxmt** -->

* 统计信息的[增量收集](https://docs.pingcap.com/zh/tidb/v7.4/statistics#增量收集)（实验特性）在 v7.5.0 中废弃。<!--**tw@Oreoxmt** -->

## 改进提升

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 错误修复

+ TiDB

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiKV

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ PD

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ TiFlash

    - note [#issue](链接) @[贡献者 GitHub ID](链接)
    - note [#issue](链接) @[贡献者 GitHub ID](链接)

+ Tools

    + Backup & Restore (BR)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiCDC

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Data Migration (DM)

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiDB Lightning

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

    + TiUP

        - note [#issue](链接) @[贡献者 GitHub ID](链接)
        - note [#issue](链接) @[贡献者 GitHub ID](链接)

## 性能测试

如需了解 TiDB v7.5.0 的性能表现，你可以参考 TiDB Dedicated 集群的 [TPC-C 性能测试报告](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-tpcc)和 [Sysbench 性能测试报告](https://docs.pingcap.com/tidbcloud/v7.5.0-performance-benchmarking-with-sysbench)（英文版）。

## 贡献者

感谢来自 TiDB 社区的贡献者们：

- [贡献者 GitHub ID]()