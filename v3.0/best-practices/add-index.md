---
title: Add Index Benchmark 以及调参对比测试
category: best-practices
---

# Add Index Benchmark 以及调参对比测试

## 测试目的

对比 TiDB 3.0 版本和 2.0 版本 `add Index` 的速度以及调参对比和建议。

## 测试版本、时间、地点

TiDB 版本：
 * Release 3.0: 6e2d6c7aa7eba3ac4f3a5201f1a36bf534fa6298
 * v2.0.6

时间：2018 年 12 月 11 日

地点：北京

## 测试环境

4 台AWS 机器，1 台机器部署 TiDB，PD, 监控，另外 3 台部署 TiKV，机器配置均为  E5-2686 v4 @ 2.30GHz，8核 59G，1.7T  本地 SSD。

磁盘： ansible 部署时报磁盘写入慢，忽略并跳过警告后。用 dd 命令测试了下磁盘速度如下：

```shell
$ time dd if=/dev/zero of=test.dbf bs=8k count=500000
500000+0 records in
500000+0 records out
4096000000 bytes (4.1 GB) copied, 7.17135 s, 571 MB/s
$ time dd if=/dev/zero of=test.dbf bs=8k count=500000 oflag=direct
500000+0 records in
500000+0 records out
4096000000 bytes (4.1 GB) copied, 45.1516 s, 90.7 MB/s
$ dd if=test.dbf bs=8k count=500000 of=/dev/null
500000+0 records in
500000+0 records out
4096000000 bytes (4.1 GB) copied, 1.06741 s, 3.8 GB/s
```

### 测试数据

一共对 2 张表进行测试，每张表 2000 万行数据：
* 表 1 是宽表：`t_wide`，200 列， c0 ~ c65 是 `int` 类型， c66~c132 是 `varchar(200)` 类型， c133~c199 是 `timestamp` 类型。
* 表 2 是窄表：`t_slim`， 10 列，c0 ~ c2 是 `int` 类型， c3~c5 是 `varchar(200)` 类型， c6~c9 是 `timestamp` 类型。

### 版本信息

Release 3.0

| 组件  |                  GitHash                   |
| :--- | :---------------------------------------- |
| TiDB  | `6e2d6c7aa7eba3ac4f3a5201f1a36bf534fa6298` |
| TiKV  | `d6a1def0c924af9751c46d5b77663f753c64c562` |
|  PD   | `6ebba48d8ce14307171e097ca782838e1d73e4bd` |


V2.0.6

| 组件  |                  GitHash                   |
| :--- | :---------------------------------------- |
| TiDB  | `b13bc08462a584a085f377625a7bab0cc0351570` |
| TiKV  | `57c83dc4ebc93d38d77dc8f7d66db224760766cc` |
|  PD   | `b64716707b7279a4ae822be767085ff17b5f3fea` |

## 参数配置

均为默认参数配置

## 集群拓扑

| 机器 IP       | 部署实例                |
| :------------ | :---------------------- |
| 172.31.25.68  | 1 * TiDB,  1 * PD, 监控 |
| 172.31.30.195 | 1 * TiKV                |
| 172.31.29.199 | 1 * TiKV                |
| 172.31.23.149 | 1 * TiKV                |

## Benchmark 对比

### add index 

对比测试 `alter table t_xx add index idx_(c0)` 的时间。

注： `alter table t add index idx_(c_int, c_timestamp)`  联合索引测试和  `alter table t add index idx_(c_varchar(100))` `varchar` 索引测试结果类似， `varchar (100)` 索引会稍微慢几秒。

TiDB V3.0 的 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 参数分别是 16，4096。

TiDB V2.0.6 不支持设置 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 参数，其默认值分别是 16，128。

![add-index-best-practices-01](/media/add-index-best-practices-01.png)

### add unique index 

`alter table t add unique index idx_(c0)`

![add-index-best-practices-02](/media/add-index-best-practices-02.png)

### 测试结论

add index 时间计算：在相同的表结构下，测试 200W 数据数据的 add index 时间，基本和 2000W 数据的 add index 的时间成 10 倍的关系。以此类推， TiDB v3.0 版本 1亿 数据在类似的硬件，且无其他负载情况下， add index 消耗的时间大致为 344 * 5 = 1720 s = 29 min。有其他负载情况下 add index 操作会更慢一些，因为 add index 是低优先级操作。

## 参数调整测试

目前 TiDB 3.0 影响 add index 速度的参数有 2 个：

* `tidb_ddl_reorg_worker_cnt` ：add index 的并发度，默认是 4
* `tidb_ddl_reorg_batch_size` ：每次 add index 时的 batch 大小，默认是 256

注：3.0.2 以及 2.0.16 之前，` tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 的默认值分别是 16 ，1024。

以下测试是对各个参数单独设置 看其对 `add index` 的影响。

注：为加速测试，下面测试的数据量为 200W。

## tidb_ddl_reorg_worker_cnt 参数测试

| batch_size | worker_cnt | time_on_t_wide | time_on_t_slim |
| :--------- | :--------- | :------------- | :------------- |
| 128        | 1          | 243            | 162            |
| 128        | 4          | 79.963         | 67.44          |
| 128        | 8          | 54.623         | 56.99          |
| 128        | 12         | 52.95          | 43.4           |
| 128        | 16         | 48.8           | 45.2           |
| 128        | 20         | 47.3           | 39.7           |
| 128        | 24         | 48.5           | 42.9           |
| 128        | 28         | 48.45          | 41.7           |
| 128        | 32         | 44.73          | 40.49          |
| 128        | 36         | 45.84          | 39.27          |
| 128        | 40         | 42.54          | 42.452         |
| 128        | 44         | 43.11          | 42.2           |

![add-index-best-practices-03](/media/add-index-best-practices-03.png)

### tidb_ddl_reorg_batch_size 参数测试

| batch_size | worker_cnt | time_on_t_wide | time_on_t_slim |
| :--------- | :--------- | :------------- | :------------- |
| 128        | 1          | 269            | 170            |
| 512        | 1          | 193            | 124            |
| 1024       | 1          | 160            | 101            |
| 1536       | 1          | 150            | 92             |
| 2048       | 1          | 143            | 92             |
| 2560       | 1          | 141            | 91             |
| 3072       | 1          | 142            | 88             |
| 3584       | 1          | 139            | 89             |
| 4096       | 1          | 137            | 87             |
| 4608       | 1          | 138            | 90             |
| 5120       | 1          | 139            | 87             |
| 5632       | 1          | 138            | 85             |
| 6144       | 1          | 137            | 87             |

![add-index-best-practices-04](/media/add-index-best-practices-04.png)

### 测试结论

在无其他负载情况下，想让 add index 尽快完成，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 适当调大，比如 16，1024, 甚至 20，2048等。

在有其他负载情况下，想让 add index 尽量不影响其他业务，可以将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 适当调小，比如 4, 256。

另外，在 `add index` 的同时，如果有对该表有比较频繁的 `Update` 操作，建议调小 `tidb_ddl_reorg_batch_size` ，比如 `128`，否则可能导致 `add index` 和 `update` 的事务冲突导致重试。

