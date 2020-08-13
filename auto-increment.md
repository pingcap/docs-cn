---
title: AUTO_INCREMENT
summary: Learn the `AUTO_INCREMENT` column attribute of TiDB.
aliases: ['/docs/dev/auto-increment/']
---

# AUTO_INCREMENT

This document introduces the `AUTO_INCREMENT` column attribute, including its concept, implementation principles, auto-increment related features, and restrictions.

## Concept 

`AUTO_INCREMENT` is a column attribute that is used to automatically fill in default column values. When the `INSERT` statement does not specify values for the `AUTO_INCREMENT` column, the system automatically assigns values to this column.

For performance reasons, `AUTO_INCREMENT` numbers are allocated in a batch of values (30 thousand by default) to each TiDB server. This means that while `AUTO_INCREMENT` numbers are guaranteed to be unique, values assigned to an `INSERT` statement will only be monotonic on a per TiDB server basis.

The following is a basic example of `AUTO_INCREMENT`:

{{< copyable "sql" >}}

```sql
create table t(id int primary key AUTO_INCREMENT, c int);
```

{{< copyable "sql" >}}

```sql
insert into t(c) values (1);
insert into t(c) values (2);
insert into t(c) values (3), (4), (5);
```

```sql
mysql> select * from t;
+----+---+
| id | c |
+----+---+
| 1  | 1 |
| 2  | 2 |
| 3  | 3 |
| 4  | 4 |
| 5  | 5 |
+----+---+
5 rows in set (0.01 sec)
```

In addition, `AUTO_INCREMENT` also supports the `INSERT` statements that explicitly specify column values. In such cases, TiDB stores the explicitly specified values:

{{< copyable "sql" >}}

```sql
insert into t(id, c) values (6, 6);
```

```sql
mysql> select * from t;
+----+---+
| id | c |
+----+---+
| 1  | 1 |
| 2  | 2 |
| 3  | 3 |
| 4  | 4 |
| 5  | 5 |
| 6  | 6 |
+----+---+
6 rows in set (0.01 sec)
```

The usage above is the same as that of `AUTO_INCREMENT` in MySQL. However, in terms of the specific value that is implicitly assigned, TiDB differs from MySQL significantly.

## Implementation principles

TiDB implements the `AUTO_INCREMENT` implicit assignment in the following way:

For each auto-increment column, a globally visible key-value pair is used to record the maximum ID that has been assigned. In a distributed environment, communication between nodes has some overhead. Therefore, to avoid the issue of write amplification, each TiDB node applies for a batch of consecutive IDs as caches when assigning IDs, and then applies for the next batch of IDs after the first batch is assigned. Therefore, TiDB nodes do not apply to the storage node for IDs when assigning IDs each time. For example:

```sql
create table t(id int unique key AUTO_INCREMENT, c int);
```

Assume two TiDB instances, `A` and `B`, in the cluster. If you execute an `INSERT` statement on the `t` table on `A` and `B` respectively:

```sql
insert into t (c) values (1)
```

Instance `A` might cache the auto-increment IDs of `[1,30000]`, and instance `B` might cache the auto-increment IDs of `[30001,60000]`. In `INSERT` statements to be executed, these cached IDs of each instance will be assigned to the `AUTO_INCREMENT` column as the default values.

## Basic Features

### Uniqueness

> **Warning:**
>
> When the cluster has multiple TiDB instances, if the table schema contains the auto-increment IDs, it is recommended not to use explicit insert and implicit assignment at the same time, which means using the default values of the auto-increment column and the custom values. Otherwise, it might break the uniqueness of implicitly assigned values.

In the example above, perform the following operations in order:

1. The client inserts a statement `insert into t values (2, 1)` to instance `B`, which sets `id` to `2`. The statement is successfully executed.

2. The client sends a statement `insert into t (c) (1)` to instance `A`. This statement does not specify the value of `id`, so the ID is assigned by `A`. At present, because `A` caches the IDs of `[1, 30000]`, it might assign `2` as the value of the auto-increment ID, and increases the local counter by `1`. At this time, the data whose ID is `2` already exists in the database, so the `Duplicated Error` error is returned.

### Increment

TiDB guarantees that implicitly assigned values of the `AUTO_INCREMENT` column are incremental only in the cluster with a single TiDB instance. That is, for the same auto-increment column, the value assigned earlier is smaller than the value assigned later. However, in a cluster with multiple instances, TiDB cannot guarantee that the auto-increment column is incremental.

In the example above, if you first execute an `INSERT` statement on instance `B`, and then execute an `INSERT` statement on instance `A`. Because of the behavior of caching auto-increment ID, the auto-increment column might be implicitly assigned `30002` and `2` respectively. The assigned values are not incremental in the time order.

### Monotonic

In a cluster with multiple TiDB instances, the `AUTO_INCREMENT` assigned values are **only** monotonic on a per-server basis.

Take the following table as an example:

```sql
create table t (a int primary key AUTO_INCREMENT)
```

Execute the following statement on the table:

```sql
insert into t values (), (), (), ()
```

Even if other TiDB instances are performing concurrent write operations, or if the current instance does not have enough cached IDs left, the assigned values are still monotonic.

### Relation with `_tidb_rowid`

If the primary key of integer type does not exist, TiDB uses `_tidb_rowid` to identify rows. `_tidb_rowid` and the auto-increment column (if any) share an allocator. In such cases, the cache size might be consumed by both `_tidb_rowid` and the auto-increment column. Therefore, you might encounter the following situation:

```sql
mysql> create table t(id int unique key AUTO_INCREMENT);
Query OK, 0 rows affected (0.05 sec)

mysql> insert into t values (),(),();
Query OK, 3 rows affected (0.00 sec)
Records: 3  Duplicates: 0  Warnings: 0

mysql> select _tidb_rowid, id from t;
+-------------+------+
| _tidb_rowid | id   |
+-------------+------+
|           4 |    1 |
|           5 |    2 |
|           6 |    3 |
+-------------+------+
3 rows in set (0.01 sec)
```

### Cache size control

In earlier versions of TiDB, the cache size of the auto-increment ID was transparent to users. Starting from v3.0.14, v3.1.2, and v4.0.rc-2, TiDB has introduced the `AUTO_ID_CACHE` table option to allow users to set the cache size for allocating the auto-increment ID.

```sql
mysql> create table t(a int auto_increment key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

mysql> insert into t values();
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> select * from t;
+---+
| a |
+---+
| 1 |
+---+
1 row in set (0.01 sec)
```

At this time, if you invalidate the auto-increment cache of this column and redo the implicit insertion, the result is as follows:

```sql
mysql> delete from t;
Query OK, 1 row affected (0.01 sec)

mysql> rename table t to t1;
Query OK, 0 rows affected (0.01 sec)

mysql> insert into t1 values()
Query OK, 1 row affected (0.00 sec)

mysql> select * from t;
+-----+
| a   |
+-----+
| 101 |
+-----+
1 row in set (0.00 sec)
```

The re-assigned value is `101`. This shows that the size of cache for allocating the auto-increment ID is `100`.

In addition, when the length of consecutive IDs in a batch `insert` statement exceeds the length of `AUTO_ID_CACHE`, TiDB increases the cache size accordingly to ensure that the statement can be inserted properly.

### Auto-increment step size and offset

Starting from v3.0.9 and v4.0.0-rc.1, similar to the behavior of MySQL, the value implicitly assigned to the auto-increment column is controlled by the `@@auto_increment_increment` and `@@auto_increment_offset` session variables.

The value (ID) implicitly assigned to auto-increment columns satisfies the following equation: 

`(ID - auto_increment_offset) % auto_increment_increment == 0`

## Restrictions

Currently, `AUTO_INCREMENT` has the following restrictions when used in TiDB:

- It must be defined on the column of the primary key or unique index.
- It must be defined on the column of `INTEGER`, `FLOAT`, or `DOUBLE` type.
- It cannot be specified on the same column with the `DEFAULT` column value.
- `ALTER TABLE` cannot be used to add the `AUTO_INCREMENT` attribute.
- `ALTER TABLE` can be used to remove the `AUTO_INCREMENT` attribute. However, starting from v2.1.18 and v3.0.4, TiDB uses the session variable `@@tidb_allow_remove_auto_inc` to control whether `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` can be used to remove the `AUTO_INCREMENT` attribute of a column. By default, you cannot use `ALTER TABLE MODIFY` or `ALTER TABLE CHANGE` to remove the `AUTO_INCREMENT` attribute.
