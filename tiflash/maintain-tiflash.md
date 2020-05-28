---
title: Maintain a TiFlash Cluster
summary: Learn common operations when you maintain a TiFlash cluster.
category: reference
aliases: ['/docs/dev/reference/tiflash/maintain/']
---

# Maintain a TiFlash Cluster

This document describes how to perform common operations when you maintain a TiFlash cluster, including checking the TiFlash version, and taking TiFlash nodes down. This document also introduces critical logs and a system table of TiFlash.

## Check the TiFlash version

There are two ways to check the TiFlash version:

- If the binary file name of TiFlash is `tiflash`, you can check the version by executing the `./tiflash version` command.

    However, to execute the above command, you need to add the directory path which includes the `libtiflash_proxy.so` dynamic library to the `LD_LIBRARY_PATH` environment variable. This is because the running of TiFlash relies on the `libtiflash_proxy.so` dynamic library.

    For example, when `tiflash` and `libtiflash_proxy.so` are in the same directory, you can first switch to this directory, and then use the following command to check the TiFlash version:

    {{< copyable "shell-regular" >}}

    ```shell
    LD_LIBRARY_PATH=./ ./tiflash version
    ```

- Check the TiFlash version by referring to the TiFlash log. For the log path, see the `[logger]` part in [the `tiflash.toml` file](/tiflash/tiflash-configuration.md#configure-the-tiflashtoml-file). For example:

    ```
    <information>: TiFlash version: TiFlash 0.2.0 master-375035282451103999f3863c691e2fc2
    ```

## Take a TiFlash node down

Taking a TiFlash node down differs from [Scaling in a TiFlash node](/scale-tidb-using-tiup.md#scale-in-a-tiflash-node) in that the former doesn't remove the node in TiDB Ansible; instead, it just safely shuts down the TiFlash process.

Follow the steps below to take a TiFlash node down:

> **Note:**
>
> After you take the TiFlash node down, if the number of the remaining nodes in the TiFlash cluster is greater than or equal to the maximum replicas of all data tables, you can go directly to step 3.

1. If the number of replicas of tables is greater than or equal to that of the remaining TiFlash nodes in the cluster, execute the following command on these tables in the TiDB client:

    {{< copyable "sql" >}}

    ```sql
    alter table <db-name>.<table-name> set tiflash replica 0;
    ```

2. To ensure that the TiFlash replicas of these tables are removed, see [Check the Replication Progress](/tiflash/use-tiflash.md#check-the-replication-progress). If you cannot view the replication progress of the related tables, it means that the replicas are removed.

3. Input the `store` command into [pd-ctl](/pd-control.md) (the binary file is in `resources/bin` of the tidb-ansible directory) to view the `store id` of the TiFlash node.

4. Input `store delete <store_id>` into `pd-ctl`. Here `<store_id>` refers to the `store id` in step 3.

5. When the corresponding `store` of the node disappears, or when `state_name` is changed to `Tombstone`, stop the TiFlash process.

> **Note:**
>
> If you don't cancel all tables replicated to TiFlash before all TiFlash nodes stop running, you need to manually delete the replication rules in PD. Or you cannot successfully take the TiFlash node down.

To manually delete the replication rules in PD, take the following steps:

1. Query all the data replication rules related to TiFlash in the current PD instance:

    {{< copyable "shell-regular" >}}

    ```shell
    curl http://<pd_ip>:<pd_port>/pd/api/v1/config/rules/group/tiflash
    ```

    ```
    [
      {
        "group_id": "tiflash",
        "id": "table-45-r",
        "override": true,
        "start_key": "7480000000000000FF2D5F720000000000FA",
        "end_key": "7480000000000000FF2E00000000000000F8",
        "role": "learner",
        "count": 1,
        "label_constraints": [
          {
            "key": "engine",
            "op": "in",
            "values": [
              "tiflash"
            ]
          }
        ]
      }
    ]
    ```

2. Delete all the data replication rules related to TiFlash. The following example command deletes the rule whose `id` is `table-45-r`:

    {{< copyable "shell-regular" >}}

    ```shell
    curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
    ```

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
