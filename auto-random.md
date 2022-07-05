---
title: AUTO_RANDOM
summary: 本文介绍了 TiDB 的 `AUTO_RANDOM` 列属性。
aliases: ['/docs-cn/dev/auto-random/','/docs-cn/dev/reference/sql/attributes/auto-random/']
---

# AUTO_RANDOM <span class="version-mark">从 v3.1.0 版本开始引入</span>

> **注意：**
>
> `AUTO_RANDOM` 属性已于 v4.0.3 版本成为正式功能。

## 基本概念

`AUTO_RANDOM` 是应用在 `BIGINT` 类型列的列属性，用于列值的自动分配。其自动分配的值满足**随机性**和**唯一性**。

以下语句均可创建包含 `AUTO_RANDOM` 列的表。注释语法请参考 [TiDB 可执行注释](/comment-syntax.md)：

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
```

其中 `AUTO_RANDOM` 列必须被包含在主键中，且主键只有该列。

在用户执行 `INSERT` 语句时，

- 如果语句中显式指定了 `AUTO_RANDOM` 列的值，则该值会被正常插入到表中；
- 如果语句中没有显式指定 `AUTO_RANDOM` 列的值，TiDB 会自动生成一个看起来随机的值插入到表中。

例如：

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

mysql> INSERT INTO t(b) VALUES ('string2');
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t(b) VALUES ('string3');
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM t;
+---------------------+---------+
| a                   | b       |
+---------------------+---------+
|                   1 | string  |
| 1152921504606846978 | string2 |
| 4899916394579099651 | string3 |
+---------------------+---------+
3 rows in set (0.00 sec)
```

TiDB 自动分配的 `AUTO_RANDOM` 列值共有 64 位，结构如下：

| 总位数   | 符号位 | 分片位  | 自增位   |
|---------|-------|--------|---------|
| 64 bits | 1 bit | 5 bits | 58 bits |

- 符号位由该列是否存在 `UNSIGNED` 属性决定：存在则为 0，否则为 1。
- 分片位通过计算当前事务的开始时间的 HASH 值而得；要使用不同的分片位数量，可以在建表时指定 `AUTO_RANDOM(n)`，其中 n 的取值范围是 1 - 15。若不指定，则默认为 5。
- 自增位的值保存在存储引擎中，按顺序分配，每次分配完值后会加一。自增位保证了 `AUTO_RANDOM` 列值全局唯一；当自增位耗尽以后，再次自动分配时会报 "Failed to read auto-increment value from storage engine" 的错误。

注意：由于总位数固定为 64 位，分片位的数量会影响到自增位的数量：当分片位数增加时，自增位数会减少，反之亦然。因此，用户需要权衡“自动分配值的随机性”以及“可用空间”。最佳实践是将分片位设置为 `log(2, x)`，其中 `x` 为当前集群存储引擎的数量。例如，一个 TiDB 集群中存在 16 个 TiKV，分片位可以设置为 `log(2, 16)`，即 4。在所有 region 被均匀调度到各个 TiKV 上以后，此时大批量写入的负载可被均匀分布到不同 TiKV 节点，以实现资源最大化利用。

`AUTO RANDOM` 列隐式分配的值会影响 `last_insert_id()`。可以使用 `SELECT last_insert_id()` 获取上一次 TiDB 隐式分配的 ID。

要查看某张含有 `AUTO_RANDOM` 属性的表的分片位数量，除了 `SHOW CREATE TABLE` 以外，还可以在系统表 `INFORMATION_SCHEMA.TABLES` 中 `TIDB_ROW_ID_SHARDING_INFO` 一列中查到模式为 `PK_AUTO_RANDOM_BITS=x` 的值，其中 `x` 为分片位的数量。

## 使用场景

由于 `AUTO_RANDOM` 的值具有随机性和唯一性，因此 `AUTO_RANDOM` 通常被用于代替 `AUTO_INCREMENT`，以避免 TiDB 分配连续的 ID 值造成单个存储节点的写热点问题。如果当前表的 `AUTO_INCREMENT` 列是主键列，且列类型为 `BIGINT`，可以通过 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);` 从 `AUTO_INCREMENT` 切换成 `AUTO_RANDOM`。

关于如何在高并发写入场景下调优 TiDB，请参阅 [TiDB 高并发写入场景最佳实践](/best-practices/high-concurrency-best-practices.md)。

## 使用限制

- 要使用显式插入的功能，需要将系统变量 `@@allow_auto_random_explicit_insert` 的值设置为 `1`（默认值为 `0`）。不建议自行显式指定含有 `AUTO_RANDOM` 列的值。不恰当地显式赋值，可能会导致该表提前耗尽用于自动分配的数值。
- 该属性必须指定在 `BIGINT` 类型的主键列上，否则会报错。此外，当主键属性为 `NONCLUSTERED` 时，即使是整型主键列，也不支持使用 `AUTO_RANDOM`。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。
- 不支持使用 `ALTER TABLE` 来修改 `AUTO_RANDOM` 属性，包括添加或移除该属性。
- 支持将 `AUTO_INCREMENT` 属性改为 `AUTO_RANDOM` 属性。但在 `AUTO_INCREMENT` 的列数据最大值已接近 `BIGINT` 类型最大值的情况下，修改可能会失败。
- 不支持修改含有 `AUTO_RANDOM` 属性的主键列的列类型。
- 不支持与 `AUTO_INCREMENT` 同时指定在同一列上。
- 不支持与列的默认值 `DEFAULT` 同时指定在同一列上。
- `AUTO_RANDOM` 列的数据很难迁移到 `AUTO_INCREMENT` 列上，因为 `AUTO_RANDOM` 列自动分配的值通常都很大。
