---
title: TiCDC Server Configurations
summary: Learn the CLI and configuration parameters used in TiCDC.
---

# TiCDC Server Configurations

This document describes the CLI and configuration file parameters used in TiCDC.

## `cdc server` CLI parameters

The following are descriptions of options available in a `cdc server` command:

- `addr`: The listening address of TiCDC, the HTTP API address, and the Prometheus address of the TiCDC service. The default value is `127.0.0.1:8300`.
- `advertise-addr`: The advertised address via which clients access TiCDC. If unspecified, the value is the same as that of `addr`.
- `pd`: A comma-separated list of PD endpoints.
- `config`: The address of the configuration file that TiCDC uses (optional). This option is supported since TiCDC v5.0.0. This option can be used in the TiCDC deployment since TiUP v1.4.0. For detailed configuration description, see [TiCDC Changefeed Configurations](/ticdc/ticdc-changefeed-config.md)
- `data-dir`: Specifies the directory that TiCDC uses when it needs to use disks to store files. The sort engine used by TiCDC and redo logs use this directory to store temporary files. It is recommended to ensure that the free disk space for this directory is greater than or equal to 500 GiB. If you are using TiUP, you can configure `data_dir` in the [`cdc_servers`](/tiup/tiup-cluster-topology-reference.md#cdc_servers) section, or directly use the default `data_dir` path in `global`.
- `gc-ttl`: The TTL (Time To Live) of the service level `GC safepoint` in PD set by TiCDC, and the duration that the replication task can suspend, in seconds. The default value is `86400`, which means 24 hours. Note: Suspending of the TiCDC replication task affects the progress of TiCDC GC safepoint, which means that it affects the progress of upstream TiDB GC, as detailed in [Complete Behavior of TiCDC GC safepoint](/ticdc/ticdc-faq.md#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint).
- `log-file`: The path to which logs are output when the TiCDC process is running. If this parameter is not specified, logs are written to the standard output (stdout).
- `log-level`: The log level when the TiCDC process is running. The default value is `"info"`.
- `ca`: Specifies the path of the CA certificate file in PEM format for TLS connection (optional).
- `cert`: Specifies the path of the certificate file in PEM format for TLS connection (optional).
- `cert-allowed-cn`: Specifies the path of the common name in PEM format for TLS connection (optional).
- `key`: Specifies the path of the private key file in PEM format for TLS connection (optional).
- `tz`: Time zone used by the TiCDC service. TiCDC uses this time zone when it internally converts time data types such as `TIMESTAMP` or when it replicates data to the downstream. The default is the local time zone in which the process runs. If you specify `time-zone` (in `sink-uri`) and `tz` at the same time, the internal TiCDC processes use the time zone specified by `tz`, and the sink uses the time zone specified by `time-zone` for replicating data to the downstream. Make sure that the time zone specified by `tz` is the same as that specified by `time-zone` (in `sink-uri`).
- `cluster-id`: (optional) The ID of the TiCDC cluster. The default value is `default`. `cluster-id` is the unique identifier of a TiCDC cluster. TiCDC nodes with the same `cluster-id` belong to the same cluster. The length of a `cluster-id` is 128 characters at most. `cluster-id` must follow the pattern of `^[a-zA-Z0-9]+(-[a-zA-Z0-9]+)*$` and cannot be one of the following: `owner`, `capture`, `task`, `changefeed`, `job`, and `meta`.

## `cdc server` configuration file parameters

The following describes the configuration file specified by the `config` option in the `cdc server` command:

```toml
# The configuration method of the following parameters is the same as that of CLI parameters, but the CLI parameters have higher priorities.
addr = "127.0.0.1:8300"
advertise-addr = ""
log-file = ""
log-level = "info"
data-dir = ""
gc-ttl = 86400 # 24 h
tz = "System"
cluster-id = "default"

[security]
  ca-path = ""
  cert-path = ""
  key-path = ""

# The session duration between TiCDC and etcd services, measured in seconds. This parameter is optional and its default value is 10.
capture-session-ttl = 10 # 10s

# The interval at which the Owner module in the TiCDC cluster attempts to push the replication progress. This parameter is optional and its default value is `50000000` nanoseconds (that is, 50 milliseconds). You can configure this parameter in two ways: specifying only the number (for example, configuring it as `40000000` represents 40000000 nanoseconds, which is 40 milliseconds), or specifying both the number and unit (for example, directly configuring it as `40ms`).
owner-flush-interval = 50000000 # 50 ms

# The interval at which the Processor module in the TiCDC cluster attempts to push the replication progress. This parameter is optional and its default value is `50000000` nanoseconds (that is, 50 milliseconds). The configuration method of this parameter is the same as that of `owner-flush-interval`.
processor-flush-interval = 50000000 # 50 ms

# [log]
# # The output location for internal error logs of the zap log module. This parameter is optional and its default value is "stderr".
#   error-output = "stderr"
#   [log.file]
#     # The maximum size of a single log file, measured in MiB. This parameter is optional and its default value is 300.
#     max-size = 300 # 300 MiB
#     # The maximum number of days to retain log files. This parameter is optional and its default value is `0`, indicating never to delete.
#     max-days = 0
#     # The number of log files to retain. This parameter is optional and its default value is `0`, indicating to keep all log files.
#     max-backups = 0

#[sorter]
# The size of the shared pebble block cache in the Sorter module for the 8 pebble DBs started by default, measured in MiB. The default value is 128.
# cache-size-in-mb = 128
# The directory where sorter files are stored relative to the data directory (`data-dir`). This parameter is optional and its default value is "/tmp/sorter".
# sorter-dir = "/tmp/sorter"

# [kv-client]
#   The number of threads that can be used in a single Region worker. This parameter is optional and its default value is 8.
#   worker-concurrent = 8
#   The number of threads in the shared thread pool of TiCDC, mainly used for processing KV events. This parameter is optional and its default value is 0, indicating that the default pool size is twice the number of CPU cores.
#   worker-pool-size = 0
#   The retry duration of Region connections. This parameter is optional and its default value is `60000000000` nanoseconds (that is, 1 minute). You can configure this parameter in two ways: specifying only the number (for example, configuring it as `50000000` represents 50000000 nanoseconds, which is 50 milliseconds), or specifying both the number and unit (for example, directly configuring it as `50ms`).
#   region-retry-duration = 60000000000
```
