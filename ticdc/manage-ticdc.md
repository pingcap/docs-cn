---
title: Manage TiCDC Cluster and Replication Tasks
summary: Learn how to manage a TiCDC cluster and replication tasks.
aliases: ['/docs/dev/ticdc/manage-ticdc/','/docs/dev/reference/tools/ticdc/manage/']
---

# Manage TiCDC Cluster and Replication Tasks

This document describes how to deploy a TiCDC cluster and how to manage the TiCDC cluster and replication tasks through the command line tool `cdc cli` and the HTTP interface.

## Deploy TiCDC

You can deploy TiCDC using either TiUP or Binary.

### Use TiUP

If you use TiUP to deploy TiCDC, you can choose one of the following ways:

- Deploy TiCDC when deploying a TiDB cluster
- Deploy a TiCDC component on an existing TiDB cluster

#### Deploy TiCDC when deploying a TiDB cluster

For details, refer to [Deploy a TiDB Cluster Using TiUP](/production-deployment-using-tiup.md#step-3-edit-the-initialization-configuration-file).

#### Deploy a TiCDC component on an existing TiDB cluster

1. First, make sure that the current TiDB version supports TiCDC; otherwise, you need to upgrade the TiDB cluster to `v4.0.0 rc.1` or later versions.

2. To deploy TiCDC, refer to [Scale out a TiCDC node](/scale-tidb-using-tiup.md#scale-out-a-ticdc-node).

### Use Binary

Binary only supports deploying the TiCDC component on an existing TiDB cluster.

Suppose that the PD cluster has a PD node (the client URL is `10.0.10.25:2379`) that can provide services. If you want to deploy three TiCDC nodes, start the TiCDC cluster by executing the following commands. Note that you only need to specify the same PD address, the newly started nodes automatically join the TiCDC cluster.

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

The following are descriptions of options available in the `cdc server` command:

- `gc-ttl`: The TTL (Time To Live) of the service level `GC safepoint` in PD set by TiCDC, in seconds. The default value is `86400`, which means 24 hours.
- `pd`: The URL of the PD client.
- `addr`: The listening address of TiCDC, the HTTP API address, and the Prometheus address of the service.
- `advertise-addr`: The access address of TiCDC to the outside world.
- `tz`: Time zone used by the TiCDC service. TiCDC uses this time zone when time data types such as `TIMESTAMP` are converted internally or when data are replicated to the downstream. The default is the local time zone in which the process runs.
- `log-file`: The address of the running log of the TiCDC process. The default is `cdc.log`.
- `log-level`: The log level when the TiCDC process is running. The default is `info`.

## Use `cdc cli` to manage cluster status and data replication task

This section introduces how to use `cdc cli` to manage a TiCDC cluster and data replication tasks. The following interface description assumes that PD listens on `127.0.0.1` and the port is `2379`.

### Manage TiCDC service progress (`capture`)

- Query the `capture` list:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli capture list --pd=http://127.0.0.1:2379
    ```

    ```
    [
            {
                    "id": "6d92386a-73fc-43f3-89de-4e337a42b766",
                    "is-owner": true
            },
            {
                    "id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "is-owner": false
            }
    ]
    ```

### Manage replication tasks (`changefeed`)

#### Create a replication task

Execute the following commands to create a replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/"
create changefeed ID: 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f info {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"config":{"filter-case-sensitive":false,"filter-rules":null,"ignore-txn-start-ts":null}}
```

Configure `--sink-uri`  according to the following format. Currently, the scheme supports `mysql`/`tidb`/`kafka`.

{{< copyable "" >}}

```
[scheme]://[userinfo@][host]:[port][/path]?[query_parameters]
```

- Configure sink URI with `mysql`/`tidb`

    Sample configuration:

    {{< copyable "shell-regular" >}}

    ```shell
    --sink-uri="mysql://root:123456@127.0.0.1:3306/?worker-count=16&max-txn-row=5000"
    ```

    The following are descriptions of parameters and parameter values in the sample configuration:

    | Parameter/Parameter Value    | Description                                             |
    | :------------ | :------------------------------------------------ |
    | `root`        | The username of the downstream database                              |
    | `123456`       | The password of the downstream database                                      |
    | `127.0.0.1`    | The IP address of the downstream database                               |
    | `3306`         | The port for the downstream data                                 |
    | `worker-count` | The number of SQL statements that can be concurrently executed to the downstream (optional, `16` by default)       |
    | `max-txn-row`  | The size of a transaction batch that can be executed to the downstream (optional, `256` by default)) |

- Configure sink URI with `kafka`

    Sample configuration:

    {{< copyable "shell-regular" >}}

    ```shell
    --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&partition-num=6&max-message-bytes=67108864&replication-factor=1"
    ```

    The following are descriptions of parameters and parameter values in the sample configuration:

    | Parameter/Parameter Value               | Description                                                        |
    | :------------------ | :------------------------------------------------------------ |
    | `127.0.0.1`          | The IP address of the downstream Kafka services                                 |
    | `9092`               | The port for the downstream Kafka                                          |
    | `cdc-test`           | The name of the Kafka topic                                      |
    | `kafka-version`      | The version of the downstream Kafka (optional, `2.4.0` by default)                      |
    | `partition-num`      | The number of the downstream Kafka partitions (Optional. The value must be **no greater than** the actual number of partitions. If you do not configure this parameter, the partition number is obtained automatically.) |
    | `max-message-bytes`  | The maximum size of data that is sent to Kafka broker each time (optional, `64MB` by default) |
    | `replication-factor` | The number of Kafka message replicas that can be saved (optional, `1` by default)                       |

#### Query the replication task list

Execute the following command to query the replication task list:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed list --pd=http://127.0.0.1:2379
```

```
[
        {
                "id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
        }
]
```

#### Query a specific replication task

Execute the following command to query a specific replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed query --pd=http://127.0.0.1:2379 --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

The information returned consists of `"info"` and `"status"` of the replication task.

```
{
        "info": {
                "sink-uri": "mysql://root:123456@127.0.0.1:3306/",
                "opts": {},
                "create-time": "2020-03-12T22:04:08.103600025+08:00",
                "start-ts": 415241823337054209,
                "target-ts": 0,
                "admin-job-type": 0,
                "config": {
                        "filter-case-sensitive": false,
                        "filter-rules": null,
                        "ignore-txn-start-ts": null
                }
        },
        "status": {
                "resolved-ts": 415241860902289409,
                "checkpoint-ts": 415241860640145409,
                "admin-job-type": 0
        }
}
```

In the above command:

- `resolved-ts`: The largest transaction `TS` in the current `changefeed`. Note that this `TS` has been successfully sent from TiKV to TiCDC.
- `checkpoint-ts`: The largest transaction `TS` in the current `changefeed` that has been successfully written to the downstream.
- `admin-job-type`: The status of a `changefeed`:
    - `0`: The state is normal. It is the initial status.
    - `1`: The task is paused. When the task is paused, all replicated `processor`s exit. The configuration and the replication status of the task are retained, so you can resume the task from `checkpiont-ts`.
    - `2`: The task is resumed. The replication task resumes from `checkpoint-ts`.
    - `3`: The task is removed. When the task is removed, all replicated `processor`s are ended, and the configuration information of the replication task is cleared up. Only the replication status is retained for later queries.

#### Pause a replication task

Execute the following command to pause a replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed pause --pd=http://127.0.0.1:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

In the above command:

- `--changefeed=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to pause.

#### Resume a replication task

Execute the following command to resume a paused replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed resume --pd=http://127.0.0.1:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

In the above command:

- `--changefeed=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to resume.

#### Remove a replication task

Execute the following command to remove a replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed remove --pd=http://127.0.0.1:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

In the above command:

- `--changefeed=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to remove.

### Manage processing units of replication sub-tasks (`processor`)

- Query the `processor` list:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor list --pd=http://127.0.0.1:2379
    ```

    ```
    [
            {
                    "id": "9f84ff74-abf9-407f-a6e2-56aa35b33888",
                    "capture-id": "b293999a-4168-4988-a4f4-35d9589b226b",
                    "changefeed-id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
            }
    ]
    ```

- Query a specific `changefeed` which corresponds to the status of a specific replication task:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor query --pd=http://127.0.0.1:2379 --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
    ```

    ```
    {
            "status": {
                    "table-infos": [
                            {
                                    "id": 45,
                                    "start-ts": 415241823337054209
                            }
                    ],
                    "table-p-lock": null,
                    "table-c-lock": null,
                    "admin-job-type": 0
            },
            "position": {
                    "checkpoint-ts": 415241893447467009,
                    "resolved-ts": 415241893971492865
            }
    }
    ```

## Use HTTP interface to manage cluster status and data replication task

Currently, the HTTP interface provides some basic features for query and maintenance. 

In the following examples, suppose that the TiCDC server listens on `127.0.0.1`, and the port is `8300` (you can specify the IP and port in `--addr=ip:port` when starting the TiCDC server).

### Get the TiCDC server status

Use the following command to get the TiCDC server status:

{{< copyable "shell-regular" >}}

```shell
curl http://127.0.0.1:8300/status
```

```
{
"version": "0.0.1",
"git_hash": "863f8ea889b144244ff53593a45c47ad22d37396",
"id": "6d92386a-73fc-43f3-89de-4e337a42b766", # capture id
"pid": 12102    # cdc server pid
}
```

### Evict the owner node

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8300/capture/owner/resign
```

The above command takes effect only for requesting on the **owner node**.

```
{
 "status": true,
 "message": ""
}
```

{{< copyable "shell-regular" >}}

```shell
curl -X POST http://127.0.0.1:8301/capture/owner/resign
```

For nodes other than owner nodes, executing the above command will return the following error.

```
election: not leader
```
