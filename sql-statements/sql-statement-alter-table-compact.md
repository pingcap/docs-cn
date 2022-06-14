---
title: ALTER TABLE ... COMPACT
summary: TiDB 数据库中 ALTER TABLE ... COMPACT 语句的使用概况。
---

# ALTER TABLE ... COMPACT

> **警告：**
>
> 该语句目前是实验性功能，不建议在生产环境中使用。

TiDB 存储节点在后台会自动发起数据整理（Compaction）。数据整理时，表中的物理数据会被重写，如清理已删除的数据、合并多版本数据等，从而可以获得更高的访问性能，并减少磁盘空间占用。使用 `ALTER TABLE ... COMPACT` 语句可以立即对指定的表进行数据整理，而无需等待后台触发。

该语句执行时不会阻塞现有 SQL 语句的执行或 TiDB 功能的使用，包括事务、DDL、GC 等，也不会改变通过 SQL 语句访问获得的数据内容。但执行过程中会占用一定量的 IO 及 CPU 资源，可能对业务延迟造成影响。

该语句会等待表中所有副本都数据整理完毕后才结束运行并返回。在执行过程中，你可以通过 [`KILL`](/sql-statements/sql-statement-kill.md) 语句安全地中断本张表的数据整理过程。中断不会破坏数据一致性或丢失数据，也不会影响后续重新发起或自动触发后台数据整理。

目前该语句仅支持对 TiFlash 进行数据整理，不支持对 TiKV 进行数据整理。

## 语法图

```ebnf+diagram
AlterTableCompactStmt ::=
    'ALTER' 'TABLE' TableName 'COMPACT' 'TIFLASH' 'REPLICA'
```

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

## MySQL 兼容性

`ALTER TABLE ... COMPACT` 语法是 TiDB 引入的对标准 SQL 语法的扩展。尽管没有对应的 MySQL 语法，但你仍然可通过 MySQL 各版本客户端，或各个遵循 MySQL 协议的数据库驱动执行该语句。

## TiDB Binlog 及 TiCDC 兼容性

`ALTER TABLE ... COMPACT` 语句不会导致逻辑数据变化，因而不会被 TiDB Binlog 及 TiCDC 同步到下游。

## 另请参阅

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)
- [KILL](/sql-statements/sql-statement-kill.md)
