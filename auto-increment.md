---
title: AUTO_INCREMENT
summary: 了解 TiDB 的 `AUTO_INCREMENT` 列属性。
---

# AUTO_INCREMENT

本文介绍 `AUTO_INCREMENT` 列属性，包括其概念、实现原理、自增相关特性和限制。

<CustomContent platform="tidb">

> **注意：**
>
> `AUTO_INCREMENT` 属性可能在生产环境中造成热点问题。详情请参见[热点问题处理](/troubleshoot-hot-spot-issues.md)。建议使用 [`AUTO_RANDOM`](/auto-random.md) 代替。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注意：**
>
> `AUTO_INCREMENT` 属性可能在生产环境中造成热点问题。详情请参见[热点问题处理](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)。建议使用 [`AUTO_RANDOM`](/auto-random.md) 代替。

</CustomContent>

你也可以在 [`CREATE TABLE`](/sql-statements/sql-statement-create-table.md) 语句中使用 `AUTO_INCREMENT` 参数来指定自增字段的初始值。

## 概念

`AUTO_INCREMENT` 是一个列属性，用于自动填充默认列值。当 `INSERT` 语句没有为 `AUTO_INCREMENT` 列指定值时，系统会自动为该列分配值。

出于性能考虑，`AUTO_INCREMENT` 数值会按批次（默认为 3 万个）分配给每个 TiDB 服务器。这意味着虽然 `AUTO_INCREMENT` 数值保证是唯一的，但分配给 `INSERT` 语句的值只在每个 TiDB 服务器基础上保持单调递增。

> **注意：**
>
> 如果你希望 `AUTO_INCREMENT` 数值在所有 TiDB 服务器上都保持单调递增，并且你的 TiDB 版本是 v6.5.0 或更高版本，建议启用 [MySQL 兼容模式](#mysql-兼容模式)。

以下是 `AUTO_INCREMENT` 的基本示例：

{{< copyable "sql" >}}

```sql
CREATE TABLE t(id int PRIMARY KEY AUTO_INCREMENT, c int);
```

{{< copyable "sql" >}}

```sql
INSERT INTO t(c) VALUES (1);
INSERT INTO t(c) VALUES (2);
INSERT INTO t(c) VALUES (3), (4), (5);
```

```sql
mysql> SELECT * FROM t;
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

此外，`AUTO_INCREMENT` 也支持显式指定列值的 `INSERT` 语句。在这种情况下，TiDB 会存储显式指定的值：

{{< copyable "sql" >}}

```sql
INSERT INTO t(id, c) VALUES (6, 6);
```

```sql
mysql> SELECT * FROM t;
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

上述用法与 MySQL 中的 `AUTO_INCREMENT` 相同。但是，在隐式分配的具体值方面，TiDB 与 MySQL 有显著的不同。

## 实现原理

TiDB 以如下方式实现 `AUTO_INCREMENT` 隐式分配：

对于每个自增列，使用一个全局可见的键值对来记录已分配的最大 ID。在分布式环境中，节点之间的通信有一定开销。因此，为了避免写放大问题，每个 TiDB 节点在分配 ID 时会申请一批连续的 ID 作为缓存，然后在第一批 ID 分配完后再申请下一批 ID。因此，TiDB 节点在每次分配 ID 时不需要向存储节点申请 ID。例如：

```sql
CREATE TABLE t(id int UNIQUE KEY AUTO_INCREMENT, c int);
```

假设集群中有两个 TiDB 实例 `A` 和 `B`。如果你在 `A` 和 `B` 上分别对 `t` 表执行 `INSERT` 语句：

```sql
INSERT INTO t (c) VALUES (1)
```

实例 `A` 可能会缓存自增 ID `[1,30000]`，实例 `B` 可能会缓存自增 ID `[30001,60000]`。在要执行的 `INSERT` 语句中，这些缓存的 ID 将作为默认值分配给 `AUTO_INCREMENT` 列。

## 基本特性

### 唯一性

> **警告：**
>
> 当集群有多个 TiDB 实例时，如果表结构包含自增 ID，建议不要同时使用显式插入和隐式分配，即使用自增列的默认值和自定义值。否则，可能会破坏隐式分配值的唯一性。

在上面的例子中，按顺序执行以下操作：

1. 客户端向实例 `B` 插入语句 `INSERT INTO t VALUES (2, 1)`，将 `id` 设置为 `2`。语句成功执行。

2. 客户端向实例 `A` 发送语句 `INSERT INTO t (c) (1)`。此语句没有指定 `id` 的值，所以 ID 由 `A` 分配。目前，由于 `A` 缓存了 `[1, 30000]` 的 ID，它可能会分配 `2` 作为自增 ID 的值，并将本地计数器加 `1`。此时，数据库中已经存在 ID 为 `2` 的数据，所以会返回 `Duplicated Error` 错误。

### 单调性

TiDB 保证 `AUTO_INCREMENT` 值在每个服务器上是单调递增的（始终增加）。考虑以下示例，其中生成了连续的 `AUTO_INCREMENT` 值 1-3：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (a int PRIMARY KEY AUTO_INCREMENT, b timestamp NOT NULL DEFAULT NOW());
INSERT INTO t (a) VALUES (NULL), (NULL), (NULL);
SELECT * FROM t;
```

```sql
Query OK, 0 rows affected (0.11 sec)

Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

+---+---------------------+
| a | b                   |
+---+---------------------+
| 1 | 2020-09-09 20:38:22 |
| 2 | 2020-09-09 20:38:22 |
| 3 | 2020-09-09 20:38:22 |
+---+---------------------+
3 rows in set (0.00 sec)
```

单调性与连续性不是相同的保证。考虑以下示例：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (id INT NOT NULL PRIMARY KEY auto_increment, a VARCHAR(10), cnt INT NOT NULL DEFAULT 1, UNIQUE KEY (a));
INSERT INTO t (a) VALUES ('A'), ('B');
SELECT * FROM t;
INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;
SELECT * FROM t;
```

```sql
Query OK, 0 rows affected (0.00 sec)

Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

+----+------+-----+
| id | a    | cnt |
+----+------+-----+
|  1 | A    |   1 |
|  2 | B    |   1 |
+----+------+-----+
2 rows in set (0.00 sec)

Query OK, 3 rows affected (0.00 sec)
Records: 2  Duplicates: 1  Warnings: 0

+----+------+-----+
| id | a    | cnt |
+----+------+-----+
|  1 | A    |   2 |
|  2 | B    |   1 |
|  4 | C    |   1 |
+----+------+-----+
3 rows in set (0.00 sec)
```

在这个例子中，`AUTO_INCREMENT` 值 `3` 被分配给了 `INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;` 中键 `A` 的 `INSERT`，但由于这个 `INSERT` 语句包含重复键 `A`，所以这个值从未被使用。这导致了序列中出现非连续的间隙。这种行为被认为是合法的，尽管它与 MySQL 不同。MySQL 在其他场景（如事务被中止和回滚）中也会在序列中出现间隙。

## AUTO_ID_CACHE

如果对不同的 TiDB 服务器执行 `INSERT` 操作，`AUTO_INCREMENT` 序列可能会出现显著的"跳跃"。这是因为每个服务器都有自己的 `AUTO_INCREMENT` 值缓存：

{{< copyable "sql" >}}

```sql
CREATE TABLE t (a int PRIMARY KEY AUTO_INCREMENT, b timestamp NOT NULL DEFAULT NOW());
INSERT INTO t (a) VALUES (NULL), (NULL), (NULL);
INSERT INTO t (a) VALUES (NULL);
SELECT * FROM t;
```

```sql
Query OK, 1 row affected (0.03 sec)

+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
+---------+---------------------+
4 rows in set (0.00 sec)
```

对初始 TiDB 服务器执行新的 `INSERT` 操作会生成 `AUTO_INCREMENT` 值 `4`。这是因为初始 TiDB 服务器的 `AUTO_INCREMENT` 缓存中仍有可分配的空间。在这种情况下，序列值不能被视为全局单调的，因为值 `4` 是在值 `2000001` 之后插入的：

```sql
mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
+---------+---------------------+
5 rows in set (0.00 sec)
```

`AUTO_INCREMENT` 缓存不会在 TiDB 服务器重启后持续存在。以下 `INSERT` 语句是在初始 TiDB 服务器重启后执行的：

```sql
mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
| 2030001 | 2020-09-09 20:54:11 |
+---------+---------------------+
6 rows in set (0.00 sec)
```

频繁的 TiDB 服务器重启可能会导致 `AUTO_INCREMENT` 值的耗尽。在上面的例子中，初始 TiDB 服务器的缓存中仍有值 `[5-30000]` 可用。这些值被丢失，不会被重新分配。

不建议依赖 `AUTO_INCREMENT` 值的连续性。考虑以下示例，其中一个 TiDB 服务器有值 `[2000001-2030000]` 的缓存。通过手动插入值 `2029998`，你可以看到在获取新的缓存范围时的行为：

```sql
mysql> INSERT INTO t (a) VALUES (2029998);
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
| 2030001 | 2020-09-09 20:54:11 |
| 2029998 | 2020-09-09 21:08:11 |
| 2029999 | 2020-09-09 21:08:11 |
| 2030000 | 2020-09-09 21:08:11 |
| 2060001 | 2020-09-09 21:08:11 |
| 2060002 | 2020-09-09 21:08:11 |
+---------+---------------------+
11 rows in set (0.00 sec)
```

在插入值 `2030000` 后，下一个值是 `2060001`。这个序列的跳跃是由于另一个 TiDB 服务器获得了中间缓存范围 `[2030001-2060000]`。当部署多个 TiDB 服务器时，由于缓存请求交错，`AUTO_INCREMENT` 序列中会出现间隙。

### 缓存大小控制

在早期版本的 TiDB 中，自增 ID 的缓存大小对用户是透明的。从 v3.0.14、v3.1.2 和 v4.0.rc-2 开始，TiDB 引入了 `AUTO_ID_CACHE` 表选项，允许用户设置分配自增 ID 的缓存大小。

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

INSERT INTO t values();
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+---+
| a |
+---+
| 1 |
+---+
1 row in set (0.01 sec)

SHOW CREATE TABLE t;
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                             |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=101 /*T![auto_id_cache] AUTO_ID_CACHE=100 */ |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

此时，如果重启 TiDB，自增 ID 缓存将丢失，新的插入操作将从超出先前缓存范围的更高值开始分配 ID。

```sql
INSERT INTO t VALUES();
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+-----+
| a   |
+-----+
|   1 |
| 101 |
+-----+
2 rows in set (0.01 sec)
```

新分配的值是 `101`。这表明分配自增 ID 的缓存大小是 `100`。

此外，当批量 `INSERT` 语句中连续 ID 的长度超过 `AUTO_ID_CACHE` 的长度时，TiDB 会相应地增加缓存大小，以确保语句可以正常插入数据。

### 清除自增 ID 缓存

在某些场景下，你可能需要清除自增 ID 缓存以确保数据一致性。例如：

<CustomContent platform="tidb">

- 在使用 [Data Migration (DM)](/dm/dm-overview.md) 进行增量复制的场景中，一旦复制完成，数据写入下游 TiDB 的方式从 DM 切换到应用程序的写操作。同时，自增列的 ID 写入模式通常从显式插入切换到隐式分配。

</CustomContent>
<CustomContent platform="tidb-cloud">

- 在使用[数据迁移](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)功能进行增量复制的场景中，一旦复制完成，数据写入下游 TiDB 的方式从 DM 切换到应用程序的写操作。同时，自增列的 ID 写入模式通常从显式插入切换到隐式分配。

</CustomContent>

- 当你的应用程序同时涉及显式 ID 插入和隐式 ID 分配时，你需要清除自增 ID 缓存，以避免未来隐式分配的 ID 与先前显式插入的 ID 发生冲突，这可能导致主键冲突错误。更多信息，请参见[唯一性](/auto-increment.md#唯一性)。

要清除集群中所有 TiDB 节点上的自增 ID 缓存，你可以执行带有 `AUTO_INCREMENT = 0` 的 `ALTER TABLE` 语句。例如：

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

INSERT INTO t VALUES();
Query OK, 1 row affected (0.02 sec)

INSERT INTO t VALUES(50);
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+----+
| a  |
+----+
|  1 |
| 50 |
+----+
2 rows in set (0.01 sec)
```

```sql
ALTER TABLE t AUTO_INCREMENT = 0;
Query OK, 0 rows affected, 1 warning (0.07 sec)

SHOW WARNINGS;
+---------+------+-------------------------------------------------------------------------+
| Level   | Code | Message                                                                 |
+---------+------+-------------------------------------------------------------------------+
| Warning | 1105 | Can't reset AUTO_INCREMENT to 0 without FORCE option, using 101 instead |
+---------+------+-------------------------------------------------------------------------+
1 row in set (0.01 sec)

INSERT INTO t VALUES();
Query OK, 1 row affected (0.02 sec)

SELECT * FROM t;
+-----+
| a   |
+-----+
|   1 |
|  50 |
| 101 |
+-----+
3 rows in set (0.01 sec)
```

### 自增步长和偏移量

从 v3.0.9 和 v4.0.0-rc.1 开始，与 MySQL 的行为类似，隐式分配给自增列的值由 `@@auto_increment_increment` 和 `@@auto_increment_offset` 会话变量控制。

隐式分配给自增列的值（ID）满足以下等式：

`(ID - auto_increment_offset) % auto_increment_increment == 0`

## MySQL 兼容模式

TiDB 为自增列提供了一个 MySQL 兼容模式，可确保 ID 严格递增且间隙最小。要启用此模式，在创建表时将 `AUTO_ID_CACHE` 设置为 `1`：

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
```

当 `AUTO_ID_CACHE` 设置为 `1` 时，ID 在所有 TiDB 实例上严格递增，每个 ID 都保证是唯一的，并且与默认缓存模式（`AUTO_ID_CACHE 0` 缓存 30000 个值）相比，ID 之间的间隙最小。

例如，使用 `AUTO_ID_CACHE 1` 时，你可能会看到如下序列：

```sql
INSERT INTO t VALUES (); -- 返回 ID 1
INSERT INTO t VALUES (); -- 返回 ID 2
INSERT INTO t VALUES (); -- 返回 ID 3
-- 故障转移后
INSERT INTO t VALUES (); -- 可能返回 ID 5
```

相比之下，使用默认缓存（`AUTO_ID_CACHE 0`）时，可能会出现更大的间隙：

```sql
INSERT INTO t VALUES (); -- 返回 ID 1
INSERT INTO t VALUES (); -- 返回 ID 2
-- 新的 TiDB 实例分配下一批
INSERT INTO t VALUES (); -- 返回 ID 30001
```

虽然 ID 始终递增且没有像 `AUTO_ID_CACHE 0` 那样的显著间隙，但在以下场景中序列中可能仍会出现小的间隙。这些间隙是必要的，以维持 ID 的唯一性和严格递增的特性。

- 主实例退出或崩溃时的故障转移期间

    启用 MySQL 兼容模式后，分配的 ID 是**唯一**且**单调递增**的，行为与 MySQL 几乎相同。即使跨多个 TiDB 实例访问，也保持 ID 的单调性。但是，如果中心化服务的主实例崩溃，少数 ID 可能会变得不连续。这是因为在故障转移期间，备用实例会丢弃主实例分配的一些 ID，以确保 ID 的唯一性。

- TiDB 节点滚动升级期间
- 正常并发事务期间（与 MySQL 类似）

> **注意：**
>
> `AUTO_ID_CACHE 1` 的行为和性能在不同的 TiDB 版本中有所演变：
>
> - v6.4.0 之前，每次 ID 分配都需要一个 TiKV 事务，这会影响性能。
> - 在 v6.4.0 中，TiDB 引入了中心化分配服务，将 ID 分配作为内存操作执行，显著提高了性能。
> - 从 v8.1.0 开始，TiDB 在主节点退出时移除了自动 `forceRebase` 操作，以实现更快的重启。虽然这可能在故障转移期间导致额外的非连续 ID，但它可以防止当许多表使用 `AUTO_ID_CACHE 1` 时可能出现的写入阻塞。

## 限制

目前，在 TiDB 中使用 `AUTO_INCREMENT` 有以下限制：

- 对于 TiDB v6.6.0 及更早版本，定义的列必须是主键或索引前缀。
- 必须定义在 `INTEGER`、`FLOAT` 或 `DOUBLE` 类型的列上。
- 不能在同一列上同时指定 `DEFAULT` 列值。
- 不能使用 `ALTER TABLE` 添加或修改带有 `AUTO_INCREMENT` 属性的列，包括使用 `ALTER TABLE ... MODIFY/CHANGE COLUMN` 为现有列添加 `AUTO_INCREMENT` 属性，或使用 `ALTER TABLE ... ADD COLUMN` 添加带有 `AUTO_INCREMENT` 属性的列。
- 可以使用 `ALTER TABLE` 移除 `AUTO_INCREMENT` 属性。但是，从 v2.1.18 和 v3.0.4 开始，TiDB 使用会话变量 `@@tidb_allow_remove_auto_inc` 来控制是否可以使用 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 移除列的 `AUTO_INCREMENT` 属性。默认情况下，不能使用 `ALTER TABLE MODIFY` 或 `ALTER TABLE CHANGE` 移除 `AUTO_INCREMENT` 属性。
- `ALTER TABLE` 需要 `FORCE` 选项才能将 `AUTO_INCREMENT` 值设置为较小的值。
- 将 `AUTO_INCREMENT` 设置为小于 `MAX(<auto_increment_column>)` 的值会导致重复键，因为不会跳过已存在的值。
