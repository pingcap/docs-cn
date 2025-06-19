---
title: ALTER RESOURCE GROUP
summary: 了解 TiDB 中 ALTER RESOURCE GROUP 的用法。
---

# ALTER RESOURCE GROUP

`ALTER RESOURCE GROUP` 语句用于修改数据库中的资源组。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法

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
    "RU_PER_SEC" EqOpt stringLit
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
|   "ACTION" EqOpt ResourceGroupRunawayActionOption
|   "WATCH" EqOpt ResourceGroupRunawayWatchOption "DURATION" EqOpt stringLit

ResourceGroupRunawayWatchOption ::=
    EXACT
|   SIMILAR

ResourceGroupRunawayActionOption ::=
    DRYRUN
|   COOLDOWN
|   KILL

BackgroundOptionList ::=
    DirectBackgroundOption
|   BackgroundOptionList DirectBackgroundOption
|   BackgroundOptionList ',' DirectBackgroundOption

DirectBackgroundOption ::=
    "TASK_TYPES" EqOpt stringLit
```

TiDB 支持以下 `DirectResourceGroupOption`，其中[请求单元 (RU)](/tidb-resource-control.md#what-is-request-unit-ru) 是 TiDB 中 CPU、IO 和其他系统资源的统一抽象单位。

| 选项     | 描述                         | 示例                |
|---------------|-------------------------------------|------------------------|
| `RU_PER_SEC` | 每秒 RU 补充率 | `RU_PER_SEC = 500` 表示此资源组每秒补充 500 个 RU |
| `PRIORITY`    | 在 TiKV 上处理任务的绝对优先级  | `PRIORITY = HIGH` 表示优先级高。如果未指定，默认值为 `MEDIUM`。 |
| `BURSTABLE`   | 如果设置了 `BURSTABLE` 属性，TiDB 允许相应的资源组在超出配额时使用可用的系统资源。 |
| `QUERY_LIMIT` | 当查询执行满足此条件时，该查询被识别为失控查询并执行相应的操作。 | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` 表示当执行时间超过 60 秒时，该查询被识别为失控查询。查询被终止。在接下来的 10 分钟内，所有具有相同 SQL 文本的 SQL 语句都将立即被终止。`QUERY_LIMIT=()` 或 `QUERY_LIMIT=NULL` 表示未启用失控控制。参见[失控查询](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)。 |
| `BACKGROUND`  | 配置后台任务。更多详情，请参见[管理后台任务](/tidb-resource-control.md#manage-background-tasks)。 | `BACKGROUND=(TASK_TYPES="br,stats")` 表示备份恢复和统计信息收集相关的任务被安排为后台任务。 |

> **注意：**
>
> - `ALTER RESOURCE GROUP` 语句只能在全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 设置为 `ON` 时执行。
> - `ALTER RESOURCE GROUP` 语句支持增量更改，未指定的参数保持不变。但是，`QUERY_LIMIT` 和 `BACKGROUND` 都是作为一个整体使用，不能部分修改。
> - 目前，只有 `default` 资源组支持修改 `BACKGROUND` 配置。

## 示例

创建名为 `rg1` 的资源组并修改其属性。

```sql
DROP RESOURCE GROUP IF EXISTS rg1;
```

```
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

修改 `default` 资源组的 `BACKGROUND` 选项。

```sql
ALTER RESOURCE GROUP default BACKGROUND = (TASK_TYPES = "br,ddl");
```

```sql
Query OK, 0 rows affected (0.08 sec)
```

```sql
SELECT * FROM information_schema.resource_groups WHERE NAME ='default';
```

```sql
+---------+------------+----------+-----------+-------------+---------------------+
| NAME    | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT | BACKGROUND          |
+---------+------------+----------+-----------+-------------+---------------------+
| default | UNLIMITED  | MEDIUM   | YES       | NULL        | TASK_TYPES='br,ddl' |
+---------+------------+----------+-----------+-------------+---------------------+
1 rows in set (1.30 sec)
```

## MySQL 兼容性

MySQL 也支持 [ALTER RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/alter-resource-group.html)。但是，可接受的参数与 TiDB 的不同，因此它们不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [CREATE RESOURCE GROUP](/sql-statements/sql-statement-create-resource-group.md)
* [请求单元 (RU)](/tidb-resource-control.md#what-is-request-unit-ru)
