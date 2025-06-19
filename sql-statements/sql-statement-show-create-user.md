---
title: SHOW CREATE USER | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW CREATE USER 的使用概览。
---

# SHOW CREATE USER

该语句显示如何使用 `CREATE USER` 语法重新创建用户。

## 语法图

```ebnf+diagram
ShowCreateUserStmt ::=
    "SHOW" "CREATE" "USER" (Username ("@" Hostname)? | "CURRENT_USER" ( "(" ")" )? )
```

## 示例

```sql
mysql> SHOW CREATE USER 'root';
+--------------------------------------------------------------------------------------------------------------------------+
| CREATE USER for root@%                                                                                                   |
+--------------------------------------------------------------------------------------------------------------------------+
| CREATE USER 'root'@'%' IDENTIFIED WITH 'mysql_native_password' AS '' REQUIRE NONE PASSWORD EXPIRE DEFAULT ACCOUNT UNLOCK |
+--------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> SHOW GRANTS FOR 'root';
+-------------------------------------------+
| Grants for root@%                         |
+-------------------------------------------+
| GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' |
+-------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

<CustomContent platform="tidb">

* `SHOW CREATE USER` 的输出设计为与 MySQL 匹配，但 TiDB 尚未支持几个 `CREATE` 选项。尚未支持的选项将被解析但被忽略。更多详细信息，请参见[安全兼容性](/security-compatibility-with-mysql.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* `SHOW CREATE USER` 的输出设计为与 MySQL 匹配，但 TiDB 尚未支持几个 `CREATE` 选项。尚未支持的选项将被解析但被忽略。更多详细信息，请参见[安全兼容性](https://docs.pingcap.com/tidb/stable/security-compatibility-with-mysql/)。

</CustomContent>

## 另请参阅

* [CREATE USER](/sql-statements/sql-statement-create-user.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [DROP USER](/sql-statements/sql-statement-drop-user.md)
