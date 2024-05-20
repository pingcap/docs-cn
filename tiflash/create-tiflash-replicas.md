---
title: 构建 TiFlash 副本
summary: 了解如何构建 TiFlash 副本。
---

# 构建 TiFlash 副本

本文档介绍如何按表和库构建 TiFlash 副本，以及如何设置可用区来调度副本。

## 按表构建 TiFlash 副本

TiFlash 接入 TiKV 集群后，默认不会开始同步数据。可通过 MySQL 客户端向 TiDB 发送 DDL 命令来为特定的表建立 TiFlash 副本：

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

该命令的参数说明如下：

- count 表示副本数，0 表示删除。

对于相同表的多次 DDL 命令，仅保证最后一次能生效。例如下面给出的操作 `tpch50` 表的两条 DDL 命令中，只有第二条删除副本的命令能生效：

为表建立 2 个副本：

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

删除副本：

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

注意事项：

* 假设有一张表 t 已经通过上述的 DDL 语句同步到 TiFlash，则通过以下语句创建的表也会自动同步到 TiFlash：

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE table_name like t;
    ```

* 如果集群版本 < v4.0.6，若先对表创建 TiFlash 副本，再使用 TiDB Lightning 导入数据，会导致数据导入失败。需要在使用 TiDB Lightning 成功导入数据至表后，再对相应的表创建 TiFlash 副本。

* 如果集群版本以及 TiDB Lightning 版本均 >= v4.0.6，无论一个表是否已经创建 TiFlash 副本，你均可以使用 TiDB Lightning 导入数据至该表。但注意此情况会导致 TiDB Lightning 导入数据耗费的时间延长，具体取决于 TiDB Lightning 部署机器的网卡带宽、TiFlash 节点的 CPU 及磁盘负载、TiFlash 副本数等因素。

* 不推荐同步 1000 张以上的表，这会降低 PD 的调度性能。这个限制将在后续版本去除。

* v5.1 版本及后续版本将不再支持设置系统表的 replica。在集群升级前，需要清除相关系统表的 replica，否则升级到较高版本后将无法再修改系统表的 replica 设置。

### 查看表同步进度

可通过如下 SQL 语句查看特定表（通过 WHERE 语句指定，去掉 WHERE 语句则查看所有表）的 TiFlash 副本的状态：

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

查询结果中：

* AVAILABLE 字段表示该表的 TiFlash 副本是否可用。1 代表可用，0 代表不可用。副本状态为可用之后就不再改变，如果通过 DDL 命令修改副本数则会重新计算同步进度。
* PROGRESS 字段代表同步进度，在 0.0~1.0 之间，1 代表至少 1 个副本已经完成同步。

## 按库构建 TiFlash 副本

类似于按表构建 TiFlash 副本的方式，你可以在 MySQL 客户端向 TiDB 发送 DDL 命令来为指定数据库中的所有表建立 TiFlash 副本：

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

在该命令中，`count` 表示 TiFlash 的副本数。当设置 `count` 值为 0 时，表示删除现有的 TiFlash 副本。

命令示例：

执行以下命令可以为 `tpch50` 库中的所有表建立 2 个 TiFlash 副本。

```sql
ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
```

执行以下命令可以删除为 `tpch50` 库建立的 TiFlash 副本：

```sql
ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
```

> **注意：**
>
> - 该命令实际是为用户执行一系列 DDL 操作，对资源要求比较高。如果在执行过程中出现中断，已经执行成功的操作不会回退，未执行的操作不会继续执行。
>
> - 从命令执行开始到该库中所有表都已**同步完成**之前，不建议执行和该库相关的 TiFlash 副本数量设置或其他 DDL 操作，否则最终状态可能非预期。非预期场景包括：
>     - 先设置 TiFlash 副本数量为 2，在库中所有的表都同步完成前，再设置 TiFlash 副本数量为 1，不能保证最终所有表的 TiFlash 副本数量都为 1 或都为 2。
>     - 在命令执行到结束期间，如果在该库下创建表，则**可能**会对这些新增表创建 TiFlash 副本。
>     - 在命令执行到结束期间，如果为该库下的表添加索引，则该命令可能陷入等待，直到添加索引完成。
>
> - 该命令执行结束后，在该库中新建的表不会自动创建 TiFlash 副本。
>
> - 该命令会跳过系统表、视图、临时表以及包含了 TiFlash 不支持字符集的表。

### 查看库同步进度

类似于按表构建，按库构建 TiFlash 副本的命令执行成功，不代表所有表都已同步完成。可以执行下面的 SQL 语句检查数据库中所有已设置 TiFlash Replica 表的同步进度：

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

可以执行下面的 SQL 语句检查数据库中尚未设置 TiFlash Replica 的表名：

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## 加快 TiFlash 副本同步速度

新增 TiFlash 副本时，各个 TiKV 实例将进行全表数据扫描，并将扫描得到的数据快照发送给 TiFlash 从而形成副本。默认情况下，为了降低对 TiKV 及 TiFlash 线上业务的影响，TiFlash 新增副本速度较慢、占用资源较少。如果集群中 TiKV 及 TiFlash 的 CPU 和磁盘 IO 资源有富余，你可以按以下步骤操作来提升 TiFlash 副本同步速度：

1. 通过 [SQL 语句在线修改配置](/dynamic-config.md)，临时调高各个 TiKV 及 TiFlash 实例的数据快照写入速度：

    ```sql
    -- 这两个参数默认值都为 100MiB，即用于副本同步的快照最大占用的磁盘带宽不超过 100MiB/s。
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '300MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '300MiB';
    ```

    以上 SQL 语句执行后，配置修改立即生效，无需重启集群。但由于副本同步速度还受到 PD 副本速度控制，因此当前你还无法观察到副本同步速度提升。

2. 使用 [PD Control](/pd-control.md) 逐步放开新增副本速度限制：

    TiFlash 默认新增副本速度是 30（每分钟大约 30 个 Region 将会新增 TiFlash 副本）。执行以下命令将调整所有 TiFlash 实例的新增副本速度到 60，即原来的 2 倍速度：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > 上述命令中，需要将 `v<CLUSTER_VERSION>` 替换为该集群版本，例如 `v8.0.0`，`<PD_ADDRESS>:2379` 替换为任一 PD 节点的地址。替换后样例为：
    >
    > ```shell
    > tiup ctl:v8.0.0 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    执行完毕后，几分钟内，你将观察到 TiFlash 节点的 CPU 及磁盘 IO 资源占用显著提升，TiFlash 将更快地创建副本。同时，TiKV 节点的 CPU 及磁盘 IO 资源占用也将有所上升。

    如果此时 TiKV 及 TiFlash 节点的资源仍有富余，且线上业务的延迟没有显著上升，则可以考虑进一步放开调度速度，例如将新增副本的速度增加为原来的 3 倍：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3. 在副本同步完毕后，恢复到默认配置，减少在线业务受到的影响。

    执行以下 PD Control 命令可恢复默认的新增副本速度：

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
    ```

    执行以下 SQL 语句可恢复默认的数据快照写入速度：

    ```sql
    SET CONFIG tikv `server.snap-io-max-bytes-per-sec` = '100MiB';
    SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '100MiB';
    ```

## 设置可用区

在配置副本时，如果为了考虑容灾，需要将 TiFlash 的不同数据副本分布到多个数据中心，则可以按如下步骤进行配置：

1. 在集群配置文件中为 TiFlash 节点指定 label：

    ```
    tiflash_servers:
      - host: 172.16.5.81
        config:
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

    注：旧版本中的 `flash.proxy.labels` 配置无法处理可用区名字中的特殊字符，建议使用 `learner_config` 中的 `server.labels` 来进行配置。

2. 启动集群后，在创建副本时为副本调度指定 label，语法如下：

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    例如：

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3. 此时 PD 会根据设置的 label 进行调度，将表 `t` 的两个副本分别调度到两个可用区中。可以通过监控或 pd-ctl 来验证这一点：

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

关于使用 label 进行副本调度划分可用区的更多内容，可以参考[通过拓扑 label 进行副本调度](/schedule-replicas-by-topology-labels.md)，[同城多数据中心部署 TiDB](/multi-data-centers-in-one-city-deployment.md) 与[两地三中心部署](/three-data-centers-in-two-cities-deployment.md)。

TiFlash 支持设置不同区域的副本选择策略，具体请参考变量 [`tiflash_replica_read`](/system-variables.md#tiflash_replica_read-从-v730-版本开始引入)。
