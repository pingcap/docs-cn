---
title: ALTER RESOURCE GROUP
summary: TiDB 数据库中 ALTER RESOURCE GROUP 的使用概况。
---

# ALTER RESOURCE GROUP

`ALTER RESOURCE GROUP` 语句用于在当前所选数据库中修改资源组。

## 语法图

```ebnf+diagram
AlterResourceGroupStmt ::=
   "ALTER" "RESOURCE" "GROUP" IfExists ResourceGroupName ResourceGroupOptionList

IfExists ::=
    ('IF' 'EXISTS')?

ResourceGroupName ::=
   Identifier

ResourceGroupOptionList ::=
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption ::=
    "RU_PER_SEC" EqOpt stringLit
|   "PRIORITY" EqOpt ResourceGroupPriorityOption
|   "BURSTABLE"

ResourceGroupPriorityOption ::=
    LOW 
|   MEDIUM
|   HIGH
```

TiDB 支持以下 `DirectResourceGroupOption`, 其中 [Request Unit (RU)](/tidb-resource-control.md#什么是-request-unit-ru) 是 TiDB 对 CPU、IO 等系统资源统一抽象的单位。

| 参数            | 含义           | 举例                                   |
|---------------|--------------|--------------------------------------|
| `RU_PER_SEC`  | 每秒 RU 填充的速度 | `RU_PER_SEC = 500` 表示此资源组每秒回填 500 个 RU。 |
| `PRIORITY`    | 任务在 TiKV 上处理的绝对优先级  | `PRIORITY = HIGH` 表示优先级高。若未指定则默认为 `MEDIUM`。 |
| `BURSTABLE`   | 允许对应的资源组超出配额后使用空余的系统资源。 |

> **注意：**
> 
> `ALTER RESOURCE GROUP` 语句只能在全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 参数设置为 `ON` 时才能执行。

## 示例

创建一个名为 `rg1` 的资源组，并修改它的属性。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 0 rows affected (0.22 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1
  RU_PER_SEC = 100
  BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE |
+------+------------+----------+-----------+
| rg1  |       100  | MEDIUM   | YES       |
+------+------------+----------+-----------+
1 rows in set (1.30 sec)
```

```sql
ALTER RESOURCE GROUP rg1
  RU_PER_SEC = 200
  PRIORITY = LOW;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE |
+------+------------+----------+-----------+
| rg1  |       200  | LOW      | NO        |
+------+------------+----------+-----------+
1 rows in set (1.30 sec)
```

## MySQL 兼容性

MySQL 也支持 [ALTER RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html)，但是接受的参数和 TiDB 不同，两者并不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [RU](/tidb-resource-control.md#什么是-request-unit-ru)
