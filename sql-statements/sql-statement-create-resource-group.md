---
title: CREATE RESOURCE GROUP
summary: 了解 TiDB 中 CREATE RESOURCE GROUP 的使用方法。
---

# CREATE RESOURCE GROUP

你可以使用 `CREATE RESOURCE GROUP` 语句创建资源组。

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

## 语法

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
```

资源组名称参数（`ResourceGroupName`）必须全局唯一。

TiDB 支持以下 `DirectResourceGroupOption`，其中[请求单元 (RU)](/tidb-resource-control.md#what-is-request-unit-ru) 是 TiDB 中 CPU、IO 和其他系统资源的统一抽象单位。

| 选项     | 描述                         | 示例                |
|---------------|-------------------------------------|------------------------|
| `RU_PER_SEC`  | 每秒 RU 补充速率   | `RU_PER_SEC = 500` 表示该资源组每秒补充 500 个 RU    |
| `PRIORITY`    | 在 TiKV 上处理任务的绝对优先级  | `PRIORITY = HIGH` 表示优先级高。如果未指定，默认值为 `MEDIUM`。 |
| `BURSTABLE`   | 如果设置了 `BURSTABLE` 属性，TiDB 允许相应的资源组在超出配额时使用可用的系统资源。 |
| `QUERY_LIMIT` | 当查询执行满足此条件时，该查询被识别为失控查询并执行相应的操作。 | `QUERY_LIMIT=(EXEC_ELAPSED='60s', ACTION=KILL, WATCH=EXACT DURATION='10m')` 表示当执行时间超过 60 秒时，该查询被识别为失控查询。查询被终止。在接下来的 10 分钟内，所有具有相同 SQL 文本的 SQL 语句都将立即被终止。`QUERY_LIMIT=()` 或 `QUERY_LIMIT=NULL` 表示不启用失控控制。参见[失控查询](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries)。 |

> **注意：**
>
> - `CREATE RESOURCE GROUP` 语句只能在全局变量 [`tidb_enable_resource_control`](/system-variables.md#tidb_enable_resource_control-new-in-v660) 设置为 `ON` 时执行。
> TiDB 在集群初始化期间自动创建一个 `default` 资源组。对于此资源组，`RU_PER_SEC` 的默认值为 `UNLIMITED`（相当于 `INT` 类型的最大值，即 `2147483647`），并且处于 `BURSTABLE` 模式。所有未绑定到任何资源组的请求都会自动绑定到这个 `default` 资源组。当你为其他资源组创建新配置时，建议根据需要修改 `default` 资源组配置。
> - 目前，只有 `default` 资源组支持修改 `BACKGROUND` 配置。

## 示例

创建两个资源组 `rg1` 和 `rg2`。

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
+------+------------+----------+-----------+---------------------------------+
| NAME | RU_PER_SEC | PRIORITY | BURSTABLE | QUERY_LIMIT                     |
+------+------------+----------+-----------+---------------------------------+
| rg1  | 100        | HIGH     | YES       | NULL                            |
| rg2  | 200        | MEDIUM   | NO        | EXEC_ELAPSED=100ms, ACTION=KILL |
+------+------------+----------+-----------+---------------------------------+
2 rows in set (1.30 sec)
```

## MySQL 兼容性

MySQL 也支持 [CREATE RESOURCE GROUP](https://dev.mysql.com/doc/refman/8.0/en/create-resource-group.html)。但是，可接受的参数与 TiDB 的不同，因此它们不兼容。

## 另请参阅

* [DROP RESOURCE GROUP](/sql-statements/sql-statement-drop-resource-group.md)
* [ALTER RESOURCE GROUP](/sql-statements/sql-statement-alter-resource-group.md)
* [ALTER USER RESOURCE GROUP](/sql-statements/sql-statement-alter-user.md#modify-the-resource-group-bound-to-the-user)
* [请求单元 (RU)](/tidb-resource-control.md#what-is-request-unit-ru)
