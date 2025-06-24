---
title: TiFlash 查询结果物化
summary: 了解如何在事务中保存 TiFlash 的查询结果。
---

# TiFlash 查询结果物化

本文介绍如何在 `INSERT INTO SELECT` 事务中将 TiFlash 查询结果保存到指定的 TiDB 表中。

从 v6.5.0 开始，TiDB 支持将 TiFlash 查询结果保存在表中，即 TiFlash 查询结果物化。在执行 `INSERT INTO SELECT` 语句时，如果 TiDB 将 `SELECT` 子查询下推到 TiFlash，TiFlash 的查询结果可以保存到 `INSERT INTO` 子句中指定的 TiDB 表中。对于 v6.5.0 之前的 TiDB 版本，TiFlash 查询结果是只读的，因此如果要保存 TiFlash 查询结果，必须从应用层获取结果，然后在单独的事务或进程中保存。

> **注意：**
>
> 默认情况下（[`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-new-in-v50)），优化器会根据 [SQL 模式](/sql-mode.md)和 TiFlash 副本的成本估算智能决定是否将查询下推到 TiFlash。
>
> - 如果当前会话的 [SQL 模式](/sql-mode.md)不是严格模式（即 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 和 `STRICT_ALL_TABLES`），优化器会根据 TiFlash 副本的成本估算智能决定是否将 `INSERT INTO SELECT` 中的 `SELECT` 子查询下推到 TiFlash。在这种模式下，如果你想忽略优化器的成本估算并强制将查询下推到 TiFlash，可以将系统变量 [`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-new-in-v51) 设置为 `ON`。
> - 如果当前会话的 [SQL 模式](/sql-mode.md)是严格模式（即 `sql_mode` 值包含 `STRICT_TRANS_TABLES` 或 `STRICT_ALL_TABLES`），`INSERT INTO SELECT` 中的 `SELECT` 子查询不能下推到 TiFlash。

`INSERT INTO SELECT` 的语法如下：

```sql
INSERT [LOW_PRIORITY | HIGH_PRIORITY] [IGNORE]
    [INTO] tbl_name
    [PARTITION (partition_name [, partition_name] ...)]
    [(col_name [, col_name] ...)]
    SELECT ...
    [ON DUPLICATE KEY UPDATE assignment_list]value:
    {expr | DEFAULT}

assignment:
    col_name = valueassignment_list:
    assignment [, assignment] ...
```

例如，你可以使用以下 `INSERT INTO SELECT` 语句将 `SELECT` 子句中表 `t1` 的查询结果保存到表 `t2` 中：

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## 典型和推荐的使用场景

- 高效的 BI 解决方案

    对于许多 BI 应用来说，分析查询请求非常重。例如，当大量用户同时访问和刷新报表时，BI 应用需要处理大量并发查询请求。为了有效处理这种情况，你可以使用 `INSERT INTO SELECT` 将报表的查询结果保存在 TiDB 表中。然后，最终用户在刷新报表时可以直接从结果表中查询数据，避免多次重复计算和分析。同样，通过保存历史分析结果，你可以进一步减少长期历史数据分析的计算量。例如，如果你有一个用于分析每日销售利润的报表 `A`，你可以使用 `INSERT INTO SELECT` 将报表 `A` 的结果保存到结果表 `T` 中。然后，当你需要生成一个分析过去一个月销售利润的报表 `B` 时，你可以直接使用表 `T` 中的每日分析结果。这种方式不仅大大减少了计算量，还提高了查询响应速度并降低了系统负载。

- 使用 TiFlash 服务在线应用

    TiFlash 支持的并发请求数量取决于数据量和查询复杂度，但通常不超过 100 QPS。你可以使用 `INSERT INTO SELECT` 保存 TiFlash 查询结果，然后使用查询结果表来支持高并发的在线请求。结果表中的数据可以在后台以低频率（例如，每 0.5 秒）更新，这远低于 TiFlash 的并发限制，同时仍然保持较高的数据新鲜度。

## 执行过程

* 在执行 `INSERT INTO SELECT` 语句期间，TiFlash 首先将 `SELECT` 子句的查询结果返回给集群中的 TiDB 服务器，然后将结果写入目标表，该表可以有 TiFlash 副本。
* `INSERT INTO SELECT` 语句的执行保证 ACID 属性。

## 限制

<CustomContent platform="tidb">

* TiDB 对 `INSERT INTO SELECT` 语句的内存限制可以通过系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 调整。从 v6.5.0 开始，不建议使用 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 控制事务内存大小。

    更多信息，请参见 [TiDB 内存控制](/configure-memory-usage.md)。

</CustomContent>

<CustomContent platform="tidb-cloud">

* TiDB 对 `INSERT INTO SELECT` 语句的内存限制可以通过系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 调整。从 v6.5.0 开始，不建议使用 [`txn-total-size-limit`](https://docs.pingcap.com/tidb/stable/tidb-configuration-file#txn-total-size-limit) 控制事务内存大小。

    更多信息，请参见 [TiDB 内存控制](https://docs.pingcap.com/tidb/stable/configure-memory-usage)。

</CustomContent>

* TiDB 对 `INSERT INTO SELECT` 语句的并发没有硬性限制，但建议考虑以下做法：

    * 当"写事务"较大时，例如接近 1 GiB，建议将并发控制在不超过 10。
    * 当"写事务"较小时，例如小于 100 MiB，建议将并发控制在不超过 30。
    * 根据测试结果和具体情况确定并发数。

## 示例

数据定义：

```sql
CREATE TABLE detail_data (
    ts DATETIME,                -- 费用产生时间
    customer_id VARCHAR(20),    -- 客户 ID
    detail_fee DECIMAL(20,2));  -- 费用金额

CREATE TABLE daily_data (
    rec_date DATE,              -- 数据采集日期
    customer_id VARCHAR(20),    -- 客户 ID
    daily_fee DECIMAL(20,2));   -- 每日费用金额

ALTER TABLE detail_data SET TIFLASH REPLICA 2;
ALTER TABLE daily_data SET TIFLASH REPLICA 2;

-- ... (detail_data 表持续更新)
INSERT INTO detail_data(ts,customer_id,detail_fee) VALUES
('2023-1-1 12:2:3', 'cus001', 200.86),
('2023-1-2 12:2:3', 'cus002', 100.86),
('2023-1-3 12:2:3', 'cus002', 2200.86),
('2023-1-4 12:2:3', 'cus003', 2020.86),
('2023-1-5 12:2:3', 'cus003', 1200.86),
('2023-1-6 12:2:3', 'cus002', 20.86),
('2023-1-7 12:2:3', 'cus004', 120.56),
('2023-1-8 12:2:3', 'cus005', 320.16);

-- 执行以下 SQL 语句 13 次，累计向表中插入 65,536 行数据。
INSERT INTO detail_data SELECT * FROM detail_data;
```

保存每日分析结果：

```sql
SET @@sql_mode='NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO';

INSERT INTO daily_data (rec_date, customer_id, daily_fee)
SELECT DATE(ts), customer_id, sum(detail_fee) FROM detail_data WHERE DATE(ts) > DATE('2023-1-1 12:2:3') GROUP BY DATE(ts), customer_id;
```

基于每日分析数据分析月度数据：

```sql
SELECT MONTH(rec_date), customer_id, sum(daily_fee) FROM daily_data GROUP BY MONTH(rec_date), customer_id;
```

上述示例将每日分析结果物化并保存到每日结果表中，基于此加速月度数据分析，从而提高数据分析效率。
