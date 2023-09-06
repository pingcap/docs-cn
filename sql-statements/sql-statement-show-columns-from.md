---
title: SHOW [FULL] COLUMNS FROM | TiDB SQL Statement Reference
summary: An overview of the usage of SHOW [FULL] COLUMNS FROM for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-columns-from/','/docs/dev/reference/sql/statements/show-columns-from/']
---

# SHOW [FULL] COLUMNS FROM

The statement `SHOW [FULL] COLUMNS FROM <table_name>` describes the columns of a table or view in a useful tabular format. The optional keyword `FULL` displays the privileges the current user has to that column, and the `comment` from the table definition.

The statements `SHOW [FULL] FIELDS FROM <table_name>`, `DESC <table_name>`, `DESCRIBE <table_name>`, and `EXPLAIN <table_name>` are aliases of this statement.

> **Note:**
>
> `DESC TABLE <table_name>`, `DESCRIBE TABLE <table_name>`, and `EXPLAIN TABLE <table_name>` are not equivalent to the above statements. They are aliases of [`DESC SELECT * FROM <table_name>`](/sql-statements/sql-statement-explain.md).

## Synopsis

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowColumnsFilterable:**

![ShowColumnsFilterable](/media/sqlgram/ShowColumnsFilterable.png)

**OptFull:**

![OptFull](/media/sqlgram/OptFull.png)

**FieldsOrColumns:**

![FieldsOrColumns](/media/sqlgram/FieldsOrColumns.png)

**ShowTableAliasOpt:**

![ShowTableAliasOpt](/media/sqlgram/ShowTableAliasOpt.png)

**FromOrIn:**

![FromOrIn](/media/sqlgram/FromOrIn.png)

**TableName:**

![TableName](/media/sqlgram/TableName.png)

**ShowDatabaseNameOpt:**

![ShowDatabaseNameOpt](/media/sqlgram/ShowDatabaseNameOpt.png)

**DBName:**

![DBName](/media/sqlgram/DBName.png)

**ShowLikeOrWhereOpt:**

![ShowLikeOrWhereOpt](/media/sqlgram/ShowLikeOrWhereOpt.png)

## Examples

```sql
mysql> create view v1 as select 1;
Query OK, 0 rows affected (0.11 sec)

mysql> show columns from v1;
+-------+-----------+------+------+---------+-------+
| Field | Type      | Null | Key  | Default | Extra |
+-------+-----------+------+------+---------+-------+
| 1     | bigint(1) | YES  |      | NULL    |       |
+-------+-----------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> desc v1;
+-------+-----------+------+------+---------+-------+
| Field | Type      | Null | Key  | Default | Extra |
+-------+-----------+------+------+---------+-------+
| 1     | bigint(1) | YES  |      | NULL    |       |
+-------+-----------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> describe v1;
+-------+-----------+------+------+---------+-------+
| Field | Type      | Null | Key  | Default | Extra |
+-------+-----------+------+------+---------+-------+
| 1     | bigint(1) | YES  |      | NULL    |       |
+-------+-----------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> explain v1;
+-------+-----------+------+------+---------+-------+
| Field | Type      | Null | Key  | Default | Extra |
+-------+-----------+------+------+---------+-------+
| 1     | bigint(1) | YES  |      | NULL    |       |
+-------+-----------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> show fields from v1;
+-------+-----------+------+------+---------+-------+
| Field | Type      | Null | Key  | Default | Extra |
+-------+-----------+------+------+---------+-------+
| 1     | bigint(1) | YES  |      | NULL    |       |
+-------+-----------+------+------+---------+-------+
1 row in set (0.00 sec)

mysql> show full columns from v1;
+-------+-----------+-----------+------+------+---------+-------+---------------------------------+---------+
| Field | Type      | Collation | Null | Key  | Default | Extra | Privileges                      | Comment |
+-------+-----------+-----------+------+------+---------+-------+---------------------------------+---------+
| 1     | bigint(1) | NULL      | YES  |      | NULL    |       | select,insert,update,references |         |
+-------+-----------+-----------+------+------+---------+-------+---------------------------------+---------+
1 row in set (0.00 sec)

mysql> show full columns from mysql.user;
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

## MySQL compatibility

The `SHOW [FULL] COLUMNS FROM` statement in TiDB is fully compatible with MySQL. If you find any compatibility differences, [report a bug](https://docs.pingcap.com/tidb/stable/support).

## See also

* [SHOW CREATE TABLE](/sql-statements/sql-statement-show-create-table.md)
