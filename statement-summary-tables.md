---
title: Statement Summary 表
summary: 了解 TiDB 中的 Statement Summary 表。
---

# Statement Summary 表

为了更好地处理 SQL 性能问题，MySQL 在 `performance_schema` 中提供了 [statement summary 表](https://dev.mysql.com/doc/refman/8.0/en/performance-schema-statement-summary-tables.html) 来监控带有统计信息的 SQL。其中，`events_statements_summary_by_digest` 表通过其丰富的字段（如延迟、执行次数、扫描行数和全表扫描等）在定位 SQL 问题时非常有用。

因此，从 v4.0.0-rc.1 开始，TiDB 在 `information_schema` 中（_不是_ `performance_schema`）提供了与 `events_statements_summary_by_digest` 功能类似的系统表。

- [`statements_summary`](#statements_summary)
- [`statements_summary_history`](#statements_summary_history)
- [`cluster_statements_summary`](#statements_summary_evicted)
- [`cluster_statements_summary_history`](#statements_summary_evicted)
- [`statements_summary_evicted`](#statements_summary_evicted)

> **注意：**
>
> 上述表在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

本文详细介绍这些表，并说明如何使用它们来排查 SQL 性能问题。

## `statements_summary`

`statements_summary` 是 `information_schema` 中的系统表。`statements_summary` 按资源组、SQL 指纹和执行计划指纹对 SQL 语句进行分组，并为每个 SQL 类别提供统计信息。

这里的"SQL 指纹"与慢日志中使用的含义相同，是通过规范化 SQL 语句计算得出的唯一标识符。规范化过程会忽略常量、空白字符，并且不区分大小写。因此，具有一致语法的语句具有相同的指纹。例如：

{{< copyable "sql" >}}

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

规范化后，它们都属于以下类别：

{{< copyable "sql" >}}

```sql
select * from employee where id in (...) and salary between ? and ?;
```

这里的"执行计划指纹"是指通过规范化执行计划计算得出的唯一标识符。规范化过程会忽略常量。相同的 SQL 语句可能会因为执行计划不同而被分到不同的类别中。同一类别的 SQL 语句具有相同的执行计划。

`statements_summary` 存储 SQL 监控指标的聚合结果。通常，每个监控指标都包括最大值和平均值。例如，执行延迟指标对应两个字段：`AVG_LATENCY`（平均延迟）和 `MAX_LATENCY`（最大延迟）。

为确保监控指标保持最新，`statements_summary` 表中的数据会定期清除，只保留和显示最近的聚合结果。定期数据清除由 `tidb_stmt_summary_refresh_interval` 系统变量控制。如果您恰好在清除后立即查询，显示的数据可能会很少。

以下是查询 `statements_summary` 的示例输出：

```
   SUMMARY_BEGIN_TIME: 2020-01-02 11:00:00
     SUMMARY_END_TIME: 2020-01-02 11:30:00
            STMT_TYPE: Select
          SCHEMA_NAME: test
               DIGEST: 0611cc2fe792f8c146cc97d39b31d9562014cf15f8d41f23a4938ca341f54182
          DIGEST_TEXT: select * from employee where id = ?
          TABLE_NAMES: test.employee
          INDEX_NAMES: NULL
          SAMPLE_USER: root
           EXEC_COUNT: 3
          SUM_LATENCY: 1035161
          MAX_LATENCY: 399594
          MIN_LATENCY: 301353
          AVG_LATENCY: 345053
    AVG_PARSE_LATENCY: 57000
    MAX_PARSE_LATENCY: 57000
  AVG_COMPILE_LATENCY: 175458
  MAX_COMPILE_LATENCY: 175458
  ...........
              AVG_MEM: 103
              MAX_MEM: 103
              AVG_DISK: 65535
              MAX_DISK: 65535
    AVG_AFFECTED_ROWS: 0
           FIRST_SEEN: 2020-01-02 11:12:54
            LAST_SEEN: 2020-01-02 11:25:24
    QUERY_SAMPLE_TEXT: select * from employee where id=3100
     PREV_SAMPLE_TEXT:
          PLAN_DIGEST: f415b8d52640b535b9b12a9c148a8630d2c6d59e419aad29397842e32e8e5de3
                 PLAN:  Point_Get_1     root    1       table:employee, handle:3100
```

> **注意：**
>
> - 在 TiDB 中，statement summary 表中字段的时间单位是纳秒（ns），而在 MySQL 中时间单位是皮秒（ps）。
> - 从 v7.5.1 和 v7.6.0 开始，对于启用了[资源控制](/tidb-resource-control.md)的集群，`statements_summary` 将按资源组进行聚合，例如，在不同资源组中执行的相同语句将被收集为不同的记录。
## `statements_summary_history`

`statements_summary_history` 的表结构与 `statements_summary` 相同。`statements_summary_history` 保存一定时间范围内的历史数据。通过检查历史数据，您可以排查异常并比较不同时间范围的监控指标。

字段 `SUMMARY_BEGIN_TIME` 和 `SUMMARY_END_TIME` 表示历史时间范围的开始时间和结束时间。

## `statements_summary_evicted`

[`tidb_stmt_summary_max_stmt_count`](/system-variables.md#tidb_stmt_summary_max_stmt_count-new-in-v40) 系统变量限制了 `statements_summary` 和 `statements_summary_history` 表在内存中可以存储的 SQL 指纹总数。一旦超过此限制，TiDB 将从 `statements_summary` 和 `statements_summary_history` 表中淘汰最近最少使用的 SQL 指纹。

<CustomContent platform="tidb">

> **注意：**
>
> 当启用 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary) 时，`statements_summary_history` 表中的数据会持久化到磁盘。在这种情况下，`tidb_stmt_summary_max_stmt_count` 仅限制 `statements_summary` 表在内存中可以存储的 SQL 指纹数量，当超过 `tidb_stmt_summary_max_stmt_count` 时，TiDB 仅从 `statements_summary` 表中淘汰最近最少使用的 SQL 指纹。

</CustomContent>

`statements_summary_evicted` 表记录了发生淘汰的时间段以及在该时间段内淘汰的 SQL 指纹数量。此表可帮助您评估 `tidb_stmt_summary_max_stmt_count` 是否针对您的工作负载进行了适当配置。如果此表包含记录，则表明在某个时间点 SQL 指纹数量超过了 `tidb_stmt_summary_max_stmt_count`。

<CustomContent platform="tidb">

在 [TiDB Dashboard 的 SQL 语句页面](/dashboard/dashboard-statement-list.md#others)中，被淘汰语句的信息显示在 `Others` 行中。

</CustomContent>

<CustomContent platform="tidb-cloud">

在[诊断页面的 SQL 语句标签页](/tidb-cloud/tune-performance.md#statement-analysis)中，被淘汰语句的信息显示在 `Others` 行中。

</CustomContent>

## statement summary 的集群表

`statements_summary`、`statements_summary_history` 和 `statements_summary_evicted` 表仅显示单个 TiDB 服务器的 statement summary。要查询整个集群的数据，您需要查询 `cluster_statements_summary`、`cluster_statements_summary_history` 或 `cluster_statements_summary_evicted` 表。

`cluster_statements_summary` 显示每个 TiDB 服务器的 `statements_summary` 数据。`cluster_statements_summary_history` 显示每个 TiDB 服务器的 `statements_summary_history` 数据。`cluster_statements_summary_evicted` 显示每个 TiDB 服务器的 `statements_summary_evicted` 数据。这些表使用 `INSTANCE` 字段表示 TiDB 服务器的地址。其他字段与 `statements_summary`、`statements_summary_history` 和 `statements_summary_evicted` 中的字段相同。
## 参数配置

以下系统变量用于控制 statement summary：

- `tidb_enable_stmt_summary`：确定是否启用 statement summary 功能。`1` 表示启用，`0` 表示禁用。默认启用此功能。如果禁用此功能，系统表中的统计信息将被清除。下次启用此功能时，统计信息将重新计算。测试表明启用此功能对性能影响很小。
- `tidb_stmt_summary_refresh_interval`：`statements_summary` 表刷新的时间间隔。时间单位为秒（s）。默认值为 `1800`。
- `tidb_stmt_summary_history_size`：`statements_summary_history` 表中存储的每个 SQL 语句类别的大小，也是 `statements_summary_evicted` 表中的最大记录数。默认值为 `24`。
- `tidb_stmt_summary_max_stmt_count`：限制 `statements_summary` 和 `statements_summary_history` 表在内存中可以存储的 SQL 指纹总数。默认值为 `3000`。

    一旦超过此限制，TiDB 将从 `statements_summary` 和 `statements_summary_history` 表中淘汰最近最少使用的 SQL 指纹。这些被淘汰的指纹随后会在 [`statements_summary_evicted`](#statements_summary_evicted) 表中计数。

    > **注意：**
    >
    > - 当一个 SQL 指纹被淘汰时，其在 `statements_summary` 和 `statements_summary_history` 表中所有时间范围的相关汇总数据都会被移除。因此，即使特定时间范围内的 SQL 指纹数量未超过限制，`statements_summary_history` 表中的 SQL 指纹数量可能少于实际的 SQL 指纹数量。如果出现这种情况并影响性能，建议增加 `tidb_stmt_summary_max_stmt_count` 的值。
    > - 对于 TiDB Self-Managed，当启用 [`tidb_stmt_summary_enable_persistent`](#persist-statements-summary) 时，`statements_summary_history` 表中的数据会持久化到磁盘。在这种情况下，`tidb_stmt_summary_max_stmt_count` 仅限制 `statements_summary` 表在内存中可以存储的 SQL 指纹数量，当超过 `tidb_stmt_summary_max_stmt_count` 时，TiDB 仅从 `statements_summary` 表中淘汰最近最少使用的 SQL 指纹。

- `tidb_stmt_summary_max_sql_length`：指定 `DIGEST_TEXT` 和 `QUERY_SAMPLE_TEXT` 的最长显示长度。默认值为 `4096`。
- `tidb_stmt_summary_internal_query`：确定是否统计 TiDB SQL 语句。`1` 表示统计，`0` 表示不统计。默认值为 `0`。

以下是 statement summary 配置的示例：

{{< copyable "sql" >}}

```sql
set global tidb_stmt_summary_max_stmt_count = 3000;
set global tidb_enable_stmt_summary = true;
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

在上述配置生效后，`statements_summary` 表每 30 分钟清除一次，`statements_summary_history` 表最多存储 3000 种 SQL 语句。对于每种类型，`statements_summary_history` 表存储最近 24 个时间段的数据。`statements_summary_evicted` 表记录最近 24 个发生 SQL 语句淘汰的时间段。`statements_summary_evicted` 表每 30 分钟更新一次。

> **注意：**
>
> - 如果一个 SQL 类型每分钟都出现，则 `statements_summary_history` 存储最近 12 小时的数据。如果一个 SQL 类型每天只在 00:00 到 00:30 出现，则 `statements_summary_history` 存储最近 24 个时间段的数据，每个时间段为 1 天。因此，对于这个 SQL 类型，`statements_summary_history` 存储最近 24 天的数据。
> - `tidb_stmt_summary_history_size`、`tidb_stmt_summary_max_stmt_count` 和 `tidb_stmt_summary_max_sql_length` 配置项会影响内存使用。建议您根据需求、SQL 大小、SQL 数量和机器配置来调整这些配置。不建议设置过大的值。您可以使用 `tidb_stmt_summary_history_size` \* `tidb_stmt_summary_max_stmt_count` \* `tidb_stmt_summary_max_sql_length` \* `3` 来计算内存使用量。
### 为 statement summary 设置合适的大小

系统运行一段时间后（取决于系统负载），您可以检查 `statement_summary` 表以查看是否发生了 SQL 淘汰。例如：

```sql
select @@global.tidb_stmt_summary_max_stmt_count;
select count(*) from information_schema.statements_summary;
```

```sql
+-------------------------------------------+
| @@global.tidb_stmt_summary_max_stmt_count |
+-------------------------------------------+
| 3000                                      |
+-------------------------------------------+
1 row in set (0.001 sec)

+----------+
| count(*) |
+----------+
|     3001 |
+----------+
1 row in set (0.001 sec)
```

您可以看到 `statements_summary` 表已经充满记录。然后从 `statements_summary_evicted` 表中检查被淘汰的数据：

```sql
select * from information_schema.statements_summary_evicted;
```

```sql
+---------------------+---------------------+---------------+
| BEGIN_TIME          | END_TIME            | EVICTED_COUNT |
+---------------------+---------------------+---------------+
| 2020-01-02 16:30:00 | 2020-01-02 17:00:00 |            59 |
+---------------------+---------------------+---------------+
| 2020-01-02 16:00:00 | 2020-01-02 16:30:00 |            45 |
+---------------------+---------------------+---------------+
2 row in set (0.001 sec)
```

从上述结果可以看出，最多有 59 个 SQL 类别被淘汰。在这种情况下，建议您至少增加 59 条记录的 `statement_summary` 表大小，这意味着将大小增加到至少 3059 条记录。
