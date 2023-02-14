---
title: Create TiFlash Replicas
summary: Learn how to create TiFlash replicas.
---

# Create TiFlash Replicas

This document introduces how to create TiFlash replicas for tables and for databases, and set available zones for replica scheduling.

## Create TiFlash replicas for tables

After TiFlash is connected to the TiKV cluster, data replication by default does not begin. You can send a DDL statement to TiDB through a MySQL client to create a TiFlash replica for a specific table:

{{< copyable "sql" >}}

```sql
ALTER TABLE table_name SET TIFLASH REPLICA count;
```

The parameter of the above command is described as follows:

- `count` indicates the number of replicas. When the value is `0`, the replica is deleted.

If you execute multiple DDL statements on the same table, only the last statement is ensured to take effect. In the following example, two DDL statements are executed on the table `tpch50`, but only the second statement (to delete the replica) takes effect.

Create two replicas for the table:

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 2;
```

Delete the replica:

{{< copyable "sql" >}}

```sql
ALTER TABLE `tpch50`.`lineitem` SET TIFLASH REPLICA 0;
```

**Notes:**

* If the table `t` is replicated to TiFlash through the above DDL statements, the table created using the following statement will also be automatically replicated to TiFlash:

    {{< copyable "sql" >}}

    ```sql
    CREATE TABLE table_name like t;
    ```

* For versions earlier than v4.0.6, if you create the TiFlash replica before using TiDB Lightning to import the data, the data import will fail. You must import data to the table before creating the TiFlash replica for the table.

* If TiDB and TiDB Lightning are both v4.0.6 or later, no matter a table has TiFlash replica(s) or not, you can import data to that table using TiDB Lightning. Note that this might slow the TiDB Lightning procedure, which depends on the NIC bandwidth on the lightning host, the CPU and disk load of the TiFlash node, and the number of TiFlash replicas.

* It is recommended that you do not replicate more than 1,000 tables because this lowers the PD scheduling performance. This limit will be removed in later versions.

* In v5.1 and later versions, setting the replicas for the system tables is no longer supported. Before upgrading the cluster, you need to clear the replicas of the relevant system tables. Otherwise, you cannot modify the replica settings of the system tables after you upgrade the cluster to a later version.

### Check replication progress

You can check the status of the TiFlash replicas of a specific table using the following statement. The table is specified using the `WHERE` clause. If you remove the `WHERE` clause, you will check the replica status of all tables.

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>' and TABLE_NAME = '<table_name>';
```

In the result of above statement:

* `AVAILABLE` indicates whether the TiFlash replicas of this table are available or not. `1` means available and `0` means unavailable. Once the replicas become available, this status does not change. If you use DDL statements to modify the number of replicas, the replication status will be recalculated.
* `PROGRESS` means the progress of the replication. The value is between `0.0` and `1.0`. `1` means at least one replica is replicated.

## Create TiFlash replicas for databases

Similar to creating TiFlash replicas for tables, you can send a DDL statement to TiDB through a MySQL client to create a TiFlash replica for all tables in a specific database:

{{< copyable "sql" >}}

```sql
ALTER DATABASE db_name SET TIFLASH REPLICA count;
```

In this statement, `count` indicates the number of replicas. When you set it to `0`, replicas are deleted.

Examples:

- Create two replicas for all tables in the database `tpch50`:

    {{< copyable "sql" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 2;
    ```

- Delete TiFlash replicas created for the database `tpch50`:

    {{< copyable "sql" >}}

    ```sql
    ALTER DATABASE `tpch50` SET TIFLASH REPLICA 0;
    ```

> **Note:**
>
> - This statement actually performs a series of DDL operations, which are resource-intensive. If the statement is interrupted during the execution, executed operations are not rolled back and unexecuted operations do not continue.
>
> - After executing the statement, do not set the number of TiFlash replicas or perform DDL operations on this database until **all tables in this database are replicated**. Otherwise, unexpected results might occur, which include:
>     - If you set the number of TiFlash replicas to 2 and then change the number to 1 before all tables in the database are replicated, the final number of TiFlash replicas of all the tables is not necessarily 1 or 2.
>     - After executing the statement, if you create tables in this database before the completion of the statement execution, TiFlash replicas **may or may not** be created for these new tables.
>     - After executing the statement, if you add indexes for tables in the database before the completion of the statement execution, the statement might hang and resume only after the indexes are added.
>
> - This statement skips system tables, views, temporary tables, and tables with character sets not supported by TiFlash.

### Check replication progress

Similar to creating TiFlash replicas for tables, successful execution of the DDL statement does not mean the completion of replication. You can execute the following SQL statement to check the progress of replication on target tables:

{{< copyable "sql" >}}

```sql
SELECT * FROM information_schema.tiflash_replica WHERE TABLE_SCHEMA = '<db_name>';
```

To check tables without TiFlash replicas in the database, you can execute the following SQL statement:

{{< copyable "sql" >}}

```sql
SELECT TABLE_NAME FROM information_schema.tables where TABLE_SCHEMA = "<db_name>" and TABLE_NAME not in (SELECT TABLE_NAME FROM information_schema.tiflash_replica where TABLE_SCHEMA = "<db_name>");
```

## Speed up TiFlash replication

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is not applicable to TiDB Cloud.

</CustomContent>

Before TiFlash replicas are added, each TiKV instance performs a full table scan and sends the scanned data to TiFlash as a "snapshot" to create replicas. By default, TiFlash replicas are added slowly with fewer resources usage in order to minimize the impact on the online service. If there are spare CPU and disk IO resources in your TiKV and TiFlash nodes, you can accelerate TiFlash replication by performing the following steps.

1. Temporarily increase the snapshot write speed limit for each TiKV and TiFlash instance by using the [Dynamic Config SQL statement](https://docs.pingcap.com/tidb/stable/dynamic-config):

   ```sql
   -- The default value for both configurations are 100MiB, i.e. the maximum disk bandwidth used for writing snapshots is no more than 100MiB/s.
   SET CONFIG tikv `server.snap-max-write-bytes-per-sec` = '300MiB';
   SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '300MiB';
   ```

   After executing these SQL statements, the configuration changes take effect immediately without restarting the cluster. However, since the replication speed is still restricted by the PD limit globally, you cannot observe the acceleration for now.

2. Use [PD Control](https://docs.pingcap.com/tidb/stable/pd-control) to progressively ease the new replica speed limit.

    The default new replica speed limit is 30, which means, approximately 30 Regions add TiFlash replicas every minute. Executing the following command will adjust the limit to 60 for all TiFlash instances, which doubles the original speed:

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 60 add-peer
    ```

    > In the preceding command, you need to replace `v<CLUSTER_VERSION>` with the actual cluster version, such as `v6.5.0` and `<PD_ADDRESS>:2379` with the address of any PD node. For example:
    >
    > ```shell
    > tiup ctl:v6.1.1 pd -u http://192.168.1.4:2379 store limit all engine tiflash 60 add-peer
    > ```

    Within a few minutes, you will observe a significant increase in CPU and disk IO resource usage of the TiFlash nodes, and TiFlash should create replicas faster. At the same time, the TiKV nodes' CPU and disk IO resource usage increases as well.

    If the TiKV and TiFlash nodes still have spare resources at this point and the latency of your online service does not increase significantly, you can further ease the limit, for example, triple the original speed:

    ```shell
    tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 90 add-peer
    ```

3. After the TiFlash replication is complete, revert to the default configuration to reduce the impact on online services.

   Execute the following PD Control command to restore the default new replica speed limit:

   ```shell
   tiup ctl:v<CLUSTER_VERSION> pd -u http://<PD_ADDRESS>:2379 store limit all engine tiflash 30 add-peer
   ```

   Execute the following SQL statements to restore the default snapshot write speed limit:

   ```sql
   SET CONFIG tikv `server.snap-max-write-bytes-per-sec` = '100MiB';
   SET CONFIG tiflash `raftstore-proxy.server.snap-max-write-bytes-per-sec` = '100MiB';
   ```

## Set available zones

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This section is not applicable to TiDB Cloud.

</CustomContent>

When configuring replicas, if you need to distribute TiFlash replicas to multiple data centers for disaster recovery, you can configure available zones by following the steps below:

1. Specify labels for TiFlash nodes in the cluster configuration file.

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

    Note that the `flash.proxy.labels` configuration in earlier versions cannot handle special characters in the available zone name correctly. It is recommended to use the `server.labels` in `learner_config` to configure the name of an available zone.

2. After starting a cluster, specify the labels when creating replicas.

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE table_name SET TIFLASH REPLICA count LOCATION LABELS location_labels;
    ```

    For example:

    {{< copyable "sql" >}}

    ```sql
    ALTER TABLE t SET TIFLASH REPLICA 2 LOCATION LABELS "zone";
    ```

3. PD schedules the replicas based on the labels. In this example, PD respectively schedules two replicas of the table `t` to two available zones. You can use pd-ctl to view the scheduling.

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

For more information about scheduling replicas by using labels, see [Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md), [Multiple Data Centers in One City Deployment](/multi-data-centers-in-one-city-deployment.md), and [Three Data Centers in Two Cities Deployment](/three-data-centers-in-two-cities-deployment.md).

</CustomContent>
