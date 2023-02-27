---
title: AUTO_RANDOM
summary: Learn the AUTO_RANDOM attribute.
aliases: ['/docs/dev/auto-random/','/docs/dev/reference/sql/attributes/auto-random/']
---

# AUTO_RANDOM <span class="version-mark">New in v3.1.0</span>

## User scenario

Since the value of `AUTO_RANDOM` is random and unique, `AUTO_RANDOM` is often used in place of [`AUTO_INCREMENT`](/auto-increment.md) to avoid write hotspot in a single storage node caused by TiDB assigning consecutive IDs. If the current `AUTO_INCREMENT` column is a primary key and the type is `BIGINT`, you can execute the `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);` statement to switch from `AUTO_INCREMENT` to `AUTO_RANDOM`.

<CustomContent platform="tidb">

For more information about how to handle highly concurrent write-heavy workloads in TiDB, see [Highly concurrent write best practices](/best-practices/high-concurrency-best-practices.md).

</CustomContent>

## Basic concepts

`AUTO_RANDOM` is a column attribute that is used to automatically assign values to a `BIGINT` column. Values assigned automatically are **random** and **unique**.

To create a table with an `AUTO_RANDOM` column, you can use the following statements. The `AUTO_RANDOM` column must be included in a primary key, and the `AUTO_RANDOM` column is the first column in the primary key.

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a, b));
```

You can wrap the keyword `AUTO_RANDOM` in an executable comment. For more details, refer to [TiDB specific comment syntax](/comment-syntax.md#tidb-specific-comment-syntax).

```sql
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT /*T![auto_rand] AUTO_RANDOM(6) */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT  /*T![auto_rand] AUTO_RANDOM(5, 54) */, b VARCHAR(255), PRIMARY KEY (a));
```

When you execute an `INSERT` statement:

- If you explicitly specify the value of the `AUTO_RANDOM` column, it is inserted into the table as is.
- If you do not explicitly specify the value of the `AUTO_RANDOM` column, TiDB generates a random value and inserts it into the table.

```sql
tidb> CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
Query OK, 0 rows affected, 1 warning (0.01 sec)

tidb> INSERT INTO t(a, b) VALUES (1, 'string');
Query OK, 1 row affected (0.00 sec)

tidb> SELECT * FROM t;
+---+--------+
| a | b      |
+---+--------+
| 1 | string |
+---+--------+
1 row in set (0.01 sec)

tidb> INSERT INTO t(b) VALUES ('string2');
Query OK, 1 row affected (0.00 sec)

tidb> INSERT INTO t(b) VALUES ('string3');
Query OK, 1 row affected (0.00 sec)

tidb> SELECT * FROM t;
+---------------------+---------+
| a                   | b       |
+---------------------+---------+
|                   1 | string  |
| 1152921504606846978 | string2 |
| 4899916394579099651 | string3 |
+---------------------+---------+
3 rows in set (0.00 sec)
```

The `AUTO_RANDOM(S, R)` column value automatically assigned by TiDB has a total of 64 bits:

- `S` is the number of shard bits. The value ranges from `1` to `15`. The default value is `5`.
- `R` is the total length of the automatic allocation range. The value ranges from `32` to `64`. The default value is `64`.

The structure of an `AUTO_RANDOM` value is as follows:

| Total number of bits | Sign bit | Reserved bits | Shard bits | Auto-increment bits |
|---------|---------|-------------|--------|--------------|
| 64 bits | 0/1 bit | (64-R) bits | S bits | (R-1-S) bits |

- The length of the sign bit is determined by the existence of an `UNSIGNED` attribute. If there is an `UNSIGNED` attribute, the length is `0`. Otherwise, the length is `1`.
- The length of the reserved bits is `64-R`. The reserved bits are always `0`.
- The content of the shard bits is obtained by calculating the hash value of the starting time of the current transaction. To use a different length of shard bits (such as 10), you can specify `AUTO_RANDOM(10)` when creating the table.
- The value of the auto-increment bits is stored in the storage engine and allocated sequentially. Each time a new value is allocated, the value is incremented by 1. The auto-increment bits ensure that the values of `AUTO_RANDOM` are unique globally. When the auto-increment bits are exhausted, an error `Failed to read auto-increment value from storage engine` is reported when the value is allocated again.

> **Note:**
>
> Selection of shard bits (`S`):
>
> - Since there is a total of 64 available bits, the shard bits length affects the auto-increment bits length. That is, as the shard bits length increases, the length of auto-increment bits decreases, and vice versa. Therefore, you need to balance the randomness of allocated values and available space.
> - The best practice is to set the shard bits as `log(2, x)`, in which `x` is the current number of storage engines. For example, if there are 16 TiKV nodes in a TiDB cluster, you can set the shard bits as `log(2, 16)`, that is `4`. After all regions are evenly scheduled to each TiKV node, the load of bulk writes can be uniformly distributed to different TiKV nodes to maximize resource utilization.
>
> Selection of range (`R`):
>
> - Typically, the `R` parameter needs to be set when the numeric type of the application cannot represent a full 64-bit integer.
> - For example, the range of JSON number is `[-2^53+1, 2^53-1]`. TiDB can easily assign an integer outside this range to a column of `AUTO_RANDOM(5)`, causing unexpected behaviors when the application reads the column. In this case, you can replace `AUTO_RANDOM(5)` with `AUTO_RANDOM(5, 54)` and TiDB does not assign an integer greater than `9007199254740991` (2^53-1) to the column.

Values allocated implicitly to the `AUTO_RANDOM` column affect `last_insert_id()`. To get the ID that TiDB last implicitly allocates, you can use the `SELECT last_insert_id ()` statement.

To view the shard bits number of the table with an `AUTO_RANDOM` column, you can execute the `SHOW CREATE TABLE` statement. You can also see the value of the `PK_AUTO_RANDOM_BITS=x` mode in the `TIDB_ROW_ID_SHARDING_INFO` column in the `information_schema.tables` system table. `x` is the number of shard bits.

## Restrictions

Pay attention to the following restrictions when you use `AUTO_RANDOM`:

- To insert values explicitly, you need to set the value of the `@@allow_auto_random_explicit_insert` system variable to `1` (`0` by default). It is **not** recommended that you explicitly specify a value for the column with the `AUTO_RANDOM` attribute when you insert data. Otherwise, the numeral values that can be automatically allocated for this table might be used up in advance.
- Specify this attribute for the primary key column **ONLY** as the `BIGINT` type. Otherwise, an error occurs. In addition, when the attribute of the primary key is `NONCLUSTERED`, `AUTO_RANDOM` is not supported even on the integer primary key. For more details about the primary key of the `CLUSTERED` type, refer to [clustered index](/clustered-indexes.md).
- You cannot use `ALTER TABLE` to modify the `AUTO_RANDOM` attribute, including adding or removing this attribute.
- You cannot use `ALTER TABLE` to change from `AUTO_INCREMENT` to `AUTO_RANDOM` if the maximum value is close to the maximum value of the column type.
- You cannot change the column type of the primary key column that is specified with `AUTO_RANDOM` attribute.
- You cannot specify `AUTO_RANDOM` and `AUTO_INCREMENT` for the same column at the same time.
- You cannot specify `AUTO_RANDOM` and `DEFAULT` (the default value of a column) for the same column at the same time.
- When`AUTO_RANDOM` is used on a column, it is difficult to change the column attribute back to `AUTO_INCREMENT` because the auto-generated values might be very large.
