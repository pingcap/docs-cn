---
title: TiDB-Lightning 监控告警
category: reference
aliases: ['/docs-cn/tools/lightning/monitor/']
---

# TiDB-Lightning 监控告警

TiDB-Lightning 支持给 [Prometheus](https://prometheus.io/) 采集监控指标 (metrics)。本文主要介绍 TiDB-Lightning 的监控配置与监控指标。

## 监控配置

- 如果是使用 TiDB-Ansible 部署 Lightning，只要将服务器地址加到 `inventory.ini` 里的 `[monitored_servers]` 部分即可。
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

```yaml
...
scrape_configs:
  - job_name: 'tidb-lightning'
    static_configs:
      - targets: ['192.168.20.10:8289']
```

## 监控指标

本节详细描述 `tikv-importer` 和 `tidb-lightning` 的监控指标。

### `tikv-importer`

`tikv-importer` 的监控指标皆以 `tikv_import_*` 为前缀。

- **`tikv_import_rpc_duration`**（直方图）

    导入 RPC 需时的直方图。标签：

    - **request**：RPC 名称，如 `open_engine`、`import_engine` 等
    - **result**：`ok` / `error`

- **`tikv_import_write_chunk_bytes`**（直方图）

    从 `tidb-lightning` 写入每个区块大小的直方图。

- **`tikv_import_write_chunk_duration`**（直方图）

    从 `tidb-lightning` 写入每个区块需时直方图。

- **`tikv_import_upload_chunk_bytes`**（直方图）

    上传到 TiKV 的每个区块大小的直方图。

- **`tikv_import_upload_chunk_duration`**（直方图）

    上传到 TiKV 的每个区块需时的直方图。

### `tidb-lightning`

`tidb-lightning` 的监控指标皆以 `lightning_*` 为前缀。

- **`lightning_importer_engine`**（计数器）

    计算已开启及关闭的引擎文档数量。标签：

    - **type**：`open` / `closed`

- **`lightning_idle_workers`**（测量仪）

    计算闲置的工作流程。数值应低于设置中的 `*-concurrency` 的值，且经常为 0。标签：

    - **name**：`table` / `region` / `io`

- **`lightning_kv_encoder`**（计数器）

    计算已开启及关闭的 KV 编码器。KV 编码器是运行于内存的 TiDB 实例，用于将 SQL 的 `INSERT` 语句转换成 KV 对。此度量的净值（开启减掉关闭）在正常情况下不应持续增长。标签：

    - **type**：`open` / `closed`

- **`lightning_tables`**（计数器）

    计算处理过的表及其状态。标签：

    - **state**：`pending` / `written` / `closed` / `imported` / `altered_auto_inc` / `checksum` / `analyzed` / `completed`
    - **result**：`success` / `failure`

- **`lightning_chunks`**（计数器）

    计算处理过的 Chunks 及其状态。标签：

    - **state**：`estimated` / `pending` / `running` / `finished` / `failed`

- **`lightning_import_seconds`**（直方图）

    导入每个表需时的直方图。

- **`lightning_block_read_seconds`**（直方图）

    读取每个 SQL 区块需时的直方图。

- **`lightning_block_read_bytes`**（直方图）

    每个 SQL 区块大小的直方图。

- **`lightning_block_encode_seconds`**（直方图）

    每个 SQL 区块转换成 KV 对需时的直方图。

- **`lightning_block_deliver_seconds`**（直方图）

    每个 KV 对区块传送到 `tikv-importer` 需时的直方图。

- **`lightning_block_deliver_bytes`**（直方图）

    每个 KV 对区块大小的直方图。

- **`lightning_chunk_parser_read_block_seconds`**（直方图）

    解析每个 SQL 区块需时的直方图。

- **`lightning_chunk_parser_read_row_seconds`**（直方图）

    解析每行 SQL 需时的直方图。

- **`lightning_checksum_seconds`**（直方图）

    计算校验和（Checksum）需时的直方图。

- **`lightning_apply_worker_seconds`**（直方图）

    获取闲置工作流程等待时间的直方图。标签：

    - **name**: `table` / `region` / `io`
