---
title: TiFlash 常见问题
summary: 介绍 TiFlash 的常见问题、原因及解决办法。
category: reference
---

# TiFlash 常见问题

本文介绍了一些 TiFlash 常见问题、原因及解决办法。

## TiFlash 副本始终处于不可用状态

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
    echo 'config placement-rules show' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    再确认 "default: count" 参数值。
    > 开启 Placement Rules 后，原先的 max-replicas 及 location-labels 配置项将不再生效。如果需要调整副本策略，应当使用 Placement Rules 相关接口。

6. 检查 TiFlash 节点对应 store 所在机器剩余的磁盘空间是否充足。默认情况下当磁盘剩余空间小于该 store 的 capacity 的 20%（通过 low-space-ratio 参数控制）时，PD 不会向 TiFlash 调度数据。

## TiFlash 查询时间不稳定，同时错误日志中打印出大量的 Lock Exception

该问题是由于集群中存在大量写入，导致 TiFlash 查询时遇到锁并发生查询重试。

可以在 TiDB 中将查询时间戳设置为 1 秒前（例如：假设当前时间为 '2020-04-08 20:15:01'，可以在执行 query 前执行 `set @@tidb_snapshot='2020-04-08 20:15:00';`），来减小 TiFlash 查询碰到锁的可能性，从而减轻查询时间不稳定的程度。

## 部分查询返回 Region Unavailable 的错误

如果在 TiFlash 上的负载压力过大，会导致 TiFlash 数据同步落后，部分查询可能会返回 `Region Unavailable` 的错误。

在这种情况下，可以通过增加 TiFlash 节点数分担负载压力。

## 数据文件损坏

可依照如下步骤进行处理：

1. 参照[下线 TiFlash 节点](/tiflash/maintain-tiflash.md#下线-tiflash-节点)一节下线对应的 TiFlash 节点。
2. 清除该 TiFlash 节点的相关数据。
3. 重新在集群中部署 TiFlash 节点。
