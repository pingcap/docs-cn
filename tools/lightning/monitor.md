---
title: TiDB-Lightning Monitoring
summary: Learn about the monitor configuration and monitoring metrics of TiDB-Lightning.
category: tools
---

# TiDB-Lightning Monitoring

Both `tidb-lightning` and `tikv-importer` supports metrics collection via [Prometheus](https://prometheus.io/). This document introduces the monitor configuration and monitoring metrics of TiDB-Lightning.

## Monitor configuration

- If TiDB-Lightning is installed using TiDB-Ansible, simply add the servers to the `[monitored_servers]` section in the `inventory.ini`. Then the Prometheus server can collect their metrics.
- If TiDB-Lightning is manually installed, follow the instructions below.

### `tikv-importer`

`tikv-importer` v2.1 uses [Pushgateway](https://github.com/prometheus/pushgateway) to deliver
metrics. Configure `tikv-importer.toml` to recognize the Pushgateway with the following settings:

```toml
[metric]

# The Prometheus client push job name.
job = "tikv-importer"

# The Prometheus client push interval.
interval = "15s"

# The Prometheus Pushgateway address.
address = ""
```

### `tidb-lightning`

The metrics of `tidb-lightning` can be gathered directly by Prometheus as long as it is discovered. You can set the metrics port in `tidb-lightning.toml`:

```toml
[lightning]
# HTTP port for debugging and Prometheus metrics pulling (0 to disable)
pprof-port = 8289

...
```

You need to configure Prometheus to make it discover the `tidb-lightning` server. For instance, you can directly add the server address to the `scrape_configs` section:

```yaml
...
scrape_configs:
  - job_name: 'tidb-lightning'
    static_configs:
      - targets: ['192.168.20.10:8289']
```

## Monitoring metrics

This section explains the monitoring metrics of `tikv-importer` and `tidb-lightning`.

### `tikv-importer`

Metrics provided by `tikv-importer` are listed under the namespace `tikv_import_*`.

- **`tikv_import_rpc_duration`** (Histogram)

    Bucketed histogram of total duration needed to complete an RPC action. Labels:

    - **request**: `switch_mode` / `open_engine` / `write_engine` / `close_engine` / `import_engine` / `cleanup_engine` / `compact_cluster` / `upload` / `ingest` / `compact`
    - **result**: `ok` / `error`

- **`tikv_import_write_chunk_bytes`** (Histogram)

    Bucketed histogram of the uncompressed size of a block of KV pairs received from Lightning.

- **`tikv_import_write_chunk_duration`** (Histogram)

    Bucketed histogram of the time needed to receive a block of KV pairs from Lightning.

- **`tikv_import_upload_chunk_bytes`** (Histogram)

    Bucketed histogram of the compressed size of a chunk of SST file uploaded to TiKV.

- **`tikv_import_upload_chunk_duration`** (Histogram)

    Bucketed histogram of the time needed to upload a chunk of SST file to TiKV.

- **`tikv_import_range_delivery_duration`** (Histogram)

    Bucketed histogram of the time needed to deliver a range of KV pairs into a `dispatch-job`.

- **`tikv_import_split_sst_duration`** (Histogram)

    Bucketed histogram of the time needed to split off a range from the engine file into a single SST file.

- **`tikv_import_sst_delivery_duration`** (Histogram)

    Bucketed histogram of the time needed to deliver an SST file from a `dispatch-job` to an `ImportSSTJob`.

- **`tikv_import_sst_recv_duration`** (Histogram)

    Bucketed histogram of the time needed to receive an SST file from a `dispatch-job` in an `ImportSSTJob`.

- **`tikv_import_sst_upload_duration`** (Histogram)

    Bucketed histogram of the time needed to upload an SST file from an `ImportSSTJob` to a TiKV node.

- **`tikv_import_sst_chunk_bytes`** (Histogram)

    Bucketed histogram of the compressed size of the SST file uploaded to a TiKV node.

- **`tikv_import_sst_ingest_duration`** (Histogram)

    Bucketed histogram of the time needed to ingest an SST file into TiKV.

- **`tikv_import_each_phase`** (Gauge)

    Indicates the running phase. Values can be 1, meaning running inside the phase, or 0, meaning outside the phase. Labels:

    - **phase**: `prepare` / `import`

- **`tikv_import_wait_store_available_count`** (Counter)

    Counts the number of times a TiKV node is found to have insufficient space when uploading SST files. Labels:

    - **store_id**: The TiKV store ID.

### `tidb-lightning`

Metrics provided by `tidb-lightning` are listed under the namespace `lightning_*`.

- **`lightning_importer_engine`** (Counter)

    Counting open and closed engine files. Labels:

    - **type**: `open` / `closed`

- **`lightning_idle_workers`** (Gauge)

    Counting idle workers. Values should be less than the `*-concurrency` settings and are typically zero. Labels:

    - **name**: `table` / `index` / `region` / `io` / `closed-engine`

- **`lightning_kv_encoder`** (Counter)

    Counting open and closed KV encoders. KV encoders are in-memory TiDB instances that convert SQL `INSERT` statements into KV pairs. The net values need to be bounded in a healthy situation. Labels:

    - **type**: `open` / `closed`

* **`lightning_tables`** (Counter)

    Counting number of tables processed and their status. Labels:

    - **state**: `pending` / `written` / `closed` / `imported` / `altered_auto_inc` / `checksum` / `analyzed` / `completed`
    - **result**: `success` / `failure`

* **`lightning_engines`** (Counter)

    Counting number of engine files processed and their status. Labels:

    - **state**: `pending` / `written` / `closed` / `imported` / `completed`
    - **result**: `success` / `failure`

- **`lightning_chunks`** (Counter)

    Counting number of chunks processed and their status. Labels:

    - **state**: `estimated` / `pending` / `running` / `finished` / `failed`

- **`lightning_import_seconds`** (Histogram)

    Bucketed histogram of the time needed to import a table.

- **`lightning_row_read_bytes`** (Histogram)

    Bucketed histogram of the size of a single SQL row.

- **`lightning_row_encode_seconds`** (Histogram)

    Bucketed histogram of the time needed to encode a single SQL row into KV pairs.

- **`lightning_row_kv_deliver_seconds`** (Histogram)

    Bucketed histogram of the time needed to deliver a set KV pairs corresponding to one single SQL row.

- **`lightning_block_deliver_seconds`** (Histogram)

    Bucketed histogram of the time needed to deliver of a block of KV pairs to Importer.

- **`lightning_block_deliver_bytes`** (Histogram)

    Bucketed histogram of the uncompressed size of a block of KV pairs delivered to Importer.

- **`lightning_chunk_parser_read_block_seconds`** (Histogram)

    Bucketed histogram of the time needed by the data file parser to read a block.

- **`lightning_checksum_seconds`** (Histogram)

    Bucketed histogram of the time taken to compute the checksum of a table.

- **`lightning_apply_worker_seconds`** (Histogram)

    Bucketed histogram of the time taken to acquire an idle worker. Labels:

    - **name**: `table` / `index` / `region` / `io` / `closed-engine`
