---
title: AUTO_RANDOM
summary: 本文介绍了 TiDB 的 `AUTO_RANDOM` 列属性。
aliases: ['/docs-cn/dev/auto-random/','/docs-cn/dev/reference/sql/attributes/auto-random/']
---

# AUTO_RANDOM <span class="version-mark">从 v3.1.0 版本开始引入</span>

## 使用场景

由于 `AUTO_RANDOM` 的值具有随机性和唯一性，因此 `AUTO_RANDOM` 通常用于代替 [`AUTO_INCREMENT`](/auto-increment.md)，以避免 TiDB 分配连续的 ID 值造成单个存储节点的写热点问题。如果当前表的 `AUTO_INCREMENT` 列是主键列，且列类型为 `BIGINT`，可以通过 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);` 从 `AUTO_INCREMENT` 切换成 `AUTO_RANDOM`。

关于如何在高并发写入场景下调优 TiDB，请参阅 [TiDB 高并发写入场景最佳实践](/best-practices/high-concurrency-best-practices.md)。

在 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句中的 `AUTO_RANDOM_BASE` 参数，也可以用来指定 `AUTO_RANDOM` 自增部分的初始值，该参数可以被认为属于内部接口的一部分，对于用户而言请忽略。

## 基本概念

`AUTO_RANDOM` 是应用在 `BIGINT` 类型列的属性，用于列值的自动分配。其自动分配的值满足**随机性**和**唯一性**。

以下语句均可创建包含 `AUTO_RANDOM` 列的表，其中 `AUTO_RANDOM` 列必须被包含在主键中，并且是主键的第一列。

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a, b));
```

`AUTO_RANDOM` 关键字可以被包裹在 TiDB 可执行注释中，注释语法请参考 [TiDB 可执行注释](/comment-syntax.md#tidb-可执行的注释语法)。

```sql
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT /*T![auto_rand] AUTO_RANDOM(6) */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT  /*T![auto_rand] AUTO_RANDOM(5, 54) */, b VARCHAR(255), PRIMARY KEY (a));
```

在用户执行 `INSERT` 语句时：

- 如果语句中显式指定了 `AUTO_RANDOM` 列的值，则该值会被正常插入到表中。
- 如果语句中没有显式指定 `AUTO_RANDOM` 列的值，TiDB 会自动生成一个随机的值插入到表中。

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
  `a` bigint NOT NULL /*T![auto_rand] AUTO_RANDOM(5) */,
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

TiDB 自动分配的 `AUTO_RANDOM(S, R)` 列值共有 64 位：

- `S` 表示分片位的数量，取值范围是 `1` 到 `15`。默认为 `5`。
- `R` 表示自动分配值域的总长度，取值范围是 `32` 到 `64`。默认为 `64`。

有符号位的 `AUTO_RANDOM` 列值的具体结构如下：

| 符号位 | 保留位      | 分片位 | 自增位       |
|--------|-------------|--------|--------------|
| 1 bit | `64-R` bits | `S` bits | `R-1-S` bits |

无符号位的 `AUTO_RANDOM` 列值的具体结构如下：

| 保留位      | 分片位 | 自增位     |
|-------------|--------|------------|
| `64-R` bits | `S` bits | `R-S` bits |

- 是否有符号位取决于该列是否存在 `UNSIGNED` 属性。
- 保留位的长度为 `64-R`，保留位的内容始终为 `0`。
- 分片位的内容通过计算当前事务的开始时间的哈希值而得。要使用不同的分片位数量（例如 10），可以在建表时指定 `AUTO_RANDOM(10)`。
- 自增位的值保存在存储引擎中，按顺序分配，每次分配完值后会自增 1。自增位保证了 `AUTO_RANDOM` 列值全局唯一。当自增位耗尽后，再次自动分配时会报 `Failed to read auto-increment value from storage engine` 的错误。
- 关于取值范围：最终生成值包含的最大位数 = 分片位 + 自增位。有符号位的列的取值范围是 `[-(2^(R-1))+1, (2^(R-1))-1]`。无符号位的列的取值范围是 `[0, (2^R)-1]`。
- `AUTO_RANDOM` 可以与 [`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions) 结合使用，用来在建表成功后就开始将表中的数据预均匀切分 `2^(PRE_SPLIT_REGIONS)` 个 Region。

> **注意：**
>
> 分片位长度 (`S`) 的选取：
>
> - 由于总位数固定为 64 位，分片位的数量会影响到自增位的数量：当分片位数增加时，自增位数会减少，反之亦然。因此，你需要权衡“自动分配值的随机性”以及“可用空间”。
> - 最佳实践是将分片位设置为 `log(2, x)`，其中 `x` 为当前集群存储引擎的数量。例如，一个 TiDB 集群中存在 16 个 TiKV，分片位可以设置为 `log(2, 16)`，即 `4`。在所有 Region 被均匀调度到各个 TiKV 上以后，此时大批量写入的负载可被均匀分布到不同 TiKV 节点，以实现资源最大化利用。
>
> 值域长度 (`R`) 的选取：
>
> - 通常，在应用程序的数值类型无法表示完整的 64 位整数时需要设置 `R` 参数。
> - 例如：JSON number 类型的取值范围为 `[-(2^53)+1, (2^53)-1]`，而 TiDB 很容易会为 `AUTO_RANDOM(5)` 的列分配超出该范围的整数，导致应用程序读取该列的值时出现异常。此时，对于有符号的列你可以用 `AUTO_RANDOM(5, 54)` 代替 `AUTO_RANDOM(5)`，无符号列可以用 `AUTO_RANDOM(5, 53)` 代替 `AUTO_RANDOM(5)`，这样使得 TiDB 不会分配出大于 `9007199254740991` (2^53-1) 的整数。

`AUTO RANDOM` 列隐式分配的值会影响 `last_insert_id()`。可以使用 `SELECT last_insert_id()` 获取上一次 TiDB 隐式分配的 ID。

要查看某张含有 `AUTO_RANDOM` 属性的表的分片位数量，除了 `SHOW CREATE TABLE` 以外，还可以在系统表 `INFORMATION_SCHEMA.TABLES` 中 `TIDB_ROW_ID_SHARDING_INFO` 一列中查到模式为 `PK_AUTO_RANDOM_BITS=x` 的值，其中 `x` 为分片位的数量。

创建完一张含有 `AUTO_RANDOM` 属性的表后，可以使用 `SHOW WARNINGS` 查看当前表可支持的最大隐式分配的次数：

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
SHOW WARNINGS;
```

输出结果如下：

```sql
+-------+------+---------------------------------------------------------+
| Level | Code | Message                                                 |
+-------+------+---------------------------------------------------------+
| Note  | 1105 | Available implicit allocation times: 288230376151711743 |
+-------+------+---------------------------------------------------------+
1 row in set (0.00 sec)
```

## ID 隐式分配规则

`AUTO_RANDOM` 列隐式分配的值和自增列类似，也遵循 session 变量 [`auto_increment_increment`](/system-variables.md#auto_increment_increment) 和 [`auto_increment_offset`](/system-variables.md#auto_increment_offset) 的控制，其中隐式分配值的自增位 (ID) 满足等式 `(ID - auto_increment_offset) % auto_increment_increment == 0`。

## 清除自增 ID 缓存

显式插入数据到 `AUTO_RANDOM` 列的行为与 `AUTO_INCREMENT` 列一致，你也需要清除自增 ID 缓存。详细信息请参阅[清除自增 ID 缓存](/auto-increment.md#清除自增-id-缓存)。

你可以执行 `ALTER TABLE` 语句设置 `AUTO_RANDOM_BASE=0` 来清除集群中所有 TiDB 节点的自增 ID 缓存。例如：

```sql
ALTER TABLE t AUTO_RANDOM_BASE=0;
```

```
Query OK, 0 rows affected, 1 warning (0.52 sec)
```

```sql
SHOW WARNINGS;
```

```
+---------+------+-------------------------------------------------------------------------+
| Level   | Code | Message                                                                 |
+---------+------+-------------------------------------------------------------------------+
| Warning | 1105 | Can't reset AUTO_INCREMENT to 0 without FORCE option, using 101 instead |
+---------+------+-------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

## 使用限制

目前在 TiDB 中使用 `AUTO_RANDOM` 有以下限制：

- 要使用显式插入的功能，需要将系统变量 `@@allow_auto_random_explicit_insert` 的值设置为 `1`（默认值为 `0`）。不建议自行显式指定含有 `AUTO_RANDOM` 列的值。不恰当地显式赋值，可能会导致该表提前耗尽用于自动分配的数值。
- 该属性必须指定在 `BIGINT` 类型的主键列上，否则会报错。此外，当主键属性为 `NONCLUSTERED` 时，即使是整型主键列，也不支持使用 `AUTO_RANDOM`。要了解关于 `CLUSTERED` 主键的详细信息，请参考[聚簇索引](/clustered-indexes.md)。
- 不支持使用 `ALTER TABLE` 来修改 `AUTO_RANDOM` 属性，包括添加或移除该属性。
- 支持将 `AUTO_INCREMENT` 属性改为 `AUTO_RANDOM` 属性。但在 `AUTO_INCREMENT` 的列数据最大值已接近 `BIGINT` 类型最大值的情况下，修改可能会失败。
- 不支持修改含有 `AUTO_RANDOM` 属性的主键列的列类型。
- 不支持与 `AUTO_INCREMENT` 同时指定在同一列上。
- 不支持与列的默认值 `DEFAULT` 同时指定在同一列上。
- `AUTO_RANDOM` 列的数据很难迁移到 `AUTO_INCREMENT` 列上，因为 `AUTO_RANDOM` 列自动分配的值通常都很大。
