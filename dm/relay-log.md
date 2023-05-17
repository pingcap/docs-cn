---
title: Data Migration Relay Log
summary: Learn the directory structure, initial migration rules and data purge of DM relay logs.
aliases: ['/docs/tidb-data-migration/dev/relay-log/']
---

# Data Migration Relay Log

The Data Migration (DM) relay log consists of several sets of numbered files containing events that describe database changes, and an index file that contains the names of all used relay log files.

After relay log is enabled, DM-worker automatically migrates the upstream binlog to the local configuration directory (the default migration directory is `<deploy_dir>/<relay_log>` if DM is deployed using TiUP). The default value of `<relay_log>` is `relay-dir` and can be modified in [Upstream Database Configuration File](/dm/dm-source-configuration-file.md). Since v5.4.0, you can configure the local configuration directory through `relay-dir` in the [DM-worker configuration file](/dm/dm-worker-configuration-file.md), which takes precedence over the configuration file of the upstream database.

## User scenarios

In MySQL, storage space is limited, so the binlog is automatically purged when the maximum retention time is reached. After the upstream database purges the binlog, DM fails to pull the purged binlog and the migration task fails. For each migration task, DM creates a connection in the upstream to pull binlog. Too many connections might cause a heavy workload on the upstream database.

When the relay log is enabled, multiple migration task with the same upstream database can reuse the relay log that has been pulled to the local disk. This **relieves the pressure on the upstream database**.

For full and incremental data migration tasks (`task-mode=all`), DM needs to first migrate full data and then perform incremental migration based on binlog. If the full migration phase takes long, the upstream binlog might be purged, which results in incremental migration failure. To avoid this situation, you can enable the relay log feature so that DM automatically retains enough log in the local disk and **ensures the incremental migration task can be performed normally**.

It is generally recommended to enable relay log, but be aware of the following potential issue:

Because relay log must be written to the disk, it consumes external IO and CPU resources. This prolongs the whole data replication process and increases the data replication latency. For **latency-sensitive** scenarios, it is not recommended to enable relay log.

> **Note:**
>
> In DM v2.0.7 and later versions, relay log writes are optimized. The latency and CPU resource consumption is relatively low.

## Use relay log

This section describes how to enable and disable relay log, query relay log status, and purge relay log.

### Enable and disable relay log

<SimpleTab>

<div label="v5.4.0 and later versions">

In v5.4.0 and later versions, you can enable relay log by setting `enable-relay` to `true`. Since v5.4.0, when binding the upstream data source, DM-worker checks the `enable-relay` item in the configuration of the data source. If `enable-relay` is `true`, the relay log feature is enabled for this data source.

For the detailed configuration method, see [Upstream Database Configuration File](/dm/dm-source-configuration-file.md).

In addition, you can also dynamically adjust the `enable-relay` configuration of the data source using the `start-relay` or `stop-relay` command to enable or disable relay log in time.

{{< copyable "shell-regular" >}}

```bash
start-relay -s mysql-replica-01
```

```
{
    "result": true,
    "msg": ""
}
```

</div>

<div label="versions between v2.0.2 (included) and v5.3.0 (included)">

> **Note:**
>
> In DM v2.0.x later than DM v2.0.2 and in v5.3.0, the configuration item `enable-relay` in the source configuration file is no longer valid, and you can only use `start-relay` and `stop-relay` to enable and disable relay log. If DM finds that `enable-relay` is set to `true` when [loading the data source configuration](/dm/dm-manage-source.md#operate-data-source), it outputs the following message:
>
> ```
> Please use `start-relay` to specify which workers should pull relay log of relay-enabled sources.
> ```

> **Warning:**
>
> This startup method is marked as deprecated in v6.1 and might be removed in a future release. You can see the following prompt in the output of the relevant command: `start-relay/stop-relay with worker name will be deprecated soon. You can try stopping relay first and use start-relay without worker name instead`.

In the command `start-relay`, you can configure one or more DM-workers to migrate relay logs for the specified data source, but the DM-workers specified in the parameter must be free or have been bound to the upstream data source. Examples are as follows:

{{< copyable "" >}}

```bash
start-relay -s mysql-replica-01 worker1 worker2
```

```
{
    "result": true,
    "msg": ""
}
```

{{< copyable "" >}}

```bash
stop-relay -s mysql-replica-01 worker1 worker2
```

```
{
    "result": true,
    "msg": ""
}
```

</div>

<div label="earlier than v2.0.2">

In DM versions earlier than v2.0.2 (not including v2.0.2), DM checks the configuration item `enable-relay` in the source configuration file when binding a DM-worker to an upstream data source. If `enable-relay` is set to `true`, DM enables the relay log feature for the data source.

See [Upstream Database Configuration File](/dm/dm-source-configuration-file.md) for how to set the configuration item `enable-relay`.

</div>
</SimpleTab>

### Query relay log status

You can use the command `query-status -s` to query the status of the relay log:

```bash
query-status -s mysql-replica-01
```

<details>
<summary>Expected output</summary>

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "no sub task started",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "worker2",
                "result": null,
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000005, 916)",
                    "masterBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relaySubDir": "09bec856-ba95-11ea-850a-58f2b4af5188.000001",
                    "relayBinlog": "(mysql-bin.000005, 4)",
                    "relayBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relayCatchUpMaster": false,
                    "stage": "Running",
                    "result": null
                }
            },
            "subTaskStatus": [
            ]
        },
        {
            "result": true,
            "msg": "no sub task started",
            "sourceStatus": {
                "source": "mysql-replica-01",
                "worker": "worker1",
                "result": null,
                "relayStatus": {
                    "masterBinlog": "(mysql-bin.000005, 916)",
                    "masterBinlogGtid": "09bec856-ba95-11ea-850a-58f2b4af5188:1-28",
                    "relaySubDir": "09bec856-ba95-11ea-850a-58f2b4af5188.000001",
                    "relayBinlog": "(mysql-bin.000005, 916)",
                    "relayBinlogGtid": "",
                    "relayCatchUpMaster": true,
                    "stage": "Running",
                    "result": null
                }
            },
            "subTaskStatus": [
            ]
        }
    ]
}
```

</details>

### Pause and resume relay log

You can use the command `pause-relay` to pause the pulling process of relay logs and use the command `resume-relay` to resume the process. You need to specify the `source-id` of the upstream data source when executing these two commands. See the following examples:

```bash
pause-relay -s mysql-replica-01 -s mysql-replica-02
```

<details>
<summary>Expected output</summary>

```
{
    "op": "PauseRelay",
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        },
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-02",
            "worker": "worker2"
        }
    ]
}
```

</details>

```bash
resume-relay -s mysql-replica-01
```

<details>
<summary>Expected output</summary>

```
{
    "op": "ResumeRelay",
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "mysql-replica-01",
            "worker": "worker1"
        }
    ]
}
```

</details>

### Purge relay logs

DM provides two ways to purge relay logs: manual purge and automatic purge. Neither of these two methods purges active relay logs.

> **Note:**
>
> - Active relay log: The relay log is being used by a data migration task. An active relay log is currently only updated and written in the Syncer Unit. If a data migration task in All mode spends more time on full export/import than the expiration time configured in the purge of the data source, the relay log is still purged.
>
> - Expired relay log: The difference between the last modification time of the relay log file and the current time is greater than the value of the `expires` field in the configuration file.

#### Automatic purge

You can enable automatic purge and configure its strategy in the source configuration file. See the following example:

```yaml
# relay log purge strategy
purge:
    interval: 3600
    expires: 24
    remain-space: 15
```

+ `purge.interval`
    - The interval of automatic purge in the background, in seconds.
    - "3600" by default, indicating a background purge task is performed every 3600 seconds.

+ `purge.expires`
    - The number of hours for which the relay log (that has been previously written to the relay processing unit, and that is not being used or will not be read later by the currently running data migration task) can be retained before being purged in the automatic background purge.
    - "0" by default, indicating data purge is not performed according to the update time of the relay log.

+ `purge.remain-space`
    - The amount of remaining disk space in GB less than which the specified DM-worker machine tries to purge the relay log that can be purged securely in the automatic background purge. If it is set to `0`, data purge is not performed according to the remaining disk space.
    - "15" by default, indicating when the available disk space is less than 15 GB, DM-master tries to purge the relay log securely.

#### Manual purge

Manual purge means using the `purge-relay` command provided by dmctl to specify `subdir` and the binlog name thus to purge all the relay logs **before** the specified binlog. If the `-subdir` option in the command is not specified, all relay logs **before** the current relay log sub-directory are purged.

Assuming that the directory structure of the current relay log is as follows:

```
$ tree .
.
|-- deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
|   |-- mysql-bin.000001
|   |-- mysql-bin.000002
|   |-- mysql-bin.000003
|   `-- relay.meta
|-- deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
|   |-- mysql-bin.000001
|   `-- relay.meta
|-- e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
|   |-- mysql-bin.000001
|   `-- relay.meta
`-- server-uuid.index

$ cat server-uuid.index
deb76a2b-09cc-11e9-9129-5242cf3bb246.000001
e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
deb76a2b-09cc-11e9-9129-5242cf3bb246.000003
```

+ Executing the following `purge-relay` command in dmctl purges all relay log files **before** `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002/mysql-bin.000001`, which are all relay log files in `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001`. Files in `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002` and `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` are retained.

    {{< copyable "" >}}

    ```bash
    purge-relay -s mysql-replica-01 --filename mysql-bin.000001 --sub-dir e4e0e8ab-09cc-11e9-9220-82cc35207219.000002
    ```

+ Executing the following `purge-relay` command in dmctl purges all relay log files **before the current** (`deb76a2b-09cc-11e9-9129-5242cf3bb246.000003`) directory's `mysql-bin.000001`, which are all relay log files in `deb76a2b-09cc-11e9-9129-5242cf3bb246.000001` and `e4e0e8ab-09cc-11e9-9220-82cc35207219.000002`. Files in `deb76a2b-09cc-11e9-9129-5242cf3bb246.000003` are retained.

    {{< copyable "" >}}

    ```bash
    purge-relay -s mysql-replica-01 --filename mysql-bin.000001
    ```

## Internal mechanism of relay log

This section introduces the internal mechanism of relay log.

### Directory structure

An example of the directory structure of the local storage for a relay log:

```
<deploy_dir>/<relay_log>/
|-- 7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001
|   |-- mysql-bin.000001
|   |-- mysql-bin.000002
|   |-- mysql-bin.000003
|   |-- mysql-bin.000004
|   `-- relay.meta
|-- 842965eb-091c-11e9-9e45-9a3bff03fa39.000002
|   |-- mysql-bin.000001
|   `-- relay.meta
`-- server-uuid.index
```

- `subdir`:

    - DM-worker stores the binlog migrated from the upstream database in the same directory. Each directory is a `subdir`.

    - `subdir` is named in the format of `<Upstream database UUID>.<Local subdir serial number>`.

    - After a switch between primary and secondary instances in the upstream, DM-worker generates a new `subdir` directory with an incremental serial number.

    - In the above example, for the `7e427cc0-091c-11e9-9e45-72b7c59d52d7.000001` directory, `7e427cc0-091c-11e9-9e45-72b7c59d52d7` is the upstream database UUID and `000001` is the local `subdir` serial number.

- `server-uuid.index`: records a list of the currently available `subdir` directories.

- `relay.meta`: stores the information of the migrated binlog in each `subdir`. For example,

    ```bash
    cat c0149e17-dff1-11e8-b6a8-0242ac110004.000001/relay.meta
    ```

    ```
    binlog-name = "mysql-bin.000010"                            # The name of the currently migrated binlog.
    binlog-pos = 63083620                                       # The position of the currently migrated binlog.
    binlog-gtid = "c0149e17-dff1-11e8-b6a8-0242ac110004:1-3328" # GTID of the currently migrated binlog.
    ```

    There might also be multiple GTIDs:

    ```bash
    cat 92acbd8a-c844-11e7-94a1-1866daf8accc.000001/relay.meta
    ```

    ```
    binlog-name = "mysql-bin.018393"
    binlog-pos = 277987307
    binlog-gtid = "3ccc475b-2343-11e7-be21-6c0b84d59f30:1-14,406a3f61-690d-11e7-87c5-6c92bf46f384:1-94321383,53bfca22-690d-11e7-8a62-18ded7a37b78:1-495,686e1ab6-c47e-11e7-a42c-6c92bf46f384:1-34981190,03fc0263-28c7-11e7-a653-6c0b84d59f30:1-7041423,05474d3c-28c7-11e7-8352-203db246dd3d:1-170,10b039fc-c843-11e7-8f6a-1866daf8d810:1-308290454"
    ```

### The position where DM receives the binlog

- DM obtains the earliest position that each migration task needs from the saved checkpoint (in the downstream `dm_meta` schema by default). If this position is later than any of the following positions, DM starts to migrate from this position.

- If the local relay log is valid, which means that the relay log contains valid `server-uuid.index`, `subdir`, and `relay.meta` files, DM-worker recovers the migration from the position recorded in `relay.meta`.

- If there is no valid local relay log, but the upstream data source configuration file specifies `relay-binlog-name` or `relay-binlog-gtid`:

    - In non-GTID mode, if `relay-binlog-name` is specified, DM-worker starts to migrate from the specified binlog file.
    - In GTID mode, if `relay-binlog-gtid` is specified, DM-worker starts to migrate from the specified GTID.

- If there is no valid local relay log and the `relay-binlog-name` or `relay-binlog-gtid` is not specified in the DM configuration file:

    - In non-GTID mode, DM-worker starts to migrate from the earliest binlog that each subtask is migrating, until the latest binlog is migrated.
    - In GTID mode, DM-worker starts to migrate from the earliest GTID that each subtask is migrating, until the latest GTID is migrated.

    > **Note:**
    >
    > If the upstream relay log is purged, an error occurs. In this case, you need to configure [`relay-binlog-gtid`](/dm/dm-source-configuration-file.md#global-configuration) to specify the start position of the migration.
