---
title: Handle Alerts in TiDB Data Migration
summary: Understand how to deal with the alert information in DM.
---

# Handle Alerts in TiDB Data Migration

This document introduces how to deal with the alert information in DM.

## Alerts related to high availability

### `DM_master_all_down`

- Description:

    If all DM-master nodes are offline, this alert is triggered.

- Solution:

    You can take the following steps to handle the alert:

    1. Check the environment of the cluster.
    2. Check the logs of all DM-master nodes for troubleshooting.

### `DM_worker_offline`

- Description:

    If a DM-worker node is offline for more than one hour, this alert is triggered. In a high-availability architecture, this alert might not directly interrupt the task but increases the risk of interruption.

- Solution:

    You can take the following steps to handle the alert:

    1. View the working status of the corresponding DM-worker node.
    2. Check whether the node is connected.
    3. Troubleshoot errors through logs.

### `DM_DDL_error`

- Description:

    This error occurs when DM is processing the sharding DDL operations.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

### `DM_pending_DDL`

- Description:

    If a sharding DDL operation is pending for more than one hour, this alert is triggered.

- Solution:

    In some scenarios, the pending sharding DDL operation might be what users expect. Otherwise, refer to [Handle Sharding DDL Locks Manually in DM](/dm/manually-handling-sharding-ddl-locks.md) for solution.

## Alert rules related to task status

### `DM_task_state`

- Description:

    When a sub-task of DM-worker is in the `Paused` state for over 20 minutes, an alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

## Alert rules related to relay log

### `DM_relay_process_exits_with_error`

- Description:

    When the relay log processing unit encounters a non-autorecoverable error (for example, binlog files not found), or when it encounters multiple recoverable errors (for example, network problems) in a short period of time (for example, more than 3 times in 2 minutes), this alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

### `DM_remain_storage_of_relay_log`

- Description:

    When the free space of the disk where the relay log is located is less than 10G, an alert is triggered.

- Solutions:

    You can take the following methods to handle the alert:

    - Delete unwanted data manually to increase free disk space.
    - Reconfigure the [automatic data purge strategy of the relay log](/dm/relay-log.md#automatic-data-purge) or [purge data manually](/dm/relay-log.md#manual-data-purge).
    - Execute the command `pause-relay` to pause the relay log pulling process. After there is enough free disk space, resume the process by running the command `resume-relay`. Note that you must not purge upstream binlog files that have not been pulled after the relay log pulling process is paused.

### `DM_relay_log_data_corruption`

- Description:

    When the relay log processing unit validates the binlog event read from the upstream and detects abnormal checksum information, this unit moves to the `Paused` state, and an alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

### `DM_fail_to_read_binlog_from_master`

- Description:

    If an error occurs when the relay log processing unit tries to read the binlog event from the upstream, this unit moves to the `Paused` state, and an alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

### `DM_fail_to_write_relay_log`

- Description:

    If an error occurs when the relay log processing unit tries to write the binlog event into the relay log file, this unit moves to the `Paused` state, and an alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

### `DM_binlog_file_gap_between_master_relay`

- Description:

    When the number of the binlog files in the current upstream MySQL/MariaDB exceeds that of the latest binlog files pulled by the relay log processing unit by **more than** 1 for 10 minutes, and an alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

## Alert rules related to Dump/Load

### `DM_dump_process_exists_with_error`

- Description:

    When the Dump processing unit encounters a non-autorecoverable error (for example, binlog files not found), or when it encounters multiple recoverable errors (for example, network problems) in a short period of time (for example, more than 3 times in 2 minutes), this alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

### `DM_load_process_exists_with_error`

- Description:

    When the Load processing unit encounters a non-autorecoverable error (for example, binlog files not found), or when it encounters multiple recoverable errors (for example, network problems) in a short period of time (for example, more than 3 times in 2 minutes), this alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

## Alert rules related to binlog replication

### `DM_sync_process_exists_with_error`

- Description:

    When the binlog replication processing unit encounters a non-autorecoverable error (for example, binlog files not found), or when it encounters multiple recoverable errors (for example, network problems) in a short period of time (for example, more than 3 times in 2 minutes), this alert is triggered.

- Solution:

    Refer to [Troubleshoot DM](/dm/dm-error-handling.md#troubleshooting).

### `DM_binlog_file_gap_between_master_syncer`

- Description:

    When the number of the binlog files in the current upstream MySQL/MariaDB exceeds that of the latest binlog files processed by the relay log processing unit by **more than** 1 for 10 minutes, an alert is triggered.

- Solution:

    Refer to [Handle Performance Issues](/dm/dm-handle-performance-issues.md).

### `DM_binlog_file_gap_between_relay_syncer`

- Description:

    When the number of the binlog files in the current relay log processing unit exceeds that of the latest binlog files processed by the binlog replication processing unit by **more than** 1 for 10 minutes, an alert is triggered.

- Solution:

    Refer to [Handle Performance Issues](/dm/dm-handle-performance-issues.md).
