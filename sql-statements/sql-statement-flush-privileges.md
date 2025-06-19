---
title: FLUSH PRIVILEGES | TiDB SQL 语句参考
summary: TiDB 数据库中 FLUSH PRIVILEGES 的使用概述。
---

# FLUSH PRIVILEGES

`FLUSH PRIVILEGES` 语句指示 TiDB 从权限表重新加载内存中的权限副本。在手动编辑如 `mysql.user` 等表后，你必须执行此语句。但是，在使用 `GRANT` 或 `REVOKE` 等权限语句后，不需要执行此语句。执行此语句需要 `RELOAD` 权限。

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
|   LogTypeOpt 'LOGS'
|   TableOrTables TableNameListOpt WithReadLockOpt
```

## 示例

```sql
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

TiDB 中的 `FLUSH PRIVILEGES` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

* [权限管理](/privilege-management.md)

</CustomContent>
