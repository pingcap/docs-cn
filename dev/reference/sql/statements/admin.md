---
title: ADMIN
category: reference
---

# `ADMIN` 语句

`ADMIN` 语句是 TiDB 扩展语法，用于查看 TiDB 自身的状态，并对 TiDB 中的表数据进行校验。示例如下。

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL
```

`ADMIN SHOW DDL` 用于查看当前正在执行的 DDL 作业。

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL JOBS
```

`ADMIN SHOW DDL JOBS` 用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。

{{< copyable "sql" >}}

```sql
ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...
```

{{< copyable "sql" >}}

```sql
ADMIN CANCEL DDL JOBS job_id [, job_id] ...
```

{{< copyable "sql" >}}

```sql
ADMIN CHECK TABLE tbl_name [, tbl_name] ...
```

## 语句概览

**AdminStmt**：

![AdminStmt](/media/sqlgram/AdminStmt.png)

## 使用示例

{{< copyable "sql" >}}

```sql
admin show ddl jobs;
```

```
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+---------------+
| JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE      | SCHEMA_STATE         | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE         |
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+---------------+
| 45     | test    | t1         | add index     | write reorganization | 32        | 37       | 0         | 2019-01-10 12:38:36.501 +0800 CST | running       |
| 44     | test    | t1         | add index     | none                 | 32        | 37       | 0         | 2019-01-10 12:36:55.18 +0800 CST  | rollback done |
| 43     | test    | t1         | add index     | public               | 32        | 37       | 6         | 2019-01-10 12:35:13.66 +0800 CST  | synced        |
| 42     | test    | t1         | drop index    | none                 | 32        | 37       | 0         | 2019-01-10 12:34:35.204 +0800 CST | synced        |
| 41     | test    | t1         | add index     | public               | 32        | 37       | 0         | 2019-01-10 12:33:22.62 +0800 CST  | synced        |
| 40     | test    | t1         | drop column   | none                 | 32        | 37       | 0         | 2019-01-10 12:33:08.212 +0800 CST | synced        |
| 39     | test    | t1         | add column    | public               | 32        | 37       | 0         | 2019-01-10 12:32:55.42 +0800 CST  | synced        |
| 38     | test    | t1         | create table  | public               | 32        | 37       | 0         | 2019-01-10 12:32:41.956 +0800 CST | synced        |
| 36     | test    |            | drop table    | none                 | 32        | 34       | 0         | 2019-01-10 11:29:59.982 +0800 CST | synced        |
| 35     | test    |            | create table  | public               | 32        | 34       | 0         | 2019-01-10 11:29:40.741 +0800 CST | synced        |
| 33     | test    |            | create schema | public               | 32        | 0        | 0         | 2019-01-10 11:29:22.813 +0800 CST | synced        |
+--------+---------+------------+---------------+----------------------+-----------+----------+-----------+-----------------------------------+---------------+
```

* `JOB_ID`：每个 DDL 操作对应一个 DDL 作业，`JOB_ID` 全局唯一。
* `DB_NAME`：执行 DDL 操作的数据库的名称。
* `TABLE_NAME`：执行 DDL 操作的表的名称。
* `JOB_TYPE`：DDL 操作的类型。
* `SCHEMA_STATE`：schema 的当前状态。如果 `JOB_TYPE` 是 `add index`，则为 index 的状态；如果是 `add column`，则为 column 的状态，如果是 `create table`，则为 table 的状态。常见的状态有以下几种：
    * `none`：表示不存在。一般 `drop` 操作或者 `create` 操作失败回滚后，会变为 `none` 状态。
    * `delete only`、`write only`、`delete reorganization`、`write reorganization`：这四种状态是中间状态，在[ Online, Asynchronous Schema Change in F1](http://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf) 论文中有详细说明，在此不再赘述。由于中间状态转换很快，一般操作中看不到这几种状态，只有执行 `add index` 操作时能看到处于 `write reorganization` 状态，表示正在添加索引数据。
    * `public`：表示存在且可用。一般 `create table` 和 `add index/column` 等操作完成后，会变为 `public` 状态，表示新建的 table/column/index 可以正常读写了。
* `SCHEMA_ID`：执行 DDL 操作的数据库的 ID。
* `TABLE_ID`：执行 DDL 操作的表的 ID。
* `ROW_COUNT`：执行 `add index` 操作时，当前已经添加完成的数据行数。
* `START_TIME`：DDL 操作的开始时间。
* `STATE`：DDL 操作的状态。常见的状态有以下几种：
    * `none`：表示该操作任务已经进入 DDL 作业队列中，但尚未执行，因为还在排队等待前面的 DDL 作业完成。另一种原因可能是执行 `drop` 操作后，会变为 `none` 状态，但是很快会更新为 `synced` 状态，表示所有 TiDB 实例都已经同步到该状态。
    * `running`：表示该操作正在执行。
    * `synced`：表示该操作已经执行成功，且所有 TiDB 实例都已经同步该状态。
    * `rollback done`：表示该操作执行失败，回滚完成。
    * `rollingback`：表示该操作执行失败，正在回滚。
    * `cancelling`：表示正在取消该操作。这个状态只有在用 `ADMIN CANCEL DDL JOBS` 命令取消 DDL 作业时才会出现。

- `ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...`：用于查看 `job_id` 对应的 DDL 任务的原始 SQL 语句。这个 `job_id` 只会搜索正在运行中的 DDL 作业以及 DDL 历史作业队列中最近的十条结果。
- `ADMIN CANCEL DDL JOBS job_id [, job_id] ...`：用于取消当前正在运行的 DDL 作业，并返回对应作业是否取消成功。如果取消失败，会显示失败的具体原因。

    > **注意：**
    >
    > - 该操作可以同时取消多个 DDL 作业。可以通过 `ADMIN SHOW DDL JOBS` 语句来获取 DDL 作业的 ID。
    > - 如果希望取消的作业已经完成，则取消操作将会失败。

- `ADMIN CHECK TABLE tbl_name [, tbl_name] ...`：用于对给定表中的所有数据和对应索引进行一致性校验，若通过校验，则返回空的查询结果；否则返回数据不一致的错误信息。

## MySQL 兼容性

ADMIN 语句是 TiDB 对于 MySQL 语法的扩展。   
