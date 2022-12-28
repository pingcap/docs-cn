---
title: REVOKE <privileges>
summary: TiDB 数据库中 REVOKE <privileges> 的使用概况。
---

# `REVOKE <privileges>`

`REVOKE <privileges>` 语句用于删除已有用户的权限。执行 `REVOKE <privileges>` 语句需要拥有分配的权限，并且拥有 `GRANT OPTION` 权限。

## 语法图

```ebnf+diagram
GrantStmt ::=
    'GRANT' PrivElemList 'ON' ObjectType PrivLevel 'TO' UserSpecList RequireClauseOpt WithGrantOptionOpt

PrivElemList ::=
    PrivElem ( ',' PrivElem )*

PrivElem ::=
    PrivType ( '(' ColumnNameList ')' )?

PrivType ::=
    'ALL' 'PRIVILEGES'?
|   'ALTER' 'ROUTINE'?
|   'CREATE' ( 'USER' | 'TEMPORARY' 'TABLES' | 'VIEW' | 'ROLE' | 'ROUTINE' )?
|    'TRIGGER'
|   'DELETE'
|    'DROP' 'ROLE'?
|    'PROCESS'
|    'EXECUTE'
|   'INDEX'
|   'INSERT'
|   'SELECT'
|   'SUPER'
|    'SHOW' ( 'DATABASES' | 'VIEW' )
|   'UPDATE'
|   'GRANT' 'OPTION'
|   'REFERENCES'
|   'REPLICATION' ( 'SLAVE' | 'CLIENT' )
|   'USAGE'
|    'RELOAD'
|   'FILE'
|   'CONFIG'
|   'LOCK' 'TABLES'
|    'EVENT'
|   'SHUTDOWN'

ObjectType ::=
    'TABLE'?

PrivLevel ::=
    '*' ( '.' '*' )?
|    Identifier ( '.' ( '*' | Identifier ) )?

UserSpecList ::=
    UserSpec ( ',' UserSpec )*
```

## 示例

{{< copyable "sql" >}}

```sql
CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
```

```
Query OK, 1 row affected (0.02 sec)
```

{{< copyable "sql" >}}

```sql
GRANT ALL ON test.* TO 'newuser';
```

```
Query OK, 0 rows affected (0.03 sec)
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'newuser';
```

```
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
REVOKE ALL ON test.* FROM 'newuser';
```

```
Query OK, 0 rows affected (0.03 sec)
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'newuser';
```

```
+-------------------------------------+
| Grants for newuser@%                |
+-------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%' |
+-------------------------------------+
1 row in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
DROP USER 'newuser';
```

```
Query OK, 0 rows affected (0.14 sec)
```

{{< copyable "sql" >}}

```sql
SHOW GRANTS FOR 'newuser';
```

```
ERROR 1141 (42000): There is no such grant defined for user 'newuser' on host '%'
```

## MySQL 兼容性

`REVOKE <privileges>` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请在 GitHub 上提交 [issue](https://github.com/pingcap/tidb/issues/new/choose)。

## 另请参阅

* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [Privilege Management](/privilege-management.md)
