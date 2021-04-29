---
title: Maintain a TiFlash Cluster
summary: Learn common operations when you maintain a TiFlash cluster.
aliases: ['/docs/dev/tiflash/maintain-tiflash/','/docs/dev/reference/tiflash/maintain/']
---

# Maintain a TiFlash Cluster

This document describes how to perform common operations when you maintain a [TiFlash](/tiflash/tiflash-overview.md) cluster, including checking the TiFlash version. This document also introduces critical logs and a system table of TiFlash.

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

## TiFlash critical logs

| Log Information | Log Description |
|---------------|-------------------|
| [INFO] [`<unknown>`] ["KVStore: Start to persist [region 47, applied: term 6 index 10]"] [thread_id=23] | Data starts to be replicated (the number in the square brackets at the start of the log refers to the thread ID |
| [DEBUG] [`<unknown>`] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handling DAG request"] [thread_id=30] | Handling DAG request, that is, TiFlash starts to handle a Coprocessor request |
| [DEBUG] [`<unknown>`] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handle DAG request done"] [thread_id=30] | Handling DAG request done, that is, TiFlash finishes handling a Coprocessor request |

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
