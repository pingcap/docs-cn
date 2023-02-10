---
title: Read Historical Data Using the `AS OF TIMESTAMP` Clause
summary: Learn how to read historical data using the `AS OF TIMESTAMP` statement clause.
---

# Read Historical Data Using the `AS OF TIMESTAMP` Clause

This document describes how to perform the [Stale Read](/stale-read.md) feature using the `AS OF TIMESTAMP` clause to read historical data in TiDB, including specific usage examples and strategies for saving historical data.

TiDB supports reading historical data through a standard SQL interface, which is the `AS OF TIMESTAMP` SQL clause, without the need for special clients or drivers. After data is updated or deleted, you can read the historical data before the update or deletion using this SQL interface.

> **Note:**
>
> When reading historical data, TiDB returns the data with the old table structure even if the current table structure is different.

## Syntax

You can use the `AS OF TIMESTAMP` clause in the following three ways:

- [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md)
- [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md)
- [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md)

If you want to specify an exact point of time, you can set a datetime value or use a time function in the `AS OF TIMESTAMP` clause. The format of datetime is like "2016-10-08 16:45:26.999", with millisecond as the minimum time unit, but for most of the time, the time unit of second is enough for specifying a datetime, such as "2016-10-08 16:45:26". You can also get the current time to the millisecond using the `NOW(3)` function. If you want to read the data of several seconds ago, it is **recommended** to use an expression such as `NOW() - INTERVAL 10 SECOND`.

If you want to specify a time range, you can use the `TIDB_BOUNDED_STALENESS()` function in the clause. When this function is used, TiDB selects a suitable timestamp within the specified time range. "Suitable" means there are no transactions that start before this timestamp and have not been committed on the accessed replica, that is, TiDB can perform read operations on the accessed replica and the read operations are not blocked. You need to use `TIDB_BOUNDED_STALENESS(t1, t2)` to call this function. `t1` and `t2` are the two ends of the time range, which can be specified using either datetime values or time functions.

Here are some examples of the `AS OF TIMESTAMP` clause:

- `AS OF TIMESTAMP '2016-10-08 16:45:26'`: Tells TiDB to read the latest data stored at 16:45:26 on October 8, 2016.
- `AS OF TIMESTAMP NOW() - INTERVAL 10 SECOND`: Tells TiDB to read the latest data stored 10 seconds ago.
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS('2016-10-08 16:45:26', '2016-10-08 16:45:29')`: Tells TiDB to read the data as new as possible within the time range of 16:45:26 to 16:45:29 on October 8, 2016.
- `AS OF TIMESTAMP TIDB_BOUNDED_STALENESS(NOW() - INTERVAL 20 SECOND, NOW())`: Tells TiDB to read the data as new as possible within the time range of 20 seconds ago to the present.

> **Note:**
>
> In addition to specifying a timestamp, the most common use of the `AS OF TIMESTAMP` clause is to read data that is several seconds old. If this approach is used, it is recommended to read historical data older than 5 seconds.
>
> You need to deploy the NTP service for your TiDB and PD nodes when you use Stale Read. This avoids the situation where the specified timestamp used by TiDB goes ahead of the latest TSO allocating progress (such as a timestamp several seconds ahead), or is later than the GC safe point timestamp. When the specified timestamp goes beyond the service scope, TiDB returns an error.

## Usage examples

This section describes different ways to use the `AS OF TIMESTAMP` clause with several examples. It first introduces how to prepare the data for recovery, and then shows how to use `AS OF TIMESTAMP` in `SELECT`, `START TRANSACTION READ ONLY AS OF TIMESTAMP`, and `SET TRANSACTION READ ONLY AS OF TIMESTAMP` respectively.

### Prepare data sample

To prepare data for recovery, create a table first and insert several rows of data:

```sql
create table t (c int);
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
insert into t values (1), (2), (3);
```

```
Query OK, 3 rows affected (0.00 sec)
```

View the data in the table:

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

View the current time:

```sql
select now();
```

```
+---------------------+
| now()               |
+---------------------+
| 2021-05-26 16:45:26 |
+---------------------+
1 row in set (0.00 sec)
```

Update the data in a row:

```sql
update t set c=22 where c=2;
```

```
Query OK, 1 row affected (0.00 sec)
```

Confirm that the data of the row is updated:

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

### Read historical data using the `SELECT` statement

You can use the [`SELECT ... FROM ... AS OF TIMESTAMP`](/sql-statements/sql-statement-select.md) statement to read data from a time point in the past.

```sql
select * from t as of timestamp '2021-05-26 16:45:26';
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **Note:**
>
> When reading multiple tables using one `SELECT` statement, you need to make sure that the format of TIMESTAMP EXPRESSIONs is consistent. For example, `select * from t as of timestamp NOW() - INTERVAL 2 SECOND, c as of timestamp NOW() - INTERVAL 2 SECOND;`. In addition, you must specify the `AS OF` information for the relevant table in the `SELECT` statement; otherwise, the `SELECT` statement reads the latest data by default.

### Read historical data using the `START TRANSACTION READ ONLY AS OF TIMESTAMP` statement

You can use the [`START TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-start-transaction.md) statement to start a read-only transaction based on a time point in the past. The transaction reads historical data of the given time.

```sql
start transaction read only as of timestamp '2021-05-26 16:45:26';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

```sql
commit;
```

```
Query OK, 0 rows affected (0.00 sec)
```

After the transaction is committed, you can read the latest data.

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **Note:**
>
> If you start a transaction with the statement `START TRANSACTION READ ONLY AS OF TIMESTAMP`, it is a read-only transaction. Write operations are rejected in this transaction.

### Read historical data using the `SET TRANSACTION READ ONLY AS OF TIMESTAMP` statement

You can use the [`SET TRANSACTION READ ONLY AS OF TIMESTAMP`](/sql-statements/sql-statement-set-transaction.md) statement to set the next transaction as a read-only transaction based on a specified time point in the past. The transaction reads historical data of the given time.

```sql
set transaction read only as of timestamp '2021-05-26 16:45:26';
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
begin;
```

```
Query OK, 0 rows affected (0.00 sec)
```

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|    2 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

```sql
commit;
```

```
Query OK, 0 rows affected (0.00 sec)
```

After the transaction is committed, you can read the latest data.

```sql
select * from t;
```

```
+------+
| c    |
+------+
|    1 |
|   22 |
|    3 |
+------+
3 rows in set (0.00 sec)
```

> **Note:**
>
> If you start a transaction with the statement `SET TRANSACTION READ ONLY AS OF TIMESTAMP`, it is a read-only transaction. Write operations are rejected in this transaction.
