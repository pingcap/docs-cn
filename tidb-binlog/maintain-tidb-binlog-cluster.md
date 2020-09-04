---
title: TiDB Binlog Cluster Operations
summary: Learn how to operate the cluster version of TiDB Binlog.
aliases: ['/docs/dev/tidb-binlog/maintain-tidb-binlog-cluster/','/docs/dev/reference/tidb-binlog/maintain/','/docs/dev/how-to/maintain/tidb-binlog/']
---

# TiDB Binlog Cluster Operations

This document introduces the following TiDB Binlog cluster operations:

+ The state of a Pump and Drainer nodes
+ Starting or exiting a Pump or Drainer process
+ Managing the TiDB Binlog cluster by using the binlogctl tool or by directly performing SQL operations in TiDB

## Pump or Drainer state

Pump or Drainer state description:

* `online`: running normally
* `pausing`: in the pausing process
* `paused`: has been stopped
* `closing`: in the offline process
* `offline`: has been offline

> **Note:**
>
> The state information of a Pump or Drainer node is maintained by the service itself and is regularly updated to the Placement Driver (PD).

## Starting and exiting a Pump or Drainer process

### Pump

* Starting: When started, the Pump node notifies all Drainer nodes in the `online` state. If the notification is successful, the Pump node sets its state to `online`. Otherwise, the Pump node reports an error, sets its state to `paused` and exits the process.
* Exiting: The Pump node enters the `paused` or `offline` state before the process is exited normally; if the process is exited abnormally (caused by the `kill -9` command, process panic, crash), the node is still in the `online` state.
    * Pause: You can pause a Pump process by using the `kill` command (not `kill -9`), pressing <kbd>Ctrl</kbd>+<kbd>C</kbd> or using the `pause-pump` command in the binlogctl tool. After receiving the pause instruction, the Pump node sets its state to `pausing`, stops receiving binlog write requests and stops providing binlog data to Drainer nodes. After all threads are safely exited, the Pump node updates its state to `paused` and exits the process.
    * Offline: You can close a Pump process only by using the `offline-pump` command in the binlogctl tool. After receiving the offline instruction, the Pump node sets its state to `closing` and stops receiving the binlog write requests. The Pump node continues providing binlog to Drainer nodes until all binlog data is consumed by Drainer nodes. Then, the Pump node sets its state to `offline` and exits the process.

### Drainer

* Starting: When started, the Drainer node sets its state to `online` and tries to pull binlogs from all Pump nodes which are not in the `offline` state. If it fails to get the binlogs, it keeps trying.
* Exiting: The Drainer node enters the `paused` or `offline` state before the process is exited normally; if the process is exited abnormally (caused by `kill -9`, process panic, crash), the Drainer node is still in the `online` state.
    * Pause: You can pause a Drainer process by using the `kill` command (not `kill -9`), pressing <kbd>Ctrl</kbd>+<kbd>C</kbd> or using the `pause-drainer` command in the binlogctl tool. After receiving the pause instruction, the Drainer node sets its state to `pausing` and stops pulling binlogs from Pump nodes. After all threads are safely exited, the Drainer node sets its state to `paused` and exits the process.
    * Offline: You can close a Drainer process only by using the `offline-drainer` command in the binlogctl tool. After receiving the offline instruction, the Drainer node sets its state to `closing` and stops pulling binlogs from Pump nodes. After all threads are safely exited, the Drainer node updates its state to `offline` and exits the process.

For how to pause, close, check, and modify the state of Drainer, see the [binlogctl guide](/tidb-binlog/binlog-control.md).

## Use `binlogctl` to manage Pump/Drainer

[`binlogctl`](https://github.com/pingcap/tidb-binlog/tree/master/binlogctl) is an operations tool for TiDB Binlog with the following features:

* Checking the state of Pump or Drainer
* Pausing or closing Pump or Drainer
* Handling the abnormal state of Pump or Drainer

For detailed usage of `binlogctl`, refer to [binlogctl overview](/tidb-binlog/binlog-control.md).

## Use SQL statements to manage Pump or Drainer

To view or modify binlog related states, execute corresponding SQL statements in TiDB.

- Check whether binlog is enabled:

    {{< copyable "sql" >}}

    ```sql
    show variables like "log_bin";
    ```

    ```
    +---------------+-------+
    | Variable_name | Value |
    +---------------+-------+
    | log_bin       |  0   |
    +---------------+-------+
    ```
    
    When the Value is `0`, binlog is enabled. When the Value is `1`, binlog is disabled.

- Check the status of all the Pump or Drainer nodes:

    {{< copyable "sql" >}}

    ```sql
    show pump status;
    ```

    ```
    +--------|----------------|--------|--------------------|---------------------|
    | NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
    +--------|----------------|--------|--------------------|---------------------|
    | pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-05-01 00:00:01 |
    +--------|----------------|--------|--------------------|---------------------|
    | pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
    +--------|----------------|--------|--------------------|---------------------|
    ```

    {{< copyable "sql" >}}

    ```sql
    show drainer status;
    ```

    ```
    +----------|----------------|--------|--------------------|---------------------|
    |  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
    +----------|----------------|--------|--------------------|---------------------|
    | drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-05-01 00:00:03 |
    +----------|----------------|--------|--------------------|---------------------|
    | drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
    +----------|----------------|--------|--------------------|---------------------|
    ```

- Modify the state of a Pump or Drainer node in abnormal situations

    {{< copyable "sql" >}}

    ```sql
    change pump to node_state ='paused' for node_id 'pump1';
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    change drainer to node_state ='paused' for node_id 'drainer1';
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    Executing the above SQL statements works the same as the `update-pump` or `update-drainer` commands in binlogctl. Use the above SQL statements **only** when the Pump or Drainer node is in abnormal situations.

> **Note:**
>
> - Checking whether binlog is enabled and the running status of Pump or Drainer is supported in TiDB v2.1.7 and later versions.
> - Modifying the status of Pump or Drainer is supported in TiDB v3.0.0-rc.1 and later versions. This feature only supports modifying the status of Pump or Drainer nodes stored in PD. To pause or close the node, use the `binlogctl` tool.
