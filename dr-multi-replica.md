---
title: DR Solution Based on Multiple Replicas in a Single Cluster
summary: Learn about the multi-replica disaster recovery solution for a single cluster.
---

# DR Solution Based on Multiple Replicas in a Single Cluster

This document describes the disaster recovery (DR) solution based on multiple replicas in a single cluster. The document is organized as follows:

- Solution introduction
- How to set up a cluster and configure replicas
- How to monitor the cluster
- How to perform a DR switchover

## Introduction

Important production systems usually require regional DR with zero RPO and minute-level RTO. A Raft-based distributed database, TiDB provides multiple replicas, which allows it to support regional DR with data consistency and high availability guaranteed. Considering the small network latency between available zones (AZs) in the same region, we can dispatch business traffic to two AZs on the same region simultaneously, and achieve load balance among AZs on the same region by properly locating the Region leader and the PD leader.

> **Note:**
>
> ["Region" in TiKV](/glossary.md#regionpeerraft-group) means a range of data while the term "region" means a physical location. The two terms are not interchangeable.

## Set up a cluster and configure replicas

This section illustrates how to create a TiDB cluster across three regions with five replicas using TiUP, and how to achieve DR by properly distributing data and PD nodes.

In this example, TiDB contains five replicas and three regions. Region 1 is the primary region, region 2 is the secondary region, and region 3 is used for voting. Similarly, the PD cluster also contains 5 replicas, which function basically the same as the TiDB cluster.

1. Create a topology file similar to the following:

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
        replication.location-labels:  ["Region","AZ"] # PD schedules replicas according to the Region and AZ configuration of TiKV nodes.

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


    tikv_servers:  # Label the Regions and AZs of each TiKV node through the labels option.
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

          raftstore.raft-min-election-timeout-ticks: 1000
          raftstore.raft-max-election-timeout-ticks: 1200

    monitoring_servers:
      - host: tidb-dr-test2

    grafana_servers:
      - host: tidb-dr-test2

    alertmanager_servers:
      - host: tidb-dr-test2
      ```

    The preceding configurations use the following options to optimize toward cross-region DR:

    - `server.grpc-compression-type: gzip` to enable gRPC message compression in TiKV, thus reducing network traffic.
    - `raftstore.raft-min-election-timeout-ticks` and `raftstore.raft-max-election-timeout-ticks` to extend the time before region 3 participates in the election, thus preventing any replica in this region from being voted as the leader.

2. Create a cluster using the preceding configuration file:

    ```shell
    tiup cluster deploy drtest v6.4.0 ./topo.yaml
    tiup cluster start drtest --init
    tiup cluster display drtest
    ```

    Configure the number of replicas and the leader limit for the cluster:

    ```shell
    tiup ctl:v6.4.0 pd config set max-replicas 5
    tiup ctl:v6.4.0 pd config set label-property reject-leader Region Region3

    # The following step adds some test data to the cluster, which is optional.
    tiup bench tpcc  prepare -H 127.0.0.1 -P 4000 -D tpcc --warehouses 1
    ```

    Specify the priority of PD leader:

    ```shell
    tiup ctl:v6.4.0 pd member leader_priority  pd-1 4
    tiup ctl:v6.4.0 pd member leader_priority  pd-2 3
    tiup ctl:v6.4.0 pd member leader_priority  pd-3 2
    tiup ctl:v6.4.0 pd member leader_priority  pd-4 1
    tiup ctl:v6.4.0 pd member leader_priority  pd-5 0
    ```

    > **Note:**
    >
    > The greater the priority number, the higher the probability that this node becomes the leader.

3. Create placement rules and fix the primary replica of the test table to region 1:

    ```sql
    -- Create two placement rules: the first rule specifies that region 1 works as the primary region, and region 2 as the secondary region.
    -- The second placement rule specifies that when region 1 is down, region 2 will become the primary region.
    MySQL [(none)]> CREATE PLACEMENT POLICY primary_rule_for_region1 PRIMARY_REGION="Region1" REGIONS="Region1, Region2,Region3";
    MySQL [(none)]> CREATE PLACEMENT POLICY secondary_rule_for_region2 PRIMARY_REGION="Region2" REGIONS="Region1,Region2,Region3";

    -- Apply the rule primary_rule_for_region1 to the corresponding user tables.
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=primary_rule_for_region1;
    ALTER TABLE tpcc.district PLACEMENT POLICY=primary_rule_for_region1;

    -- Note: You can modify the database name, table name, and placement rule name as needed.

    -- Confirm whether the leaders have been transferred by executing the following query to check the number of leaders in each region.
    SELECT STORE_ID, address, leader_count, label FROM TIKV_STORE_STATUS ORDER BY store_id;
    ```

    The following SQL statement can generate a SQL script to configure the leader of all non-system schema tables to a specific region:

    ```sql
    SET @region_name=primary_rule_for_region1;
    SELECT CONCAT('ALTER TABLE ', table_schema, '.', table_name, ' PLACEMENT POLICY=', @region_name, ';') FROM information_schema.tables WHERE table_schema NOT IN ('METRICS_SCHEMA', 'PERFORMANCE_SCHEMA', 'INFORMATION_SCHEMA','mysql');
    ```

## Monitor the cluster

You can monitor the performance metrics of TiKV, TiDB, PD, and other components in the cluster by accessing Grafana or TiDB Dashboard. Based on the status of the components, you can determine whether to perform a DR switchover. For details, see the following documents:

- [Key Monitoring Metrics of TiDB](/grafana-tidb-dashboard.md)
- [Key Monitoring Metrics of TiKV](/grafana-tikv-dashboard.md)
- [Key Monitoring Metrics of PD](/grafana-pd-dashboard.md)
- [TiDB Dashboard Monitoring Page](/dashboard/dashboard-monitoring.md)

## Perform a DR switchover

This section describes how to perform a DR switchover, including planned switchover and unplanned switchover.

### Planned switchover

A planned switchover is a scheduled switchover between the primary and secondary regions based on the maintenance needs. It can be used to verify whether the DR system works properly. This section describes how to perform a planned switchover.

1. Run the following command to switch all user tables and PD leaders to region 2:

    ```sql
    -- Apply the rule secondary_rule_for_region2 to the corresponding user tables.
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=secondary_rule_for_region2;
    ALTER TABLE tpcc.district PLACEMENT POLICY=secondary_rule_for_region2;
    ```

    Note: You can modify the database name, table name, and placement rule name as needed.

    Run the following commands to lower the priority of PD nodes in region 1 and increase that of PD nodes in region 2.

    ``` shell
    tiup ctl:v6.4.0 pd member leader_priority pd-1 2
    tiup ctl:v6.4.0 pd member leader_priority pd-2 1
    tiup ctl:v6.4.0 pd member leader_priority pd-3 4
    tiup ctl:v6.4.0 pd member leader_priority pd-4 3
    ```

2. Observe the PD and TiKV nodes in Grafana and ensure that leaders of the PD and user tables have been transferred to the target region. The steps for switching back to the original region are the same as the preceding steps and are therefore not covered in this document.

### Unplanned switchover

An unplanned switchover means a switchover between primary and secondary regions when a disaster occurs. It can also be a primary-secondary region switchover initiated to simulate disaster scenarios so as to verify the effectiveness of DR systems.

1. Run the following command to stop all TiKV, TiDB, and PD nodes in region 1:

    ``` shell
    tiup cluster stop drtest -N tidb-dr-test1:20160,tidb-dr-test2:20160,tidb-dr-test1:2379,tidb-dr-test2:2379
    ```

2. Run the following commands to switch the leaders of all user tables to region 2:

    ```sql
    -- Apply the rule secondary_rule_for_region2 to the corresponding user tables.
    ALTER TABLE tpcc.warehouse PLACEMENT POLICY=secondary_rule_for_region2;
    ALTER TABLE tpcc.district PLACEMENT POLICY=secondary_rule_for_region2;

    --- Confirm whether the leaders have been transferred by executing the following query to check the number of leaders in each region.
    SELECT STORE_ID, address, leader_count, label FROM TIKV_STORE_STATUS ORDER BY store_id;
    ```

    After region 1 recovers, you can use commands similar to the preceding ones to switch the leaders of user tables back to region 1.
