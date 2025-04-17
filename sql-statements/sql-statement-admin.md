---
title: ADMIN
aliases: ['/docs-cn/dev/sql-statements/sql-statement-admin/','/docs-cn/dev/reference/sql/statements/admin/']
summary: TiDB的 `ADMIN` 语句是用于查看TiDB状态和对表数据进行校验的扩展语法。其中包括 `ADMIN RELOAD`、`ADMIN PLUGIN`、`ADMIN ... BINDINGS`、`ADMIN REPAIR TABLE` 和 `ADMIN SHOW NEXT_ROW_ID` 等扩展语句。这些语句可以用于重新加载表达式下推的黑名单、启用或禁用插件、持久化 SQL Plan 绑定信息、修复表的元信息以及查看表中特殊列的详情。这些功能对于管理和维护 TiDB 数据库非常有用。
---

# ADMIN

`ADMIN` 语句是 TiDB 扩展语法，用于查看 TiDB 自身的状态，并对 TiDB 中的表数据进行校验。本文介绍了下列与 ADMIN 相关的扩展语句：

- [`ADMIN RELOAD`](#admin-reload-语句)
- [`ADMIN PLUGIN`](#admin-plugin-语句)
- [`ADMIN ... BINDINGS`](#admin--bindings-语句)
- [`ADMIN REPAIR TABLE`](#admin-repair-table-语句)
- [`ADMIN SHOW NEXT_ROW_ID`](#admin-show-next_row_id-语句)
- [`ADMIN SHOW SLOW`](#admin-show-slow-语句)
- [`ADMIN CREATE WORKLOAD SNAPSHOT`](#admin-create-workload-snapshot-语句)

## ADMIN 与 DDL 相关的扩展语句

| 语句                                                                                | 功能描述                 |
|------------------------------------------------------------------------------------------|-----------------------------|
| [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md)             | 取消当前正在运行的 DDL 作业 |
| [`ADMIN PAUSE DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md)               | 暂停当前正在运行的 DDL 作业 |
| [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md)             | 恢复当前处于暂停中的 DDL 作业 |
| [`ADMIN CHECKSUM TABLE`](/sql-statements/sql-statement-admin-checksum-table.md)          | 计算表中所有行和索引的 CRC64 校验和 |
| [<code>ADMIN CHECK [TABLE\|INDEX]</code>](/sql-statements/sql-statement-admin-check-table-index.md) | 校验表中数据和对应索引的一致性 |
| [<code>ADMIN SHOW DDL [JOBS\|QUERIES]</code>](/sql-statements/sql-statement-admin-show-ddl.md)      | 显示有关当前正在运行或最近完成的 DDL 作业的详细信息|

## `ADMIN RELOAD` 语句

```sql
ADMIN RELOAD expr_pushdown_blacklist;
```

以上语句用于重新加载表达式下推的黑名单。

```sql
ADMIN RELOAD opt_rule_blacklist;
```

以上语句用于重新加载逻辑优化规则的黑名单。

## `ADMIN PLUGIN` 语句

```sql
ADMIN PLUGINS ENABLE plugin_name [, plugin_name] ...;
```

以上语句用于启用 `plugin_name` 插件。

```sql
ADMIN PLUGINS DISABLE plugin_name [, plugin_name] ...;
```

以上语句用于禁用 `plugin_name` 插件。

## `ADMIN ... BINDINGS` 语句

```sql
ADMIN FLUSH bindings;
```

以上语句用于持久化 SQL Plan 绑定的信息。

```sql
ADMIN CAPTURE bindings;
```

以上语句可以将出现超过一次的 `select`execution-plan 语句生成 SQL Plan 的绑定。

```sql
ADMIN EVOLVE bindings;
```

开启自动绑定功能后，每隔 `bind-info-lease`（默认值为 `3s`）触发一次 SQL Plan 绑定信息的演进。以上语句用于主动触发此演进，SQL Plan 绑定详情可参考：[执行计划管理](/sql-plan-management.md)。

```sql
ADMIN RELOAD bindings;
```

以上语句用于重新加载 SQL Plan 绑定的信息。

## `ADMIN REPAIR TABLE` 语句

```sql
ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT;
```

`ADMIN REPAIR TABLE tbl_name CREATE TABLE STATEMENT` 用于在极端情况下，对存储层中的表的元信息进行非可信的覆盖。“非可信”是指需要人为保证原表的元信息可以完全由 `CREATE TABLE STATEMENT` 提供。该语句需要打开配置文件项中的 [`repair-mode`](/tidb-configuration-file.md#repair-mode) 开关，并且需要确保所修复的表名在 [`repair-table-list`](/tidb-configuration-file.md#repair-table-list) 名单中。

## `ADMIN SHOW NEXT_ROW_ID` 语句

```sql
ADMIN SHOW t NEXT_ROW_ID;
```

以上语句可以查看表中某些特殊列的详情。输出结果与 [SHOW TABLE NEXT_ROW_ID](/sql-statements/sql-statement-show-table-next-rowid.md) 相同。

## `ADMIN SHOW SLOW` 语句

```sql
ADMIN SHOW SLOW RECENT N;
```

```sql
ADMIN SHOW SLOW TOP [INTERNAL | ALL] N;
```

这两种语句的具体操作详情可参考：[ADMIN SHOW SLOW 语句](/identify-slow-queries.md#admin-show-slow-命令)。

## `ADMIN CREATE WORKLOAD SNAPSHOT` 语句

以下 SQL 语句将在 [Workload Repository](/workload-repository.md) 中触发手动快照：

```sql
ADMIN CREATE WORKLOAD SNAPSHOT;
```

注意，必须启用 Workload Repository，此语句才能生效，否则会报错。

## 语句概览

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
        | 'CREATE' 'WORKLOAD' 'SNAPSHOT'
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

## 使用示例

执行以下命令，可查看正在执行的 DDL 任务中最近 10 条已经完成的 DDL 任务。未指定 `NUM` 时，默认只显示最近 10 条已经执行完的 DDL 任务。

```sql
ADMIN SHOW DDL jobs;
```

```
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
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

执行以下命令，可查看正在执行的 DDL 任务中最近 5 条已经执行完的 DDL 任务：

```sql
ADMIN SHOW DDL JOBS 5;
```

```
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
| 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | 2019-01-10 12:35:14.925 +0800 CST | synced        |
| 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | 2019-01-10 12:34:36.958 +0800 CST | synced        |
| 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | 2019-01-10 12:33:24.625 +0800 CST | synced        |
| 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | 2019-01-10 12:33:09.78 +0800 CST  | synced        |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

执行以下命令，查看表中某些特殊列的详情。输出结果与 [SHOW TABLE NEXT_ROW_ID](/sql-statements/sql-statement-show-table-next-rowid.md) 相同。

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

执行以下命令，可查看 test 数据库中未执行完成的 DDL 任务，包括正在执行中以及最近 5 条已经执行完但是执行失败的 DDL 任务。

```sql
ADMIN SHOW DDL JOBS 5 WHERE state != 'synced' AND db_name = 'test';
```

```
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | END_TIME                          | STATE         |
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST |                                   | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | 2019-01-10 12:36:55.852 +0800 CST | rollback done |
+--------+---------+------------+---------------------+----------------+-----------+----------+-----------+-----------------------------------+-----------------------------------+---------------+
```

* `JOB_ID`：每个 DDL 操作对应一个 DDL 作业，`JOB_ID` 全局唯一。
* `DB_NAME`：执行 DDL 操作的数据库的名称。
* `TABLE_NAME`：执行 DDL 操作的表的名称。
* `JOB_TYPE`：DDL 操作的类型。
* `SCHEMA_STATE`：schema 的当前状态。如果 `JOB_TYPE` 是 `add index`，则为 index 的状态；如果是 `add column`，则为 column 的状态，如果是 `create table`，则为 table 的状态。常见的状态有以下几种：
    * `none`：表示不存在。一般 `drop` 操作或者 `create` 操作失败回滚后，会变为 `none` 状态。
    * `delete only`、`write only`、`delete reorganization`、`write reorganization`：这四种状态是中间状态。由于中间状态转换很快，一般操作中看不到这几种状态，只有执行 `add index` 操作时能看到处于 `write reorganization` 状态，表示正在添加索引数据。
    * `public`：表示存在且可用。一般 `create table` 和 `add index/column` 等操作完成后，会变为 `public` 状态，表示新建的 table/column/index 可以正常读写了。
* `SCHEMA_ID`：执行 DDL 操作的数据库的 ID。
* `TABLE_ID`：执行 DDL 操作的表的 ID。
* `ROW_COUNT`：执行 `add index` 操作时，当前已经添加完成的数据行数。
* `START_TIME`：DDL 操作的开始时间。
* `END_TIME`：DDL 操作的结束时间。
* `STATE`：DDL 操作的状态。常见的状态有以下几种：
    * `none`：表示该操作任务已经进入 DDL 作业队列中，但尚未执行，因为还在排队等待前面的 DDL 作业完成。另一种原因可能是执行 `drop` 操作后，会变为 `none` 状态，但是很快会更新为 `synced` 状态，表示所有 TiDB 实例都已经同步到该状态。
    * `running`：表示该操作正在执行。
    * `synced`：表示该操作已经执行成功，且所有 TiDB 实例都已经同步该状态。
    * `rollback done`：表示该操作执行失败，回滚完成。
    * `rollingback`：表示该操作执行失败，正在回滚。
    * `cancelling`：表示正在取消该操作。这个状态只有在用 [`ADMIN CANCEL DDL JOBS`](/sql-statements/sql-statement-admin-cancel-ddl.md) 命令取消 DDL 作业时才会出现。
    * `paused`：表示 DDL 已被暂停运行。这个状态只有在用 [`ADMIN PAUSED DDL JOBS`](/sql-statements/sql-statement-admin-pause-ddl.md) 命令暂停 DDL 任务时才会出现。可以通过 [`ADMIN RESUME DDL JOBS`](/sql-statements/sql-statement-admin-resume-ddl.md) 命令进行恢复运行。

## MySQL 兼容性

`ADMIN` 语句是 TiDB 对于 MySQL 语法的扩展。
