---
title: INSPECTION_SUMMARY
summary: Learn the `INSPECTION_SUMMARY` inspection summary table.
category: reference
---

# INSPECTION_SUMMARY

In some scenarios, you might pay attention only to the monitoring summary of specific links or modules. For example, the number of threads for Coprocessor in the thread pool is configured as 8. If the CPU usage of Coprocessor reaches 750%, you can determine that a risk exists and Coprocessor might become a bottleneck in advance. However, some monitoring metrics vary greatly due to different user workloads, so it is difficult to define specific thresholds. It is important to troubleshoot issues in this scenario, so TiDB provides the `inspection_summary` table for link summary.

The structure of the `information_schema.inspection_summary` inspection summary table is as follows:

{{< copyable "sql" >}}

```sql
desc inspection_summary;
```

```sql
+--------------+-----------------------+------+------+---------+-------+
| Field        | Type                  | Null | Key  | Default | Extra |
+--------------+-----------------------+------+------+---------+-------+
| RULE         | varchar(64)           | YES  |      | NULL    |       |
| INSTANCE     | varchar(64)           | YES  |      | NULL    |       |
| METRICS_NAME | varchar(64)           | YES  |      | NULL    |       |
| LABEL        | varchar(64)           | YES  |      | NULL    |       |
| QUANTILE     | double unsigned       | YES  |      | NULL    |       |
| AVG_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| MIN_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
| MAX_VALUE    | double(22,6) unsigned | YES  |      | NULL    |       |
+--------------+-----------------------+------+------+---------+-------+
```

Field description:

* `RULE`: Summary rules. Because new rules are being added continuously, you can execute the `select * from inspection_rules where type='summary'` statement to query the latest rule list.
* `INSTANCE`: The monitored instance.
* `METRICS_NAME`: The monitoring metrics name.
* `QUANTILE`: Takes effect on monitoring tables that contain `QUANTILE`. You can specify multiple percentiles by pushing down predicates. For example, you can execute `select * from inspection_summary where rule='ddl' and quantile in (0.80, 0.90, 0.99, 0.999)` to summarize the DDL-related monitoring metrics and query the P80/P90/P99/P999 results. `AVG_VALUE`, `MIN_VALUE`, and `MAX_VALUE` respectively indicate the average value, minimum value, and maximum value of the aggregation.

> **Note:**
>
> Because summarizing all results causes overhead, the rules in `information_summary` are triggered passively. That is, the specified `rule` runs only when it displays in the SQL predicate. For example, executing the `select * from inspection_summary` statement returns an empty result set. Executing `select * from inspection_summary where rule in ('read-link', 'ddl')` summarizes the read link and DDL-related monitoring metrics.

Usage example:

Both the diagnosis result table and the diagnosis monitoring summary table can specify the diagnosis time range using `hint`. `select **+ time_range('2020-03-07 12:00:00','2020-03-07 13:00:00') */* from inspection_summary` is the monitoring summary for the `2020-03-07 12:00:00` to `2020-03-07 13:00:00` period. Like the monitoring summary table, you can use the diagnosis result table to quickly find the monitoring items with large differences by comparing the data of two different periods.

See the following example that diagnoses issues within a specified range, from "2020-01-16 16:00:54.933" to "2020-01-16 16:10:54.933":

{{< copyable "sql" >}}

```sql
SELECT
  t1.avg_value / t2.avg_value AS ratio,
  t1.*,
  t2.*
FROM
  (
    SELECT
      /*+ time_range("2020-01-16 16:00:54.933", "2020-01-16 16:10:54.933")*/ *
    FROM inspection_summary WHERE rule='read-link'
  ) t1
  JOIN
  (
    SELECT
      /*+ time_range("2020-01-16 16:10:54.933","2020-01-16 16:20:54.933")*/ *
    FROM inspection_summary WHERE rule='read-link'
  ) t2
  ON t1.metrics_name = t2.metrics_name
  and t1.instance = t2.instance
  and t1.label = t2.label
ORDER BY
  ratio DESC;
```
