---
title: AUTO_RANDOM
summary: 本文介绍了 TiDB 的 `AUTO_RANDOM` 列属性。
aliases: ['/docs-cn/dev/auto-random/','/docs-cn/dev/reference/sql/attributes/auto-random/']
---

# AUTO_RANDOM <span class="version-mark">从 v3.1.0 版本开始引入</span>

> **注意：**
>
> `AUTO_RANDOM` 属性已于 v4.0.3 版本成为正式功能。

## 使用场景

`AUTO_RANDOM` 用于解决大批量写数据入 TiDB 时因含有**整型自增主键列**的表而产生的热点问题。详情参阅 [TiDB 高并发写入场景最佳实践](/best-practices/high-concurrency-best-practices.md)。

以下面语句建立的表为例：

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_INCREMENT, b varchar(255))
```

在以上语句所建的表上执行大量未指定主键值的 `INSERT` 语句，示例如下：

```sql
INSERT INTO t(b) VALUES ('a'), ('b'), ('c')
```

如以上语句，由于未指定主键列的值（`a` 列），TiDB 会使用连续自增的行值作为行 ID，可能导致单个 TiKV 节点上产生写入热点，进而影响对外提供服务的性能。要避免这种写入热点，可以在执行建表语句时为 `a` 列指定 `AUTO_RANDOM` 属性而不是 `AUTO_INCREMENT` 属性。示例如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM, b varchar(255))
```

或者

{{< copyable "sql" >}}

```sql
CREATE TABLE t (a bigint AUTO_RANDOM, b varchar(255), PRIMARY KEY (a))
```

此时再执行形如 `INSERT INTO t(b) values...` 的 `INSERT` 语句。

+ 隐式分配：如果该 `INSERT` 语句没有指定整型主键列（`a` 列）的值，或者指定为 `NULL`，TiDB 会为该列自动分配值。该值不保证自增，不保证连续，只保证唯一，避免了连续的行 ID 带来的热点问题。
+ 显式插入：如果该 `INSERT` 语句显式指定了整型主键列的值，和 `AUTO_INCREMENT` 属性类似，TiDB 会保存该值。注意，如果未在系统变量 `@@sql_mode` 中设置 `NO_AUTO_VALUE_ON_ZERO`，即使显式指定整型主键列的值为 `0`，TiDB 也会为该列自动分配值。

> **注意：**
>
> 从 v4.0.3 开始，要使用显式插入的功能，需要将系统变量 `@@allow_auto_random_explicit_insert` 的值设置为 `1`（默认值为 `0`）。默认不支持显式插入的具体原因请参考[使用限制](#使用限制)一节。

自动分配值的计算方式如下：

该行值在二进制形式下，除去符号位的最高五位（称为 shard bits）由当前事务的开始时间决定，剩下的位数按照自增的顺序分配。

若要使用一个不同的 shard bits 的数量，可以在 `AUTO_RANDOM` 后面加一对括号，并在括号中指定想要的 shard bits 数量。示例如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM(3), b varchar(255))
```

以上建表语句中，shard bits 的数量为 `3`。shard bits 的数量的取值范围是 `[1, field_max_bits)`，其中 `field_max_bits` 为整型主键列类型占用的位长度。

创建完表后，使用 `SHOW WARNINGS` 可以查看当前表可支持的最大隐式分配的次数：

{{< copyable "sql" >}}

```sql
SHOW WARNINGS
```

```sql
+-------+------+----------------------------------------------------------+
| Level | Code | Message                                                  |
+-------+------+----------------------------------------------------------+
| Note  | 1105 | Available implicit allocation times: 1152921504606846976 |
+-------+------+----------------------------------------------------------+
```

> **注意：**
>
> 为保证可隐式分配的次数最大，从 v4.0.3 开始，`AUTO_RANDOM` 列类型只能为 `BIGINT`。

另外，要查看某张含有 `AUTO_RANDOM` 属性的表的 shard bits 数量，可以在系统表 `information_schema.tables` 中 `TIDB_ROW_ID_SHARDING_INFO` 一列看到模式为 `PK_AUTO_RANDOM_BITS=x` 的值，其中 `x` 为 shard bits 的数量。

`AUTO RANDOM` 列隐式分配的值会影响 `last_insert_id()`。可以使用 `SELECT last_insert_id()` 获取上一次 TiDB 隐式分配的 ID，例如：

{{< copyable "sql" >}}

```sql
INSERT INTO t (b) VALUES ("b")
SELECT * FROM t;
SELECT last_insert_id()
```

可能得到的结果如下：

```sql
+------------+---+
| a          | b |
+------------+---+
| 1073741825 | b |
+------------+---+

+------------------+
| last_insert_id() |
+------------------+
| 1073741825       |
+------------------+
```

## 兼容性

TiDB 支持解析版本注释语法。示例如下：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] auto_random */)
```

{{< copyable "sql" >}}

```sql
CREATE TABLE t (a bigint PRIMARY KEY AUTO_RANDOM)
```

以上两个语句含义相同。

在 `SHOW CREATE TABLE` 的结果中，`AUTO_RANDOM` 属性会被注释掉。注释会附带一个特性标识符，例如 `/*T![auto_rand] auto_random */`。其中 `auto_rand` 表示 `AUTO_RANDOM` 的特性标识符，只有实现了该标识符对应特性的 TiDB 版本才能够正常解析 SQL 语句片段。

该功能支持向前兼容，即降级兼容。没有实现对应特性的 TiDB 版本则会忽略表（带有上述注释）的 `AUTO_RANDOM` 属性，因此能够使用含有该属性的表。

## 使用限制

目前在 TiDB 中使用 `AUTO_RANDOM` 有以下限制：

- 该属性必须指定在整数类型的主键列上，否则会报错。此外，当主键属性为 `NONCLUSTERED` 时，即使是整型主键列，也不支持使用 `AUTO_RANDOM`。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。
- 不支持使用 `ALTER TABLE` 来修改 `AUTO_RANDOM` 属性，包括添加或移除该属性。
- 不支持修改含有 `AUTO_RANDOM` 属性的主键列的列类型。
- 不支持与 `AUTO_INCREMENT` 同时指定在同一列上。
- 不支持与列的默认值 `DEFAULT` 同时指定在同一列上。
- 插入数据时，不建议自行显式指定含有 `AUTO_RANDOM` 列的值。不恰当地显式赋值，可能会导致该表提前耗尽用于自动分配的数值。
