---
title: TiFlash 常见问题
summary: 介绍 TiFlash 的常见问题、原因及解决办法。
aliases: ['/docs-cn/dev/tiflash/troubleshoot-tiflash/','/docs-cn/dev/tiflash/tiflash-faq/']
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

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} store
    ```

    store.labels 中含有 `{"key": "engine", "value": "tiflash"}` 信息的为 TiFlash proxy。

4. 检查 TiFlash 配置的副本数是否小于等于集群 TiKV 节点数。若配置的副本数超过 TiKV 节点数，则 PD 不会向 TiFlash 同步数据：

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} config placement-rules show | grep -C 10 default
    ```

    再确认 "default: count" 参数值。

    > **注意：**
    >
    > - 开启 [Placement Rules](/configure-placement-rules.md) 且存在多条 rule 的情况下，原先的 [`max-replicas`](/pd-configuration-file.md#max-replicas)、[`location-labels`](/pd-configuration-file.md#location-labels) 及 [`isolation-level`](/pd-configuration-file.md#isolation-level) 配置项将不再生效。如果需要调整副本策略，应当使用 Placement Rules 相关接口。
    > - 开启 [Placement Rules](/configure-placement-rules.md) 且只存在一条默认的 rule 的情况下，当改变 `max-replicas`、`location-labels` 或 `isolation-level` 配置项时，系统会自动更新这条默认的 rule。

5. 检查 TiFlash 节点对应 store 所在机器剩余的磁盘空间是否充足。默认情况下当磁盘剩余空间小于该 store 的 capacity 的 20%（通过 [`low-space-ratio`](/pd-configuration-file.md#low-space-ratio) 参数控制）时，PD 不会向 TiFlash 调度数据。

## 部分查询返回 Region Unavailable 的错误

如果在 TiFlash 上的负载压力过大，会导致 TiFlash 数据同步落后，部分查询可能会返回 `Region Unavailable` 的错误。

在这种情况下，可以增加 TiFlash 节点分担负载压力。

## 数据文件损坏

可依照如下步骤进行处理：

1. 参照[下线 TiFlash 节点](/scale-tidb-using-tiup.md#方案二手动缩容-tiflash-节点)下线对应的 TiFlash 节点。
2. 清除该 TiFlash 节点的相关数据。
3. 重新在集群中部署 TiFlash 节点。

## 缩容 TiFlash 节点慢

可依照如下步骤进行处理：

1. 检查是否有某些数据表的 TiFlash 副本数大于缩容后的 TiFlash 节点数：
    
    ```sql
    SELECT * FROM information_schema.tiflash_replica WHERE REPLICA_COUNT > 'tobe_left_nodes';
    ```

    `tobe_left_nodes` 表示缩容后的 TiFlash 节点数。
    
    如果查询结果不为空，则需要修改对应表的 TiFlash 副本数。这是因为，当 TiFlash 副本数大于缩容后的 TiFlash 节点数时，PD 不会将 Region peer 从待缩容的 TiFlash 节点上移走，导致 TiFlash 节点无法缩容。

2. 针对需要移除集群中所有 TiFlash 节点的场景，如果 `INFORMATION_SCHEMA.TIFLASH_REPLICA` 表显示集群已经不存在 TiFlash 副本了，但 TiFlash 节点缩容仍然无法成功，请检查最近是否执行过 `DROP TABLE <db-name>.<table-name>` 或 `DROP DATABASE <db-name>` 操作。

    对于带有 TiFlash 副本的表或数据库，直接执行 `DROP TABLE <db-name>.<table-name>` 或 `DROP DATABASE <db-name>` 后，TiDB 不会立即清除 PD 上相应的表的 TiFlash 同步规则，而是会等到相应的表满足垃圾回收 (GC) 条件后才清除这些同步规则。在垃圾回收完成后，TiFlash 节点就可以缩容成功。

    如需在满足垃圾回收条件之前清除 TiFlash 的数据同步规则，可以参考以下步骤手动清除。
    
    > **注意：**
    >
    > 手动清除数据表的 TiFlash 同步规则后，如果对这些表执行 `RECOVER TABLE`、`FLASHBACK TABLE` 或 `FLASHBACK DATABASE` 操作，表的 TiFlash 副本不会恢复。

    1. 查询当前 PD 实例中所有与 TiFlash 相关的数据同步规则。

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

        ```shell
        curl -v -X DELETE http://<pd_ip>:<pd_port>/pd/api/v1/config/rule/tiflash/table-45-r
        ```

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

2. 检查 TiFlash Region 同步是否正常。

    查看 `progress` 是否有变化:

    - 如果有变化，说明 TiFlash 同步正常，进入下一步。
    - 如果没有变化，说明 TiFlash 同步异常，在 `tidb.log` 中，搜索 `Tiflash replica is not available` 相关日志。检查对应表的 `progress` 是否更新。如果无更新，请检查 `tiflash log` 来获取更多信息。例如，在 `tiflash log` 中搜索 `lag_region_info` 来判断同步落后的 Region。

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

5. 检查 TiDB 是否为表创建 Placement rule。

    搜索 TiDB DDL Owner 的日志，检查 TiDB 是否通知 PD 添加  Placement rule。对于非分区表搜索 `ConfigureTiFlashPDForTable`；对于分区表，搜索 `ConfigureTiFlashPDForPartitions`。

    - 有关键字，进入下一步。
    - 没有关键字，收集相关组件的日志进行排查。

6. 检查 PD 是否为表设置  Placement rule。

    可以通过 `curl http://<pd-ip>:<pd-port>/pd/api/v1/config/rules/group/tiflash` 查询比较当前 PD 上的所有 TiFlash 的 Placement rule。如果观察到有 id 为 `table-<table_id>-r` 的 Rule，则表示 PD rule 设置成功。

7. 检查 PD 是否正常发起调度。

    查看 `pd.log` 日志是否出现 `table-<table_id>-r` 关键字，且之后是否出现 `add operator` 之类的调度行为。

    - 是，PD 调度正常。
    - 否，PD 调度异常。

## TiFlash 数据同步卡住

如果 TiFlash 数据一开始可以正常同步，过一段时间后全部或者部分数据无法继续同步，你可以通过以下步骤确认或解决问题：

1. 检查磁盘空间。

    检查磁盘使用空间比例是否高于 `low-space-ratio` 的值（默认值 0.8，即当节点的空间占用比例超过 80% 时，为避免磁盘空间被耗尽，PD 会尽可能避免往该节点迁移数据）。

    - 如果磁盘使用率大于等于 `low-space-ratio`，说明磁盘空间不足。此时，请删除不必要的文件，如 `${data}/flash/` 目录下的 `space_placeholder_file` 文件（必要时可在删除文件后将 `reserve-space` 设置为 0MB）。
    - 如果磁盘使用率小于 `low-space-ratio`，说明磁盘空间正常，进入下一步。

2. 检查是否有 `down peer` （`down peer` 没有清理干净可能会导致同步卡住）。

    - 执行 `pd-ctl region check-down-peer` 命令检查是否有 `down peer`。
    - 如果存在 `down peer`，执行 `pd-ctl operator add remove-peer <region-id> <tiflash-store-id>` 命令将其清除。

## 数据同步慢

同步慢可能由多种原因引起，你可以按以下步骤进行排查。

1. 调大调度参数 [`store limit`](/configure-store-limit.md#使用方法)，加快同步速度。

2. 调整 TiFlash 侧负载。

    TiFlash 负载过大会引起同步慢，可通过 Grafana 中的 **TiFlash-Summary** 面板查看各个指标的负载情况：

    - `Applying snapshots Count`: `TiFlash-summary` > `raft` > `Applying snapshots Count`
    - `Snapshot Predecode Duration`: `TiFlash-summary` > `raft` > `Snapshot Predecode Duration`
    - `Snapshot Flush Duration`: `TiFlash-summary` > `raft` > `Snapshot Flush Duration`
    - `Write Stall Duration`: `TiFlash-summary` > `Storage Write Stall` > `Write Stall Duration`
    - `generate snapshot CPU`: `TiFlash-Proxy-Details` > `Thread CPU` > `Region task worker pre-handle/generate snapshot CPU`

    根据业务优先级，调整负载情况。
