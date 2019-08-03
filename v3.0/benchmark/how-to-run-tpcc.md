---
title: 如何对 TiDB 进行 TPC-C 测试
category: benchmark
---

# 如何对 TiDB 进行 TPC-C 测试

本文介绍如何对 TiDB 进行 [TPC-C](http://www.tpc.org/tpcc/) 测试。

## 准备测试程序

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

本文使用开源的 BenchmarkSQL 5.0 作为 TPC-C 测试实现并添加了对 MySQL 协议的支持，可以通过以下命令下载测试程序:

{{< copyable "shell-regular" >}}

```shell
git clone -b 5.0-mysql-support-opt-2.1 https://github.com/pingcap/benchmarksql.git
```

安装 java 和 ant，以 CentOS 为例，可以执行以下命令进行安装

{{< copyable "shell-regular" >}}

```shell
sudo yum install -y java ant
```

进入 benchmarksql 目录并执行 ant 构建

{{< copyable "shell-regular" >}}

```shell
cd benchmarksql
ant
```

## 部署 TiDB 集群

对于 1000 WAREHOUSE 我们将在 3 台服务器上部署集群。

在 3 台服务器的条件下，建议每台机器部署 1 个 TiDB，1 个 PD 和 1 个 TiKV 实例。

比如这里采用的机器硬件配置是：

| 类别 | 名称 |
| :-: | :-: |
| OS | Linux (CentOS 7.3.1611) |
| CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| RAM | 128GB |
| DISK | Optane 500GB SSD |

因为该型号 CPU 是 NUMA 架构，建议先用 `taskset` 进行绑核，首先用 `lscpu` 查看 NUMA node，比如：

```text
NUMA node0 CPU(s):     0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38
NUMA node1 CPU(s):     1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39
```

之后可以通过下面的命令来启动 TiDB：

{{< copyable "shell-regular" >}}

```shell
nohup taskset -c 0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38 bin/tidb-server && \
nohup taskset -c 1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39 bin/tidb-server
```

最后，可以选择部署一个 HAproxy 来进行多个 TiDB node 的负载均衡，推荐配置 nbproc 为 CPU 核数。

## 配置调整

### TiDB 配置

```toml
[log]
level = "error"

[performance]
# 根据 NUMA 配置，设置单个 TiDB 最大使用的 CPU 核数
max-procs = 20

[prepared_plan_cache]
# 开启 TiDB 配置中的 prepared plan cache，以减少优化执行计划的开销
enabled = true
```

### TiKV 配置

开始可以使用基本的配置，压测运行后可以通过观察 Grafana 并参考 [TiKV 调优说明](../reference/performance/tune-tikv.md)进行调整。

### BenchmarkSQL 配置

修改 `benchmarksql/run/props.mysql`：

```text
conn=jdbc:mysql://{HAPROXY-HOST}:{HAPROXY-PORT}/tpcc?useSSL=false&useServerPrepStmts=true&useConfigs=maxPerformance
warehouses=1000 # 使用 1000 个 warehouse
terminals=500   # 使用 500 个终端
loadWorkers=32  # 导入数据的并发数
```

## 导入数据

首先用 MySQL 客户端连接到 TiDB-Server 并执行：

{{< copyable "sql" >}}

```sql
create database tpcc
```

之后在 shell 中运行 BenchmarkSQL 建表脚本：

{{< copyable "shell-regular" >}}

```shell
cd run && \
./runSQL.sh props.mysql sql.mysql/tableCreates.sql && \
./runSQL.sh props.mysql sql.mysql/indexCreates.sql
```

运行导入数据脚本：

{{< copyable "shell-regular" >}}

```shell
./runLoader.sh props.mysql
```

根据机器配置这个过程可能会持续几个小时。

数据导入完成之后，可以运行 `sql.common/test.sql` 进行数据正确性验证，如果所有 SQL 语句都返回结果为空，即为数据导入正确。

## 运行测试

执行 BenchmarkSQL 测试脚本：

{{< copyable "shell-regular" >}}

```shell
nohup ./runBenchmark.sh props.mysql &> test.log &
```

运行结束后通过 `test.log` 查看结果：

```text
07:09:53,455 [Thread-351] INFO   jTPCC : Term-00, Measured tpmC (NewOrders) = 77373.25
07:09:53,455 [Thread-351] INFO   jTPCC : Term-00, Measured tpmTOTAL = 171959.88
07:09:53,455 [Thread-351] INFO   jTPCC : Term-00, Session Start     = 2019-03-21 07:07:52
07:09:53,456 [Thread-351] INFO   jTPCC : Term-00, Session End       = 2019-03-21 07:09:53
07:09:53,456 [Thread-351] INFO   jTPCC : Term-00, Transaction Count = 345240
```

tpmC 部分即为测试结果。

测试完成之后，也可以运行 `sql.common/test.sql` 进行数据正确性验证，如果所有 SQL 语句的返回结果都为空，即为数据测试过程正确。
