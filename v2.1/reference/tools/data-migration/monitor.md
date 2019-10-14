---
title: Data Migration Monitoring Metrics
summary: Learn about the monitoring metrics when you use Data Migration to replicate data.
category: reference
---

# Data Migration Monitoring Metrics

If your DM cluster is deployed using DM-Ansible, the [monitoring system](/v2.1/reference/tools/data-migration/deploy.md#step-7-monitor-the-task-and-check-logs) is also deployed at the same time. This document describes the monitoring metrics provided by DM-worker.

> **Note:**
>
> Currently, DM-master does not provide monitoring metrics yet.

## Task

In the Grafana dashboard, the default name of DM is `DM-task`.

### `overview`

`overview` contains some monitoring metrics of all the DM-worker instances in the currently selected task. The current default alert rule is only for a single DM-worker instance.

| Metric name | Description | Alert | Severity level |
|:----|:------------|:----|:----|
| task state | The state of subtasks for replication | N/A | N/A |
| storage capacity | The total storage capacity of the disk occupied by relay logs | N/A | N/A |
| storage remain | The remaining storage capacity of the disk occupied by relay logs | N/A | N/A |
| binlog file gap between master and relay | The number of binlog files by which the `relay` processing unit is behind the upstream master | N/A | N/A |
| load progress | The percentage of the completed loading process of the load unit. The value is between 0%~100% | N/A | N/A |
| binlog file gap between master and syncer | The number of binlog files by which binlog replication is behind the upstream master | N/A | N/A |
| shard lock resolving | Whether the current subtask is waiting for sharding DDL replication. A value greater than 0 means that the current subtask is waiting for sharding DDL replication | N/A | N/A |

### Task state

| Metric name | Description | Alert | Severity level |
|:----|:------------|:----|:----|
| task state | The state of subtasks | An alert occurs when the subtask has been paused for more than 10 minutes | critical |

### Relay log

| Metric name | Description | Alert | Severity level |
|:----|:------------|:----|:----|
| storage capacity | The storage capacity of the disk occupied by the relay log | N/A | N/A |
| storage remain | The remaining storage capacity of the disk occupied by the relay log | An alert is needed once the value is smaller than 10G | critical |
| process exits with error | The relay log encounters an error within the DM-worker and exits | Immediate alerts | critical |
| relay log data corruption | The number of corrupted relay log files | Immediate alerts | emergency |
| fail to read binlog from master | The number of errors encountered when the relay log reads the binlog from the upstream MySQL | Immediate alerts | critical |
| fail to write relay log | The number of errors encountered when the relay log writes the binlog to disks | Immediate alerts | critical |
| binlog file index | The largest index number of relay log files. For example, "value = 1" indicates "relay-log.000001" | N/A | N/A |
| binlog file gap between master and relay | The number of binlog files in the relay log that are behind the upstream master | An alert occurs when the number of binlog files by which the `relay` processing unit is behind the upstream master exceeds one (>1) and the condition lasts over 10 minutes | critical |
| binlog pos | The write offset of the latest relay log file | N/A | N/A |
| read binlog duration | The duration that the relay log reads binlog from the upstream MySQL (in seconds) | N/A | N/A |
| write relay log duration | The duration that the relay log writes binlog into the disks each time (in seconds) | N/A | N/A |
| binlog size | The size of a single binlog event that the relay log writes into the disks | N/A | N/A |

### Dump/Load unit

The following metrics show only when `task-mode` is in the `full` or `all` mode.

| Metric name | Description | Alert | Severity level |
|:----|:------------|:----|:----|
| load progress | The percentage of the completed loading process of the load unit. The value range is 0%~100%. | N/A | N/A |
| data file size | The total size of the data files (includes the `INSERT INTO` statement) in the full data imported by the load unit | N/A | N/A |
| dump process exits with error | The dump unit encounters an error within the DM-worker and exits | Immediate alerts | critical |
| load process exits with error | The load unit encounters an error within the DM-worker and exits | Immediate alerts | critical |
| table count | The total number of tables in the full data imported by the load unit | N/A | N/A |
| data file count | The total number of data files (includes the `INSERT INTO` statement) in the full data imported by the load unit | N/A | N/A |
| latency of execute transaction | The latency of executing a transaction by the load unit (in seconds) | N/A | N/A |
| latency of query | The latency of executing of executing a query by the load unit (in seconds) | N/A | N/A |

### Binlog replication

The following metrics show only when `task-mode` is in the `incremental` or `all` mode.

| Metric name | Description | Alert | Severity level |
|:----|:------------|:----|:----|
| remaining time to sync | The predicted remaining time it takes `syncer` to be completely replicated with the master (in minutes) | N/A | N/A |
| replicate lag | The latency time it takes to replicate the binlog from master to `syncer` (in seconds) | N/A | N/A |
| process exist with error | The binlog replication process encounters an error within the DM-worker and exits | Immediate alerts | critical |
| binlog file gap between master and syncer | The number of binlog files by which the `syncer` processing unit is behind the master | An alert occurs when the number of binlog files by which the `syncer` processing unit is behind the master exceeds one (>1) and the condition lasts over 10 minutes | critical |
| binlog file gap between relay and syncer | The number of binlog files by which `syncer` is behind `relay` | An alert occurs when the number of binlog files by which the `syncer` processing unit is behind the `relay` processing unit exceeds one (>1) and the condition lasts over 10 minutes | critical |
| binlog event qps | The number of binlog events received per unit of time (this number does not include the events that need to be skipped) | N/A | N/A |
| skipped binlog event qps | The number of binlog events received per unit of time that need to be skipped | N/A | N/A |
| cost of binlog event transform | The time it takes `syncer` to parse and transform the binlog into SQL statements (in seconds) | N/A | N/A |
| total sqls jobs | The number of newly added jobs per unit of time | N/A | N/A |
| finished sqls jobs | The number of finished jobs per unit of time | N/A | N/A |
| execution latency | The time it takes `syncer` to execute the transaction to the downstream (in seconds) | N/A | N/A |
| unsynced tables | The number of tables that have not received the shard DDL statement in the current subtask | N/A | N/A |
| shard lock resolving | Whether the current subtask is waiting for the shard DDL lock to be resolved. A value greater than 0 indicates that it is waiting for the shard DDL lock to be resolved | N/A | N/A |

## Instance

In the Grafana dashboard, the default name of an instance is `DM-instance`.

### Relay log

| Metric name | Description | Alert | Severity level |
|:----|:------------|:----|:----|
| storage capacity | The total storage capacity of the disk occupied by the relay log | N/A | N/A |
| storage remain | The remaining storage capacity within the disk occupied by the relay log | An alert occurs once the value is smaller than 10G | critical |
| process exits with error | The relay log encounters an error in DM-worker and exits | Immediate alerts | critical |
| relay log data corruption | The number of corrupted relay logs | Immediate alerts | emergency |
| fail to read binlog from master | The number of errors encountered when relay log reads the binlog from the upstream MySQL | Immediate alerts | critical |
| fail to write relay log | The number of errors encountered when the relay log writes the binlog to disks | Immediate alerts | critical |
| binlog file index | The largest index number of relay log files. For example, "value = 1" indicates "relay-log.000001" | N/A | N/A |
| binlog file gap between master and relay | The number of binlog files by which the `relay` processing unit is behind the upstream master | An alert occurs when the number of binlog files by which the `relay` processing unit is behind the upstream master exceeds one (>1) and the condition lasts over 10 minutes | critical |
| binlog pos | The write offset of the latest relay log file | N/A | N/A |
| read binlog duration | The duration that the relay log reads the binlog from the upstream MySQL (in seconds) | N/A | N/A |
| write relay log duration | The duration that the relay log writes the binlog into the disk each time (in seconds) | N/A | N/A |
| binlog size | The size of a single binlog event that the relay log writes into the disks | N/A | N/A |

### Task

| Metric name | Description | Alert | Severity level |
|:----|:------------|:----|:----|
| task state | The state of subtasks for replication | An alert occurs when the subtask has been paused for more than 10 minutes | critical |
| load progress | The percentage of the completed loading process of the load unit. The value range is 0%~100% | N/A | N/A |
| binlog file gap between master and syncer | The number of binlog files by which binlog replication is behind the upstream master | N/A | N/A |
| shard lock resolving | Whether the current subtask is waiting for sharding DDL replication. A value greater than 0 means that the current subtask is waiting for sharding DDL replication | N/A | N/A |