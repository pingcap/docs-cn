---
title: SHOW PRIVILEGES
summary: TiDB 数据库中 SHOW PRIVILEGES 的使用概况。
---

# SHOW PRIVILEGES

`SHOW PRIVILEGES` 语句用于显示 TiDB 中可分配权限的列表。此列表为静态列表，不反映当前用户的权限。

## 语法图

```ebnf+diagram
ShowPrivilegesStmt ::=
    "SHOW" "PRIVILEGES"
```

## 示例

```sql
SHOW PRIVILEGES;
```

```sql
+---------------------------------+---------------------------------------+-------------------------------------------------------+
| Privilege                       | Context                               | Comment                                               |
+---------------------------------+---------------------------------------+-------------------------------------------------------+
| Alter                           | Tables                                | To alter the table                                    |
| Alter routine                   | Functions,Procedures                  | To alter or drop stored functions/procedures          |
| Config                          | Server Admin                          | To use SHOW CONFIG and SET CONFIG statements          |
| Create                          | Databases,Tables,Indexes              | To create new databases and tables                    |
| Create routine                  | Databases                             | To use CREATE FUNCTION/PROCEDURE                      |
| Create role                     | Server Admin                          | To create new roles                                   |
| Create temporary tables         | Databases                             | To use CREATE TEMPORARY TABLE                         |
| Create view                     | Tables                                | To create new views                                   |
| Create user                     | Server Admin                          | To create new users                                   |
| Delete                          | Tables                                | To delete existing rows                               |
| Drop                            | Databases,Tables                      | To drop databases, tables, and views                  |
| Drop role                       | Server Admin                          | To drop roles                                         |
| Event                           | Server Admin                          | To create, alter, drop and execute events             |
| Execute                         | Functions,Procedures                  | To execute stored routines                            |
| File                            | File access on server                 | To read and write files on the server                 |
| Grant option                    | Databases,Tables,Functions,Procedures | To give to other users those privileges you possess   |
| Index                           | Tables                                | To create or drop indexes                             |
| Insert                          | Tables                                | To insert data into tables                            |
| Lock tables                     | Databases                             | To use LOCK TABLES (together with SELECT privilege)   |
| Process                         | Server Admin                          | To view the plain text of currently executing queries |
| Proxy                           | Server Admin                          | To make proxy user possible                           |
| References                      | Databases,Tables                      | To have references on tables                          |
| Reload                          | Server Admin                          | To reload or refresh tables, logs and privileges      |
| Replication client              | Server Admin                          | To ask where the slave or master servers are          |
| Replication slave               | Server Admin                          | To read binary log events from the master             |
| Select                          | Tables                                | To retrieve rows from table                           |
| Show databases                  | Server Admin                          | To see all databases with SHOW DATABASES              |
| Show view                       | Tables                                | To see views with SHOW CREATE VIEW                    |
| Shutdown                        | Server Admin                          | To shut down the server                               |
| Super                           | Server Admin                          | To use KILL thread, SET GLOBAL, CHANGE MASTER, etc.   |
| Trigger                         | Tables                                | To use triggers                                       |
| Create tablespace               | Server Admin                          | To create/alter/drop tablespaces                      |
| Update                          | Tables                                | To update existing rows                               |
| Usage                           | Server Admin                          | No privileges - allow connect only                    |
| BACKUP_ADMIN                    | Server Admin                          |                                                       |
| RESTORE_ADMIN                   | Server Admin                          |                                                       |
| SYSTEM_USER                     | Server Admin                          |                                                       |
| SYSTEM_VARIABLES_ADMIN          | Server Admin                          |                                                       |
| ROLE_ADMIN                      | Server Admin                          |                                                       |
| CONNECTION_ADMIN                | Server Admin                          |                                                       |
| PLACEMENT_ADMIN                 | Server Admin                          |                                                       |
| DASHBOARD_CLIENT                | Server Admin                          |                                                       |
| RESTRICTED_TABLES_ADMIN         | Server Admin                          |                                                       |
| RESTRICTED_STATUS_ADMIN         | Server Admin                          |                                                       |
| RESTRICTED_VARIABLES_ADMIN      | Server Admin                          |                                                       |
| RESTRICTED_USER_ADMIN           | Server Admin                          |                                                       |
| RESTRICTED_CONNECTION_ADMIN     | Server Admin                          |                                                       |
| RESTRICTED_REPLICA_WRITER_ADMIN | Server Admin                          |                                                       |
| RESOURCE_GROUP_ADMIN            | Server Admin                          |                                                       |
+---------------------------------+---------------------------------------+-------------------------------------------------------+
49 rows in set (0.00 sec)
```

## MySQL 兼容性

`SHOW PRIVILEGES` 语句与 MySQL 完全兼容。如发现任何兼容性差异，请尝试 [TiDB 支持资源](/support.md)。

## 另请参阅

* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [权限管理](/privilege-management.md)
* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)
