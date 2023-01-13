---
title: Drop Resource Group
summary: TiDB 数据库中 DROP Resource Group 的使用概况
aliases: ['/docs-cn/dev/sql-statements/sql-statement-drop-resource-group/','/docs-cn/dev/reference/sql/statements/drop-resource-group/']
---

# DROP RESOURCE GROUP

`DROP RESOURCE GROUP` 语句用于在当前所选数据库中删除资源组。

## 语法图

```ebnf+diagram
DropResourceGroupStmt:
	"DROP" "RESOURCE" "GROUP" IfNotExists ResourceGroupName

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

ResourceGroupName:
	Identifier
```

> **注意：**
> 
> `DROP RESOURCE GROUP` 语句只能在全局变量 `tidb_resource_group_enable` 参数设置为 `ON` 的时候才被允许执行

## 示例

删除名字是 rg1 的资源组

{{< copyable "sql" >}}

```sql
mysql> DROP RESOURCE GROUP IF EXISTS rg1;
Query OK, 0 rows affected (0.22 sec)
mysql> CREATE RESOURCE GROUP IF NOT EXISTS rg1 (
    ->  RRU_PER_SEC = 500
    ->  RRU_PER_SEC = 300
    ->  BURSTABLE
    -> );
Query OK, 0 rows affected (0.08 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+--------------+---------------------------------------------------------------+
| Name | Plan_type    | Directive | 
+------+--------------+---------------------------------------------------------------+
| rg1  |   tenancy    | {"RRU_PER_SEC": 500, "WRU_PER_SEC": 300, "BURSTABLE": true} |
+------+--------------+---------------------------------------------------------------+
1 row in set (0.00 sec)

mysql> DROP RESOURCE GROUP IF NOT EXISTS rg1 ;
Query OK, 1 rows affected (0.09 sec)
mysql> SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
+------+--------------+---------------------------------------------------------------+
| Name | Plan_type    | Directive | 
+------+--------------+---------------------------------------------------------------+
+------+--------------+---------------------------------------------------------------+
0 row in set (0.00 sec)
```

## MySQL 兼容性

* MySQL 也支持创建 [Resource Group](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html) ，但是接受的参数和 TiDB 不同。

## 另请参阅

* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
