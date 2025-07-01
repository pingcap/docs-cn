---
title: IMPORT INTO 和 TiDB Lightning 与日志备份和 TiCDC 的兼容性
summary: 了解 IMPORT INTO 和 TiDB Lightning 与日志备份和 TiCDC 的兼容性及使用场景。
---

# IMPORT INTO 和 TiDB Lightning 与日志备份和 TiCDC 的兼容性

本文档介绍 TiDB Lightning 和 [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 与[日志备份](/br/br-pitr-guide.md)、[TiCDC](/ticdc/ticdc-overview.md) 的兼容性，以及某些特殊的使用场景。

## `IMPORT INTO` 和 TiDB Lightning 对比

[`IMPORT INTO`](/sql-statements/sql-statement-import-into.md) 目前已经集成了 TiDB Lightning 的物理导入模式，但二者还存在一些差异。详情请参见 [`IMPORT INTO` 和 TiDB Lightning 对比](/tidb-lightning/import-into-vs-tidb-lightning.md)。

## 与日志备份和 TiCDC 的兼容性

- TiDB Lightning 的[逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)与日志备份以及 TiCDC 兼容。

- TiDB Lightning 的[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)与日志备份以及 TiCDC 均不兼容。原因是 TiDB Lightning 物理导入模式是将源数据编码后的 KV Pairs 直接 Ingest 到 TiKV，该过程 TiKV 不会产生相应的 Change log，由于没有这部分的 Change log，相关数据无法通过日志备份的方式备份，也无法被 TiCDC 复制。

- 如果你需要在同一个集群上同时使用 TiDB Lightning 和 TiCDC，请参考 [TiCDC 与 TiDB Lightning 的兼容性](/ticdc/ticdc-compatibility.md#ticdc-与-tidb-lightning-的兼容性)。

- `IMPORT INTO` 与日志备份以及 TiCDC 均不兼容。原因是 `IMPORT INTO` 的导入过程也是将源数据编码后的 KV Pairs 直接 Ingest 到 TiKV。

## TiDB Lightning 逻辑导入模式的使用场景

如果 TiDB Lightning 逻辑导入的性能可以满足业务的性能要求，且业务要求 TiDB Lightning 导入的表进行数据备份，或者使用 TiCDC 同步到下游，建议使用 TiDB Lightning 逻辑导入模式。

## TiDB Lightning 物理导入模式的使用场景

本节介绍 TiDB Lightning 物理导入模式与[日志备份](/br/br-pitr-guide.md)和 [TiCDC](/ticdc/ticdc-overview.md) 同时使用时的操作方法。

如果 TiDB Lightning 逻辑导入的性能无法满足业务的性能要求，且只能使用 TiDB Lightning 物理导入模式的场景，同时这些表还需要备份或者使用 TiCDC 同步到下游，则建议使用以下方案进行处理。

### 和日志备份同时使用

该场景下，如果开启了 [PITR](/br/br-log-architecture.md#pitr)，启动 TiDB Lightning 后兼容性检查会报错。如果你确定不需要备份这些表，你可以把 [TiDB Lightning 配置文件](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)中的 `Lightning.check-requirements` 参数改成 `false`，然后重新启动导入任务即可。

由于无法对 TiDB Lightning 物理导入模式导入的数据进行日志备份，如果你需要对该表进行备份，可在 TiDB Lightning 物理导入模式完成数据导入后，对该表执行一次表级别快照备份即可，操作步骤请参考[备份单张表的数据](/br/br-snapshot-manual.md#备份单张表的数据)。

### 和 TiCDC 同时使用

该场景短期内无法兼容，因为 TiCDC 很难追上 TiDB Lightning 物理导入的写入速度，可能造成集群同步延迟不断增加。

可根据如下不同的场景进行操作：

- 场景 1：该表不需要被 TiCDC 同步到下游。

    在该场景下，如果开启了 TiCDC 同步任务，启动 TiDB Lightning 后兼容性检查会报错。如果你确定这些表不需要被 TiCDC 同步，你可以把 [TiDB Lightning 配置文件](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)中的 `Lightning.check-requirements` 参数改成 `false`，然后重新启动导入任务即可。

- 场景 2：该表需要被 TiCDC 同步到下游。

    在该场景下，由于上游 TiDB 集群开启了 TiCDC 同步任务，因此启动 TiDB Lightning 后兼容性检查会报错。你需要在上游 TiDB 集群把 [TiDB Lightning 配置文件](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-任务配置)中的 `Lightning.check-requirements` 参数改成 `false`，然后重新启动导入任务即可。

    上游 TiDB 集群的导入任务完成后，再使用 TiDB Lightning 在下游 TiDB 集群也导入一份同样的数据。如果下游是 Redshift、Snowflake 等数据库，可直接让这些数据库从 Cloud Storage 读取 CSV、SQL、Parquet 等格式的文件并写入到数据库。

## `IMPORT INTO` 的使用场景

本节介绍 `IMPORT INTO` 与[日志备份](/br/br-pitr-guide.md)和 [TiCDC](/ticdc/ticdc-overview.md) 同时使用时的操作方法。

### 和日志备份同时使用

该场景下，如果开启了 [PITR](/br/br-log-architecture.md#pitr)，提交 `IMPORT INTO` SQL 语句后兼容性检查会报错。如果你确定不需要备份这些表，你可以在该 SQL 的 [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) 里带上参数 `DISABLE_PRECHECK`（从 v8.0.0 版本引入）重新提交即可，这样数据导入任务会忽略该兼容性检查，直接导入数据。

由于无法对 `IMPORT INTO` 导入的数据进行日志备份，如果你需要对该表进行备份，可在完成数据导入后，对该表执行一次表级别快照备份即可，操作步骤请参考[备份单张表的数据](/br/br-snapshot-manual.md#备份单张表的数据)。

### 和 TiCDC 同时使用

可根据如下不同的场景进行操作：

- 场景 1：该表不需要被 TiCDC 同步到下游。

    在该场景下，如果开启了 TiCDC Changefeed，提交 `IMPORT INTO` SQL 语句后兼容性检查会报错。如果你确定这些表不需要被 TiCDC 同步，你可以在该 SQL 的 [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) 里带上参数 `DISABLE_PRECHECK`（从 v8.0.0 版本引入）重新提交即可，这样数据导入任务会忽略该兼容性检查，直接导入数据。

- 场景 2：该表需要被 TiCDC 同步到下游。

    在该场景下，如果上游 TiDB 集群开启了 TiCDC 同步任务，提交 `IMPORT INTO` SQL 语句后兼容性检查会报错。你需要在该 SQL 的 [`WithOptions`](/sql-statements/sql-statement-import-into.md#withoptions) 里带上参数 `DISABLE_PRECHECK`（从 v8.0.0 版本引入）重新提交即可。

    上游 TiDB 集群的导入任务完成后，再使用 `IMPORT INTO` 在下游 TiDB 集群也导入一份同样的数据。如果下游是 Redshift、Snowflake 等数据库，可直接让这些数据库从 Cloud Storage 读取 CSV、SQL、Parquet 等格式的文件并写入到数据库。
