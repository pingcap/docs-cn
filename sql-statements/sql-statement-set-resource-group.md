---
title: SET RESOURCE GROUP
summary: TiDB 数据库中 SET RESOURCE GROUP 的使用概述。
---

# SET RESOURCE GROUP

`SET RESOURCE GROUP` 用于设置当前会话的资源组。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法图

**SetResourceGroupStmt:**

```ebnf+diagram
SetResourceGroupStmt ::=
    "SET" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

## 示例

创建用户 `user1`，创建两个资源组 `rg1` 和 `rg2`，并将用户 `user1` 绑定到资源组 `rg1`。

```sql
CREATE USER 'user1';
CREATE RESOURCE GROUP 'rg1' RU_PER_SEC = 1000;
ALTER USER 'user1' RESOURCE GROUP `rg1`;
```

使用 `user1` 登录并查看当前用户绑定的资源组。

```sql
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg1                      |
+--------------------------+
1 row in set (0.00 sec)
```

执行 `SET RESOURCE GROUP` 将当前会话的资源组设置为 `rg2`。

```sql
SET RESOURCE GROUP `rg2`;
SELECT CURRENT_RESOURCE_GROUP();
```

```
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| rg2                      |
+--------------------------+
1 row in set (0.00 sec)
```

执行 `SET RESOURCE GROUP` 指定当前会话使用默认资源组。

```sql
SET RESOURCE GROUP `default`;
SELECT CURRENT_RESOURCE_GROUP();
```

```sql
+--------------------------+
| CURRENT_RESOURCE_GROUP() |
+--------------------------+
| default                  |
+--------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

MySQL 也支持 [SET RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/set-resource-group.html)。但是可接受的参数与 TiDB 的不同，它们不兼容。

## 另请参阅

* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [资源控制](/tidb-resource-control.md)
