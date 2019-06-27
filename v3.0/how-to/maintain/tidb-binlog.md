---
title: TiDB Binlog Cluster Operations
summary: Learn how to operate the cluster version of TiDB Binlog.
category: reference
aliases: ['/docs/tools/binlog/operation/','/docs/dev/reference/tools/tidb-binlog/operation/']
---

# TiDB Binlog Cluster Operations

## Pump or Drainer state

Pump or Drainer state description:

* `online`: running normally.
* `pausing`: in the pausing process. It turns into this state after you use `kill` or press Ctrl + C to exit from the process. When Pump or Drainer exits all internal threads in safe, it becomes `paused`.
* `paused`: has been stopped. While Pump is in this state, it rejects the request of writing binlog into it and does not provide the binlog for Drainer any more. When Drainer is in this state, it does not replicate data to the downstream. After Pump and Drainer exit normally from all the threads, they switch the state to `paused` and then exits from the process.
* `closing`: in the offline process. The `binlogctl` is used to get Pump or Drainer offline and Pump or Drainer is in this state before the process exits. In this state, Pump does not accept new requests of writing binlog into it and waits for all the binlog data to be used up by Drainer.
* `offline`: becomes offline. After Pump sends all the binlog data that it saves to Drainer, its state is switched to `offline`.

> **Note:**
>
> * When Pump or Drainer is `pausing` or `paused`, the data replication is interrupted.
> * Pump and Drainer have several states, including `online`, `paused`, and `offline`. If you press Ctrl + C or `kill` the process, both Pump and Drainer become `pausing` then finally turn to `paused` . There is no need for Pump to send all the binlog data to Drainer before it become `paused` while Pump need to send all the binlog data to Drainer before it become `offline` . If you need to exit from Pump for a long period of time (or are permanently removing Pump from the cluster), use `binlogctl` to make Pump offline. The same goes for Drainer.
> * When Pump is `closing`, you need to guarantee that all the data has been consumed by all the Drainers that are not `offline`. So before making Pump offline, you need to guarantee all the Drainers are `online`. Otherwise, Pump cannot get offline normally.
> * The binlog data that Pump saves is processed by GC only when it has been consumed by all the Drainers that are not `offline`.
> * Close Drainer only when it will not be used any more.

For how to pause, close, check, and modify the state of Drainer, see the [binlogctl guide](#binlogctl-guide) as follows.

## `binlogctl` guide

[`binlogctl`](https://github.com/pingcap/tidb-tools/tree/master/tidb-binlog/binlogctl) is an operations tool for TiDB Binlog with the following features:

* Obtaining the current `tso` of TiDB cluster
* Checking the state of Pump or Drainer
* Modifying the state of Pump or Drainer
* Pausing or closing Pump or Drainer

### Usage scenarios of `binlogctl`

* It is the first time you run Drainer and you need to obtain the current `tso` of TiDB cluster.
* When Pump or Drainer exits abnormally, its state is not updated and the service is affected. You can use this tool to modify the state.
* An error occurs during data replication and you need to check the running status and state of Pump or Drainer.
* While maintaining the cluster, you need to pause or close Pump or Drainer.

### Download `binlogctl`

Your distribution of TiDB or TiDB Binlog may already include binlogctl. If not, download `binlogctl`:

```bash
wget https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz
wget https://download.pingcap.org/tidb-{version}-linux-amd64.sha256

# Check the file integrity. If the result is OK, the file is correct.
sha256sum -c tidb-{version}-linux-amd64.sha256
```

### `binlogctl` usage description

Command line parameters:

```
Usage of binlogctl:
-V
    Outputs the binlogctl version information
-cmd string
    the command mode, including "generate_meta", "pumps", "drainers", "update-pump" ,"update-drainer", "pause-pump", "pause-drainer", "offline-pump", and "offline-drainer"
-data-dir string
    the file path where the checkpoint file of Drainer is stored ("binlog_position" by default)
-node-id string
    ID of Pump or Drainer
-pd-urls string
    the address of PD. If multiple addresses exist, use "," to separate each ("http://127.0.0.1:2379" by default)
-ssl-ca string
    the file path of SSL CAs
-ssl-cert string
    the file path of the X509 certificate file in the PEM format
-ssl-key string
    the file path of X509 key file of the PEM format
-time-zone string
    If a time zone is set, the corresponding time of the obtained `tso` is printed in the "generate_meta" mode. For example, "Asia/Shanghai" is the CST time zone and "Local" is the local time zone
```
Command example:

- Check the state of all the Pump or Drainer nodes:

    Set `cmd` as `pumps` or `drainers` to check the state of all the Pump or Drainer nodes. For example,

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pumps

    INFO[0000] pump: {NodeID: ip-172-16-30-67:8250, Addr: 172.16.30.192:8250, State: online, MaxCommitTS: 405197570529820673, UpdateTime: 2018-12-25 14:23:37 +0800 CST}
    ```

- Modify the state of Pump or Drainer:

    Set `cmd` as `update-pump` or `update-drainer` to modify the states of Pump or Drainer, which can be `online`, `pausing`, `paused`, `closing` or `offline`.

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd update-pump -node-id ip-127-0-0-1:8250 -state paused
    ```

    This command modifies the state of Pump or Drainer saved in the Placement Driver (PD).

- Pause or close Pump or Drainer:

    - Set `cmd` as `pause-pump` or `pause-drainer` to pause Pump or Drainer.

    - Set `cmd` as `offline-pump` or `offline-drainer` to close Pump or Drainer.

    For example,

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd pause-pump -node-id ip-127-0-0-1:8250
    ```

    `binlogctl` sends the HTTP request to Pump or Drainer, and Pump or Drainer exits from the process after receiving the command and sets its state to `paused`/`offline`.

- Generate the meta file that Drainer needs to start:

    ```bash
    bin/binlogctl -pd-urls=http://127.0.0.1:2379 -cmd generate_meta

    INFO[0000] [pd] create pd client with endpoints [http://192.168.199.118:32379]
    INFO[0000] [pd] leader switches to: http://192.168.199.118:32379, previous:
    INFO[0000] [pd] init cluster id 6569368151110378289
    2018/06/21 11:24:47 meta.go:117: [info] meta: &{CommitTS:400962745252184065}
    ```

    This command generates a `{data-dir}/savepoint` file. This file stores the `tso` information which is needed for the initial start of Drainer.

## Use SQL statements to manage Pump or Drainer

To view or modify binlog related states, execute corresponding SQL statements in TiDB.

- Check whether binlog is enabled:

    ```bash
    mysql> show variables like "log_bin";
    +---------------+-------+
    | Variable_name | Value |
    +---------------+-------+
    | log_bin       |  ON   |
    +---------------+-------+
    ```

    When the Value is `ON`, it means that the binlog is enabled.

- Check the status of all the Pump or Drainer nodes:

    ```bash
    mysql> show pump status;
    +--------|----------------|--------|--------------------|---------------------|
    | NodeID |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
    +--------|----------------|--------|--------------------|---------------------|
    | pump1  | 127.0.0.1:8250 | Online | 408553768673342237 | 2019-05-01 00:00:01 |
    +--------|----------------|--------|--------------------|---------------------|
    | pump2  | 127.0.0.2:8250 | Online | 408553768673342335 | 2019-05-01 00:00:02 |
    +--------|----------------|--------|--------------------|---------------------|
    ```

    ```bash
    mysql> show drainer status;
    +----------|----------------|--------|--------------------|---------------------|
    |  NodeID  |     Address    | State  |   Max_Commit_Ts    |    Update_Time      |
    +----------|----------------|--------|--------------------|---------------------|
    | drainer1 | 127.0.0.3:8249 | Online | 408553768673342532 | 2019-05-01 00:00:03 |
    +----------|----------------|--------|--------------------|---------------------|
    | drainer2 | 127.0.0.4:8249 | Online | 408553768673345531 | 2019-05-01 00:00:04 |
    +----------|----------------|--------|--------------------|---------------------|
    ```

- Modify the states of a Pump or Drainer node:

    ```bach
    mysql> change pump to node_state ='paused' for node_id 'pump1'";
    Query OK, 0 rows affected (0.01 sec)
    ```

    ```bach
    mysql> change drainer to node_state ='paused' for node_id 'drainer1'";
    Query OK, 0 rows affected (0.01 sec)
    ```

> **Note:**
>
> - Checking whether binlog is enabled and the running status of Pump or Drainer is supported in TiDB v2.1.7 and later versions.
> - Modifying the status of Pump or Drainer is supported in TiDB v3.0.0-rc.1 and later versions. This feature only supports modifying the status of Pump or Drainer nodes stored in the Placement Driver (PD). To pause or close the node, use the `binlogctl` tool.
