---
title: Data Migration Monitoring Metrics
summary: Learn about the monitoring metrics when you use Data Migration to replicate data.
category: operations
---

# Data Migration Monitoring Metrics

If your DM cluster is deployed using DM-Ansible, the [monitoring system](../tools/data-migration-practice.md#step-7-monitor-the-task-and-check-logs) is also deployed at the same time. This document describes the monitoring metrics provided by DM-worker.

> **Note:**
>
> Currently, DM-master does not provide monitoring metrics yet.

## Task

| Metric name | Description | Alert |
|----|------------|----|
| task state | the state of subtasks | 10 minutes after subtasks become paused |

## Relay log

| Metric name | Description | Alert |
|----|------------|----|
| storage capacity | The storage capacity of the disk occupied by the relay log | N/A |
| storage remain | The remaining storage capacity of the disk occupied by the relay log | An alert is needed once the value is smaller than 10G. |
| process exits with error | The relay log encounters an error within the DM-worker and exits. | Immediate alerts |
| relay log data corruption | The number of corrupted relay log files | Immediate alerts |
| fail to read binlog from master | The number of errors encountered when the relay log reads the binlog from the upstream MySQL | Immediate alerts |
| fail to write relay log | The number of errors encountered when the relay log writes the binlog to disks | Immediate alerts |
| binlog file index | The largest index number of relay log files. For example, "value = 1" indicates "relay-log.000001". | N/A |
| binlog file gap between master and relay | The number of binlog files in the relay log that are behind the upstream master | When the number of binlog files in relay that are behind the upstream master exceeds one (>1) and the condition lasts over 10 minutes |
| binlog pos | The write offset of the latest relay log file | N/A |
| read binlog duration | The duration that the relay log reads binlog from the upstream MySQL (in seconds) |  N/A |
| write relay log duration | The duration that the relay log writes binlog into the disks each time (in seconds) | N/A |
| binlog size | The size of a single binlog event that the relay log writes into the disks | N/A |

## Dumper

The following metric shows only when `task-mode` is in the `full` or `all` mode.

| Metric name | Description | Alert |
|----|------------|----|
| dump process exits with error | Dumper encounters an error within the DM-worker and exits. | Immediate alerts |

## Loader

The following metrics show only when `task-mode` is in the `full` or `all` mode.

| Metric name | Description | Alert |
|----|------------|----|
| load progress | The data import process percentage of Loader. The value range is 0% ~ 100%. | N/A |
| data file size | The total size of the data files in the full data imported by Loader (including the `INSERT INTO` statement) | N/A |
| load process exits with error | Loader encounters an error within the DM-worker and exits. | Immediate alerts |
| table count | The total number of tables in the full data imported by Loader | N/A |
| data file count | The total number of data files in the full data imported by Loader (including the `INSERT INTO` statement) | N/A |
| latency of execute transaction | The duration that Loader executes a transaction (in seconds) | N/A |
| latency of query | The duration that Loader executes a query (in seconds) | N/A |

## Binlog replication

The following metrics show only when `task-mode` is in the `incremental` or `all` mode.

| Metric name | Description | Alert |
|----|------------|----|
| remaining time to sync | The predicted remaining time it takes Syncer to be completely replicated with the master (in minutes) | N/A |
| replicate lag | The latency time it takes to replicate the binlog from master to Syncer (in seconds) | N/A |
| process exist with error | The binlog replication process encounters an error within the DM-worker and exits. | Immediate alerts |
| binlog file gap between master and syncer | The number of binlog files in Syncer that are behind the master | When the number of binlog files in Syncer that are behind the master exceeds one (>1) and the condition lasts over 10 minutes |
| binlog file gap between relay and syncer | The number of binlog files in Syncer that are behind relay | When the number of binlog files in Syncer that are behind relay exceeds one (>1) and the condition lasts over 10 minutes |
| binlog event qps | The number of binlog events received per unit of time (this number does not include the events that need to be skipped) | N/A |
| skipped binlog event qps | The number of binlog events received per unit of time that need to be skipped | N/A |
| cost of binlog event transform | The time it takes Syncer to parse and transform the binlog into SQL statements (in seconds) | N/A |
| total sqls jobs | The number of newly added jobs per unit of time | N/A |
| finished sqls jobs | The number of finished jobs per unit of time | N/A |
| execution latency | The time it takes Syncer to execute the transaction to the downstream (in seconds) | N/A |