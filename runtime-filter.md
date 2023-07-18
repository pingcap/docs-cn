---
title: Runtime Filter
summary: 介绍 Runtime Filter 的原理及使用方式
---

# Runtime Filter  

Runtime Filter 是 TiDB v7.3 引入的新功能，旨在提升 MPP 场景下 Hash Join 的性能。通过动态生成 Filter 来提前过滤 Hash Join 的数据从而减少运行时的扫描量以及 Hash Join 的计算量，最终达到提升查询性能的效果。

## 名词解释

1. Hash Join：一种实现 Join 关系代数的方式。通过一侧构建 Hash Table 来，另一侧不断 match Hash Table 来得到 Join 的结果。
2. Build Side：Hash Join 中构建 Hash Table 的一侧称之为 Build Side。*文中默认以 Join 的右表作为 Build Side*
3. Probe Side：Hash Join 中不断 match Hash Table 的一侧称之为 Probe Side。*文中默认以 Join 的左表作为 Probe Side*
4. Filter: 文中也用谓词指代，指代过滤条件。

## 优化思路

  Hash Join 通过将右表的数据构建 Hash Table，左表的数据不断 probe Hash Table 来完成 Join。Probe 过程一部分 Join Key 值中无法命中 Hash Table，则说明中的这部分数据在右表中不存在，也不会出现在最后 Join 的结果中。

  如果在扫描时能够**提前过滤掉这部分 Join Key** 的数据，将会减少扫描时间和网络开销，**从而大幅提升 Join 效率**。

## 原理

  Runtime Filter 是一种在查询规划时生成的**动态取值的谓词。**这个谓词和 TiDB Selection 中的其他谓词的作用是一样的，都是应用在 Table Scan 上，用来过滤不满足谓词条件的行。唯一不同的就是，Runtime Filter 这个谓词的参数取值是在 Hash Join 中构建的。

  ### 例子

  当前存在 ```store_sales``` 表与 ```date_dim``` 表的 Join 查询，它的 Join 方式为 Hash Join， ```store_sales``` 是一张事实表，主要存储门店销售数据，行数为 100万。T2 是一张时间维度表，主要存储时间信息。  当前查询想查询 2001 年的销售数据，则时间维度表的参与 Join 的数据量为 365 行。

```sql
SELECT * FROM store_sales, date_dim
WHERE ss_date_sk = d_date_sk
      AND d_year = 2001
```

  Hash Join 通常情况下的执行方式为：

```
                 +-------------------+
                 | PhysicalHashJoin  |
        +------->|                   |<------+
        |        +-------------------+       |
        |                                    |
        |                                    |
  100w  |                                    | 365
        |                                    |
        |                                    |
+-------+-------+                   +--------+-------+
| TableFullScan |                   | TableFullScan  |
|  store_sales  |                   |    date_dim    |
+---------------+                   +----------------+
```

*（上图为示意图，省略了 exchange 等节点）*

  RF 的执行方式是，先扫描 ```date_dim``` 的数据，PhysicalHashJoin 根据 ```date_dim``` 的数据计算出一个过滤条件，比如 ```date_dim in (2001/01/01~2001/12/31)```。接着将这个过滤条件发给等待扫描 ```store_sales``` 的 TableFullScan。```store_sales``` 再应用这个过滤条件，将过滤后的数据交给 PhysicalHashJoin，从而减少 Probe Side 的扫表数据量以及 Hash Table match 的计算量。

```
                         2. build RF values
            +-------->+-------------------+
            |         |PhysicalHashJoin   |<-----+
            |    +----+                   |      |
4.after RF  |    |    +-------------------+      | 1. scan T2
    5000    |    |3. send RF                     |      365
            |    | filter data                   |
            |    |                               |
      +-----+----v------+                +-------+--------+
      |  TableFullScan  |                | TabelFullScan  |
      |  store_sales    |                |    date_dim    |
      +-----------------+                +----------------+
```

  从两个图中对比可知。```store_sales``` 的扫描量从 100W -> 5000。减少 Table Full Scan 扫描的数据量，进而减少 probe Hash Table的次数，避免不必要的 I/O 和网络传输。Runtime Filter 就是通过这种方式来大大提升 Join 的效率的。

## 使用方法

这里以 TPC-DS 的数据集为例。主要用到表 catalog_sales 和表 date_dim 二者进行 Join。

#### Step1: 创建带 TiFlash Replica 的表

给表 ```catalog_sales``` 和 ```date_dim``` 各增加一个 TiFlash 的副本。

```sql
alter table catalog_sales set tiflash replica 1;
alter table date_dim set tiflash replica 1;
```

等待一段时间，并检查两个表的 TiFlash 副本已经 Ready。

```sql
mysql> select * from INFORMATION_SCHEMA.TIFLASH_REPLICA where TABLE_NAME='catalog_sales';
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME    | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | catalog_sales |     1055 |             1 |                 |         1 |        1 |
+--------------+---------------+----------+---------------+-----------------+-----------+----------+
mysql> select * from INFORMATION_SCHEMA.TIFLASH_REPLICA where TABLE_NAME='date_dim';
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| tpcds50      | date_dim   |     1015 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
```

#### Step2: 开启 Runtime Filter

将 ```tidb_runtime_filter_mode``` 设置为 LOCAL，即开启 Runtime Filter。

```sql
set tidb_runtime_filter_mode="LOCAL";
```

查看是否更改成功

```sql
show variables like "tidb_runtime_filter_mode";
+--------------------------+-------+
| Variable_name            | Value |
+--------------------------+-------+
| tidb_runtime_filter_mode | LOCAL |
+--------------------------+-------+
```

显示 LOCAL 则成功开启 Runtime Filter。

#### Step3: 查询

在准备查询之前，先查看一下查询规划。

```sql
explain select cs_ship_date_sk from catalog_sales, date_dim 
where d_date = '2002-2-01' and 
     cs_ship_date_sk = d_date_sk;
```

在开启 Runtime Filter 的情况下，可以看到，HashJoin 节点和 TableScan 节点上分别挂在了对应的 Runtime Filter，说明 Runtime Filter 规划成功。

```
TableFullScan: runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk   

HashJoin: runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
```

完整的查询规划如下：

```
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| id                                     | estRows     | task         | access object       | operator info                                                                                                                                 |
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
| TableReader_53                         | 37343.19    | root         |                     | MppVersion: 1, data:ExchangeSender_52                                                                                                         |
| └─ExchangeSender_52                    | 37343.19    | mpp[tiflash] |                     | ExchangeType: PassThrough                                                                                                                     |
|   └─Projection_51                      | 37343.19    | mpp[tiflash] |                     | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         |
|     └─HashJoin_48                      | 37343.19    | mpp[tiflash] |                     | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk |
|       ├─ExchangeReceiver_29(Build)     | 1.00        | mpp[tiflash] |                     |                                                                                                                                               |
|       │ └─ExchangeSender_28            | 1.00        | mpp[tiflash] |                     | ExchangeType: Broadcast, Compression: FAST                                                                                                    |
|       │   └─TableFullScan_26           | 1.00        | mpp[tiflash] | table:date_dim      | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  |
|       └─Selection_31(Probe)            | 71638034.00 | mpp[tiflash] |                     | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            |
|         └─TableFullScan_30             | 71997669.00 | mpp[tiflash] | table:catalog_sales | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     |
+----------------------------------------+-------------+--------------+---------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+
9 rows in set (0.01 sec)
```

查询，即可应用 Runtime Filter。

```sql
select cs_ship_date_sk from catalog_sales, date_dim 
where d_date = '2002-2-01' and 
     cs_ship_date_sk = d_date_sk;
```

#### Step4: 性能对比

以 TPCDS 的 50G 数据量为例，查询速度提升 50%，从 0.38s 提升至 0.17s。通过 analyze 语句可以看到具体的 Runtime Filter 生效后的各个算子的执行时间。

下面为不开启 Runtime Filter 的查询 Summary：

```
mysql> explain analyze select cs_ship_date_sk from catalog_sales, date_dim  where d_date = '2002-2-01' and       cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows  | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                    | operator info                                                                                | memory  | disk |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574    | root         |                     | time:379.7ms, loops:83, RU:0.000000, cop_task: {num: 48, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                          | MppVersion: 1, data:ExchangeSender_52                                                        | 12.0 KB | N/A  |
| └─ExchangeSender_52                | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | ExchangeType: PassThrough                                                                    | N/A     | N/A  |
|   └─Projection_51                  | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | tpcds50.catalog_sales.cs_ship_date_sk                                                        | N/A     | N/A  |
|     └─HashJoin_48                  | 37343.19    | 59574    | mpp[tiflash] |                     | tiflash_task:{proc max:377ms, min:375.3ms, avg: 376.1ms, p80:377ms, p95:377ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)]    | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build) | 1.00        | 2        | mpp[tiflash] |                     | tiflash_task:{proc max:291.3ms, min:290ms, avg: 290.6ms, p80:291.3ms, p95:291.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  |                                                                                              | N/A     | N/A  |
|       │ └─ExchangeSender_28      | 1.00        | 1        | mpp[tiflash] |                     | tiflash_task:{proc max:290.9ms, min:0s, avg: 145.4ms, p80:290.9ms, p95:290.9ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                      | ExchangeType: Broadcast, Compression: FAST                                                   | N/A     | N/A  |
|       │   └─TableFullScan_26     | 1.00        | 1        | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.88ms, min:0s, avg: 1.94ms, p80:3.88ms, p95:3.88ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                  | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false | N/A     | N/A  |
|       └─Selection_31(Probe)        | 71638034.00 | 71638034 | mpp[tiflash] |                     | tiflash_task:{proc max:47ms, min:34.3ms, avg: 40.6ms, p80:47ms, p95:47ms, iters:1160, tasks:2, threads:16}                                                                                                                                                                                                                                                                                        | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                           | N/A     | N/A  |
|         └─TableFullScan_30         | 71997669.00 | 71997669 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:34ms, min:17.3ms, avg: 25.6ms, p80:34ms, p95:34ms, iters:1160, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:8893, total_skipped_packs:4007, total_scanned_rows:72056474, total_skipped_rows:32476901, total_rs_index_load_time: 8ms, total_read_time: 579ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false                                                   | N/A     | N/A  |
+----------------------------------------+-------------+----------+--------------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+----------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.38 sec)
```

下面为开启 Runtime Filter 后的查询 Summary：

```
mysql> explain analyze select cs_ship_date_sk from catalog_sales, date_dim
    -> where d_date = '2002-2-01' and
    ->      cs_ship_date_sk = d_date_sk;
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
| id                                     | estRows     | actRows | task         | access object       | execution info                                                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                 | memory  | disk |
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
| TableReader_53                         | 37343.19    | 59574   | root         |                     | time:162.1ms, loops:82, RU:0.000000, cop_task: {num: 47, max: 0s, min: 0s, avg: 0s, p95: 0s, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                                                             | MppVersion: 1, data:ExchangeSender_52                                                                                                         | 12.7 KB | N/A  |
| └─ExchangeSender_52                | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | ExchangeType: PassThrough                                                                                                                     | N/A     | N/A  |
|   └─Projection_51                  | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | tpcds50.catalog_sales.cs_ship_date_sk                                                                                                         | N/A     | N/A  |
|     └─HashJoin_48                  | 37343.19    | 59574   | mpp[tiflash] |                     | tiflash_task:{proc max:160.8ms, min:154.3ms, avg: 157.6ms, p80:160.8ms, p95:160.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                  | inner join, equal:[eq(tpcds50.date_dim.d_date_sk, tpcds50.catalog_sales.cs_ship_date_sk)], runtime filter:0[IN] <- tpcds50.date_dim.d_date_sk | N/A     | N/A  |
|       ├─ExchangeReceiver_29(Build) | 1.00        | 2       | mpp[tiflash] |                     | tiflash_task:{proc max:132.3ms, min:130.8ms, avg: 131.6ms, p80:132.3ms, p95:132.3ms, iters:2, tasks:2, threads:16}                                                                                                                                                                                                                                                                                   |                                                                                                                                               | N/A     | N/A  |
|       │ └─ExchangeSender_28      | 1.00        | 1       | mpp[tiflash] |                     | tiflash_task:{proc max:131ms, min:0s, avg: 65.5ms, p80:131ms, p95:131ms, iters:1, tasks:2, threads:1}                                                                                                                                                                                                                                                                                                | ExchangeType: Broadcast, Compression: FAST                                                                                                    | N/A     | N/A  |
|       │   └─TableFullScan_26     | 1.00        | 1       | mpp[tiflash] | table:date_dim      | tiflash_task:{proc max:3.01ms, min:0s, avg: 1.51ms, p80:3.01ms, p95:3.01ms, iters:1, tasks:2, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:2, total_skipped_packs:12, total_scanned_rows:16384, total_skipped_rows:97625, total_rs_index_load_time: 0ms, total_read_time: 0ms}, total_create_snapshot_time: 0ms, total_local_region_num: 1, total_remote_region_num: 0}                     | pushed down filter:eq(tpcds50.date_dim.d_date, 2002-02-01 00:00:00.000000), keep order:false                                                  | N/A     | N/A  |
|       └─Selection_31(Probe)        | 71638034.00 | 5308995 | mpp[tiflash] |                     | tiflash_task:{proc max:39.8ms, min:24.3ms, avg: 32.1ms, p80:39.8ms, p95:39.8ms, iters:86, tasks:2, threads:16}                                                                                                                                                                                                                                                                                       | not(isnull(tpcds50.catalog_sales.cs_ship_date_sk))                                                                                            | N/A     | N/A  |
|         └─TableFullScan_30         | 71997669.00 | 5335549 | mpp[tiflash] | table:catalog_sales | tiflash_task:{proc max:36.8ms, min:23.3ms, avg: 30.1ms, p80:36.8ms, p95:36.8ms, iters:86, tasks:2, threads:16}, tiflash_scan:{dtfile:{total_scanned_packs:660, total_skipped_packs:12451, total_scanned_rows:5335549, total_skipped_rows:100905778, total_rs_index_load_time: 2ms, total_read_time: 47ms}, total_create_snapshot_time: 0ms, total_local_region_num: 194, total_remote_region_num: 0} | pushed down filter:empty, keep order:false, runtime filter:0[IN] -> tpcds50.catalog_sales.cs_ship_date_sk                                     | N/A     | N/A  |
+----------------------------------------+-------------+---------+--------------+---------------------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------------------------+---------+------+
9 rows in set (0.17 sec)
```

1. IO 的减少：对比Table Full Scan 算子的 ```total_scanned_rows```可知，开启 Runtime Filter 后 TableFullScan 的扫描量减少了 2/3 。
2. Hash Join 的性能提升：Hash Join 算子的执行速度从 376.1ms 提升至 157.6ms。

### 最佳实践

Runtime Filter 最适用于大表和小表进行 Join 的情况，比如事实表和维度表进行关联查询的业务逻辑。维度表的命中的数据量越小，意味着 Filter 的取值越少，事实表就能更多的过滤掉不满足条件的数据，对比默认情况下的扫全事实表的情况，其性能效果非常明显。

比如 TPC-DS 中的 泛 Sales 表和 date_dim 表 Join 就是典型的例子。

## Runtime Filter Mode

Runtime Filter Mode 指的是 Runtime Filter 的模式，简单来说就是 **生成 Filter 的算子** 和 **接收 Filter 算子**之间的关系。 一共有三种 Mode：OFF, LOCAL, GLOBAL。目前（v7.3）仅支持 OFF，LOCAL。通过 Session Variable ```tidb_runtime_filter_mode``` 控制。

+ OFF：设置为 OFF，则关闭 Runtime Filter。关闭 Runtime Filter 后查询行为和过去完全一致。
+ LOCAL：开启 LOCAL 模式的 Runtime Filter。LOCAL 模式指的是 **生成 Filter 的算子** 和 **接收 Filter 的算子**在同一个 Task 中。 简单说就是 Runtime Filter 可应用于 Hash Join 算子和 Table Scan 算子在同一个 Task 中的情况。*目前 Runtime Filter 仅支持 LOCAL 模式，如果要开启直接设置 LOCAL 即可。*
+ GLOBAL: 暂未支持 GLOBAL 模式。不可设置为该模式。

```tidb_runtime_filter_mode```: 默认取值为 OFF，则查询不开启 Runtime Filter。LOCAL 则为开启 LOCAL 模式的 Runtime Filter。详细变量使用方式见[Ref](https://docs.pingcap.com/tidb/v7.2/system-variables#tidb_runtime_filter_mode-new-in-v720)

## Runtime Filter Type

 Runtime Filter Type 指的是 Runtime Filter 谓词的类型，简单来说就是生成的 Filter 算子他的谓词类型是什么。目前一共一种：IN，即生成的谓词类似于 ```k1 in (xxx)```。通过 Session Variable ```tidb_runtime_filter_type``` 控制。

+ IN：设置为 IN，默认也是 IN。即生成的 Runtime Filter 类型为 IN 类型的谓词。

## 限制

+ Runtime Filter 是一个 MPP 架构下的优化，其仅可应用于 TiFlash 执行引擎。
+ Join Type：Left outer，Full outer，anti join（当左表为 Probe Side 时）均不可生成 Runtime Filter。由于 Runtime Filter 是提前过滤参与 Join 的数据，所以这些类型的 Join 其并不会丢弃未 match 上的数据所以不可使用该优化。
+ Equal Join expression：当等值 Join 表达式中的 Probe Column 为复杂表达式，或者 Probe Column 的类型为 Json，Blob，Array 等复合类型，则也不会生成 Runtime Filter。主要原因是这类 Column 一般很少作为 Equal Join 的关联列，且即使生成了 Filter 过滤率也一般很差。

以上限制均可以通过 ```explain + query``` 的形式验证 Runtime Filter 是否正确的生成。
