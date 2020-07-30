---
title: METRICS_TABLES
summary: 了解 TiDB 系统表 `METRICS_TABLES`。
aliases: ['/docs-cn/dev/reference/system-databases/metrics-tables/']
---

# METRICS_TABLES

`INFORMATION_SCHEMA.METRICS_TABLES` 表提供了 `metrics_schema` 数据库中所有监控表的相关信息。

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

表 `metrics_tables` 的字段解释：

* `TABLE_NAME`：对应于 `metrics_schema` 中的表名。
* `PROMQL`：监控表的主要原理是将 SQL 映射成 `PromQL`，并将 Prometheus 结果转换成 SQL 查询结果。这个字段是 `PromQL` 的表达式模板，查询监控表数据时使用查询条件改写模板中的变量，生成最终的查询表达式。
* `LABELS`：监控定义的 label，每一个 label 对应监控表中的一列。SQL 中如果包含对应列的过滤，对应的 `PromQL` 也会改变。
* `QUANTILE`：百分位。对于直方图类型的监控数据，指定一个默认百分位。如果值为 `0`，表示该监控表对应的监控不是直方图。
* `COMMENT`：对这个监控表的解释。
