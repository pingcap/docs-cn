---
title: CREATE RESOURCE GROUP
summary: TiDB 数据库中 CREATE RESOURCE GROUP 的使用概况。
---

# CREATE RESOURCE GROUP

`CREATE RESOURCE GROUP` 语句用于在当前所选数据库中创建资源组。

## 语法图

```ebnf+diagram
CreateResourceGroupStmt ::=
   "CREATE" "RESOURCE" "GROUP" IfNotExists ResourceGroupName ResourceGroupOptionList

IfNotExists ::=
    ('IF' 'NOT' 'EXISTS')?

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

资源组的 `ResourceGroupName` 是全局唯一的，不允许重复。

TiDB 支持以下 `DirectResourceGroupOption`, 其中 [Request Unit (RU)](/tidb-resource-control.md#什么是-request-unit-ru) 是 TiDB 对 CPU、IO 等系统资源统一抽象的单位。

| 参数            | 含义           | 举例                                   |
|---------------|--------------|--------------------------------------|
| `RU_PER_SEC`  | 每秒 RU 填充的速度 | `RU_PER_SEC = 500` 表示此资源组每秒回填 500 个 RU。 |
| `PRIORITY`    | 任务在 TiKV 上处理的绝对优先级  | `PRIORITY = HIGH` 表示优先级高。若未指定，则默认为 `MEDIUM`。 |
| `BURSTABLE`   | 允许对应的资源组超出配额后使用空余的系统资源。 |

> **注意：**
>
> - `CREATE RESOURCE GROUP` 语句只能在全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 设置为 `ON` 时才能执行。
> - TiDB 集群在初始化时会自动创建 `default` 资源组，其 `RU_PER_SEC` 的默认值为 `UNLIMITED` (等同于 `INT` 类型最大值，即 `2147483647`)，且为 `BURSTABLE` 模式。所有未绑定资源组的请求都将自动绑定至此资源组。在新建配置其他资源组时，建议根据实际情况修改 `default` 资源组的配置。

## 示例

创建 `rg1` 和 `rg2` 两个资源组。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```sql
Query OK, 0 rows affected (0.22 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg1
  RU_PER_SEC = 100
  PRIORITY = HIGH
  BURSTABLE;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
CREATE RESOURCE GROUP IF NOT EXISTS rg2
  RU_PER_SEC = 200;
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1' or NAME = 'rg2';
```

```sql
+------+------------+----------+-----------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE |
+------+------------+----------+-----------+
| rg1  |        100 | HIGH     | YES       |
| rg2  |        200 | MEDIUM   | NO        |
+------+------------+----------+-----------+
2 rows in set (1.30 sec)
```

## MySQL 兼容性

MySQL 也支持 [CREATE RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html)，但是接受的参数和 TiDB 不同，两者并不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [ALTER USER RESOURCE GROUP](/sql-statements/sql-statement-alter-user.md#修改用户绑定的资源组)
* [RU](/tidb-resource-control.md#什么是-request-unit-ru)
