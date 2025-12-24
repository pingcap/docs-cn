---
title: TiFlash 查询结果物化
summary: 介绍如何在同一个事务中保存 TiFlash 的查询结果。
---

# TiFlash 查询结果物化

本文介绍如何在同一个事务 (`INSERT INTO SELECT`) 中实现将 TiFlash 查询结果保存至某一指定的 TiDB 表中。

从 v6.5.0 起，TiDB 支持将 TiFlash 查询结果保存到数据表中，即物化了 TiFlash 的查询结果。执行 `INSERT INTO SELECT` 语句时，如果 TiDB 将 `SELECT` 子查询下推到了 TiFlash，TiFlash 的查询结果可以保存到 `INSERT INTO` 指定的 TiDB 表中。v6.5.0 之前的 TiDB 版本不允许此类行为，即通过 TiFlash 执行的查询必须是只读的，你需要从应用程序层面接收 TiFlash 返回的结果，然后另行在其它事务或处理中保存结果。

> **注意：**
>
> 默认情况下 ([`tidb_allow_mpp = ON`](/system-variables.md#tidb_allow_mpp-从-v50-版本开始引入))，优化器将根据 [SQL 模式](/sql-mode.md)及 TiFlash 副本的代价估算自行决定是否将查询下推到 TiFlash。
>
> - 如果当前会话的 [SQL 模式](/sql-mode.md)为非严格模式（即 `sql_mode` 值不包含 `STRICT_TRANS_TABLES` 和 `STRICT_ALL_TABLES`），优化器会根据 TiFlash 副本的代价估算自行决定是否将 `INSERT INTO SELECT` 中的 `SELECT` 子查询将下推到 TiFlash。在此模式下，如需忽略优化器代价估算强制使用 TiFlash 查询，你可以设置[`tidb_enforce_mpp`](/system-variables.md#tidb_enforce_mpp-从-v51-版本开始引入) 为 `ON`。
> - 如果当前会话的 [SQL 模式](/sql-mode.md)为严格模式（即 `sql_mode` 值包含 `STRICT_TRANS_TABLES` 或 `STRICT_ALL_TABLES`），`INSERT INTO SELECT` 中的 `SELECT` 子查询将无法下推到 TiFlash。

`INSERT INTO SELECT` 语法如下：

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

例如，通过以下 `INSERT INTO SELECT` 语句，你可以将 `SELECT` 子句中表 `t1` 的查询结果保存到表 `t2` 中：

```sql
INSERT INTO t2 (name, country)
SELECT app_name, country FROM t1;
```

## 典型和推荐的使用场景

- 高效的 BI 解决方案

    很多报表类应用有较重的分析查询，如果有很多用户同时打开和刷新报表，则会产生较多的查询请求。一个有效的解决方案是使用本功能在 TiDB 表中保存报表查询的结果，报表刷新时再从结果表中抽取数据，则可以避免多次重复的分析计算。同理，在保存历史分析记录的基础上，可以进一步优化长时间历史数据分析的计算量。例如，某报表 A 用于分析每日的销售利润，使用本功能你可以将报表 A 中每日的分析结果保存到某结果表 T 中。那么，在生成报表 B 分析过去一个月的销售利润时，可以直接使用表 T 中的每日分析结果数据，不仅大幅降低计算量也提升了查询响应速度，减轻系统负载。

- 使用 TiFlash 服务在线应用

    TiFlash 支持的并发请求数量视数据量和查询复杂度不同，但一般不会超过 100 QPS。你可以使用本功能保存 TiFlash 的查询结果，然后通过查询结果表来支持在线的高并发请求。后台的结果表数据更新可以以较低的频率进行，例如以 0.5 秒间隔更新结果表数据也远低于 TiFlash 的并发上限，同时仍然较好地保证了数据新鲜度。

## 执行过程

* 在 `INSERT INTO SELECT` 语句的执行过程中，TiFlash 首先将 `SELECT` 子句的查询结果返回到集群中某单一 TiDB server 节点，然后再写入目标表（可以有 TiFlash 副本）。
* `INSERT INTO SELECT` 语句的执行保证 ACID 特性。

## 限制

* TiDB 对 `INSERT INTO SELECT` 语句的内存限制可以通过系统变量 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query) 调整。从 v6.5.0 版本开始，不推荐使用 [`txn-total-size-limit`](/tidb-configuration-file.md#txn-total-size-limit) 来控制事务内存大小，详见该配置项文档。

    更多信息，请参考 [TiDB 内存控制](/configure-memory-usage.md)。

* TiDB 对 `INSERT INTO SELECT` 语句的并发没有硬性限制，但是推荐考虑以下用法：

    * 当“写事务”较大时，例如接近 1 GiB，建议控制并发不超过 10。
    * 当“写事务”较小时，例如小于 100 MiB，建议控制并发不超过 30。
    * 请基于测试和具体情况做出合理选择。

## 示例

数据定义：

```sql
CREATE TABLE detail_data (
    ts DATETIME,                -- 费用产生时间
    customer_id VARCHAR(20),    -- 客户 ID
    detail_fee DECIMAL(20,2));  -- 费用数额


CREATE TABLE daily_data (
    rec_date DATE,              -- 汇总数据的日期
    customer_id VARCHAR(20),    -- 客户 ID
    daily_fee DECIMAL(20,2));   -- 单日汇总费用

ALTER TABLE detail_data SET TIFLASH REPLICA 2;
ALTER TABLE daily_data SET TIFLASH REPLICA 2;

-- ... (detail_data 表不断增加数据)
INSERT INTO detail_data(ts,customer_id,detail_fee) VALUES 
('2023-1-1 12:2:3', 'cus001', 200.86),
('2023-1-2 12:2:3', 'cus002', 100.86),
('2023-1-3 12:2:3', 'cus002', 2200.86),
('2023-1-4 12:2:3', 'cus003', 2020.86),
('2023-1-5 12:2:3', 'cus003', 1200.86),
('2023-1-6 12:2:3', 'cus002', 20.86),
('2023-1-7 12:2:3', 'cus004', 120.56),
('2023-1-8 12:2:3', 'cus005', 320.16);

-- 重复执行以下 SQL 语句 13 次，一共插入 65536 行数据
INSERT INTO detail_data SELECT * FROM detail_data;
```

每日分析数据保存：

```sql
SET @@sql_mode='NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO';

INSERT INTO daily_data (rec_date, customer_id, daily_fee)
SELECT DATE(ts), customer_id, sum(detail_fee) FROM detail_data WHERE DATE(ts) > DATE('2023-1-1 12:2:3') GROUP BY DATE(ts), customer_id;
```

基于日分析数据的月数据分析：

```sql
SELECT MONTH(rec_date), customer_id, sum(daily_fee) FROM daily_data GROUP BY MONTH(rec_date), customer_id;
```

将每日分析结果数据物化，保存到日数据结果表中。使用日数据结果表加速月数据分析，从而提升月数据分析效率。