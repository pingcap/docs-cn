---
title: Manage TiCDC Cluster and Replication Tasks
summary: Learn how to manage a TiCDC cluster and replication tasks.
aliases: ['/docs/dev/ticdc/manage-ticdc/','/docs/dev/reference/tools/ticdc/manage/']
---

# Manage TiCDC Cluster and Replication Tasks

This document describes how to deploy a TiCDC cluster and how to manage the TiCDC cluster and replication tasks through the command line tool `cdc cli` and the HTTP interface.

## Deploy and install TiCDC

You can deploy TiCDC using either TiUP or Binary.

### Software and hardware recommendations

In production environments, the recommendations of software and hardware for TiCDC are as follows:

| Linux OS       | Version        |
| :----------------------- | :----------: |
| Red Hat Enterprise Linux | 7.3 or later versions   |
| CentOS                   | 7.3 or later versions   |

| **CPU** | **Memory** | **Disk type** | **Network** | **Number of TiCDC cluster instances (minimum requirements for production environment)** |
| --- | --- | --- | --- | --- |
| 16 core+ | 64 GB+ | SSD | 10 Gigabit network card (2 preferred） | 2 |

For more information, see [Software and Hardware Recommendations](/hardware-and-software-requirements.md)

### Deploy and install TiCDC using TiUP

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

This section introduces how to use `cdc cli` to manage a TiCDC cluster and data replication tasks. The following interface description assumes that PD listens on `10.0.10.25` and the port is `2379`.

### Manage TiCDC service progress (`capture`)

- Query the `capture` list:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli capture list --pd=http://10.0.10.25:2379
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
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/"
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
    | `protocol` | The protocol with which messages are output to Kafka. The optional values are `default` and `canal` (`default` by default.)    |

For more replication configuration (for example, specify replicating a single table), see [Task configuration file](#task-configuration-file).

You can use a configuration file to create a replication task in the following way:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --config changefeed.toml
```

In the command above, `changefeed.toml` is the configuration file for the replication task.

#### Query the replication task list

Execute the following command to query the replication task list:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed list --pd=http://10.0.10.25:2379
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
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
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
    - `0`: The state is normal.
    - `1`: The task is paused. When the task is paused, all replicated `processor`s exit. The configuration and the replication status of the task are retained, so you can resume the task from `checkpiont-ts`.
    - `2`: The task is resumed. The replication task resumes from `checkpoint-ts`.
    - `3`: The task is removed. When the task is removed, all replicated `processor`s are ended, and the configuration information of the replication task is cleared up. Only the replication status is retained for later queries.

#### Pause a replication task

Execute the following command to pause a replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed pause --pd=http://10.0.10.25:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

In the above command:

- `--changefeed=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to pause.

#### Resume a replication task

Execute the following command to resume a paused replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed resume --pd=http://10.0.10.25:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

In the above command:

- `--changefeed=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to resume.

#### Remove a replication task

Execute the following command to remove a replication task:

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed remove --pd=http://10.0.10.25:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

In the above command:

- `--changefeed=uuid` represents the ID of the `changefeed` that corresponds to the replication task you want to remove.

### Manage processing units of replication sub-tasks (`processor`)

- Query the `processor` list:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor list --pd=http://10.0.10.25:2379
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
    cdc cli processor query --pd=http://10.0.10.25:2379 --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
    ```

    ```
    {
      "status": {
        "tables": {
          "56": {    # ID of the replication table, corresponding to tidb_table_id of a table in TiDB
            "start-ts": 417474117955485702,
            "mark-table-id": 0  # ID of mark tables in the cyclic replication, corresponding to tidb_table_id of mark tables in TiDB
          }
        },
        "operation": null,
        "admin-job-type": 0
      },
      "position": {
        "checkpoint-ts": 417474143881789441,
        "resolved-ts": 417474143881789441,
        "count": 0
      }
    }
    ```

    In the command above:

    - `status.tables`: Each key number represents the ID of the replication table, corresponding to `tidb_table_id` of a table in TiDB.
    - `mark-table-id`: The ID of mark tables in the cyclic replication, corresponding to `tidb_table_id` of mark tables in TiDB.
    - `resolved-ts`: The largest TSO among the sorted data in the current processor.
    - `checkpoint-ts`: The largest TSO that has been successfully written to the downstream in the current processor.

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

### Manually schedule a table to other node

{{< copyable "shell-regular" >}}

```shell
curl -X POST curl 127.0.0.1:8300/capture/owner/move_table -X POST -d 'cf-id=cf060953-036c-4f31-899f-5afa0ad0c2f9&target-cp-id=6f19a6d9-0f8c-4dc9-b299-3ba7c0f216f5&table-id=49'
```

Parameter description:

| Parameter name        | Description |
| :----------- | :--- |
| `cf-id`        | The ID of the `changefeed` to be scheduled |
| `target-cp-id` | The ID of the target `capture` |
| `table-id`     | The ID of the table to be scheduled |

For nodes other than owner nodes, executing the above command will return the following error.

```
{
 "status": true,
 "message": ""
}
```

## Task configuration file

This section introduces the configuration of a replication task.

```toml
# Specifies whether the database names and tables in the configuration file are case-sensitive.
# The default value is true.
# This configuration item affects configurations related to filter and sink.
case-sensitive = true

[filter]
# Ignores the transaction of specified start_ts.
ignore-txn-start-ts = [1, 2]

# Filter rules.
# Filter syntax: https://docs.pingcap.com/tidb/stable/table-filter#syntax.
rules = ['*.*', '!test.*']

[mounter]
# mounter thread counts, which is used to decode the TiKV output data.
worker-num = 16

[sink]
# For the sink of MQ type, you can use dispatchers to configure the event dispatcher.
# Supports four dispatchers: default, ts, rowid, and table
# The matching syntax of matcher is the same as the filter rule syntax.
dispatchers = [
    {matcher = ['test1.*', 'test2.*'], dispatcher = "ts"},
    {matcher = ['test3.*', 'test4.*'], dispatcher = "rowid"},
]
# For the sink of MQ type, you can specify the protocol format of the message.
# Currently two protocols are supported: default and canal. The default protocol is TiCDC Open Protocol.
protocol = "default"

[cyclic-replication]
# Whether to enable cyclic replication.
enable = false
# The replica ID of the current TiCDC.
replica-id = 1
# The replica ID to be filtered.
filter-replica-ids = [2,3]
# Whether to replicate DDL statements.
sync-ddl = true
```

### Notes for compatibility

* In TiCDC v4.0.0, `ignore-txn-commit-ts` is removed and `ignore-txn-start-ts` is added, which uses start_ts to filter transactions.
* In TiCDC v4.0.2, `db-dbs`/`db-tables`/`ignore-dbs`/`ignore-tables` are removed and `rules` is added, which uses new filter rules for databases and tables. For detailed filter syntax, see [Table Filter](/table-filter.md).

## Cyclic replication

> **Warning:**
>
> Currently (v4.0.2), cyclic replication is still an experimental feature. It is **NOT** recommended to use it in the production environment.

The cyclic replication feature supports replicating data across multiple independent TiDB clusters. For example, TiDB clusters A, cluster B, and cluster C all have a table named `test.user_data` and write data into this table respectively. With the cyclic replication feature, the data written into `test.user_data` in one cluster can be replicated to the other two clusters, so that the `test.user_data` table in the three clusters is consistent with each other.

### Usage example

Enable cyclic replication in the three clusters of A, B, and C. Two TiCDC clusters are used for the replication from cluster A to cluster B. Among the three clusters, DDL statements enters cluster A first.

![TiCDC cyclic replication](/media/cdc-cyclic-replication.png)

To use the cyclic replication feature, you need to configure the following parameters for the replication task upon the task creation.

+ `--cyclic-replica-id`: Specifies the data source (to be written) ID of the upstream cluster. Each cluster ID must be unique.
+ `--cyclic-filter-replica-ids`: Specifies the data source ID to be filtered, which is usually the downstream cluster ID.
+ `--cyclic-sync-ddl`: Determines whether to replicate DDL statements to the downstream. DDL replication can only be enabled in the TiCDC component of one cluster.

To create a cyclic replication task, take the following steps:

1. [Enable the TiCDC component](#deploy-and-install-ticdc) in TiDB cluster A, cluster B, and cluster C.

    {{< copyable "shell-regular" >}}

    ```shell
    # Enables TiCDC in cluster A.
    cdc server \
        --pd="http://${PD_A_HOST}:${PD_A_PORT}" \
        --log-file=ticdc_1.log \
        --addr=0.0.0.0:8301 \
        --advertise-addr=127.0.0.1:8301
    # Enables TiCDC in cluster B.
    cdc server \
        --pd="http://${PD_B_HOST}:${PD_B_PORT}" \
        --log-file=ticdc_2.log \
        --addr=0.0.0.0:8301 \
        --advertise-addr=127.0.0.1:8301
    # Enables TiCDC in cluster C.
    cdc server \
        --pd="http://${PD_C_HOST}:${PD_C_PORT}" \
        --log-file=ticdc_3.log \
        --addr=0.0.0.0:8301 \
        --advertise-addr=127.0.0.1:8301
    ```

2. Create the mark tables used for the cyclic replication in cluster A, cluster B, and cluster C.

    {{< copyable "shell-regular" >}}

    ```shell
    # Creates mark tables in cluster A.
    cdc cli changefeed cyclic create-marktables \
        --cyclic-upstream-dsn="root@tcp(${TIDB_A_HOST}:${TIDB_A_PORT})/" \
        --pd="http://${PD_A_HOST}:${PD_A_PORT}"
    # Creates mark tables in cluster B.
    cdc cli changefeed cyclic create-marktables \
        --cyclic-upstream-dsn="root@tcp(${TIDB_B_HOST}:${TIDB_B_PORT})/" \
        --pd="http://${PD_B_HOST}:${PD_B_PORT}"
    # Creates mark tables in cluster C.
    cdc cli changefeed cyclic create-marktables \
        --cyclic-upstream-dsn="root@tcp(${TIDB_C_HOST}:${TIDB_C_PORT})/" \
        --pd="http://${PD_C_HOST}:${PD_C_PORT}"
    ```

3. Create the cyclic replication task in cluster A, cluster B, and cluster C.

    {{< copyable "shell-regular" >}}

    ```shell
    # Creates the cyclic replication task in cluster A.
    cdc cli changefeed create \
        --sink-uri="mysql://root@${TiDB_B_HOST}/" \
        --pd="http://${PD_A_HOST}:${PD_A_PORT}" \
        --cyclic-replica-id 1 \
        --cyclic-filter-replica-ids 2 \
        --cyclic-sync-ddl true
    # Creates the cyclic replication task in cluster B.
    cdc cli changefeed create \
        --sink-uri="mysql://root@${TiDB_C_HOST}/" \
        --pd="http://${PD_B_HOST}:${PD_B_PORT}" \
        --cyclic-replica-id 2 \
        --cyclic-filter-replica-ids 3 \
        --cyclic-sync-ddl true
    # Creates the cyclic replication task in cluster C.
    cdc cli changefeed create \
        --sink-uri="mysql://root@${TiDB_A_HOST}/" \
        --pd="http://${PD_C_HOST}:${PD_C_PORT}" \
        --cyclic-replica-id 3 \
        --cyclic-filter-replica-ids 1 \
        --cyclic-sync-ddl false
    ```

### Usage notes

+ Before creating the cyclic replication task, you must execute `cdc cli changefeed cyclic create-marktables` to create the mark tables for the cyclic replication.
+ Tables with cyclic replication enabled only contain the `[a-zA-Z0-9_]` characters.
+ Before creating the cyclic replication task, the tables for the task must be created.
+ After enabling the cyclic replication, you cannot create a table that will be replicated by the cyclic replication task.
+ To perform online DDL operations, ensure the following requirements are met:
    - The TiCDC components of multiple clusters form a one-way DDL replication chain, which is not cyclic. For example, in the example above, only the TiCDC component of cluster C disables `sync-ddl`.
    - DDL operations must be performed on the cluster that is the starting point of the one-way DDL replication chain, such as cluster A in the example above.
