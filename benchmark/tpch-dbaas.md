---
title: TiDB TPC-H 10G 性能测试报告
category: benchmark
---

# TiDB TPC-H 10G 性能测试报告

## 测试目的

测试 DBaaS 上 TiDB 在 OLAP 场景下 4.0 版本的性能。

## 测试环境

### 测试集群

High 配置，2 个 TiDB 节点、3 个 TiKV 节点、3 个 TiFlash。其中 TiKV 节点与 TiFlash 节点混合部署。

> **注意：**
>
> 4.0.0-rc.1 版本中，TiFlash 不支持新的[字符排序规则](/reference/sql/characterset-and-collation.md#排序规则支持)下的计算下推，此环境中关闭了新的字符排序规则。后续版本 TiFlash 会支持新的排序规则。
> 
> ```
> mysql> select VARIABLE_VALUE from mysql.tidb where VARIABLE_NAME='new_collation_enabled';
> +----------------+
> | VARIABLE_VALUE |
> +----------------+
> | False          |
> +----------------+
> ```

### TiDB 版本信息

|  组件名  |  版本号      | commit hash                                |
|---------|-------------|--------------------------------------------|
| TiDB    | v4.0.0-rc.1 | 7267747ae0ec624dffc3fdedb00f1ed36e10284b   |
| PD      | v4.0.0-rc.1 | 31dae220db6294f2dc2ec0df330892fe76e59edc   |
| TiKV    | v4.0.0-rc.1 | e26d1524044327df3976c4477fba253a88ba3afa   |
| TiFlash | v4.0.0-rc.1 | 2d30a83ffa9508fd0468a708cdb0579327f788da   |

## 运行测试

### 导入数据

使用以下命令安装 [TiUP](https://tiup.io/)：

```
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

使用下面 `tiup bench` 命令导入 TPC-H 10 数据。
该命令导入的同时，会给测试的表创建 TiFlash 副本。导入完成后会自动对表进行 `analyze table` 操作，收集[统计信息](/reference/performance/statistics.md)，供 TiDB 优化器优化执行计划。

```
tiup bench tpch prepare
    --host ${tidb_host} --port 4000 --db tpch_10 --password ${password} \
    --sf 10 \
    --tiflash \
    --analyze --tidb_build_stats_concurrency 8 --tidb_distsql_scan_concurrency 30
```

运行完之后，确认数据已经建立好 TiFlash 副本：

```
mysql> select * from information_schema.tiflash_replica;
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| TABLE_SCHEMA | TABLE_NAME | TABLE_ID | REPLICA_COUNT | LOCATION_LABELS | AVAILABLE | PROGRESS |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
| tpch_10      | nation     |       53 |             1 |                 |         1 |        1 |
| tpch_10      | part       |       59 |             1 |                 |         1 |        1 |
| tpch_10      | supplier   |       62 |             1 |                 |         1 |        1 |
| tpch_10      | partsupp   |       65 |             1 |                 |         1 |        1 |
| tpch_10      | region     |       56 |             1 |                 |         1 |        1 |
| tpch_10      | orders     |       72 |             1 |                 |         1 |        1 |
| tpch_10      | customer   |       68 |             1 |                 |         1 |        1 |
| tpch_10      | lineitem   |       75 |             1 |                 |         1 |        1 |
+--------------+------------+----------+---------------+-----------------+-----------+----------+
```

### 执行查询

本文会比较智能选择、TiKV 隔离读、TiFlash 隔离读等三种[读取模式](/reference/tiflash/use-tiflash.md#使用-tidb-读取-tiflash)下的 TiDB 性能。使用 MySQL 客户端连接到 TiDB 集群，先设置优化参数以及读取的模式。

```
mysql> set @@session.tidb_allow_batch_cop = 1; set @@session.tidb_opt_distinct_agg_push_down = 1; set @@tidb_distsql_scan_concurrency = 30;
# 设置读取模式. 不同读取模式对应的值如下:
# 智能选择:'tikv,tiflash', TiKV隔离读:'tikv', TiFlash隔离读:'tiflash'.
mysql> set @@session.tidb_isolation_read_engines = 'tikv,tiflash';
# 可以通过以下语句确认当前变量值
mysql> select @@tidb_isolation_read_engines , @@tidb_allow_batch_cop , @@tidb_opt_distinct_agg_push_down , @@tidb_distsql_scan_concurrency;
+-------------------------------+------------------------+-----------------------------------+---------------------------------+
| @@tidb_isolation_read_engines | @@tidb_allow_batch_cop | @@tidb_opt_distinct_agg_push_down | @@tidb_distsql_scan_concurrency |
+-------------------------------+------------------------+-----------------------------------+---------------------------------+
| tikv,tiflash                  | 1                      | 1                                 | 30                              |
+-------------------------------+------------------------+-----------------------------------+---------------------------------+
```

然后执行 TPC-H 的查询语句。你可以在这里找到具体的查询语句：[tidb-bench/tpch/queries](https://github.com/pingcap/tidb-bench/tree/master/tpch/queries)。

### 测试结果

| Query ID |  智能选择  |  TiKV 隔离读  |  TiFlash 隔离读  | 
|--------:|-----------:|------------:|--------------:|
| 1       |      2.25s |      15.02s |         2.24s |
| 2       |      2.57s |       2.74s |         2.59s |
| 3       |      4.89s |       9.35s |         4.80s |
| 4       |      2.38s |       2.91s |         5.33s |
| 5       |      8.19s |       9.69s |         8.53s |
| 6       |      0.44s |       5.52s |         0.45s |
| 7       |      3.93s |       6.49s |         4.24s |
| 8       |      9.53s |       6.38s |         9.61s |
| 9       |     21.24s |      22.90s |        22.12s |
| 10      |      4.27s |       4.62s |         4.47s |
| 11      |      1.83s |       2.05s |         1.85s |
| 12      |      1.13s |       5.30s |         1.34s |
| 13      |      5.78s |       6.15s |         6.18s |
| 14      |      0.97s |       3.93s |         0.97s |
| 15      |      1.08s |       8.02s |         1.00s |
| 16      |      1.95s |       2.34s |         1.27s |
| 17      |      8.45s |      15.20s |         8.79s |
| 18      |      ?.??s |       ?.??s |         ?.??s |
| 19      |      3.24s |       5.61s |         3.29s |
| 20      |      1.39s |       4.20s |         9.51s |
| 21      |      6.63s |       7.74s |        14.61s |
| 22      |      2.50s |       3.12s |         2.63s |

![TPC-H Query Result](/media/tpch-query-result-v4.0-dbaas.png)

说明：

- 图中蓝色为智能选择，红色为 TiKV 隔离读，黄色为 TiFlash 隔离读，纵坐标是 Query 的处理时间，纵坐标越低，性能越好。
- 图中不显示 Query 18 结果，因为 4.0.0-rc.1 版本 TiDB 聚合算子在大数据量情况下消耗较多内存，Query 18 查询时会报错：`Lost connection to MySQL server during query`。相关 Issue 见 [tidb#14103](https://github.com/pingcap/tidb/issues/14103)、[tidb#14413](https://github.com/pingcap/tidb/issues/14413)。
