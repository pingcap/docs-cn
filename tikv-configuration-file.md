---
title: TiKV Configuration File
summary: Learn the TiKV configuration file.
aliases: ['/docs/dev/tikv-configuration-file/','/docs/dev/reference/configuration/tikv-server/configuration-file/']
---

# TiKV Configuration File

<!-- markdownlint-disable MD001 -->

The TiKV configuration file supports more options than command-line parameters. You can find the default configuration file in [etc/config-template.toml](https://github.com/tikv/tikv/blob/master/etc/config-template.toml) and rename it to `config.toml`.

This document only describes the parameters that are not included in command-line parameters. For more details, see [command-line parameter](/command-line-flags-for-tikv-configuration.md).

## Global configuration

### `abort-on-panic`

+ Sets whether to call `abort()` to exit the process when TiKV panics. This option affects whether TiKV allows the system to generate core dump files.

    + If the value of this configuration item is `false`, when TiKV panics, it calls `exit()` to exit the process.
    + If the value of this configuration item is `true`, when TiKV panics, TiKV calls `abort()` to exit the process. At this time, TiKV allows the system to generate core dump files when exiting. To generate the core dump file, you also need to perform the system configuration related to core dump (for example, setting the size limit of the core dump file via `ulimit -c` command, and configure the core dump path. Different operating systems have different related configurations). To avoid the core dump files occupying too much disk space and causing insufficient TiKV disk space, it is recommended to set the core dump generation path to a disk partition different to that of TiKV data.

+ Default value: `false`

### `slow-log-file`

+ The file that stores slow logs
+ If this configuration item is not set, but `log.file.filename` is set, slow logs are output to the log file specified by `log.file.filename`.
+ If neither `slow-log-file` nor `log.file.filename` are set, all logs are output to "stderr" by default.
+ If both configuration items are set, ordinary logs are output to the log file specified by `log.file.filename`, and slow logs are output to the log file set by `slow-log-file`.
+ Default value: `""`

### `slow-log-threshold`

+ The threshold for outputing slow logs. If the processing time is longer than this threshold, slow logs are output.
+ Default value: `"1s"`

### `memory-usage-limit`

+ The limit on memory usage of the TiKV instance. When the memory usage of TiKV almost reaches this threshold, internal cache will be evicted to release memory.
+ In most cases, the TiKV instance is set to use 75% of the total available system memory, so you do not need to explicitly specify this configuration item. The rest 25% of the memory is reserved for the OS page cache. See [`storage.block-cache.capacity`](#capacity) for details.
+ When deploying multiple TiKV nodes on a single physical machine, you still do not need to set this configuration item. In this case, the TiKV instance uses `5/3 * block-cache.capacity` of memory.
+ The default value for different system memory capacity is as follows:

    + system=8G    block-cache=3.6G    memory-usage-limit=6G   page-cache=2G
    + system=16G   block-cache=7.2G    memory-usage-limit=12G  page-cache=4G
    + system=32G   block-cache=14.4G   memory-usage-limit=24G  page-cache=8G

## log <span class="version-mark">New in v5.4.0</span>

+ Configuration items related to the log.

+ From v5.4.0, to make the log configuration items of TiKV and TiDB consistent, TiKV deprecates the former configuration item `log-rotation-timespan` and changes `log-level`, `log-format`, `log-file`, `log-rotation-size` to the following ones. If you only set the old configuration items, and their values are set to non-default values, the old items remain compatible with the new items. If both old and new configuration items are set, the new items take effect.

### `level` <span class="version-mark">New in v5.4.0</span>

+ The log level
+ Optional values: `"debug"`, `"info"`, `"warn"`, `"error"`, `"fatal"`
+ Default value: `"info"`

### `format` <span class="version-mark">New in v5.4.0</span>

+ The log format
+ Optional values: `"json"`, `"text"`
+ Default value: `"text"`

### `enable-timestamp` <span class="version-mark">New in v5.4.0</span>

+ Determines whether to enable or disable the timestamp in the log
+ Optional values: `true`, `false`
+ Default value: `true`

## log.file <span class="version-mark">New in v5.4.0</span>

+ Configuration items related to the log file.

### `filename` <span class="version-mark">New in v5.4.0</span>

+ The log file. If this configuration item is not set, logs are output to "stderr" by default. If this configuration item is set, logs are output to the corresponding file.
+ Default value: `""`

### `max-size` <span class="version-mark">New in v5.4.0</span>

+ The maximum size of a single log file. When the file size is larger than the value set by this configuration item, the system automatically splits the single file into multiple files.
+ Default value: `300`
+ Maximum value: `4096`
+ Unit: MiB

### `max-days` <span class="version-mark">New in v5.4.0</span>

+ The maximum number of days that TiKV keeps log files.
    + If the configuration item is not set, or the value of it is set to the default value `0`, TiKV does not clean log files.
    + If the parameter is set to a value other than `0`, TiKV cleans up the expired log files after `max-days`.
+ Default value: `0`

### `max-backups` <span class="version-mark">New in v5.4.0</span>

+ The maximum number of log files that TiKV keeps.
    + If the configuration item is not set, or the value of it is set to the default value `0`, TiKV keeps all log files.
    + If the configuration item is set to a value other than `0`, TiKV keeps at most the number of old log files specified by `max-backups`. For example, if the value is set to `7`, TiKV keeps up to 7 old log files.
+ Default value: `0`

### `pd.enable-forwarding` <span class="version-mark">New in v5.0.0</span>

+ Controls whether the PD client in TiKV forwards requests to the leader via the followers in the case of possible network isolation.
+ Default value: `false`
+ If the environment might have isolated network, enabling this parameter can reduce the window of service unavailability.
+ If you cannot accurately determine whether isolation, network interruption, or downtime has occurred, using this mechanism has the risk of misjudgment and causes reduced availability and performance. If network failure has never occurred, it is not recommended to enable this parameter.

## server

+ Configuration items related to the server.

### `addr`

+ The listening IP address and the listening port
+ Default value: `"127.0.0.1:20160"`

### `advertise-addr`

+ Advertise the listening address for client communication
+ If this configuration item is not set, the value of `addr` is used.
+ Default value: `""`

### `status-addr`

+ The configuration item reports TiKV status directly through the `HTTP` address

    > **Warning:**
    >
    > If this value is exposed to the public, the status information of the TiKV server might be leaked.

+ To disable the status address, set the value to `""`.
+ Default value: `"127.0.0.1:20180"`

### `status-thread-pool-size`

+ The number of worker threads for the `HTTP` API service
+ Default value: `1`
+ Minimum value: `1`

### `grpc-compression-type`

+ The compression algorithm for gRPC messages
+ Optional values: `"none"`, `"deflate"`, `"gzip"`
+ Default value: `"none"`
+ Note: When the value is `gzip`, TiDB Dashboard will have a display error because it might not complete the corresponding compression algorithm in some cases. If you adjust the value back to the default `none`, TiDB Dashboard will display normally.

### `grpc-concurrency`

+ The number of gRPC worker threads. When you modify the size of the gRPC thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools).
+ Default value: `5`
+ Minimum value: `1`

### `grpc-concurrent-stream`

+ The maximum number of concurrent requests allowed in a gRPC stream
+ Default value: `1024`
+ Minimum value: `1`

### `grpc-memory-pool-quota`

+ Limits the memory size that can be used by gRPC
+ Default value: No limit
+ Limit the memory in case OOM is observed. Note that limit the usage can lead to potential stall

### `grpc-raft-conn-num`

+ The maximum number of links among TiKV nodes for Raft communication
+ Default value: `1`
+ Minimum value: `1`

### `max-grpc-send-msg-len`

+ Sets the maximum length of a gRPC message that can be sent
+ Default value: `10485760`
+ Unit: Bytes
+ Maximum value: `2147483647`

### `grpc-stream-initial-window-size`

+ The window size of the gRPC stream
+ Default value: `2MB`
+ Unit: KB|MB|GB
+ Minimum value: `"1KB"`

### `grpc-keepalive-time`

+ The time interval at which that gRPC sends `keepalive` Ping messages
+ Default value: `"10s"`
+ Minimum value: `"1s"`

### `grpc-keepalive-timeout`

+ Disables the timeout for gRPC streams
+ Default value: `"3s"`
+ Minimum value: `"1s"`

### `concurrent-send-snap-limit`

+ The maximum number of snapshots sent at the same time
+ Default value: `32`
+ Minimum value: `1`

### `concurrent-recv-snap-limit`

+ The maximum number of snapshots received at the same time
+ Default value: `32`
+ Minimum value: `1`

### `end-point-recursion-limit`

+ The maximum number of recursive levels allowed when TiKV decodes the Coprocessor DAG expression
+ Default value: `1000`
+ Minimum value: `1`

### `end-point-request-max-handle-duration`

+ The longest duration allowed for a TiDB's push down request to TiKV for processing tasks
+ Default value: `"60s"`
+ Minimum value: `"1s"`

### `snap-max-write-bytes-per-sec`

+ The maximum allowable disk bandwidth when processing snapshots
+ Default value: `"100MB"`
+ Unit: KB|MB|GB
+ Minimum value: `"1KB"`

### `enable-request-batch`

+ Determines whether to process requests in batches
+ Default value: `true`

### `labels`

+ Specifies server attributes, such as `{ zone = "us-west-1", disk = "ssd" }`.
+ Default value: `{}`

### `background-thread-count`

+ The working thread count of the background pool, including endpoint threads, BR threads, split-check threads, Region threads, and other threads of delay-insensitive tasks.
+ Default value: when the number of CPU cores is less than 16, the default value is `2`; otherwise, the default value is `3`.

### `end-point-slow-log-threshold`

+ The time threshold for a TiDB's push-down request to output slow log. If the processing time is longer than this threshold, the slow logs are output.
+ Default value: `"1s"`
+ Minimum value: `0`

### `raft-client-queue-size`

+ Specifies the queue size of the Raft messages in TiKV. If too many messages not sent in time result in a full buffer, or messages discarded, you can specify a greater value to improve system stability.
+ Default value: `8192`

### `simplify-metrics` <span class="version-mark">New in v6.2.0</span>

+ Specifies whether to simplify the returned monitoring metrics. After you set the value to `true`, TiKV reduces the amount of data returned for each request by filtering out some metrics.
+ Default value: `false`

### `forward-max-connections-per-address` <span class="version-mark">New in v5.0.0</span>

+ Sets the size of the connection pool for service and forwarding requests to the server. Setting it to too small a value affects the request latency and load balancing.
+ Default value: `4`

## readpool.unified

Configuration items related to the single thread pool serving read requests. This thread pool supersedes the original storage thread pool and coprocessor thread pool since the 4.0 version.

### `min-thread-count`

+ The minimal working thread count of the unified read pool
+ Default value: `1`

### `max-thread-count`

+ The maximum working thread count of the unified read pool or the UnifyReadPool thread pool. When you modify the size of this thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools).
+ Value range: `[min-thread-count, MAX(4, CPU)]`. In `MAX(4, CPU)`, `CPU` means the number of your CPU cores. `MAX(4, CPU)` takes the greater value out of `4` and the `CPU`.
+ Default value: MAX(4, CPU * 0.8)

### `stack-size`

+ The stack size of the threads in the unified thread pool
+ Type: Integer + Unit
+ Default value: `"10MB"`
+ Unit: KB|MB|GB
+ Minimum value: `"2MB"`
+ Maximum value: The number of Kbytes output in the result of the `ulimit -sH` command executed in the system.

### `max-tasks-per-worker`

+ The maximum number of tasks allowed for a single thread in the unified read pool. `Server Is Busy` is returned when the value is exceeded.
+ Default value: `2000`
+ Minimum value: `2`

### `auto-adjust-pool-size` <span class="version-mark">New in v6.3.0</span>

+ Controls whether to automatically adjust the thread pool size. When it is enabled, the read performance of TiKV is optimized by automatically adjusting the UnifyReadPool thread pool size based on the current CPU usage. The possible range of the thread pool is `[max-thread-count, MAX(4, CPU)]`. The maximum value is the same as the one of [`max-thread-count`](#max-thread-count).
+ Default value: `false`

## readpool.storage

Configuration items related to storage thread pool.

### `use-unified-pool`

+ Determines whether to use the unified thread pool (configured in [`readpool.unified`](#readpoolunified)) for storage requests. If the value of this parameter is `false`, a separate thread pool is used, which is configured through the rest parameters in this section (`readpool.storage`).
+ Default value: If this section (`readpool.storage`) has no other configurations, the default value is `true`. Otherwise, for the backward compatibility, the default value is `false`. Change the configuration in [`readpool.unified`](#readpoolunified) as needed before enabling this option.

### `high-concurrency`

+ The allowable number of concurrent threads that handle high-priority `read` requests
+ When `8` ≤ `cpu num` ≤ `16`, the default value is `cpu_num * 0.5`; when `cpu num` is smaller than `8`, the default value is `4`; when `cpu num` is greater than `16`, the default value is `8`.
+ Minimum value: `1`

### `normal-concurrency`

+ The allowable number of concurrent threads that handle normal-priority `read` requests
+ When `8` ≤ `cpu num` ≤ `16`, the default value is `cpu_num * 0.5`; when `cpu num` is smaller than `8`, the default value is `4`; when `cpu num` is greater than `16`, the default value is `8`.
+ Minimum value: `1`

### `low-concurrency`

+ The allowable number of concurrent threads that handle low-priority `read` requests
+ When `8` ≤ `cpu num` ≤ `16`, the default value is `cpu_num * 0.5`; when `cpu num` is smaller than `8`, the default value is `4`; when `cpu num` is greater than `16`, the default value is `8`.
+ Minimum value: `1`

### `max-tasks-per-worker-high`

+ The maximum number of tasks allowed for a single thread in a high-priority thread pool. `Server Is Busy` is returned when the value is exceeded.
+ Default value: `2000`
+ Minimum value: `2`

### `max-tasks-per-worker-normal`

+ The maximum number of tasks allowed for a single thread in a normal-priority thread pool. `Server Is Busy` is returned when the value is exceeded.
+ Default value: `2000`
+ Minimum value: `2`

### `max-tasks-per-worker-low`

+ The maximum number of tasks allowed for a single thread in a low-priority thread pool. `Server Is Busy` is returned when the value is exceeded.
+ Default value: `2000`
+ Minimum value: `2`

### `stack-size`

+ The stack size of threads in the Storage read thread pool
+ Type: Integer + Unit
+ Default value: `"10MB"`
+ Unit: KB|MB|GB
+ Minimum value: `"2MB"`
+ Maximum value: The number of Kbytes output in the result of the `ulimit -sH` command executed in the system.

## `readpool.coprocessor`

Configuration items related to the Coprocessor thread pool.

### `use-unified-pool`

+ Determines whether to use the unified thread pool (configured in [`readpool.unified`](#readpoolunified)) for coprocessor requests. If the value of this parameter is `false`, a separate thread pool is used, which is configured through the rest parameters in this section (`readpool.coprocessor`).
+ Default value: If none of the parameters in this section (`readpool.coprocessor`) are set, the default value is `true`. Otherwise, the default value is `false` for the backward compatibility. Adjust the configuration items in [`readpool.unified`](#readpoolunified) before enabling this parameter.

### `high-concurrency`

+ The allowable number of concurrent threads that handle high-priority Coprocessor requests, such as checkpoints
+ Default value: `CPU * 0.8`
+ Minimum value: `1`

### `normal-concurrency`

+ The allowable number of concurrent threads that handle normal-priority Coprocessor requests
+ Default value: `CPU * 0.8`
+ Minimum value: `1`

### `low-concurrency`

+ The allowable number of concurrent threads that handle low-priority Coprocessor requests, such as table scan
+ Default value: `CPU * 0.8`
+ Minimum value: `1`

### `max-tasks-per-worker-high`

+ The number of tasks allowed for a single thread in a high-priority thread pool. When this number is exceeded, `Server Is Busy` is returned.
+ Default value: `2000`
+ Minimum value: `2`

### `max-tasks-per-worker-normal`

+ The number of tasks allowed for a single thread in a normal-priority thread pool. When this number is exceeded, `Server Is Busy` is returned.
+ Default value: `2000`
+ Minimum value: `2`

### `max-tasks-per-worker-low`

+ The number of tasks allowed for a single thread in a low-priority thread pool. When this number is exceeded, `Server Is Busy` is returned.
+ Default value: `2000`
+ Minimum value: `2`

### `stack-size`

+ The stack size of the thread in the Coprocessor thread pool
+ Type: Integer + Unit
+ Default value: `"10MB"`
+ Unit: KB|MB|GB
+ Minimum value: `"2MB"`
+ Maximum value: The number of Kbytes output in the result of the `ulimit -sH` command executed in the system.

## storage

Configuration items related to storage.

### `data-dir`

+ The storage path of the RocksDB directory
+ Default value: `"./"`

### `scheduler-concurrency`

+ A built-in memory lock mechanism to prevent simultaneous operations on a key. Each key has a hash in a different slot.
+ Default value: `524288`
+ Minimum value: `1`

### `scheduler-worker-pool-size`

+ The number of threads in the Scheduler thread pool. Scheduler threads are mainly used for checking transaction consistency before data writing. If the number of CPU cores is greater than or equal to `16`, the default value is `8`; otherwise, the default value is `4`. When you modify the size of the Scheduler thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools).
+ Default value: `4`
+ Value range: `[1, MAX(4, CPU)]`. In `MAX(4, CPU)`, `CPU` means the number of your CPU cores. `MAX(4, CPU)` takes the greater value out of `4` and the `CPU`.

### `scheduler-pending-write-threshold`

+ The maximum size of the write queue. A `Server Is Busy` error is returned for a new write to TiKV when this value is exceeded.
+ Default value: `"100MB"`
+ Unit: MB|GB

### `enable-async-apply-prewrite`

+ Determines whether Async Commit transactions respond to the TiKV client before applying prewrite requests. After enabling this configuration item, latency can be easily reduced when the apply duration is high, or the delay jitter can be reduced when the apply duration is not stable.
+ Default value: `false`

### `reserve-space`

+ When TiKV is started, some space is reserved on the disk as disk protection. When the remaining disk space is less than the reserved space, TiKV restricts some write operations. The reserved space is divided into two parts: 80% of the reserved space is used as the extra disk space required for operations when the disk space is insufficient, and the other 20% is used to store the temporary file. In the process of reclaiming space, if the storage is exhausted by using too much extra disk space, this temporary file serves as the last protection for restoring services.
+ The name of the temporary file is `space_placeholder_file`, located in the `storage.data-dir` directory. When TiKV goes offline because its disk space ran out, if you restart TiKV, the temporary file is automatically deleted and TiKV tries to reclaim the space.
+ When the remaining space is insufficient, TiKV does not create the temporary file. The effectiveness of the protection is related to the size of the reserved space. The size of the reserved space is the larger value between 5% of the disk capacity and this configuration value. When the value of this configuration item is `"0MB"`, TiKV disables this disk protection feature.
+ Default value: `"5GB"`
+ Unit: MB|GB

### `enable-ttl`

> **Warning:**
>
> - Set `enable-ttl` to `true` or `false` **ONLY WHEN** deploying a new TiKV cluster. **DO NOT** modify the value of this configuration item in an existing TiKV cluster. TiKV clusters with different `enable-ttl` values use different data formats. Therefore, if you modify the value of this item in an existing TiKV cluster, the cluster will store data in different formats, which causes the "can't enable TTL on a non-ttl" error when you restart the TiKV cluster.
> - Use `enable-ttl` **ONLY IN** a TiKV cluster. **DO NOT** use this configuration item in a cluster that has TiDB nodes (which means setting `enable-ttl` to `true` in such clusters). Otherwise, critical issues such as data corruption and the upgrade failure of TiDB clusters will occur.

+ TTL is short for "Time to live". If this item is enabled, TiKV automatically deletes data that reaches its TTL. To set the value of TTL, you need to specify it in the requests when writing data via the client. If the TTL is not specified, it means that TiKV does not automatically delete the corresponding data.
+ Default value: `false`

### `ttl-check-poll-interval`

+ The interval of checking data to reclaim physical spaces. If data reaches its TTL, TiKV forcibly reclaims its physical space during the check.
+ Default value: `"12h"`
+ Minimum value: `"0s"`

### `background-error-recovery-window` <span class="version-mark">New in v6.1.0</span>

+ The maximum allowable time for TiKV to recover after RocksDB detects a recoverable background error. If some background SST files are damaged, RocksDB will report to PD via heartbeat after locating the Peer to which the damaged SST files belong. PD then performs scheduling operations to remove this Peer. Finally, the damaged SST files are deleted directly, and the TiKV background will work as normal again.
+ The damaged SST files still exist before the recovery finishes. During such a period, RocksDB can continue writing data, but an error will be reported when the damaged part of the data is read.
+ If the recovery fails to finish within this time window, TiKV will panic.
+ Default value: 1h

### `api-version` <span class="version-mark">New in v6.1.0</span>

+ The storage format and interface version used by TiKV when TiKV serves as the RawKV store.
+ Value options:
    + `1`: Uses API V1, does not encode the data passed from the client, and stores data as it is. In versions earlier than v6.1.0, TiKV uses API V1 by default.
    + `2`: Uses API V2:
        + The data is stored in the Multi-Version Concurrency Control (MVCC) format, where the timestamp is obtained from PD (which is TSO) by tikv-server.
        + Data is scoped according to different usage and API V2 supports co-existence of TiDB, Transactional KV, and RawKV applications in a single cluster.
        + When API V2 is used, you are expected to set `storage.enable-ttl = true` at the same time. Because API V2 supports the TTL feature, you must turn on `enable-ttl` explicitly. Otherwise, it will be in conflict because `storage.enable-ttl` defaults to `false`.
        + When API V2 is enabled, you need to deploy at least one tidb-server instance to reclaim obsolete data. This tidb-server instance can provide read and write services at the same time. To ensure high availability, you can deploy multiple tidb-server instances.
        + Client support is required for API V2. For details, see the corresponding instruction of the client for the API V2.
        + Since v6.2.0, Change Data Capture (CDC) for RawKV is supported. Refer to [RawKV CDC](https://tikv.org/docs/latest/concepts/explore-tikv-features/cdc/cdc).
+ Default value: `1`

> **Warning:**

> - API V1 and API V2 are different from each other in the storage format. You can enable or disable API V2 directly **only** when TiKV contains only TiDB data. In other scenarios, you need to deploy a new cluster, and migrate data using [RawKV Backup & Restore](https://tikv.org/docs/latest/concepts/explore-tikv-features/backup-restore/).
> - After API V2 is enabled, you **cannot** downgrade the TiKV cluster to a version earlier than v6.1.0. Otherwise, data corruption might occur.

## storage.block-cache

Configuration items related to the sharing of block cache among multiple RocksDB Column Families (CF). When these configuration items are enabled, block cache separately configured for each column family is disabled.

### `shared`

+ Enables or disables the sharing of block cache.
+ Default value: `true`

### `capacity`

+ The size of the shared block cache.
+ Default value: 45% of the size of total system memory
+ Unit: KB|MB|GB

## storage.flow-control

Configuration items related to the flow control mechanism in TiKV. This mechanism replaces the write stall mechanism in RocksDB and controls flow at the scheduler layer, which avoids secondary disasters caused by the stuck Raftstore or Apply threads.

### `enable`

+ Determines whether to enable the flow control mechanism. After it is enabled, TiKV automatically disables the write stall mechanism of KvDB and the write stall mechanism of RaftDB (excluding memtable).
+ Default value: `true`

### `memtables-threshold`

+ When the number of kvDB memtables reaches this threshold, the flow control mechanism starts to work. When `enable` is set to `true`, this configuration item overrides `rocksdb.(defaultcf|writecf|lockcf).max-write-buffer-number`.
+ Default value: `5`

### `l0-files-threshold`

+ When the number of kvDB L0 files reaches this threshold, the flow control mechanism starts to work. When `enable` is set to `true`, this configuration item overrides `rocksdb.(defaultcf|writecf|lockcf).level0-slowdown-writes-trigger`.
+ Default value: `20`

### `soft-pending-compaction-bytes-limit`

+ When the pending compaction bytes in KvDB reach this threshold, the flow control mechanism starts to reject some write requests and reports the `ServerIsBusy` error. When `enable` is set to `true`, this configuration item overrides `rocksdb.(defaultcf|writecf|lockcf).soft-pending-compaction-bytes-limit`.
+ Default value: `"192GB"`

### `hard-pending-compaction-bytes-limit`

+ When the pending compaction bytes in KvDB reach this threshold, the flow control mechanism rejects all write requests and reports the `ServerIsBusy` error. When `enable` is set to `true`, this configuration item overrides `rocksdb.(defaultcf|writecf|lockcf).hard-pending-compaction-bytes-limit`.
+ Default value: `"1024GB"`

## storage.io-rate-limit

Configuration items related to the I/O rate limiter.

### `max-bytes-per-sec`

+ Limits the maximum I/O bytes that a server can write to or read from the disk (determined by the `mode` configuration item below) in one second. When this limit is reached, TiKV prefers throttling background operations over foreground ones. The value of this configuration item should be set to the disk's optimal I/O bandwidth, for example, the maximum I/O bandwidth specified by your cloud disk vendor. When this configuration value is set to zero, disk I/O operations are not limited.
+ Default value: `"0MB"`

### `mode`

+ Determines which types of I/O operations are counted and restrained below the `max-bytes-per-sec` threshold. Currently, only the write-only mode is supported.
+ Value options: `"read-only"`, `"write-only"`, and `"all-io"`
+ Default value: `"write-only"`

## pd

### `endpoints`

+ The endpoints of PD. When multiple endpoints are specified, you need to separate them using commas.
+ Default value: `["127.0.0.1:2379"]`

### `retry-interval`

+ The interval for retrying to initialize the PD connection
+ Default value: `"300ms"`

### `retry-log-every`

+ Specified the frequency at which the PD client skips reporting errors when the client observes errors. For example, when the value is `5`, after the PD client observes errors, the client skips reporting errors every 4 times and reports errors every 5th time.
+ To disable this feature, set the value to `1`.
+ Default value: `10`

### `retry-max-count`

+ The maximum number of times to retry to initialize PD connection
+ To disable the retry, set its value to `0`. To release the limit on the number of retries, set the value to `-1`.
+ Default value: `-1`

## raftstore

Configuration items related to Raftstore.

### `prevote`

+ Enables or disables `prevote`. Enabling this feature helps reduce jitter on the system after recovery from network partition.
+ Default value: `true`

### `capacity`

+ The storage capacity, which is the maximum size allowed to store data. If `capacity` is left unspecified, the capacity of the current disk prevails. To deploy multiple TiKV instances on the same physical disk, add this parameter to the TiKV configuration. For details, see [Key parameters of the hybrid deployment](/hybrid-deployment-topology.md#key-parameters).
+ Default value: `0`
+ Unit: KB|MB|GB

### `raftdb-path`

+ The path to the Raft library, which is `storage.data-dir/raft` by default
+ Default value: `""`

### `raft-base-tick-interval`

> **Note:**
>
> This configuration item cannot be queried via SQL statements but can be configured in the configuration file.

+ The time interval at which the Raft state machine ticks
+ Default value: `"1s"`
+ Minimum value: greater than `0`

### `raft-heartbeat-ticks`

> **Note:**
>
> This configuration item cannot be queried via SQL statements but can be configured in the configuration file.

+ The number of passed ticks when the heartbeat is sent. This means that a heartbeat is sent at the time interval of `raft-base-tick-interval` * `raft-heartbeat-ticks`.
+ Default value: `2`
+ Minimum value: greater than `0`

### `raft-election-timeout-ticks`

> **Note:**
>
> This configuration item cannot be queried via SQL statements but can be configured in the configuration file.

+ The number of passed ticks when Raft election is initiated. This means that if Raft group is missing the leader, a leader election is initiated approximately after the time interval of `raft-base-tick-interval` * `raft-election-timeout-ticks`.
+ Default value: `10`
+ Minimum value: `raft-heartbeat-ticks`

### `raft-min-election-timeout-ticks`

> **Note:**
>
> This configuration item cannot be queried via SQL statements but can be configured in the configuration file.

+ The minimum number of ticks during which the Raft election is initiated. If the number is `0`, the value of `raft-election-timeout-ticks` is used. The value of this parameter must be greater than or equal to `raft-election-timeout-ticks`.
+ Default value: `0`
+ Minimum value: `0`

### `raft-max-election-timeout-ticks`

> **Note:**
>
> This configuration item cannot be queried via SQL statements but can be configured in the configuration file.

+ The maximum number of ticks during which the Raft election is initiated. If the number is `0`, the value of `raft-election-timeout-ticks` * `2` is used.
+ Default value: `0`
+ Minimum value: `0`

### `raft-max-size-per-msg`

> **Note:**
>
> This configuration item cannot be queried via SQL statements but can be configured in the configuration file.

+ The soft limit on the size of a single message packet
+ Default value: `"1MB"`
+ Minimum value: greater than `0`
+ Maximum value: `3GB`
+ Unit: KB|MB|GB

### `raft-max-inflight-msgs`

> **Note:**
>
> This configuration item cannot be queried via SQL statements but can be configured in the configuration file.

+ The number of Raft logs to be confirmed. If this number is exceeded, the Raft state machine slows down log sending.
+ Default value: `256`
+ Minimum value: greater than `0`
+ Maximum value: `16384`

### `raft-entry-max-size`

+ The hard limit on the maximum size of a single log
+ Default value: `"8MB"`
+ Minimum value: `0`
+ Unit: MB|GB

### `raft-log-compact-sync-interval` <span class="version-mark">New in v5.3</span>

+ The time interval to compact unnecessary Raft logs
+ Default value: `"2s"`
+ Minimum value: `"0s"`

### `raft-log-gc-tick-interval`

+ The time interval at which the polling task of deleting Raft logs is scheduled. `0` means that this feature is disabled.
+ Default value: `"3s"`
+ Minimum value: `"0s"`

### `raft-log-gc-threshold`

+ The soft limit on the maximum allowable count of residual Raft logs
+ Default value: `50`
+ Minimum value: `1`

### `raft-log-gc-count-limit`

+ The hard limit on the allowable number of residual Raft logs
+ Default value: the log number that can be accommodated in the 3/4 Region size (calculated as 1MB for each log)
+ Minimum value: `0`

### `raft-log-gc-size-limit`

+ The hard limit on the allowable size of residual Raft logs
+ Default value: 3/4 of the Region size
+ Minimum value: greater than `0`

### `raft-log-reserve-max-ticks` <span class="version-mark">New in v5.3</span>

+ After the number of ticks set by this configuration item passes, even if the number of residual Raft logs does not reach the value set by `raft-log-gc-threshold`, TiKV still performs garbage collection (GC) to these logs.
+ Default value: `6`
+ Minimum value: greater than `0`

### `raft-engine-purge-interval`

+ The interval for purging old TiKV log files to recycle disk space as soon as possible. Raft engine is a replaceable component, so the purging process is needed for some implementations.
+ Default value: `"10s"`

### `raft-entry-cache-life-time`

+ The maximum remaining time allowed for the log cache in memory
+ Default value: `"30s"`
+ Minimum value: `0`

### `hibernate-regions`

+ Enables or disables Hibernate Region. When this option is enabled, a Region idle for a long time is automatically set as hibernated. This reduces the extra overhead caused by heartbeat messages between the Raft leader and the followers for idle Regions. You can use `peer-stale-state-check-interval` to modify the heartbeat interval between the leader and the followers of hibernated Regions.
+ Default value: `true` in v5.0.2 and later versions; `false` in versions before v5.0.2

### `split-region-check-tick-interval`

+ Specifies the interval at which to check whether the Region split is needed. `0` means that this feature is disabled.
+ Default value: `"10s"`
+ Minimum value: `0`

### `region-split-check-diff`

+ The maximum value by which the Region data is allowed to exceed before Region split
+ Default value: 1/16 of the Region size.
+ Minimum value: `0`

### `region-compact-check-interval`

+ The time interval at which to check whether it is necessary to manually trigger RocksDB compaction. `0` means that this feature is disabled.
+ Default value: `"5m"`
+ Minimum value: `0`

### `region-compact-check-step`

+ The number of Regions checked at one time for each round of manual compaction
+ Default value: `100`
+ Minimum value: `0`

### `region-compact-min-tombstones`

+ The number of tombstones required to trigger RocksDB compaction
+ Default value: `10000`
+ Minimum value: `0`

### `region-compact-tombstones-percent`

+ The proportion of tombstone required to trigger RocksDB compaction
+ Default value: `30`
+ Minimum value: `1`
+ Maximum value: `100`

### `pd-heartbeat-tick-interval`

+ The time interval at which a Region's heartbeat to PD is triggered. `0` means that this feature is disabled.
+ Default value: `"1m"`
+ Minimum value: `0`

### `pd-store-heartbeat-tick-interval`

+ The time interval at which a store's heartbeat to PD is triggered. `0` means that this feature is disabled.
+ Default value: `"10s"`
+ Minimum value: `0`

### `snap-mgr-gc-tick-interval`

+ The time interval at which the recycle of expired snapshot files is triggered. `0` means that this feature is disabled.
+ Default value: `"1m"`
+ Minimum value: `0`

### `snap-gc-timeout`

+ The longest time for which a snapshot file is saved
+ Default value: `"4h"`
+ Minimum value: `0`

### `snap-generator-pool-size` <span class="version-mark">New in v5.4.0</span>

+ Configures the size of the `snap-generator` thread pool.
+ To make Regions generate snapshot faster in TiKV in recovery scenarios, you need to increase the count of the `snap-generator` threads of the corresponding worker. You can use this configuration item to increase the size of the `snap-generator` thread pool.
+ Default value: `2`
+ Minimum value: `1`

### `lock-cf-compact-interval`

+ The time interval at which TiKV triggers a manual compaction for the Lock Column Family
+ Default value: `"256MB"`
+ Default value: `"10m"`
+ Minimum value: `0`

### `lock-cf-compact-bytes-threshold`

+ The size out of which TiKV triggers a manual compaction for the Lock Column Family
+ Default value: `"256MB"`
+ Minimum value: `0`
+ Unit: MB

### `notify-capacity`

+ The longest length of the Region message queue.
+ Default value: `40960`
+ Minimum value: `0`

### `messages-per-tick`

+ The maximum number of messages processed per batch
+ Default value: `4096`
+ Minimum value: `0`

### `max-peer-down-duration`

+ The longest inactive duration allowed for a peer. A peer with timeout is marked as `down`, and PD tries to delete it later.
+ Default value: `"10m"`
+ Minimum value: When Hibernate Region is enabled, the minimum value is `peer-stale-state-check-interval * 2`; when Hibernate Region is disabled, the minimum value is `0`.

### `max-leader-missing-duration`

+ The longest duration allowed for a peer to be in the state where a Raft group is missing the leader. If this value is exceeded, the peer verifies with PD whether the peer has been deleted.
+ Default value: `"2h"`
+ Minimum value: greater than `abnormal-leader-missing-duration`

### `abnormal-leader-missing-duration`

+ The longest duration allowed for a peer to be in the state where a Raft group is missing the leader. If this value is exceeded, the peer is seen as abnormal and marked in metrics and logs.
+ Default value: `"10m"`
+ Minimum value: greater than `peer-stale-state-check-interval`

### `peer-stale-state-check-interval`

+ The time interval to trigger the check for whether a peer is in the state where a Raft group is missing the leader.
+ Default value: `"5m"`
+ Minimum value: greater than `2 * election-timeout`

### `leader-transfer-max-log-lag`

+ The maximum number of missing logs allowed for the transferee during a Raft leader transfer
+ Default value: `128`
+ Minimum value: `10`

### `max-snapshot-file-raw-size` <span class="version-mark">New in v6.1.0</span>

+ When the size of a snapshot file exceeds this configuration value, this file will be split into multiple files.
+ Default value: `100MiB`
+ Minimum value: `100MiB`

### `snap-apply-batch-size`

+ The memory cache size required when the imported snapshot file is written into the disk
+ Default value: `"10MB"`
+ Minimum value: `0`
+ Unit: MB

### `consistency-check-interval`

> **Warning:**
>
> It is **NOT** recommended to enable the consistency check in production environments, because it affects cluster performance and is incompatible with the garbage collection in TiDB.

+ The time interval at which the consistency check is triggered. `0` means that this feature is disabled.
+ Default value: `"0s"`
+ Minimum value: `0`

### `raft-store-max-leader-lease`

+ The longest trusted period of a Raft leader
+ Default value: `"9s"`
+ Minimum value: `0`

### `merge-max-log-gap`

+ The maximum number of missing logs allowed when `merge` is performed
+ Default value: `10`
+ Minimum value: greater than `raft-log-gc-count-limit`

### `merge-check-tick-interval`

+ The time interval at which TiKV checks whether a Region needs merge
+ Default value: `"2s"`
+ Minimum value: greater than `0`

### `use-delete-range`

+ Determines whether to delete data from the `rocksdb delete_range` interface
+ Default value: `false`

### `cleanup-import-sst-interval`

+ The time interval at which the expired SST file is checked. `0` means that this feature is disabled.
+ Default value: `"10m"`
+ Minimum value: `0`

### `local-read-batch-size`

+ The maximum number of read requests processed in one batch
+ Default value: `1024`
+ Minimum value: greater than `0`

### `apply-yield-write-size` <span class="version-mark">New in v6.4.0</span>

+ The maximum number of bytes that the Apply thread can write for one FSM (Finite-state Machine) in one round of poll. This is a soft limit.
+ Default value: `"32KiB"`
+ Minimum value: greater than `0`
+ Unit: KiB|MiB|GiB

### `apply-max-batch-size`

+ Raft state machines process data write requests in batches by the BatchSystem. This configuration item specifies the maximum number of Raft state machines that can process the requests in one batch.
+ Default value: `256`
+ Minimum value: greater than `0`
+ Maximum value: `10240`

### `apply-pool-size`

+ The allowable number of threads in the pool that flushes data to the disk, which is the size of the Apply thread pool. When you modify the size of this thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools).
+ Default value: `2`
+ Value ranges: `[1, CPU * 10]`. `CPU` means the number of your CPU cores.

### `store-max-batch-size`

+ Raft state machines process requests for flushing logs into the disk in batches by the BatchSystem. This configuration item specifies the maximum number of Raft state machines that can process the requests in one batch.
+ If `hibernate-regions` is enabled, the default value is `256`. If `hibernate-regions` is disabled, the default value is `1024`.
+ Minimum value: greater than `0`
+ Maximum value: `10240`

### `store-pool-size`

+ The allowable number of threads in the pool that processes Raft, which is the size of the Raftstore thread pool. When you modify the size of this thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools).
+ Default value: `2`
+ Value ranges: `[1, CPU * 10]`. `CPU` means the number of your CPU cores.

### `store-io-pool-size` <span class="version-mark">New in v5.3.0</span>

+ The allowable number of threads that process Raft I/O tasks, which is the size of the StoreWriter thread pool. When you modify the size of this thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools).
+ Default value: `0`
+ Minimum value: `0`

### `future-poll-size`

+ The allowable number of threads that drive `future`
+ Default value: `1`
+ Minimum value: greater than `0`

### `cmd-batch`

+ Controls whether to enable batch processing of the requests. When it is enabled, the write performance is significantly improved.
+ Default value: `true`

### `inspect-interval`

+ At a certain interval, TiKV inspects the latency of the Raftstore component. This parameter specifies the interval of the inspection. If the latency exceeds this value, this inspection is marked as timeout.
+ Judges whether the TiKV node is slow based on the ratio of timeout inspection.
+ Default value: `"500ms"`
+ Minimum value: `"1ms"`

### `raft-write-size-limit` <span class="version-mark">New in v5.3.0</span>

+ Determines the threshold at which Raft data is written into the disk. If the data size is larger than the value of this configuration item, the data is written to the disk. When the value of `store-io-pool-size` is `0`, this configuration item does not take effect.
+ Default value: `1MB`
+ Minimum value: `0`

## Coprocessor

Configuration items related to Coprocessor.

### `split-region-on-table`

+ Determines whether to split Region by table. It is recommended for you to use the feature only in TiDB mode.
+ Default value: `false`

### `batch-split-limit`

+ The threshold of Region split in batches. Increasing this value speeds up Region split.
+ Default value: `10`
+ Minimum value: `1`

### `region-max-size`

+ The maximum size of a Region. When the value is exceeded, the Region splits into many.
+ Default value: `region-split-size / 2 * 3`
+ Unit: KiB|MiB|GiB

### `region-split-size`

+ The size of the newly split Region. This value is an estimate.
+ Default value: `"96MiB"`
+ Unit: KiB|MiB|GiB

### `region-max-keys`

+ The maximum allowable number of keys in a Region. When this value is exceeded, the Region splits into many.
+ Default value: `region-split-keys / 2 * 3`

### `region-split-keys`

+ The number of keys in the newly split Region. This value is an estimate.
+ Default value: `960000`

### `consistency-check-method`

+ Specifies the method of data consistency check
+ For the consistency check of MVCC data, set the value to `"mvcc"`. For the consistency check of raw data, set the value to `"raw"`.
+ Default value: `"mvcc"`

## coprocessor-v2

### `coprocessor-plugin-directory`

+ The path of the directory where compiled coprocessor plugins are located. Plugins in this directory are automatically loaded by TiKV.
+ If this configuration item is not set, the coprocessor plugin is disabled.
+ Default value: `"./coprocessors"`

### `enable-region-bucket` <span class="version-mark">New in v6.1.0</span>

+ Determines whether to divide a Region into smaller ranges called buckets. The bucket is used as the unit of the concurrent query to improve the scan concurrency. For more about the design of the bucket, refer to [Dynamic size Region](https://github.com/tikv/rfcs/blob/master/text/0082-dynamic-size-region.md).
+ Default value: false

> **Warning:**
>
> - `enable-region-bucket` is an experimental feature introduced in TiDB v6.1.0. It is not recommended that you use it in production environments.
> - This configuration makes sense only when `region-split-size` is twice of `region-bucket-size` or above; otherwise, no bucket is actually generated.
> - Adjusting `region-split-size` to a larger value might have the risk of performance regression and slow scheduling.

### `region-bucket-size` <span class="version-mark">New in v6.1.0</span>

+ The size of a bucket when `enable-region-bucket` is true.
+ Default value: `96MiB`

> **Warning:**
>
> `region-bucket-size` is an experimental feature introduced in TiDB v6.1.0. It is not recommended that you use it in production environments.

### `report-region-buckets-tick-interval` <span class="version-mark">New in v6.1.0</span>

> **Warning:**
>
> `report-region-buckets-tick-interval` is an experimental feature introduced in TiDB v6.1.0. It is not recommended that you use it in production environments.

+ The interval at which TiKV reports bucket information to PD when `enable-region-bucket` is true.
+ Default value: `10s`

## RocksDB

Configuration items related to RocksDB

### `max-background-jobs`

+ The number of background threads in RocksDB. When you modify the size of the RocksDB thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools).
+ Default value:
    + When the number of CPU cores is 10, the default value is `9`.
    + When the number of CPU cores is 8, the default value is `7`.
    + When the number of CPU cores is `N`, the default value is `max(2, min(N - 1, 9))`.
+ Minimum value: `2`

### `max-background-flushes`

+ The maximum number of concurrent background memtable flush jobs
+ Default value:
    + When the number of CPU cores is 10, the default value is `3`.
    + When the number of CPU cores is 8, the default value is `2`.
    + When the number of CPU cores is `N`, the default value is `[(max-background-jobs + 3) / 4]`.
+ Minimum value: `1`

### `max-sub-compactions`

+ The number of sub-compaction operations performed concurrently in RocksDB
+ Default value: `3`
+ Minimum value: `1`

### `max-open-files`

+ The total number of files that RocksDB can open
+ Default value: `40960`
+ Minimum value: `-1`

### `max-manifest-file-size`

+ The maximum size of a RocksDB Manifest file
+ Default value: `"128MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `create-if-missing`

+ Determines whether to automatically create a DB switch
+ Default value: `true`

### `wal-recovery-mode`

+ WAL recovery mode
+ Optional values:
    + `"tolerate-corrupted-tail-records"`: tolerates and discards the records that have incomplete trailing data on all logs
    + `"absolute-consistency"`: abandons recovery when corrupted logs are found
    + `"point-in-time"`: recovers logs sequentially until the first corrupted log is encountered
    + `"skip-any-corrupted-records"`: post-disaster recovery. The data is recovered as much as possible, and corrupted records are skipped.
+ Default value: `"point-in-time"`

### `wal-dir`

+ The directory in which WAL files are stored
+ Default value: `"/tmp/tikv/store"`

### `wal-ttl-seconds`

+ The living time of the archived WAL files. When the value is exceeded, the system deletes these files.
+ Default value: `0`
+ Minimum value: `0`
+ unit: second

### `wal-size-limit`

+ The size limit of the archived WAL files. When the value is exceeded, the system deletes these files.
+ Default value: `0`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `max-total-wal-size`

+ The maximum RocksDB WAL size in total, which is the size of `*.log` files in the `data-dir`.
+ Default value: `"4GB"`

### `enable-statistics`

+ Determines whether to enable the statistics of RocksDB
+ Default value: `true`

### `stats-dump-period`

+ The interval at which statistics are output to the log.
+ Default value: `10m`

### `compaction-readahead-size`

+ Enables the readahead feature during RocksDB compaction and specifies the size of readahead data. If you are using mechanical disks, it is recommended to set the value to 2MB at least.
+ Default value: `0`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `writable-file-max-buffer-size`

+ The maximum buffer size used in WritableFileWrite
+ Default value: `"1MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `use-direct-io-for-flush-and-compaction`

+ Determines whether to use `O_DIRECT` for both reads and writes in the background flush and compactions. The performance impact of this option: enabling `O_DIRECT` bypasses and prevents contamination of the OS buffer cache, but the subsequent file reads require re-reading the contents to the buffer cache.
+ Default value: `false`

### `rate-bytes-per-sec`

+ The maximum rate permitted by RocksDB's compaction rate limiter
+ Default value: `10GB`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `rate-limiter-refill-period`

+ Controls how often I/O tokens are refilled. A smaller value reduces I/O bursts but causes more CPU overhead.
+ Default value: `"100ms"`

### `rate-limiter-mode`

+ RocksDB's compaction rate limiter mode
+ Optional values: `"read-only"`, `"write-only"`, `"all-io"`
+ Default value: `"write-only"`

### `rate-limiter-auto-tuned` <span class="version-mark">New in v5.0</span>

+ Determines whether to automatically optimize the configuration of the RocksDB's compaction rate limiter based on recent workload. When this configuration is enabled, compaction pending bytes will be slightly higher than usual.
+ Default value: `true`

### `enable-pipelined-write`

+ Controls whether to enable Pipelined Write. When this configuration is enabled, the previous Pipelined Write is used. When this configuration is disabled, the new Pipelined Commit mechanism is used.
+ Default value: `false`

### `bytes-per-sync`

+ The rate at which OS incrementally synchronizes files to disk while these files are being written asynchronously
+ Default value: `"1MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `wal-bytes-per-sync`

+ The rate at which OS incrementally synchronizes WAL files to disk while the WAL files are being written
+ Default value: `"512KB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `info-log-max-size`

+ The maximum size of Info log
+ Default value: `"1GB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `info-log-roll-time`

+ The time interval at which Info logs are truncated. If the value is `0s`, logs are not truncated.
+ Default value: `"0s"`

### `info-log-keep-log-file-num`

+ The maximum number of kept log files
+ Default value: `10`
+ Minimum value: `0`

### `info-log-dir`

+ The directory in which logs are stored
+ Default value: `""`

### `info-log-level`

+ Log levels of RocksDB
+ Default value: `"info"`

## rocksdb.titan

Configuration items related to Titan.

### `enabled`

+ Enables or disables Titan
+ Default value: `false`

### `dirname`

+ The directory in which the Titan Blob file is stored
+ Default value: `"titandb"`

### `disable-gc`

+ Determines whether to disable Garbage Collection (GC) that Titan performs to Blob files
+ Default value: `false`

### `max-background-gc`

+ The maximum number of GC threads in Titan
+ Default value: `4`
+ Minimum value: `1`

## rocksdb.defaultcf | rocksdb.writecf | rocksdb.lockcf

Configuration items related to `rocksdb.defaultcf`, `rocksdb.writecf`, and `rocksdb.lockcf`.

### `block-size`

+ The default size of a RocksDB block
+ Default value for `defaultcf` and `writecf`: `"64KB"`
+ Default value for `lockcf`: `"16KB"`
+ Minimum value: `"1KB"`
+ Unit: KB|MB|GB

### `block-cache-size`

+ The cache size of a RocksDB block
+ Default value for `defaultcf`: `Total machine memory * 25%`
+ Default value for `writecf`: `Total machine memory * 15%`
+ Default value for `lockcf`: `Total machine memory * 2%`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `disable-block-cache`

+ Enables or disables block cache
+ Default value: `false`

### `cache-index-and-filter-blocks`

+ Enables or disables caching index and filter
+ Default value: `true`

### `pin-l0-filter-and-index-blocks`

+ Determines whether to pin the index and filter blocks of the level 0 SST files in memory.
+ Default value: `true`

### `use-bloom-filter`

+ Enables or disables bloom filter
+ Default value: `true`

### `optimize-filters-for-hits`

+ Determines whether to optimize the hit ratio of filters
+ Default value for `defaultcf`: `true`
+ Default value for `writecf` and `lockcf`: `false`

### `whole-key-filtering`

+ Determines whether to put the entire key to bloom filter
+ Default value for `defaultcf` and `lockcf`: `true`
+ Default value for `writecf`: `false`

### `bloom-filter-bits-per-key`

+ The length that bloom filter reserves for each key
+ Default value: `10`
+ Unit: byte

### `block-based-bloom-filter`

+ Determines whether each block creates a bloom filter
+ Default value: `false`

### `read-amp-bytes-per-bit`

+ Enables or disables statistics of read amplification.
+ Optional values: `0` (disabled), > `0` (enabled).
+ Default value: `0`
+ Minimum value: `0`

### `compression-per-level`

+ The default compression algorithm for each level
+ Default value for `defaultcf`: ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]
+ Default value for `writecf`: ["no", "no", "lz4", "lz4", "lz4", "zstd", "zstd"]
+ Default value for `lockcf`: ["no", "no", "no", "no", "no", "no", "no"]

### `bottommost-level-compression`

+ Sets the compression algorithm of the bottommost layer. This configuration item overrides the `compression-per-level` setting.
+ Ever since data is written to LSM-tree, RocksDB does not directly adopt the last compression algorithm specified in the `compression-per-level` array for the bottommost layer. `bottommost-level-compression` enables the bottommost layer to use the compression algorithm of the best compression effect from the beginning.
+ If you do not want to set the compression algorithm for the bottommost layer, set the value of this configuration item to `disable`.
+ Default value: `"zstd"`

### `write-buffer-size`

+ Memtable size
+ Default value for `defaultcf` and `writecf`: `"128MB"`
+ Default value for `lockcf`: `"32MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `max-write-buffer-number`

+ The maximum number of memtables. When `storage.flow-control.enable` is set to `true`, `storage.flow-control.memtables-threshold` overrides this configuration item.
+ Default value: `5`
+ Minimum value: `0`

### `min-write-buffer-number-to-merge`

+ The minimum number of memtables required to trigger flush
+ Default value: `1`
+ Minimum value: `0`

### `max-bytes-for-level-base`

+ The maximum number of bytes at base level (level-1). Generally, it is set to 4 times the size of a memtable. When the level-1 data size reaches the limit value of `max-bytes-for-level-base`, the SST files of level-1 and their overlapping SST files of level-2 will be compacted.
+ Default value for `defaultcf` and `writecf`: `"512MB"`
+ Default value for `lockcf`: `"128MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB
+ It is recommended that the value of `max-bytes-for-level-base` is set approximately equal to the data volume in L0 to reduce unnecessary compaction. For example, if the compression method is "no:no:lz4:lz4:lz4:lz4:lz4", the value of `max-bytes-for-level-base` should be `write-buffer-size * 4`, because there is no compression of L0 and L1 and the trigger condition of compaction for L0 is that the number of the SST files reaches 4 (the default value). When L0 and L1 both adopt compaction, you need to analyze RocksDB logs to understand the size of an SST file compressed from a memtable. For example, if the file size is 32 MB, it is recommended to set the value of `max-bytes-for-level-base` to 128 MB (`32 MB * 4`).

### `target-file-size-base`

+ The size of the target file at base level. This value is overridden by `compaction-guard-max-output-file-size` when the `enable-compaction-guard` value is `true`.
+ Default value: `"8MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `level0-file-num-compaction-trigger`

+ The maximum number of files at L0 that trigger compaction
+ Default value for `defaultcf` and `writecf`: `4`
+ Default value for `lockcf`: `1`
+ Minimum value: `0`

### `level0-slowdown-writes-trigger`

+ The maximum number of files at L0 that trigger write stall. When `storage.flow-control.enable` is set to `true`, `storage.flow-control.l0-files-threshold` overrides this configuration item.
+ Default value: `20`
+ Minimum value: `0`

### `level0-stop-writes-trigger`

+ The maximum number of files at L0 required to completely block write
+ Default value: `36`
+ Minimum value: `0`

### `max-compaction-bytes`

+ The maximum number of bytes written into disk per compaction
+ Default value: `"2GB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `compaction-pri`

+ The priority type of compaction
+ Optional values: `"by-compensated-size"`, `"oldest-largest-seq-first"`, `"oldest-smallest-seq-first"`, `"min-overlapping-ratio"`
+ Default value for `defaultcf` and `writecf`: `"min-overlapping-ratio"`
+ Default value for `lockcf`: `"by-compensated-size"`

### `dynamic-level-bytes`

+ Determines whether to optimize dynamic level bytes
+ Default value: `true`

### `num-levels`

+ The maximum number of levels in a RocksDB file
+ Default value: `7`

### `max-bytes-for-level-multiplier`

+ The default amplification multiple for each layer
+ Default value: `10`

### `compaction-style`

+ Compaction method
+ Optional values: `"level"`, `"universal"`, `"fifo"`
+ Default value: `"level"`

### `disable-auto-compactions`

+ Determines whether to disable auto compaction.
+ Default value: `false`

### `soft-pending-compaction-bytes-limit`

+ The soft limit on the pending compaction bytes. When `storage.flow-control.enable` is set to `true`, `storage.flow-control.soft-pending-compaction-bytes-limit` overrides this configuration item.
+ Default value: `"192GB"`
+ Unit: KB|MB|GB

### `hard-pending-compaction-bytes-limit`

+ The hard limit on the pending compaction bytes. When `storage.flow-control.enable` is set to `true`, `storage.flow-control.hard-pending-compaction-bytes-limit` overrides this configuration item.
+ Default value: `"256GB"`
+ Unit: KB|MB|GB

### `enable-compaction-guard`

+ Enables or disables the compaction guard, which is an optimization to split SST files at TiKV Region boundaries. This optimization can help reduce compaction I/O and allows TiKV to use larger SST file size (thus less SST files overall) and at the time efficiently clean up stale data when migrating Regions.
+ Default value for `defaultcf` and `writecf`: `true`
+ Default value for `lockcf`: `false`

### `compaction-guard-min-output-file-size`

+ The minimum SST file size when the compaction guard is enabled. This configuration prevents SST files from being too small when the compaction guard is enabled.
+ Default value: `"8MB"`
+ Unit: KB|MB|GB

### `compaction-guard-max-output-file-size`

+ The maximum SST file size when the compaction guard is enabled. The configuration prevents SST files from being too large when the compaction guard is enabled. This configuration overrides `target-file-size-base` for the same column family.
+ Default value: `"128MB"`
+ Unit: KB|MB|GB

## rocksdb.defaultcf.titan

Configuration items related to `rocksdb.defaultcf.titan`.

### `min-blob-size`

+ The smallest value stored in a Blob file. Values smaller than the specified size are stored in the LSM-Tree.
+ Default value: `"1KB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `blob-file-compression`

+ The compression algorithm used in a Blob file
+ Optional values: `"no"`, `"snappy"`, `"zlib"`, `"bzip2"`, `"lz4"`, `"lz4hc"`, `"zstd"`
+ Default value: `"lz4"`

### `blob-cache-size`

+ The cache size of a Blob file
+ Default value: `"0GB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `min-gc-batch-size`

+ The minimum total size of Blob files required to perform GC for one time
+ Default value: `"16MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `max-gc-batch-size`

+ The maximum total size of Blob files allowed to perform GC for one time
+ Default value: `"64MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `discardable-ratio`

+ The ratio at which GC is triggered for Blob files. The Blob file can be selected for GC only if the proportion of the invalid values in a Blob file exceeds this ratio.
+ Default value: `0.5`
+ Minimum value: `0`
+ Maximum value: `1`

### `sample-ratio`

+ The ratio of (data read from a Blob file/the entire Blob file) when sampling the file during GC
+ Default value: `0.1`
+ Minimum value: `0`
+ Maximum value: `1`

### `merge-small-file-threshold`

+ When the size of a Blob file is smaller than this value, the Blob file might still be selected for GC. In this situation, `discardable-ratio` is ignored.
+ Default value: `"8MB"`
+ Minimum value: `0`
+ Unit: KB|MB|GB

### `blob-run-mode`

+ Specifies the running mode of Titan.
+ Optional values:
    + `normal`: Writes data to the blob file when the value size exceeds `min-blob-size`.
    + `read_only`: Refuses to write new data to the blob file, but still reads the original data from the blob file.
    + `fallback`: Writes data in the blob file back to LSM.
+ Default value: `normal`

### `level-merge`

+ Determines whether to optimize the read performance. When `level-merge` is enabled, there is more write amplification.
+ Default value: `false`

## raftdb

Configuration items related to `raftdb`

### `max-background-jobs`

+ The number of background threads in RocksDB. When you modify the size of the RocksDB thread pool, refer to [Performance tuning for TiKV thread pools](/tune-tikv-thread-performance.md#performance-tuning-for-tikv-thread-pools).
+ Default value: `4`
+ Minimum value: `2`

### `max-sub-compactions`

+ The number of concurrent sub-compaction operations performed in RocksDB
+ Default value: `2`
+ Minimum value: `1`

### `max-open-files`

+ The total number of files that RocksDB can open
+ Default value: `40960`
+ Minimum value: `-1`

### `max-manifest-file-size`

+ The maximum size of a RocksDB Manifest file
+ Default value: `"20MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `create-if-missing`

+ If the value is `true`, the database will be created if it is missing
+ Default value: `true`

### `enable-statistics`

+ Determines whether to enable the statistics of Raft RocksDB
+ Default value: `true`

### `stats-dump-period`

+ The interval at which statistics are output to the log
+ Default value: `10m`

### `wal-dir`

+ The directory in which Raft RocksDB WAL files are stored, which is the absolute directory path for WAL. **Do not** set this configuration item to the same value as [`rocksdb.wal-dir`](#wal-dir).
+ If this configuration item is not set, the log files are stored in the same directory as data.
+ If there are two disks on the machine, storing RocksDB data and WAL logs on different disks can improve performance.
+ Default value: `""`

### `wal-ttl-seconds`

+ Specifies how long the archived WAL files are retained. When the value is exceeded, the system deletes these files.
+ Default value: `0`
+ Minimum value: `0`
+ Unit: second

### `wal-size-limit`

+ The size limit of the archived WAL files. When the value is exceeded, the system deletes these files.
+ Default value: `0`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `max-total-wal-size`

+ The maximum RocksDB WAL size in total
+ Default value: `"4GB"`

### `compaction-readahead-size`

+ Controls whether to enable the readahead feature during RocksDB compaction and specify the size of readahead data.
+ If you use mechanical disks, it is recommended to set the value to `2MB` at least.
+ Default value: `0`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `writable-file-max-buffer-size`

+ The maximum buffer size used in WritableFileWrite
+ Default value: `"1MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `use-direct-io-for-flush-and-compaction`

+ Determines whether to use `O_DIRECT` for both reads and writes in the background flush and compactions. The performance impact of this option: enabling `O_DIRECT` bypasses and prevents contamination of the OS buffer cache, but the subsequent file reads require re-reading the contents to the buffer cache.
+ Default value: `false`

### `enable-pipelined-write`

+ Controls whether to enable Pipelined Write. When this configuration is enabled, the previous Pipelined Write is used. When this configuration is disabled, the new Pipelined Commit mechanism is used.
+ Default value: `true`

### `allow-concurrent-memtable-write`

+ Controls whether to enable concurrent memtable write.
+ Default value: `true`

### `bytes-per-sync`

+ The rate at which OS incrementally synchronizes files to disk while these files are being written asynchronously
+ Default value: `"1MB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `wal-bytes-per-sync`

+ The rate at which OS incrementally synchronizes WAL files to disk when the WAL files are being written
+ Default value: `"512KB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `info-log-max-size`

+ The maximum size of Info logs
+ Default value: `"1GB"`
+ Minimum value: `0`
+ Unit: B|KB|MB|GB

### `info-log-roll-time`

+ The interval at which Info logs are truncated. If the value is `0s`, logs are not truncated.
+ Default value: `"0s"` (which means logs are not truncated)

### `info-log-keep-log-file-num`

+ The maximum number of Info log files kept in RaftDB
+ Default value: `10`
+ Minimum value: `0`

### `info-log-dir`

+ The directory in which Info logs are stored
+ Default value: `""`

### `info-log-level`

+ Log levels of RocksDB
+ Default value: `"info"`

## raft-engine

Configuration items related to Raft Engine.

> **Note:**
>
> - When you enable Raft Engine for the first time, TiKV transfers its data from RocksDB to Raft Engine. Therefore, you need to wait extra tens of seconds for TiKV to start.
> - The data format of Raft Engine in TiDB v5.4.0 is not compatible with earlier TiDB versions. Therefore, if you need to downgrade a TiDB cluster from v5.4.0 to an earlier version, **before** downgrading, disable Raft Engine by setting `enable` to `false` and restart TiKV for the configuration to take effect.

### `enable`

+ Determines whether to use Raft Engine to store Raft logs. When it is enabled, configurations of `raftdb` are ignored.
+ Default value: `true`

### `dir`

+ The directory at which raft log files are stored. If the directory does not exist, it will be created when TiKV is started.
+ If this configuration item is not set, `{data-dir}/raft-engine` is used.
+ If there are multiple disks on your machine, it is recommended to store the data of Raft Engine on a different disk to improve TiKV performance.
+ Default value: `""`

### `batch-compression-threshold`

+ Specifies the threshold size of a log batch. A log batch larger than this configuration is compressed. If you set this configuration item to `0`, compression is disabled.
+ Default value: `"8KB"`

### `bytes-per-sync`

+ Specifies the maximum accumulative size of buffered writes. When this configuration value is exceeded, buffered writes are flushed to the disk.
+ If you set this configuration item to `0`, incremental sync is disabled.
+ Default value: `"4MB"`

### `target-file-size`

+ Specifies the maximum size of log files. When a log file is larger than this value, it is rotated.
+ Default value: `"128MB"`

### `purge-threshold`

+ Specifies the threshold size of the main log queue. When this configuration value is exceeded, the main log queue is purged.
+ This configuration can be used to adjust the disk space usage of Raft Engine.
+ Default value: `"10GB"`

### `recovery-mode`

+ Determines how to deal with file corruption during recovery.
+ Value options: `"absolute-consistency"`, `"tolerate-tail-corruption"`, `"tolerate-any-corruption"`
+ Default value: `"tolerate-tail-corruption"`

### `recovery-read-block-size`

+ The minimum I/O size for reading log files during recovery.
+ Default value: `"16KB"`
+ Minimum value: `"512B"`

### `recovery-threads`

+ The number of threads used to scan and recover log files.
+ Default value: `4`
+ Minimum value: `1`

### `memory-limit`

+ Specifies the limit on the memory usage of Raft Engine.
+ When this configuration value is not set, 15% of the available system memory is used.
+ Default value: `Total machine memory * 15%`

### `format-version` <span class="version-mark">New in v6.3.0</span>

> **Note:**
>
> After `format-version` is set to `2`, if you need to downgrade a TiKV cluster from v6.3.0 to an earlier version, take the following steps **before** the downgrade:
>
> 1. Disable Raft Engine by setting [`enable`](/tikv-configuration-file.md#enable-1) to `false` and restart TiKV to make the configuration take effect.
> 2. Set `format-version` to `1`.
> 3. Enable Raft Engine by setting `enable` to `true` and restart TiKV to make the configuration take effect.

+ Specifies the version of log files in Raft Engine.
+ Value Options:
    + `1`: Default log file version for TiKV earlier than v6.3.0. Can be read by TiKV >= v6.1.0.
    + `2`: Supports log recycling. Can be read by TiKV >= v6.3.0.
+ Default value: `2`

### `enable-log-recycle` <span class="version-mark">New in v6.3.0</span>

> **Note:**
>
> This configuration item is only available when [`format-version`](#format-version-new-in-v630) >= 2.

+ Determines whether to recycle stale log files in Raft Engine. When it is enabled, logically purged log files will be reserved for recycling. This reduces the long tail latency on write workloads.
+ Default value: `false`

## security

Configuration items related to security.

### `ca-path`

+ The path of the CA file
+ Default value: `""`

### `cert-path`

+ The path of the Privacy Enhanced Mail (PEM) file that contains the X.509 certificate
+ Default value: `""`

### `key-path`

+ The path of the PEM file that contains the X.509 key
+ Default value: `""`

### `cert-allowed-cn`

+ A list of acceptable X.509 Common Names in certificates presented by clients. Requests are permitted only when the presented Common Name is an exact match with one of the entries in the list.
+ Default value: `[]`. This means that the client certificate CN check is disabled by default.

### `redact-info-log` <span class="version-mark">New in v4.0.8</span>

+ This configuration item enables or disables log redaction. If the configuration value is set to `true`, all user data in the log will be replaced by `?`.
+ Default value: `false`

## security.encryption

Configuration items related to [encryption at rest](/encryption-at-rest.md) (TDE).

### `data-encryption-method`

+ The encryption method for data files
+ Value options: "plaintext", "aes128-ctr", "aes192-ctr", "aes256-ctr", and "sm4-ctr" (supported since v6.3.0)
+ A value other than "plaintext" means that encryption is enabled, in which case the master key must be specified.
+ Default value: `"plaintext"`

### `data-key-rotation-period`

+ Specifies how often TiKV rotates the data encryption key.
+ Default value: `7d`

### `enable-file-dictionary-log`

+ Enables the optimization to reduce I/O and mutex contention when TiKV manages the encryption metadata.
+ To avoid possible compatibility issues when this configuration parameter is enabled (by default), see [Encryption at Rest - Compatibility between TiKV versions](/encryption-at-rest.md#compatibility-between-tikv-versions) for details.
+ Default value: `true`

### `master-key`

+ Specifies the master key if encryption is enabled. To learn how to configure a master key, see [Encryption at Rest - Configure encryption](/encryption-at-rest.md#configure-encryption).

### `previous-master-key`

+ Specifies the old master key when rotating the new master key. The configuration format is the same as that of `master-key`. To learn how to configure a master key, see [Encryption at Rest - Configure encryption](/encryption-at-rest.md#configure-encryption).

## `import`

Configuration items related to TiDB Lightning import and BR restore.

### `num-threads`

+ The number of threads to process RPC requests
+ Default value: `8`
+ Minimum value: `1`

### `stream-channel-window`

+ The window size of Stream channel. When the channel is full, the stream is blocked.
+ Default value: `128`

### `memory-use-ratio` <span class="version-mark">New in v6.5.0</span>

+ Starting from v6.5.0, PITR supports directly accessing backup log files in memory and restoring data. This configuration item specifies the ratio of memory available for PITR to the total memory of TiKV.
+ Value range: [0.0, 0.5]
+ Default value: `0.3`, which means that 30% of the system memory is available for PITR. When the value is `0.0`, PITR is performed through downloading log files to a local directory.

> **Note:**
>
> In versions earlier than v6.5.0, point-in-time recovery (PITR) only supports restoring data by downloading backup files to a local directory.

## gc

### `batch-keys`

+ The number of keys to be garbage-collected in one batch
+ Default value: `512`

### `max-write-bytes-per-sec`

+ The maximum bytes that GC worker can write to RocksDB in one second.
+ If the value is set to `0`, there is no limit.
+ Default value: `"0"`

### `enable-compaction-filter` <span class="version-mark">New in v5.0</span>

+ Controls whether to enable the GC in Compaction Filter feature
+ Default value: `true`

### `ratio-threshold`

+ The garbage ratio threshold to trigger GC.
+ Default value: `1.1`

## backup

Configuration items related to BR backup.

### `num-threads`

+ The number of worker threads to process backup
+ Default value: `MIN(CPU * 0.5, 8)`
+ Value range: `[1, CPU]`
+ Minimum value: `1`

### `batch-size`

+ The number of data ranges to back up in one batch
+ Default value: `8`

### `sst-max-size`

+ The threshold of the backup SST file size. If the size of a backup file in a TiKV Region exceeds this threshold, the file is backed up to several files with the TiKV Region split into multiple Region ranges. Each of the files in the split Regions is the same size as `sst-max-size` (or slightly larger).
+ For example, when the size of a backup file in the Region of `[a,e)` is larger than `sst-max-size`, the file is backed up to several files with regions `[a,b)`, `[b,c)`, `[c,d)` and `[d,e)`, and the size of `[a,b)`, `[b,c)`, `[c,d)` is the same as that of `sst-max-size` (or slightly larger).
+ Default value: `"144MB"`

### `enable-auto-tune` <span class="version-mark">New in v5.4.0</span>

+ Controls whether to limit the resources used by backup tasks to reduce the impact on the cluster when the cluster resource utilization is high. For more information, refer to [BR Auto-Tune](/br/br-auto-tune.md).
+ Default value: `true`

### `s3-multi-part-size` <span class="version-mark">New in v5.3.2</span>

> **Note:**
>
> This configuration is introduced to address backup failures caused by S3 rate limiting. This problem has been fixed by [refining the backup data storage structure](/br/br-snapshot-architecture.md#structure-of-backup-files). Therefore, this configuration is deprecated from v6.1.1 and is no longer recommended.

+ The part size used when you perform multipart upload to S3 during backup. You can adjust the value of this configuration to control the number of requests sent to S3.
+ If data is backed up to S3 and the backup file is larger than the value of this configuration item, [multipart upload](https://docs.aws.amazon.com/AmazonS3/latest/API/API_UploadPart.html) is automatically enabled. Based on the compression ratio, the backup file generated by a 96-MiB Region is approximately 10 MiB to 30 MiB.
+ Default value: 5MiB

## backup.hadoop

### `home`

+ Specifies the location of the HDFS shell command and allows TiKV to find the shell command. This configuration item has the same effect as the environment variable `$HADOOP_HOME`.
+ Default value: `""`

### `linux-user`

+ Specifies the Linux user with which TiKV runs HDFS shell commands.
+ If this configuration item is not set, TiKV uses the current linux user.
+ Default value: `""`

## log-backup

Configuration items related to log backup.

### `enable` <span class="version-mark">New in v6.2.0</span>

+ Determines whether to enable log backup.
+ Default value: `true`

### `file-size-limit` <span class="version-mark">New in v6.2.0</span>

+ The size limit on backup log data to be stored.
+ Default value: 256MiB
+ Note: Generally, the value of `file-size-limit` is greater than the backup file size displayed in external storage. This is because the backup files are compressed before being uploaded to external storage.

### `initial-scan-pending-memory-quota` <span class="version-mark">New in v6.2.0</span>

+ The quota of cache used for storing incremental scan data during log backup.
+ Default value: `min(Total machine memory * 10%, 512 MB)`

### `initial-scan-rate-limit` <span class="version-mark">New in v6.2.0</span>

+ The rate limit on throughput in an incremental data scan during log backup.
+ Default value: 60, indicating that the rate limit is 60 MB/s by default.

### `max-flush-interval` <span class="version-mark">New in v6.2.0</span>

+ The maximum interval for writing backup data to external storage in log backup.
+ Default value: 3min

### `num-threads` <span class="version-mark">New in v6.2.0</span>

+ The number of threads used in log backup.
+ Default value: CPU * 0.5
+ Value range: [2, 12]

### `temp-path` <span class="version-mark">New in v6.2.0</span>

+ The temporary path to which log files are written before being flushed to external storage.
+ Default value: `${deploy-dir}/data/log-backup-temp`

## cdc

Configuration items related to TiCDC.

### `min-ts-interval`

+ The interval at which Resolved TS is calculated and forwarded.
+ Default value: `"200ms"`

### `old-value-cache-memory-quota`

+ The upper limit of memory usage by TiCDC old values.
+ Default value: `512MB`

### `sink-memory-quota`

+ The upper limit of memory usage by TiCDC data change events.
+ Default value: `512MB`

### `incremental-scan-speed-limit`

+ The maximum speed at which historical data is incrementally scanned.
+ Default value: `"128MB"`, which means 128 MB per second.

### `incremental-scan-threads`

+ The number of threads for the task of incrementally scanning historical data.
+ Default value: `4`, which means 4 threads.

### `incremental-scan-concurrency`

+ The maximum number of concurrent executions for the tasks of incrementally scanning historical data.
+ Default value: `6`, which means 6 tasks can be concurrent executed at most.
+ Note: The value of `incremental-scan-concurrency` must be greater than or equal to that of `incremental-scan-threads`; otherwise, TiKV will report an error at startup.

## resolved-ts

Configuration items related to maintaining the Resolved TS to serve Stale Read requests.

### `enable`

+ Determines whether to maintain the Resolved TS for all Regions.
+ Default value: `true`

### `advance-ts-interval`

+ The interval at which Resolved TS is calculated and forwarded.
+ Default value: `"1s"`

### `scan-lock-pool-size`

+ The number of threads that TiKV uses to scan the MVCC (multi-version concurrency control) lock data when initializing the Resolved TS.
+ Default value: `2`, which means 2 threads.

## pessimistic-txn

For pessimistic transaction usage, refer to [TiDB Pessimistic Transaction Mode](/pessimistic-transaction.md).

### `wait-for-lock-timeout`

- The longest time that a pessimistic transaction in TiKV waits for other transactions to release the lock. If the time is out, an error is returned to TiDB, and TiDB retries to add a lock. The lock wait timeout is set by `innodb_lock_wait_timeout`.
- Default value: `"1s"`
- Minimum value: `"1ms"`

### `wake-up-delay-duration`

- When pessimistic transactions release the lock, among all the transactions waiting for lock, only the transaction with the smallest `start_ts` is woken up. Other transactions will be woken up after `wake-up-delay-duration`.
- Default value: `"20ms"`

### `pipelined`

- This configuration item enables the pipelined process of adding the pessimistic lock. With this feature enabled, after detecting that data can be locked, TiKV immediately notifies TiDB to execute the subsequent requests and write the pessimistic lock asynchronously, which reduces most of the latency and significantly improves the performance of pessimistic transactions. But there is a still low probability that the asynchronous write of the pessimistic lock fails, which might cause the failure of pessimistic transaction commits.
- Default value: `true`

### `in-memory` <span class="version-mark">New in v6.0.0</span>

+ Enables the in-memory pessimistic lock feature. With this feature enabled, pessimistic transactions try to store their locks in memory, instead of writing the locks to disk or replicating the locks to other replicas. This improves the performance of pessimistic transactions. However, there is a still low probability that the pessimistic lock gets lost and causes the pessimistic transaction commits to fail.
+ Default value: `true`
+ Note that `in-memory` takes effect only when the value of `pipelined` is `true`.

## quota

Configuration items related to Quota Limiter.

### `max-delay-duration` <span class="version-mark">New in v6.0.0</span>

+ The maximum time that a single read or write request is forced to wait before it is processed in the foreground.
+ Default value: `500ms`
+ Recommended setting: It is recommended to use the default value in most cases. If out of memory (OOM) or violent performance jitter occurs in the instance, you can set the value to 1S to make the request waiting time shorter than 1 second.

### Foreground Quota Limiter

Configuration items related to foreground Quota Limiter.

Suppose that your machine on which TiKV is deployed has limited resources, for example, with only 4v CPU and 16 G memory. In this situation, the foreground of TiKV might process too many read and write requests so that the CPU resources used by the background are occupied to help process such requests, which affects the performance stability of TiKV. To avoid this situation, you can use the foreground quota-related configuration items to limit the CPU resources to be used by the foreground. When a request triggers Quota Limiter, the request is forced to wait for a while for TiKV to free up CPU resources. The exact waiting time depends on the number of requests, and the maximum waiting time is no longer than the value of [`max-delay-duration`](#max-delay-duration-new-in-v600).

#### `foreground-cpu-time` <span class="version-mark">New in v6.0.0</span>

+ The soft limit on the CPU resources used by TiKV foreground to process read and write requests.
+ Default value: `0` (which means no limit)
+ Unit: millicpu (for example, `1500` means that the foreground requests consume 1.5v CPU)
+ Recommended setting: For the instance with more than 4 cores, use the default value `0`. For the instance with 4 cores, setting the value to the range of `1000` and `1500` can make a balance. For the instance with 2 cores, keep the value smaller than `1200`.

#### `foreground-write-bandwidth` <span class="version-mark">New in v6.0.0</span>

+ The soft limit on the bandwidth with which transactions write data.
+ Default value: `0KB` (which means no limit)
+ Recommended setting: Use the default value `0` in most cases unless the `foreground-cpu-time` setting is not enough to limit the write bandwidth. For such an exception, it is recommended to set the value smaller than `50MB` in the instance with 4 or less cores.

#### `foreground-read-bandwidth` <span class="version-mark">New in v6.0.0</span>

+ The soft limit on the bandwidth with which transactions and the Coprocessor read data.
+ Default value: `0KB` (which means no limit)
+ Recommended setting: Use the default value `0` in most cases unless the `foreground-cpu-time` setting is not enough to limit the read bandwidth. For such an exception, it is recommended to set the value smaller than `20MB` in the instance with 4 or less cores.

### Background Quota Limiter

Configuration items related to background Quota Limiter.

Suppose that your machine on which TiKV is deployed has limited resources, for example, with only 4v CPU and 16 G memory. In this situation, the background of TiKV might process too many calculations and read and write requests, so that the CPU resources used by the foreground are occupied to help process such requests, which affects the performance stability of TiKV. To avoid this situation, you can use the background quota-related configuration items to limit the CPU resources to be used by the background. When a request triggers Quota Limiter, the request is forced to wait for a while for TiKV to free up CPU resources. The exact waiting time depends on the number of requests, and the maximum waiting time is no longer than the value of [`max-delay-duration`](#max-delay-duration-new-in-v600).

> **Warning:**
>
> - Background Quota Limiter is an experimental feature introduced in TiDB v6.2.0, and it is **NOT** recommended to use it in the production environment.
> - This feature is only suitable for environments with limited resources to ensure that TiKV can run stably in those environments. If you enable this feature in an environment with rich resources, performance degradation might occur when the amount of requests reaches a peak.

#### `background-cpu-time` <span class="version-mark">New in v6.2.0</span>

+ The soft limit on the CPU resources used by TiKV background to process read and write requests.
+ Default value: `0` (which means no limit)
+ Unit: millicpu (for example, `1500` means that the background requests consume 1.5v CPU)

#### `background-write-bandwidth` <span class="version-mark">New in v6.2.0</span>

> **Note:**
>
> This configuration item is returned in the result of `SHOW CONFIG`, but currently setting it does not take any effect.

+ The soft limit on the bandwidth with which background transactions write data.
+ Default value: `0KB` (which means no limit)

#### `background-read-bandwidth` <span class="version-mark">New in v6.2.0</span>

> **Note:**
>
> This configuration item is returned in the result of `SHOW CONFIG`, but currently setting it does not take any effect.

+ The soft limit on the bandwidth with which background transactions and the Coprocessor read data.
+ Default value: `0KB` (which means no limit)

#### `enable-auto-tune` <span class="version-mark">New in v6.2.0</span>

+ Determines whether to enable the auto-tuning of quota. If this configuration item is enabled, TiKV dynamically adjusts the quota for the background requests based on the load of TiKV instances.
+ Default value: `false` (which means that the auto-tuning is disabled)

## causal-ts <span class="version-mark">New in v6.1.0</span>

Configuration items related to getting the timestamp when TiKV API V2 is enabled (`storage.api-version = 2`).

To reduce write latency, TiKV periodically fetches and caches a batch of timestamps locally. Cached timestamps help avoid frequent access to PD and allow short-term TSO service failure.

### `alloc-ahead-buffer` <span class="version-mark">New in v6.4.0</span>

+ The pre-allocated TSO cache size (in duration).
+ Indicates that TiKV pre-allocates the TSO cache based on the duration specified by this configuration item. TiKV estimates the TSO usage based on the previous period, and requests and caches TSOs satisfying `alloc-ahead-buffer` locally.
+ This configuration item is often used to increase the tolerance of PD failures when TiKV API V2 is enabled (`storage.api-version = 2`).
+ Increasing the value of this configuration item might result in more TSO consumption and memory overhead of TiKV. To obtain enough TSOs, it is recommended to decrease the [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) configuration item of PD.
+ According to the test, when `alloc-ahead-buffer` is in its default value, and the PD leader fails and switches to another node, the write request will experience a short-term increase in latency and a decrease in QPS (about 15%).
+ To avoid the impact on the business, you can configure `tso-update-physical-interval = "1ms"` in PD and the following configuration items in TiKV:
    + `causal-ts.alloc-ahead-buffer = "6s"`
    + `causal-ts.renew-batch-max-size = 65536`
    + `causal-ts.renew-batch-min-size = 2048`
+ Default value: `3s`

### `renew-interval`

+ The interval at which the locally cached timestamps are updated.
+ At an interval of `renew-interval`, TiKV starts a batch of timestamp refresh and adjusts the number of cached timestamps according to the timestamp consumption in the previous period and the setting of [`alloc-ahead-buffer`](#alloc-ahead-buffer-new-in-v640). If you set this parameter to too large a value, the latest TiKV workload changes are not reflected in time. If you set this parameter to too small a value, the load of PD increases. If the write traffic is strongly fluctuating, if timestamps are frequently exhausted, and if write latency increases, you can set this parameter to a smaller value. At the same time, you should also consider the load of PD.
+ Default value: `"100ms"`

### `renew-batch-min-size`

+ The minimum number of TSOs in a timestamp request.
+ TiKV adjusts the number of cached timestamps according to the timestamp consumption in the previous period. If only a few TSOs are required, TiKV reduces the TSOs requested until the number reaches `renew-batch-min-size`. If large bursty write traffic often occurs in your application, you can set this parameter to a larger value as appropriate. Note that this parameter is the cache size for a single tikv-server. If you set the parameter to too large a value and the cluster contains many tikv-servers, the TSO consumption will be too fast.
+ In the **TiKV-RAW** \> **Causal timestamp** panel in Grafana, **TSO batch size** is the number of locally cached timestamps that has been dynamically adjusted according to the application workload. You can refer to this metric to adjust `renew-batch-min-size`.
+ Default value: `100`

### `renew-batch-max-size` <span class="version-mark">New in v6.4.0</span>

+ The maximum number of TSOs in a timestamp request.
+ In a default TSO physical time update interval (`50ms`), PD provides at most 262144 TSOs. When requested TSOs exceed this number, PD provides no more TSOs. This configuration item is used to avoid exhausting TSOs and the reverse impact of TSO exhaustion on other businesses. If you increase the value of this configuration item to improve high availability, you need to decrease the value of [`tso-update-physical-interval`](/pd-configuration-file.md#tso-update-physical-interval) at the same time to get enough TSOs.
+ Default value: `8192`
