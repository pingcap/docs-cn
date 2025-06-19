---
title: AUTO_RANDOM
summary: 了解 AUTO_RANDOM 属性。
---

# AUTO_RANDOM <span class="version-mark">v3.1.0 新功能</span>

## 使用场景

由于 `AUTO_RANDOM` 的值是随机且唯一的，`AUTO_RANDOM` 通常用于替代 [`AUTO_INCREMENT`](/auto-increment.md)，以避免 TiDB 分配连续 ID 导致单个存储节点出现写入热点。如果当前 `AUTO_INCREMENT` 列是主键且类型为 `BIGINT`，你可以执行 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);` 语句将其从 `AUTO_INCREMENT` 切换为 `AUTO_RANDOM`。

<CustomContent platform="tidb">

有关如何在 TiDB 中处理高并发写入工作负载的更多信息，请参见[高并发写入最佳实践](/best-practices/high-concurrency-best-practices.md)。

</CustomContent>

[CREATE TABLE](/sql-statements/sql-statement-create-table.md) 语句中的 `AUTO_RANDOM_BASE` 参数用于设置 `auto_random` 的初始增量部分值。此选项可以视为内部接口的一部分。你可以忽略此参数。

## 基本概念

`AUTO_RANDOM` 是一个用于自动为 `BIGINT` 列分配值的列属性。自动分配的值是**随机**且**唯一**的。

要创建带有 `AUTO_RANDOM` 列的表，你可以使用以下语句。`AUTO_RANDOM` 列必须包含在主键中，且 `AUTO_RANDOM` 列是主键中的第一列。

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a, b));
```

你可以将关键字 `AUTO_RANDOM` 包装在可执行注释中。有关更多详细信息，请参考 [TiDB 特定注释语法](/comment-syntax.md#tidb-specific-comment-syntax)。

```sql
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT /*T![auto_rand] AUTO_RANDOM(6) */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT  /*T![auto_rand] AUTO_RANDOM(5, 54) */, b VARCHAR(255), PRIMARY KEY (a));
```

当你执行 `INSERT` 语句时：

- 如果你显式指定 `AUTO_RANDOM` 列的值，它将按原样插入表中。
- 如果你未显式指定 `AUTO_RANDOM` 列的值，TiDB 将生成一个随机值并将其插入表中。

```sql
tidb> CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255)) /*T! PRE_SPLIT_REGIONS=2 */ ;
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

tidb> SHOW CREATE TABLE t;
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                    |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` bigint(20) NOT NULL /*T![auto_rand] AUTO_RANDOM(5) */,
  `b` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T! PRE_SPLIT_REGIONS=2 */ |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

tidb> SHOW TABLE t REGIONS;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS               | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
|     62798 | t_158_                      | t_158_r_2305843009213693952 |     62810 |              28 | 62811, 62812, 62810 |          0 |           151 |          0 |                    1 |                0 |                        |                  |
|     62802 | t_158_r_2305843009213693952 | t_158_r_4611686018427387904 |     62803 |               1 | 62803, 62804, 62805 |          0 |            39 |          0 |                    1 |                0 |                        |                  |
|     62806 | t_158_r_4611686018427387904 | t_158_r_6917529027641081856 |     62813 |               4 | 62813, 62814, 62815 |          0 |           160 |          0 |                    1 |                0 |                        |                  |
|      9289 | t_158_r_6917529027641081856 | 78000000                    |     48268 |               1 | 48268, 58951, 62791 |          0 |         10628 |      43639 |                    2 |             7999 |                        |                  |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
4 rows in set (0.00 sec)
```

TiDB 自动分配的 `AUTO_RANDOM(S, R)` 列值总共有 64 位：

- `S` 是分片位数。值范围从 `1` 到 `15`。默认值为 `5`。
- `R` 是自动分配范围的总长度。值范围从 `32` 到 `64`。默认值为 `64`。

带有符号位的 `AUTO_RANDOM` 值的结构如下：

| 符号位 | 保留位 | 分片位 | 自增位 |
|---------|-------------|--------|--------------|
| 1 位 | `64-R` 位 | `S` 位 | `R-1-S` 位 |

不带符号位的 `AUTO_RANDOM` 值的结构如下：

| 保留位 | 分片位 | 自增位 |
|-------------|--------|--------------|
| `64-R` 位 | `S` 位 | `R-S` 位 |

- 值是否有符号位取决于相应列是否有 `UNSIGNED` 属性。
- 符号位的长度由是否存在 `UNSIGNED` 属性决定。如果有 `UNSIGNED` 属性，长度为 `0`。否则，长度为 `1`。
- 保留位的长度为 `64-R`。保留位始终为 `0`。
- 分片位的内容是通过计算当前事务开始时间的哈希值获得的。要使用不同长度的分片位（例如 10），可以在创建表时指定 `AUTO_RANDOM(10)`。
- 自增位的值存储在存储引擎中并按顺序分配。每次分配新值时，该值增加 1。自增位确保 `AUTO_RANDOM` 的值在全局范围内是唯一的。当自增位用尽时，再次分配值时会报错 `Failed to read auto-increment value from storage engine`。
- 值范围：最终生成值的最大位数 = 分片位 + 自增位。有符号列的范围是 `[-(2^(R-1))+1, (2^(R-1))-1]`，无符号列的范围是 `[0, (2^R)-1]`。
- 你可以将 `AUTO_RANDOM` 与 `PRE_SPLIT_REGIONS` 一起使用。当表创建成功时，`PRE_SPLIT_REGIONS` 会将表中的数据预先分割为 `2^(PRE_SPLIT_REGIONS)` 个 Region。

> **注意：**
>
> 分片位（`S`）的选择：
>
> - 由于总共有 64 个可用位，分片位长度会影响自增位长度。也就是说，随着分片位长度的增加，自增位长度会减少，反之亦然。因此，你需要平衡分配值的随机性和可用空间。
> - 最佳实践是将分片位设置为 `log(2, x)`，其中 `x` 是当前存储引擎的数量。例如，如果 TiDB 集群中有 16 个 TiKV 节点，你可以将分片位设置为 `log(2, 16)`，即 `4`。在所有 Region 均匀调度到每个 TiKV 节点后，批量写入的负载可以均匀分布到不同的 TiKV 节点，以最大化资源利用率。
>
> 范围（`R`）的选择：
>
> - 通常，当应用程序的数值类型无法表示完整的 64 位整数时，需要设置 `R` 参数。
> - 例如，JSON 数字的范围是 `[-(2^53)+1, (2^53)-1]`。TiDB 可以轻松地为定义为 `AUTO_RANDOM(5)` 的列分配超出此范围的整数，导致应用程序读取该列时出现意外行为。在这种情况下，你可以将有符号列的 `AUTO_RANDOM(5)` 替换为 `AUTO_RANDOM(5, 54)`，将无符号列的 `AUTO_RANDOM(5)` 替换为 `AUTO_RANDOM(5, 53)`，确保 TiDB 不会为该列分配大于 `9007199254740991`（2^53-1）的整数。

隐式分配给 `AUTO_RANDOM` 列的值会影响 `last_insert_id()`。要获取 TiDB 最后隐式分配的 ID，你可以使用 `SELECT last_insert_id ()` 语句。

要查看带有 `AUTO_RANDOM` 列的表的分片位数，你可以执行 `SHOW CREATE TABLE` 语句。你还可以在 `information_schema.tables` 系统表的 `TIDB_ROW_ID_SHARDING_INFO` 列中看到 `PK_AUTO_RANDOM_BITS=x` 模式的值。`x` 是分片位数。

创建带有 `AUTO_RANDOM` 列的表后，你可以使用 `SHOW WARNINGS` 查看最大隐式分配次数：

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
SHOW WARNINGS;
```

输出如下：

```sql
+-------+------+---------------------------------------------------------+
| Level | Code | Message                                                 |
+-------+------+---------------------------------------------------------+
| Note  | 1105 | Available implicit allocation times: 288230376151711743 |
+-------+------+---------------------------------------------------------+
1 row in set (0.00 sec)
```

## ID 的隐式分配规则

TiDB 对 `AUTO_RANDOM` 列的隐式分配值与 `AUTO_INCREMENT` 列类似。它们也受会话级系统变量 [`auto_increment_increment`](/system-variables.md#auto_increment_increment) 和 [`auto_increment_offset`](/system-variables.md#auto_increment_offset) 的控制。隐式分配值的自增位（ID）符合方程 `(ID - auto_increment_offset) % auto_increment_increment == 0`。

## 限制

使用 `AUTO_RANDOM` 时请注意以下限制：

- 要显式插入值，你需要将 `@@allow_auto_random_explicit_insert` 系统变量的值设置为 `1`（默认为 `0`）。**不建议**在插入数据时显式指定具有 `AUTO_RANDOM` 属性的列的值。否则，此表可自动分配的数值可能会提前用尽。
- 仅为 `BIGINT` 类型的主键列指定此属性。否则，会出现错误。此外，当主键的属性为 `NONCLUSTERED` 时，即使在整数主键上也不支持 `AUTO_RANDOM`。有关 `CLUSTERED` 类型的主键的更多详细信息，请参考[聚簇索引](/clustered-indexes.md)。
- 你不能使用 `ALTER TABLE` 修改 `AUTO_RANDOM` 属性，包括添加或删除此属性。
- 如果最大值接近列类型的最大值，则不能使用 `ALTER TABLE` 从 `AUTO_INCREMENT` 更改为 `AUTO_RANDOM`。
- 你不能更改指定了 `AUTO_RANDOM` 属性的主键列的列类型。
- 你不能同时为同一列指定 `AUTO_RANDOM` 和 `AUTO_INCREMENT`。
- 你不能同时为同一列指定 `AUTO_RANDOM` 和 `DEFAULT`（列的默认值）。
- 当在列上使用 `AUTO_RANDOM` 时，很难将列属性改回 `AUTO_INCREMENT`，因为自动生成的值可能会很大。
