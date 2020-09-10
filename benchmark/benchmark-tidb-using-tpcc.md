---
title: How to Run TPC-C Test on TiDB
aliases: ['/docs/dev/benchmark/benchmark-tidb-using-tpcc/','/docs/dev/benchmark/how-to-run-tpcc/']
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

{{< copyable "shell-regular" >}}

```shell
git clone -b 5.0-mysql-support-opt-2.1 https://github.com/pingcap/benchmarksql.git
```

To install Java and Ant, run the following command (take CentOS as an example):

{{< copyable "shell-regular" >}}

```shell
sudo yum install -y java ant
```

Enter the `benchmarksql` directory and run `ant` to build:

{{< copyable "shell-regular" >}}

```shell
cd benchmarksql && \
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

1. Because this type of CPU has a NUMA architecture, it is recommended to [bind the core using `numactl`](/check-before-deployment.md#install-the-numactl-tool).

2. Execute the `lscpu` command to view the NUMA nodes. The result is similar to:

    ```text
    NUMA node0 CPU(s):     0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38
    NUMA node1 CPU(s):     1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39
    ```

3. Start TiDB by adding `numactl` to the `{tidb_deploy_path}/scripts/run_tidb.sh` start-up script:

    ```text
    #!/bin/bash
    set -e

    ulimit -n 1000000

    # WARNING: This file was auto-generated. Do not edit!
    #          All your edit might be overwritten!
    DEPLOY_DIR=/home/damon/deploy/tidb1-1

    cd "${DEPLOY_DIR}" || exit 1

    export TZ=Asia/Shanghai

    # You need to specify different cpunodebind and membind for different TiDB instances on the same machine to bind different Numa nodes.
    exec numactl --cpunodebind=0  --membind=0 bin/tidb-server \
        -P 4111 \
        --status="10191" \
        --advertise-address="172.16.4.53" \
        --path="172.16.4.10:2490" \
        --config=conf/tidb.toml \
        --log-slow-query="/home/damon/deploy/tidb1-1/log/tidb_slow_query.log" \
        --log-file="/home/damon/deploy/tidb1-1/log/tidb.log" 2>> "/home/damon/deploy/tidb1-1/log/tidb_stderr.log"
    ```

    > **Note:**
    >
    > Direct modification of `run_tidb.sh` may be overwritten. So in a production environment, it is recommended to use TiUP if you need to bind the core.

4. You can deploy an HAproxy to balance the loads on multiple TiDB nodes. It is recommended to configure `nbproc` as the number of CPU cores.

## Edit the configuration

### Configure TiDB

```toml
[log]
level = "error"

[performance]
# Sets the maximum number of CPU cores to use for a single TiDB instance according to NUMA configuration.
max-procs = 20

[prepared-plan-cache]
# Enables the prepared plan cache in TiDB configuration to reduce the overhead of optimizing your execution plan.
enabled = true
```

### Configure TiKV

You can use the basic configuration at the beginning. Then after the test is run, you can adjust it based on the metrics on Grafana and the [Tune TiKV Thread Performance](/tune-tikv-thread-performance.md).

### Configure BenchmarkSQL

Edit the `benchmarksql/run/props.mysql` file:

```text
conn=jdbc:mysql://{HAPROXY-HOST}:{HAPROXY-PORT}/tpcc?useSSL=false&useServerPrepStmts=true&useConfigs=maxPerformance
warehouses=1000 # Uses 1,000 warehouses.
terminals=500   # Uses 500 terminals.
loadWorkers=32  # The number of concurrent workers that load data.
```

## Load data

**Loading data is usually the most time-consuming and problematic stage of the entire TPC-C test.** This section provides the following four steps to load data.

First, use a MySQL client to connect to the TiDB server and run the following command:

{{< copyable "sql" >}}

```sql
create database tpcc;
```

Second, run the following BenchmarkSQL script in shell to create tables:

{{< copyable "shell-regular" >}}

```shell
cd run && \
./runSQL.sh props.mysql sql.mysql/tableCreates.sql && \
./runSQL.sh props.mysql sql.mysql/indexCreates.sql
```

Third, use one of the following two ways to load data:

* [Use BenchmarkSQL to load data directly](#use-benchmarksql-to-load-data-directly)
* [Use TiDB Lightning to load data](#use-tidb-lightning-to-load-data)

### Use BenchmarkSQL to load data directly

Run the following script to load data:

{{< copyable "shell-regular" >}}

```shell
./runLoader.sh props.mysql
```

This process might last for several hours depending on the machine configuration.

### Use TiDB Lightning to load data

The amount of loaded data increases as the number of warehouses increases. When you need to load more than 1000 warehouses of data, you can first use BenchmarkSQL to generate CSV files, and then quickly load the CSV files through TiDB Lightning (hereinafter referred to as Lightning). The CSV files can be reused multiple times, which saves the time required for each generation.

Follow the steps below to use TiDB Lightning to load data:

1. Modify the BenchmarkSQL configuration file.

    The CSV file of one warehouse requires 77 MB of disk space. To ensure sufficient disk space, add a line to the `benchmarksql/run/props.mysql` file:

    ```text
    fileLocation=/home/user/csv/  # The absolute path of the directory where your CSV files are stored
    ```

    It is recommended that the CSV file names adhere to the naming rules in Lightning, that is, `{database}.{table}.csv`, because eventually you'll use Lightning to load data. Here you can modify the above configuration as follows:

    ```text
    fileLocation=/home/user/csv/tpcc.  # The absolute path of the directory where your CSV files are stored + the file name prefix (database)
    ```

    This will generate CSV files with a naming style such as `tpcc.bmsql_warehouse.csv`.

2. Generate the CSV file.

    {{< copyable "shell-regular" >}}

    ```shell
    ./runLoader.sh props.mysql
    ```

3. Use Lightning to load data.

    To load data using Lightning, see [TiDB Lightning Deployment](/tidb-lightning/deploy-tidb-lightning.md). The following steps introduce how to use TiDB Ansible to deploy Lightning and use Lightning to load data.

    1. Edit `inventory.ini`.

        It is recommended to manually specify the deployed IP address, the port, and the deployment directory to avoid anomalies caused by conflicts. For the disk space of `import_dir`, see [TiDB Lightning Deployment](/tidb-lightning/deploy-tidb-lightning.md). `data_source_dir` refers to the directory where the CSV files are stored as mentioned before.

        ```ini
        [importer_server]
        IS1 ansible_host=172.16.5.34 deploy_dir=/data2/is1 tikv_importer_port=13323 import_dir=/data2/import
        [lightning_server]
        LS1 ansible_host=172.16.5.34 deploy_dir=/data2/ls1 tidb_lightning_pprof_port=23323 data_source_dir=/home/user/csv
        ```

    2. Edit `conf/tidb-lightning.yml`.

        ```yaml
        mydumper:
            no-schema: true
            csv:
                separator: ','
                delimiter: ''
                header: false
                not-null: false
                'null': 'NULL'
                backslash-escape: true
                trim-last-separator: false
        ```

    3. Deploy Lightning and Importer.

        {{< copyable "shell-regular" >}}

        ```shell
        ansible-playbook deploy.yml --tags=lightning
        ```

    4. Start Lightning and Importer.

       * Log into the server where Lightning and Importer are deployed.
       * Enter the deployment directory.
       * Execute `scripts/start_importer.sh` under the Importer directory to start Importer.
       * Execute `scripts/start_lightning.sh` under the Lightning directory to begin to load data.

       Because you've used TiDB Ansible deployment method, you can see the loading progress of Lightning on the monitoring page, or check whether the loading process is completed through the log.

Fourth, after successfully loading data, you can run `sql.common/test.sql` to validate the correctness of the data. If all SQL statements return an empty result, then the data is correctly loaded.

## Run the test

Run the following BenchmarkSQL test script:

{{< copyable "shell-regular" >}}

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
