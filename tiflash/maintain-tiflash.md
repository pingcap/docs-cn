---
title: TiFlash 集群运维
aliases: ['/docs-cn/dev/tiflash/maintain-tiflash/','/docs-cn/dev/reference/tiflash/maintain/']
---

# TiFlash 集群运维

本文介绍 [TiFlash](/tiflash/tiflash-overview.md) 集群运维的一些常见操作，包括查看 TiFlash 版本，以及 TiFlash 重要日志及系统表。

## 查看 TiFlash 版本

查看 TiFlash 版本有以下两种方法：

- 假设 TiFlash 的二进制文件名为 `tiflash`，则可以通过 `./tiflash version` 方式获取 TiFlash 版本。

    但是由于 TiFlash 的运行依赖于动态库 `libtiflash_proxy.so`，因此需要将包含动态库 `libtiflash_proxy.so` 的目录路径添加到环境变量 `LD_LIBRARY_PATH` 后，上述命令才能正常执行。

    例如，当 `tiflash` 和 `libtiflash_proxy.so` 在同一个目录下时，切换到该目录后，可以通过如下命令查看 TiFlash 版本：

    {{< copyable "shell-regular" >}}

    ```shell
    LD_LIBRARY_PATH=./ ./tiflash version
    ```

- 在 TiFlash 日志（日志路径见[配置文件 tiflash.toml [logger] 部分](/tiflash/tiflash-configuration.md#配置文件-tiflashtoml)）中查看 TiFlash 版本，例如：
   
    ```
    <information>: TiFlash version: TiFlash 0.2.0 master-375035282451103999f3863c691e2fc2
    ```

## TiFlash 重要日志介绍

| 日志信息 | 日志含义 |
|---------------|-------------------|
| [INFO] [`<unknown>`] ["KVStore: Start to persist [region 47, applied: term 6 index 10]"] [thread_id=23] | 在 TiFlash 中看到类似日志代表数据开始同步 |
| [DEBUG] [`<unknown>`] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handling DAG request"] [thread_id=30] | 该日志代表 TiFlash 开始处理一个 Coprocessor 请求 |
| [DEBUG] [`<unknown>`] ["CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute(): Handle DAG request done"] [thread_id=30] | 该日志代表 TiFlash 完成 Coprocessor 请求的处理 |

你可以找到一个 Coprocessor 请求的开始或结束，然后通过日志前面打印的线程号找到该 Coprocessor 请求的其他相关日志。

## TiFlash 系统表

`information_schema.tiflash_replica` 系统表的列名及含义如下：

| 列名          | 含义                |
|---------------|---------------------|
| TABLE_SCHEMA  | 数据库名            |
| TABLE_NAME    | 表名                |
| TABLE_ID      | 表 ID               |
| REPLICA_COUNT | TiFlash 副本数      |
| AVAILABLE     | 是否可用（0/1）     |
| PROGRESS      | 同步进度 [0.0~1.0] |
