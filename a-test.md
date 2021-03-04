---
title: TiDB Cluster Alert Rules
summary: Learn the alert rules in a TiDB cluster.
aliases: ['/docs/dev/alert-rules/','/docs/dev/reference/alert-rules/']
---

<!-- markdownlint-disable MD024 -->
<!-- markdownlint-disable MD024 -->

<!--

-->

# TiDB Cluster Alert Rules

This document describes the alert rules for different components in a TiDB cluster, including the rule descriptions and solutions of the alert items in TiDB, TiKV, PD, TiDB Binlog, Node_exporter and Blackbox_exporter.

According to the severity level, alert rules are divided into three categories (from high to low): emergency-level, critical-level and warning-level.

## TiDB alert rules

This section gives the
alert rules for the TiDB component.

```sql
INSERT INTO t(c) VALUES (1);
INSERT INTO t(c) VALUES (2);
INSERT INTO t(c) VALUES (3), (4), (5);
```

### Emergency-level alerts

Emergency-level alerts are often caused by a service or node failure. Manual intervention is required immediately.

```sql
DESC mysql.expr_pushdown_blacklist;

+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------+
| id                         | estRows | actRows | task      | access object | execution info                                                               | operator info                   | memory    | disk |
+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------+
| StreamAgg_16               | 1.00    | 1       | root      |               | time:170.08572ms, loops:2                                                     | funcs:count(Column#5)->Column#3 | 372 Bytes | N/A  |
| └─TableReader_17           | 1.00    | 1       | root      |               | time:170.080369ms, loops:2, rpc num: 1, rpc time:17.023347ms, proc keys:28672 | data:StreamAgg_8                | 202 Bytes | N/A  |
|   └─StreamAgg_8            | 1.00    | 1       | cop[tikv] |               | time:170ms, loops:29                                                          | funcs:count(1)->Column#5        | N/A       | N/A  |
|     └─TableFullScan_15     | 7.00    | 28672   | cop[tikv] | table:t       | time:170ms, loops:29                                                          | keep order:false, stats:pseudo  | N/A       | N/A  |
+----------------------------+---------+---------+-----------+---------------+------------------------------------------------------------------------------+---------------------------------+-----------+------
```

## TiKV

- Support Region Merge
- Inform PD immediately once the Raft snapshot
  process is completed, to speed up balancing
- Add the Raw DeleteRange API
- Add the GetMetric API
- Reduce the I/O fluctuation caused by RocksDB sync files
- Optimize the space reclaiming mechanism after deleting data
- Improve the data recovery tool `tikv-ctl`
- Fix the issue that it is slow to make nodes down caused by snapshot
- Support streaming in Coprocessor
- Support Readpool and increase the `raw_get/get/batch_get` by 30%

> Note:
>
> lalalala

| Service type         | EC2 type     | Instance count |
|:----------|:----------|:----------|
| PD        | m5.xlarge |     3     |
| TiKV      | i3.4xlarge|     3     |
| TiDB      | c5.4xlarge|     3     |
| Sysbench  | m5.4xlarge|     1     |

1. Deploy TiDB v4.0
   and v3.0 using TiUP.

2. Use BenchmarkSQL to import the TPC-C 5000 Warehouse data.

    1. Compile BenchmarkSQL：

        {{< copyable "bash" >}}

        ```bash
        git clone https://github.com/pingcap/benchmarksql && cd benchmarksql && ant
        ```

    2. Enter the `run` directory, edit the `props.mysql` file according to the actual situation, and modify the `conn`, `warehouses`, `loadWorkers`, `terminals`, and `runMins` configuration items.

        a. Build a hash table from the outer rows
        b. Build key ranges from outer rows and fetches inner rows
        c. Probe the hash table and sends the join result to the result channel. Note: step a and step b are running concurrently.

        > **Note:**
        >
        > Direct modification of `run_tidb.sh` may be overwritten. So in a production environment, it is recommended to use TiUP if you need to bind the core.

    3. Execute TPC-H queries and record the executing time of each query.

        * For TiDB v3.0, use the MySQL client to connect to TiDB, execute the queries, and record the execution time of each query.
        * For TiDB v4.0, use the MySQL client to connect to TiDB, and choose one of the following operations based on where data is read from:
            * If data is read only from TiKV, set `set @@session.tidb_isolation_read_engines = 'tikv,tidb';`, execute the queries, and record the execution time of each query.
            * If data is read from TiKV and TiFlash automatically based on cost-based intelligent choice, set `set @@session.tidb_isolation_read_engines = 'tikv,tiflash,tidb';`, execute the query, and record the execution time of each query.

    4. Example 4

        + TiCDC

            - Support Kafka SSL connection [#764](https://github.com/pingcap/ticdc/pull/764)
            - Support outputting the old value [#708](https://github.com/pingcap/ticdc/pull/708)
            - Add the column flags [#796](https://github.com/pingcap/ticdc/pull/796)
            - Support outputting the DDL statements and table schema of the previous
            version [#799](https://github.com/pingcap/ticdc/pull/799)

    5. Example 5

        Our thanks go to the following contributors from the community for helping this release:
        - [sduzh](https://github.com/sduzh)
        - [lizhenda](https://github.com/lizhenda)

* The `STOCK` table has W \* 100,000 records
  (Each warehouse corresponds to the stock data of 100,000 items)
* The `DISTRICT` table has W \* 10 records (Each warehouse provides services to 10 districts)
* The `CUSTOMER` table has W \* 10 \* 3,000 records (Each district has 3,000 customers)
* The `HISTORY` table has W \* 10 \* 3,000 records (Each customer has one transaction history)
* The `ORDER` table has W \* 10 \* 3,000 records (Each district has 3,000 orders and the last 900 orders generated are added to the `NEW-ORDER` table. Each order randomly generates 5 ~ 15 ORDER-LINE records.

<table>
  <thead><tr><th>Loader</th><th>TiDB Lightning</th></tr></thead>
<tbody>
<tr><td>

</td></tr>
</tbody>
</table>

```
--------------
mysql  Ver 15.1 Distrib 10.4.10-MariaDB, for Linux (x86_64) using readline 5.1

Connection id:       1
Current database:    test
Current user:        root@127.0.0.1
SSL:                 Cipher in use is TLS_AES_256_GCM_SHA384
```