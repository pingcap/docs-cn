---
title: Statement Summary Table
category: reference
---

# Statement Summary Table

## 前言
我们在排查线上 TiDB 问题时，可能有下面这样的需求：
- SQL 延迟比较大，是不是服务端的问题？
- 哪类 SQL 的总耗时最高？

遇到这类需要定位 SQL 的问题，我们会首先想到两种方式来排查：
- 打开 general log，但是打印 general log 对 Server 的性能会有影响。
- `admin show slow` 显示慢查询日志，但是有问题的 SQL 可能没有被归为慢 SQL。

针对于这些 SQL 类的性能问题，MySQL 在 `performance_schema` 提供了 [statement summary tables](https://dev.mysql.com/doc/refman/5.6/en/statement-summary-tables.html)，用来监控和统计 SQL。例如其中的一张表 `events_statements_summary_by_digest`，提供了丰富的字段，包括延迟、执行次数、扫描行数、全表扫描次数等，有助于用户定位 SQL 问题。

为此，从 3.0.4 版本开始，TiDB 也提供系统表 `events_statements_summary_by_digest`，方便用户定位 SQL 问题。

## events_statements_summary_by_digest 介绍
`events_statement_summary_by_digest` 是 `performance_schema` 里的一张系统表。顾名思义，它把 SQL 按 digest 分组，统计每一组的 SQL 信息。

digest 是什么呢？它与 slow log 里的 digest 一样，是把 SQL 规范化后算出的唯一标识符。
SQL 的规范化会忽略常量、空白符、大小写的差别。也就是说，只要语法一致，就会归到同一类。

例如：
```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```
规范化后都是：
```sql
select * from employee where id in (...) and salary between ? and ?;
```

接下来详细看一下 `events_statements_summary_by_digest` 的表结构。
因为 TiDB 中的很多概念不同于 MySQL，所以 `events_statements_summary_by_digest` 也与 MySQL 有一些区别。

查询 `events_statements_summary_by_digest` 的输出示例：
```
      SCHEMA_NAME: test
           DIGEST: 0611cc2fe792f8c146cc97d39b31d9562014cf15f8d41f23a4938ca341f54182
      DIGEST_TEXT: select * from employee where id = ?
       EXEC_COUNT: 3
      SUM_LATENCY: 1035161
      MAX_LATENCY: 399594
      MIN_LATENCY: 301353
      AVG_LATENCY: 345053
SUM_ROWS_AFFECTED: 0
       FIRST_SEEN: 2019-09-12 18:47:14
        LAST_SEEN: 2019-09-12 18:47:16
QUERY_SAMPLE_TEXT: select * from employee where id=3100
```

以下是各个字段的含义：

| 列名           | 含义                      |
|:----------------- |:-------------------------------- |
| SCHEMA_NAME       | 执行这类 SQL 的当前 schema |
| DIGEST            | SQL 的 digest                   |
| DIGEST_TEXT       | 规范化后的 SQL              |
| EXEC_COUNT        | 这类 SQL 执行的总次数    |
| SUM_LATENCY       | 这类 SQL 执行的总延迟，单位 ns |
| MAX_LATENCY       | 这类 SQL 执行的最大延迟，单位 ns |
| MIN_LATENCY       | 这类 SQL 执行的最小延迟，单位 ns |
| AVG_LATENCY       | 这类 SQL 执行的平均延迟，单位 ns |
| SUM_ROWS_AFFECTED | 这类 SQL 的总影响行数    |
| FIRST_SEEN        | 这类 SQL 第一次执行的时间 |
| LAST_SEEN         | 这类 SQL 最后一次执行的时间 |
| QUERY_SAMPLE_TEXT | 这类 SQL 首次出现的原 SQL 语句 |

## 排查示例
对于文章开头描述的几个问题，下面来演示如何利用 statement summary 来排查。

### SQL 延迟比较大，是不是服务端的问题？
例如客户端显示 employee 表的点查比较慢，那么可以按 SQL 文本来模糊查询：
```sql
SELECT avg_latency, exec_count, query_sample_text 
    FROM performance_schema.events_statements_summary_by_digest 
    WHERE digest_text LIKE ‘select * from employee%’;
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
如果要对系统调优，可以找出耗时最高的 3 类 SQL：
```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
	FROM performance_schema.events_statements_summary_by_digest
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
statement summary 功能默认关闭，通过设置系统变量打开。例如：
```sql
set global tidb_enable_stmt_summary = true;
```

`tidb_enable_stmt_summary` 有 global 和 session 两种作用域，它们的生效方式与其他系统变量不一样：
- 设置 global 变量后整个集群立即生效
- 设置 session 变量后当前节点立即生效，这对于调试单个节点比较有用
- 优先读 session 变量，没有设置过 session 变量才会读 global 变量
- 把 session 变量设为空字符串，将会重新读 global 变量

statement summary 关闭后，系统表里的数据会被清空，下次打开后重新统计。经测试，打开后对性能几乎没有影响。

由于 `events_statements_summary_by_digest` 是内存表，为了防止内存问题，需要限制保存的 SQL 条数和 SQL 的最大显示长度。这两个参数都在 config.toml 的 [stmt-summary] 类别下配置：
- 通过 `max-stmt-count` 更改保存的 SQL 种类数量，默认 100 条。当 SQL 种类超过 `max-stmt-count` 时，会移除最近没有使用的 SQL。
- 通过 `max-sql-length` 更改 `DIGEST_TEXT` 和 `QUERY_SAMPLE_TEXT` 的最大显示长度，默认是 4096。

这两个参数建议根据实际情况调整，不宜设置得过大。

## 目前的限制
`events_statements_summary_by_digest` 现在还存在一起限制：

- 查询 `events_statements_summary_by_digest` 时，只会显示当前节点的 statement summary，而不是整个群集的 statement summary。
- statement summary 不会滚动更新。一旦 `tidb_enable_stmt_summary` 打开，SQL 信息就开始统计。随着时间的推移，statement summary 累加，所以无法查看最近一段时间内的 statement summary。所以最佳实践是，需要排查问题的时候再打开，查看一段时间内的 statement summary。
- TiDB Server 重启后 statement summary 丢失。因为 `events_statements_summary_by_digest` 是内存表，不会持久化数据，所以一旦 Server 被重启，statement summary 随之丢失。
