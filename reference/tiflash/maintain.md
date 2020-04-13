---
title: Maintain a TiFlash Cluster
summary: Learn common operations when you maintain a TiFlash cluster.
category: reference
---

# Maintain a TiFlash Cluster

This document describes how to perform common operations when you maintain a TiFlash cluster, including checking the TiFlash version, taking TiFlash nodes down, and troubleshooting TiFlash. This document also introduces critical logs and a system table of TiFlash.

## Check the TiFlash version

There are two ways to check the TiFlash version:

- If the binary file name of TiFlash is `tiflash`, you can check the version by executing the `./tiflash version` command.

    However, to execute the above command, you need to add the directory path which includes the `libtiflash_proxy.so` dynamic library to the `LD_LIBRARY_PATH` environment variable. This is because the running of TiFlash relies on the `libtiflash_proxy.so` dynamic library.

    For example, when `tiflash` and `libtiflash_proxy.so` are in the same directory, you can first switch to this directory, and then use the following command to check the TiFlash version:

    {{< copyable "shell-regular" >}}

    ```shell
    LD_LIBRARY_PATH=./ ./tiflash version
    ```

- Check the TiFlash version by referring to the TiFlash log. For the log path, see the `[logger]` part in [the `tiflash.toml` file](/reference/tiflash/configuration.md#configure-the-tiflashtoml-file). For example:

    ```
    <information>: TiFlash version: TiFlash 0.2.0 master-375035282451103999f3863c691e2fc2
    ```

## Take a TiFlash node down

Taking a TiFlash node down differs from [Scaling in a TiFlash node](/how-to/scale/with-tiup.md#scale-in-a-tiflash-node) in that the former doesn't remove the node in TiDB Ansible; instead, it just safely shuts down the TiFlash process.

Follow the steps below to take a TiFlash node down:

> **Note:**
>
> After you take the TiFlash node down, if the number of the remaining nodes in the TiFlash cluster is greater than or equal to the maximum replicas of all data tables, you can go directly to step 3.

1. If the number of replicas of tables is greater than or equal to that of the remaining TiFlash nodes in the cluster, execute the following command on these tables in the TiDB client:

    {{< copyable "sql" >}}

    ```sql
    alter table <db-name>.<table-name> set tiflash replica 0;
    ```

2. To ensure that the TiFlash replicas of these tables are removed, see [Check the Replication Progress](/reference/tiflash/use-tiflash.md#check-the-replication-progress). If you cannot view the replication progress of the related tables, it means that the replicas are removed.

3. Input the `store` command into [pd-ctl](/reference/tools/pd-control.md) (the binary file is in `resources/bin` of the tidb-ansible directory) to view the `store id` of the TiFlash node.

4. Input `store delete <store_id>` into `pd-ctl`. Here `<store_id>` refers to the `store id` in step 3.

5. When the corresponding `store` of the node disappears, or when `state_name` is changed to `Tombstone`, stop the TiFlash process.

> **Note:**
>
> If you don't cancel all tables replicated to TiFlash before all TiFlash nodes stop running, you need to manually delete the replication rule in PD. Or you cannot successfully take the TiFlash node down.
>
> To manually delete the replication rule in PD, send the `DELETE` request `http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/<rule_id>`. `rule_id` refers to the `id` of the `rule` to be deleted.

## TiFlash troubleshooting

This section describes some commonly encountered issues when using TiFlash, the reasons, and the solutions.

### TiFlash replica is always unavailable

This is because TiFlash is in an abnormal state caused by configuration errors or environment issues. Take the following steps to identify the faulty component:

1. Check whether PD enables the `Placement Rules` feature (to enable the feature, see the step 2 of [Add TiFlash component to an existing TiDB cluster](/reference/tiflash/deploy.md#add-tiflash-component-to-an-existing-tidb-cluster):

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    The expected result is `"enable-placement-rules": "true"`.

2. Check whether the TiFlash process is working correctly by viewing `UpTime` on the TiFlash-Summary monitoring panel.

3. Check whether the TiFlash proxy status is normal through `pd-ctl`.

    {{< copyable "shell-regular" >}}

    ```shell
    echo "store" | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    The TiFlash proxy's `store.labels` includes information such as `{"key": "engine", "value": "tiflash"}`. You can check this information to confirm a TiFlash proxy.

4. Check whether `pd buddy` can correctly print the logs (the log path is the value of `log` in the [flash.flash_cluster] configuration item; the default log path is under the `tmp` directory configured in the TiFlash configuration file).

5. Check whether the value of `max-replicas` in PD is less than or equal to the number of TiKV nodes in the cluster. If not, PD cannot replicate data to TiFlash:

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    Reconfirm the value of `max-replicas`.

6. Check whether the remaining disk space of the machine (where `store` of the TiFlash node is) is sufficient. By default, when the remaining disk space is less than 20% of the `store` capacity (which is controlled by the `low-space-ratio` parameter), PD cannot schedule data to this TiFlash node.

### TiFlash query time is unstable, and the error log prints many `Lock Exception` messages

This is because large amounts of data are written to the cluster, which causes that the TiFlash query encounters a lock and requires query retry.

You can set the query timestamp to one second earlier in TiDB. For example, if the current time is '2020-04-08 20:15:01', you can execute `set @@tidb_snapshot='2020-04-08 20:15:00';` before you execute the query. This makes less TiFlash queries encounter a lock and mitigates the risk of unstable query time.

### Some queries return the `Region Unavailable` error

If the load pressure on TiFlash is too heavy and it causes that TiFlash data replication falls behind, some queries might return the `Region Unavailable` error.

In this case, you can balance the load pressure by adding more TiFlash nodes.

### Data file corruption

Take the following steps to handle the data file corruption:

1. Refer to [Take a TiFlash node down](#take-a-tiflash-node-down) to take the corresponding TiFlash node down.
2. Delete the related data of the TiFlash node.
3. Redeploy the TiFlash node in the cluster.

## TiFlash critical logs

| Log Information | Log Description |
|---------------|-------------------|
| [ 23 ] <Information> KVStore: Start to persist [region 47, applied: term 6 index 10] | Data starts to be replicated (the number in the square brackets at the start of the log refers to the thread ID |
| [ 30 ] <Debug> CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute() | Handling DAG request, that is, TiFlash starts to handle a Coprocessor request |
| [ 30 ] <Debug> CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute() | Handling DAG request done, that is, TiFlash finishes handling a Coprocessor request |

You can find the beginning or the end of a Coprocessor request, and then locate the related logs of the Coprocessor request through the thread ID printed at the start of the log.

## TiFlash system table

The column names and their descriptions of the `information_schema.tiflash_replica` system table are as follows:

| Column Name | Description |
|---------------|-----------|
| TABLE_SCHEMA | database name |
| TABLE_NAME | table name |
| TABLE_ID | table ID |
| REPLICA_COUNT | number of TiFlash replicas |
| AVAILABLE | available or not (0/1)|
| PROGRESS | replication progress [0.0~1.0] |
