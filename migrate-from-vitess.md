---
title: 从 Vitess 迁移数据到 TiDB
summary: 介绍从 Vitess 迁移数据到 TiDB 所使用的工具。
---

# 从 Vitess 迁移数据到 TiDB

本文档介绍了将数据从 [Vitess](https://vitess.io/) 迁移到 TiDB 时可以采用的工具。

由于 Vitess 的后端基于 MySQL，当从 Vitess 迁移数据到 TiDB 时，你可以直接使用 MySQL 适用的迁移数据工具，如 [Dumpling](/dumpling-overview.md)、[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 和 [TiDB Data Migration (DM)](/dm/dm-overview.md)。需要注意的是，针对 Vitess 中的每个分片，你都需要进行相应的迁移工具配置以完成数据迁移。通常情况下，推荐使用 DM 进行数据迁移（将 DM 的 `task-mode` 设为 `all`，`import-mode` 设为 `physical`）。如果数据量超过 10 TiB，建议分两步导入：第一步使用 Dumpling 和 TiDB Lightning 导入已有数据，第二步使用 DM 导入增量数据。

除了以上工具，你还可以使用 [Debezium 的 Vitess 连接器](https://debezium.io/documentation/reference/connectors/vitess.html)。该连接器可以通过 [Kafka Connect](https://kafka.apache.org/documentation/#connect) 或 [Apache Flink](https://nightlies.apache.org/flink/flink-docs-stable/) 将 Vitess 的数据变更同步到 TiDB 中。

由于 Vitess 和 TiDB 都支持 MySQL 协议和 SQL 方言，应用层预计只涉及较少的更改。但对于一些直接管理分片或实现特定业务逻辑的任务，可能涉及较大的更改。为了方便从 Vitess 向 TiDB 迁移数据，TiDB 引入了 [`VITESS_HASH()`](/functions-and-operators/tidb-functions.md) 函数，该函数返回的字符串哈希值与 Vitess 的 HASH 函数兼容。

## 示例

### Dumpling 和 TiDB Lightning

以下两个示例展示了 Dumpling 和 TiDB Lightning 如何协同工作，将数据从 Vitess 迁移到 TiDB。

- 在此示例中，TiDB Lightning 使用[逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)，先将数据编码为 SQL 语句，然后运行这些 SQL 语句来导入数据。

    ![Vitess to TiDB Migration with TiDB backend](/media/vitess_to_tidb.png)

- 在此示例中，TiDB Lightning 使用[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)直接将数据导入 TiKV。

    ![Vitess to TiDB Migration with local backend](/media/vitess_to_tidb_dumpling_local.png)

### DM

以下示例展示了 [DM](/dm/dm-overview.md) 如何将数据从 Vitess 迁移到 TiDB。

![Vitess to TiDB with DM](/media/vitess_to_tidb_dm.png)