---
title: 基于多副本的单集群容灾方案
summary: 了解 TiDB 提供的基于多副本的单集群容灾方案。
---

# 基于多副本的单集群容灾方案

本文介绍了基于多副本的单集群容灾方案，文档内容组织如下：

- 方案简介
- 搭建集群
- 配置副本
- 监控集群
- 容灾切换

## 简介

对于重要的生产系统，很多用户需要能够实现区域级别的容灾，并且做到 RPO = 0 和分钟级别的 RTO。TiDB 作为基于 Raft 协议的分布式数据库，其自带的多副本特性可以用于支持区域级别的容灾目标，并同时确保数据的一致性和高可用性。而同区域可用区 (Available Zone, AZ) 之间的网络延迟相对较小，可以把业务流量同时派发到同区域两个 AZ，并通过控制 Region Leader 和 PD Leader 分布实现同区域 AZ 共同负载业务流量。

## 搭建集群和配置副本

在这一部分当中，会以一个 5 副本的集群为例，演示如何使用 TiUP 创建一个跨 3 个区域的集群，以及如何控制数据和 PD 的分布位置，从而达到容灾的目的。

在下面的示例中，TiDB 集群的区域 1 作为 primary region，区域 2 作为 secondary region，而区域 3 则作为投票使用的第三个区域，一共包含 5 个副本。同理，PD 集群也包含了 5 个副本，其功能和 TiDB 集群的功能基本一致。

1. 创建类似于以下的集群拓扑文件：

    ```toml
    global:
      user: "root"
      ssh_port: 22
      deploy_dir: "/data/tidb_cluster/tidb-deploy"
      data_dir: "/data/tidb_cluster/tidb-data"

    server_configs:
      tikv:
        server.grpc-compression-type: gzip
      pd:
        replication.location-labels:  ["Region","AZ"] # PD 会根据 TiKV 节点的 Region 和 AZ 配置来进行副本的调度。

    pd_servers:
      - host: tidb-dr-test1
        name: "pd-1"
      - host: tidb-dr-test2
        name: "pd-2"
      - host: tidb-dr-test3
        name: "pd-3"
      - host: tidb-dr-test4
        name: "pd-4"
      - host: tidb-dr-test5
        name: "pd-5"

    tidb_servers:
      - host: tidb-dr-test1
      - host: tidb-dr-test3

    tikv_servers:  # 在 TiKV 节点中通过 labels 选项来对每个 TiKV 节点所在的 Region 和 AZ 进行标记
      - host: tidb-dr-test1
        config:
          server.labels: { Region: "Region1", AZ: "AZ1" }
      - host: tidb-dr-test2
        config:
          server.labels: { Region: "Region1", AZ: "AZ2" }
      - host: tidb-dr-test3
        config:
          server.labels: { Region: "Region2", AZ: "AZ3" }
      - host: tidb-dr-test4
        config:
          server.labels: { Region: "Region2", AZ: "AZ4" }
      - host: tidb-dr-test5
        config:
          server.labels: { Region: "Region3", AZ: "AZ5" }

          raftstore.raft-min-election-timeout-ticks: 50
          raftstore.raft-max-election-timeout-ticks: 60

    monitoring_servers:
      - host: tidb-dr-test2

    grafana_servers:
      - host: tidb-dr-test2

    alertmanager_servers:
      - host: tidb-dr-test2
    ```

    在上面的配置中，使用了以下一系列配置来针对跨区域容灾场景进行优化：

    - 使用 `server.grpc-compression-type`：gzip 启用 TiKV 之间的消息压缩，从而降低网络流量。
    - 使用 `raftstore.raft-min-election-timeout-ticks` 和 `raftstore.raft-max-election-timeout-ticks` 延长区域 3 参加选举的时间，从而避免该区域中的副本被选举为主节点。

2. 使用上面的配置文件创建集群：

    ```shell
    tiup cluster deploy drtest v6.4.0 ./topo.yaml
    tiup cluster start drtest --init
    tiup cluster display drtest
    ```

    对集群的副本数和 Leader 限制进行配置：

    ```shell
    tiup ctl:v6.4.0 pd config set max-replicas 5
    tiup ctl:v6.4.0 pd config set label-property reject-leader Region Region3

    # 下面的步骤用于向集群中添加一些测试数据，可选
    tiup bench tpcc  prepare -H 127.0.0.1 -P 4000 -D tpcc --warehouses 1
    ```

    指定 PD leader 的优先级：

    ```shell
    tiup ctl:v6.4.0 pd member leader_priority  pd-1 4
    tiup ctl:v6.4.0 pd member leader_priority  pd-2 3
    tiup ctl:v6.4.0 pd member leader_priority  pd-3 2
    tiup ctl:v6.4.0 pd member leader_priority  pd-4 1
    tiup ctl:v6.4.0 pd member leader_priority  pd-5 0
    ```

    > **注意：**
    >
    > 在可用的 PD 节点中，优先级数值最大的节点会直接当选 leader。

3. 创建 placement rule，并将测试表的主副本固定在区域 1：

    ```sql
    -- 创建两个 placement rules，第一个是区域 1 作为主区域，在系统正常时使用，第二个是区域 2 作为备区域。
    -- 作为主区域，当区域 1 出现问题时，区域 2 会作为主区域。
    MySQL [(none)]> CREATE PLACEMENT POLICY primary_rule_for_region1 PRIMARY_REGION="Region1" REGIONS="Region1, Region2,Region3";
    MySQL [(none)]> CREATE PLACEMENT POLICY secondary_rule_for_region2 PRIMARY_REGION="Region2" REGIONS="Region1,Region2,Region3";

    -- 将刚刚创建的规则 primary_rule_for_region1 应用到对应的用户表上。
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=primary_rule_for_region1;
    ALTER TABLE tpcc.district PLACEMENT POLICY=primary_rule_for_region1;

    -- 说明：请根据需要修改上面的数据库名称、表名和 placement rule 的名称。

    -- 使用类似下面的查询，用户可以查看每个区域包含的 leader 数量，以确认 leader 迁移是否完成。
    SELECT STORE_ID, address, leader_count, label FROM TIKV_STORE_STATUS ORDER BY store_id;
    ```

    下面的语句可以产生一个 SQL 脚本，把所有非系统 schema 中的表的 leader 都设置到特定的区域上：

    ```sql
    SET @region_name=primary_rule_for_region1;
    SELECT concat('ALTER TABLE ', table_schema, '.', table_name, ' PLACEMENT POLICY=', @region_name, ';') FROM information_schema.tables WHERE table_schema NOT IN ('METRICS_SCHEMA', 'PERFORMANCE_SCHEMA', 'INFORMATION_SCHEMA','mysql');
    ```

## 监控集群

对于部署的集群，你可以通过访问集群中的 Grafana 地址或者 TiDB Dashboard 组件来对集群中的各个 TiKV、TiDB 和 PD 组件的各种性能指标进行监控。根据组件的状态，确定是否进行容灾切换。详细信息，请参考如下文档：

- [TiDB 重要监控指标详解](/grafana-tidb-dashboard.md)
- [TiKV 监控指标详解](/grafana-tikv-dashboard.md)
- [PD 重要监控指标详解](/grafana-pd-dashboard.md)
- [TiDB Dashboard 监控页面](/dashboard/dashboard-monitoring.md)

## 容灾切换

本部分介绍容灾切换，包括计划内切换和计划外切换。

### 计划内切换

指根据维护需要进行的主备区域切换，可用于验证容灾系统是否可以正常工作。本部分介绍如何在计划内切换主备区域。

1. 执行如下命令，将所有用户表和 PD Leader 都切换到区域 2：

    ```sql
    -- 将之前创建的规则 secondary_rule_for_region2 应用到对应的用户表上。
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=secondary_rule_for_region2;
    ALTER TABLE tpcc.district PLACEMENT POLICY=secondary_rule_for_region2;
    ```

    说明：请根据需要修改上面的数据库名称、表名和 placement rule 的名称。

    执行如下命令，调低区域 1 的 PD 节点的优先级，并调高区域 2 的 PD 节点的优先级。

    ``` shell
    tiup ctl:v6.4.0 pd member leader_priority pd-1 2
    tiup ctl:v6.4.0 pd member leader_priority pd-2 1
    tiup ctl:v6.4.0 pd member leader_priority pd-3 4
    tiup ctl:v6.4.0 pd member leader_priority pd-4 3
    ```

2. 观察 Grafana 中 PD 和 TiKV 部分中的内容，确保 PD 的 Leader 和用户表的 Leader 已经迁移到对应的区域。另外，切换回原有区域的步骤与上面的步骤基本相同，本文不做过多的描述。

### 计划外切换

计划外切换，指灾难发生时的主备区域切换，或者为了验证容灾系统的有效性，而模拟灾难发生时的主备区域切换。

1. 执行类似下面的命令终止区域 1 上所有的 TiKV、TiDB 和 PD 节点:

    ``` shell
    tiup cluster stop drtest -N tidb-dr-test1:20160,tidb-dr-test2:20160,tidb-dr-test1:2379,tidb-dr-test2:2379
    ```

2. 运行类似于下面的命令切换用户表的 leader 到区域 2:

    ```sql
    -- 将之前创建的规则 secondary_rule_for_region2 应用到对应的用户表上。
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=secondary_rule_for_region2;
    ALTER TABLE tpcc.district PLACEMENT POLICY=secondary_rule_for_region2;

    ---可以使用类似下面的查询查看每个区域包含的 leader 数量，以确认 leader 迁移是否完成。
    SELECT STORE_ID, address, leader_count, label FROM TIKV_STORE_STATUS ORDER BY store_id;
    ```

    当区域 1 恢复正常之后，可以使用类似于上面的命令将用户表的 leader 重新切换到区域 1。
