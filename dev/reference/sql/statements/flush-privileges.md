---
title: FLUSH PRIVILEGES
summary: TiDB 数据库中 FLUSH PRIVILEGES 的使用概况。
category: reference
---

# FLUSH PRIVILEGES

`FLUSH PRIVILEGES` 语句可触发 TiDB 从权限表中重新加载权限的内存副本。在对如 `mysql.user` 一类的表进行手动编辑后，应当执行 `FLUSH PRIVILEGES`。使用如 `GRANT` 或 `REVOKE` 一类的权限语句后，不需要执行 `FLUSH PRIVILEGES` 语句。

## 总览

**FlushStmt:**

![FlushStmt](/media/sqlgram/FlushStmt.png)

**NoWriteToBinLogAliasOpt:**

![NoWriteToBinLogAliasOpt](/media/sqlgram/NoWriteToBinLogAliasOpt.png)

**FlushOption:**

![FlushOption](/media/sqlgram/FlushOption.png)

## 实例

```sql
mysql> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.01 sec)
```

## MySQL 兼容性

`FLUSH PRIVILEGES` 语句可视为与 MySQL 完全兼容。如有任何兼容性差异，请在 GitHub 上 提交 [issue](/report-issue.md)。

## 另请参阅

* [GRANT](/dev/reference/sql/statements/grant.md)
* [REVOKE](/dev/reference/sql/statements/revoke.md)
* [Privilege Management](/dev/reference/security/privilege-system.md)