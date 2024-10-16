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
|   "DEFAULT"

ResourceGroupOptionList ::=
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption ::=
    "RU_PER_SEC" EqOpt LengthNum
|   "PRIORITY" EqOpt ResourceGroupPriorityOption
|   "BURSTABLE"
|   "BURSTABLE" EqOpt Boolean
|   "QUERY_LIMIT" EqOpt '(' ResourceGroupRunawayOptionList ')'
|   "QUERY_LIMIT" EqOpt '(' ')'
|   "QUERY_LIMIT" EqOpt "NULL"
|   "BACKGROUND" EqOpt '(' BackgroundOptionList ')'
|   "BACKGROUND" EqOpt '(' ')'
|   "BACKGROUND" EqOpt "NULL"

ResourceGroupPriorityOption ::=
    LOW
|   MEDIUM
|   HIGH

ResourceGroupRunawayOptionList ::=
    DirectResourceGroupRunawayOption
|   ResourceGroupRunawayOptionList DirectResourceGroupRunawayOption
|   ResourceGroupRunawayOptionList ',' DirectResourceGroupRunawayOption

DirectResourceGroupRunawayOption ::=
    "EXEC_ELAPSED" EqOpt stringLit
|   "PROCESSED_KEYS" EqOpt intLit
|   "RU" EqOpt intLit
|   "ACTION" EqOpt ResourceGroupRunawayActionOption
|   "WATCH" EqOpt ResourceGroupRunawayWatchOption "DURATION" EqOpt stringLit

ResourceGroupRunawayWatchOption ::=
    EXACT
|   SIMILAR

ResourceGroupRunawayActionOption ::=
    DRYRUN
|   COOLDOWN
|   KILL
|   "SWITCH_GROUP" '(' ResourceGroupName ')'

BackgroundOptionList ::=
    DirectBackgroundOption
|   BackgroundOptionList DirectBackgroundOption
|   BackgroundOptionList ',' DirectBackgroundOption

DirectBackgroundOption ::=
    "TASK_TYPES" EqOpt stringLit
|   "UTILIZATION_LIMIT" EqOpt LengthNum
```

TiDB 支持以下 `DirectResourceGroupOption`, 其中 [Request Unit (RU)](/tidb-resource-control.md#什么是-request-unit-ru) 是 TiDB 对 CPU、IO 等系统资源统一抽象的单位。

| 参数            | 含义           | 举例                                   |
|---------------|--------------|--------------------------------------|
| `RU_PER_SEC`  | 每秒 RU 填充的速度 | `RU_PER_SEC = 500` 表示此资源组每秒回填 500 个 RU。 |
| `PRIORITY`    | 任务在 TiKV 上处理的绝对优先级  | `PRIORITY = HIGH` 表示优先级高。若未指定则默认为 `MEDIUM`。 |
| `BURSTABLE`   | 允许对应的资源组超出配额后使用空余的系统资源。 |
| `QUERY_LIMIT` | 当查询执行满足该条件时，识别该查询为 Runaway Query 并执行相应的操作 | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` 表示当执行时间超过 60 秒后识别为 Runaway Query，对该查询执行终止操作，并在 10 分钟内对同样的 SQL 直接执行终止操作。`QUERY_LIMIT=()` 或 `QUERY_LIMIT=NULL` 则表示不进行 Runaway 控制。具体参数介绍参见[管理资源消耗超出预期的查询 (Runaway Queries)](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。 ｜
| `BACKGROUND`  | 后台任务相关的设置。具体参数介绍参见[管理后台任务](/tidb-resource-control.md#管理后台任务) | `BACKGROUND=(TASK_TYPES="br,stats", UTILIZATION_LIMIT=30)` 表示将备份恢复和收集统计信息相关的任务作为后台任务调度，并且后台任务最多可以使用 TiKV 30% 的资源。 |

> **注意：**
>
> - `ALTER RESOURCE GROUP` 语句只能在全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 参数设置为 `ON` 时才能执行。
> - `ALTER RESOURCE GROUP` 语句支持以增量方式修改，未指定的参数保持不变。但其中 `QUERY_LIMIT` 和 `BACKGROUND` 各自作为一个整体，无法部分修改其中的参数。
> - 目前仅 `default` 资源组支持修改 `BACKGROUND` 相关设置。

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
+------+------------+----------+-----------+-------------+------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND |
+------+------------+----------+-----------+-------------+------------+
| rg1  | 100        | MEDIUM   | NO        | NULL        | NULL       |
+------+------------+----------+-----------+-------------+------------+
1 rows in set (1.30 sec)
```

```sql
ALTER RESOURCE GROUP rg1
  RU_PER_SEC = 200
  PRIORITY = LOW
  QUERY_LIMIT = (EXEC_ELAPSED='1s' ACTION=COOLDOWN WATCH=EXACT DURATION '30s');
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1';
```

```sql
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT                                                    | BACKGROUND |
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
| rg1  | 200        | LOW      | NO        | EXEC_ELAPSED='1s', ACTION=COOLDOWN, WATCH=EXACT DURATION='30s' | NULL       |
+------+------------+----------+-----------+----------------------------------------------------------------+------------+
1 rows in set (1.30 sec)
```

修改 `default` 资源组的后台任务 `BACKGROUND` 相关设置。

```sql
ALTER RESOURCE GROUP default BACKGROUND = (TASK_TYPES = "br,ddl", UTILIZATION_LIMIT=30);
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='default';
```

```sql
+---------+------------+----------+-----------+-------------+-------------------------------------------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND                                |
+---------+------------+----------+-----------+-------------+-------------------------------------------+
| default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl', UTILIZATION_LIMIT=30 |
+---------+------------+----------+-----------+-------------+-------------------------------------------+
1 rows in set (1.30 sec)
```

## MySQL 兼容性

MySQL 也支持 [ALTER RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html)，但是接受的参数和 TiDB 不同，两者并不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [RU](/tidb-resource-control.md#什么是-request-unit-ru)
