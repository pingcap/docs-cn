---
title: ADMIN | TiDB SQL 语句参考
summary: TiDB 数据库中 ADMIN 的使用概述。
---

# ADMIN

该语句是 TiDB 扩展语法，用于查看 TiDB 的状态和检查 TiDB 中表的数据。本文档介绍以下 `ADMIN` 相关语句：

- [`ADMIN RELOAD`](#admin-reload-语句)
- [`ADMIN PLUGINS`](#admin-plugins-相关语句)
- [`ADMIN ... BINDINGS`](#admin-bindings-相关语句)
- [`ADMIN REPAIR`](#admin-repair-语句)
- [`ADMIN SHOW NEXT_ROW_ID`](#admin-show-next_row_id-语句)
- [`ADMIN SHOW SLOW`](#admin-show-slow-语句)

## DDL 相关语句

<CustomContent platform="tidb-cloud">

| 语句                                                                                | 描述                 |
|------------------------------------------------------------------------------------------|-----------------------------|
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)             | 取消当前正在运行的 DDL 作业。 |
| [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)               | 暂停当前正在运行的 DDL 作业。 |
| [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)             | 恢复已暂停的 DDL 作业。 |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)          | 计算表中所有行和索引的 CRC64。 |
| [<code>ADMIN CHECK [TABLE\|INDEX]</code>](/sql-statements/sql-statement-admin-check-table-index.md) | 检查表或索引的一致性。 |
| [<code>ADMIN SHOW DDL [JOBS\|QUERIES]</code>](/sql-statements/sql-statement-admin-show-ddl.md)      | 显示当前正在运行或最近完成的 DDL 作业的详细信息。 |

</CustomContent>

<CustomContent platform="tidb">

| 语句                                                                                | 描述                 |
|------------------------------------------------------------------------------------------|-----------------------------|
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)             | 取消当前正在运行的 DDL 作业。 |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)          | 计算表中所有行和索引的 CRC64。 |
| [<code>ADMIN CHECK [TABLE\|INDEX]</code>](/sql-statements/sql-statement-admin-check-table-index.md) | 检查表或索引的一致性。 |
| [<code>ADMIN SHOW DDL [JOBS\|QUERIES]</code>](/sql-statements/sql-statement-admin-show-ddl.md)      | 显示当前正在运行或最近完成的 DDL 作业的详细信息。 |

</CustomContent>

## `ADMIN RELOAD` 语句

```sql
ADMIN RELOAD expr_pushdown_blacklist;
```

上述语句用于重新加载表达式下推的黑名单。

```sql
ADMIN RELOAD opt_rule_blacklist;
```

上述语句用于重新加载逻辑优化规则的黑名单。

## `ADMIN PLUGINS` 相关语句

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

```sql
ADMIN PLUGINS ENABLE plugin_name [, plugin_name] ...;
```

上述语句用于启用 `plugin_name` 插件。

```sql
ADMIN PLUGINS DISABLE plugin_name [, plugin_name] ...;
```

上述语句用于禁用 `plugin_name` 插件。

## `ADMIN BINDINGS` 相关语句

```sql
ADMIN FLUSH BINDINGS;
```

上述语句用于持久化 SQL Plan 绑定信息。

```sql
ADMIN CAPTURE BINDINGS;
```

上述语句可以为出现多次的 `SELECT` 语句生成 SQL Plan 绑定。

```sql
ADMIN EVOLVE BINDINGS;
```

启用自动绑定功能后，每隔 `bind-info-leave`（默认值为 `3s`）会触发 SQL Plan 绑定信息的演进。上述语句用于主动触发此演进。

```sql
ADMIN RELOAD BINDINGS;
```

上述语句用于重新加载 SQL Plan 绑定信息。

## `ADMIN REPAIR` 语句

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 此 TiDB 语句不适用于 TiDB Cloud。

</CustomContent>

在极端情况下，要以不可信的方式覆盖存储表的元数据，使用 `ADMIN REPAIR TABLE`：

```sql
ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT;
```

<CustomContent platform="tidb">

这里的"不可信"意味着你需要手动确保原始表的元数据可以被 `CREATE TABLE STATEMENT` 操作覆盖。要使用此 `REPAIR` 语句，需要启用 [`repair-mode`](/tidb-configuration-file.md#repair-mode) 配置项，并确保要修复的表列在 [`repair-table-list`](/tidb-configuration-file.md#repair-table-list) 中。

</CustomContent>

## `ADMIN SHOW NEXT_ROW_ID` 语句

```sql
ADMIN SHOW t NEXT_ROW_ID;
```

上述语句用于查看表的某些特殊列的详细信息。输出与 [SHOW TABLE NEXT_ROW_ID](/sql-statements/sql-statement-show-table-next-rowid.md) 相同。

## `ADMIN SHOW SLOW` 语句

> **注意：**
>
> 此功能在 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群上不可用。

```sql
ADMIN SHOW SLOW RECENT N;
```

```sql
ADMIN SHOW SLOW TOP [INTERNAL | ALL] N;
```

<CustomContent platform="tidb">

详情请参考 [`ADMIN SHOW SLOW` 命令](/identify-slow-queries.md#admin-show-slow-command)。

</CustomContent>

## 语法图

```ebnf+diagram
AdminStmt ::=
    'ADMIN' ( 
        'SHOW' ( 
            'DDL' ( 
                'JOBS' Int64Num? WhereClauseOptional 
                | 'JOB' 'QUERIES' (NumList | AdminStmtLimitOpt)
            )? 
            | TableName 'NEXT_ROW_ID' 
            | 'SLOW' AdminShowSlow 
            | 'BDR' 'ROLE'
        ) 
        | 'CHECK' ( 
            'TABLE' TableNameList 
            | 'INDEX' TableName Identifier ( HandleRange ( ',' HandleRange )* )? 
        ) 
        | 'RECOVER' 'INDEX' TableName Identifier 
        | 'CLEANUP' ( 
            'INDEX' TableName Identifier 
            | 'TABLE' 'LOCK' TableNameList ) 
        | 'CHECKSUM' 'TABLE' TableNameList | 'CANCEL' 'DDL' 'JOBS' NumList 
        | ( 'CANCEL' | 'PAUSE' | 'RESUME' ) 'DDL' 'JOBS' NumList
        | 'RELOAD' (
            'EXPR_PUSHDOWN_BLACKLIST' 
            | 'OPT_RULE_BLACKLIST' 
            | 'BINDINGS'
            | 'STATS_EXTENDED'
            | 'STATISTICS'
        ) 
        | 'PLUGINS' ( 'ENABLE' | 'DISABLE' ) PluginNameList 
        | 'REPAIR' 'TABLE' TableName CreateTableStmt 
        | ( 'FLUSH' | 'CAPTURE' | 'EVOLVE' ) 'BINDINGS'
        | 'FLUSH' ('SESSION' | 'INSTANCE') 'PLAN_CACHE'
        | 'SET' 'BDR' 'ROLE' ( 'PRIMARY' | 'SECONDARY' )
        | 'UNSET' 'BDR' 'ROLE'
    )

NumList ::=
    Int64Num ( ',' Int64Num )*

AdminStmtLimitOpt ::=
    'LIMIT' LengthNum
|    'LIMIT' LengthNum ',' LengthNum
|    'LIMIT' LengthNum 'OFFSET' LengthNum

TableNameList ::=
    TableName ( ',' TableName )*
```

## 示例

运行以下命令查看当前正在运行的 DDL 作业队列中最后 10 个已完成的 DDL 作业。当未指定 `NUM` 时，默认只显示最后 10 个已完成的 DDL 作业。

```sql
ADMIN SHOW DDL JOBS;
```

```
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
| 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
| 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
| 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
| 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
| 39     | test    | t1         | add column    | public               | 32        | 37       | 0         | 2019-01-10 12:32:55.42 +0800 CST  | 2019-01-10 12:32:56.24 +0800 CST  | synced        |
| 38     | test    | t1         | create table  | public               | 32        | 37       | 0         | 2019-01-10 12:32:41.956 +0800 CST | 2019-01-10 12:32:43.956 +0800 CST | synced        |
| 36     | test    |            | drop table    | none                 | 32        | 34       | 0         | 2019-01-10 11:29:59.982 +0800 CST | 2019-01-10 11:30:00.45 +0800  CST | synced        |
| 35     | test    |            | create table  | public               | 32        | 34       | 0         | 2019-01-10 11:29:40.741 +0800 CST | 2019-01-10 11:29:41.682 +0800 CST | synced        |
| 33     | test    |            | create schema | public               | 32        | 0        | 0         | 2019-01-10 11:29:22.813 +0800 CST | 2019-01-10 11:29:23.954 +0800 CST | synced        |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

运行以下命令查看当前正在运行的 DDL 作业队列中最后 5 个已完成的 DDL 作业：

```sql
ADMIN SHOW DDL JOBS 5;
```

```
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
| 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
| 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
| 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
| 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

运行以下命令查看表的某些特殊列的详细信息。输出与 [SHOW TABLE NEXT_ROW_ID](/sql-statements/sql-statement-show-table-next-rowid.md) 相同。

```sql
ADMIN SHOW t NEXT_ROW_ID;
```

```sql
+---------+------------+-------------+--------------------+----------------+
| DB_NAME | TABLE_NAME | COLUMN_NAME | NEXT_GLOBAL_ROW_ID | ID_TYPE        |
+---------+------------+-------------+--------------------+----------------+
| test    | t          | _tidb_rowid |                101 | _TIDB_ROWID    |
| test    | t          | _tidb_rowid |                  1 | AUTO_INCREMENT |
+---------+------------+-------------+--------------------+----------------+
2 rows in set (0.01 sec)
```

运行以下命令查看 test 数据库中未完成的 DDL 作业。结果包括正在运行的 DDL 作业和最后 5 个已完成但失败的 DDL 作业。

```sql
ADMIN SHOW DDL JOBS 5 WHERE state != 'synced' AND db_name = 'test';
```

```
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE            | SCHEMA_STATE   | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

* `JOB_ID`：每个 DDL 操作对应一个 DDL 作业。`JOB_ID` 全局唯一。
* `DB_NAME`：执行 DDL 操作的数据库名称。
* `TABLE_NAME`：执行 DDL 操作的表名。
* `JOB_TYPE`：DDL 操作的类型。
* `SCHEMA_STATE`：架构的当前状态。如果 `JOB_TYPE` 是 `add index`，则是索引的状态；如果 `JOB_TYPE` 是 `add column`，则是列的状态；如果 `JOB_TYPE` 是 `create table`，则是表的状态。常见状态包括：
    * `none`：表示不存在。当 `drop` 或 `create` 操作失败并回滚时，通常会变成 `none` 状态。
    * `delete only`、`write only`、`delete reorganization`、`write reorganization`：这四个状态是中间状态。这些状态在普通操作中不可见，因为中间状态的转换非常快。你只能在 `add index` 操作中看到 `write reorganization` 状态，这表示正在添加索引数据。
    * `public`：表示存在且可用。当 `create table` 和 `add index/column` 等操作完成时，通常会变成 `public` 状态，这意味着创建的表/列/索引现在可以正常读写了。
* `SCHEMA_ID`：执行 DDL 操作的数据库的 ID。
* `TABLE_ID`：执行 DDL 操作的表的 ID。
* `ROW_COUNT`：运行 `add index` 操作时已添加的数据行数。
* `START_TIME`：DDL 操作的开始时间。
* `END_TIME`：DDL 操作的结束时间。
* `STATE`：DDL 操作的状态。常见状态包括：
    * `none`：表示操作任务已被放入 DDL 作业队列但尚未执行，因为它在等待前面的任务完成。另一个原因可能是它在运行 drop 操作后变成 `none` 状态，但很快会更新为 `synced` 状态，这意味着所有 TiDB 实例都已同步到这个状态。
    * `running`：表示正在执行操作。
    * `synced`：表示操作已成功执行，并且所有 TiDB 实例都已同步到这个状态。
    * `rollback done`：表示操作已失败并已完成回滚。
    * `rollingback`：表示操作已失败并正在回滚。
    * `cancelling`：表示正在取消操作。此状态仅在使用 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 作业时出现。
    * `paused`：表示操作已暂停。此状态仅在使用 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 命令暂停 DDL 作业时出现。你可以使用 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) 命令恢复 DDL 作业。

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。
