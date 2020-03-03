---
title: AUTO_RANDOM
summary: Learn the AUTO_RANDOM attribute.
category: reference
---

# AUTO_RANDOM <span class="version-mark">New in v3.1.0</span>

> **Warning:**
>
> `AUTO_RANDOM` is still an experimental feature. It is **NOT** recommended that you use this attribute in the production environment. In later TiDB versions, the syntax or semantics of `AUTO_RANDOM` might change.

Before using the `AUTO_RANDOM` attribute, set `allow-auto-random = true` in the `experimental` section of the TiDB configuration file. Refer to [`allow-auto-random`](/reference/configuration/tidb-server/configuration-file.md#allow-auto-random) for details.

## User scenario

When you write data intensively into TiDB and TiDB has the table with a primary key of the auto-increment integer type, hotspot issue might occur. To solve the hotspot issue, you can use the `AUTO_RANDOM` attribute. Refer to [Highly Concurrent Write Best Practices](/reference/best-practices/high-concurrency.md#complex-hotspot-problems) for details.

Take the following created table as an example:

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_increment, b varchar(255))
```

On this `t` table, you execute a large number of `INSERT` statements that do not specify the values of the primary key as below:

{{< copyable "sql" >}}

```sql
insert into t(b) values ('a'), ('b'), ('c')
```

In the above statement, values of the primary key (column `a`) are not specified, so TiDB uses the continuous auto-increment row values as the row IDs, which might cause write hotspot in a single TiKV node and affect the performance. To avoid such performance decrease, you can specify the `AUTO_RANDOM` attribute rather than the `AUTO_INCREMENT` attribute for the column `a` when you create the table. See the follow examples:

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random, b varchar(255))
```

or

{{< copyable "sql" >}}

```sql
create table t (a int auto_random, b varchar(255), primary key (a))
```

Then execute the `INSERT` statement such as `INSERT INTO t(b) values...`.  Now the results will be as follows:

+ If the `INSERT` statement does not specify the values of the integer primary key column (column `a`), TiDB automatically assigns values to this column. These values are not necessarily auto-increment or continuous but are unique, which avoids the hotspot problem caused by continuous row IDs.
+ If the `INSERT` statement explicitly specifies the values of the integer primary key column, TiDB saves these values, which works similarly to the `AUTO_INCREMENT` attribute.

TiDB automatically assigns values in the following way:

The highest five digits of the row value in binary (namely, shard bits) are determined by the starting time of the current transaction. The remaining digits are assigned values in an auto-increment order.

To use different number of shard bits, append a pair of parentheses to `AUTO_RANDOM` and specify the desired number of shard bits in the parentheses. See the following example:

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random(3), b varchar(255))
```

In the above `CREATE TABLE` statement, `3` shard bits are specified. The range of the number of shard bits is `[1, field_max_bits)`. `field_max_bits` is the length of bits occupied by the primary key column.

For tables with the `AUTO_RANDOM` attribute, the value of the corresponding `TIDB_ROW_ID_SHARDING_INFO` column in the `information_schema.tables` system table is `PK_AUTO_RANDOM_BITS=x`. `x` is the number of shard bits.

## Compatibility

TiDB supports parsing the version comment syntax. See the following example:

{{< copyable "sql" >}}

```sql
create table t (a int primary key /*T!30100 auto_random */)
```

{{< copyable "sql" >}}

```sql
create table t (a int primary key auto_random)
```

The above two statements have the same meaning.

In the result of `show create table`, the `AUTO_RANDOM` attribute is commented out. This comment includes a version number (for example, `/*T!30100 auto_random */`). Here `30100` indicates that the `AUTO_RANDOM` attribute is introduced in v3.1.0. TiDB of a lower version ignores the `AUTO_RANDOM` attribute in the above comment.

This attribute supports forward compatibility, namely, downgrade compatibility. TiDB earlier than v3.1.0 ignores the `AUTO_RANDOM` attribute of a table (with the above comment), so TiDB of earlier versions can also use the table with the attribute.

## Restrictions

Pay attention to the following restrictions when you use `AUTO_RANDOM`:

- Specify this attribute for the primary key column **ONLY** of integer type. Otherwise, an error might occur. Refer to [Notes for `alter-primary-key`](#notes-for-alter-primary-key) for exception.
- You cannot use `ALTER TABLE` to modify the `AUTO_RANDOM` attribute, including adding or removing this attribute.
- You cannot change the column type of the primary key column that is specified with `AUTO_RANDOM` attribute.
- You cannot specify `AUTO_RANDOM` and `AUTO_INCREMENT` for the same column at the same time.
- You cannot specify `AUTO_RANDOM` and `DEFAULT` (the default value of a column) for the same column at the same time.
- It is **not** recommended that you explicitly specify a value for the column with the `AUTO_RANDOM` attribute when you insert data. Otherwise, the numeral values that can be automatically assigned for this table might be used up in advance.

### Notes for `alter-primary-key`

- When `alter-primary-key = true`, the `AUTO_RANDOM` attribute is not supported even if the primary key is the integer type.
- In the configuration file, `alter-primary-key`and `allow-auto-random` cannot be set to `true` at the same time.
