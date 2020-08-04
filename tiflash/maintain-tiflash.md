---
title: TiFlash 集群运维
aliases: ['/docs-cn/v3.1/tiflash/maintain-tiflash/','/docs-cn/v3.1/reference/tiflash/maintain/']
---

# TiFlash 集群运维

本文介绍 TiFlash 集群运维的一些常见操作，包括查看 TiFlash 版本、下线 TiFlash 节点、TiFlash 故障处理等，以及 TiFlash 重要日志及系统表。

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

下线 TiFlash 节点与[缩容 TiFlash 节点](/tiflash/scale-tiflash.md#缩容-tiflash-节点)不同，下线 TiFlash 并不会在 TiDB Ansible 中删除这个节点，而仅仅是安全地关闭这个进程。

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

4. 在 pd-ctl 中输入 `store delete <store_id>`，其中 `<store_id>` 为上一步查到的该 TiFlash 节点对应的 store id。

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

## TiFlash 故障处理

本节介绍了一些 TiFlash 常见问题、原因及解决办法。

### TiFlash 副本始终处于不可用状态

该问题一般由于配置错误或者环境问题导致 TiFlash 处于异常状态，可以先通过以下步骤定位问题组件：

1. 检查 PD 是否开启 Placement Rules 功能（开启方法见[在原有 TiDB 集群上新增 TiFlash 组件](/tiflash/deploy-tiflash.md#在原有-tidb-集群上新增-tiflash-组件)的第 2 步）：

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    预期结果为 `"enable-placement-rules": "true"`。

2. 通过 TiFlash-Summary 监控面板下的 UpTime 检查操作系统中 TiFlash 进程是否正常。

3. 通过 pd-ctl 查看 TiFlash proxy 状态是否正常：

    {{< copyable "shell-regular" >}}

    ```shell
    echo "store" | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    store.labels 中含有 `{"key": "engine", "value": "tiflash"}` 信息的为 TiFlash proxy。

4. 查看 pd buddy 是否正常打印日志（日志路径的对应配置项 [flash.flash_cluster] log 设置的值，默认为 TiFlash 配置文件配置的 tmp 目录下）。

5. 检查 PD 配置的 max-replicas 是否小于等于集群 TiKV 节点数。若 max-replicas 超过 TiKV 节点数，则 PD 不会向 TiFlash 同步数据；

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    再确认 "max-replicas" 参数值。

6. 检查 TiFlash 节点对应 store 所在机器剩余的磁盘空间是否充足。默认情况下当磁盘剩余空间小于该 store 的 capacity 的 20%（通过 low-space-ratio 参数控制）时，PD 不会向 TiFlash 调度数据。

### TiFlash 查询时间不稳定，同时错误日志中打印出大量的 Lock Exception

该问题是由于集群中存在大量写入，导致 TiFlash 查询时遇到锁并发生查询重试。

可以在 TiDB 中将查询时间戳设置为 1 秒前（例如：假设当前时间为 '2020-04-08 20:15:01'，可以在执行 query 前执行 `set @@tidb_snapshot='2020-04-08 20:15:00';`），来减小 TiFlash 查询碰到锁的可能性，从而减轻查询时间不稳定的程度。

### 部分查询返回 Region Unavailable 的错误

如果在 TiFlash 上的负载压力过大，会导致 TiFlash 数据同步落后，部分查询可能会返回 `Region Unavailable` 的错误。

在这种情况下，可以通过增加 TiFlash 节点数分担负载压力。

### 数据文件损坏

可依照如下步骤进行处理：

1. 参照[下线 TiFlash 节点](/tiflash/maintain-tiflash.md#下线-tiflash-节点)一节下线对应的 TiFlash 节点。
2. 清除该 TiFlash 节点的相关数据。
3. 重新在集群中部署 TiFlash 节点。

## TiFlash 重要日志介绍

| 日志信息          | 日志含义                |
|---------------|---------------------|
| [ 23 ] `<Information>` KVStore: Start to persist [region 47, applied: term 6 index 10] | 在 TiFlash 中看到类似日志代表数据开始同步（该日志开头方括号内的数字代表线程号，下同） |
| [ 30 ] `<Debug>` CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute() | Handling DAG request，该日志代表 TiFlash 开始处理一个 Coprocessor 请求 |
| [ 30 ] `<Debug>` CoprocessorHandler: grpc::Status DB::CoprocessorHandler::execute() | Handle DAG request done，该日志代表 TiFlash 完成 Coprocessor 请求的处理 |

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
