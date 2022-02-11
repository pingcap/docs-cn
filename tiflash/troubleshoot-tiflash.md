---
title: TiFlash 常见问题
summary: 介绍 TiFlash 的常见问题、原因及解决办法。
---

# TiFlash 常见问题

本文介绍了一些 TiFlash 常见问题、原因及解决办法。

## TiFlash 未能正常启动

该问题可能由多个因素构成，可以通过以下步骤依次排查：

1. 检查系统环境是否是 CentOS8。

    CentOS8 中缺少 `libnsl.so` 系统库，可以通过手动安装的方式解决：

    {{< copyable "shell-regular" >}}

    ```shell
    dnf install libnsl
    ```

2. 检查系统的 `ulimit` 参数设置。

    {{< copyable "shell-regular" >}}

    ```shell
    ulimit -n 1000000
    ```

3. 使用 PD Control 工具检查在该节点（相同 IP 和 Port）是否有之前未成功下线的 TiFlash 实例，并将它们强制下线。（下线步骤参考[手动缩容 TiFlash 节点](/scale-tidb-using-tiup.md#方案二手动缩容-tiflash-节点)）

如果遇到上述方法无法解决的问题，可以打包 TiFlash 的 log 文件夹，并在 [AskTUG](http://asktug.com) 社区中提问。

## TiFlash 副本始终处于不可用状态

该问题一般由于配置错误或者环境问题导致 TiFlash 处于异常状态，可以先通过以下步骤定位问题组件：

1. 使用 pd-ctl 检查 PD 的 [Placement Rules](/configure-placement-rules.md) 功能是否开启：

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    - 如果返回 `true`，进入下一步。
    - 如果返回 `false`，你需要先[开启 Placement Rules 特性](/configure-placement-rules.md#开启-placement-rules-特性) 后再进入下一步。

2. 通过 TiFlash-Summary 监控面板下的 UpTime 检查操作系统中 TiFlash 进程是否正常。

3. 通过 pd-ctl 查看 TiFlash proxy 状态是否正常：

    {{< copyable "shell-regular" >}}

    ```shell
    echo "store" | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    store.labels 中含有 `{"key": "engine", "value": "tiflash"}` 信息的为 TiFlash proxy。

4. 查看 pd buddy 是否正常打印日志（日志路径的对应配置项 [flash.flash_cluster] log 设置的值，默认为 TiFlash 配置文件配置的 tmp 目录下）。

5. 检查配置的副本数是否小于等于集群 TiKV 节点数。若配置的副本数超过 TiKV 节点数，则 PD 不会向 TiFlash 同步数据；

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config placement-rules show' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    再确认 "default: count" 参数值。

    > **注意：**
    >
    > 开启 Placement Rules 后，原先的 `max-replicas` 及 `location-labels` 配置项将不再生效。如果需要调整副本策略，应当使用 Placement Rules 相关接口。

6. 检查 TiFlash 节点对应 store 所在机器剩余的磁盘空间是否充足。默认情况下当磁盘剩余空间小于该 store 的 capacity 的 20%（通过 low-space-ratio 参数控制）时，PD 不会向 TiFlash 调度数据。

## TiFlash 查询时间不稳定，同时错误日志中打印出大量的 Lock Exception

该问题是由于集群中存在大量写入，导致 TiFlash 查询时遇到锁并发生查询重试。

可以在 TiDB 中将查询时间戳设置为 1 秒前（例如：假设当前时间为 '2020-04-08 20:15:01'，可以在执行 query 前执行 `set @@tidb_snapshot='2020-04-08 20:15:00';`），来减小 TiFlash 查询碰到锁的可能性，从而减轻查询时间不稳定的程度。

## 部分查询返回 Region Unavailable 的错误

如果在 TiFlash 上的负载压力过大，会导致 TiFlash 数据同步落后，部分查询可能会返回 `Region Unavailable` 的错误。

在这种情况下，可以增加 TiFlash 节点分担负载压力。

## 数据文件损坏

可依照如下步骤进行处理：

1. 参照[下线 TiFlash 节点](/scale-tidb-using-tiup.md#方案二手动缩容-tiflash-节点)下线对应的 TiFlash 节点。
2. 清除该 TiFlash 节点的相关数据。
3. 重新在集群中部署 TiFlash 节点。

## TiFlash 分析慢

如果语句中含有 MPP 模式不支持的算子或函数等，TiDB 不会选择 MPP 模式，可能导致分析慢。此时，可以执行 `EXPLAIN` 语句检查 SQL 中是否含有 TiFlash 不支持的函数或算子。

{{< copyable "sql" >}}

```sql
create table t(a datetime);
alter table t set tiflash replica 1;
insert into t values('2022-01-13');
set @@session.tidb_enforce_mpp=1;
explain select count(*) from t where subtime(a, '12:00:00') > '2022-01-01' group by a;
show warnings;
```

示例中，warning 消息显示，因为 TiDB 5.4 及更早的版本尚不支持 `subtime` 函数的下推，因此 TiDB 没有选择 MPP 模式。

```
+---------+------+-----------------------------------------------------------------------------+
> | Level   | Code | Message                                                                     |
+---------+------+-----------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
+---------+------+-----------------------------------------------------------------------------+
```

## TiFlash 数据不同步

在部署完 TiFlash 节点且进行了数据的同步操作（ALTER 操作）之后，如果实际没有数据同步到 TiFlash 节点，你可以通过以下步骤确认或解决问题：

1. 检查同步操作是否执行。

    执行 `ALTER table <tbl_name> set tiflash replica <num>` 操作，查看是否有正常返回:

    - 如果有正常返回，进入下一步。
    - 如果无正常返回，请执行 `SELECT * FROM information_schema.tiflash_replica` 检查是否已经创建 TiFlash replica。如果没有，请重新执行 `ALTER table ${tbl_name} set tiflash replica ${num}`，查看是否有其他执行语句（如 `add index` ），或者检查 DDL 操作是否正常。

2. 检查 TiFlash 进程是否正常。

    查看 `progress` 和 `tiflash_cluster_manager.log` 日志中的 `flash_region_count` 参数以及 TiFlash Uptime 是否有变化:

    - 如果有变化，说明 TiFlash 进程正常，进入下一步。
    - 如果没有变化，说明 TiFlash 进程异常，请通过 `tiflash` 日志进一步排查。

3. 使用 pd-ctl 检查 PD 的 [Placement Rules](/configure-placement-rules.md) 功能是否开启：

    {{< copyable "shell-regular" >}}

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://<pd-ip>:<pd-port>
    ```

    - 如果返回 `true`，进入下一步。
    - 如果返回 `false`，你需要先[开启 Placement Rules 特性](/configure-placement-rules.md#开启-placement-rules-特性)，然后进入下一步。

4. 检查集群副本数 `max-replicas` 配置是否合理。

    - 如果 `max-replicas` 取值未超过 TiKV 节点数，进入下一步。
    - 如果 `max-replicas` 超过 TiKV 节点数，PD 不会向 TiFlash 同步数据。此时，请将 `max-replicas` 修改为小于等于 TiKV 节点数的整数。

    > **注意：**
    >
    > `max-replicas` 的默认值是 3。在生产环境中，TiKV 节点数一般大于该值；在测试环境中，可以修改为 1。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST -d '{
        "group_id": "pd",
        "id": "default",
        "start_key": "",
        "end_key": "",
        "role": "voter",
        "count": 3,
        "location_labels": [
        "host"

        ]
    }' <http://172.16.x.xxx:2379/pd/api/v1/config/rule>
    ```

5. 检查 TiFlash 与 TiDB 或 PD 的连接是否正常。

    检查 `flash_cluster_manager.log` 日志，查找关键字 `ERROR`。

    - 如果没有关键字 `ERROR`，说明连接正常，进入下一步。
    - 如果有关键字 `ERROR`，说明连接异常，请进行以下检查。

      - 检查日志文件中是否出现了 PD 相关关键字。

        如果出现，请检查 TiFlash 配置文件中 `raft.pd_addr` 对应 PD 地址是否有效。检查方法：执行 `curl '{pd-addr}/pd/api/v1/config/rules'`，检查 5 秒内是否有正常返回。

      - 检查日志文件中是否出现了 TiDB 相关关键字。

        如果出现，请检查 TiFlash 配置文件中 `flash.tidb_status_addr` 对应 TiDB 的 status 服务地址是否有效。检查方法：执行 `curl '{tidb-status-addr}/tiflash/replica'`, 检查 5 秒内是否有正常返回。

      - 检查节点间能否相互连通。

    > **注意：**
    >
    > 如问题依然无法解决，收集相关组件的日志进行排查。

6. 检查表是否创建 `placement-rule`。

    检查 `flash_cluster_manager.log` 日志，查找是否存在关键字 `Set placement rule … table-<table_id>-r`。

    - 有关键字，进入下一步。
    - 没有关键字，收集相关组件的日志进行排查。

7. 检查 PD 是否正常发起调度。

    查看 `pd.log` 日志是否出现 `table-<table_id>-r` 关键字，且之后是否出现 `add operator` 之类的调度行为。

    - 是，PD 调度正常。
    - 否，PD 调度异常，请联系 PingCAP 技术支持人员协助排查。

> **注意：**
>
> 当需要同步的表有很多小 Region 且 Region merge 参数已开启或取值较大时，可能会出现同步进度一段时间不变化或者变小的现象。

## TiFlash 数据同步卡住

如果 TiFlash 数据一开始可以正常同步，过一段时间后全部或者部分数据无法继续同步，你可以通过以下步骤确认或解决问题：

1. 检查磁盘空间。

    检查磁盘使用空间比例是否高于 `low-space-ratio` 的值（默认值 0.8，即当节点的空间占用比例超过 80% 时，为避免磁盘空间被耗尽，PD 会尽可能避免往该节点迁移数据）。

    - 如果磁盘使用率大于等于 `low-space-ratio`，说明磁盘空间不足。此时，请删除不必要的文件，如 `${data}/flash/` 目录下的 `space_placeholder_file` 文件（必要时可在删除文件后将 `reserve-space` 设置为 0MB）。
    - 如果磁盘使用率小于 `low-space-ratio` ，说明磁盘空间正常，进入下一步。

2. 检查 TiKV、PD、TiFlash 之间的网络连接情况。

    在 `flash_cluster_manager.log` 中，检查同步卡住的表对应的 `flash_region_count` 是否有更新。

    - 没有更新，检查下一步。
    - 有更新，检查是否有 `down peer` （`down peer` 没有清理干净可能会导致同步卡住）。

      - 执行 `pd-ctl region check-down-peer` 命令检查是否有 `down peer`。
      - 如果存在 `down peer`，执行 `pd-ctl operator add remove-peer\<region-id> \<tiflash-store-id>` 命令将其清除。

3. 查看 CPU 使用率。

    在 Grafana 界面，选择 **TiFlash-Proxy-Details** > **Thread CPU** > **Region task worker pre-handle/generate snapshot CPU**，查看监控中 `<instance-ip>:<instance-port>-region-worker` 对应线程的 CPU 使用率。

    若曲线为一条直线，表示 TiFlash 发生卡死，可强制杀进程重启或联系 PingCAP 技术支持人员。

## 数据同步慢

同步慢可能由多种原因引起，你可以按以下步骤进行排查。

1. 调整调度参数取值。

    - 调大 [`store limit`](/configure-store-limit.md#使用方法)，加快同步速度。
    - 调小 [`config set patrol-region-interval 10ms`](/pd-control.md#命令-command)，增加 TiKV 侧 checker 扫描 Region 的频率。
    - 调大 [`region merge`](/pd-control.md#命令-command) 参数，减少 Region 数量，从而减少扫描数量，提高检查频次。

2. 调整 TiFlash 侧负载。

    TiFlash 负载过大会引起同步慢，可通过 Grafana 中的 **TiFlash-Summary** 面板查看各个指标的负载情况：

    - `Applying snapshots Count`: `TiFlash-summary` > `raft` > `Applying snapshots Count`
    - `Snapshot Predecode Duration`: `TiFlash-summary` > `raft` > `Snapshot Predecode Duration`
    - `Snapshot Flush Duration`: `TiFlash-summary` > `raft` > `Snapshot Flush Duration`
    - `Write Stall Duration`: `TiFlash-summary` > `Storage Write Stall` > `Write Stall Duration`
    - `generate snapshot CPU`: `TiFlash-Proxy-Details` > `Thread CPU` > `Region task worker pre-handle/generate snapshot CPU`

    根据业务优先级，调整负载情况。