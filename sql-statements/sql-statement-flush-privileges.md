---
title: FLUSH PRIVILEGES
summary: TiDB 数据库中 FLUSH PRIVILEGES 的使用概况。
---

# FLUSH PRIVILEGES

`FLUSH PRIVILEGES` 语句可触发 TiDB 从权限表中重新加载权限的内存副本。在对如 `mysql.user` 一类的表进行手动编辑后，应当执行 `FLUSH PRIVILEGES`。使用如 `GRANT` 或 `REVOKE` 一类的权限语句后，不需要执行 `FLUSH PRIVILEGES` 语句。执行 `FLUSH PRIVILEGES` 语句的用户需要拥有 `RELOAD` 权限。

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

{{< copyable "sql" >}}

```sql
FLUSH PRIVILEGES;
```

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

`FLUSH PRIVILEGES` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)
* [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
* [Privilege Management](/privilege-management.md)
