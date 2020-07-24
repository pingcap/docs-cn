---
title: Use TiFlash
aliases: ['/docs/dev/tiflash/use-tiflash/','/docs/dev/reference/tiflash/use-tiflash/']
---

# Use TiFlash

After TiFlash is deployed, data replication does not automatically begin. You need to manually specify the tables to be replicated.

You can either use TiDB to read TiFlash replicas for medium-scale analytical processing, or use TiSpark to read TiFlash replicas for large-scale analytical processing, which is based on your own needs. See the following sections for details:

- [Use TiDB to read TiFlash replicas](#use-tidb-to-read-tiflash-replicas)
- [Use TiSpark to read TiFlash replicas](#use-tispark-to-read-tiflash-replicas)

## Create TiFlash replicas for tables

After TiFlash is connected to the TiKV cluster, data replication by default does not begin. You can send a DDL statement to TiDB through a MySQL client to create a TiFlash replica for a specific table:

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count
```

The parameter of the above command is described as follows:

- `count` indicates the number of replicas. When the value is `0`, the replica is deleted.

If you execute multiple DDL statements on a same table, only the last statement is ensured to take effect. In the following example, two DDL statements are executed on the table `tpch50`, but only the second statement (to delete the replica) takes effect.

Create two replicas for the table:

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2
```

Delete the replica:

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0
```

**Notes:**

* If the table `t` is replicated to TiFlash through the above DDL statements, the table created using the following statement will also be automatically replicated to TiFlash:

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE table_name like t
    ```

* For the current version, if you create the TiFlash replica before using TiDB Lightning to import the data, the data import will fail. You must import data to the table before creating the TiFlash replica for the table.

* It is recommended that you do not replicate more than 1,000 tables because this lowers the PD scheduling performance. This limit will be removed in later versions.

## Check the replication progress

You can check the status of the TiFlash replicas of a specific table using the following statement. The table is specified using the `WHERE` clause. If you remove the `WHERE` clause, you will check the replica status of all tables.

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>'
```

In the result of above statement:

* `AVAILABLE` indicates whether the TiFlash replicas of this table is available or not. `1` means available and `0` means unavailable. Once the replicas become available, this status does not change. If you use DDL statements to modify the number of replicas, the replication status will be recalculated.
* `PROGRESS` means the progress of the replication. The value is between `0.0` and `1.0`. `1` means at least one replica is replicated.

## Use TiDB to read TiFlash replicas

TiDB provides three ways to read TiFlash replicas. If you have added a TiFlash replica without any engine configuration, the CBO (cost-based optimization) mode is used by default.

### Smart selection

For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use TiFlash replicas based on the cost estimation. You can use the `desc` or `explain analyze` statement to check whether or not a TiFlash replica is selected. For example:

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
|   └─TableFullScan_16     | 1.00    | 1       | cop[tiflash] | table:t       | time:43ms, loops:1                                                   | keep order:false, stats:pseudo | N/A       | N/A  |
+--------------------------+---------+---------+--------------+---------------+----------------------------------------------------------------------+--------------------------------+-----------+------+
```

`cop[tiflash]` means that the task will be sent to TiFlash for processing. If you have not selected a TiFlash replica, you can try to update the statistics using the `analyze table` statement, and then check the result using the `explain analyze` statement.

Note that if a table has only a single TiFlash replica and the related node cannot provide service, queries in the CBO mode will repeatedly retry. In this situation, you need to specify the engine or use the manual hint to read data from the TiKV replica.

### Engine isolation

Engine isolation is to specify that all queries use a replica of the specified engine by configuring the corresponding variable. The optional engines are "tikv", "tidb" (indicates the internal memory table area of TiDB, which stores some TiDB system tables and cannot be actively used by users), and "tiflash", with the following two configuration levels:

* TiDB instance-level, namely, INSTANCE level. Add the following configuration item in the TiDB configuration file:

    ```
    [isolation-read]
    engines = ["tikv", "tidb", "tiflash"]
    ```

    **The INSTANCE-level default configuration is `["tikv", "tidb", "tiflash"]`.**

* SESSION level. Use the following statement to configure:

    {{< copyable "sql" >}}

    ```sql
    set @@session.tidb_isolation_read_engines = "engine list separated by commas";
    ```

    or

    {{< copyable "sql" >}}

    ```sql
    set SESSION tidb_isolation_read_engines = "engine list separated by commas";
    ```

    The default configuration of the SESSION level inherits from the configuration of the TiDB INSTANCE level.

The final engine configuration is the session-level configuration, that is, the session-level configuration overrides the instance-level configuration. For example, if you have configured "tikv" in the INSTANCE level and "tiflash" in the SESSION level, then the TiFlash replicas are read. If the final engine configuration is "tikv" and "tiflash", then the TiKV and TiFlash replicas are both read, and the optimizer automatically selects a better engine to execute.

> **Note:**
>
> Because [TiDB Dashboard](/dashboard/dashboard-intro.md) and other components need to read some system tables stored in the TiDB memory table area, it is recommended to always add the "tidb" engine to the instance-level engine configuration.

If the queried table does not have a replica of the specified engine (for example, the engine is configured as "tiflash" but the table does not have a TiFlash replica), the query returns an error.

### Manual hint

Manual hint can force TiDB to use specified replicas for specific table(s) on the premise of satisfying engine isolation. Here is an example of using the manual hint:

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

If you set an alias to a table in a query statement, you must use the alias in the statement that includes a hint for the hint to take effect. For example:

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[alias_a,alias_b]) */ ... from table_name_1 as alias_a, table_name_2 as alias_b where alias_a.column_1 = alias_b.column_2;
```

In the above statements, `tiflash[]` prompts the optimizer to read the TiFlash replicas. You can also use `tikv[]` to prompt the optimizer to read the TiKV replicas as needed. For hint syntax details, refer to [READ_FROM_STORAGE](/optimizer-hints.md#read_from_storagetiflasht1_name--tl_name--tikvt2_name--tl_name-).

If the table specified by a hint does not have a replica of the specified engine, the hint is ignored and a warning is reported. In addition, a hint only takes effect on the premise of engine isolation. If the engine specified in a hint is not in the engine isolation list, the hint is also ignored and a warning is reported.

> **Note:**
>
> The MySQL client of 5.7.7 or earlier versions clears optimizer hints by default. To use the hint syntax in these early versions, start the client with the `--comments` option, for example, `mysql -h 127.0.0.1 -P 4000 -uroot --comments`.

### The relationship of smart selection, engine isolation, and manual hint

In the above three ways of reading TiFlash replicas, engine isolation specifies the overall range of available replicas of engines; within this range, manual hint provides statement-level and table-level engine selection that is more fine-grained; finally, CBO makes the decision and selects a replica of an engine based on cost estimation within the specified engine list.

> **Note:**
>
> Before v4.0.3, the behavior of reading from TiFlash replica in a non-read-only SQL statement (for example, `INSERT INTO ... SELECT`, `SELECT ... FOR UPDATE`, `UPDATE ...`, `DELETE ...`) is undefined. In v4.0.3 and later versions, internally TiDB ignores the TiFlash replica for a non-read-only SQL statement to guarantee the data correctness. That is, for [smart selection](#smart-selection), TiDB automatically chooses the non-TiFlash replica; for [engine isolation](#engine-isolation) that specifies TiFlash replica **only**, TiDB reports an error; and for [manual hint](#manual-hint), TiDB ignores the hint.

## Use TiSpark to read TiFlash replicas

Currently, you can use TiSpark to read TiFlash replicas in a method similar to the engine isolation in TiDB. This method is to configure the `spark.tispark.use.tiflash` parameter to `true` (or `false`).

> **Notes**
>
> When this parameter is set to `true`, only the TiFlash replicas of all tables involved in the query are read and these tables must have TiFlash replicas; for tables that do not have TiFlash replicas, an error is reported. When this parameter is set to `false`, only the TiKV replica is read.

You can configure this parameter in either of the following ways:

* Add the following item in the `spark-defaults.conf` file:

    ```
    spark.tispark.use.tiflash true
    ```

* Add `--conf spark.tispark.use.tiflash=true` in the initialization command when initializing Spark shell or Thrift server.

* Set `spark.conf.set("spark.tispark.use.tiflash", true)` in Spark shell in a real-time manner.

* Set `set spark.tispark.use.tiflash=true` in Thrift server after the server is connected via beeline.

## Supported push-down calculations

> **Note:**
>
> Before v4.0.2, TiDB does not support the new framework for collations, so in those previous versions, if you enable the [new framework for collations](/character-set-and-collation.md#new-framework-for-collations), none of the expressions can be pushed down. This restriction is removed in v4.0.2 and later versions.

TiFlash mainly supports predicate and aggregate push-down calculations. Push-down calculations can help TiDB perform distributed acceleration. Currently, table joins and `DISTINCT COUNT` are not the supported calculation types, which will be optimized in later versions.

Currently, TiFlash supports pushing down a limited number of expressions. To learn the supported expressions, refer to [expression list](https://github.com/pingcap/tidb/blob/692e0098b1207ef26ea18bedfcc9ba067604da3c/expression/expression.go#L1115).

TiFlash does not support push-down calculations in the following situations:

- Expressions that contain `Duration` and `JSON` cannot be pushed down.
- If an aggregate function or a `WHERE` clause contains expressions that are not in [this list](https://github.com/pingcap/tidb/blob/692e0098b1207ef26ea18bedfcc9ba067604da3c/expression/expression.go#L1115), the aggregate or related predicate filtering cannot be pushed down.

If a query encounters unsupported push-down calculations, TiDB needs to complete the remaining calculations, which might greatly affect the TiFlash acceleration effect.
