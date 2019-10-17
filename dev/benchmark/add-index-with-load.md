---
title: 线上负载与 `Add Index` 相互影响测试
category: benchmark
---

# 线上负载与 `Add Index` 相互影响测试

## 测试目的

测试 OLTP 场景下，`Add Index` 与线上负载的相互影响。

## 测试版本、时间、地点

TiDB 版本：v3.0.1

时间：2019 年 7 月

地点：北京

## 测试环境

测试在 Kubernetes 集群上进行，部署了 3 个 TiDB 实例，3 个 TiKV 实例和 3 个 PD 实例。

### 版本信息

| 组件  |                  GitHash                   |
| :--- | :---------------------------------------- |
| TiDB  | `9e4e8da3c58c65123db5f26409759fe1847529f8` |
| TiKV  | `4151dc8878985df191b47851d67ca21365396133` |
|  PD   | `811ce0b9a1335d1b2a049fd97ef9e186f1c9efc1` |

Sysbench 版本：1.0.17

### TiDB 参数配置

TiDB、TiKV 和 PD 均使用 [TiDB Operator](https://github.com/pingcap/tidb-operator) 默认配置。

### 集群拓扑

|                 机器 IP                  |   部署实例   |
| :-------------------------------------- | :----------|
|                172.31.8.8                 |  Sysbench |
| 172.31.7.69, 172.31.5.152, 172.31.11.133 |      PD      |
| 172.31.4.172, 172.31.1.155, 172.31.9.210 |     TiKV     |
| 172.31.7.80, 172.31.5.163, 172.31.11.123 |     TiDB     |

### 使用 Sysbench 模拟线上负载

使用 Sysbench 向集群导入 **1 张表，数据 200 万**。

执行如下命令导入数据：

{{< copyable "shell-regular" >}}

```sh
sysbench oltp_common \
    --threads=16 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    prepare --tables=1 --table-size=2000000
```

执行如下命令测试数据：

{{< copyable "shell-regular" >}}

```sh
sysbench $testname \
    --threads=$threads \
    --time=300000 \
    --report-interval=15 \
    --rand-type=uniform \
    --rand-seed=$RANDOM \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$tidb_host \
    --mysql-port=$tidb_port \
    --mysql-user=root \
    run --tables=1 --table-size=2000000
```

## 测试方案 1：`Add Index` 目标列被频繁 Update

1. 开始 `oltp_read_write` 测试。
2. 与步骤 1 同时，使用 `alter table sbtest1 add index c_idx(c)` 添加索引。
3. 在步骤 2 结束，即索引添加完成时，停止步骤 1 的测试。
4. 获取指标 `alter table ... add index` 的运行时间，sysbench 在该时间段内的平均 TPS 和 QPS。
5. 逐渐增大 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 两个参数的值，重复步骤 1-4。

### 测试结果

#### 无 `Add Index` 时 `oltp_read_write` 的结果

| sysbench TPS | sysbench QPS    |
| :------- | :-------- |
| 350.31   | 6806 |

#### `tidb_ddl_reorg_batch_size = 32`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 402 |  338.4 |           6776 |
| 2     | 266 |  330.3 |           6001 |
| 4     | 174 |  288.5 |           5769 |
| 8     | 129 |  280.6 |           5612 |
| 16    | 90 |   263.5 |           5273 |
| 32    | 54 |   229.2 |           4583 |
| 48    | 57 |   230.1 |           4601 |

![add-index-load-1-b32](/media/add-index-load-1-b32.png)

#### `tidb_ddl_reorg_batch_size = 64`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 264 |  269.4 |           5388 |
| 2     | 163 |  266.2 |           5324 |
| 4     | 105 |  272.5 |           5430 |
| 8     | 78 |  262.5 |           5228 |
| 16    | 57 |   215.5 |           4308 |
| 32    | 42 |   185.2 |           3715 |
| 48    | 45 |   189.2 |           3794 |

![add-index-load-1-b64](/media/add-index-load-1-b64.png)

#### `tidb_ddl_reorg_batch_size = 128`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 171 |  289.1 |           5779 |
| 2     | 110 |  274.2 |           5485 |
| 4     | 79 |  250.6 |           5011 |
| 8     | 51 |  246.1 |           4922 |
| 16    | 39 |   171.1 |           3431 |
| 32    | 35 |   130.8 |           2629 |
| 48    | 35 |   120.5 |           2425 |

![add-index-load-1-b128](/media/add-index-load-1-b128.png)

#### `tidb_ddl_reorg_batch_size = 256`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 145 |  283.0 |           5659 |
| 2     | 96 |  282.2 |           5593 |
| 4     | 56 |  236.5 |           4735 |
| 8     | 45 |  194.2 |           3882 |
| 16    | 39 |   149.3 |           2893 |
| 32    | 36 |   113.5 |           2268 |
| 48    | 33 |   86.2 |           1715 |

![add-index-load-1-b256](/media/add-index-load-1-b256.png)

#### `tidb_ddl_reorg_batch_size = 512`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 135 |  257.8 |           5147 |
| 2     | 78 |  252.8 |           5053 |
| 4     | 49 |  222.7 |           4478 |
| 8     | 36 |  145.4 |           2904 |
| 16    | 33 |   109 |           2190 |
| 32    | 33 |   72.5 |           1503 |
| 48    | 33 |   54.2 |           1318 |

![add-index-load-1-b512](/media/add-index-load-1-b512.png)

#### `tidb_ddl_reorg_batch_size = 1024`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 111 |  244.3 |           4885 |
| 2     | 78 |  228.4 |           4573 |
| 4     | 54 |  168.8 |           3320 |
| 8     | 39 |  123.8 |           2475 |
| 16    | 36 |   59.6 |           1213 |
| 32    | 42 |   93.2 |           1835 |
| 48    | 51 |   115.7 |           2261 |

![add-index-load-1-b1024](/media/add-index-load-1-b1024.png)

#### `tidb_ddl_reorg_batch_size = 2048`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 918 |  243.3 |           4855 |
| 2     | 1160 |  209.9 |           4194 |
| 4     | 342 |  185.4 |           3707 |
| 8     | 1316 |  151.0 |           3027 |
| 16    | 795 |   30.5 |           679 |
| 32    | 1130 |   26.69 |           547 |
| 48    | 893 |   27.5 |           552 |

![add-index-load-1-b2048](/media/add-index-load-1-b2048.png)

#### `tidb_ddl_reorg_batch_size = 4096`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 3042 |  200.0 |           4001 |
| 2     | 3022 |  203.8 |           4076 |
| 4     | 858 |  195.5 |            3971 |
| 8     | 3015 |  177.1 |           3522 |
| 16    | 837 |   143.8 |           2875 |
| 32    | 942 |   114 |           2267 |
| 48    | 187 |   54.2 |           1416 |

![add-index-load-1-b4096](/media/add-index-load-1-b4096.png)

### 测试结论

若 `Add Index` 的目标列正在进行较为频繁的写操作（本测试涉及列的 `UPDATE`、`INSERT` 和 `DELETE`），默认 `Add Index` 配置对系统的线上负载有比较明显的影响，该影响主要来源于 `Add Index` 与 Column Update 并发进行造成的写冲突，系统的表现反应在：

- 随着两个参数的逐渐增大，`TiKV_prewrite_latch_wait_duration` 有明显的升高，造成写入变慢。
- `tidb_ddl_reorg_worker_cnt` 与 `tidb_ddl_reorg_batch_size` 非常大时，`admin show ddl` 命令可以看到 DDL job 的多次重试（例如 `Write conflict, txnStartTS 410327455965380624 is stale [try again later], ErrCount:38, SnapshotVersion:410327228136030220`），此时 `Add Index` 会持续非常久才能完成。

## 测试方案 2：`Add Index` 目标列不涉及写入（仅查询）

1. 开始 `oltp_read_only` 测试。
2. 与步骤 1 同时，使用 `alter table sbtest1 add index c_idx(c)` 添加索引。
3. 在步骤 2 结束，即索引添加完成时，停止步骤 1。
4. 获取指标 `alter table ... add index` 的运行时间，sysbench 在该时间段内的平均 TPS 和 QPS。
5. 逐渐增大 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 两个参数，重复步骤 1-4。

### 测试结果

#### 无 `Add Index` 时 `oltp_read_only` 结果

| sysbench TPS | sysbench QPS    |
| :------- | :-------- |
| 550.9   | 8812.8 |

#### `tidb_ddl_reorg_batch_size = 32`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 376 |  548.9 |           8780 |
| 2     | 212 |  541.5 |           8523 |
| 4     | 135 |  538.6 |           8549 |
| 8     | 114 |  536.7 |           8393 |
| 16    | 77 |   533.9 |           8292 |
| 32    | 46 |   533.4 |           8103 |
| 48    | 46 |   532.2 |           8074 |

![add-index-load-2-b32](/media/add-index-load-2-b32.png)

#### `tidb_ddl_reorg_batch_size = 1024`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 91 |  536.8 |           8316 |
| 2     | 52 |  533.9 |           8165 |
| 4     | 40 |  522.4 |           7947 |
| 8     | 36 |  510 |           7860 |
| 16    | 33 |   485.5 |           7704 |
| 32    | 31 |   467.5 |           7516 |
| 48    | 30 |   562.1 |           7442 |

![add-index-load-2-b1024](/media/add-index-load-2-b1024.png)

#### `tidb_ddl_reorg_batch_size = 4096`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 103 |  502.2 |           7823 |
| 2     | 63 |  486.5 |           7672 |
| 4     | 52 |  467.4 |            7516 |
| 8     | 39 |  452.5 |           7302 |
| 16    | 35 |   447.2 |           7206 |
| 32    | 30 |   441.9 |           7057 |
| 48    | 30 |   440.1 |           7004 |

![add-index-load-2-b4096](/media/add-index-load-2-b4096.png)

### 测试结论

`Add Index` 的目标列仅有查询负载时，`Add Index` 对负载的影响不明显。

## 测试方案 3：集群负载不涉及 `Add Index` 目标列

1. 开始 `oltp_read_write` 测试。
2. 与步骤 1 同时，使用 `alter table test add index pad_idx(pad)` 添加索引。
3. 在步骤 2 结束，即索引添加完成时，停止步骤 1 的测试。
4. 获取指标 `alter table ... add index` 的运行时间，sysbench 在该时间段内的平均 TPS 和 QPS。
5. 逐渐增大 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 两个参数，重复步骤 1-4。

### 测试结果

#### 无 `Add Index` 时 `oltp_read_write` 的结果

| sysbench TPS | sysbench QPS    |
| :------- | :-------- |
| 350.31   | 6806 |

#### `tidb_ddl_reorg_batch_size = 32`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 372 |  350.4 |           6892 |
| 2     | 207 |  344.2 |           6700 |
| 4     | 140 |  343.1 |           6672 |
| 8     | 121 |  339.1 |           6579 |
| 16    | 76 |   340   |           6607 |
| 32    | 42 |   343.1 |           6695 |
| 48    | 42 |   333.4 |           6454 |

![add-index-load-3-b32](/media/add-index-load-3-b32.png)

#### `tidb_ddl_reorg_batch_size = 1024`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 94 |  352.4 |           6794 |
| 2     | 50 |  332 |           6493 |
| 4     | 45 |  330 |           6456 |
| 8     | 36 |  325.5 |           6324 |
| 16    | 32 |   312.5   |           6294 |
| 32    | 32 |   300.6 |           6017 |
| 48    | 31 |   279.5 |           5612 |

![add-index-load-3-b1024](/media/add-index-load-3-b1024.png)

#### `tidb_ddl_reorg_batch_size = 4096`

| tidb_ddl_reorg_worker_cnt |  add_index_durations(s) | sysbench TPS   | sysbench QPS |
| :------------------------ | :---------------------- | :------------- | :----------- |
| 1     | 116 |  325.5 |           6324 |
| 2     | 65 |  312.5 |           6290 |
| 4     | 50 |  300.6 |           6017 |
| 8     | 37 |  279.5 |           5612 |
| 16    | 34 |   250.4   |           5365 |
| 32    | 32 |   220.2 |           4924 |
| 48    | 33 |   214.8 |           4544 |

![add-index-load-3-b4096](/media/add-index-load-3-b4096.png)

### 测试结论

`Add Index` 的目标列与负载无关时，`Add Index` 对负载的影响不明显。

## 总结

- 当 `Add Index` 的目标列被频繁更新（包含 `UPDATE`, `INSERT` 和 `DELETE`）时，默认配置会造成较为频繁的写冲突，使得在线负载较大；同时 `Add Index` 也可能由于不断地重试，需要很长的时间才能完成。在本次测试中，将 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 的乘积调整为默认值的 1/32（例如 `tidb_ddl_reorg_worker_cnt` = 4，`tidb_ddl_reorg_batch_size` = 256）可以取得较好的效果。
- 当 `Add Index` 的目标列仅涉及查询负载，或者与线上负载不直接相关时，可以直接使用默认配置。