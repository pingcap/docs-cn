---
title: RUNAWAY_WATCHES
summary: Learn the `RUNAWAY_WATCHES` INFORMATION_SCHEMA table.
---

# RUNAWAY_WATCHES

The `RUNAWAY_WATCHES` table shows the watch list of runaway queries that consume more resources than expected. For more information, see [Runaway Queries](/tidb-resource-control.md#manage-queries-that-consume-more-resources-than-expected-runaway-queries).

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
+---------------------+--------------+------+------+---------+-------+
8 rows in set (0.00 sec)
```

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Examples

Query the watch list of runaway queries:

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES;
```

The output is as follows:

```sql
*************************** 1. row ***************************
                 ID: 20003
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 13:06:08
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 5b7fd445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 2. row ***************************
                 ID: 16004
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 01:45:30
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 3d48fca401d8cbb31a9f29adc9c0f9d4be967ca80a34f59c15f73af94e000c84
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
2 rows in set (0.00 sec)
```

Add a watch item into list to the resource group `rg1`:

```sql
QUERY WATCH ADD RESOURCE GROUP rg1 SQL TEXT EXACT TO 'select * from sbtest.sbtest1';
```

Query the watch list of runaway queries again:

```sql
SELECT * FROM INFORMATION_SCHEMA.RUNAWAY_WATCHES\G;
```

The output is as follows:

```sql
*************************** 1. row ***************************
                 ID: 20003
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 13:06:08
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 5b7fd445c5756a16f910192ad449c02348656a5e9d2aa61615e6049afbc4a82e
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 2. row ***************************
                 ID: 16004
RESOURCE_GROUP_NAME: rg2
         START_TIME: 2023-07-28 01:45:30
           END_TIME: UNLIMITED
              WATCH: Similar
         WATCH_TEXT: 3d48fca401d8cbb31a9f29adc9c0f9d4be967ca80a34f59c15f73af94e000c84
             SOURCE: 127.0.0.1:4000
             ACTION: Kill
*************************** 3. row ***************************
                 ID: 20004
RESOURCE_GROUP_NAME: rg1
         START_TIME: 2023-07-28 14:23:04
           END_TIME: UNLIMITED
              WATCH: Exact
         WATCH_TEXT: select * from sbtest.sbtest1
             SOURCE: manual
             ACTION: NoneAction
3 row in set (0.00 sec)
```

The meaning of each column field in the `RUNAWAY_WATCHES` table is as follows:

- `ID`: the ID of the watch item.
- `RESOURCE_GROUP_NAME`: the name of the resource group.
- `START_TIME`: the start time.
- `END_TIME`: the end time. `UNLIMITED` means that the watch item has an unlimited validity period.
- `WATCH`: the match type of the quick identification. The values are as follows:
    - `Plan` indicates that the Plan Digest is matched. In this case, the `WATCH_TEXT` column shows the Plan Digest.
    - `Similar` indicates that the SQL Digest is matched. In this case, the `WATCH_TEXT` column shows the SQL Digest.
    - `Exact` indicates that the SQL text is matched. In this case, the `WATCH_TEXT` column shows the SQL text.
- `SOURCE`: the source of the watch item. If it is identified by the `QUERY_LIMIT` rule, the identified TiDB IP address is displayed. If it is manually added, `manual` is displayed.
- `ACTION`: the corresponding operation after the identification.
