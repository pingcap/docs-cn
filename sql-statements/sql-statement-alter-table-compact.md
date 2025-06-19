---
title: ALTER TABLE ... COMPACT
summary: TiDB 数据库中 ALTER TABLE ... COMPACT 的使用概述。
---

# ALTER TABLE ... COMPACT

为了提高读取性能并减少磁盘使用，TiDB 会在后台自动调度存储节点上的数据压缩。在压缩过程中，存储节点会重写物理数据，包括清理已删除的行和合并由更新引起的多个数据版本。`ALTER TABLE ... COMPACT` 语句允许你立即对特定表启动压缩，而无需等待后台触发压缩。

执行此语句不会阻塞现有的 SQL 语句或影响任何 TiDB 功能，如事务、DDL 和 GC。通过 SQL 语句可以选择的数据也不会改变。执行此语句会消耗一些 IO 和 CPU 资源。请注意选择合适的执行时机，例如在资源充足时执行，以避免对业务产生负面影响。

当表的所有副本都压缩完成时，压缩语句将完成并返回。在执行过程中，你可以通过执行 [`KILL`](/sql-statements/sql-statement-kill.md) 语句安全地中断压缩。中断压缩不会破坏数据一致性或导致数据丢失，也不会影响后续的手动或后台压缩。

此数据压缩语句目前仅支持 TiFlash 副本，不支持 TiKV 副本。

## 语法概要

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' ( 'PARTITION' PartitionNameList )? ( 'TIFLASH' 'REPLICA' )?
```

从 v6.2.0 开始，语法中的 `TIFLASH REPLICA` 部分可以省略。省略时，语句的语义保持不变，仅对 TiFlash 生效。

## 示例

### 压缩表中的 TiFlash 副本

以下以一个具有 4 个分区和 2 个 TiFlash 副本的 `employees` 表为例：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);
ALTER TABLE employees SET TIFLASH REPLICA 2;
```

你可以执行以下语句立即对 `employees` 表中所有分区的 2 个 TiFlash 副本启动压缩：

{{< copyable "sql" >}}

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

### 压缩表中指定分区的 TiFlash 副本

以下以一个具有 4 个分区和 2 个 TiFlash 副本的 `employees` 表为例：

```sql
CREATE TABLE employees (
    id INT NOT NULL,
    hired DATE NOT NULL DEFAULT '1970-01-01',
    store_id INT
)
PARTITION BY LIST (store_id) (
    PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
    PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
    PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
    PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
);

ALTER TABLE employees SET TIFLASH REPLICA 2;
```

你可以执行以下语句立即对 `employees` 表中 `pNorth` 和 `pEast` 分区的 2 个 TiFlash 副本启动压缩：

```sql
ALTER TABLE employees COMPACT PARTITION pNorth, pEast TIFLASH REPLICA;
```

## 并发性

`ALTER TABLE ... COMPACT` 语句同时压缩表中的所有副本。

为了避免对在线业务产生重大影响，默认情况下每个 TiFlash 实例一次只压缩一个表的数据（后台触发的压缩除外）。这意味着如果你同时对多个表执行 `ALTER TABLE ... COMPACT` 语句，它们的执行将在同一个 TiFlash 实例上排队，而不是同时执行。

<CustomContent platform="tidb">

要获得更高的表级并发性和更高的资源使用率，你可以修改 TiFlash 配置 [`manual_compact_pool_size`](/tiflash/tiflash-configuration.md)。例如，当 `manual_compact_pool_size` 设置为 2 时，可以同时处理 2 个表的压缩。

</CustomContent>

## 观察数据压缩进度

你可以通过检查 `INFORMATION_SCHEMA.TIFLASH_TABLES` 表中的 `TOTAL_DELTA_ROWS` 列来观察数据压缩的进度或确定是否需要对表启动压缩。`TOTAL_DELTA_ROWS` 的值越大，可以压缩的数据就越多。如果 `TOTAL_DELTA_ROWS` 为 `0`，则表中的所有数据都处于最佳状态，不需要压缩。

<details>
  <summary>示例：检查非分区表的压缩状态</summary>

```sql
USE test;

CREATE TABLE foo(id INT);

ALTER TABLE foo SET TIFLASH REPLICA 1;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 0 |
+------------------+-------------------+

INSERT INTO foo VALUES (1), (3), (7);

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                3 |                 0 |
+------------------+-------------------+
-- 新写入的数据可以压缩

ALTER TABLE foo COMPACT TIFLASH REPLICA;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 3 |
+------------------+-------------------+
-- 所有数据都处于最佳状态，不需要压缩
```

</details>

<details>
  <summary>示例：检查分区表的压缩状态</summary>

```sql
USE test;

CREATE TABLE employees
    (id INT NOT NULL, store_id INT)
    PARTITION BY LIST (store_id) (
        PARTITION pNorth VALUES IN (1, 2, 3, 4, 5),
        PARTITION pEast VALUES IN (6, 7, 8, 9, 10),
        PARTITION pWest VALUES IN (11, 12, 13, 14, 15),
        PARTITION pCentral VALUES IN (16, 17, 18, 19, 20)
    );

ALTER TABLE employees SET TIFLASH REPLICA 1;

INSERT INTO employees VALUES (1, 1), (6, 6), (10, 10);

SELECT PARTITION_NAME, TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS
    FROM INFORMATION_SCHEMA.TIFLASH_TABLES t, INFORMATION_SCHEMA.PARTITIONS p
    WHERE t.IS_TOMBSTONE = 0 AND t.TABLE_ID = p.TIDB_PARTITION_ID AND
    p.TABLE_SCHEMA = "test" AND p.TABLE_NAME = "employees";
+----------------+------------------+-------------------+
| PARTITION_NAME | TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+----------------+------------------+-------------------+
| pNorth         |                1 |                 0 |
| pEast          |                2 |                 0 |
| pWest          |                0 |                 0 |
| pCentral       |                0 |                 0 |
+----------------+------------------+-------------------+
-- 某些分区可以压缩

ALTER TABLE employees COMPACT TIFLASH REPLICA;

SELECT PARTITION_NAME, TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS
    FROM INFORMATION_SCHEMA.TIFLASH_TABLES t, INFORMATION_SCHEMA.PARTITIONS p
    WHERE t.IS_TOMBSTONE = 0 AND t.TABLE_ID = p.TIDB_PARTITION_ID AND
    p.TABLE_SCHEMA = "test" AND p.TABLE_NAME = "employees";
+----------------+------------------+-------------------+
| PARTITION_NAME | TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+----------------+------------------+-------------------+
| pNorth         |                0 |                 1 |
| pEast          |                0 |                 2 |
| pWest          |                0 |                 0 |
| pCentral       |                0 |                 0 |
+----------------+------------------+-------------------+
-- 所有分区中的数据都处于最佳状态，不需要压缩
```

</details>

> **注意：**
>
> - 如果在压缩过程中更新了数据，压缩完成后 `TOTAL_DELTA_ROWS` 可能仍然是非零值。这是正常的，表示这些更新尚未被压缩。要压缩这些更新，请再次执行 `ALTER TABLE ... COMPACT` 语句。
>
> - `TOTAL_DELTA_ROWS` 表示数据版本，而不是行数。例如，如果你插入一行然后删除它，`TOTAL_DELTA_ROWS` 将增加 2。

## 兼容性

### MySQL 兼容性

`ALTER TABLE ... COMPACT` 语法是 TiDB 特有的，是对标准 SQL 语法的扩展。虽然没有等效的 MySQL 语法，但你仍然可以使用符合 MySQL 协议的 MySQL 客户端或各种数据库驱动程序执行此语句。

### TiDB Binlog 和 TiCDC 兼容性

`ALTER TABLE ... COMPACT` 语句不会导致逻辑数据更改，因此不会被 TiDB Binlog 或 TiCDC 复制到下游。

## 另请参阅

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
- [KILL TIDB](/sql-statements/sql-statement-kill.md)
