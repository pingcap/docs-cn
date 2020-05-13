---
title: FLUSH TABLES
summary: TiDB 数据库中 FLUSH TABLES 的使用概况。
category: reference
---

# FLUSH TABLES

`FLUSH TABLES` 语句用于提供 MySQL 兼容性，但在 TiDB 中并无有效用途。

## 语法图

**FlushStmt:**

![FlushStmt](/media/sqlgram/FlushStmt.png)

**NoWriteToBinLogAliasOpt:**

![NoWriteToBinLogAliasOpt](/media/sqlgram/NoWriteToBinLogAliasOpt.png)

**FlushOption:**

![FlushOption](/media/sqlgram/FlushOption.png)

**TableOrTables:**

![TableOrTables](/media/sqlgram/TableOrTables.png)

**TableNameListOpt:**

![TableNameListOpt](/media/sqlgram/TableNameListOpt.png)

**WithReadLockOpt:**

![WithReadLockOpt](/media/sqlgram/WithReadLockOpt.png)

## 示例

{{< copyable "sql" >}}

```sql
FLUSH TABLES;
```

```
Query OK, 0 rows affected (0.00 sec)
```

{{< copyable "sql" >}}

```sql
FLUSH TABLES WITH READ LOCK;
```

```
ERROR 1105 (HY000): FLUSH TABLES WITH READ LOCK is not supported.  Please use @@tidb_snapshot
```

## MySQL 兼容性

* TiDB 没有 MySQL 中的表缓存这一概念。所以，`FLUSH TABLES` 因 MySQL 兼容性会在 TiDB 中解析出但会被忽略掉。
* 因为 TiDB 目前不支持锁表，所以`FLUSH TABLES WITH READ LOCK` 语句会产生错误。建议使用 [Historical reads] 来实现锁表。

## 另请参阅

* [Read historical data](/how-to/get-started/read-historical-data.md)
