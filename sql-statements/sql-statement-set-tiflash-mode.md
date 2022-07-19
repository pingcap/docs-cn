---
title: ALTER TABLE ... SET TIFLASH MODE ...
summary: TiDB 数据库中 ALTER TABLE ... SET TIFLASH MODE ... 语句的使用概况。
---

# `ALTER TABLE ... SET TIFLASH MODE ...`

> **警告：**
>
> 该语句目前是实验性功能，不建议在生产环境中使用。

使用 `ALTER TABLE ... SET TIFLASH MODE ...` 语句可以切换对应表在 TiFlash 中的模式状态。目前我们支持两种模式：`Normal Mode` 以及 `Fast Mode`。`Normal Mode`下，查询结果保证精度以及数据的一致性；`Fast Mode` 下则不保证数据精度和数据一致性，但提供更高效的查询性能。

该语句执行时不会阻塞现有 SQL 语句的执行或 TiDB 功能的使用，包括事务、DDL、GC 等，也不会改变通过 SQL 语句访问获得的数据内容。该语句会在模式切换完毕后返回。

该语句仅支持对表在 TiFlash 中的模式进行修改，因此模式修改后也仅对涉及到 TiFlash 表部分的读取产生对应模式的影响。

对表 TiFlash 模式的修改在表具有 TiFlash Replica 时才真实生效。若修改模式时，表的 TiFlash Replica 为空，则需等后续重新设置表的 TiFlash Replica 后修改的模式才真正生效。

我们可以通过 `information_schema.tiflash_replica` 这张系统表来查询对应表目前的 TiFlash table mode。

## 语法图

```ebnf+diagram
AlterTableSetTiFlashModeStmt ::=
    'ALTER' 'TABLE' TableName 'SET' 'TIFLASH' 'MODE' mode
```

## 示例

假设我们目前有张 `test` 表，它具有一个 TiFlash 副本。

{{< copyable "sql" >}}

```sql
USE TEST;

CREATE TABLE test (a INT NOT NULL, b INT);

ALTER TABLE test SET TIFLASH REPLICA 1;
```

`test` 表默认的 mode 为 Normal Mode，我们可以通过以下语句进行查询

```sql
SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'test' AND table_schema = 'test'
```

```
+------------+
| table_mode |
+------------+
| NORMAL     |
+------------+
```

当我们想启用 fast mode 来对表 test 进行查询时，执行以下语句来切换模式, 并可以重新查询当前表的 mode。

```sql
ALTER TABLE test SET tiflash mode FAST

SELECT table_mode FROM information_schema.tiflash_replica WHERE table_name = 'test' AND table_schema = 'test'
```

```
+------------+
| table_mode |
+------------+
| FAST       |
+------------+
```

当我们想重新使用 normal mode 模式时，执行以下语句将表切换回 normal 模式。

```sql
ALTER TABLE test SET tiflash mode NORMAL
```

## MySQL 兼容性

`ALTER TABLE ...SET TiFLASH MODE ..`  语法是 TiDB 引入的对标准 SQL 语法的扩展。尽管没有对应的 MySQL 语法，但你仍然可通过 MySQL 各版本客户端，或各个遵循 MySQL 协议的数据库驱动执行该语句。

## TiDB Binlog 及 TiCDC 兼容性

当 下游也为 TiDB 时，`ALTER TABLE ...SET TiFLASH MODE ..` 会被 TiDB Binlog 同步到下游。其他状态下，Binlog 和 TiCDC 都不会同步该语句。

## 另请参阅

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)