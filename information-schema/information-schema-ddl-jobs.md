---
title: DDL_JOBS
summary: 了解 information_schema 表 `DDL_JOBS`。
aliases: ['/docs-cn/dev/information-schema/information-schema-ddl-jobs/']
---

# DDL_JOBS

`DDL_JOBS` 表为 `ADMIN SHOW DDL JOBS` 命令提供了一个 `INFORMATION_SCHEMA` 接口。它提供了 TiDB 集群中 DDL 操作的当前状态和简短历史记录。

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC ddl_jobs;
```

```sql
+--------------+-------------+------+------+---------+-------+
| Field        | Type        | Null | Key  | Default | Extra |
+--------------+-------------+------+------+---------+-------+
| JOB_ID       | bigint(21)  | YES  |      | NULL    |       |
| DB_NAME      | varchar(64) | YES  |      | NULL    |       |
| TABLE_NAME   | varchar(64) | YES  |      | NULL    |       |
| JOB_TYPE     | varchar(64) | YES  |      | NULL    |       |
| SCHEMA_STATE | varchar(64) | YES  |      | NULL    |       |
| SCHEMA_ID    | bigint(21)  | YES  |      | NULL    |       |
| TABLE_ID     | bigint(21)  | YES  |      | NULL    |       |
| ROW_COUNT    | bigint(21)  | YES  |      | NULL    |       |
| START_TIME   | datetime    | YES  |      | NULL    |       |
| END_TIME     | datetime    | YES  |      | NULL    |       |
| STATE        | varchar(64) | YES  |      | NULL    |       |
| QUERY        | varchar(64) | YES  |      | NULL    |       |
+--------------+-------------+------+------+---------+-------+
12 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SELECT * FROM ddl_jobs LIMIT 3\G
```

```sql
*************************** 1. row ***************************
      JOB_ID: 44
     DB_NAME: mysql
  TABLE_NAME: opt_rule_blacklist
    JOB_TYPE: create table
SCHEMA_STATE: public
   SCHEMA_ID: 3
    TABLE_ID: 43
   ROW_COUNT: 0
  START_TIME: 2020-07-06 15:24:27
    END_TIME: 2020-07-06 15:24:27
       STATE: synced
       QUERY: CREATE TABLE IF NOT EXISTS mysql.opt_rule_blacklist (
        name char(100) NOT NULL
    );
*************************** 2. row ***************************
      JOB_ID: 42
     DB_NAME: mysql
  TABLE_NAME: expr_pushdown_blacklist
    JOB_TYPE: create table
SCHEMA_STATE: public
   SCHEMA_ID: 3
    TABLE_ID: 41
   ROW_COUNT: 0
  START_TIME: 2020-07-06 15:24:27
    END_TIME: 2020-07-06 15:24:27
       STATE: synced
       QUERY: CREATE TABLE IF NOT EXISTS mysql.expr_pushdown_blacklist (
        name char(100) NOT NULL,
        store_type char(100) NOT NULL DEFAULT 'tikv,tiflash,tidb',
        reason varchar(200)
    );
*************************** 3. row ***************************
      JOB_ID: 40
     DB_NAME: mysql
  TABLE_NAME: stats_top_n
    JOB_TYPE: create table
SCHEMA_STATE: public
   SCHEMA_ID: 3
    TABLE_ID: 39
   ROW_COUNT: 0
  START_TIME: 2020-07-06 15:24:26
    END_TIME: 2020-07-06 15:24:27
       STATE: synced
       QUERY: CREATE TABLE if not exists mysql.stats_top_n (
        table_id bigint(64) NOT NULL,
        is_index tinyint(2) NOT NULL,
        hist_id bigint(64) NOT NULL,
        value longblob,
        count bigint(64) UNSIGNED NOT NULL,
        index tbl(table_id, is_index, hist_id)
    );
3 rows in set (0.01 sec)
```
