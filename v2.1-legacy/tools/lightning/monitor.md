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
pprof-port = 10089

...
```

You need to configure Prometheus to make it discover the `tidb-lightning` server. For instance, you can directly add the server address to the `scrape_configs` section:

```yaml
...
scrape_configs:
  - job_name: 'tidb-lightning'
    static_configs:
      - targets: ['192.168.20.10:10089']
```

## Monitoring metrics

This section explains the monitoring metrics of `tikv-importer` and `tidb-lightning`.

### `tikv-importer`

Metrics provided by `tikv-importer` are listed under the namespace `tikv_import_*`.

- **`tikv_import_rpc_duration`** (Histogram)

    Bucketed histogram of importing RPC duration. Labels:

    - **request**: RPC name, e.g. `open_engine`, `import_engine`, etc.
    - **result**: `ok` / `error`

- **`tikv_import_write_chunk_bytes`** (Histogram)

    Bucketed histogram of importing write chunk bytes.

- **`tikv_import_write_chunk_duration`** (Histogram)

    Bucketed histogram of importing write chunk duration.

- **`tikv_import_upload_chunk_bytes`** (Histogram)

    Bucketed histogram of importing upload chunk bytes.

- **`tikv_import_upload_chunk_duration`** (Histogram)

    Bucketed histogram of importing upload chunk duration.

### `tidb-lightning`

Metrics provided by `tidb-lightning` are listed under the namespace `lightning_*`.

- **`lightning_importer_engine`** (Counter)

    Counting open and closed engine files. Labels:

    - **type**: `open` / `closed`

- **`lightning_idle_workers`** (Gauge)

    Counting idle workers. Values should be less than the `*-concurrency` settings and are typically zero. Labels:

    - **name**: `table` / `region` / `io`

- **`lightning_kv_encoder`** (Counter)

    Counting open and closed KV encoders. KV encoders are in-memory TiDB instances that convert SQL `INSERT` statements into KV pairs. The net values need to be bounded in a healthy situation. Labels:

    - **type**: `open` / `closed`

* **`lightning_tables`** (Counter)

    Counting number of tables processed and their status. Labels:

    - **state**: `pending` / `written` / `closed` / `imported` / `altered_auto_inc` / `checksum` / `analyzed` / `completed`
    - **result**: `success` / `failure`

- **`lightning_chunks`** (Counter)

    Counting number of chunks processed and their status. Labels:

    - **state**: `estimated` / `pending` / `running` / `finished` / `failed`

- **`lightning_import_seconds`** (Histogram)

    Bucketed histogram of the time needed to import a table.

- **`lightning_block_read_seconds`** (Histogram)

    Bucketed histogram of the time needed to read a block of SQL rows from the data source.

- **`lightning_block_read_bytes`** (Histogram)

    Bucketed histogram of the size of a block of SQL rows.

- **`lightning_block_encode_seconds`** (Histogram)

    Bucketed histogram of the time needed to encode a block of SQL rows into KV pairs.

- **`lightning_block_deliver_seconds`** (Histogram)

    Bucketed histogram of the time needed to deliver a block of KV pairs.

- **`lightning_block_deliver_bytes`** (Histogram)

    Bucketed histogram of the size of a block of KV pairs.

- **`lightning_chunk_parser_read_block_seconds`** (Histogram)

    Bucketed histogram of the time needed by the data file parser to read a block.

- **`lightning_chunk_parser_read_row_seconds`** (Histogram)

    Bucketed histogram of the time needed by the data file parser to read a row.

- **`lightning_checksum_seconds`** (Histogram)

    Bucketed histogram of the time taken to compute the checksum of a table.

- **`lightning_apply_worker_seconds`** (Histogram)

    Bucketed histogram of the time taken to acquire an idle worker. Labels:

    - **name**: `table` / `region` / `io`
