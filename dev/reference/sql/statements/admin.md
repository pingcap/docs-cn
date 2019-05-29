---
title: 数据库管理语句
category: reference
aliases: ['/docs-cn/sql/admin/']
---

# 数据库管理语句

TiDB 可以通过一些语句对数据库进行管理，包括设置权限、修改系统变量、查询数据库状态。

## 权限管理

参考[权限管理文档](/dev/reference/security/privilege-system.md)。

## `SET` 语句

`SET` 语句有多种作用和形式：

### 设置变量值

```sql
SET variable_assignment [, variable_assignment] ...

variable_assignment:
      user_var_name = expr
    | param_name = expr
    | local_var_name = expr
    | [GLOBAL | SESSION]
        system_var_name = expr
    | [@@global. | @@session. | @@]
        system_var_name = expr
```

这种语法可以设置 TiDB 的变量值，包括系统变量以及用户定义变量。对于用户自定义变量，都是会话范围的变量；对于系统变量，通过 `@@global.` 或者是 `GLOBAL` 设置的变量为全局范围变量，否则为会话范围变量，具体参考[系统变量](../sql/variable.md)一章。

### `SET CHARACTER` 语句和 `SET NAMES`

```sql
SET {CHARACTER SET | CHARSET}
    {'charset_name' | DEFAULT}

SET NAMES {'charset_name'
    [COLLATE 'collation_name'] | DEFAULT}
```

这个语句设置这三个会话范围的系统变量：`character_set_client`，`character_set_results`，`character_set_connection` 设置为给定的字符集。目前 `character_set_connection` 变量的值和 MySQL 有所区别，MySQL 将其设置为 `character_set_database` 的值。

### 设置密码

```sql
SET PASSWORD [FOR user] = password_option

password_option: {
    'auth_string'
  | PASSWORD('auth_string')
}
```

设置用户密码，具体信息参考[权限管理](../sql/privilege.md)。

### 设置隔离级别

```sql
SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED;
```

设置事务隔离级别，具体信息参考[事务语句](../sql/transaction.md#事务隔离级别)。

## `SHOW` 语句

TiDB 支持部分 `SHOW` 语句，用于查看 Database/Table/Column 信息，或者是数据库内部的状态。已经支持的语句：

```sql
# 已支持，且和 MySQL 行为一致
SHOW CHARACTER SET [like_or_where]
SHOW COLLATION [like_or_where]
SHOW [FULL] COLUMNS FROM tbl_name [FROM db_name] [like_or_where]
SHOW CREATE {DATABASE|SCHEMA} db_name
SHOW CREATE TABLE tbl_name
SHOW DATABASES [like_or_where]
SHOW GRANTS FOR user
SHOW INDEX FROM tbl_name [FROM db_name]
SHOW PRIVILEGES
SHOW [FULL] PROCESSLIST
SHOW [GLOBAL | SESSION] STATUS [like_or_where]
SHOW TABLE STATUS [FROM db_name] [like_or_where]
SHOW [FULL] TABLES [FROM db_name] [like_or_where]
SHOW [GLOBAL | SESSION] VARIABLES [like_or_where]
SHOW WARNINGS

# 已支持，但是返回空结果，目的是提升兼容性
SHOW ENGINE engine_name {STATUS | MUTEX}
SHOW [STORAGE] ENGINES
SHOW PLUGINS
SHOW PROCEDURE STATUS [like_or_where]
SHOW TRIGGERS [FROM db_name] [like_or_where]
SHOW EVENTS
SHOW FUNCTION STATUS [like_or_where]
SHOW MASTER STATUS

# TiDB 特有语句，用于查看统计信息
SHOW STATS_META [like_or_where]
SHOW STATS_HISTOGRAMS [like_or_where]
SHOW STATS_BUCKETS [like_or_where]

like_or_where:
    LIKE 'pattern'
  | WHERE expr
```

说明：

* 通过 `SHOW` 语句展示统计信息请参考[统计信息说明](https://github.com/pingcap/docs-cn/blob/master/sql/statistics.md#统计信息的查看)。
* 关于 `SHOW` 语句更多信息请参考 [MySQL 文档](https://dev.mysql.com/doc/refman/5.7/en/show.html)

在 TiDB 中，`SHOW MASTER STATUS` 语句返回的 `UniqueID` 实际上是从 `PD` 获取的当前 `TSO` 时间，这个时间在做 binlog 增量同步过程中需要使用。

```sql
mysql> show master status;
+-------------|--------------------|--------------|------------------|-------------------+
| File        | UniqueID           | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
+-------------|--------------------|--------------|------------------|-------------------+
| tidb-binlog | 403756327834484736 |              |                  |                   |
+-------------|--------------------|--------------|------------------|-------------------+
1 row in set (0.00 sec)
```

## `ADMIN` 语句

该语句是 TiDB 扩展语法，用于查看 TiDB 自身的状态，及对 TiDB 中的表数据进行校验。

```sql
ADMIN SHOW DDL
ADMIN SHOW DDL JOBS
ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...
ADMIN CANCEL DDL JOBS job_id [, job_id] ...
ADMIN CHECK TABLE tbl_name [, tbl_name] ...
```

* `ADMIN SHOW DDL`

    用于查看当前正在执行的 DDL 作业。

* `ADMIN SHOW DDL JOBS`

    用于查看当前 DDL 作业队列中的所有结果（包括正在运行以及等待运行的任务）以及已执行完成的 DDL 作业队列中的最近十条结果。

    ```sql
    mysql> admin show ddl jobs;
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

    * `JOB_ID`：每个 DDL 操作对应一个DDL job，`JOB_ID` 全局唯一。
    * `DB_NAME`：DDL 操作的 database name。
    * `TABLE_NAME`：DDL 操作的 table name。
    * `JOB_TYPE`：DDL 操作的类型。
    * `SCHEMA_STATE`：当前 schema 的状态，如果是 `add index`，就是 index 的状态，如果是 `add column`，就是 column 的状态，如果是 `create table`，就是 table 的状态。常见的状态有以下几种：
        * `none`：表示不存在。一般 drop 操作或者 create 操作失败回滚后，会是 `none` 状态。
        * `delete only`，`write only`，`delete reorganization`，`write reorganization`：这四个状态是中间状态，在[Online, Asynchronous Schema Change in F1](http://static.googleusercontent.com/media/research.google.com/zh-CN//pubs/archive/41376.pdf) 论文中有详细说明，在此不详细描述。一般操作中看不到这几种状态，因为中间状态转换很快，只有 `add index` 操作时能看到处于 `write reorganization` 状态，表示正在填充索引数据。 
        * `public`：表示存在且可用。一般 `create table`，`add index/column` 等操作完成后，会是 `public` 状态，表示新建的 table/column/index 可以正常读写了。
    * `SCHEMA_ID`：当前 DDL 操作的 database ID。
    * `TABLE_ID`：当前 DDL 操作的 table ID。
    * `ROW_COUNT`：表示在 `add index` 时，当前已经添加完成的数据行数。
    * `START_TIME`：DDL 操作的开始时间。
    * `STATE`：DDL 操作的状态：
        * `none`：表示已经放入 DDL 作业队列中，但还没开始执行，还在排队等待前面的 DDL 作业完成。另一种原因可能是 drop 操作后，会变成 none 状态，但是很快会更新成 synced 状态，表示所有 TiDB 都同步到该状态了。
        * `running`：表示正在执行。
        * `synced`：表示已经执行成功，且所有 TiDB 都已经同步该状态了。
        * `rollback done`：表示执行失败，回滚完成。
        * `rollingback`：表示执行失败，还在回滚过程中。
        * `cancelling`：表示正在取消过程中。这个状态只有在用 `ADMIN CANCEL DDL JOBS` 语法取消 DDL 作业后，才会出现。

* `ADMIN SHOW DDL JOB QUERIES job_id [, job_id] ...`

    用于显示 `job_id` 对应的 DDL 任务的原始 SQL 语句。这个 `job_id` 只会搜索正在执行中的任务以及 DDL 历史作业队伍中最近的十条。

* `ADMIN CANCEL DDL JOBS job_id [, job_id] ...`

    用于取消正在执行的 DDL 作业，其返回值为对应的作业取消是否成功，如果失败会显示失败的具体原因。这个操作可以同时取消多个 DDL 作业，其中 DDL 作业 ID 可以通过 `ADMIN SHOW DDL JOBS` 语句来获取。其中如果希望取消的作业已经完成，则取消操作将会失败。

* `ADMIN CHECK TABLE tbl_name [, tbl_name] ...`

    用于对给定表中的所有数据和对应索引进行一致性校验，若通过校验，则返回空的查询结果；否则返回 `data isn't equal` 错误。
