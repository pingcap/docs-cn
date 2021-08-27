---
title: HTAP 快速上手指南
summary: 本文介绍如何快速上手体验 TiDB 的 HTAP 功能。 
---

# HTAP 快速上手指南

本指南介绍如何快速上手体验 TiDB 的一站式混合型在线事务与在线分析处理 (Hybrid Transactional and Analytical Processing, HTAP) 功能。

> **注意：**
>
> 本指南中的步骤仅适用于快速上手体验，不适用于生产环境。如需探索 HTAP 更多功能，请参考[深入探索 HTAP](/explore-htap.md)。

## 基础概念

在试用前，你需要对 TiDB 面向在线事务处理的行存储引擎 [TiKV](/tikv-overview.md) 与面向实时分析场景的列存储引擎 [TiFlash](/tiflash/tiflash-overview.md) 有一些基本了解：

- HTAP 存储引擎：行存 (Row-store) 与列存 (columnar-store) 同时存在，自动同步，保持强一致性。行存为在线事务处理 OLTP 提供优化，列存则为在线分析处理 OLAP 提供性能优化。
- HTAP 数据一致性：作为一个分布式事务型的键值数据库，TiKV 提供了满足 ACID 约束的分布式事务接口，并通过 [Raft](https://raft.github.io/raft.pdf) 协议保证了多副本数据一致性以及高可用。TiFlash 通过 Multi-Raft Learner 协议实时从 TiKV 复制数据，确保与 TiKV 之间的数据强一致。
- HTAP 数据隔离性：TiKV、TiFlash 可按需部署在不同的机器，解决 HTAP 资源隔离的问题。
- MPP 计算引擎：从 v5.0 版本起，TiFlash 引入了分布式计算框架 [MPP](/tiflash/use-tiflash.md#使用-mpp-模式)，允许节点之间的数据交换并提供高性能、高吞吐的 SQL 算法，可以大幅度缩短分析查询的执行时间。

## 体验步骤

本文的步骤以业界比较流行的 [TPC-H](http://www.tpc.org/tpch/) 数据集为例，通过其中一个查询场景来体验 TiDB HTAP 的便捷性和高性能。

### 第 1 步：部署试用环境

在试用 TiDB HTAP 功能前，请按照 [TiDB 数据库快速上手指南](/quick-start-with-tidb.md)中的步骤准备 TiDB 本地测试环境，执行以下命令启动 TiDB 集群：

{{< copyable "shell-regular" >}}

```shell
tiup playground
```

> **注意：**
>
> `tiup playground` 命令仅适用于快速上手体验，不适用于生产环境。

### 第 2 步：准备试用数据

通过以下步骤，将生成一个 [TPC-H](http://www.tpc.org/tpch/) 数据集用于体验 TiDB HTAP 功能。如果你对 TPC-H 感兴趣，可查看其[规格说明](http://tpc.org/tpc_documents_current_versions/pdf/tpc-h_v3.0.0.pdf)。

> **注意：**
>
> 如果你想使用自己现有的数据进行分析查询，可以将[数据迁移到 TiDB](/migration-overview.md) 中；如果你想自己设计并生成数据，可以通过 SQL 语句或相关工具生成。

1. 使用以下命令安装数据生成工具：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install bench
    ```

2. 使用以下命令生成数据：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup bench tpch --sf=1 prepare
    ```

    当命令行输出 `Finished` 时，表示数据生成完毕。

3. 运行以下 SQL 语句查看生成的数据：

    {{< copyable "sql" >}}

    ```sql
    SELECT CONCAT(table_schema,'.',table_name) AS 'Table Name', table_rows AS 'Number of Rows', CONCAT(ROUND(data_length/(1024*1024*1024),4),'G') AS 'Data Size', CONCAT(ROUND(index_length/(1024*1024*1024),4),'G') AS 'Index Size', CONCAT(ROUND((data_length+index_length)/(1024*1024*1024),4),'G') AS'Total'FROM information_schema.TABLES WHERE table_schema LIKE 'test';
    ```

    从输出中可以看到，一共生成了八张表，最大的一张表数据量有 600 万行（由于数据是工具随机生成，所以实际的数据生成量以 SQL 实际查询到的值为准）。

    ```sql
    +---------------+----------------+-----------+------------+---------+
    | Table Name    | Number of Rows | Data Size | Index Size | Total   |
    +---------------+----------------+-----------+------------+---------+
    | test.nation   |             25 | 0.0000G   | 0.0000G    | 0.0000G |
    | test.region   |              5 | 0.0000G   | 0.0000G    | 0.0000G |
    | test.part     |         200000 | 0.0245G   | 0.0000G    | 0.0245G |
    | test.supplier |          10000 | 0.0014G   | 0.0000G    | 0.0014G |
    | test.partsupp |         800000 | 0.1174G   | 0.0119G    | 0.1293G |
    | test.customer |         150000 | 0.0242G   | 0.0000G    | 0.0242G |
    | test.orders   |        1514336 | 0.1673G   | 0.0000G    | 0.1673G |
    | test.lineitem |        6001215 | 0.7756G   | 0.0894G    | 0.8651G |
    +---------------+----------------+-----------+------------+---------+
    8 rows in set (0.06 sec)
     ```

    这是一个商业订购系统的数据库。其中，`test.nation` 表是国家信息、`test.region` 表是地区信息、`test.part` 表是零件信息、`test.supplier` 表是供货商信息、`test.partsupp` 表是供货商的零件信息、`test.customer` 表是消费者信息、`test.orders` 表是订单信息、`test.lineitem` 表是在线商品的信息。

### 第 3 步：使用行存查询数据

执行以下 SQL 语句，你可以体验当只使用行存（大多数数据库）时 TiDB 的表现：

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

这是一个运送优先权查询，用于给出在指定日期之前尚未运送的订单中收入最高订单的优先权和潜在的收入。潜在的收入被定义为 `l_extendedprice * (1-l_discount)` 的和。订单按照收入的降序列出。在本示例中，此查询将列出潜在查询收入在前 10 的尚未运送的订单。

### 第 4 步：同步列存数据

TiFlash 部署完成后并不会自动同步 TiKV 数据，你可以在 MySQL 客户端向 TiDB 发送以下 DDL 命令指定需要同步到 TiFlash 的表。指定后，TiDB 将创建对应的 TiFlash 副本。

{{< copyable "sql" >}}

```sql
ALTER TABLE test.customer SET TIFLASH REPLICA 1;
ALTER TABLE test.orders SET TIFLASH REPLICA 1;
ALTER TABLE test.lineitem SET TIFLASH REPLICA 1;
```

如需查询 TiFlash 表的同步状态，请使用以下 SQL 语句：

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'customer';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'orders';
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = 'test' and TABLE_NAME = 'lineitem';
```

以上查询结果中：

- `AVAILABLE` 字段表示该表的 TiFlash 副本是否可用。1 代表可用，0 代表不可用。副本状态变为可用之后就不再改变，如果通过 DDL 命令修改副本数则会重新计算同步进度。
- `PROGRESS` 字段代表同步进度，在 0.0~1.0 之间，1 代表至少 1 个副本已经完成同步。

### 第 5 步：使用 HTAP 更快地分析数据

再次执行[第 3 步](#第-3-步使用行存查询数据)中的 SQL 语句，你可以感受 TiDB HTAP 的表现。

对于创建了 TiFlash 副本的表，TiDB 优化器会自动根据代价估算选择是否使用 TiFlash 副本。如需查看实际是否选择了 TiFlash 副本，可以使用 `desc` 或 `explain analyze` 语句，例如：

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

如果结果中出现 ExchangeSender 和 ExchangeReceiver 算子，表明 MPP 已生效。

此外，你也可以指定整个查询的各个计算部分都只使用 TiFlash 引擎，详情请参阅[使用 TiDB 读取 TiFlash](/tiflash/use-tiflash.md#使用-tidb-读取-tiflash)。

你可以对比两次的查询结果和查询性能。

## 探索更多

- [TiDB HTAP 形态架构](/tiflash/tiflash-overview.md#整体架构)
- [深入探索 HTAP](/explore-htap.md)
- [使用 TiFlash](/tiflash/use-tiflash.md)  
