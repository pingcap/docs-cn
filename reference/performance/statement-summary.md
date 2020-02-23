---
title: Statement Summary Tables
category: reference
---

# Statement Summary Tables

针对 SQL 性能相关的问题，MySQL 在 `performance_schema` 提供了 [statement summary tables](https://dev.mysql.com/doc/refman/5.6/en/statement-summary-tables.html)，用来监控和统计 SQL。例如其中的一张表 `events_statements_summary_by_digest`，提供了丰富的字段，包括延迟、执行次数、扫描行数、全表扫描次数等，有助于用户定位 SQL 问题。

为此，从 3.0.4 版本开始，TiDB 也提供系统表 `events_statements_summary_by_digest`，从 3.0.8 开始提供系统表 `events_statements_summary_by_digest_history`。本文将详细介绍这两张表，以及如何利用它们来排查 SQL 性能问题。

## `events_statements_summary_by_digest`

`events_statements_summary_by_digest` 是 `performance_schema` 里的一张系统表，它把 SQL 按 SQL digest 和 plan digest 分组，统计每一组的 SQL 信息。

此处的 SQL digest 与 slow log 里的 SQL digest 一样，是把 SQL 规一化后算出的唯一标识符。SQL 的规一化会忽略常量、空白符、大小写的差别。即语法一致的 SQL 语句，其 digest 也相同。

例如：

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

规一化后都是：

```sql
select * from employee where id in (...) and salary between ? and ?;
```

此处的 plan digest 是把执行计划规一化后算出的唯一标识符。执行计划的规一化会忽略常量的差别。由于相同的 SQL 可能产生不同的执行计划，所以可能分到多个组，同一个组内的执行计划是相同的。

`events_statements_summary_by_digest` 用于保存 SQL 监控指标聚合后的结果。一般来说，每一项监控指标都包含平均值和最大值。例如执行延时对应 `AVG_LATENCY` 和 `MAX_LATENCY` 两个字段，分别是平均延时和最大延时。

为了监控指标的即时性，`events_statements_summary_by_digest` 里的数据定期被清空，只展现最近一段时间内的聚合结果。清空周期由系统变量 `tidb_stmt_summary_refresh_interval` 设置。如果刚好在清空之后进行查询，显示的数据可能很少。

因为 TiDB 中的很多概念不同于 MySQL，所以 TiDB 中 `events_statements_summary_by_digest` 的表结构与 MySQL 中的有很大区别。

以下为查询 `events_statements_summary_by_digest` 的部分结果：

```
   SUMMARY_BEGIN_TIME: 2020-01-02 11:00:00
     SUMMARY_END_TIME: 2020-01-02 11:30:00
            STMT_TYPE: select
          SCHEMA_NAME: test
               DIGEST: 0611cc2fe792f8c146cc97d39b31d9562014cf15f8d41f23a4938ca341f54182
          DIGEST_TEXT: select * from employee where id = ?
          TABLE_NAMES: test.employee
          INDEX_NAMES: NULL
          SAMPLE_USER: root
           EXEC_COUNT: 3
          SUM_LATENCY: 1035161
          MAX_LATENCY: 399594
          MIN_LATENCY: 301353
          AVG_LATENCY: 345053
    AVG_PARSE_LATENCY: 57000
    MAX_PARSE_LATENCY: 57000
  AVG_COMPILE_LATENCY: 175458
  MAX_COMPILE_LATENCY: 175458
  ...........
              AVG_MEM: 103
              MAX_MEM: 103
    AVG_AFFECTED_ROWS: 0
           FIRST_SEEN: 2020-01-02 11:12:54
            LAST_SEEN: 2020-01-02 11:25:24
    QUERY_SAMPLE_TEXT: select * from employee where id=3100
     PREV_SAMPLE_TEXT:
          PLAN_DIGEST: f415b8d52640b535b9b12a9c148a8630d2c6d59e419aad29397842e32e8e5de3
                 PLAN:  Point_Get_1     root    1       table:employee, handle:3100
```

> **注意：**
>
> 在 TiDB 中，statement summary tables 中字段的时间单位是纳秒 (ns)，而 MySQL 中的时间单位是皮秒 (ps)。

### 表的字段介绍

SQL 的基础信息：

- `STMT_TYPE`：SQL 语句的类型
- `SCHEMA_NAME`：执行这类 SQL 的当前 schema
- `DIGEST`：这类 SQL 的 digest
- `DIGEST_TEXT`：规一化后的 SQL
- `QUERY_SAMPLE_TEXT`：这类 SQL 的原 SQL 语句，多条语句只取其中一条
- `TABLE_NAMES`：SQL 中涉及的所有表，多张表用 `,` 分隔
- `INDEX_NAMES`：SQL 中使用的索引名，多个索引用 `,` 分隔
- `SAMPLE_USER`：执行这类 SQL 的用户名，多个用户名只取其中一个
- `PLAN_DIGEST`：执行计划的 digest
- `PLAN`：原执行计划，多条语句只取其中一条的执行计划

执行时间相关的信息：

- `SUMMARY_BEGIN_TIME`：当前统计的时间段的开始时间
- `SUMMARY_END_TIME`：当前统计的时间段的结束时间
- `FIRST_SEEN`：这类 SQL 的首次出现时间
- `LAST_SEEN`：这类 SQL 的最后一次出现时间

在 TiDB server 上的执行数据：

- `EXEC_COUNT`：这类 SQL 的总执行次数
- `SUM_LATENCY`：这类 SQL 的总延时
- `MAX_LATENCY`：这类 SQL 的最大延时
- `MIN_LATENCY`：这类 SQL 的最小延时
- `AVG_LATENCY`：这类 SQL 的平均延时
- `AVG_PARSE_LATENCY`：解析器的平均延时
- `MAX_PARSE_LATENCY`：解析器的最大延时
- `AVG_COMPILE_LATENCY`：优化器的平均延时
- `MAX_COMPILE_LATENCY`：优化器的最大延时
- `AVG_MEM`：使用的平均内存，单位 byte
- `MAX_MEM`：使用的最大内存，单位 byte

和 TiKV Coprocessor Task 相关的字段：

- `COP_TASK_NUM`：每条 SQL 发送的 Coprocessor 请求数量
- `AVG_COP_PROCESS_TIME`：cop-task 的平均处理时间
- `MAX_COP_PROCESS_TIME`：cop-task 的最大处理时间
- `MAX_COP_PROCESS_ADDRESS`：执行时间最长的 cop-task 所在地址
- `AVG_COP_WAIT_TIME`：cop-task 的平均等待时间
- `MAX_COP_WAIT_TIME`：cop-task 的最大等待时间
- `MAX_COP_WAIT_ADDRESS`：等待时间最长的 cop-task 所在地址
- `AVG_PROCESS_TIME`：SQL 在 TiKV 的平均处理时间
- `MAX_PROCESS_TIME`：SQL 在 TiKV 的最大处理时间
- `AVG_WAIT_TIME`：SQL 在 TiKV 的平均等待时间
- `MAX_WAIT_TIME`：SQL 在 TiKV 的最大等待时间
- `AVG_BACKOFF_TIME`：SQL 遇到需要重试的错误时在重试前的平均等待时间
- `MAX_BACKOFF_TIME`：SQL 遇到需要重试的错误时在重试前的最大等待时间
- `AVG_TOTAL_KEYS`：Coprocessor 扫过的 key 的平均数量
- `MAX_TOTAL_KEYS`：Coprocessor 扫过的 key 的最大数量
- `AVG_PROCESSED_KEYS`：Coprocessor 处理的 key 的平均数量。相比 `avg_total_keys`，`avg_processed_keys` 不包含 MVCC 的旧版本。如果 `avg_total_keys` 和 `avg_processed_keys` 相差很大，说明旧版本比较多
- `MAX_PROCESSED_KEYS`：Coprocessor 处理的 key 的最大数量

和事务相关的字段：

- `AVG_PREWRITE_TIME`：prewrite 阶段消耗的平均时间
- `MAX_PREWRITE_TIME` prewrite 阶段消耗的最大时间
- `AVG_COMMIT_TIME`：commit 阶段消耗的平均时间
- `MAX_COMMIT_TIME`：commit 阶段消耗的最大时间
- `AVG_GET_COMMIT_TS_TIME`：获取 commit_ts 的平均时间
- `MAX_GET_COMMIT_TS_TIME`：获取 commit_ts 的最大时间
- `AVG_COMMIT_BACKOFF_TIME`：commit 时遇到需要重试的错误时在重试前的平均等待时间
- `MAX_COMMIT_BACKOFF_TIME`：commit 时遇到需要重试的错误时在重试前的最大等待时间
- `AVG_RESOLVE_LOCK_TIME`：解决事务的锁冲突的平均时间
- `MAX_RESOLVE_LOCK_TIME`：解决事务的锁冲突的最大时间
- `AVG_LOCAL_LATCH_WAIT_TIME`：本地事务等待的平均时间
- `MAX_LOCAL_LATCH_WAIT_TIME`：本地事务等待的最大时间
- `AVG_WRITE_KEYS`：写入 key 的平均数量
- `MAX_WRITE_KEYS`：写入 key 的最大数量
- `AVG_WRITE_SIZE`：写入的平均数据量，单位 byte
- `MAX_WRITE_SIZE`：写入的最大数据量，单位 byte
- `AVG_PREWRITE_REGIONS`：prewrite 涉及的平均 Region 数量
- `MAX_PREWRITE_REGIONS`：prewrite 涉及的最大 Region 数量
- `AVG_TXN_RETRY`：事务平均重试次数
- `MAX_TXN_RETRY`：事务最大重试次数
- `SUM_BACKOFF_TIMES`：这类 SQL 遇到需要重试的错误后的总重试次数
- `BACKOFF_TYPES`：遇到需要重试的错误时的所有错误类型及每种类型重试的次数，格式为 `类型:次数`。如有多种错误则用 `,` 分隔，例如 `txnLock:2,pdRPC:1`
- `AVG_AFFECTED_ROWS`：平均影响行数
- `PREV_SAMPLE_TEXT`：当 SQL 是 `COMMIT` 时，该字段为 `COMMIT` 的前一条语句；否则该字段为空字符串。当 SQL 是 `COMMIT` 时，按 digest 和 `prev_sample_text` 一起分组，即不同 `prev_sample_text` 的 `COMMIT` 也会分到不同的行

## `events_statements_summary_by_digest_history`

`events_statements_summary_by_digest_history` 的表结构与 `events_statements_summary_by_digest` 完全相同，用于保存历史时间段的数据。通过历史数据，可以排查过去出现的异常，也可以对比不同时间的监控指标。

字段 `SUMMARY_BEGIN_TIME` 和 `SUMMARY_END_TIME` 代表历史时间段的开始时间和结束时间。

## 排查示例

下面用两个示例问题演示如何利用 statement summary 来排查。

### SQL 延迟比较大，是不是服务端的问题？

例如客户端显示 employee 表的点查比较慢，那么可以按 SQL 文本来模糊查询：

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM performance_schema.events_statements_summary_by_digest
    WHERE digest_text LIKE 'select * from employee%';
```

结果如下，`avg_latency` 是 1 ms 和 0.3 ms，在正常范围，所以可以判定不是服务端的问题，继而排查客户端或网络问题。

```
+-------------+------------+------------------------------------------+
| avg_latency | exec_count | query_sample_text                        |
+-------------+------------+------------------------------------------+
|     1042040 |          2 | select * from employee where name='eric' |
|      345053 |          3 | select * from employee where id=3100     |
+-------------+------------+------------------------------------------+
2 rows in set (0.00 sec)
```

### 哪类 SQL 的总耗时最高？

假如上午 10:00 到 10:30 的 QPS 明显下降，可以从历史表中找出当时耗时最高的三类 SQL：

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM performance_schema.events_statements_summary_by_digest_history
    WHERE summary_begin_time='2020-01-02 10:00:00'
    ORDER BY sum_latency DESC LIMIT 3;
```

结果显示以下三类 SQL 的总延迟最高，所以这些 SQL 需要重点优化。

```
+-------------+-------------+------------+-----------------------------------------------------------------------+
| sum_latency | avg_latency | exec_count | query_sample_text                                                     |
+-------------+-------------+------------+-----------------------------------------------------------------------+
|     7855660 |     1122237 |          7 | select avg(salary) from employee where company_id=2013                |
|     7241960 |     1448392 |          5 | select * from employee join company on employee.company_id=company.id |
|     2084081 |     1042040 |          2 | select * from employee where name='eric'                              |
+-------------+-------------+------------+-----------------------------------------------------------------------+
3 rows in set (0.00 sec)
```

## 参数配置

statement summary 功能默认关闭，通过设置系统变量打开，例如：

```sql
set global tidb_enable_stmt_summary = true;
```

statement summary 关闭后，系统表里的数据会被清空，下次打开后重新统计。经测试，打开后对性能几乎没有影响。

还有两个控制 statement summary 的系统变量：

- `tidb_stmt_summary_refresh_interval`：`events_statements_summary_by_digest` 的清空周期，单位是秒 (s)，默认值是 `1800`。
- `tidb_stmt_summary_history_size`：`events_statements_summary_by_digest_history` 保存每种 SQL 的历史的数量，默认值是 `24`。

statement summary 配置示例如下：

```sql
set global tidb_stmt_summary_refresh_interval = 1800;
set global tidb_stmt_summary_history_size = 24;
```

以上配置生效后，`events_statements_summary_by_digest` 每 30 分钟清空一次，`events_statements_summary_by_digest_history` 保存最近 12 小时的历史数据。

以上两个系统变量都有 global 和 session 两种作用域，它们的生效方式与其他系统变量不一样：

- 设置 global 变量后整个集群立即生效
- 设置 session 变量后当前 TiDB server 立即生效，这对于调试单个 TiDB server 比较有用
- 优先读 session 变量，没有设置过 session 变量才会读 global 变量
- 把 session 变量设为空字符串，将会重新读 global 变量

由于 statement summary tables 是内存表，为了防止内存问题，需要限制保存的 SQL 条数和 SQL 的最大显示长度。这两个参数都在 config.toml 的 `[stmt-summary]` 类别下配置：

- 通过 `max-stmt-count` 更改保存的 SQL 种类数量，默认 200 条。当 SQL 种类超过 `max-stmt-count` 时，会移除最近没有使用的 SQL。
- 通过 `max-sql-length` 更改 `DIGEST_TEXT` 和 `QUERY_SAMPLE_TEXT` 的最大显示长度，默认是 4096。

> **注意：**
>
> `tidb_stmt_summary_history_size`、`max-stmt-count`、`max-sql-length` 这些配置都影响内存占用，建议根据实际情况调整，不宜设置得过大。

## 目前的限制

Statement summary tables 现在还存在一些限制：

- 查询 statement summary tables 时，只会显示当前 TiDB server 的 statement summary，而不是整个集群的 statement summary。
- TiDB server 重启后 statement summary 会丢失。因为 statement summary tables 是内存表，不会持久化数据，所以一旦 server 被重启，statement summary 随之丢失。
