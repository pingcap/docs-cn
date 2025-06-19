---
title: FLUSH TABLES | TiDB SQL 语句参考
summary: TiDB 数据库中 FLUSH TABLES 的使用概览。
---

# FLUSH TABLES

该语句是为了与 MySQL 兼容而包含的。在 TiDB 中没有实际用途。

## 语法图

```ebnf+diagram
FlushStmt ::=
    'FLUSH' NoWriteToBinLogAliasOpt FlushOption

NoWriteToBinLogAliasOpt ::=
    ( 'NO_WRITE_TO_BINLOG' | 'LOCAL' )?

FlushOption ::=
    'PRIVILEGES'
|   'STATUS'
|    'TIDB' 'PLUGINS' PluginNameList
|    'HOSTS'
|    LogTypeOpt 'LOGS'
|    TableOrTables TableNameListOpt WithReadLockOpt

LogTypeOpt ::=
    ( 'BINARY' | 'ENGINE' | 'ERROR' | 'GENERAL' | 'SLOW' )?

TableOrTables ::=
    'TABLE'
|   'TABLES'

TableNameListOpt ::=
    TableNameList?

WithReadLockOpt ::=
    ( 'WITH' 'READ' 'LOCK' )?
```

## 示例

```sql
mysql> FLUSH TABLES;
Query OK, 0 rows affected (0.00 sec)

mysql> FLUSH TABLES WITH READ LOCK;
ERROR 1105 (HY000): FLUSH TABLES WITH READ LOCK is not supported.  Please use @@tidb_snapshot
```

## MySQL 兼容性

* TiDB 没有 MySQL 中表缓存的概念。因此，为了兼容性，TiDB 会解析但忽略 `FLUSH TABLES`。
* 语句 `FLUSH TABLES WITH READ LOCK` 会产生错误，因为 TiDB 目前不支持锁定表。建议使用[历史读取](/read-historical-data.md)来代替。

## 另请参阅

* [读取历史数据](/read-historical-data.md)
