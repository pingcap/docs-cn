---
title: SHOW PRIVILEGES | TiDB SQL 语句参考
summary: TiDB 数据库中 SHOW PRIVILEGES 的使用概述。
---

# SHOW PRIVILEGES

此语句显示 TiDB 中可分配的权限列表。这是一个静态列表，不反映当前用户的权限。

## 语法图

```ebnf+diagram
ShowPrivilegesStmt ::=
    "SHOW" "PRIVILEGES"
```

## 示例

```sql
SHOW PRIVILEGES;
```

```
+---------------------------------+---------------------------------------+-------------------------------------------------------+
| Privilege                       | Context                               | Comment                                               |
+---------------------------------+---------------------------------------+-------------------------------------------------------+
| Alter                           | Tables                                | 修改表                                                |
| Alter routine                   | Functions,Procedures                  | 修改或删除存储函数/存储过程                              |
| Config                          | Server Admin                          | 使用 SHOW CONFIG 和 SET CONFIG 语句                    |
| Create                          | Databases,Tables,Indexes              | 创建新的数据库和表                                      |
| Create routine                  | Databases                             | 使用 CREATE FUNCTION/PROCEDURE                         |
| Create role                     | Server Admin                          | 创建新角色                                            |
| Create temporary tables         | Databases                             | 使用 CREATE TEMPORARY TABLE                           |
| Create view                     | Tables                                | 创建新视图                                            |
| Create user                     | Server Admin                          | 创建新用户                                            |
| Delete                          | Tables                                | 删除现有行                                            |
| Drop                            | Databases,Tables                      | 删除数据库、表和视图                                    |
| Drop role                       | Server Admin                          | 删除角色                                              |
| Event                           | Server Admin                          | 创建、修改、删除和执行事件                              |
| Execute                         | Functions,Procedures                  | 执行存储过程                                          |
| File                            | File access on server                 | 在服务器上读写文件                                     |
| Grant option                    | Databases,Tables,Functions,Procedures | 将你拥有的权限授予其他用户                              |
| Index                           | Tables                                | 创建或删除索引                                         |
| Insert                          | Tables                                | 向表中插入数据                                         |
| Lock tables                     | Databases                             | 使用 LOCK TABLES（需要配合 SELECT 权限）                |
| Process                         | Server Admin                          | 查看当前执行查询的明文                                  |
| Proxy                           | Server Admin                          | 使代理用户成为可能                                     |
| References                      | Databases,Tables                      | 在表上拥有引用                                         |
| Reload                          | Server Admin                          | 重新加载或刷新表、日志和权限                            |
| Replication client              | Server Admin                          | 查询从服务器或主服务器的位置                            |
| Replication slave               | Server Admin                          | 从主服务器读取二进制日志事件                            |
| Select                          | Tables                                | 从表中检索行                                          |
| Show databases                  | Server Admin                          | 使用 SHOW DATABASES 查看所有数据库                     |
| Show view                       | Tables                                | 使用 SHOW CREATE VIEW 查看视图                         |
| Shutdown                        | Server Admin                          | 关闭服务器                                            |
| Super                           | Server Admin                          | 使用 KILL thread、SET GLOBAL、CHANGE MASTER 等         |
| Trigger                         | Tables                                | 使用触发器                                            |
| Create tablespace               | Server Admin                          | 创建/修改/删除表空间                                   |
| Update                          | Tables                                | 更新现有行                                            |
| Usage                           | Server Admin                          | 无权限 - 仅允许连接                                    |
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

TiDB 中的 `SHOW PRIVILEGES` 语句与 MySQL 完全兼容。如果发现任何兼容性差异，请[报告问题](https://docs.pingcap.com/tidb/stable/support)。

## 另请参阅

<CustomContent platform="tidb">

* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [权限管理](/privilege-management.md)
* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)

</CustomContent>

<CustomContent platform="tidb-cloud">

* [SHOW GRANTS](/sql-statements/sql-statement-show-grants.md)
* [权限管理](https://docs.pingcap.com/tidb/stable/privilege-management)
* [`GRANT <privileges>`](/sql-statements/sql-statement-grant-privileges.md)

</CustomContent>
