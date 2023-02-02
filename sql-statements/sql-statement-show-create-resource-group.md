---
title: SHOW CREATE RESOURCE GROUP
summary: TiDB 数据库中 SHOW CREATE RESOURCE GROUP 的使用概况。
---

# SHOW CREATE RESOURCE GROUP

`SHOW CREATE RESOURCE GROUP` 语句可用于查看资源组当前的定义。

## 语法图

```ebnf+diagram
ShowCreateResourceGroupStmt ::=
    "SHOW" "CREATE" "RESOURCE" "GROUP" ResourceGroupName

ResourceGroupName ::=
    Identifier
```

## 示例

查看资源组 `rg1` 当前的定义：

```sql
CREATE RESOURCE GROUP rg1 RRU_PER_SEC=100 WRU_PER_SEC=200;
Query OK, 0 rows affected (0.10 sec)
```

```sql
SHOW CREATE RESOURCE GROUP rg1;
***************************[ 1. row ]***************************
Resource_Group        | rg1
Create Resource Group | CREATE RESOURCE GROUP `rg1` RRU_PER_SEC=100 WRU_PER_SEC=200
1 row in set (0.00 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [TiDB RESOURCE CONTROL](/tidb-resource-control.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
