---
title: SHOW CREATE RESOURCE GROUP
summary: 了解 TiDB 中 SHOW CREATE RESOURCE GROUP 的使用方法。
---

# SHOW CREATE RESOURCE GROUP

你可以使用 `SHOW CREATE RESOURCE GROUP` 语句查看资源组的当前定义。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法

```ebnf+diagram
ShowCreateResourceGroupStmt ::=
    "SHOW" "CREATE" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
|   "DEFAULT"
```

## 示例

创建一个资源组 `rg1`。

```sql
CREATE RESOURCE GROUP rg1 RU_PER_SEC=100;
Query OK, 0 rows affected (0.10 sec)
```

查看 `rg1` 的定义。

```sql
SHOW CREATE RESOURCE GROUP rg1;
***************************[ 1. row ]***************************
+----------------+------------------------------------------------------------+
| Resource_Group | Create Resource Group                                      |
+----------------+------------------------------------------------------------+
| rg1            | CREATE RESOURCE GROUP `rg1` RU_PER_SEC=100 PRIORITY=MEDIUM |
+----------------+------------------------------------------------------------+
1 row in set (0.01 sec)
```

## MySQL 兼容性

此语句是 TiDB 对 MySQL 的扩展。

## 另请参阅

* [TiDB 资源控制](/tidb-resource-control.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
