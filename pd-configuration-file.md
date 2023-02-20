---
title: PD Configuration File
summary: Learn the PD configuration file.
aliases: ['/docs/dev/pd-configuration-file/','/docs/dev/reference/configuration/pd-server/configuration-file/']
---

# PD Configuration File

<!-- markdownlint-disable MD001 -->

The PD configuration file supports more options than command-line parameters. You can find the default configuration file [here](https://github.com/pingcap/pd/blob/master/conf/config.toml).

This document only describes parameters that are not included in command-line parameters. Check [here](/command-line-flags-for-pd-configuration.md) for the command line parameters.

### `name`

- The unique name of a PD node
- Default value: `"pd"`
- To start multiply PD nodes, use a unique name for each node.

### `data-dir`

- The directory in which PD stores data
- Default value: `default.${name}"`

### `client-urls`

- The list of client URLs to be listened to by PD
- Default value: `"http://127.0.0.1:2379"`
- When you deploy a cluster, you must specify the IP address of the current host as `client-urls` (for example, `"http://192.168.100.113:2379"`). If the cluster runs on Docker, specify the IP address of Docker as `"http://0.0.0.0:2379"`.

### `advertise-client-urls`

- The list of advertise URLs for the client to access PD
- Default value: `"${client-urls}"`
- In some situations such as in the Docker or NAT network environment, if a client cannot access PD through the default client URLs listened to by PD, you must manually set the advertise client URLs.
- For example, the internal IP address of Docker is `172.17.0.1`, while the IP address of the host is `192.168.100.113` and the port mapping is set to `-p 2380:2380`. In this case, you can set `advertise-client-urls` to `"http://192.168.100.113:2380"`. The client can find this service through `"http://192.168.100.113:2380"`.

### `peer-urls`

- The list of peer URLs to be listened to by a PD node
- Default value: `"http://127.0.0.1:2380"`
- When you deploy a cluster, you must specify `peer-urls` as the IP address of the current host, such as `"http://192.168.100.113:2380"`. If the cluster runs on Docker, specify the IP address of Docker as `"http://0.0.0.0:2380"`.

### `advertise-peer-urls`

- The list of advertise URLs for other PD nodes (peers) to access a PD node
- Default: `"${peer-urls}"`
- In some situations such as in the Docker or NAT network environment, if the other nodes (peers) cannot access the PD node through the default peer URLs listened to by this PD node, you must manually set the advertise peer URLs.
- For example, the internal IP address of Docker is `172.17.0.1`, while the IP address of the host is `192.168.100.113` and the port mapping is set to `-p 2380:2380`. In this case, you can set `advertise-peer-urls` to `"http://192.168.100.113:2380"`. The other PD nodes can find this service through `"http://192.168.100.113:2380"`.

### `initial-cluster`

- The initial cluster configuration for bootstrapping
- Default value: `"{name}=http://{advertise-peer-url}"`
- For example, if `name` is "pd", and `advertise-peer-urls` is `"http://192.168.100.113:2380"`, the `initial-cluster` is `"pd=http://192.168.100.113:2380"`.
- If you need to start three PD servers, the `initial-cluster` might be:

    ```
    pd1=http://192.168.100.113:2380, pd2=http://192.168.100.114:2380, pd3=192.168.100.115:2380
    ```

### `initial-cluster-state`

+ The initial state of the cluster
+ Default value: `"new"`

### `initial-cluster-token`

+ Identifies different clusters during the bootstrap phase
+ Default value: `"pd-cluster"`
+ If multiple clusters that have nodes with same configurations are deployed successively, you must specify different tokens to isolate different cluster nodes.

### `lease`

+ The timeout of the PD Leader Key lease. After the timeout, the system re-elects a Leader.
+ Default value: `3`
+ Unit: second

### `quota-backend-bytes`

+ The storage size of the meta-information database, which is 8GiB by default
+ Default value: `8589934592`

### `auto-compaction-mod`

+ The automatic compaction modes of the meta-information database
+ Available options: `periodic` (by cycle) and `revision` (by version number).
+ Default value: `periodic`

### `auto-compaction-retention`

+ The time interval for automatic compaction of the meta-information database when `auto-compaction-retention` is `periodic`. When the compaction mode is set to `revision`, this parameter indicates the version number for the automatic compaction.
+ Default value: 1h

### `force-new-cluster`

+ Determines whether to force PD to start as a new cluster and modify the number of Raft members to `1`
+ Default value: `false`

### `tso-update-physical-interval`

+ The interval at which PD updates the physical time of TSO.
+ In a default update interval of TSO physical time, PD provides at most 262144 TSOs. To get more TSOs, you can reduce the value of this configuration item. The minimum value is `1ms`.
+ Decreasing this configuration item might increase the CPU usage of PD. According to the test, compared with the interval of `50ms`, the [CPU usage](https://man7.org/linux/man-pages/man1/top.1.html) of PD will increase by about 10% when the interval is `1ms`.
+ Default value: `50ms`
+ Minimum value: `1ms`

## pd-server

Configuration items related to pd-server

### `server-memory-limit` <span class="version-mark">New in v6.6.0</span>

> **Warning:**
>
> This configuration is an experimental feature. It is not recommended to use it in production environments.

+ The memory limit ratio for a PD instance. The value `0` means no memory limit.
+ Default value: `0`
+ Minimum value: `0`
+ Maximum value: `0.99`

### `server-memory-limit-gc-trigger` <span class="version-mark">New in v6.6.0</span>

> **Warning:**
>
> This configuration is an experimental feature. It is not recommended to use it in production environments.

+ The threshold ratio at which PD tries to trigger GC. When the memory usage of PD reaches the value of `server-memory-limit` * the value of `server-memory-limit-gc-trigger`, PD triggers a Golang GC. Only one GC is triggered in one minute.
+ Default value: `0.7`
+ Minimum value: `0.5`
+ Maximum value: `0.99`

### `enable-gogc-tuner` <span class="version-mark">New in v6.6.0</span>

> **Warning:**
>
> This configuration is an experimental feature. It is not recommended to use it in production environments.

+ Controls whether to enable the GOGC Tuner.
+ Default value: `false`

### `gc-tuner-threshold` <span class="version-mark">New in v6.6.0</span>

> **Warning:**
>
> This configuration is an experimental feature. It is not recommended to use it in production environments.

+ The maximum memory threshold ratio for tuning GOGC. When the memory exceeds this threshold, i.e. the value of `server-memory-limit` * the value of `gc-tuner-threshold`, GOGC Tuner stops working.
+ Default value: `0.6`
+ Minimum value: `0`
+ Maximum value: `0.9`

### `flow-round-by-digit` <span class="version-mark">New in TiDB 5.1</span>

+ Default value: 3
+ PD rounds the lowest digits of the flow number, which reduces the update of statistics caused by the changes of the Region flow information. This configuration item is used to specify the number of lowest digits to round for the Region flow information. For example, the flow `100512` will be rounded to `101000` because the default value is `3`. This configuration replaces `trace-region-flow`.

> **Note:**
>
> If you have upgraded your cluster from a TiDB 4.0 version to the current version, the behavior of `flow-round-by-digit` after the upgrading and the behavior of `trace-region-flow` before the upgrading are consistent by default. This means that if the value of `trace-region-flow` is false before the upgrading, the value of `flow-round-by-digit` after the upgrading is 127; if the value of `trace-region-flow` is `true` before the upgrading, the value of `flow-round-by-digit` after the upgrading is `3`.

## security

Configuration items related to security

### `cacert-path`

+ The path of the CA file
+ Default value: ""

### `cert-path`

+ The path of the Privacy Enhanced Mail (PEM) file that contains the X509 certificate
+ Default value: ""

### `key-path`

+ The path of the PEM file that contains the X509 key
+ Default value: ""

### `redact-info-log` <span class="version-mark">New in v5.0</span>

+ Controls whether to enable log redaction in the PD log
+ When you set the configuration value to `true`, user data is redacted in the PD log.
+ Default value: `false`

## `log`

Configuration items related to log

### `level`

+ Specifies the level of the output log
+ Optional value: `"debug"`, `"info"`, `"warn"`, `"error"`, `"fatal"`
+ Default value: `"info"`

### `format`

+ The log format
+ Optional value: `"text"`, `"json"`
+ Default value: `"text"`

### `disable-timestamp`

+ Whether to disable the automatically generated timestamp in the log
+ Default value: `false`

## `log.file`

Configuration items related to the log file

### `max-size`

+ The maximum size of a single log file. When this value is exceeded, the system automatically splits the log into several files.
+ Default value: `300`
+ Unit: MiB
+ Minimum value: `1`

### `max-days`

+ The maximum number of days in which a log is kept
+ If the configuration item is not set, or the value of it is set to the default value 0, PD does not clean log files.
+ Default value: `0`

### `max-backups`

+ The maximum number of log files to keep
+ If the configuration item is not set, or the value of it is set to the default value 0, PD keeps all log files.
+ Default value: `0`

## `metric`

Configuration items related to monitoring

### `interval`

+ The interval at which monitoring metric data is pushed to Prometheus
+ Default value: `15s`

## `schedule`

Configuration items related to scheduling

### `max-merge-region-size`

+ Controls the size limit of `Region Merge`. When the Region size is greater than the specified value, PD does not merge the Region with the adjacent Regions.
+ Default value: `20`
+ Unit: MiB

### `max-merge-region-keys`

+ Specifies the upper limit of the `Region Merge` key. When the Region key is greater than the specified value, the PD does not merge the Region with its adjacent Regions.
+ Default value: `200000`

### `patrol-region-interval`

+ Controls the running frequency at which `replicaChecker` checks the health state of a Region. The smaller this value is, the faster `replicaChecker` runs. Normally, you do not need to adjust this parameter.
+ Default value: `10ms`

### `split-merge-interval`

+ Controls the time interval between the `split` and `merge` operations on the same Region. That means a newly split Region will not be merged for a while.
+ Default value: `1h`

### `max-snapshot-count`

+ Controls the maximum number of snapshots that a single store receives or sends at the same time. PD schedulers depend on this configuration to prevent the resources used for normal traffic from being preempted.
+ Default value value: `64`

### `max-pending-peer-count`

+ Controls the maximum number of pending peers in a single store. PD schedulers depend on this configuration to prevent too many Regions with outdated logs from being generated on some nodes.
+ Default value: `64`

### `max-store-down-time`

+ The downtime after which PD judges that the disconnected store cannot be recovered. When PD fails to receive the heartbeat from a store after the specified period of time, it adds replicas at other nodes.
+ Default value: `30m`

### `max-store-preparing-time` <span class="version-mark">New in v6.1.0</span>

+ Controls the maximum waiting time for the store to go online. During the online stage of a store, PD can query the online progress of the store. When the specified time is exceeded, PD assumes that the store has been online and cannot query the online progress of the store again. But this does not prevent Regions from transferring to the new online store. In most scenarios, you do not need to adjust this parameter.
+ Default value: `48h`

### `leader-schedule-limit`

+ The number of Leader scheduling tasks performed at the same time
+ Default value: `4`

### `region-schedule-limit`

+ The number of Region scheduling tasks performed at the same time
+ Default value: `2048`

### `enable-diagnostic` <span class="version-mark">New in v6.3.0</span>

+ Controls whether to enable the diagnostic feature. When it is enabled, PD records the state during scheduling to help diagnose. If enabled, it might slightly affect the scheduling speed and consume more memory when there are many stores.
+ Default value: false

### `hot-region-schedule-limit`

+ Controls the hot Region scheduling tasks that are running at the same time. It is independent of the Region scheduling.
+ Default value: `4`

### `hot-region-cache-hits-threshold`

+ The threshold used to set the number of minutes required to identify a hot Region. PD can participate in the hotspot scheduling only after the Region is in the hotspot state for more than this number of minutes.
+ Default value: `3`

### `replica-schedule-limit`

+ The number of Replica scheduling tasks performed at the same time
+ Default value: `64`

### `merge-schedule-limit`

+ The number of the `Region Merge` scheduling tasks performed at the same time. Set this parameter to `0` to disable `Region Merge`.
+ Default value: `8`

### `high-space-ratio`

+ The threshold ratio below which the capacity of the store is sufficient. If the space occupancy ratio of the store is smaller than this threshold value, PD ignores the remaining space of the store when performing scheduling, and balances load mainly based on the Region size. This configuration takes effect only when `region-score-formula-version` is set to `v1`.
+ Default value: `0.7`
+ Minimum value: greater than `0`
+ Maximum value: less than `1`

### `low-space-ratio`

+ The threshold ratio above which the capacity of the store is insufficient. If the space occupancy ratio of a store exceeds this threshold value, PD avoids migrating data to this store as much as possible. Meanwhile, to avoid the disk space of the corresponding store being exhausted, PD performs scheduling mainly based on the remaining space of the store.
+ Default value: `0.8`
+ Minimum value: greater than `0`
+ Maximum value: less than `1`

### `tolerant-size-ratio`

+ Controls the `balance` buffer size
+ Default value: `0` (automatically adjusts the buffer size)
+ Minimum value: `0`

### `enable-cross-table-merge`

+ Determines whether to enable the merging of cross-table Regions
+ Default value: `true`

### `region-score-formula-version` <span class="version-mark">New in v5.0</span>

+ Controls the version of the Region score formula
+ Default value: `v2`
+ Optional values: `v1` and `v2`. Compared to v1, the changes in v2 are smoother, and the scheduling jitter caused by space reclaim is improved.

> **Note:**
>
> If you have upgraded your cluster from a TiDB 4.0 version to the current version, the new formula version is automatically disabled by default to ensure consistent PD behavior before and after the upgrading. If you want to change the formula version, you need to manually switch through the `pd-ctl` setting. For details, refer to [PD Control](/pd-control.md#config-show--set-option-value--placement-rules).

### `enable-joint-consensus` <span class="version-mark">New in v5.0</span>

+ Controls whether to use Joint Consensus for replica scheduling. If this configuration is disabled, PD schedules one replica at a time.
+ Default value: `true`

### `hot-regions-write-interval` <span class="version-mark">New in v5.4.0</span>

+ The time interval at which PD stores hot Region information.
+ Default value: `10m`

> **Note:**
>
> The information about hot Regions is updated every three minutes. If the interval is set to less than three minutes, updates during the interval might be meaningless.

### `hot-regions-reserved-days` <span class="version-mark">New in v5.4.0</span>

+ Specifies how many days the hot Region information is retained.
+ Default value: `7`

## `replication`

Configuration items related to replicas

### `max-replicas`

+ The number of replicas, that is, the sum of the number of leaders and followers. The default value `3` means 1 leader and 2 followers. When this configuration is modified dynamically, PD will schedule Regions in the background so that the number of replicas matches this configuration.
+ Default value: `3`

### `location-labels`

+ The topology information of a TiKV cluster
+ Default value: `[]`
+ [Cluster topology configuration](/schedule-replicas-by-topology-labels.md)

### `isolation-level`

+ The minimum topological isolation level of a TiKV cluster
+ Default value: `""`
+ [Cluster topology configuration](/schedule-replicas-by-topology-labels.md)

### `strictly-match-label`

+ Enables the strict check for whether the TiKV label matches PD's `location-labels`.
+ Default value: `false`

### `enable-placement-rules`

+ Enables `placement-rules`.
+ Default value: `true`
+ See [Placement Rules](/configure-placement-rules.md).

## `label-property`

Configuration items related to labels

### `key`

+ The label key for the store that rejected the Leader
+ Default value: `""`

### `value`

+ The label value for the store that rejected the Leader
+ Default value: `""`

## `dashboard`

Configuration items related to the [TiDB Dashboard](/dashboard/dashboard-intro.md) built in PD.

### `tidb-cacert-path`

+ The path of the root CA certificate file. You can configure this path when you connect to TiDB's SQL services using TLS.
+ Default value: `""`

### `tidb-cert-path`

+ The path of the SSL certificate file. You can configure this path when you connect to TiDB's SQL services using TLS.
+ Default value: `""`

### `tidb-key-path`

+ The path of the SSL private key file. You can configure this path when you connect to TiDB's SQL services using TLS.
+ Default value: `""`

### `public-path-prefix`

+ When TiDB Dashboard is accessed behind a reverse proxy, this item sets the public URL path prefix for all web resources.
+ Default value: `/dashboard`
+ Do **not** modify this configuration item when TiDB Dashboard is accessed not behind a reverse proxy; otherwise, access issues might occur. See [Use TiDB Dashboard behind a Reverse Proxy](/dashboard/dashboard-ops-reverse-proxy.md) for details.

### `enable-telemetry`

+ Determines whether to enable the telemetry collection feature in TiDB Dashboard.
+ Default value: `false`
+ See [Telemetry](/telemetry.md) for details.

## `replication-mode`

Configuration items related to the replication mode of all Regions. See [Enable the DR Auto-Sync mode](/two-data-centers-in-one-city-deployment.md#enable-the-dr-auto-sync-mode) for details.
