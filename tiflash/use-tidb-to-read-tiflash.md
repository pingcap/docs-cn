---
title: 使用 TiDB 读取 TiFlash 副本
summary: 了解如何使用 TiDB 读取 TiFlash 副本。
---

# 使用 TiDB 读取 TiFlash 副本

本文介绍如何使用 TiDB 读取 TiFlash 副本。

TiDB 提供三种方式来读取 TiFlash 副本。如果你添加了 TiFlash 副本但没有任何引擎配置，默认使用 CBO（基于成本的优化）模式。

## 智能选择

对于有 TiFlash 副本的表，TiDB 优化器会根据成本估算自动决定是否使用 TiFlash 副本。你可以使用 `desc` 或 `explain analyze` 语句来检查是否选择了 TiFlash 副本。例如：

{{< copyable "sql" >}}

```sql
desc select count(*) from test.t;
```

```
+--------------------------+---------+--------------+---------------+--------------------------------+
| id                       | estRows | task         | access object | operator info                  |
+--------------------------+---------+--------------+---------------+--------------------------------+
| StreamAgg_9              | 1.00    | root         |               | funcs:count(1)->Column#4       |
| └─TableReader_17         | 1.00    | root         |               | data:TableFullScan_16          |
|   └─TableFullScan_16     | 1.00    | cop[tiflash] | table:t       | keep order:false, stats:pseudo |
+--------------------------+---------+--------------+---------------+--------------------------------+
3 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
explain analyze select count(*) from test.t;
```

```
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| id                       | estRows | actRows | task         | access object | execution info                                                       | operator info                  | memory    | disk |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
| StreamAgg_9              | 1.00    | 1       | root         |               | time:83.8372ms, loops:2                                              | funcs:count(1)->Column#4       | 372 Bytes | N/A  |
| └─TableReader_17         | 1.00    | 1       | root         |               | time:83.7776ms, loops:2, rpc num: 1, rpc time:83.5701ms, proc keys:0 | data:TableFullScan_16          | 152 Bytes | N/A  |
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | tiflash_task:{time:43ms, loops:1, threads:1}, tiflash_scan:{...}     | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` 表示该任务将被发送到 TiFlash 进行处理。如果你没有选择 TiFlash 副本，可以尝试使用 `analyze table` 语句更新统计信息，然后使用 `explain analyze` 语句检查结果。

注意，如果一个表只有一个 TiFlash 副本且相关节点无法提供服务，CBO 模式下的查询将重复重试。在这种情况下，你需要指定引擎或使用手动提示来从 TiKV 副本读取数据。

## 引擎隔离

引擎隔离是通过配置相应变量来指定所有查询使用指定引擎的副本。可选的引擎包括 "tikv"、"tidb"（表示 TiDB 的内部内存表区域，用于存储一些 TiDB 系统表，用户不能主动使用）和 "tiflash"。

<CustomContent platform="tidb">

你可以在以下两个配置级别指定引擎：

* TiDB 实例级别，即 INSTANCE 级别。在 TiDB 配置文件中添加以下配置项：

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **INSTANCE 级别的默认配置是 `["tikv", "tidb", "tiflash"]`。**

* SESSION 级别。使用以下语句进行配置：

    {{< copyable "sql" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "以逗号分隔的引擎列表";
    ```

    或

    {{< copyable "sql" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "以逗号分隔的引擎列表";
    ```

    SESSION 级别的默认配置继承自 TiDB INSTANCE 级别的配置。

最终的引擎配置是会话级别的配置，即会话级别的配置会覆盖实例级别的配置。例如，如果你在 INSTANCE 级别配置了 "tikv"，在 SESSION 级别配置了 "tiflash"，那么将读取 TiFlash 副本。如果最终的引擎配置是 "tikv" 和 "tiflash"，那么会同时读取 TiKV 和 TiFlash 副本，优化器会自动选择更好的引擎来执行。

> **注意：**
>
> 因为 [TiDB Dashboard](/dashboard/dashboard-intro.md) 和其他组件需要读取存储在 TiDB 内存表区域的一些系统表，建议始终在实例级别的引擎配置中添加 "tidb" 引擎。

</CustomContent>

<CustomContent platform="tidb-cloud">

你可以使用以下语句指定引擎：

```sql
set @@session.tidb_isolation_read_engines = "以逗号分隔的引擎列表";
```

或

```sql
set SESSION tidb_isolation_read_engines = "以逗号分隔的引擎列表";
```

</CustomContent>

如果查询的表没有指定引擎的副本（例如，引擎配置为 "tiflash" 但表没有 TiFlash 副本），查询将返回错误。

## 手动提示

手动提示可以在满足引擎隔离的前提下强制 TiDB 对特定表使用指定的副本。以下是使用手动提示的示例：

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

如果你在查询语句中为表设置了别名，你必须在包含提示的语句中使用别名才能使提示生效。例如：

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

在上述语句中，`tiflash[]` 提示优化器读取 TiFlash 副本。你也可以根据需要使用 `tikv[]` 提示优化器读取 TiKV 副本。有关提示语法的详细信息，请参考 [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-)。

如果提示指定的表没有指定引擎的副本，提示将被忽略并报告警告。此外，提示只在引擎隔离的前提下生效。如果提示中指定的引擎不在引擎隔离列表中，提示也会被忽略并报告警告。

> **注意：**
>
> 5.7.7 或更早版本的 MySQL 客户端默认会清除优化器提示。要在这些早期版本中使用提示语法，请使用 `--comments` 选项启动客户端，例如，`mysql -h 127.0.0.1 -P 4000 -uroot --comments`。

## 智能选择、引擎隔离和手动提示的关系

在上述三种读取 TiFlash 副本的方式中，引擎隔离指定了可用引擎副本的整体范围；在此范围内，手动提示提供了更细粒度的语句级和表级引擎选择；最后，CBO 在指定的引擎列表内基于成本估算做出决策并选择一个引擎的副本。

> **注意：**
>
> - 在 v4.0.3 之前，在非只读 SQL 语句中读取 TiFlash 副本的行为是未定义的（例如，`INSERT INTO ... SELECT`、`SELECT ... FOR UPDATE`、`UPDATE ...`、`DELETE ...`）。
> - 从 v4.0.3 到 v6.2.0 版本，为了保证数据正确性，TiDB 在内部忽略非只读 SQL 语句的 TiFlash 副本。也就是说，对于[智能选择](#智能选择)，TiDB 自动选择非 TiFlash 副本；对于仅指定 TiFlash 副本的[引擎隔离](#引擎隔离)，TiDB 报错；对于[手动提示](#手动提示)，TiDB 忽略提示。
> - 从 v6.3.0 到 v7.0.0 版本，如果启用了 TiFlash 副本，你可以使用 [`tidb_enable_tiflash_read_for_write_stmt`](/system-variables.md#tidb_enable_tiflash_read_for_write_stmt-new-in-v630) 变量来控制 TiDB 是否在非只读 SQL 语句中使用 TiFlash 副本。
> - 从 v7.1.0 开始，如果启用了 TiFlash 副本且当前会话的 [SQL 模式](/sql-mode.md)不是严格模式（即 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 或 `STRICT_ALL_TABLES`），TiDB 会根据成本估算自动决定是否在非只读 SQL 语句中使用 TiFlash 副本。
