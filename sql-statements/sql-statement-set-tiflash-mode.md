---
title: ALTER TABLE ... SET TIFLASH MODE ...
summary: TiDB 数据库中 ALTER TABLE ... SET TIFLASH MODE ... 语句的使用概况。
---

# `ALTER TABLE ... SET TIFLASH MODE ...`

> **警告：**
>
> 该语句目前是实验性功能，不建议在生产环境中使用。

使用 `ALTER TABLE ... SET TIFLASH MODE ...` 语句可以切换对应表在 TiFlash 中的模式状态。目前支持以下模式：

- `Normal Mode` 模式。默认模式。该模式能够保证查询结果精度以及数据一致性。
- `Fast Mode` 模式。该模式不保证查询结果精度和数据一致性，但可以实现更高效的查询性能。

该语句执行时不会阻塞现有 SQL 语句的执行或 TiDB 功能的使用，包括事务、DDL、GC 等，也不会改变通过 SQL 语句访问获得的数据内容。该语句会在模式切换完毕后正常结束。

该语句仅支持对表在 TiFlash 中的模式进行修改，因此模式修改后也仅对涉及到 TiFlash 表部分的读取产生对应模式的影响。

对表 TiFlash 模式的修改在表具有 TiFlash Replica 时才真实生效。若修改模式时，表的 TiFlash Replica 为空，则需等后续重新设置表的 TiFlash Replica 后修改的模式才真正生效。你可以使用 [`ALTER TABLE ... SET TIFLASH REPLICA ...`](/sql-statements/sql-statement-alter-table.md) 语句来设置表的 TiFlash Replica。

可以通过系统表 `information_schema.tiflash_replica` 查询对应表目前的 TiFlash table mode。

## 语法图

```ebnf+diagram
AlterTableSetTiFlashModeStmt ::=
    'ALTER' 'TABLE' TableName 'SET' 'TIFLASH' 'MODE' mode
```

## 示例

假设表 `test` 有一个 TiFlash 副本。

{{< copyable "sql" >}}

```sql
USE TEST;

CREATE TABLE test (a INT NOT NULL, b INT);

ALTER TABLE test SET TIFLASH REPLICA 1;
```

`test` 表默认的模式为 Normal Mode。你可以通过以下语句查询该表的 table mode：

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

如果要启用 Fast Mode 查询 `test` 表，执行以下语句来切换模式，并查询当前表的模式。

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

如果想重新使用 Normal Mode，执行以下语句切换。

```sql
ALTER TABLE test SET tiflash mode NORMAL
```

## MySQL 兼容性

`ALTER TABLE ...SET TiFLASH MODE ...`  语法是 TiDB 引入的对标准 SQL 语法的扩展。尽管没有对应的 MySQL 语法，你仍然可通过 MySQL 各版本客户端，或各个遵循 MySQL 协议的数据库驱动执行该语句。

## TiDB Binlog 及 TiCDC 兼容性

当下游也为 TiDB 时，`ALTER TABLE ...SET TiFLASH MODE ..` 会被 TiDB Binlog 同步到下游。其他场景下，TiDB Binlog 不会同步该语句。

Fast Mode 不支持 TiCDC。

## 另请参阅

- [ALTER TABLE](/sql-statements/sql-statement-alter-table.md)