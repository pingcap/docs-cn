---
title: Statement Summary Table
summary: Learn about Statement Summary Table in TiDB.
category: reference
---

# Statement Summary Table

To better handle SQL performance related issues, MySQL has provided [statement summary tables](https://dev.mysql.com/doc/refman/5.6/en/statement-summary-tables.html) in `performance_schema` to monitor SQL with statistics. Among these tables, `events_statements_summary_by_digest` is very useful in locating SQL problems with its abundant fields such as latency, execution times, rows scanned, and full table scans.

Starting from v3.0.4, TiDB provides the support for the `events_statements_summary_by_digest`
table. In this document, you will learn about this feature, and how to troubleshoot SQL performance issues with it.

## Introduction

`events_statement_summary_by_digest` is a system table in `performance_schema`. As indicated by the name, it groups the SQL statements by digests, and provides statistics for each SQL group.

The "digest" here means the same as used in slow logs, which is a unique identifier calculated through normalized SQL statements. The normalization process ignores constant, blank characters, and is case insensitive. Therefore, statements with consistent syntaxes will be grouped as one category. For example:

```sql
SELECT * FROM employee WHERE id IN (1, 2, 3) AND salary BETWEEN 1000 AND 2000;
select * from EMPLOYEE where ID in (4, 5) and SALARY between 3000 and 4000;
```

After normalization, they are both of the following category:

```sql
select * from employee where id in (...) and salary between ? and ?;
```

Some concepts in TiDB are different from that in MySQL. For this reason, the schema of `events_statements_summary_by_digest` in TiDB differs.

The following is a sample output of querying `events_statements_summary_by_digest`:

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

Description of each field:

| Column Name          | Description                      |
|:----------------- |:-------------------------------- |
| SCHEMA_NAME       | The current schema under which the group of SQL statements are executed|
| DIGEST            | The digest of the SQL statement                   |
| DIGEST_TEXT       | Normalized SQL statement              |
| EXEC_COUNT        | Total execution times of SQL statements of this category   |
| SUM_LATENCY       | Total execution latency (ns) of SQL statements of this category  |
| MAX_LATENCY       | Maximum latency (ns) of SQL statements of this category  |
| MIN_LATENCY       | Minimum latency (ns) of SQL statements of this category|
| AVG_LATENCY       | Average latency (ns) of SQL statements of this category |
| SUM_ROWS_AFFECTED | Rows impacted by SQL statements of this category |
| FIRST_SEEN        | Duration of the first execution for SQL statements of this category|
| LAST_SEEN         |  Duration of the last execution for SQL statements of this category|
| QUERY_SAMPLE_TEXT | The original SQL statement where SQL statements of this category firstly appeared |

## Troubleshooting examples

This section shows how to use the statement summary feature to troubleshoot SQL performance issues using two sample questions.

### Could high SQL latency be caused by the server end?

In this example, the client shows slow performance with point queries on the employee table. You can perform a fuzzy search by SQL texts:

```sql
SELECT avg_latency, exec_count, query_sample_text
    FROM performance_schema.events_statements_summary_by_digest
    WHERE digest_text LIKE ‘select * from employee%’;
```

As shown in the result below, `avg_latency` of 1ms and 0.3ms are in the normal range. Therefore, it can be concluded that the server end is not the cause, and continue the troubleshooting with the client or the network.

```
+-------------+------------+------------------------------------------+
| avg_latency | exec_count | query_sample_text                        |
+-------------+------------+------------------------------------------+
|     1042040 |          2 | select * from employee where name='eric' |
|      345053 |          3 | select * from employee where id=3100     |
+-------------+------------+------------------------------------------+
2 rows in set (0.00 sec)
```

### Which categories of SQL statements consume the longest total time?

To fine tune the system, you can find out the 3 categories of SQL statements with the longest time consumption:

```sql
SELECT sum_latency, avg_latency, exec_count, query_sample_text
    FROM performance_schema.events_statements_summary_by_digest
    ORDER BY sum_latency DESC LIMIT 3;
```

The result shows that the following three SQL categories consume the longest time in total, which require focus on optimization.

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

## Configurations

The statement summary feature is disabled by default. You can enable it by setting a system variable, for example:

{{< copyable "sql" >}}

```sql
set global tidb_enable_stmt_summary = true;
```

The `tidb_enable_stmt_summary` system variable has two scopes - global and session, which work a little differently from other system variables, as described below:

- Set the global variable to apply to the cluster immediately.
- Set the session variable to apply to the current TiDB server immediately. This is useful when you debug on a single TiDB server instance.
- The session variable has a higher read priority. The global variable will be read only if no session variable is set.
- Set the session variable to a blank string to re-read the global variable.

The statistics in the system table will be cleared if the statement summary feature is disabled, and will be re-calculated next time the statement summary feature is enabled. Tests have shown that enabling this feature has little impact on performance.

`events_statements_summary_by_digest` is a memory table. To prevent potential memory issues, we need to limit the number of statements to be saved and the longest SQL display length. You can configure these limits using the following parameters under `[stmt-summary]` of `config.toml`:

- `max-stmt-count` limits the number of SQL categories that can be saved. The default value is 100. If the set limit is exceeded, the most recent SQL statements that remain unused will be removed.
- `max-sql-length` specifies the longest display length of `DIGEST_TEXT` and `QUERY_SAMPLE_TEXT`. The default value is 4096.

> **Note:**
>
> It is suggested that you adjust the configuration of this two parameters based on your actual scenarios. However, setting them to too large values is not recommended.

## Known limitations

`events_statements_summary_by_digest` has some known limitations:

- Querying `events_statements_summary_by_digest` only returns the statement summary of the current TiDB server, not the entire cluster.
- Statement summary tables do not support rolling update. This means that the SQL statistics start to accumulate the second `tidb_enable_stmt_summary` is enabled. As time goes, the numbers mount. This makes it impossible to view the statement summary of the most recent period. Therefore, it's strongly recommended that you enable `tidb_enable_stmt_summary` when you need to troubleshoot issues.
- The statement summary will be lost when the TiDB server restarts. This is because `events_statements_summary_by_digest` is a memory table, and the data is cached in memory instead of persisted on storage.
