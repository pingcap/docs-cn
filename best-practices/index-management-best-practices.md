---
title: 管理索引和识别未使用索引的最佳实践
summary: 了解在 TiDB 中管理和优化索引、识别并移除未使用索引的最佳实践。
---

# 理索引和识别未使用索引的最佳实践

索引对于优化数据库查询性能至关重要，可以减少全表扫描的数据量。然而，随着应用演进、业务逻辑变化和数据量增长，原有的索引设计也会遇到问题，包括：

- 未使用索引：这些索引曾经有用，但现在查询优化器已不再选择它们，导致占用存储空间并增加写入操作的额外开销。
- 低效索引：某些索引虽然被优化器使用，但扫描的数据量远超预期，增加磁盘 I/O 并拖慢查询速度。

如果不及时处理，索引问题会导致存储成本上升、性能下降和运维效率降低。在 TiDB 这样的分布式 SQL 数据库中，索引效率问题影响更大，因为分布式查询和多节点协作更为复杂。因此，定期进行索引审计对于保持数据库优化至关重要。

主动识别和优化索引有助于：

- 降低存储开销：移除未使用索引可释放磁盘空间，降低长期存储成本。
- 提升写入性能：写密集型场景（如 `INSERT`、`UPDATE`、`DELETE`）在减少不必要索引维护后，性能更佳。
- 优化查询执行：高效索引能够减少扫描行数，加快查询速度和响应时间。
- 简化数据库管理：减少并优化索引后，可以简化备份、恢复和数据库变更。

由于索引会随业务逻辑变化而演进，定期索引审计是数据库维护的标准流程。TiDB 提供内置可观测性手段，帮助你安全高效地观测、评估和优化索引。

TiDB v8.0.0 引入了 [`INFORMATION_SCHEMA.TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 表和 [`sys.schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 视图，帮助你追踪索引使用情况，根据运行数据做出正确判断。

本文介绍如何利用这些工具检测并移除未使用或低效索引，从而提升 TiDB 性能与稳定性。

## TiDB 索引优化：数据驱动的方法

索引对查询性能至关重要，但如果没有充分分析就移除，可能导致性能回退甚至系统不稳定。为确保索引管理的安全与有效，TiDB 提供内置可观测性手段，支持以下操作：

- 实时追踪索引使用：识别索引访问频率及其对性能的贡献。
- 检测未使用索引：定位自上次数据库重启后未被使用的索引。
- 评估索引效率：判断索引是否有效过滤数据，或带来过多 I/O 开销。
- 安全测试索引移除：可先将索引暂时设为不可见，确保无查询依赖后再删除。

TiDB 通过以下手段简化索引优化：

- `INFORMATION_SCHEMA.TIDB_INDEX_USAGE`：监控索引使用模式和查询频率。
- `sys.schema_unused_indexes`：列出自数据库上次重启后未被使用的索引。
- 不可见索引：可在删除前测试移除索引的影响。

借助这些可观测性工具，你可以放心清理冗余索引，避免性能下降风险。

## 使用 `TIDB_INDEX_USAGE` 追踪索引使用情况

从 [TiDB v8.0.0](/releases/release-8.0.0.md) 开始，你可以使用 `TIDB_INDEX_USAGE` 系统表实时观测索引使用情况，帮助你优化查询性能并移除不必要的索引。

具体来说，你可以通过 `TIDB_INDEX_USAGE` 进行以下操作：

- 检测未使用索引：识别未被查询访问的索引，判断是否可安全移除。
- 分析索引效率：追踪索引使用频率及其对查询执行的贡献。
- 评估查询模式：了解索引对读操作、数据扫描和 KV 请求的影响。

从 [TiDB v8.4.0](/releases/release-8.4.0.md) 开始，`TIDB_INDEX_USAGE` 还包含聚簇表的主键，进一步提升索引性能可见性。

### `TIDB_INDEX_USAGE` 关键指标

如需查看 `TIDB_INDEX_USAGE` 表字段，可执行以下 SQL 语句：

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

各字段说明，请详见 [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md)。

### 利用 `TIDB_INDEX_USAGE` 识别未使用和低效的索引

本节介绍如何利用 `TIDB_INDEX_USAGE` 系统表识别未使用和低效的索引。

- 未使用索引：

    - `QUERY_TOTAL = 0` 表示该索引未被任何查询使用。
    - `LAST_ACCESS_TIME` 距今较久，说明索引可能已无用。

- 低效索引：

    - `PERCENTAGE_ACCESS_100` 数值较大，说明存在全索引扫描，可能为低效索引。
    - 对比 `ROWS_ACCESS_TOTAL` 与 `QUERY_TOTAL`，判断索引每次使用时扫描的行数是否过多。

通过 `TIDB_INDEX_USAGE`，你可详细了解索引性能，便于移除冗余索引、优化查询执行。

### 高效使用 `TIDB_INDEX_USAGE`

以下要点可以帮助你正确理解并使用 `TIDB_INDEX_USAGE` 系统表。

#### 数据更新有延迟

为降低性能影响，`TIDB_INDEX_USAGE` 的数据并非实时更新，索引使用指标可能会有最多 5 分钟的延迟。在分析查询时请注意这一时效性。

#### 索引使用数据不持久化

`TIDB_INDEX_USAGE` 数据存储于每个 TiDB 实例的内存中，不会持久化，在节点重启后数据会丢失。

#### 跟踪历史数据

你可以定期导出索引使用快照：

```sql
SELECT * FROM INFORMATION_SCHEMA.TIDB_INDEX_USAGE INTO OUTFILE '/backup/index_usage_snapshot.csv';
```

通过对比快照，可以跟踪索引使用趋势，辅助决策。

## 使用 `CLUSTER_TIDB_INDEX_USAGE` 汇总全集群索引数据

TiDB 为分布式 SQL 数据库，查询负载分布于多个节点。每个节点独立追踪本地索引使用。若需全局视角，TiDB 提供 [`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) 系统表，汇总所有节点的索引使用数据，便于优化分布式环境下的索引策略。

不同的 TiDB 节点的查询负载可能不同。某索引在部分节点未用，但在其他节点可能至关重要。你可以使用如下 SQL 按实例分组分析：

```sql
SELECT INSTANCE, TABLE_NAME, INDEX_NAME, SUM(QUERY_TOTAL) AS total_queries
FROM INFORMATION_SCHEMA.CLUSTER_TIDB_INDEX_USAGE
GROUP BY INSTANCE, TABLE_NAME, INDEX_NAME
ORDER BY total_queries DESC;
```

帮助判断索引是否在所有节点都未用，辅助安全移除。

### `TIDB_INDEX_USAGE` 与 `CLUSTER_TIDB_INDEX_USAGE` 的区别

`TIDB_INDEX_USAGE` 与 `CLUSTER_TIDB_INDEX_USAGE` 的区别如下表所示。

| 功能           | `TIDB_INDEX_USAGE`                        | `CLUSTER_TIDB_INDEX_USAGE`                   |
| -------------- | ----------------------------------------- | -------------------------------------------- |
| 作用范围        | 单一数据库实例内索引使用                    | 汇总整个 TiDB 集群的索引使用                 |
| 索引追踪        | 数据为本地实例级                           | 提供集群级统一视图                           |
| 主要用途        | 实例级调试索引使用                         | 分析全局索引模式及多节点行为                 |

### 高效使用 `CLUSTER_TIDB_INDEX_USAGE`

由于 `CLUSTER_TIDB_INDEX_USAGE` 系统表汇总了多个节点的数据，使用时请注意以下事项：

- 数据更新有延迟

    为将对性能的影响降到最低，`CLUSTER_TIDB_INDEX_USAGE` 不会实时更新。索引使用数据更新可能延迟最多 5 分钟。在分析查询时候请注意该延时。

- 内存存储

    与 `TIDB_INDEX_USAGE` 一样，在节点重启后，储存在内存中的索引使用数据会丢失。

通过 `CLUSTER_TIDB_INDEX_USAGE`，可获得全局索引行为视角，确保索引策略与分布式负载匹配。

## 使用 `schema_unused_indexes` 快速识别未使用索引

手动分析索引使用数据较为繁琐。为简化该流程，TiDB 提供了 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 视图，自动列出自上次数据库重启后未被使用的索引。

使用该功能，你可以：

- 快速识别不再使用的索引，降低存储成本。
- 通过移除无用索引，加速 DML 操作（如 `INSERT`、`UPDATE`、`DELETE`）。
- 无需手动分析查询模式，简化索引审计。

通过使用 `schema_unused_indexes`，你可以快速识别不必要的索引，轻松降低数据库开销。

### `schema_unused_indexes` 的工作原理

`schema_unused_indexes` 视图基于 `TIDB_INDEX_USAGE`，可以自动筛选出自上次 TiDB 重启后查询次数为零的索引。

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

使用 `schema_unused_indexes` 时，注意以下事项。

#### 仅统计自上次重启以来未用索引

- TiDB 节点重启后，使用数据会被重置。
- 建议系统运行一段时间，确保捕获到有代表性的业务负载后再参考该数据。

#### 并非所有未用索引都可立即删除

部分索引虽很少用，但对特定查询、批处理或报表任务仍然重要。删除索引前，请确认该索引是否支持以下功能：

- 低频但关键的查询，如月度报表、分析任务
- 非每日运行的批处理作业
- 临时排查用的查询

如索引仅在重要但不频繁的查询中出现，建议先保留或设为不可见。

你可以使用[不可见索引](#使用不可见索引安全移除测试索引)先进行测试。

### 手动创建 `schema_unused_indexes` 视图

如从旧版本升级到 TiDB v8.0.0 及以上，需手动创建系统 schema 及相关视图。

详见[手动创建 `schema_unused_indexes` 视图](/sys-schema/sys-schema-unused-indexes.md#manually-create-the-schema_unused_indexes-view)。

## 使用不可见索引安全移除测试索引

直接删除索引可能带来性能风险，尤其是那些虽不常用但对特定查询仍关键的索引。

为降低风险，TiDB 支持不可见索引，可以临时禁用索引但不删除。这样你可安全验证移除决策，确保数据库优化过程更可控。

### 什么是不可见索引？

不可见索引仍保留在数据库中，但优化器会忽略它。你可以使用 [`ALTER TABLE ... INVISIBLE`](/sql-statements/sql-statement-alter-table.md) 将索引设为不可见，测试其是否真的无用。

不可见索引有如下优势：

- **安全测试**：查询不再使用该索引，相关优化器统计信息仍旧会被维护，若需恢复可随时快速还原。
- **对索引存储无影响**：索引结构未变，无需重建。
- **性能监控**：可观察禁用索引后的查询表现，辅助决策。

### 设置索引为不可见

示例 SQL：

```sql
ALTER TABLE bookshop.users ALTER INDEX nickname INVISIBLE;
```

设置后，观察系统查询性能：

- 若性能无明显变化，说明你可以安全移除该索引。
- 若查询延迟上升，说明该索引仍有必要保留。

### 高效使用不可见索引

- **建议在业务低峰期测试**：便于在可控环境中监控对性能的影响。
- **结合查询监控工具**：对比索引可见与不可见时的执行计划。
- **覆盖多种业务场景**：确保索引不被特殊报表或定时任务依赖。

### 不可见索引建议保留多久？

- OLTP 负载：建议至少观察一周，覆盖日常波动。
- 批处理或 ETL 负载：建议覆盖完整报表周期，如月度财务报表。
- 临时分析查询：结合查询日志确认无依赖后再删除。

为安全起见，建议至少覆盖一个完整业务周期后再做最终决策。

## 索引优化五大最佳实践

为保持高性能和资源高效，索引优化应成为数据库维护的常规工作。TiDB 索引管理建议如下：

1. **定期监控索引使用**

    - 利用 [`TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md) 和 [`CLUSTER_TIDB_INDEX_USAGE`](/information-schema/information-schema-tidb-index-usage.md#cluster_tidb_index_usage) 追踪索引活动。
    - 通过 [`schema_unused_indexes`](/sys-schema/sys-schema-unused-indexes.md) 识别未用索引，评估是否可移除。
    - 监控查询执行计划，发现可能导致高 I/O 的低效索引。

2. **移除索引前务必验证**

    - 使用 [`ALTER TABLE ... INVISIBLE`](/sql-statements/sql-statement-alter-table.md) 将索引设为暂时不可见，观察影响后再决定是否永久删除。
    - 若查询性能稳定，可考虑移除索引。
    - 观察期应覆盖所有业务场景，确保安全。

3. **优化现有索引**

    - 合并冗余索引，减少存储和写入开销。若多个索引服务类似查询，可合并为更高效的复合索引。

        - 查找前缀重叠的索引，可执行：

            ```sql
            SELECT TABLE_SCHEMA, TABLE_NAME, INDEX_NAME, COLUMN_NAME, SEQ_IN_INDEX
            FROM INFORMATION_SCHEMA.STATISTICS
            WHERE TABLE_NAME = 'your_table'
            ORDER BY TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, SEQ_IN_INDEX;
            ```

        - 若两个索引前导列相同，建议合并为复合索引。

    - 提高选择性。可以通过以下方式优化低选择性索引（即那些过滤行数过多的索引）：

        - 增加额外的列，以提升过滤效率。
        - 调整索引结构（如前缀索引、复合索引）。

    - 利用 `TIDB_INDEX_USAGE` 的 `PERCENTAGE_ACCESS_*` 字段分析索引选择性。

4. **关注 DML 性能影响**

    - 避免过度索引。每增加一个索引，`INSERT`、`UPDATE`、`DELETE` 的维护成本都会上升。
    - 仅为查询必要字段建索引，降低写入负担。

5. **定期测试与调优**

    - 定期进行索引审计，尤其在业务负载变化后。
    - 利用 TiDB 执行计划分析工具，验证索引是否被高效使用。
    - 新增索引建议先在隔离环境测试，避免性能回退。

遵循以上最佳实践，可确保查询高效、存储开销最小、数据库性能最优。
