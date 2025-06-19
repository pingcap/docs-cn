---
title: GRANT <privileges> | TiDB SQL 语句参考
summary: TiDB 数据库中 GRANT <privileges> 的使用概览。
---

# `GRANT <privileges>`

此语句为 TiDB 中的已存在用户分配权限。TiDB 中的权限系统遵循 MySQL，其中凭据是基于数据库/表模式分配的。执行此语句需要 `GRANT OPTION` 权限和你分配的所有权限。

## 语法

```ebnf+diagram
GrantStmt ::=
    'GRANT' PrivElemList 'ON' ObjectType PrivLevel 'TO' UserSpecList RequireClauseOpt WithGrantOptionOpt

PrivElemList ::=
    PrivElem ( ',' PrivElem )*

PrivElem ::=
    PrivType ( '(' ColumnNameList ')' )?

PrivType ::=
    'ALL' 'PRIVILEGES'?
|    'ALTER' 'ROUTINE'?
|   'CREATE' ( 'USER' | 'TEMPORARY' 'TABLES' | 'VIEW' | 'ROLE' | 'ROUTINE' )?
|   'TRIGGER'
|   'DELETE'
|   'DROP' 'ROLE'?
|    'PROCESS'
|   'EXECUTE'
|   'INDEX'
|   'INSERT'
|   'SELECT'
|   'SUPER'
|   'SHOW' ( 'DATABASES' | 'VIEW' )
|   'UPDATE'
|    'GRANT' 'OPTION'
|    'REFERENCES'
|    'REPLICATION' ( 'SLAVE' | 'CLIENT' )
|    'USAGE'
|   'RELOAD'
|   'FILE'
|   'CONFIG'
|   'LOCK' 'TABLES'
|   'EVENT'
|   'SHUTDOWN'

ObjectType ::=
    'TABLE'?

PrivLevel ::=
    '*' ( '.' '*' )?
|    Identifier ( '.' ( '*' | Identifier ) )?

UserSpecList ::=
    UserSpec ( ',' UserSpec )*

RequireClauseOpt ::= ('REQUIRE' ('NONE' | 'SSL' | 'X509' | RequireListElement ('AND'? RequireListElement)*))?

RequireListElement ::= 'ISSUER' Issuer | 'SUBJECT' Subject | 'CIPHER' Cipher | 'SAN' SAN | 'TOKEN_ISSUER' TokenIssuer
```

## 示例

```sql
mysql> CREATE USER 'newuser' IDENTIFIED BY 'mypassword';
Query OK, 1 row affected (0.02 sec)

mysql> GRANT ALL ON test.* TO 'newuser';
Query OK, 0 rows affected (0.03 sec)

mysql> SHOW GRANTS FOR 'newuser';
+-------------------------------------------------+
| Grants for newuser@%                            |
+-------------------------------------------------+
| GRANT USAGE ON *.* TO 'newuser'@'%'             |
| GRANT ALL PRIVILEGES ON test.* TO 'newuser'@'%' |
+-------------------------------------------------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

* 与 MySQL 类似，`USAGE` 权限表示登录 TiDB 服务器的能力。
* 目前不支持列级权限。
* 与 MySQL 类似，当不存在 `NO_AUTO_CREATE_USER` SQL 模式时，如果用户不存在，`GRANT` 语句将自动创建一个空密码的新用户。移除此 SQL 模式（默认启用）会带来安全风险。
* 在 TiDB 中，`GRANT <privileges>` 语句成功执行后，执行结果会立即在当前连接上生效。而[在 MySQL 中，对于某些权限，执行结果仅在后续连接中生效](https://dev.mysql.com/doc/refman/8.0/en/privilege-changes.html)。详情请参见 [TiDB #39356](https://github.com/pingcap/tidb/issues/39356)。

## 另请参阅

* [`GRANT <role>`](/sql-statements/sql-statement-grant-role.md)
* [`REVOKE <privileges>`](/sql-statements/sql-statement-revoke-privileges.md)
* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)

<CustomContent platform="tidb">

* [权限管理](/privilege-management.md)

</CustomContent>
