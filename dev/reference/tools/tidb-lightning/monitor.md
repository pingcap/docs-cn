---
title: TiDB Lightning 监控告警
category: reference
---

# TiDB Lightning 监控告警

`tidb-lightning` 和 `tikv-importer` 都支持使用 [Prometheus](https://prometheus.io/) 采集监控指标 (metrics)。本文主要介绍 TiDB Lightning 的监控配置与监控指标。

## 监控配置

- 如果是使用 TiDB Ansible 部署 Lightning，只要将服务器地址加到 `inventory.ini` 文件里的 `[monitored_servers]` 部分即可。
- 如果是手动部署 Lightning，则参照以下步骤进行配置。

### `tikv-importer`

`tikv-importer` v2.1 使用 [Pushgateway](https://github.com/prometheus/pushgateway) 来推送监控指标。需要配置 `tikv-importer.toml` 来连接 Pushgateway：

```toml
[metric]

# 给 Prometheus 客户端的推送任务名称。
job = "tikv-importer"

# 给 Prometheus 客户端的推送间隔。
interval = "15s"

# Prometheus Pushgateway 地址。
address = ""
```

### `tidb-lightning`

只要 Prometheus 能发现 `tidb-lightning` 的监控地址，就能收集监控指标。

监控的端口可在 `tidb-lightning.toml` 中配置：

```toml
[lightning]
# 用于调试和 Prometheus 监控的 HTTP 端口。输入 0 关闭。
pprof-port = 8289

...
```

要让 Prometheus 发现 Lightning，可以将地址直接写入其配置文件，例如：

{{< copyable "" >}}

```yaml
...
scrape_configs:
  - job_name: 'tidb-lightning'
    static_configs:
      - targets: ['192.168.20.10:8289']
```

## Grafana 仪表板

[Grafana](https://grafana.com/) 的可视化仪表盘可以帮助用户在网页上对 Prometheus metrics 进行监控。

使用 TiDB Ansible 部署 TiDB 集群时，会同时部署一套 Grafana + Prometheus 的监控系统。

如果使用其他方式部署 TiDB Lightning，需先[导入仪表盘（JSON 文件）](https://raw.githubusercontent.com/pingcap/tidb-ansible/master/scripts/lightning.json)。

### 速度面板

![第一行速度面板](/media/lightning-grafana-row-1.png)

第一行的面板显示速度，具体为：

| 面板名称 | 功能 | 描述 |
|:-----|:-----|:-----|
| Import speed | write from lightning | 从 TiDB Lightning 向 TiKV Importer 发送键值对的速度，取决于每个表的复杂性 |
| Import speed | upload to tikv | TiKV Importer 上传所有 TiKV replicas 的总体速度 |
| Chunk process duration) | | 完全编码单个数据文件所需的平均时间 |

有时导入速度会降到 0，这是为了平衡其他部分的速度，属于正常现象。

### 进度面板

![第二行进度面板](/media/lightning-grafana-row-2.png)

第二行的面板显示进度，具体为：

| 面板名称 | 描述 |
|:-----|:-----|
| Import progress | 已编码的文件所占百分比 |
| Checksum progress | 已导入的表所占百分比 |
| Failures | 导入失败的表的数量以及故障点，通常为空 |

### 资源使用面板

![第三行资源面板](/media/lightning-grafana-row-3.png)

第三行的面板显示资源使用情况，具体为：

| 面板名称 | 描述 |
|:-----|:-----|
| Memory usage | 每个服务占用的内存 |
| Number of Lightning Goroutines | TiDB Lightning 正在使用的 goroutines 数量 |
| CPU% | 每个服务使用的逻辑 CPU 数 |

### 配额使用面板

![第四行配额使用面板](/media/lightning-grafana-row-4.png)

第四行的面板显示配额使用情况，具体为：

| 面板名称 | 功能 | 描述 |
|:-----|:-----|:-----|
| Idle workers | io | 未使用的 `io-concurrency` 的数量，通常接近配置值（默认为5），接近 0 时表示磁盘太慢 |
| Idle workers | closed-engine | 已关闭但未清理的引擎数量，通常接近 `index-concurrency` 与`table-concurrency` 的和（默认为 8），接近 0 时表示 TiDB Lightning 比 TiKV Importer 快，这会导致 TiDB Lightning 延迟 |
| Idle workers | table | 未使用的 `table-concurrency` 的数量，通常为 0，直到进程结束 |
| Idle workers | index | 未使用的 `index-concurrency` 的数量，通常为 0，直到进程结束 |
| Idle workers | region | 未使用的 `region-concurrency` 的数量，通常为 0，直到进程结束 |
| External resources | KV Encoder | 已激活的 KV encoder 的数量，通常与 `region-concurrency` 的数量相同，直到进程结束 |
| External resources | Importer Engines | 打开的引擎文件数量，不应超过`max-open-engines` 的设置。 |

### 读取速度面板

![第五行读取速度面板](/media/lightning-grafana-row-5.png)

第五行面板显示读取速度，具体为：

| 面板名称 | 功能 | 描述 |
|:-----|:-----|:-----|
| Chunk parser read block duration | read block | 读取一个字节块以准备解析所消耗的时间 |
| Chunk parser read block duration | apply worker | 等待 `io-concurrency` 空闲所消耗的时间 |
| SQL process duration | row encode | 解析和编码单行所消耗的时间 |
| SQL process duration | block deliver | 将一组键/值对发送到 TiKV Importer 所消耗的时间 |

如果上述项的持续时间过长，则表示 TiDB Lightning 使用的磁盘太慢或 I/O 太忙。

### 存储空间面板

![第六行存储空间面板](/media/lightning-grafana-row-6.png)

第六行面板显示存储空间使用情况，具体为：

| 面板名称 | 功能 | 描述 |
|:-----|:-----|:-----|
| SQL process rate | data deliver rate | 向 TiKV Importer 发送键值对 data 的速度 |
| SQL process rate | index deliver rate | 向 TiKV Importer 发送键值对 index 的速度 |
| SQL process rate | total deliver rate | 键值对上传的总速度 |
| Total bytes | parser read size | TiDB Lightning 正在读取的字节数 |
| Total bytes | data deliver size | 已发送到 TiKV Importer 的键值对 data 的字节数 |
| Total bytes | index deliver size | 已发送到 TiKV Importer 的键值对 index 的字节数 |
| Total bytes | storage_size / 3 | TiKV 集群的占用大小的三分之一（3 为默认的副本数量）|

### 导入速度面板

![第七行导入速度面板](/media/lightning-grafana-row-7.png)

第七行面板显示导入速度，具体为：

| 面板名称 | 功能 | 描述 |
|:-----|:-----|:-----|
| Delivery duration | Range delivery | 将一系列键值对上传到 TiKV 集群所消耗的时间  |
| Delivery duration | SST delivery | 将单个 SST 文件上传到 TiKV 集群所消耗的时间 |
| SST process duration | Split SST | 将键值对流切分成若干 SST 文件所消耗的时间 |
| SST process duration | SST upload | 上传单个 SST 文件所消耗的时间 |
| SST process duration | SST ingest | Ingest 单个 SST 文件所消耗的时间 |
| SST process duration | SST size | 单个 SST 文件的大小 |

## 监控指标

本节将详细描述 `tikv-importer` 和 `tidb-lightning` 的监控指标。

### `tikv-importer`

`tikv-importer` 的监控指标皆以 `tikv_import_*` 为前缀。

- **`tikv_import_rpc_duration`**（直方图）

    完成一次 RPC 操作所需时的直方图。标签：

    - **request**：`switch_mode` / `open_engine` / `write_engine` / `close_engine` / `import_engine` / `cleanup_engine` / `compact_cluster` / `upload` / `ingest` / `compact`
    - **result**：`ok` / `error`

- **`tikv_import_write_chunk_bytes`**（直方图）

    从 Lightning 接收的 KV 对区块大小（未压缩）的直方图。

- **`tikv_import_write_chunk_duration`**（直方图）

    从 `tidb-lightning` 接收每个 KV 对区块需时直方图。

- **`tikv_import_upload_chunk_bytes`**（直方图）

     上传到 TiKV 的每个 SST 文件区块大小（压缩）的直方图。

- **`tikv_import_range_delivery_duration`** (直方图)

    将一个 range 的 KV 对发送至 `dispatch-job` 任务需时的直方图。

- **`tikv_import_split_sst_duration`** (直方图)

    将 range 从引擎文件中分离到单个 SST 文件中需时的直方图。

- **`tikv_import_sst_delivery_duration`** (直方图)

    将 SST 文件从 `dispatch-job` 任务发送到 `ImportSSTJob`任务需时的直方图

- **`tikv_import_sst_recv_duration`** (直方图)

    `ImportSSTJob`任务接收从 `dispatch-job` 任务发送过来的 SST 文件需时的直方图。

- **`tikv_import_sst_upload_duration`** (直方图)

    从 `ImportSSTJob` 任务上传 SST 文件到 TiKV 节点需时的直方图。

- **`tikv_import_sst_chunk_bytes`** (直方图)

    上传到 TiKV 节点的 SST 文件（压缩）大小的直方图。

- **`tikv_import_sst_ingest_duration`** (直方图)

    将 SST 文件传入至 TiKV 需时的直方图。

- **`tikv_import_each_phase`** (测量仪)

    表示运行阶段。值为 1 时表示在阶段内运行，值为 0 时表示在阶段内运行。标签：

    - **phase**: `prepare` / `import`

- **`tikv_import_wait_store_available_count`** (计数器)

    计算出现 TiKV 节点没有充足空间上传 SST 文件现象的次数。标签：

    - **store_id**: TiKV 存储 ID。

- **`tikv_import_upload_chunk_duration`**（直方图）

    上传到 TiKV 的每个区块需时的直方图。

### `tidb-lightning`

`tidb-lightning` 的监控指标皆以 `lightning_*` 为前缀。

- **`lightning_importer_engine`**（计数器）

    计算已开启及关闭的引擎文件数量。标签：

    - **type**：`open` / `closed`

- **`lightning_idle_workers`**（计量表盘）

    计算闲置的 worker。数值应低于设置中的 `*-concurrency` 的值，且经常为 0。标签：

    - **name**: `table` / `index` / `region` / `io` / `closed-engine`

- **`lightning_kv_encoder`**（计数器）

    计算已开启及关闭的 KV 编码器。KV 编码器是运行于内存的 TiDB 实例，用于将 SQL 的 `INSERT` 语句转换成 KV 对。此度量的净值（开启减掉关闭）在正常情况下不应持续增长。标签：

    - **type**：`open` / `closed`

- **`lightning_tables`**（计数器）

    计算处理过的表及其状态。标签：

    - **state**：`pending` / `written` / `closed` / `imported` / `altered_auto_inc` / `checksum` / `analyzed` / `completed`
    - **result**：`success` / `failure`

- **`lightning_engines`** (计数器)

    计算处理后引擎文件的数量以及其状态。标签：

    - **state**: `pending` / `written` / `closed` / `imported` / `completed`
    - **result**: `success` / `failure`

- **`lightning_chunks`**（计数器）

    计算处理过的 Chunks 及其状态。标签：

    - **state**：`estimated` / `pending` / `running` / `finished` / `failed`

- **`lightning_import_seconds`**（直方图）

    导入每个表需时的直方图。

- **`lightning_row_read_bytes`**（直方图）

    单行 SQL 数据大小的直方图。

- **`lightning_row_encode_seconds`**（直方图）

    解码单行 SQL 数据到 KV 对需时的直方图。

- **`lightning_row_kv_deliver_seconds`**（直方图）

    发送一组与单行 SQL 数据对应的 KV 对需时的直方图。

- **`lightning_block_deliver_seconds`**（直方图）

    每个 KV 对中的区块传送到 `tikv-importer` 需时的直方图。

- **`lightning_block_deliver_bytes`**（直方图）

    发送到 Importer 的 KV 对中区块（未压缩）的大小的直方图。

- **`lightning_chunk_parser_read_block_seconds`**（直方图）

    数据文件解析每个 SQL 区块需时的直方图。

- **`lightning_checksum_seconds`**（直方图）

    计算表中 Checksum 需时的直方图。

- **`lightning_apply_worker_seconds`**（直方图）

    获取闲置 worker 等待时间的直方图。标签：

    - **name**: `table` / `index` / `region` / `io` / `closed-engine`
