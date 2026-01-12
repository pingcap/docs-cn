---
title: SHOW [FULL] COLUMNS FROM
summary: TiDB 数据库中 SHOW [FULL] COLUMNS FROM 的使用概况。
aliases: ['/docs-cn/dev/sql-statements/sql-statement-show-columns-from/','/docs-cn/dev/reference/sql/statements/show-columns-from/']
---

# SHOW [FULL] COLUMNS FROM

`SHOW [FULL] COLUMNS FROM <table_name>` 语句用于以表格格式描述表或视图中的列。可选关键字 `FULL` 用于显示当前用户对该列的权限，以及表定义中的 `comment`。

`SHOW [FULL] FIELDS FROM <table_name>`、`DESC <table_name>`、`DESCRIBE <table_name>` 和 `EXPLAIN <table_name>` 语句都是 `SHOW [FULL] COLUMNS FROM` 的别名。

> **注意：**
>
> `DESC TABLE <table_name>`、`DESCRIBE TABLE <table_name>` 和 `EXPLAIN TABLE <table_name>` 与上面的语句并不等价，它们是 [`DESC SELECT * FROM <table_name>`](/sql-statements/sql-statement-explain.md) 的别名。

## 语法图

```ebnf+diagram
ShowColumnsFromStmt ::=
    "SHOW" "FULL"? ("COLUMNS" | "FIELDS") ("FROM" | "IN") TableName ( ("FROM" | "IN") SchemaName)? ShowLikeOrWhere?

TableName ::=
    (Identifier ".")? Identifier

ShowLikeOrWhere ::=
    "LIKE" SimpleExpr
|   "WHERE" Expression
```

## 示例

```sql
CREATE VIEW v1 AS SELECT 1;
```

```
Query OK, 0 rows affected (0.11 sec)
```

```sql
SHOW COLUMNS FROM v1;
```

```
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+--------+------+------+---------+-------+
1 row in set (0.00 sec)
```

```sql
DESC v1;
```

```
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+--------+------+------+---------+-------+
1 row in set (0.00 sec)
```

```sql
DESCRIBE v1;
```

```
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+-----------+------+------+---------+-------+
1 row in set (0.00 sec)
```

```sql
EXPLAIN v1;
```

```
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+--------+------+------+---------+-------+
1 row in set (0.00 sec)
```

```sql
SHOW FIELDS FROM v1;
```

```
+-------+--------+------+------+---------+-------+
| Field | Type   | Null | Key  | Default | Extra |
+-------+--------+------+------+---------+-------+
| 1     | bigint | YES  |      | NULL    |       |
+-------+--------+------+------+---------+-------+
1 row in set (0.00 sec)
```

```sql
SHOW FULL COLUMNS FROM v1
```

```
+-------+--------+-----------+------+------+---------+-------+---------------------------------+---------+
| Field | Type   | Collation | Null | Key  | Default | Extra | Privileges                      | Comment |
+-------+--------+-----------+------+------+---------+-------+---------------------------------+---------+
| 1     | bigint | NULL      | YES  |      | NULL    |       | select,insert,update,references |         |
+-------+--------+-----------+------+------+---------+-------+---------------------------------+---------+
1 row in set (0.00 sec)
```

```sql
SHOW FULL COLUMNS FROM mysql.user;
```

```
+------------------------+---------------+-------------+------+------+---------+-------+---------------------------------+---------+
| Field                  | Type          | Collation   | Null | Key  | Default | Extra | Privileges                      | Comment |
+------------------------+---------------+-------------+------+------+---------+-------+---------------------------------+---------+
| Host                   | char(255)     | utf8mb4_bin | NO   | PRI  | NULL    |       | select,insert,update,references |         |
| User                   | char(32)      | utf8mb4_bin | NO   | PRI  | NULL    |       | select,insert,update,references |         |
| authentication_string  | text          | utf8mb4_bin | YES  |      | NULL    |       | select,insert,update,references |         |
| plugin                 | char(64)      | utf8mb4_bin | YES  |      | NULL    |       | select,insert,update,references |         |
| Select_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Insert_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Update_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Delete_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Drop_priv              | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Process_priv           | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Grant_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| References_priv        | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Alter_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Show_db_priv           | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Super_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_tmp_table_priv  | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Lock_tables_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Execute_priv           | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_view_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Show_view_priv         | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_routine_priv    | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Alter_routine_priv     | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Index_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_user_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Event_priv             | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Repl_slave_priv        | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Repl_client_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Trigger_priv           | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_role_priv       | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Drop_role_priv         | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Account_locked         | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Shutdown_priv          | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Reload_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| FILE_priv              | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Config_priv            | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| Create_Tablespace_Priv | enum('N','Y') | utf8mb4_bin | NO   |      | N       |       | select,insert,update,references |         |
| User_attributes        | json          | NULL        | YES  |      | NULL    |       | select,insert,update,references |         |
+------------------------+---------------+-------------+------+------+---------+-------+---------------------------------+---------+
38 rows in set (0.00 sec)
```

## MySQL 兼容性

`SHOW [FULL] COLUMNS FROM` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
