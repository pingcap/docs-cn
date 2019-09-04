---
title: How to Run TPC-C Test on TiDB
category: benchmark
---

# How to Run TPC-C Test on TiDB

This document describes how to test TiDB using [TPC-C](http://www.tpc.org/tpcc/).

TPC-C is an online transaction processing (OLTP) benchmark. It tests the OLTP system by using a commodity sales model that involves the following five transactions of different types:

* NewOrder
* Payment
* OrderStatus
* Delivery
* StockLevel

## Prepare

Before testing, TPC-C Benchmark specifies the initial state of the database, which is the rule for data generation in the database. The `ITEM` table contains a fixed number of 100,000 items, while the number of warehouses can be adjusted. If there are W records in the `WAREHOUSE` table, then:

* The `STOCK` table has W \* 100,000 records (Each warehouse corresponds to the stock data of 100,000 items)
* The `DISTRICT` table has W \* 10 records (Each warehouse provides services to 10 districts)
* The `CUSTOMER` table has W \* 10 \* 3,000 records (Each district has 3,000 customers)
* The `HISTORY` table has W \* 10 \* 3,000 records (Each customer has one transaction history)
* The `ORDER` table has W \* 10 \* 3,000 records (Each district has 3,000 orders and the last 900 orders generated are added to the `NEW-ORDER` table. Each order randomly generates 5 ~ 15 ORDER-LINE records.

In this document, the testing uses 1,000 warehouses as an example to test TiDB.

TPC-C uses tpmC (transactions per minute) to measure the maximum qualified throughput (MQTh, Max Qualified Throughput). The transactions are the NewOrder transactions and the final unit of measure is the number of new orders processed per minute.

This testing uses the open-source BenchmarkSQL 5.0 as the TPC-C testing tool and adds the support for the MySQL protocol. You can download the testing program by using the following command:

```shell
git clone -b 5.0-mysql-support-opt-2.1 https://github.com/pingcap/benchmarksql.git
```

To install Java and Ant, run the following command (take CentOS as an example):

```shell
sudo yum install -y java ant
```

Enter the `benchmarksql` directory and run `ant` to build:

```shell
cd benchmarksql
ant
```

## Deploy the TiDB cluster

For 1,000 warehouses, the TiDB cluster can be deployed on three machines, with one TiDB instance, one PD instance, and one TiKV instance on each machine.

For example, the hardware configuration is as follows:

| Type | Name |
| :--- | :---|
| OS | Linux (CentOS 7.3.1611) |
| CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| RAM | 128GB |
| DISK | Optane 500GB SSD |

1. Because this type of CPU has an NUMA architecture, it is recommended to bind the core using `taskset` and view the NUMA node using `lscpu`. For example:

    ```text
    NUMA node0 CPU(s):     0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38
    NUMA node1 CPU(s):     1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39
    ```

2. Start TiDB using the following command:

    ```shell
    nohup taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38 bin/tidb-server
    nohup taskset -c 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39 bin/tidb-server
    ```

3. You can deploy a HAproxy to balance the load of multiple TiDB nodes. It is recommended to configure `nbproc` as the number of CPU cores.

## Edit the configuration

### Configure TiDB

```toml
[log]
level = "error"

[performance]
# Sets the maximum number of CPU cores to use for a single TiDB instance according to NUMA configuration.
max-procs = 20

[prepared_plan_cache]
# Enables the prepared plan cache in TiDB configuration to reduce the overhead of optimizing your execution plan.
enabled = true
```

### Configure TiKV

You can use the basic configuration at the beginning. Then after the test is run, you can adjust it based on the metrics on Grafana and the [TiKV Tuning Instructions](/v3.0/reference/performance/tune-tikv.md).

### Configure BenchmarkSQL

Edit the `benchmarksql/run/props.mysql` file:

```text
conn=jdbc:mysql://{HAPROXY-HOST}:{HAPROXY-PORT}/tpcc?useSSL=false&useServerPrepStmts=true&useConfigs=maxPerformance
warehouses=1000 # Uses 1,000 warehouses.
terminals=500   # Uses 500 terminals.
loadWorkers=32  # The number of concurrent workers that load data.
```

## Load data

1. Use a MySQL client to connect to the TiDB server and run the following command:

    ```sql
    create database tpcc
    ```

2. Run the following BenchmarkSQL script in shell to create tables:

    ```shell
    cd run
    ./runSQL.sh props.mysql sql.mysql/tableCreates.sql
    ./runSQL.sh props.mysql sql.mysql/indexCreates.sql
    ```

3. Run the following script to load data:

    ```shell
    ./runLoader.sh props.mysql
    ```

This process might last for several hours depending on the machine configuration.

After importing data, you can run `sql.common/test.sql` to validate the correctness of the data. If all SQL statements return an empty result, then the data is correctly imported.

## Run the test

Run the following BenchmarkSQL test script:

```shell
nohup ./runBenchmark.sh props.mysql &> test.log &
```

After the execution is finished, view the result using `test.log`:

```text
07:09:53,455 [Thread-351] INFO   jTPCC : Term-00, Measured tpmC (NewOrders) = 77373.25
07:09:53,455 [Thread-351] INFO   jTPCC : Term-00, Measured tpmTOTAL = 171959.88
07:09:53,455 [Thread-351] INFO   jTPCC : Term-00, Session Start     = 2019-03-21 07:07:52
07:09:53,456 [Thread-351] INFO   jTPCC : Term-00, Session End       = 2019-03-21 07:09:53
07:09:53,456 [Thread-351] INFO   jTPCC : Term-00, Transaction Count = 345240
```

The value in the tpmC section is the testing result.

After the test completes, you can also run `sql.common/test.sql` to validate the correctness of the data. If all SQL statements return an empty result, then the testing of the data is correctly performed.
