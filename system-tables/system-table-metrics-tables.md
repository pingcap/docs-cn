---
title: METRICS_TABLES
summary: Learn the `METRICS_TABLES` system table.
aliases: ['/docs/dev/system-tables/system-table-metrics-tables/','/docs/dev/reference/system-databases/metrics-tables/']
---

# METRICS_TABLES

The `INFORMATION_SCHEMA.METRICS_TABLES` table provides information of all monitoring tables in the [metrics_schema](/system-tables/system-table-metrics-schema.md) database.

{{< copyable "sql" >}}

```sql
desc information_schema.metrics_tables;
```

```sql
+------------+--------------+------+------+---------+-------+
| Field      | Type         | Null | Key  | Default | Extra |
+------------+--------------+------+------+---------+-------+
| TABLE_NAME | varchar(64)  | YES  |      | NULL    |       |
| PROMQL     | varchar(64)  | YES  |      | NULL    |       |
| LABELS     | varchar(64)  | YES  |      | NULL    |       |
| QUANTILE   | double       | YES  |      | NULL    |       |
| COMMENT    | varchar(256) | YES  |      | NULL    |       |
+------------+--------------+------+------+---------+-------+
```

Field description:

* `TABLE_NAME`: Corresponds to the table name in `metrics_schema`.
* `PROMQL`: The working principle of the monitoring table is to map SQL statements to `PromQL` and convert Prometheus results into SQL query results. This field is the expression template of `PromQL`. When you query the data of the monitoring table, the query conditions are used to rewrite the variables in this template to generate the final query expression.
* `LABELS`: The label for the monitoring item. Each label corresponds to a column in the monitoring table. If the SQL statement contains the filter of the corresponding column, the corresponding `PromQL` changes accordingly.
* `QUANTILE`: The percentile. For monitoring data of the histogram type, a default percentile is specified. If the value of this field is `0`, it means that the monitoring item corresponding to the monitoring table is not a histogram.
* `COMMENT`: The comment about the monitoring table.
