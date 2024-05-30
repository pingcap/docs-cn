---
title: TiDB Lightning 和 IMPORT INTO 的兼容性和使用场景
summary: 了解 TiDB Lightning 和 IMPORT INTO、Log Backup、TiCDC 的兼容性。
---

# TiDB Lightning 和 IMPORT INTO 的兼容性和使用场景

本文档介绍 TiDB Lightning 和 `IMPORT INTO` 与 Log Backup、TiCDC 的兼容性，以及某些特殊的使用场景。

## TiDB Lightning 和 IMPORT INTO 对比

[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 目前已经集成了 TiDB Lightning 的物理导入模式，但二者还存在一些差异。

> **注意：**
>
> 与 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 相比，[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 语句可以直接在 TiDB 节点上执行，支持自动化分布式任务调度和 [TiDB 全局排序](/tidb-global-sort.md)，在部署、资源利用率、任务配置便捷性、调用集成便捷性、高可用性和可扩展性等方面都有很大提升。建议在合适的场景下，使用 `IMPORT INTO` 代替 TiDB Lightning。

### TiDB Lightning

TiDB Lightning 目前支持物理导入模式和逻辑导入模式，不同的模式决定 TiDB Lightning 如何将数据导入到目标 TiDB 集群。你可以通过 [`backend`](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置) 配置使用相关导入模式。

- [物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)：TiDB Lightning 首先将数据编码成键值对并排序存储在本地临时目录，然后将这些键值对上传到各个 TiKV 节点，最后调用 TiKV Ingest 接口将数据插入到 TiKV 的 RocksDB 中。如果用于初始化导入，请优先考虑使用物理导入模式，其拥有较高的导入速度，单节点峰值性能可达到 500 GiB/h。物理导入模式对应的后端模式为 `local`。

- [逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)：TiDB Lightning 先将数据编码成 SQL，然后直接运行这些 SQL 语句进行数据导入，单节点性能峰值 50 GiB/h。如果需要导入的集群为生产环境线上集群，或需要导入的目标表中已包含数据，则应使用逻辑导入模式。逻辑导入模式对应的后端模式为 `tidb`。

### IMPORT INTO

[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 目前已经集成了 TiDB Lightning 的物理导入模式，但尚不支持逻辑导入模式。

## 兼容性说明

- TiDB Lightning 的逻辑导入模式与 Log Backup 以及 TiCDC 兼容。

- TiDB Lightning 的物理导入模式以及 `IMPORT INTO` 与 Log Backup 以及 TiCDC 均不兼容。原因是 TiDB Lightning 物理导入模式或 `IMPORT INTO`，均是将源数据编码后的 KV Pairs 直接 Ingest 到 TiKV，该过程 TiKV 不会产生相应的 Change log，由于没有这部分的 Change log，相关数据无法被 Log Backup 备份，也无法被 TiCDC 复制。

## TiDB Lightning 物理导入模式的使用场景

如果 TiDB Lightning 逻辑导入的性能可以满足业务的性能要求，且业务要求 TiDB Lightning 导入的表进行数据备份，或者使用 TiCDC 同步到下游，建议使用 TiDB Lightning 逻辑导入模式。

如果业务对导入性能有要求，且只能使用 TiDB Lightning 物理导入模式的场景，同时这些表还需要备份或者使用 TiCDC 同步到下游，则建议使用以下方案进行处理。

### TiDB Lightning 物理导入模式和 Log Backup

#### 场景 1：物理导入模式的表不需要备份

该场景下，由于开启了 [PITR](/br/br-log-architecture.md#pitr)，因此启动 TiDB Lightning 后兼容性检查会报错。如果你确定这些表不需要备份或者 Log Backup，你可以把 [TiDB Lightning 配置文件](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)中的 `Lightning.check-requirements` 参数改成 `false`，然后重新启动任务即可。

#### 场景 2：物理导入模式导入完成后，该表不会有 DML 操作

该场景由于不涉及增量数据写入，因此在 TiDB Lightning 物理导入模式完成数据导入后，对该表执行一次表级别快照备份即可，操作步骤请参考[备份单张表的数据](/br/br-snapshot-manual.md#备份单张表的数据)。

在数据恢复时，对该表的快照数据进行恢复，操作步骤请参考[恢复单张表格](/br/br-snapshot-manual.md#恢复单张表的数据)。

#### 场景 3：物理导入模式导入完成后，该表会执行 DML 操作（不支持）

该场景下，对该表的备份操作，只能在执行全量快照备份和增量备份之间二选一，无法备份并恢复该表的全量快照数据+增量数据。

### TiDB Lightning 物理导入模式和 TiCDC

该场景短期内无法兼容，因为 TiCDC 也很难追上 TiDB Lightning 物理导入的写入速度，造成集群同步延迟不断增加。

在该场景下，如果上游 TiDB 集群某张表使用 TiDB Lightning 物理导入模式导入数据，而且需要被同步到下游，建议按如下步骤操作：

- 在该场景下，由于开启了 TiCDC Changefeed，因此启动 TiDB Lightning 后兼容性检查会报错。如果你确定这些表不需要被 TiCDC 同步，你可以把 [TiDB Lightning 配置文件](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)中的 `Lightning.check-requirements` 参数改成 `false`，然后重新启动任务即可。

- 使用 TiDB Lightning 在下游 TiDB 集群也导入一份同样的数据。如果下游是 Redshift、Snowflake 等数据库，这些数据库也支持直接从 Cloud Storage 读取 CSV、Parquet 等文件并写入到数据库。

## `IMPORT INTO` 的使用场景

### `IMPORT INTO` 和 Log Backup

该场景下，由于开启了 [PITR](/br/br-log-architecture.md#pitr)，因此提交 `IMPORT INTO` SQL 后兼容性检查会报错。如果你确定这些表不需要备份或者 Log Backup，你可以在该 SQL 的 [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) 里带上参数 `DISABLE_PRECHECK`（从 v8.0.0 版本引入）重新提交即可，这样数据导入任务会忽略该兼容性检查，直接导入数据。

### `IMPORT INTO` 和 TiCDC

在该场景下，由于开启了 TiCDC Changefeed，因此提交 `IMPORT INTO` SQL 语句后兼容性检查会报错。如果你确定这些表不需要被 TiCDC 同步，你可以在该 SQL 的 [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) 里带上参数 `DISABLE_PRECHECK`（从 v8.0.0 版本引入）重新提交即可，这样数据导入任务会忽略该兼容性检查，直接导入数据。