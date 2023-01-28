---
title: ALTER RESOURCE GROUP
summary: TiDB 数据库中 ALTER RESOURCE GROUP 的使用概况
aliases: ['/docs-cn/dev/sql-statements/sql-statement-alter-resource-group/','/docs-cn/dev/reference/sql/statements/alter-resource-group/']
---

# ALTER RESOURCE GROUP

`ALTER RESOURCE GROUP` 语句用于在当前所选数据库中修改资源组。

## 语法图

```ebnf+diagram
AlterResourceGroupStmt:
   "ALTER" "RESOURCE" "GROUP" IfNotExists ResourceGroupName ResourceGroupOptionList BurstableOption

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

ResourceGroupName:
   Identifier

ResourceGroupOptionList:
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption:
    "RRU_PER_SEC" EqOpt stringLit
|   "WRU_PER_SEC" EqOpt stringLit

BurstableOption ::=
    ("BURSTABLE")?

```

TiDB 支持以下 `DirectResourceGroupOption`, 其中 [`RU` (Resource Unit)](/tidb-RU.md) 是 TiDB 对 CPU、IO 等系统资源统一抽象的单位。

| 参数           |含义                                 | 举例                    |
|---------------|-------------------------------------|------------------------|
|`RRU_PER_SEC`|每秒钟读 RU 的配额                       |`RRU_PER_SEC = 500`     |
|`WRU_PER_SEC`|每秒钟写 RU 的配额                       |`WRU_PER_SEC = 300`     |

如果设置了 `BURSTABLE` 属性，对应的资源组就允许在系统资源充足的情况下，允许超出配额使用系统资源。

> **注意：**
> 
> `ALTER RESOURCE GROUP` 语句只能在全局变量 [`tidb_enable_resource_group`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 参数设置为 `ON` 的时候才被允许执行。

## 示例

创建一个名为 `rg1` 的资源组，并修改它的属性。

```sql
mysql> DROP RESOURCE GROUP IF EXISTS rg1;
Query OK, 0 rows affected (0.22 sec)
mysql> CREATE RESOURCE GROUP IF NOT EXISTS rg1
    ->  RRU_PER_SEC = 500
    ->  WRU_PER_SEC = 300
    ->  BURSTABLE
    -> ;
Query OK, 0 rows affected (0.08 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+--------------+---------------------------------------------------------------+
| Name | Plan_type    | Directive | 
+------+--------------+---------------------------------------------------------------+
| rg1  |   tenancy    | {"RRU_PER_SEC": 500, "WRU_PER_SEC": 300, "BURSTABLE": true} |
+------+--------------+---------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> ALTER RESOURCE GROUP IF NOT EXISTS rg1
    ->  RRU_PER_SEC = 600
    ->  WRU_PER_SEC = 400
    -> ;
Query OK, 0 rows affected (0.09 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+--------------+---------------------------------------------------------------+
| Name | Plan_type    | Directive | 
+------+--------------+---------------------------------------------------------------+
| rg1  |   tenancy    | {"RRU_PER_SEC": 600, "WRU_PER_SEC": 400, "BURSTABLE": false} |
+------+--------------+---------------------------------------------------------------+
1 row in set (0.00 sec)
```

## MySQL 兼容性

MySQL 也支持 [ALTER RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html)，但是接受的参数和 TiDB 不同，两者并不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [RU](/tidb-RU.md)
