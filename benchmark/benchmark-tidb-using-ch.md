---
title: How to Run CH-benCHmark Test on TiDB
summary: Learn how to run CH-benCHmark test on TiDB.
---

# How to Run CH-benCHmark Test on TiDB

This document describes how to test TiDB using CH-benCHmark.

CH-benCHmark is a mixed workload containing both [TPC-C](http://www.tpc.org/tpcc/) and [TPC-H](http://www.tpc.org/tpch/) tests. It is the most common workload to test HTAP systems. For more information, see [The mixed workload CH-benCHmark](https://research.tableau.com/sites/default/files/a8-cole.pdf).

Before running the CH-benCHmark test, you need to deploy [TiFlash](/tiflash/tiflash-overview.md) first, which is a TiDB's HTAP component. After you deploy TiFlash and [create TiFlash replicas](#create-tiflash-replicas), TiKV will replicate the latest data of TPC-C online transactions to TiFlash in real time, and the TiDB optimizer will automatically push down OLAP queries from TPC-H workload to the MPP engine of TiFlash for efficient execution.

The CH-benCHmark test in this document is implemented based on [go-tpc](https://github.com/pingcap/go-tpc). You can download the test program using the following [TiUP](/tiup/tiup-overview.md) command:

{{< copyable "shell-regular" >}}

```shell
tiup install bench
```

For detailed usage of the TiUP Bench component, see [TiUP Bench](/tiup/tiup-bench.md).

## Load data

### Load TPC-C data

**Loading data is usually the most time-consuming and problematic stage of the entire TPC-C test.**

Taking 1000 warehouses as an example, you can execute the following TiUP command in shell for data load and test. Note that you need to replace `172.16.5.140` and `4000` in this document with your TiDB host and port values.

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 prepare -T 32
```

Depending on different machine configurations, this loading process might take a few hours. If the cluster size is small, you can use a smaller warehouse value for the test.

After the data is loaded, you can execute the `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 check` command to validate the data correctness.

### Load additional tables and views required for TPC-H

Run the following TiUP command in the shell:

{{< copyable "shell-regular" >}}

```shell
tiup bench ch -H 172.16.5.140 -P 4000 -D tpcc prepare
```

The following is the log output:

```
creating nation
creating region
creating supplier
generating nation table
generate nation table done
generating region table
generate region table done
generating suppliers table
generate suppliers table done
creating view revenue1
```

## Create TiFlash replicas

After TiFlash is deployed, TiFlash does not automatically replicate TiKV data. You need to execute the following SQL statement to create TiFlash replicas for the `tpcc` database. Once the specified TiFlash replicas are created, TiKV automatically replicates the latest data to TiFlash in real-time. In the following example, two TiFlash nodes are deployed in the cluster and the replica number is set to 2.

```
ALTER DATABASE tpcc SET tiflash replica 2;
```

To check whether the replication of all tables in the `tpcc` database is complete, execute the following statement, in which the `WHERE` clause is used to specify the databases and tables to be checked. If you want to check the replication status of all databases, remove the `WHERE` clause from the statement.

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'tpcc';
```

In the result of the above statement:

- `AVAILABLE` indicates whether the TiFlash replica of a specific table is available or not. `1` means available and `0` means unavailable. Once a replica becomes available, this status does not change anymore.
- `PROGRESS` means the progress of the replication. The value is between `0` and `1`. `1` means that the replication is complete for the TiFlash replica.

## Collect statistics

To ensure that the TiDB optimizer can generate the optimal execution plan, execute the following SQL statements to collect statistics in advance.

```
analyze table customer;
analyze table district;
analyze table history;
analyze table item;
analyze table new_order;
analyze table order_line;
analyze table orders;
analyze table stock;
analyze table warehouse;
analyze table nation;
analyze table region;
analyze table supplier;
```

## Run the test

Taking 50 TP concurrency and 1 AP concurrency as an example, execute the following command to run the test:

{{< copyable "shell-regular" >}}

```shell
tiup bench ch --host 172.16.5.140 -P4000 --warehouses 1000 run -D tpcc -T 50 -t 1 --time 1h
```

During the test, test results are continuously printed on the console. For example:

```text
[Current] NEW_ORDER - Takes(s): 10.0, Count: 13524, TPM: 81162.0, Sum(ms): 998317.6, Avg(ms): 73.9, 50th(ms): 71.3, 90th(ms): 100.7, 95th(ms): 113.2, 99th(ms): 159.4, 99.9th(ms): 209.7, Max(ms): 243.3
[Current] ORDER_STATUS - Takes(s): 10.0, Count: 1132, TPM: 6792.7, Sum(ms): 16196.6, Avg(ms): 14.3, 50th(ms): 13.1, 90th(ms): 24.1, 95th(ms): 27.3, 99th(ms): 37.7, 99.9th(ms): 50.3, Max(ms): 52.4
[Current] PAYMENT - Takes(s): 10.0, Count: 12977, TPM: 77861.1, Sum(ms): 773982.0, Avg(ms): 59.7, 50th(ms): 56.6, 90th(ms): 88.1, 95th(ms): 100.7, 99th(ms): 151.0, 99.9th(ms): 201.3, Max(ms): 243.3
[Current] STOCK_LEVEL - Takes(s): 10.0, Count: 1134, TPM: 6806.0, Sum(ms): 31220.9, Avg(ms): 27.5, 50th(ms): 25.2, 90th(ms): 37.7, 95th(ms): 44.0, 99th(ms): 71.3, 99.9th(ms): 117.4, Max(ms): 125.8
[Current] Q11    - Count: 1, Sum(ms): 3682.9, Avg(ms): 3683.6
[Current] DELIVERY - Takes(s): 10.0, Count: 1167, TPM: 7002.6, Sum(ms): 170712.9, Avg(ms): 146.3, 50th(ms): 142.6, 90th(ms): 192.9, 95th(ms): 209.7, 99th(ms): 251.7, 99.9th(ms): 335.5, Max(ms): 385.9
[Current] NEW_ORDER - Takes(s): 10.0, Count: 13238, TPM: 79429.5, Sum(ms): 1010795.3, Avg(ms): 76.4, 50th(ms): 75.5, 90th(ms): 104.9, 95th(ms): 117.4, 99th(ms): 159.4, 99.9th(ms): 234.9, Max(ms): 352.3
[Current] ORDER_STATUS - Takes(s): 10.0, Count: 1224, TPM: 7350.6, Sum(ms): 17874.1, Avg(ms): 14.6, 50th(ms): 13.6, 90th(ms): 23.1, 95th(ms): 27.3, 99th(ms): 37.7, 99.9th(ms): 54.5, Max(ms): 60.8
[Current] PAYMENT - Takes(s): 10.0, Count: 12650, TPM: 75901.1, Sum(ms): 761981.3, Avg(ms): 60.3, 50th(ms): 56.6, 90th(ms): 88.1, 95th(ms): 104.9, 99th(ms): 159.4, 99.9th(ms): 218.1, Max(ms): 318.8
[Current] STOCK_LEVEL - Takes(s): 10.0, Count: 1179, TPM: 7084.9, Sum(ms): 32829.8, Avg(ms): 27.9, 50th(ms): 26.2, 90th(ms): 37.7, 95th(ms): 44.0, 99th(ms): 71.3, 99.9th(ms): 100.7, Max(ms): 117.4
[Current] Q12    - Count: 1, Sum(ms): 9945.8, Avg(ms): 9944.7
[Current] Q13    - Count: 1, Sum(ms): 1729.6, Avg(ms): 1729.6
...
```

After the test is finished, the test summary results are printed. For example:

```text
Finished: 50 OLTP workers, 1 OLAP workers
[Summary] DELIVERY - Takes(s): 3599.7, Count: 501795, TPM: 8363.9, Sum(ms): 63905178.8, Avg(ms): 127.4, 50th(ms): 125.8, 90th(ms): 167.8, 95th(ms): 184.5, 99th(ms): 226.5, 99.9th(ms): 318.8, Max(ms): 604.0
[Summary] DELIVERY_ERR - Takes(s): 3599.7, Count: 14, TPM: 0.2, Sum(ms): 1027.7, Avg(ms): 73.4, 50th(ms): 71.3, 90th(ms): 109.1, 95th(ms): 109.1, 99th(ms): 113.2, 99.9th(ms): 113.2, Max(ms): 113.2
[Summary] NEW_ORDER - Takes(s): 3599.7, Count: 5629221, TPM: 93826.9, Sum(ms): 363758020.7, Avg(ms): 64.6, 50th(ms): 62.9, 90th(ms): 88.1, 95th(ms): 100.7, 99th(ms): 130.0, 99.9th(ms): 184.5, Max(ms): 570.4
[Summary] NEW_ORDER_ERR - Takes(s): 3599.7, Count: 20, TPM: 0.3, Sum(ms): 404.2, Avg(ms): 20.2, 50th(ms): 18.9, 90th(ms): 37.7, 95th(ms): 50.3, 99th(ms): 56.6, 99.9th(ms): 56.6, Max(ms): 56.6
[Summary] ORDER_STATUS - Takes(s): 3599.8, Count: 500318, TPM: 8339.0, Sum(ms): 7135956.6, Avg(ms): 14.3, 50th(ms): 13.1, 90th(ms): 24.1, 95th(ms): 27.3, 99th(ms): 37.7, 99.9th(ms): 50.3, Max(ms): 385.9
[Summary] PAYMENT - Takes(s): 3599.8, Count: 5380815, TPM: 89684.8, Sum(ms): 269863092.5, Avg(ms): 50.2, 50th(ms): 48.2, 90th(ms): 75.5, 95th(ms): 88.1, 99th(ms): 125.8, 99.9th(ms): 184.5, Max(ms): 1073.7
[Summary] PAYMENT_ERR - Takes(s): 3599.8, Count: 11, TPM: 0.2, Sum(ms): 313.0, Avg(ms): 28.5, 50th(ms): 10.0, 90th(ms): 67.1, 95th(ms): 67.1, 99th(ms): 88.1, 99.9th(ms): 88.1, Max(ms): 88.1
[Summary] STOCK_LEVEL - Takes(s): 3599.8, Count: 500467, TPM: 8341.5, Sum(ms): 13208726.4, Avg(ms): 26.4, 50th(ms): 25.2, 90th(ms): 37.7, 95th(ms): 44.0, 99th(ms): 62.9, 99.9th(ms): 96.5, Max(ms): 570.4
[Summary] STOCK_LEVEL_ERR - Takes(s): 3599.8, Count: 2, TPM: 0.0, Sum(ms): 7.6, Avg(ms): 3.7, 50th(ms): 3.1, 90th(ms): 4.7, 95th(ms): 4.7, 99th(ms): 4.7, 99.9th(ms): 4.7, Max(ms): 4.7
tpmC: 93826.9, efficiency: 729.6%
[Summary] Q1     - Count: 11, Sum(ms): 42738.2, Avg(ms): 3885.3
[Summary] Q10    - Count: 11, Sum(ms): 440370.3, Avg(ms): 40034.3
[Summary] Q11    - Count: 11, Sum(ms): 44208.6, Avg(ms): 4018.7
[Summary] Q12    - Count: 11, Sum(ms): 105320.3, Avg(ms): 9574.6
[Summary] Q13    - Count: 11, Sum(ms): 19199.5, Avg(ms): 1745.4
[Summary] Q14    - Count: 11, Sum(ms): 84582.1, Avg(ms): 7689.5
[Summary] Q15    - Count: 11, Sum(ms): 271944.8, Avg(ms): 24722.8
[Summary] Q16    - Count: 11, Sum(ms): 183894.9, Avg(ms): 16718.1
[Summary] Q17    - Count: 11, Sum(ms): 89018.9, Avg(ms): 8092.7
[Summary] Q18    - Count: 10, Sum(ms): 767814.5, Avg(ms): 76777.6
[Summary] Q19    - Count: 10, Sum(ms): 17099.1, Avg(ms): 1709.8
[Summary] Q2     - Count: 11, Sum(ms): 53513.6, Avg(ms): 4865.2
[Summary] Q20    - Count: 10, Sum(ms): 73717.7, Avg(ms): 7372.1
[Summary] Q21    - Count: 10, Sum(ms): 166001.4, Avg(ms): 16601.1
[Summary] Q22    - Count: 10, Sum(ms): 48268.4, Avg(ms): 4827.7
[Summary] Q3     - Count: 11, Sum(ms): 31110.1, Avg(ms): 2828.5
[Summary] Q4     - Count: 11, Sum(ms): 83814.2, Avg(ms): 7619.3
[Summary] Q5     - Count: 11, Sum(ms): 368301.0, Avg(ms): 33483.5
[Summary] Q6     - Count: 11, Sum(ms): 61702.5, Avg(ms): 5608.9
[Summary] Q7     - Count: 11, Sum(ms): 158928.2, Avg(ms): 14446.3
```

After the test is finished, you can execute the `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 check` command to validate the data correctness.