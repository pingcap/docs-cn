---
title: Quick start with HTAP
summary: Learn how to quickly get started with the TiDB HTAP.
---

# Quick Start Guide for TiDB HTAP

This guide walks you through the quickest way to get started with TiDB's one-stop solution of Hybrid Transactional and Analytical Processing (HTAP).

> **Note:**
>
> The steps provided in this guide is ONLY for quick start in the test environment. For production environments, [explore HTAP](/explore-htap.md) is recommended. 

## Basic concepts

Before using TiDB HTAP, you need to have some basic knowledge about [TiKV](/tikv-overview.md), a row-based storage engine for TiDB Online Transactional Processing (OLTP), and [TiFlash](/tiflash/tiflash-overview.md), a columnar storage engine for TiDB Online Analytical Processing (OLAP).

- Storage engines of HTAP: The row-based storage engine and the columnar storage engine co-exist for HTAP. Both storage engines can replicate data automatically and keep strong consistency. The row-based storage engine optimizes OLTP performance, and the columnar storage engine optimizes OLAP performance.
- Data consistency of HTAP: As a distributed and transactional key-value database, TiKV provides transactional interfaces with ACID compliance, and guarantees data consistency between multiple replicas and high availability with the implementation of the [Raft consensus algorithm](https://raft.github.io/raft.pdf). As a columnar storage extension of TiKV, TiFlash replicates data from TiKV in real time according to the Raft Learner consensus algorithm, which ensures that data is strongly consistent between TiKV and TiFlash.
- Data isolation of HTAP: TiKV and TiFlash can be deployed on different machines as needed to solve the problem of HTAP resource isolation.
- MPP computing engine: [MPP](/tiflash/use-tiflash.md#control-whether-to-select-the-mpp-mode) is a distributed computing framework provided by the TiFlash engine since TiDB 5.0, which allows data exchange between nodes and provides high-performance, high-throughput SQL algorithms. In the MPP mode, the run time of the analytic queries can be significantly reduced.

## Steps

In this document, you can experience the convenience and high performance of TiDB HTAP by querying an example table in a popular [TPC-H](http://www.tpc.org/tpch/) dataset.

### Step 1. Deploy a local test environment 

Before using TiDB HTAP, follow the steps in the [Quick Start Guide for the TiDB Database Platform](/quick-start-with-tidb.md) to prepare a local test environment, and run the following command to deploy a TiDB cluster:

{{< copyable "shell-regular" >}}

```shell
tiup playground
```

> **Note:**
>
> `tiup playground` command is ONLY for quick start, NOT for production.

### Step 2. Prepare test data

In the following steps, you can create a [TPC-H](http://www.tpc.org/tpch/) dataset as the test data to use TiDB HTAP. If you are interested in TPC-H, see [General Implementation Guidelines](http://tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.0.pdf).

> **Note:**
>
> If you want to use your existing data for analytic queries, you can [migrate your data to TiDB](/migration-overview.md). If you want to design and create your own test data, you can create it by executing SQL statements or using related tools.

1. Install the test data generation tool by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install bench
    ```

2. Generate the test data by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

    If the output of this command shows `Finished`, it indicates that the data is created.

3. Execute the following SQL statement to view the generated data:

    {{< copyable "sql" >}}

    ```sql
    SELECT 
      CONCAT(table_schema,'.',table_name) AS 'Table Name', 
      table_rows AS 'Number of Rows', 
      FORMAT_BYTES(data_length) AS 'Data Size', 
      FORMAT_BYTES(index_length) AS 'Index Size', 
      FORMAT_BYTES(data_length+index_length) AS'Total' 
    FROM 
      information_schema.TABLES 
    WHERE 
      table_schema='test';
    ```

    As you can see from the output, eight tables are created in total, and the largest table has 6.5 million rows (the number of rows created by the tool depends on the actual SQL query result because the data is randomly generated).

    ```sql
    +---------------+----------------+-----------+------------+-----------+
    |  Table Name   | Number of Rows | Data Size | Index Size |   Total   |
    +---------------+----------------+-----------+------------+-----------+
    | test.nation   |             25 | 2.44 KiB  | 0 bytes    | 2.44 KiB  |
    | test.region   |              5 | 416 bytes | 0 bytes    | 416 bytes |
    | test.part     |         200000 | 25.07 MiB | 0 bytes    | 25.07 MiB |
    | test.supplier |          10000 | 1.45 MiB  | 0 bytes    | 1.45 MiB  |
    | test.partsupp |         800000 | 120.17 MiB| 12.21 MiB  | 132.38 MiB|
    | test.customer |         150000 | 24.77 MiB | 0 bytes    | 24.77 MiB |
    | test.orders   |        1527648 | 174.40 MiB| 0 bytes    | 174.40 MiB|
    | test.lineitem |        6491711 | 849.07 MiB| 99.06 MiB  | 948.13 MiB|
    +---------------+----------------+-----------+------------+-----------+
    8 rows in set (0.06 sec)
     ```

    This is a database of a commercial ordering system. In which, the `test.nation` table indicates the information about countries, the `test.region` table indicates the information about regions, the `test.part` table indicates the information about parts, the `test.supplier` table indicates the information about suppliers, the `test.partsupp` table indicates the information about parts of suppliers, the `test.customer` table indicates the information about customers, the `test.customer` table indicates the information about orders, and the `test.lineitem` table indicates the information about online items.

### Step 3. Query data with the row-based storage engine

To know the performance of TiDB with only the row-based storage engine, execute the following SQL statements:

{{< copyable "sql" >}}

```sql
SELECT
    l_orderkey,
    SUM(
        l_extendedprice * (1 - l_discount)
    ) AS revenue,
    o_orderdate,
    o_shippriority
FROM
    customer,
    orders,
    lineitem
WHERE
    c_mktsegment = 'BUILDING'
AND c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND o_orderdate < DATE '1996-01-01'
AND l_shipdate > DATE '1996-02-01'
GROUP BY
    l_orderkey,
    o_orderdate,
    o_shippriority
ORDER BY
    revenue DESC,
    o_orderdate
limit 10;
```

This is a shipping priority query, which provides the priority and potential revenue of the highest-revenue order that has not been shipped before a specified date. The potential revenue is defined as the sum of `l_extendedprice * (1-l_discount)`. The orders are listed in the descending order of revenue. In this example, this query lists the unshipped orders with potential query revenue in the top 10.

### Step 4. Replicate the test data to the columnar storage engine

After TiFlash is deployed, TiKV does not replicate data to TiFlash immediately. You need to execute the following DDL statements in a MySQL client of TiDB to specify which tables need to be replicated. After that, TiDB will create the specified replicas in TiFlash accordingly. 

{{< copyable "sql" >}}

```sql
ALTER TABLE test.customer SET TIFLASH REPLICA 1;
ALTER TABLE test.orders SET TIFLASH REPLICA 1;
ALTER TABLE test.lineitem SET TIFLASH REPLICA 1;
```

To check the replication status of the specific tables, execute the following statements:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'customer';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'orders';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'lineitem';
```

In the result of the above statements:

- `AVAILABLE` indicates whether the TiFlash replica of a specific table is available or not. `1` means available and `0` means unavailable. Once a replica becomes available, this status does not change any more. If you use DDL statements to modify the number of replicas, the replication status will be recalculated.
- `PROGRESS` means the progress of the replication. The value is between 0.0 and 1.0. 1 means at least one replica is replicated.

### Step 5. Analyze data faster using HTAP

Execute the SQL statements in [Step 3](#step-3-query-data-with-the-row-based-storage-engine) again, and you can see the performance of TiDB HTAP.

For tables with TiFlash replicas, the TiDB optimizer automatically determines whether to use TiFlash replicas based on the cost estimation. To check whether or not a TiFlash replica is selected, you can use the `desc` or `explain analyze` statement. For example:

{{< copyable "sql" >}}

```sql
explain analyze SELECT
    l_orderkey,
    SUM(
        l_extendedprice * (1 - l_discount)
    ) AS revenue,
    o_orderdate,
    o_shippriority
FROM
    customer,
    orders,
    lineitem
WHERE
    c_mktsegment = 'BUILDING'
AND c_custkey = o_custkey
AND l_orderkey = o_orderkey
AND o_orderdate < DATE '1996-01-01'
AND l_shipdate > DATE '1996-02-01'
GROUP BY
    l_orderkey,
    o_orderdate,
    o_shippriority
ORDER BY
    revenue DESC,
    o_orderdate
limit 10;
```

If the result of the `EXPLAIN` statement shows `ExchangeSender` and `ExchangeReceiver` operators, it indicates that the MPP mode has taken effect.

In addition, you can specify that each part of the entire query is computed using only the TiFlash engine. For detailed information, see [Use TiDB to read TiFlash replicas](/tiflash/use-tiflash.md#use-tidb-to-read-tiflash-replicas).

You can compare query results and query performance of these two methods.

## What's next

- [Architecture of TiDB HTAP](/tiflash/tiflash-overview.md#architecture)
- [Explore HTAP](/explore-htap.md)
- [Use TiFlash](/tiflash/use-tiflash.md#use-tiflash)
