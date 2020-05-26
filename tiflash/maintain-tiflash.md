---
title: TiFlash 集群运维
category: reference
aliases: ['/docs-cn/dev/reference/tiflash/maintain/']
---

# TiFlash 集群运维

本文介绍 TiFlash 集群运维的一些常见操作，包括查看 TiFlash 版本、下线 TiFlash 节点等，以及 TiFlash 重要日志及系统表。

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

## 下线 TiFlash 节点

下线 TiFlash 节点与[缩容 TiFlash 节点](/scale-tidb-using-tiup.md#4-缩容-tiflash-节点)不同，下线 TiFlash 并不会在 TiDB Ansible 中删除这个节点，而仅仅是安全地关闭这个进程。

下线 TiFlash 节点的步骤如下：

> **注意：**
>
> 如果下线该 TiFlash 节点后，TiFlash 集群剩余节点数大于等于所有数据表的最大副本数，直接进行下面第 3 步。

1. 在 TiDB 客户端中针对所有副本数大于集群剩余 TiFlash 节点数的表执行：

    {{< copyable "sql" >}}

    ```sql
    alter table <db-name>.<table-name> set tiflash replica 0;
    ```

2. 等待相关表的 TiFlash 副本被删除（按照[查看表同步进度](/tiflash/use-tiflash.md#查看表同步进度)一节操作，查不到相关表的同步信息时即为副本被删除）。

3. 在 [pd-ctl](/pd-control.md) (tidb-ansible 目录下的 `resources/bin` 包含对应的二进制文件) 中输入 store 命令，查看该 TiFlash 节点对应的 store id。

4. 在 pd-ctl 中输入 `store delete <store_id>`，其中 <store_id> 为上一步查到的该 TiFlash 节点对应的 store id。

5. 等待该 TiFlash 节点对应的 store 消失或者 state_name 变成 Tombstone 再关闭 TiFlash 进程。

> **注意：**
>
> 如果在集群中所有的 TiFlash 节点停止运行之前，没有取消所有同步到 TiFlash 的表，则需要手动在 PD 中清除同步规则，否则无法成功完成 TiFlash 节点的下线。

手动在 PD 中清除同步规则的步骤如下：

1. 查询当前 PD 实例中所有与 TiFlash 相关的的数据同步规则。

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

2. 删除所有与 TiFlash 相关的数据同步规则。以 `id` 为 `table-45-r` 的规则为例，通过以下命令可以删除该规则。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
    ```

## TiFlash 重要日志介绍

| 日志信息          | 日志含义                |
|---------------|---------------------|
| [ 23 ] <Information> KVStore: Start to persist [region 47, applied: term 6 index 10] | 在 TiFlash 中看到类似日志代表数据开始同步（该日志开头方括号内的数字代表线程号，下同） |
| [ 30 ] <Debug> CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute() | Handling DAG request，该日志代表 TiFlash 开始处理一个 Coprocessor 请求 |
| [ 30 ] <Debug> CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute() | Handle DAG request done，该日志代表 TiFlash 完成 Coprocessor 请求的处理 |

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
