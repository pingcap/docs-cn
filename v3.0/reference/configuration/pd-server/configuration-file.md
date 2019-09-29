---
title: PD Configuration File
summary: Learn the PD configuration file.
category: reference
---

# PD Configuration File

<!-- markdownlint-disable MD001 -->

The PD configuration file supports more options than command-line parameters. You can find the default configuration file [here](https://github.com/pingcap/pd/blob/master/conf/config.toml).

This document only describes parameters that are not included in command-line parameters. Check [here](/v3.0/reference/configuration/pd-server/configuration.md) for the command line parameters.

### `lease`

+ The timeout of the PD Leader Key lease. After the timeout, the system re-elects a Leader.
+ Default value: `3`
+ unit: second

### `tso-save-interval`

+ The interval for PD to allocate TSOs for persistent storage in etcd
+ Default value: `3` seconds

### `initial-cluster-state`

+ The initial state of the cluster
+ Default value: `new`

### `enable-prevote`

+ Enables or disables `raft prevote`
+ Default value: `true`

### `quota-backend-bytes`

+ The storage size of the meta-information database, which is 2GB by default
+ Default value: `2147483648`

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

### `tick-interval`

+ The tick period of etcd Raft
+ Default value: `100ms`

### `election-interval`

+ The timeout for the etcd leader election
+ Default value: `3s`

### `use-region-storage`

+ Enables or disables independent Region storage
+ Default value: `false`

## `log`

Configuration items related to log

### `format`

+ The log format, which can be specified as "text", "json", or "console"
+ Default value: `text`

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
+ Default value: `28`
+ Minimum value: `1`

### `max-backups`

+ The maximum number of log files to keep
+ Default value: `7`
+ Minimum value: `1`

## `metric`

Configuration items related to monitoring

### `interval`

+ The interval at which monitoring metric data is pushed to Promethus
+ Default value: `15s`

## `schedule`

Configuration items related to scheduling

### `max-merge-region-size`

+ Controls the size limit of `Region Merge`. When the Region size is greater than the specified value, PD does not merge the Region with the adjacent Regions.
+ Default value: `20`

### `max-merge-region-keys`

+ Specifies the upper limit of the `Region Merge` key. When the Region key is greater than the specified value, the PD does not merge the Region with its adjacent Regions.
+ Default value: `200000`

### `patrol-region-interval`

+ Controls the running frequency at which `replicaChecker` checks the health state of a Region. The smaller this value is, the faster `replicaChecker` runs. Normally, you do not need to adjust this parameter.
+ Default value: `100ms`

### `split-merge-interval`

+ Controls the time interval between the `split` and `merge` operations on the same Region. That means a newly split Region will not be merged for a while.
+ Default value: `1h`

### `max-snapshot-count`

+ Control the maximum number of snapshots that a single store receives or sends at the same time. PD schedulers depend on this configuration to prevent the resources used for normal traffic from being preempted.
+ Default value value: `3`

### `max-pending-peer-count`

+ Controls the maximum number of pending peers in a single store. PD schedulers depend on this configuration to prevent too many Regions with outdated logs from being generated on some nodes.
+ Default value: `16`

### `max-store-down-time`

+ The downtime after which PD judges that the disconnected store can not be recovered. When PD fails to receive the heartbeat from a store after the specified period of time, it adds replicas at other nodes.
+ Default value: `30m`

### `leader-schedule-limit`

+ The number of Leader scheduling tasks performed at the same time
+ Default value: `4`

### `region-schedule-limit`

+ The number of Region scheduling tasks performed at the same time
+ Default value: `4`

### `replica-schedule-limit`

+ The number of Replica scheduling tasks performed at the same time
+ Default value: `8`

### `merge-schedule-limit`

+ The number of the `Region Merge` scheduling tasks performed at the same time. Set this parameter to `0` to disable `Region Merge`.
+ Default value: `8`

### `high-space-ratio`

+ The threshold ratio below which the capacity of the store is sufficient
+ Default value: `0.6`
+ Minimum value: greater than `0`
+ Maximum value: less than `1`

### `low-space-ratio`

+ The threshold ratio above which the capacity of the store is insufficient
+ Default value: `0.8`
+ Minimum value: greater than `0`
+ Maximum value: less than `1`

### `tolerant-size-ratio`

+ Controls the `balance` buffer size
+ Default value: `5`
+ Minimum value: `0`

### `disable-remove-down-replica`

+ Determines whether to disable the feature that automatically removes `DownReplica`. When this parameter is set to `true`, PD does not automatically clean up the copy in the down state.
+ Default value: `false`

### `disable-replace-offline-replica`

+ Determines whether to disable the feature that migrates `OfflineReplica`. When this parameter is set to `true`, PD does not migrate the replicas in the offline state.
+ Default value: `false`

### `disable-make-up-replica`

+ Determines whether to disable the feature that automatically supplements replicas. When this parameter is set to `true`, PD does not supplement replicas for the Region with insufficient replicas.
+ Default value: `false`

### `disable-remove-extra-replica`

+ Determines whether to disable the feature that removes extra replicas. When this parameter is set to `true`, PD does not remove the extra replicas from the Region with excessive replicas.
+ Default value: `false`

### `disable-location-replacement`

+ Determines whether to disable isolation level check. When this parameter is set to `true`, PD does not increase the isolation level of the Region replicas through scheduling.
+ Default value: `false`

## `replication`

Configuration items related to replicas

### `max-replicas`

+ The number of replicas
+ Default value: `3`

### `location-labels`

+ The topology information of a TiKV cluster
+ Default value: `[]`

## `label-property`

Configuration items related to labels

### `key`

+ The label key for the store that rejected the Leader
+ Default value: `""`

### `value`

+ The label value for the store that rejected the Leader
+ Default value: `""`
