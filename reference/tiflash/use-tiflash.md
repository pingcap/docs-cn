---
title: Use TiFlash
category: reference
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

* TiFlash reserves the `system` database. You cannot create TiFlash replicas for the table in the database named `system` in TiDB. If you forcibly create such TiFlash replica, the result will be an undefined behavior (a temporary restriction).

## Check the replication progress

You can check the status of the TiFlash replicas of a specific table using the following statement. The table is specified using the `WHERE` clause. If you remove the `WHERE` clause, you will check the replica status of all tables.

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>'
```

In the result of above statement:

* `AVAILABLE` indicates whether the TiFlash replicas of this table is available or not. `1` means available and `0` means unavailable.
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

### Engine isolation

Engine isolation is to specify that all queries use a replica of the specified engine by configuring the corresponding variable. The optional engines are `tikv` and `tiflash`, with the following two configuration levels:

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

    The default configuration of the SESSION level inherits from TiDB configuration of the INSTANCE level.

* TiDB instance-level, namely, INSTANCE level. This level overlaps with the SESSION level. For example, if you have configured "tikv, tiflash" in the SESSION level and "tikv" in the INSTANCE level, only TiKV is read.

    Add the following configuration item in the TiDB configuration file:

    ```
    [isolation-read]
    engines = ["tikv", "tiflash"]
    ```

    The INSTANCE-level default configuration is `["tikv", "tiflash"]`.

When the engine is configured as "tikv, tiflash", it can read both TiKV and TiFlash replicas at the same time, and the optimizer automatically chooses to read which one. After the engine is specified, if the table in the query does not have a corresponding engine replica, an error is reported indicating that the table does not have the engine replica. Because the TiKV replica always exist, so the only situation is that the engine is configured as `tiflash` but the TiFlash replica does not exist.

### Manual Hint

Manual Hint can force TiDB to use TiFlash replicas for specific table(s). The priority of manual Hint is lower than that of engine isolation. If the engine specified in Hint is not in the engine list, a warning is returned. Here is an example of using the manual Hint:

{{< copyable "sql" >}}

```sql
select /*+ read_from_storage(tiflash[table_name]) */ ... from table_name;
```

Engine isolation has higher priority over CBO and Hint, and Hint has higher priority over the cost estimation, which means that the cost estimation only selects the replica of the specified engine.

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

TiFlash mainly supports predicate and aggregate push-down calculations. Push-down calculations can help TiDB perform distributed acceleration. Currently, table joins and `DISTINCT COUNT` are not the supported calculation types, which will be optimized in later versions.

Currently, TiFlash supports the limited push-down of common expressions. To learn the specific push-down expressions, refer to [expression list](https://github.com/pingcap/tidb/blob/release-3.1/expression/expression.go#L409).

For example, if an aggregation function or the `WHERE` clause contains an expression that is not in the above list, the aggregation or related predicate filtering cannot be pushed down.

If a query encounters unsupported push-down calculations, TiDB needs to complete the remaining calculations, which might greatly affect the TiFlash acceleration effect.
