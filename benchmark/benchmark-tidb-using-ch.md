---
title: 如何对 TiDB 进行 CH-benCHmark 测试
summary: 本文介绍如何对 TiDB 进行 CH-benCHmark 测试。
---

# 如何对 TiDB 进行 CH-benCHmark 测试

本文介绍如何对 TiDB 进行 CH-benCHmark 测试。

CH-benCHmark 是包含 [TPC-C](http://www.tpc.org/tpcc/) 和 [TPC-H](http://www.tpc.org/tpch/) 的混合负载，也是用于测试 HTAP 系统的最常见负载。更多信息，请参考 [The mixed workload CH-benCHmark](https://research.tableau.com/sites/default/files/a8-cole.pdf)。

在进行 CH-benCHmark 测试前，你需要先部署 TiDB 的 HTAP 组件 [TiFlash](/tiflash/tiflash-overview.md)。部署 TiFlash 并[创建 TiFlash 副本](#创建-tiflash-副本)后，对于 TPC-C 联机交易数据，系统将实时同步最新的数据到 TiFlash 组件；TiDB 优化器会自动将 TPC-H 负载的 OLAP 查询下推到 TiFlash MPP 引擎进行高效执行。

本文使用 [go-tpc](https://github.com/pingcap/go-tpc) 作为 CH 测试实现，可以通过 [TiUP](/tiup/tiup-overview.md) 命令下载测试程序：

{{< copyable "shell-regular" >}}

```shell
tiup install bench
```

关于 TiUP Bench 组件的详细用法可参考 [TiUP Bench](/tiup/tiup-bench.md)。

## 导入数据

### 导入 TPC-C 数据

**导入数据通常是整个 TPC-C 测试中最耗时、也是最容易出问题的阶段。**

本文以 1000 WAREHOUSE 为例，在 shell 中运行以下 TiUP 命令进行数据导入和测试。注意你需要将本文中的 `172.16.5.140` 和 `4000` 替换为你实际的 TiDB host 和 port 值。

{{< copyable "shell-regular" >}}

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 prepare -T 32
```

基于不同的机器配置，数据导入过程可能会持续几个小时。如果是小型集群，可以使用较小的 WAREHOUSE 值进行测试。

数据导入完成后，可以通过命令 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 check` 验证数据正确性。

### 导入 TPC-H 所需额外的表和视图

在 shell 中运行 TiUP 命令：

{{< copyable "shell-regular" >}}

```shell
tiup bench ch -H 172.16.5.140 -P 4000 -D tpcc prepare
```

日志输出如下：

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

## 创建 TiFlash 副本

部署 TiFlash 后，TiFlash 并不会自动同步 TiKV 数据，你需要执行以下 SQL 语句创建整库的 TiFlash 副本。创建 TiFlash 副本后，系统自动实时同步最新数据到 TiFlash 组件。例如，当集群中部署了两个 TiFlash 节点时，如果将 replica 设置为 2，执行以下 SQL 语句将创建两个 TiFlash 副本。

```
ALTER DATABASE tpcc SET TIFLASH REPLICA 2;
```

可通过如下 SQL 语句确认所有表（通过 WHERE 语句可以指定需要确认的表，去掉 WHERE 语句则查看所有表）的 TiFlash 副本的状态是否完成同步：

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'tpcc';
```

查询结果中：

* AVAILABLE 字段表示该表的 TiFlash 副本是否可用。1 代表可用，0 代表不可用。副本状态为可用之后就不再改变，如果通过 DDL 命令修改副本数则会重新计算同步进度。
* PROGRESS 字段代表同步进度，在 0.0~1.0 之间，1.0 代表至少 1 个副本已经完成同步。

## 搜集统计信息

为了确保优化器能生成最优的执行计划，请执行以下 SQL 语句提前搜集统计信息：

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

## 运行测试

以 50 TP 并发，1 AP 并发为例，运行以下测试命令：

{{< copyable "shell-regular" >}}

```shell
go-tpc ch --host 172.16.5.140 -P4000 --warehouses 1000 run -D tpcc -T 50 -t 1 --time 1h
```

命令运行过程中，控制台上会持续打印测试结果。例如：

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

命令运行结束后，控制台会打印测试统计结果。例如：

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

测试完成之后，也可以运行 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 check`  验证数据正确性。