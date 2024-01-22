---
title: INSPECTION_SUMMARY
summary: 了解 TiDB 系统表 `INSPECTION_SUMMARY`。
---

# INSPECTION_SUMMARY

在部分场景下，用户只需要关注特定链路或模块的监控汇总。例如当前 Coprocessor 配置的线程池为 8，如果 Coprocessor 的 CPU 使用率达到了 750%，就可以确定存在风险，或者可能提前成为瓶颈。但是部分监控会因为用户的 workload 不同而差异较大，所以难以定义确定的阈值。排查这部分场景的问题也非常重要，所以 TiDB 提供了 `inspection_summary` 来进行链路汇总。

诊断汇总表 `information_schema.inspection_summary` 的表结构如下：

{{< copyable "sql" >}}

```sql
USE information_schema;
DESC inspection_summary;
```

```sql
+--------------+--------------+------+------+---------+-------+
| Field        | Type         | Null | Key  | Default | Extra |
+--------------+--------------+------+------+---------+-------+
| RULE         | varchar(64)  | YES  |      | NULL    |       |
| INSTANCE     | varchar(64)  | YES  |      | NULL    |       |
| METRICS_NAME | varchar(64)  | YES  |      | NULL    |       |
| LABEL        | varchar(64)  | YES  |      | NULL    |       |
| QUANTILE     | double       | YES  |      | NULL    |       |
| AVG_VALUE    | double(22,6) | YES  |      | NULL    |       |
| MIN_VALUE    | double(22,6) | YES  |      | NULL    |       |
| MAX_VALUE    | double(22,6) | YES  |      | NULL    |       |
| COMMENT      | varchar(256) | YES  |      | NULL    |       |
+--------------+--------------+------+------+---------+-------+
9 rows in set (0.00 sec)
```

字段解释：

* `RULE`：汇总规则。由于规则在持续添加，最新的规则列表可以通过 `select * from inspection_rules where type='summary'` 查询。
* `INSTANCE`：监控的具体实例。
* `METRICS_NAME`：监控表的名字。
* `QUANTILE`：对于包含 `QUANTILE` 的监控表有效，可以通过谓词下推指定多个百分位，例如 `select * from inspection_summary where rule='ddl' and quantile in (0.80, 0.90, 0.99, 0.999)` 来汇总 DDL 相关监控，查询百分位为 80/90/99/999 的结果。`AVG_VALUE`、`MIN_VALUE`、`MAX_VALUE` 分别表示聚合的平均值、最小值、最大值。
* `COMMENT`：对应监控的解释。

> **注意：**
>
> 由于汇总所有结果有一定开销，建议在 SQL 的谓词中显示指定的 `rule` 以减小开销。例如 `select * from inspection_summary where rule in ('read-link', 'ddl')` 会汇总读链路和 DDL 相关的监控。

使用示例:

诊断结果表和诊断监控汇总表都可以通过 `hint` 的方式指定诊断的时间范围，例如 `select /*+ time_range('2020-03-07 12:00:00','2020-03-07 13:00:00') */* from inspection_summary` 是对 2020-03-07 12:00:00 - 2020-03-07 13:00:00 时间段的监控汇总。和监控汇总表一样，`inspection_summary` 系统表也可以通过对比两个不同时间段的数据，快速发现差异较大的监控项。

以下为一个例子，对比以下两个时间段，读系统链路的监控项:

* `(2020-01-16 16:00:54.933, 2020-01-16 16:10:54.933)`
* `(2020-01-16 16:10:54.933, 2020-01-16 16:20:54.933)` 

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
    FROM information_schema.inspection_summary WHERE rule='read-link'
  ) t1
  JOIN
  (
    SELECT
      /*+ time_range("2020-01-16 16:10:54.933", "2020-01-16 16:20:54.933")*/ *
    FROM information_schema.inspection_summary WHERE rule='read-link'
  ) t2
  ON t1.metrics_name = t2.metrics_name
  and t1.instance = t2.instance
  and t1.label = t2.label
ORDER BY
  ratio DESC;
```
