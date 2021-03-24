---
title: 如何对 TiDB 进行 TPC-C 测试
---

# 如何对 TiDB 进行 TPC-C 测试

本文介绍如何对 TiDB 进行 [TPC-C](http://www.tpc.org/tpcc/) 测试。

TPC-C 是一个对 OLTP（联机交易处理）系统进行测试的规范，使用一个商品销售模型对 OLTP 系统进行测试，其中包含五类事务：

* NewOrder – 新订单的生成
* Payment – 订单付款
* OrderStatus – 最近订单查询
* Delivery – 配送
* StockLevel – 库存缺货状态分析

在测试开始前，TPC-C Benchmark 规定了数据库的初始状态，也就是数据库中数据生成的规则，其中 ITEM 表中固定包含 10 万种商品，仓库的数量可进行调整，假设 WAREHOUSE 表中有 W 条记录，那么：

* STOCK 表中应有 W \* 10 万条记录（每个仓库对应 10 万种商品的库存数据）
* DISTRICT 表中应有 W \* 10 条记录（每个仓库为 10 个地区提供服务）
* CUSTOMER 表中应有 W \* 10 \* 3000 条记录（每个地区有 3000 个客户）
* HISTORY 表中应有 W \* 10 \* 3000 条记录（每个客户一条交易历史）
* ORDER 表中应有 W \* 10 \* 3000 条记录（每个地区 3000 个订单），并且最后生成的 900 个订单被添加到 NEW-ORDER 表中，每个订单随机生成 5 ~ 15 条 ORDER-LINE 记录。

我们将以 1000 WAREHOUSE 为例进行测试。

TPC-C 使用 tpmC 值（Transactions per Minute）来衡量系统最大有效吞吐量 (MQTh, Max Qualified Throughput)，其中 Transactions 以 NewOrder Transaction 为准，即最终衡量单位为每分钟处理的新订单数。

本文使用 [go-tpc](https://github.com/pingcap/go-tpc) 作为 TPC-C 测试实现，可以通过 [TiUP](/tiup/tiup-overview.md) 命令下载测试程序:

{{< copyable "shell-regular" >}}

```shell
tiup install bench
```

关于 TiUP Bench 组件的详细用法可参考 [TiUP Bench](/tiup/tiup-bench.md)。

## 导入数据

**导入数据通常是整个 TPC-C 测试中最耗时，也是最容易出问题的阶段。**

在 shell 中运行 TiUP 命令：

{{< copyable "shell-regular" >}}

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 prepare
```

基于不同的机器配置，这个过程可能会持续几个小时。如果是小型集群，可以使用较小的 WAREHOUSE 值进行测试。

数据导入完成后，可以通过命令 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 check` 验证数据正确性。

## 运行测试

运行测试的命令是：

{{< copyable "shell-regular" >}}

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 1000 run
```

运行过程中控制台上会持续打印测试结果：

```text
[Current] NEW_ORDER - Takes(s): 4.6, Count: 5, TPM: 65.5, Sum(ms): 4604, Avg(ms): 920, 90th(ms): 1500, 99th(ms): 1500, 99.9th(ms): 1500
[Current] ORDER_STATUS - Takes(s): 1.4, Count: 1, TPM: 42.2, Sum(ms): 256, Avg(ms): 256, 90th(ms): 256, 99th(ms): 256, 99.9th(ms): 256
[Current] PAYMENT - Takes(s): 6.9, Count: 5, TPM: 43.7, Sum(ms): 2208, Avg(ms): 441, 90th(ms): 512, 99th(ms): 512, 99.9th(ms): 512
[Current] STOCK_LEVEL - Takes(s): 4.4, Count: 1, TPM: 13.8, Sum(ms): 224, Avg(ms): 224, 90th(ms): 256, 99th(ms): 256, 99.9th(ms): 256
...
```

运行结束后，会打印测试统计结果：

```text
[Summary] DELIVERY - Takes(s): 455.2, Count: 32, TPM: 4.2, Sum(ms): 44376, Avg(ms): 1386, 90th(ms): 2000, 99th(ms): 4000, 99.9th(ms): 4000
[Summary] DELIVERY_ERR - Takes(s): 455.2, Count: 1, TPM: 0.1, Sum(ms): 953, Avg(ms): 953, 90th(ms): 1000, 99th(ms): 1000, 99.9th(ms): 1000
[Summary] NEW_ORDER - Takes(s): 487.8, Count: 314, TPM: 38.6, Sum(ms): 282377, Avg(ms): 899, 90th(ms): 1500, 99th(ms): 1500, 99.9th(ms): 1500
[Summary] ORDER_STATUS - Takes(s): 484.6, Count: 29, TPM: 3.6, Sum(ms): 8423, Avg(ms): 290, 90th(ms): 512, 99th(ms): 1500, 99.9th(ms): 1500
[Summary] PAYMENT - Takes(s): 490.1, Count: 321, TPM: 39.3, Sum(ms): 144708, Avg(ms): 450, 90th(ms): 512, 99th(ms): 1000, 99.9th(ms): 1500
[Summary] STOCK_LEVEL - Takes(s): 487.6, Count: 41, TPM: 5.0, Sum(ms): 9318, Avg(ms): 227, 90th(ms): 512, 99th(ms): 1000, 99.9th(ms): 1000
```

测试完成之后，也可以运行 `tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 check` 进行数据正确性验证。

## 清理测试数据

{{< copyable "shell-regular" >}}

```shell
tiup bench tpcc -H 172.16.5.140 -P 4000 -D tpcc --warehouses 4 cleanup
```
