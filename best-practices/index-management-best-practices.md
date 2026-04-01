---
title: 管理索引和识别未使用索引的最佳实践
summary: 了解在 TiDB 中管理和优化索引、识别并移除未使用索引的最佳实践。
aliases: ['/zh/tidb/stable/index-management-best-practices/','/zh/tidb/dev/index-management-best-practices/']
---

# 管理索引和识别未使用索引的最佳实践

索引对于优化数据库查询性能至关重要，能够减少大规模数据扫描的需求。然而，随着应用的演进、业务逻辑的变化以及数据规模的增长，原有的索引设计也可能会遇到问题，包括以下两类：

- 未使用索引：这些索引曾经有用，但现在查询优化器已不再选择它们，却仍占用存储空间，并给写入操作带来不必要的开销。
- 低效索引：某些索引虽然被优化器使用，但扫描的数据量远超预期，导致磁盘 I/O 增加，查询速度变慢。

如果不及时处理，这些索引问题会导致存储成本上升、性能下降和运维效率降低。在 TiDB 这样的分布式 SQL 数据库中，索引效率低下的影响更大，因为分布式查询规模大且多节点协同更复杂。因此，定期进行索引审计对于保持数据库优化至关重要。

主动识别并优化索引有助于：

- 降低存储开销：移除未使用索引可释放磁盘空间，降低长期存储成本。
- 提升写入性能：写密集型场景（如 `INSERT`、`UPDATE`、`DELETE`）下，移除不必要的索引维护可以提升性能。
- 优化查询执行：高效的索引能够减少扫描的行数，从而加快查询速度、缩短响应时间。
- 简化数据库管理：减少并优化索引可以简化备份、恢复和 schema 变更。

由于索引会随着业务逻辑的变化而不断演进，定期进行索引审计已成为数据库维护的标准流程。TiDB 提供了内置的可观测性手段，帮助你安全高效地观测、评估和优化索引。

TiDB v8.0.0 引入了 [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 表和 [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 表，来帮助你追踪索引使用情况，并根据运行数据做出正确判断。

本文介绍如何使用观测工具检测并移除未使用或低效索引，从而提升 TiDB 的性能与稳定性。

## TiDB 索引优化：数据驱动的方法

索引对于查询性能至关重要，但如果没有充分分析就移除索引，可能导致意想不到的性能回退，甚至引发系统不稳定。为确保索引管理的安全性与有效性，TiDB 提供了内置的可观测性手段，支持以下操作：

- 实时追踪索引使用情况：识别索引的访问频率，并判断其是否有助于性能提升。
- 检测未使用索引：定位自数据库上次重启以来从未被使用过的索引。
- 评估索引效率：判断索引是否能有效过滤数据，或是否导致 I/O 开销过多。
- 安全测试索引移除：在删除索引前，可将其暂时设为不可见，确认无查询依赖该索引后再删除。

TiDB 通过以下手段简化了索引优化：

- `INFORMATION_SCHEMA.TIDB_INDEX_USAGE`：监控索引使用模式和查询频率。
- `sys.schema_unused_indexes`：列出自数据库上次重启以来未被使用过的索引。
- 不可见索引：在永久删除索引之前，你可以先测试移除索引的影响。

借助这些可观测性工具，你可以放心清理冗余索引，避免性能下降风险。

## 使用 `TIDB_INDEX_USAGE` 追踪索引使用情况

从 [TiDB v8.0.0](/releases/release-8.0.0.md) 开始，你可以使用 `TIDB_INDEX_USAGE` 系统表实时观测索引使用情况，帮助你优化查询性能并移除不必要的索引。

具体来说，你可以通过 `TIDB_INDEX_USAGE` 进行以下操作：

- 检测未使用索引：识别未被查询访问过的索引，帮助判断哪些索引可以安全移除。
- 分析索引效率：追踪索引使用频率，评估其是否有助于提升查询执行效率。
- 评估查询模式：了解索引对读操作、数据扫描和 KV 请求的影响。

从 [TiDB v8.4.0](/releases/release-8.4.0.md) 开始，`TIDB_INDEX_USAGE` 还包含聚簇表的主键，进一步提升了索引性能可见性。

### `TIDB_INDEX_USAGE` 关键指标

如需查看 `TIDB_INDEX_USAGE` 系统表字段，可执行以下 SQL 语句：

```sql
USE INFORMATION_SCHEMA;
DESC TIDB_INDEX_USAGE;
```

```sql
+--------------------------+-------------+------+------+---------+-------+
| Field                    | Type        | Null | Key  | Default | Extra |
+--------------------------+-------------+------+------+---------+-------+
| TABLE_SCHEMA             | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME               | varchar(64) | YES  |      | NULL    |       |
| INDEX_NAME               | varchar(64) | YES  |      | NULL    |       |
| QUERY_TOTAL              | bigint(21)  | YES  |      | NULL    |       |
| KV_REQ_TOTAL             | bigint(21)  | YES  |      | NULL    |       |
| ROWS_ACCESS_TOTAL        | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0      | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_0_1    | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_1_10   | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_10_20  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_20_50  | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_50_100 | bigint(21)  | YES  |      | NULL    |       |
| PERCENTAGE_ACCESS_100    | bigint(21)  | YES  |      | NULL    |       |
| LAST_ACCESS_TIME         | datetime    | YES  |      | NULL    |       |
+--------------------------+-------------+------+------+---------+-------+
共 14 行
```

关于这些列的详细说明，参见 [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)。

### 利用 `TIDB_INDEX_USAGE` 识别未使用和低效索引

本节介绍如何利用 `TIDB_INDEX_USAGE` 系统表识别未使用和低效索引。

- 未使用索引：

    - 如果 `QUERY_TOTAL = 0`，说明该索引未被任何查询使用。
    - 如果 `LAST_ACCESS_TIME` 显示的时间距今较久，说明该索引可能已无用。

- 低效索引：

    - 如果 `PERCENTAGE_ACCESS_100` 数值较大，说明存在全索引扫描，可能为低效索引。
    - 对比 `ROWS_ACCESS_TOTAL` 与 `QUERY_TOTAL`，判断索引在查询中扫描的行数是否过多。

通过 `TIDB_INDEX_USAGE` 系统表，你可以详细了解索引性能，以便移除冗余索引、优化查询执行。

### 高效使用 `TIDB_INDEX_USAGE`

以下要点可以帮助你正确理解并使用 `TIDB_INDEX_USAGE` 系统表。

#### 数据更新存在延迟

为降低性能影响，`TIDB_INDEX_USAGE` 的数据并非实时更新，索引使用指标可能会有最多 5 分钟的延迟。在分析查询时，需要考虑这一延迟。

#### 索引使用数据不持久化

`TIDB_INDEX_USAGE` 系统表的数据存储在每个 TiDB 实例的内存中，不会持久化，在节点重启后数据会丢失。

#### 跟踪历史数据

你可以定期使用以下 SQL 语句导出索引使用快照：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEX_USAGE INTO OUTFILE '/backup/index_usage_snapshot.csv';
```

通过比较不同时间的快照，可以进行历史追踪，帮助你发现索引使用趋势，从而做出更有依据的索引优化或清理决策。

## 使用 `CLUSTER_TIDB_INDEX_USAGE` 汇总全集群索引数据

由于 TiDB 是分布式 SQL 数据库，查询负载会分布于多个节点。每个 TiDB 节点独立追踪本地索引使用情况。为获得全局索引性能，TiDB 提供了 [`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) 系统表，汇总了所有节点的索引使用数据，确保在优化索引策略时充分考虑分布式查询负载。

不同 TiDB 节点的查询负载可能不同。某个索引在部分节点看似未被使用，但在其他节点可能仍然至关重要。如果要按查询负载对索引分析进行划分，执行以下 SQL 语句：

```sql
SELECT INSTANCE, TABLE_NAME, INDEX_NAME, SUM(QUERY_TOTAL) AS total_queries
FROM INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE
GROUP BY INSTANCE, TABLE_NAME, INDEX_NAME
ORDER BY total_queries DESC;
```

这样可以帮助判断一个索引是在所有节点上都未被使用，还是仅在特定节点未被使用，从而帮助你在删除索引时做出更明智的决策。

### `TIDB_INDEX_USAGE` 与 `CLUSTER_TIDB_INDEX_USAGE` 的区别

`TIDB_INDEX_USAGE` 与 `CLUSTER_TIDB_INDEX_USAGE` 的区别如下表所示：

| 功能           | `TIDB_INDEX_USAGE`                        | `CLUSTER_TIDB_INDEX_USAGE`                   |
| -------------- | ----------------------------------------- | -------------------------------------------- |
| 作用范围        | 追踪单个数据库实例内的索引使用情况                   | 汇总整个 TiDB 集群的索引使用情况                 |
| 索引追踪        | 数据为本地实例级                           | 提供集群级统一视图                           |
| 主要用途        | 调试数据库实例级的索引使用情况                         | 分析全局索引模式及多节点行为                 |

### 高效使用 `CLUSTER_TIDB_INDEX_USAGE`

由于 `CLUSTER_TIDB_INDEX_USAGE` 系统表汇总了多个节点的数据，使用时需注意以下事项：

- 数据更新存在延迟

    为将对性能的影响降到最低，`CLUSTER_TIDB_INDEX_USAGE` 不会实时更新。索引使用指标可能会有最多 5 分钟的延迟。在分析查询时，需要考虑这一延迟。

- 内存存储

    与 `TIDB_INDEX_USAGE` 一样，在节点重启后，储存在内存中的索引使用数据会丢失。

通过 `CLUSTER_TIDB_INDEX_USAGE`，可获得全局视角的索引行为，确保索引策略与分布式查询负载匹配。

## 使用 `schema_unused_indexes` 快速识别未使用索引

手动分析索引使用数据可能会非常耗时。为简化该过程，TiDB 提供了 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 系统视图，用于列出自数据库上次重启以来未被使用过的索引。

使用该视图，你可以：

- 快速识别不再使用的索引，降低不必要的存储成本。
- 通过移除无用索引，加速 DML 操作（如 `INSERT`、`UPDATE`、`DELETE`）。
- 无需手动分析查询模式，简化索引审计。

通过使用 `schema_unused_indexes`，你可以快速识别不必要的索引，轻松降低数据库开销。

### `schema_unused_indexes` 的工作原理

`schema_unused_indexes` 视图基于 `TIDB_INDEX_USAGE`，可以自动筛选出自上次 TiDB 重启以来查询次数为零的索引。

查询未使用索引：

```sql
SELECT * FROM sys.schema_unused_indexes;
```

返回类似如下结果：

```
+-----------------+---------------+--------------------+
| object_schema   | object_name   | index_name         |
+---------------- + ------------- + -------------------+
| bookshop        | users         | nickname           |
| bookshop        | ratings       | uniq_book_user_idx |
+---------------- + ------------- + -------------------+
```

### 使用 `schema_unused_indexes` 的注意事项

使用 `schema_unused_indexes` 时，需注意以下事项。

#### 仅统计自上次重启以来的未使用索引

- 如果 TiDB 节点重启，索引使用数据会被重置。
- 在使用索引数据之前，确保系统已经运行了足够长的时间，以便捕获具有代表性的业务负载。

#### 并非所有未使用索引都可立即删除

有些索引可能使用频率很低，但对于特定查询、批处理或报表任务仍然至关重要。在删除索引之前，请考虑它是否支持以下场景：

- 低频但关键的查询，如月度报表、分析任务
- 非每日运行的批处理作业
- 临时排查故障用的查询

如果索引在重要但不频繁的查询中出现，建议先保留或设为不可见。

你可以使用[不可见索引](#使用不可见索引安全测试索引移除)来安全地验证某个索引是否可以删除，而不会影响系统性能。

### 手动创建 `schema_unused_indexes` 视图

对于从较早版本升级到 TiDB v8.0.0 或更高版本的集群，需要手动创建系统 schema 及相关视图。

详见[手动创建 `schema_unused_indexes` 视图](/sys-schema/sys-schema-unused-indexes.md#手动创建-schema_unused_indexes-视图)。

## 使用不可见索引安全测试索引移除

在未经充分验证的情况下直接删除索引可能带来性能风险，尤其是那些虽不常用但对特定查询仍至关重要的索引。

为降低风险，TiDB 提供了不可见索引，可以临时禁用索引但不删除。通过使用不可见索引，你可以安全地验证索引删除决策，确保数据库优化过程更加可控和可预测。

### 什么是不可见索引？

不可见索引仍然存在于数据库中，但 TiDB 优化器会忽略它。你可以使用 [`ALTER TABLE ... INVISIBLE`](/sql-statements/sql-statement-alter-table.md) 将索引设为不可见，从而在不永久删除索引的情况下测试该索引是否真的无用。

不可见索引的主要优势如下：

- **安全测试索引**：查询将不再使用该索引，但相关的优化器统计信息仍然会被维护，必要时可随时快速恢复。
- **不影响索引存储**：索引结构未变，无需重新创建，避免额外开销。
- **性能监控**：数据库管理员可观察禁用索引后的查询表现，辅助决策。

### 设置索引为不可见

要在不删除索引的情况下使其不可见，可执行以下 SQL 语句：

```sql
ALTER TABLE bookshop.users ALTER INDEX nickname INVISIBLE;
```

设置索引为不可见后，观察系统的查询性能：

- 如果性能保持不变，说明该索引可能不必要，可以安全删除。
- 如果查询延迟增加，说明该索引可能仍有必要保留。

### 高效使用不可见索引

- **建议在业务低峰期测试**：便于在可控环境中监控对性能的影响。
- **结合查询监控工具**：对比分析索引可见与不可见时的执行计划。
- **在多种业务场景进行验证**：确保索引不被特定报表或定时任务依赖。

### 不可见索引建议保留多久？

- OLTP 负载：建议至少观察一周，覆盖日常波动。
- 批处理或 ETL 负载：建议覆盖一个完整的报表周期，如月度财务报表。
- 临时分析查询：结合查询日志确认不依赖该索引后再删除。

安全起见，建议至少保持索引在一个完整业务周期内处于不可见状态，以确保所有工作负载都已经过验证，再做最终决定。

## 索引优化的五大最佳实践

为了保持高性能和高效的资源利用，定期进行索引优化是数据库运维的常规工作。以下是 TiDB 中有效管理索引的最佳实践：

1. **定期监控索引使用。**

    - 使用 [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 和 [`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) 追踪索引使用情况。
    - 通过 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 识别未使用的索引，并评估是否可删除。
    - 监控查询执行计划，识别可能导致高 I/O 的低效索引。

2. **在删除索引前，务必进行验证。**

    - 使用 [`ALTER TABLE ... INVISIBLE`](/sql-statements/sql-statement-alter-table.md) 将索引设为不可见，临时禁用索引，观察影响后再决定是否永久删除。
    - 若查询性能保持稳定，可考虑删除索引。
    - 确保有足够的观察周期，以覆盖所有业务场景或查询模式后再做最终决策。

3. **优化现有索引。**

    - 合并冗余索引。合并冗余索引可以减少存储开销、提升写入性能。如果多个索引服务于相似的查询，可以考虑将它们合并为单个更高效的复合索引。

        - 执行以下 SQL 语句，查找前缀重叠的索引（表明可能存在冗余）：

            ```sql
            SELECT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_NAME = 'your_table'
            ORDER BY TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, SEQ_IN_INDEX;
            ```

        - 若两个索引的前导列相同，建议考虑将它们合并为复合索引。

    - 提高选择性。可以通过以下方式优化低选择性索引（即那些过滤行数过多的索引）：

        - 增加额外的列，以提升过滤效率。
        - 调整索引结构（如前缀索引、复合索引）。

    - 分析索引选择性。利用 `TIDB_INDEX_USAGE` 的 `PERCENTAGE_ACCESS_*` 字段评估索引过滤数据的效果。

4. **关注 DML 性能影响。**

    - 避免过度索引。每增加一个索引，`INSERT`、`UPDATE` 和 `DELETE` 操作的开销都会增加。
    - 仅为查询所必需的字段建立索引，以减少写入密集型负载的维护成本。

5. **定期测试与调优。**

    - 定期进行索引审计，尤其在业务负载发生重大变化后。
    - 利用 TiDB 执行计划分析工具，验证索引是否被高效使用。
    - 新增索引时，建议先在隔离环境中测试，避免出现意外的性能回退。

通过遵循以上这些最佳实践，你可以确保查询高效执行，减少不必要的存储开销，并保持数据库性能最优。
