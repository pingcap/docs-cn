---
title: 如何对 TiDB 进行 TPC-C 测试
aliases: ['/docs-cn/dev/benchmark/benchmark-tidb-using-tpcc/','/docs-cn/dev/benchmark/how-to-run-tpcc/']
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

对于 1000 WAREHOUSE，在 3 台服务器上部署集群。

在 3 台服务器的条件下，建议每台机器部署 1 个 TiDB，1 个 PD 和 1 个 TiKV 实例。

比如这里采用的机器硬件配置是：

| 类别 | 名称 |
| :-: | :-: |
| OS | Linux (CentOS 7.3.1611) |
| CPU | 40 vCPUs, Intel(R) Xeon(R) CPU E5-2630 v4 @ 2.20GHz |
| RAM | 128GB |
| DISK | Optane 500GB SSD |

因为该型号 CPU 是 NUMA 架构，建议用 `numactl` 进行绑核。

1. [安装 numactl 工具](/check-before-deployment.md#安装-numactl-工具) 。

2. 用 `lscpu` 查看 NUMA node，比如：

    ```text
    NUMA node0 CPU(s):     0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38
    NUMA node1 CPU(s):     1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35,37,39
    ```

3. 通过修改 `{tidb_deploy_path}/scripts/run_tidb.sh` 启动脚本，加入 `numactl` 来启动 TiDB：

    ```text
    #!/bin/bash
    set -e

    ulimit -n 1000000

    # WARNING: This file was auto-generated. Do not edit!
    #          All your edit might be overwritten!
    DEPLOY_DIR=/home/damon/deploy/tidb1-1

    cd "${DEPLOY_DIR}" || exit 1

    export TZ=Asia/Shanghai

    # 同一台机器不同的 TiDB 实例需要指定不同的 cpunodebind 以及 membind；来绑定不同的 Numa node
    exec numactl --cpunodebind=0  --membind=0 bin/tidb-server \
        -P 4111 \
        --status="10191" \
        --advertise-address="172.16.4.53" \
        --path="172.16.4.10:2490" \
        --config=conf/tidb.toml \
        --log-slow-query="/home/damon/deploy/tidb1-1/log/tidb_slow_query.log" \
        --log-file="/home/damon/deploy/tidb1-1/log/tidb.log" 2>> "/home/damon/deploy/tidb1-1/log/tidb_stderr.log"
    ```

    > **注意：**
    >
    > 直接修改 `run_tidb.sh` 可能会被覆盖，因此在生产环境中，如有绑核需求，建议使用 TiUP 绑核。

4. 选择部署一个 HAproxy 来进行多个 TiDB node 的负载均衡，推荐配置 nbproc 为 CPU 核数。

## 配置调整

### TiDB 配置

```toml
[log]
level = "error"

[performance]
# 根据 NUMA 配置，设置单个 TiDB 最大使用的 CPU 核数
max-procs = 20

[prepared-plan-cache]
# 开启 TiDB 配置中的 prepared plan cache，以减少优化执行计划的开销
enabled = true
```

### TiKV 配置

开始可以使用基本的配置，压测运行后可以通过观察 Grafana 并参考 [TiKV 线程池调优说明](/tune-tikv-thread-performance.md)进行调整。

### BenchmarkSQL 配置

修改 `benchmarksql/run/props.mysql`：

```text
conn=jdbc:mysql://{HAPROXY-HOST}:{HAPROXY-PORT}/tpcc?useSSL=false&useServerPrepStmts=true&useConfigs=maxPerformance
warehouses=1000 # 使用 1000 个 warehouse
terminals=500   # 使用 500 个终端
loadWorkers=32  # 导入数据的并发数
```

## 导入数据

**导入数据通常是整个 TPC-C 测试中最耗时，也是最容易出问题的阶段。**

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

### 直接使用 BenchmarkSQL 导入

运行导入数据脚本：

{{< copyable "shell-regular" >}}

```shell
./runLoader.sh props.mysql
```

根据机器配置这个过程可能会持续几个小时。

### 通过 TiDB Lightning 导入

由于导入数据量随着 warehouse 的增加而增加，当需要导入 1000 warehouse 以上数据时，可以先用 BenchmarkSQL 生成 csv 文件，再将文件通过 TiDB Lightning（以下简称 Lightning）导入的方式来快速导入。生成的 csv 文件也可以多次复用，节省每次生成所需要的时间。

#### 修改 BenchmarkSQL 的配置文件

1 warehouse 的 csv 文件需要 77 MB 磁盘空间，在生成之前要根据需要分配足够的磁盘空间来保存 csv 文件。可以在 `benchmarksql/run/props.mysql` 文件中增加一行：

```text
fileLocation=/home/user/csv/  # 存储 csv 文件的目录绝对路径，需保证有足够的空间
```

因为最终要使用 Lightning 导入数据，所以 csv 文件名最好符合 Lightning 要求，即 `{database}.{table}.csv` 的命名法。这里可以将以上配置改为：

```text
fileLocation=/home/user/csv/tpcc.  # 存储 csv 文件的目录绝对路径 + 文件名前缀（database）
```

这样生成的 csv 文件名将会是类似 `tpcc.bmsql_warehouse.csv` 的样式，符合 Lightning 的要求。

#### 生成 csv 文件

{{< copyable "shell-regular" >}}

```shell
./runLoader.sh props.mysql
```

#### 通过 Lightning 导入

通过 Lightning 导入数据请参考 [Lightning 部署执行](/tidb-lightning/deploy-tidb-lightning.md)章节。这里我们介绍下通过 TiDB Ansible 部署 Lightning 导入数据的方法。

##### 修改 inventory.ini

这里最好手动指定清楚部署的 IP、端口、目录，避免各种冲突问题带来的异常，其中 import_dir 的磁盘空间参考 [Lightning 部署执行](/tidb-lightning/deploy-tidb-lightning.md)，data_source_dir 就是存储上一节 csv 数据的目录。

```ini
[importer_server]
IS1 ansible_host=172.16.5.34 deploy_dir=/data2/is1 tikv_importer_port=13323 import_dir=/data2/import

[lightning_server]
LS1 ansible_host=172.16.5.34 deploy_dir=/data2/ls1 tidb_lightning_pprof_port=23323 data_source_dir=/home/user/csv
```

##### 修改 conf/tidb-lightning.yml

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

##### 部署 Lightning 和 Importer

{{< copyable "shell-regular" >}}

```shell
ansible-playbook deploy.yml --tags=lightning
```

##### 启动

* 登录到部署 Lightning 和 Importer 的服务器
* 进入部署目录
* 在 Importer 目录下执行 `scripts/start_importer.sh`，启动 Importer
* 在 Lightning 目录下执行 `scripts/start_lightning.sh`，开始导入数据

由于是用 TiDB Ansible 进行部署的，可以在监控页面看到 Lightning 的导入进度，或者通过日志查看导入是否结束。

### 导入完成后

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
