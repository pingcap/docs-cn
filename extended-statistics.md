---
title: Introduction to Extended Statistics
summary: Learn how to use extended statistics to guide the optimizer.
---

# Introduction to Extended Statistics

TiDB can collect the following two types of statistics:

- Basic statistics: statistics such as histograms and Count-Min Sketch. See [Introduction to Statistics](/statistics.md) for details.
- Extended statistics: statistics filtered by tables and columns.

> **Tip:**
>
> Before reading this document, it is recommended that you read [Introduction to Statistics](/statistics.md) first.

When the `ANALYZE` statement is executed manually or automatically, TiDB by default only collects the basic statistics and does not collect the extended statistics. This is because the extended statistics are only used for optimizer estimates in specific scenarios, and collecting them requires additional overhead.

Extended statistics are disabled by default. To collect extended statistics, you need to first enable the extended statistics, and then register each individual extended statistics object.

After the registration, the next time the `ANALYZE` statement is executed, TiDB collects both the basic statistics and the registered extended statistics.

## Limitations

Extended statistics are not collected in the following scenarios:

- Statistics collection on indexes only
- Statistics collection using the `ANALYZE INCREMENTAL` command
- Statistics collection when the value of the system variable `tidb_enable_fast_analyze` is set to `true`

## Common operations

### Enable extended statistics

To enable extended statistics, set the system variable `tidb_enable_extended_stats` to `ON`:

```sql
SET GLOBAL tidb_enable_extended_stats = ON;
```

The default value of this variable is `OFF`. The setting of this system variable applies to all extended statistics objects.

### Register extended statistics

The registration for extended statistics is not a one-time task, and you need repeat the registration for each extended statistics object.

To register extended statistics, use the SQL statement `ALTER TABLE ADD STATS_EXTENDED`. The syntax is as follows:

```sql
ALTER TABLE table_name ADD STATS_EXTENDED IF NOT EXISTS stats_name stats_type(column_name, column_name...);
```

In the syntax, you can specify the table name, statistics name, statistics type, and column name of the extended statistics to be collected.

- `table_name` specifies the name of the table from which the extended statistics are collected.
- `stats_name` specifies the name of the statistics object, which must be unique for each table.
- `stats_type` specifies the type of the statistics. Currently, only the correlation type is supported.
- `column_name` specifies the column group, which might have multiple columns. Currently, you can only specify two column names.

<details>
<summary> How it works</summary>

To improve access performance, each TiDB node maintains a cache in the system table `mysql.stats_extended` for extended statistics. After you register the extended statistics, the next time the `ANALYZE` statement is executed, TiDB will collect the extended statistics if the system table `mysql.stats_extended` has the corresponding objects.

Each row in the `mysql.stats_extended` table has a `version` column. Once a row is updated, the value of `version` is increased. In this way, TiDB loads the table into memory incrementally, instead of fully.

TiDB loads `mysql.stats_extended` periodically to ensure that the cache is kept the same as the data in the table.

> **Warning:**
>
> It is **NOT RECOMMENDED** to directly operate on the `mysql.stats_extended` system table. Otherwise, inconsistent caches occur on different TiDB nodes.
>
> If you have mistakenly operated on the table, you can execute the following statement on each TiDB node. Then the current cache will be cleared and the `mysql.stats_extended` table will be fully reloaded:
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### Delete extended statistics

To delete an extended statistics object, use the following statement:

```sql
ALTER TABLE table_name DROP STATS_EXTENDED stats_name;
```

<details>
<summary>How it works</summary>

After you execute the statement, TiDB marks the value of the corresponding object in `mysql.stats_extended`'s column `status` to `2`, instead of deleting the object directly.

Other TiDB nodes will read this change and delete the object in their memory cache. The background garbage collection will delete the object eventually.

> **Warning:**
>
> It is **NOT RECOMMENDED** to directly operate on the `mysql.stats_extended` system table. Otherwise, inconsistent caches occur on different TiDB nodes.
>
> If you have mistakenly operated on the table, you can use the following statement on each TiDB node. Then the current cache will be cleared and the `mysql.stats_extended` table will be fully reloaded:
>
> ```sql
> ADMIN RELOAD STATS_EXTENDED;
> ```

</details>

### Export and import extended statistics

The way of exporting or importing extended statistics is the same as exporting or importing basic statistics. See [Introduction to Statistics - Import and export statistics](/statistics.md#import-and-export-statistics) for details.

## Usage examples for correlation-type extended statistics

Currently, TiDB only supports the correlation-type extended statistics. This type is used to estimate the number of rows in the range query and improve index selection. The following example shows how the correlation-type extended statistics are used to estimate the number of rows in a range query.

### Step 1. Define the table

Define a table `t` as follows:

```sql
CREATE TABLE t(col1 INT, col2 INT, KEY(col1), KEY(col2));
```

Suppose that `col1` and `col2` of table `t` both obey monotonically increasing constraints in row order. This means that the values of `col1` and `col2` are strictly correlated in order, and the correlation factor is `1`.

### Step 2. Execute an example query without extended statistics

Execute the following query without using extended statistics:

```sql
SELECT * FROM t WHERE col1 > 1 ORDER BY col2 LIMIT 1;
```

For the execution of the preceding query, the TiDB optimizer has the following options to access table `t`:

- Uses the index on `col1` to access table `t` and then sorts the result by `col2` to calculate `Top-1`.
- Uses the index on `col2` to meet the first row that satisfies `col1 > 1`. The cost of this access method mainly depends on how many rows are filtered out when TiDB scans the table in `col2`'s order.

Without extended statistics, the TiDB optimizer only supposes that `col1` and `col2` are independent, which **leads to a significant estimation error**.

### Step 3. Enable extended statistics

Set `tidb_enable_extended_stats` to `ON`, and register the extended statistics object for `col1` and `col2`:

```sql
ALTER TABLE t ADD STATS_EXTENDED s1 correlation(col1, col2);
```

When you execute `ANALYZE` after the registration, TiDB calculates the [Pearson correlation coefficient](https://en.wikipedia.org/wiki/Pearson_correlation_coefficient) of `col` and `col2` of table `t`, and writes the object into the `mysql.stats_extended` table.

### Step 4. See how extended statistics make a difference

After TiDB has the extended statistics for correlation, the optimizer can estimate how many rows to be scanned more precisely.

At this time, for the query in [Stage 2. Execute an example query without extended statistics](#step-2-execute-an-example-query-without-extended-statistics), `col1` and `col2` are strictly correlated in order. If TiDB accesses table `t` by using the index on `col2` to meet the first row that satisfies `col1 > 1`, the TiDB optimizer will equivalently translate the row count estimation into the following query:

```sql
SELECT * FROM t WHERE col1 <= 1 OR col1 IS NULL;
```

The preceding query result plus one will be the final estimation for the row count. In this way, you do not need to use the independent assumption and **the significant estimation error is avoided**.

If the correlation factor (`1` in this example) is less than the value of the system variable `tidb_opt_correlation_threshold`, the optimizer will use the independent assumption, but it will also increase the estimation heuristically. The larger the value of `tidb_opt_correlation_exp_factor`, the larger the estimation result. The larger the absolute value of the correlation factor, the larger the estimation result.
