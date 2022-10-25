---
title: ALTER TABLE ... COMPACT
summary: TiDB 数据库中 ALTER TABLE ... COMPACT 语句的使用概况。
---

# ALTER TABLE ... COMPACT

TiDB 存储节点在后台会自动发起数据整理（Compaction）。数据整理时，表中的物理数据会被重写，如清理已删除的数据、合并多版本数据等，从而可以获得更高的访问性能，并减少磁盘空间占用。使用 `ALTER TABLE ... COMPACT` 语句可以立即对指定的表进行数据整理，而无需等待后台触发。

该语句执行时不会阻塞现有 SQL 语句的执行或 TiDB 功能的使用，包括事务、DDL、GC 等，也不会改变通过 SQL 语句访问获得的数据内容。该语句执行时会消耗一定量的 IO 及 CPU 资源，请注意选择合适的时机执行，如资源空闲时段，避免对业务造成负面影响。

该语句会等待表中所有副本都数据整理完毕后才结束运行并返回。在执行过程中，你可以通过 [`KILL`](/sql-statements/sql-statement-kill.md) 语句安全地中断本张表的数据整理过程。中断不会破坏数据一致性或丢失数据，也不会影响后续重新发起或自动触发后台数据整理。

目前该语句仅支持对 TiFlash 进行数据整理，不支持对 TiKV 进行数据整理。

## 语法图

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' ( 'TIFLASH' 'REPLICA' )?
```

自 v6.2.0 起，语法中 `TIFLASH REPLICA` 部分可以被省略。省略后语句含义不变，同样只对 TiFlash 列存有效。

## 示例

### 对表中 TiFlash 副本进行数据整理

假设目前有一张 `employees` 表具有 4 个分区，且具有 2 个 TiFlash 副本：

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

执行以下语句可对 `employees` 表上所有分区的 2 个 TiFlash 副本立即进行数据整理：

{{< copyable "sql" >}}

```sql
ALTER TABLE employees COMPACT TIFLASH REPLICA;
```

## 并发度

`ALTER TABLE ... COMPACT` 语句会同时对表中所有副本发起数据整理操作。

为了避免数据整理操作对在线业务造成显著影响，在同一时间，每个 TiFlash 实例默认只会处理一张表的数据整理操作（后台自动触发的数据整理除外）。这意味着，若你同时对多张表执行 `ALTER TABLE ... COMPACT` 语句，则它们在同一个 TiFlash 实例上会排队依次执行，而非同时执行。

你可以修改 TiFlash 配置文件参数 [`manual_compact_pool_size`](/tiflash/tiflash-configuration.md)，以更大资源占用为代价、获得更大的表级别并发度。例如，参数指定为 2 时，可以同时对 2 张表进行数据整理。

## 观测数据整理进度

你可以通过 `INFORMATION_SCHEMA.TIFLASH_TABLES` 表中 `TOTAL_DELTA_ROWS` 列来观测 TiFlash 存储引擎上数据整理的进度，或判断是否有必要对某张表发起数据整理。`TOTAL_DELTA_ROWS` 的值越大，说明还能被整理的数据越多；若 `TOTAL_DELTA_ROWS` 为 `0`，说明表中所有数据都处于最佳状态，无需整理。

<details>
  <summary>示例：查询普通表的数据整理状态</summary>

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
-- 新写入的数据可被整理

ALTER TABLE foo COMPACT TIFLASH REPLICA;

SELECT TOTAL_DELTA_ROWS, TOTAL_STABLE_ROWS FROM INFORMATION_SCHEMA.TIFLASH_TABLES
    WHERE IS_TOMBSTONE = 0 AND
    `TIDB_DATABASE` = "test" AND `TIDB_TABLE` = "foo";
+------------------+-------------------+
| TOTAL_DELTA_ROWS | TOTAL_STABLE_ROWS |
+------------------+-------------------+
|                0 |                 3 |
+------------------+-------------------+
-- 所有数据都处于最佳整理状态
```

</details>

<details>
  <summary>示例：查询分区表的数据整理状态</summary>

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
-- 一些分区上有数据可被整理

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
-- 所有分区上的数据都处于最佳整理状态
```

</details>

> **注意：**
>
> - 若数据整理的过程中发生了数据更新，你可能观察到数据整理完毕后 `TOTAL_DELTA_ROWS` 仍为非零值。这是正常现象，表明这些更新部分没有被整理到。若你想对这部分更新数据也进行整理，可再次执行 `ALTER TABLE ... COMPACT` 语句。
>
> - `TOTAL_DELTA_ROWS` 的单位是数据版本数，而非数据行数。例如，插入一行记录再删除该行后，`TOTAL_DELTA_ROWS` 会增加 2。

## 兼容性

### MySQL 兼容性

`ALTER TABLE ... COMPACT` 语法是 TiDB 引入的对标准 SQL 语法的扩展。尽管没有对应的 MySQL 语法，但你仍然可通过 MySQL 各版本客户端，或各个遵循 MySQL 协议的数据库驱动执行该语句。

### TiDB Binlog 及 TiCDC 兼容性

`ALTER TABLE ... COMPACT` 语句不会导致逻辑数据变化，因而不会被 TiDB Binlog 及 TiCDC 同步到下游。

## 另请参阅

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
- [KILL](/sql-statements/sql-statement-kill.md)
