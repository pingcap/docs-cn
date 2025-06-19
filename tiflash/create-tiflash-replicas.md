---
title: 创建 TiFlash 副本
summary: 了解如何创建 TiFlash 副本。
---

# 创建 TiFlash 副本

本文介绍如何为表和数据库创建 TiFlash 副本，以及如何为副本调度设置可用区。

## 为表创建 TiFlash 副本

TiFlash 连接到 TiKV 集群后，默认不会开始数据复制。您可以通过 MySQL 客户端向 TiDB 发送 DDL 语句，为特定表创建 TiFlash 副本：

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

上述命令的参数说明如下：

- `count` 表示副本数量。当值为 `0` 时，副本会被删除。

> **注意：**
>
> 对于 [TiDB Cloud Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-cloud-serverless) 集群，TiFlash 副本的 `count` 只能是 `2`。如果您设置为 `1`，它将自动调整为 `2` 执行。如果您设置为大于 2 的数字，您将收到关于副本数量的错误。

如果您对同一个表执行多个 DDL 语句，只有最后一个语句保证生效。在以下示例中，对表 `tpch50` 执行了两个 DDL 语句，但只有第二个语句（删除副本）生效。

为表创建两个副本：

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

删除副本：

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**注意事项：**

* 如果表 `t` 通过上述 DDL 语句复制到 TiFlash，使用以下语句创建的表也会自动复制到 TiFlash：

    ```sql
    CREATE TABLE table_name like t;
    ```

* 对于早于 v4.0.6 的版本，如果在使用 TiDB Lightning 导入数据之前创建 TiFlash 副本，数据导入将失败。您必须在为表创建 TiFlash 副本之前将数据导入到表中。

* 如果 TiDB 和 TiDB Lightning 都是 v4.0.6 或更高版本，无论表是否有 TiFlash 副本，您都可以使用 TiDB Lightning 向该表导入数据。请注意，这可能会降低 TiDB Lightning 的速度，具体取决于 lightning 主机上的网卡带宽、TiFlash 节点的 CPU 和磁盘负载以及 TiFlash 副本的数量。

* 建议不要复制超过 1,000 个表，因为这会降低 PD 调度性能。此限制将在后续版本中移除。

* 在 v5.1 及更高版本中，不再支持为系统表设置副本。在升级集群之前，您需要清除相关系统表的副本。否则，在将集群升级到更高版本后，您将无法修改系统表的副本设置。

* 目前，当您使用 TiCDC 将表复制到下游 TiDB 集群时，不支持为表创建 TiFlash 副本，这意味着 TiCDC 不支持复制与 TiFlash 相关的 DDL 语句，例如：

    * `ALTER TABLE table_name SET TIFLASH REPLICA count;`
    * `ALTER DATABASE db_name SET TIFLASH REPLICA count;`

### 检查复制进度

您可以使用以下语句检查特定表的 TiFlash 副本状态。表通过 `WHERE` 子句指定。如果您删除 `WHERE` 子句，将检查所有表的副本状态。

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

在上述语句的结果中：

* `AVAILABLE` 表示该表的 TiFlash 副本是否可用。`1` 表示可用，`0` 表示不可用。一旦副本变为可用，此状态就不会改变。如果您使用 DDL 语句修改副本数量，复制状态将重新计算。
* `PROGRESS` 表示复制进度。值在 `0.0` 和 `1.0` 之间。`1` 表示至少复制了一个副本。

## 为数据库创建 TiFlash 副本

与为表创建 TiFlash 副本类似，您可以通过 MySQL 客户端向 TiDB 发送 DDL 语句，为特定数据库中的所有表创建 TiFlash 副本：

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

在此语句中，`count` 表示副本数量。当设置为 `0` 时，副本会被删除。

示例：

- 为数据库 `tpch50` 中的所有表创建两个副本：

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

- 删除为数据库 `tpch50` 创建的 TiFlash 副本：

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **注意：**
>
> - 此语句实际上执行一系列 DDL 操作，这些操作会消耗大量资源。如果语句在执行过程中被中断，已执行的操作不会回滚，未执行的操作也不会继续。
>
> - 执行语句后，在**该数据库中的所有表都复制完成之前**，不要设置 TiFlash 副本数量或对该数据库执行 DDL 操作。否则，可能会出现意外结果，包括：
>     - 如果您将 TiFlash 副本数量设置为 2，然后在数据库中的所有表复制完成之前将数量更改为 1，所有表的最终 TiFlash 副本数量不一定是 1 或 2。
>     - 执行语句后，如果您在语句执行完成之前在此数据库中创建表，这些新表**可能会或可能不会**创建 TiFlash 副本。
>     - 执行语句后，如果您在语句执行完成之前为数据库中的表添加索引，语句可能会挂起，并且只有在添加索引后才会恢复。
>
> - 如果您在语句执行完成**之后**在此数据库中创建表，不会自动为这些新表创建 TiFlash 副本。
>
> - 此语句会跳过系统表、视图、临时表和具有 TiFlash 不支持的字符集的表。

> - 您可以通过设置 [`tidb_batch_pending_tiflash_count`](/system-variables.md#tidb_batch_pending_tiflash_count-new-in-v60) 系统变量来控制执行期间允许保持不可用的表的数量。降低此值有助于减少复制期间对集群的压力。请注意，此限制不是实时的，因此在应用设置后，不可用表的数量仍可能超过限制。

### 检查复制进度

与为表创建 TiFlash 副本类似，成功执行 DDL 语句并不意味着复制完成。您可以执行以下 SQL 语句来检查目标表的复制进度：

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

要检查数据库中没有 TiFlash 副本的表，您可以执行以下 SQL 语句：

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## 加速 TiFlash 复制

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节不适用于 TiDB Cloud。

</CustomContent>

在添加 TiFlash 副本之前，每个 TiKV 实例都会执行全表扫描，并将扫描的数据作为"快照"发送给 TiFlash 以创建副本。默认情况下，TiFlash 副本添加速度较慢，使用较少的资源，以最小化对在线服务的影响。如果您的 TiKV 和 TiFlash 节点有空闲的 CPU 和磁盘 IO 资源，您可以通过执行以下步骤来加速 TiFlash 复制。

1. 使用[动态配置 SQL 语句](https://docs.pingcap.com/tidb/stable/dynamic-config)临时增加每个 TiKV 和 TiFlash 实例的快照写入速度限制：

    ```sql
    -- 这两个配置的默认值都是 100MiB，即用于写入快照的最大磁盘带宽不超过 100MiB/s。
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '300MiB';
    ```

    执行这些 SQL 语句后，配置更改立即生效，无需重启集群。但是，由于复制速度仍然受到 PD 全局限制，您现在还无法观察到加速效果。

2. 使用 [PD Control](https://docs.pingcap.com/tidb/stable/pd-control) 逐步放宽新副本速度限制。

    默认的新副本速度限制是 30，这意味着每分钟大约有 30 个 Region 添加 TiFlash 副本。执行以下命令将所有 TiFlash 实例的限制调整为 60，这将使原始速度翻倍：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 在上述命令中，您需要将 `v<CLUSTER_VERSION>` 替换为实际的集群版本，例如 `v8.1.2`，并将 `<PD_ADDRESS>:2379` 替换为任何 PD 节点的地址。例如：
    >
    > ```shell
    > tiup ctl:v8.1.2 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    几分钟内，您将观察到 TiFlash 节点的 CPU 和磁盘 IO 资源使用率显著增加，TiFlash 应该会更快地创建副本。同时，TiKV 节点的 CPU 和磁盘 IO 资源使用率也会增加。

    如果此时 TiKV 和 TiFlash 节点仍有空闲资源，并且您的在线服务延迟没有显著增加，您可以进一步放宽限制，例如，将原始速度提高三倍：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3. TiFlash 复制完成后，恢复默认配置以减少对在线服务的影响。

    执行以下 PD Control 命令恢复默认的新副本速度限制：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    ```

    执行以下 SQL 语句恢复默认的快照写入速度限制：

    ```sql
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '100MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-io-max-bytes-per-sec` = '100MiB';
    ```

## 设置可用区

<CustomContent platform="tidb-cloud">

> **注意：**
>
> 本节不适用于 TiDB Cloud。

</CustomContent>

在配置副本时，如果您需要将 TiFlash 副本分布到多个数据中心以实现灾难恢复，可以按照以下步骤配置可用区：

1. 在集群配置文件中为 TiFlash 节点指定标签。

    ```
    tiflash_servers:
      - host: 172.16.5.81
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z1"
      - host: 172.16.5.82
        config:
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z1"
      - host: 172.16.5.85
        config:
          logger.level: "info"
        learner_config:
          server.labels:
            zone: "z2"
    ```

    请注意，早期版本中的 `flash.proxy.labels` 配置无法正确处理可用区名称中的特殊字符。建议使用 `learner_config` 中的 `server.labels` 来配置可用区名称。

2. 启动集群后，在创建副本时指定标签。

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例如：

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3. PD 根据标签调度副本。在本例中，PD 分别将表 `t` 的两个副本调度到两个可用区。您可以使用 pd-ctl 查看调度情况。

    ```shell
    > tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store

        ...
        "address": "172.16.5.82:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 4,

        ...
        "address": "172.16.5.81:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z1" }
        ],
        "region_count": 5,
        ...

        "address": "172.16.5.85:23913",
        "labels": [
          { "key": "engine", "value": "tiflash"},
          { "key": "zone", "value": "z2" }
        ],
        "region_count": 9,
        ...
    ```

<CustomContent platform="tidb">

有关使用标签调度副本的更多信息，请参见[通过拓扑 Label 进行副本调度](/schedule-replicas-by-topology-labels.md)、[同城多数据中心部署](/multi-data-centers-in-one-city-deployment.md)和[两地三中心部署](/three-data-centers-in-two-cities-deployment.md)。

TiFlash 支持为不同区域配置副本选择策略。更多信息，请参见 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-new-in-v730)。

</CustomContent>
