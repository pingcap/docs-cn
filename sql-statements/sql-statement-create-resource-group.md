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
|   "DEFAULT"

ResourceGroupOptionList ::=
    DirectResourceGroupOption
|   ResourceGroupOptionList DirectResourceGroupOption
|   ResourceGroupOptionList ',' DirectResourceGroupOption

DirectResourceGroupOption ::=
    "RU_PER_SEC" EqOpt stringLit
|   "PRIORITY" EqOpt ResourceGroupPriorityOption
|   "BURSTABLE"
|   "BURSTABLE" EqOpt "MODERATED"
|   "BURSTABLE" EqOpt "UNLIMITED"
|   "BURSTABLE" EqOpt "OFF"
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
|   "WATCH" EqOpt ResourceGroupRunawayWatchOption WatchDurationOption

WatchDurationOption ::=
    ("DURATION" EqOpt stringLit | "DURATION" EqOpt "UNLIMITED")?

ResourceGroupRunawayWatchOption ::=
    EXACT
|   SIMILAR
|   PLAN

ResourceGroupRunawayActionOption ::=
    DRYRUN
|   COOLDOWN
|   KILL
|   "SWITCH_GROUP" '(' ResourceGroupName ')'
```

资源组的 `ResourceGroupName` 是全局唯一的，不允许重复。

TiDB 支持以下 `DirectResourceGroupOption`, 其中 [Request Unit (RU)](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru) 是 TiDB 对 CPU、IO 等系统资源统一抽象的单位。

| 参数            | 含义           | 举例                                   |
|---------------|--------------|--------------------------------------|
| `RU_PER_SEC`  | 每秒 RU 填充的速度 | `RU_PER_SEC = 500` 表示此资源组每秒回填 500 个 RU。 |
| `PRIORITY`    | 任务在 TiKV 上处理的绝对优先级  | `PRIORITY = HIGH` 表示优先级高。若未指定，则默认为 `MEDIUM`。 |
| `BURSTABLE`   | 是否允许此资源组超额使用剩余的系统资源 | 从 v9.0.0 开始，支持以下三种模式：`OFF`，表示不允许此资源组超额使用剩余的系统资源；`MODERATED`，表示有限度地允许此资源组超额使用剩余的系统资源；`UNLIMITED`，表示无限度地允许此资源组超额使用剩余的系统资源。如果没有为 `BURSTABLE` 指定目标值，将默认启用 `MODERATED` 模式。 |
| `QUERY_LIMIT` | 当查询执行满足该条件时，识别该查询为 Runaway Query 并进行相应的控制 | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` 表示当执行时间超过 60 秒后识别为 Runaway Query，对该查询执行终止操作，并在 10 分钟内对同样的 SQL 直接执行终止操作。`QUERY_LIMIT=()` 或 `QUERY_LIMIT=NULL` 则表示不进行 Runaway 控制。具体参数介绍详见[管理资源消耗超出预期的查询 (Runaway Queries)](/tidb-resource-control-runaway-queries.md)。 ｜

> **注意：**
>
> - `CREATE RESOURCE GROUP` 语句只能在全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-从-v660-版本开始引入) 设置为 `ON` 时才能执行。
> - TiDB 集群在初始化时会自动创建 `default` 资源组，其 `RU_PER_SEC` 的默认值为 `UNLIMITED` (等同于 `INT` 类型最大值，即 `2147483647`)，且 `BURSTABLE` 为 `UNLIMITED` 模式。所有未绑定资源组的语句将自动绑定至该资源组。`default` 资源组不支持删除，但支持修改其 RU 配置。
> - 目前仅 `default` 资源组支持修改 `BACKGROUND` 相关设置。

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
  RU_PER_SEC = 200 QUERY_LIMIT=(EXEC_ELAPSED='100ms', ACTION=KILL);
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='rg1' or NAME = 'rg2';
```

```sql
+------+------------+----------+-----------+-----------------------------------+------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABL  | QUERY_LIMIT                       | BACKGROUND |
+------+------------+----------+-----------+-----------------------------------+------------+
| rg1  | 100        | HIGH     | MODERATED | NULL                              | NULL       |
| rg2  | 200        | MEDIUM   | OFF       | EXEC_ELAPSED='100ms', ACTION=KILL | NULL       |
+------+------------+----------+-----------+-----------------------------------+------------+
2 rows in set (1.30 sec)
```

## MySQL 兼容性

MySQL 也支持 [CREATE RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html)，但是接受的参数和 TiDB 不同，两者并不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [ALTER USER RESOURCE GROUP](/sql-statements/sql-statement-alter-user.md#修改用户绑定的资源组)
* [RU](/tidb-resource-control-ru-groups.md#什么是-request-unit-ru)
