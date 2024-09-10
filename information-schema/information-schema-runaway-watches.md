---
title: RUNAWAY_WATCHES
summary: 了解 INFORMATION_SCHEMA 表 `RUNAWAY_WATCHES`。
---

# RUNAWAY_WATCHES

`RUNAWAY_WATCHES` 表展示资源消耗超出预期的查询 Runaway Queries 监控列表，见 [Runaway Queries](/tidb-resource-control.md#管理资源消耗超出预期的查询-runaway-queries)。

```sql
USE INFORMATION_SCHEMA;
DESC RUNAWAY_WATCHES;
```

```sql
+---------------------+--------------+------+------+---------+-------+
| Field               | Type         | Null | Key  | Default | Extra |
+---------------------+--------------+------+------+---------+-------+
| ID                  | bigint(64)   | NO   |      | NULL    |       |
| RESOURCE_GROUP_NAME | varchar(32)  | NO   |      | NULL    |       |
| START_TIME          | varchar(32)  | NO   |      | NULL    |       |
| END_TIME            | varchar(32)  | YES  |      | NULL    |       |
| WATCH               | varchar(12)  | NO   |      | NULL    |       |
| WATCH_TEXT          | text         | NO   |      | NULL    |       |
| SOURCE              | varchar(128) | NO   |      | NULL    |       |
| ACTION              | varchar(12)  | NO   |      | NULL    |       |
| RULE                | varchar(128)  | NO   |      | NULL    |       |
+---------------------+--------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

## 示例

查询 Runaway Queries 识别名单：

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G
```

输出结果如下：

```sql
mysql> SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES ORDER BY id\G
*************************** 1. row ***************************
                 ID: 1
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-09 03:35:31
           END_TIME: 2024-09-09 03:45:31
              WATCH: Exact
         WATCH_TEXT: SELECT variable_name, variable_value FROM mysql.global_variables
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ProcessedKeys = 666(10)
*************************** 2. row ***************************
                 ID: 2
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-09 03:36:22
           END_TIME: 2024-09-09 03:46:22
              WATCH: Exact
         WATCH_TEXT: select table_id, is_index, hist_id, distinct_count, version, null_count, tot_col_size, stats_ver, flag, correlation, last_analyze_pos from mysql.stats_histograms where table_id = 124
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ProcessedKeys = 17(10)
3 rows in set (0.00 sec)
```

添加一个识别项到资源组 `rg1`：

```sql
QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT EXACT TO 'select * from sbtest.sbtest1';
```

再次查询 Runaway Queries 识别名单：

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G
```

输出结果如下：

```sql
*************************** 1. row ***************************
                 ID: 1
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-09 03:35:31
           END_TIME: 2024-09-09 03:45:31
              WATCH: Exact
         WATCH_TEXT: SELECT variable_name, variable_value FROM mysql.global_variables
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ProcessedKeys = 666(10)
*************************** 2. row ***************************
                 ID: 2
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-09 03:36:22
           END_TIME: 2024-09-09 03:46:22
              WATCH: Exact
         WATCH_TEXT: select table_id, is_index, hist_id, distinct_count, version, null_count, tot_col_size, stats_ver, flag, correlation, last_analyze_pos from mysql.stats_histograms where table_id = 124
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
               RULE: ProcessedKeys = 17(10)
*************************** 7. row ***************************
                 ID: 7
RESOURCE_GROUP_NAME: default
         START_TIME: 2024-09-09 11:41:21
           END_TIME: UNLIMITED
              WATCH: Exact
         WATCH_TEXT: select * from sbtest.sbtest1
             SOURCE: manual
             ACTION: Kill
               RULE: None
3 row in set (0.00 sec)
```

`RUNAWAY_WATCHES` 表中列的含义如下：

* `ID`：识别项 ID。
* `RESOURCE_GROUP_NAME`：资源组名称。
* `START_TIME`：开始时间。
* `END_TIME`：结束时间。`UNLIMITED` 表示识别项的有效时间无限长。
* `WATCH`：识别匹配类型，其值如下：
    - `Plan` 表示按照 Plan Digest 匹配，此时列 `WATCH_TEXT` 显示 Plan Digest。
    - `Similar` 表示按照 SQL Digest 匹配，此时列 `WATCH_TEXT` 显示 SQL Digest。
    - `Exact` 表示按照 SQL 文本匹配，此时列 `WATCH_TEXT` 显示 SQL 文本。
* `SOURCE`：识别项来源，如果是被 `QUERY_LIMIT` 规则识别，则显示识别到的 TiDB IP；如果是手动添加，则显示 `manual`。
* `ACTION`：识别后的对应操作。
* `RULE`：识别规则。目前包括 `ElapsedTime`、`ProcessedKeys` 和 `RequestUnit` 这三种规则。格式为 `ProcessedKeys = 666(10)`，其中 `666` 为实际值，`10` 为阈值。
