---
title: TiFlash 常见问题
summary: 介绍 TiFlash 的常见问题、原因及解决办法。
aliases: ['/docs-cn/dev/tiflash/troubleshoot-tiflash/','/docs-cn/dev/tiflash/tiflash-faq/']
---

# TiFlash 常见问题

本文介绍了一些 TiFlash 常见问题、原因及解决办法。

## TiFlash 未能正常启动

TiFlash 无法正常启动可能由多个因素导致，可以通过以下步骤依次排查：

1. 检查系统环境是否是 CentOS 8。

    CentOS 8 默认缺少 `libnsl.so` 系统库，可能导致 TiFlash 启动失败。你可以通过以下命令手动安装：

    ```shell
    dnf install libnsl
    ```

2. 检查系统的 `ulimit` 参数设置。

    ```shell
    ulimit -n 1000000
    ```

3. 使用 PD Control 工具检查在该节点（相同 IP 和 Port）是否有之前未成功下线的 TiFlash 实例，并将它们强制下线。下线的操作步骤，请参考[手动缩容 TiFlash 节点](/scale-tidb-using-tiup.md#方案二手动缩容-tiflash-节点)。

4. 检查系统 CPU 是否支持 SIMD 指令集。

    自 v6.3 版本开始，在 Linux AMD64 架构的硬件平台部署 TiFlash 时，CPU 必须支持 AVX2 指令集。确保命令 `grep avx2 /proc/cpuinfo` 有输出。而在 Linux ARM64 架构的硬件平台部署 TiFlash 时，CPU 必须支持 ARMv8 架构。确保命令 `grep 'crc32' /proc/cpuinfo | grep 'asimd'` 有输出。

    如果在虚拟机上部署时遇到此问题，建议将虚拟机的 CPU 架构改成 Haswell，然后重新部署 TiFlash。

如果遇到上述方法无法解决的问题，请从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。

## 部分查询返回 Region Unavailable 的错误

如果在 TiFlash 上的负载压力过大，会导致 TiFlash 数据同步落后，部分查询可能会返回 `Region Unavailable` 的错误。

在这种情况下，可以[增加 TiFlash 节点](/scale-tidb-using-tiup.md#扩容-tiflash-节点)分担负载压力。

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

```sql
create table t(a datetime);
alter table t set tiflash replica 1;
insert into t values('2022-01-13');
set @@session.tidb_enforce_mpp=1;
explain select count(*) from t where subtime(a, '12:00:00') > '2022-01-01' group by a;
show warnings;
```

示例中，warning 消息显示，因为 TiDB v5.4 及更早的版本尚不支持 `subtime` 函数的下推，因此 TiDB 没有选择 MPP 模式。

```
+---------+------+-----------------------------------------------------------------------------+
| Level   | Code | Message                                                                     |
+---------+------+-----------------------------------------------------------------------------+
| Warning | 1105 | Scalar function 'subtime'(signature: SubDatetimeAndString, return type: datetime) is not supported to push down to tiflash now.       |
+---------+------+-----------------------------------------------------------------------------+
```

## TiFlash 副本始终处于不可用状态

如果 TiFlash 副本无法创建成功，或者创建后部分数据同步中断，你可以通过以下步骤排查或解决问题：

1. 检查 PD 的 [Placement Rules](/configure-placement-rules.md) 功能是否开启，该功能在 TiDB v5.0 及以上的版本中默认开启：

    ```shell
    echo 'config show replication' | /path/to/pd-ctl -u http://${pd-ip}:${pd-port}
    ```

    - 如果返回 `true`，进入下一步。
    - 如果返回 `false`，你需要先[开启 Placement Rules 特性](/configure-placement-rules.md#开启-placement-rules-特性)后再进入下一步。

2. 通过 **TiFlash-Summary** 监控面板中的 **UpTime** 指标，确认 TiFlash 进程在操作系统中是否正常运行。

3. 查看 PD 与 TiFlash 之间的连接状态是否正常：

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} store
    ```

    `store.labels` 中含有 `{"key": "engine", "value": "tiflash"}` 信息的为 TiFlash。

4. 检查集群 Placement Rule 中 ID 为 `default` Rule 的 `count` 配置是否合理：

    ```shell
    tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} config placement-rules show | grep -C 10 default
    ```

    - 如果 `count` 小于或等于 TiKV 节点数，进入下一步。
    - 如果 `count` 大于 TiKV 节点数（例如某些测试集群中只有 1 个 TiKV 节点，但是 `count` 值为 `3`），PD 不会向 TiFlash 调度 Region。此时，请参考[使用 pd-ctl 设置规则](/configure-placement-rules.md#使用-pd-ctl-设置规则)，将 `count` 修改为小于或等于 TiKV 节点数的整数。

    > **注意：**
    >
    > `count` 的默认值是 `3`。在生产环境中，TiKV 节点数一般大于该值。在测试环境中，如果允许集群中的 Region 副本数只有 1 个，可以修改为 `1`。

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

5. 检查 TiFlash 节点所在机器的磁盘空间使用情况。

    当 TiFlash 节点磁盘使用率超过 [`low-space-ratio`](/pd-configuration-file.md#low-space-ratio) 配置（默认值为 `0.8`）时，PD 会停止向该节点调度新的数据，以防止磁盘空间耗尽。如果所有 TiFlash 节点的剩余磁盘空间都不足，PD 将无法向 TiFlash 调度新的 Region peer，导致副本始终处于不可用状态，即 progress < 1。

    - 如果磁盘使用率大于或等于 `low-space-ratio`，说明磁盘空间不足。此时可以采取以下一个或多个措施：

        - 修改 `low-space-ratio` 的值，这会允许 PD 向 TiFlash 节点调度 Region，直到再次达到使用率限制。

            ```shell
            tiup ctl:nightly pd -u http://${pd-ip}:${pd-port} config set low-space-ratio 0.9
            ```

        - 扩容 TiFlash 节点，PD 会自动平衡各个 TiFlash 节点间的数据，将 Region 副本调度到空闲的 TiFlash 节点。

        - 删除 TiFlash 节点磁盘中不必要的文件，如日志文件、`${data}/flash/` 目录下的 `space_placeholder_file` 文件。必要时可同时将 `tiflash-learner.toml` 的 `storage.reserve-space` 设置为 `0MB`，让 TiFlash 临时恢复服务。

    - 如果磁盘使用率小于 `low-space-ratio`，说明磁盘空间正常，进入下一步。

6. 检查是否存在 `down peer`。

    未清理的 `down peer` 可能会导致同步卡住，执行以下命令检查是否有 `down peer`：

    ```shell
    pd-ctl region check-down-peer
    ```

    如果存在 `down peer`，执行以下命令将其清除：

    ```shell
    pd-ctl operator add remove-peer <region-id> <tiflash-store-id>
    ```

如果上述所有检查项都正常，但问题仍然存在，请按照 [TiFlash 数据不同步](#tiflash-数据不同步)排查同步环节出现异常的组件或数据。

## TiFlash 数据不同步

在完成 TiFlash 节点部署并执行数据同步操作 (`ALTER TABLE ... SET TIFLASH REPLICA ...`) 后，如果数据未同步至 TiFlash 节点，你可以通过以下步骤排查或解决问题：

1. 检查同步操作是否能正常执行。

    执行 `ALTER TABLE <tbl_name> SET TIFLASH REPLICA <num>` 并检查返回结果：

    - 如果语句被阻塞，请执行 `SELECT * FROM information_schema.tiflash_replica` 检查是否已经创建 TiFlash replica。
        - 通过 [`ADMIN SHOW DDL`](/sql-statements/sql-statement-show-processlist.md) 检查 DDL 操作是否正常。查看是否有其他 DDL 语句（如 `ADD INDEX`）阻塞修改 TiFlash 副本的操作。
        - 通过 [`SHOW PROCESSLIST`](/sql-statements/sql-statement-show-processlist.md) 检查是否有 DML 语句在执行，阻塞修改 TiFlash 副本的操作。
    - 等待阻塞设置 TiFlash 副本的其他语句完成或者被取消后，再次尝试设置 TiFlash 副本。如果没有异常情况，进入下一步。

2. 检查 TiFlash Region 同步是否正常。

    查询 [`information_schema.tiflash_replica`](/information-schema/information-schema-tiflash-replica.md) 表，观察 TiFlash 副本同步进度 `PROGRESS` 字段的值是否变化。或者在 `tidb.log` 中搜索关键字 `Tiflash replica is not available`，查看相关日志及 `progress` 值。

    - 如果同步进度有变化，说明 TiFlash 同步正常，但可能速度较慢，参考[数据同步慢](/tiflash/troubleshoot-tiflash.md#数据同步慢)进行调整。
    - 如果同步进度没有变化，说明 TiFlash 同步异常，进入下一步。

3. 检查 TiDB 是否成功为表创建 Placement Rule。

    在 TiDB DDL Owner 的日志中搜索以下关键字，检查 TiDB 是否通知 PD 添加 Placement Rule：

    - 非分区表：搜索 `ConfigureTiFlashPDForTable`
    - 分区表：搜索 `ConfigureTiFlashPDForPartitions`

    - 如果找到关键字，进入下一步。
    - 如果未找到关键字，收集相关组件的日志[获取支持](/support.md)。

4. 检查 PD 是否成功为表设置 Placement Rule。

    通过以下接口查看当前 PD 上的所有 TiFlash 的 Placement Rule：

    ```shell
    curl http://<pd-ip>:<pd-port>/pd/api/v1/config/rules/group/tiflash
    ```
    
    - 如果存在 ID 格式为 `table-<table_id>-r` 的 Rule，则表示 PD Rule 设置成功，进入下一步。
    - 如果没有 Rule，请收集相关组件的日志[获取支持](/support.md)。

5. 检查 PD 是否正常发起调度。

    查看 `pd.log` 日志是否包含 `table-<table_id>-r` 关键字及 `add operator` 调度日志。或检查 Grafana PD 面板的 **Operator/Schedule operator create** 看板中是否出现 `add-rule-peer` 调度，检查 **Scheduler/Patrol Region time** 看板的耗时值。**Patrol Region time** 显示的值为 PD 扫描一轮集群内所有 Region 并生成调度的耗时，这个值较高时，PD 生成调度会存在延迟。

    - 如果 `pd.log` 日志出现 `table-<table_id>-r` 关键字及 `add operator` 调度日志，或者 **Scheduler/Patrol Region time** 看板的耗时值大小正常，说明 PD 调度正常。
    - 如果没有 `add-rule-peer` 调度日志，或者 **Patrol Region time** 显示的值超过 30 分钟，PD 调度存在异常或者速度比较慢，收集相关组件的日志[获取支持](/support.md)。

如果遇到上述方法无法解决的问题，请收集必要的信息如 TiDB、PD、TiFlash 日志等，从 PingCAP 官方或 TiDB 社区[获取支持](/support.md)。

## 数据同步慢

同步慢可能由多种原因引起，你可以按以下步骤进行排查。

1. 参考[加快 TiFlash 副本同步速度](/tiflash/create-tiflash-replicas.md#加快-tiflash-副本同步速度)调整调度参数，加快同步速度。

2. 调整 TiFlash 侧负载。

    TiFlash 负载过大会引起同步慢，可通过 Grafana 中的 **TiFlash-Summary** 面板查看各个指标的负载情况：

    - `Applying snapshots Count`: `TiFlash-summary` > `raft` > `Applying snapshots Count`
    - `Snapshot Predecode Duration`: `TiFlash-summary` > `raft` > `Snapshot Predecode Duration`
    - `Snapshot Flush Duration`: `TiFlash-summary` > `raft` > `Snapshot Flush Duration`
    - `Write Stall Duration`: `TiFlash-summary` > `Storage Write Stall` > `Write Stall Duration`
    - `generate snapshot CPU`: `TiFlash-Proxy-Details` > `Thread CPU` > `Region task worker pre-handle/generate snapshot CPU`

    根据业务优先级，调整负载情况。
