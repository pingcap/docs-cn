---
title: Manage TiCDC Cluster and Replication Tasks
summary: Learn how to manage a TiCDC cluster and replication tasks.
category: reference
---

# Manage TiCDC Cluster and Replication Tasks

Currently, you can manage a TiCDC cluster and replication tasks using the `cdc cli` command-line tool or the HTTP interface.

## Use `cdc cli` to manage cluster status and data replication task

This section introduces how to use `cdc cli` to manage a TiCDC cluster and data replication tasks.

### Manage TiCDC service progress (`capture`)

- Query the `capture` list:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli capture list
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

- Create `changefeed`:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed create --sink-uri="mysql://root:123456@127.0.0.1:3306/"
    create changefeed ID: 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f info {"sink-uri":"mysql://root:123456@127.0.0.1:3306/","opts":{},"create-time":"2020-03-12T22:04:08.103600025+08:00","start-ts":415241823337054209,"target-ts":0,"admin-job-type":0,"config":{"filter-case-sensitive":false,"filter-rules":null,"ignore-txn-commit-ts":null}}
    ```

- Query the `changefeed` list:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed list
    ```

    ```
    [
            {
                    "id": "28c43ffc-2316-4f4f-a70b-d1a7c59ba79f"
            }
    ]
    ```

- Query a specific `changefeed` which corresponds to the status of a specific replication task:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli changefeed query --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
    ```

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
                            "ignore-txn-commit-ts": null
                    }
            },
            "status": {
                    "resolved-ts": 415241860902289409,
                    "checkpoint-ts": 415241860640145409,
                    "admin-job-type": 0
            }
    }
    ```

### Manage processing units of replication sub-tasks (`processor`)

- Query the `processor` list:

    {{< copyable "shell-regular" >}}

    ```shell
    cdc cli processor list
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
    cdc cli processor query --changefeed-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f --capture-id=b293999a-4168-4988-a4f4-35d9589b226b
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

In the following examples, suppose that the interface IP address for querying the TiCDC server status is `127.0.0.1`, and the port address is `8300` (you can specify the IP and port in `--status-addr=ip:port` when starting the TiCDC server). In later TiCDC versions, these features will be integrated to `cdc cli`.

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

### Stop replication task

Use the following command to stop a replication task:

{{< copyable "shell-regular" >}}

```shell
curl -X POST -d "admin-job=1&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
```

```
{
 "status": true,
 "message": ""
}
```

In the above command:

- `admin-job=1` means to stop the replication task. After the task is stopped, all `processor`s are stopped and exit but the configuration and status of the task are saved and can be recovered from `checkpoint-ts`.
- `cf-id=xxx` is the ID of `changefeed` that needs operation.

### Resume replication task

Use the following command to resume a replication task:

{{< copyable "shell-regular" >}}

```shell
curl -X POST -d "admin-job=2&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
```

```
{
 "status": true,
 "message": ""
}
```

In the above command:

- `admin-job=2` means to resume the replication task from `checkpoint-ts`.
- `cf-id=xxx` is the ID of `changefeed` that needs operation.

### Delete replication task

Use the following command to delete a replication task:

{{< copyable "shell-regular" >}}

```shell
curl -X POST -d "admin-job=3&cf-id=28c43ffc-2316-4f4f-a70b-d1a7c59ba79f" http://127.0.0.1:8301/capture/owner/admin
```

```
{
 "status": true,
 "message": ""
}
```

- `admin-job=3` means to delete the replication task. After the TiCDC server receives the request, all `processor`s are stopped and the configuration information of the task is cleared. The replication status is reserved. No service is available except for the query.
- `cf-id=xxx` is the ID of `changefeed` that needs operation.

## Error handling

This section introduces how to handle the error occurred when using TiCDC to replicate data.

### An error occurs when TiCDC replicates statements downstream

When an error occurs when TiCDC executes DDL or DML statements downstream, the replication task is stopped.

- If the error occurs because of downstream anomalies or network jitter, directly resume the replication task;
- If the error occurs because the downstream is incompatible with the SQL statement, resuming the task will fail. In this situation, you can configure the `ignore-txn-commit-ts` parameter in the replication configuration to skip the transaction at `commit-ts` and resume the task.
