---
title: TiDB Cloud Replication
summary: Learn how to create a replica to stream data from a primary TiDB cluster to a secondary TiDB cluster.
---

# TiDB Cloud Replication

TiDB Cloud Replication is a feature that allows you to create a continuously replicated readable secondary TiDB cluster for a primary TiDB cluster in TiDB Cloud. This readable secondary cluster (also known as cross-region replication, secondary replication, or geo-replication) can be in the same region as the primary TiDB cluster, or more commonly, in a different region.

With TiDB Cloud Replication, you can perform quick disaster recovery of a database in the event of a regional disaster or large-scale failure, which helps achieve business continuity. Once a secondary cluster is set up, you can manually initiate geographic failover to the secondary cluster in a different region.

> **Warning:**
>
> Currently, the **TiDB Cloud Replication** feature is in beta with the following limitations:
>
> * One primary cluster can only have one replication.
> * You cannot use a secondary cluster as a source of **TiDB Cloud Replication** to another cluster.
> * **TiDB Cloud Replication** contradicts [**Sink to Apache Kafka**](/tidb-cloud/changefeed-sink-to-apache-kafka.md) and [**Sink to MySQL**](/tidb-cloud/changefeed-sink-to-mysql.md). When **TiDB Cloud Replication** is enabled, neither the primary nor the secondary cluster can use the **Sink to Apache Kafka** or **Sink to MySQL** changefeed and vice versa.
> * Because TiDB Cloud uses TiCDC to establish replication, it has the same [restrictions as TiCDC](https://docs.pingcap.com/tidb/stable/ticdc-overview#restrictions).
> * **TiDB Cloud Replication** is only available upon request. To request this feature, click **?** in the lower-right corner of the [TiDB Cloud console](https://tidbcloud.com) and click **Request Support**. Then, fill in "Apply for TiDB Cloud Replication" in the **Description** field and click **Send**.

To support application replication, you must deploy your applications in both primary and secondary regions, and ensure that each application is connected to the TiDB cluster in the same region. The applications in the secondary region are on standby. When the primary region fails, you can initiate a "Detach" operation to make the TiDB cluster in the secondary region active, and then transfer all data traffic to the applications in the secondary region.

The following diagram illustrates a typical deployment of a geo-redundant cloud application using TiDB Cloud Replication:

<!-- https://www.figma.com/file/DaevXzW4aq35QodwZEkcTS/DBaaS-Architecture-Chart-(high-level)-(Copy)?node-id=0%3A1 -->
![TiDB Cloud Replication](/media/tidb-cloud/changefeed-replication-deployment.png)

Creating a secondary TiDB cluster is only a part of the business continuity solution. To recover an application (or service) end-to-end after a catastrophic failure, you also need to ensure that all components and dependent services of the application can be restored.

- Check whether each component of the application is resilient to the same failures and become available within recovery time objective (RTO) of your application. The typical components of an application include client software (such as browsers with custom JavaScript), web front ends, storage, and DNS.
- Identify all dependent services, check the guarantees and capabilities of these services, and ensure that your application is operational during a failover of these services.

## Terminology and capabilities of TiDB Cloud Replication

### Automatic asynchronous replication

For each primary TiDB cluster, only one secondary cluster can be created. TiDB Cloud makes a full backup of the primary TiDB cluster and then restores the backup to the newly created secondary cluster, which makes sure that the secondary cluster has all the existing data. After the secondary cluster is created, all data changes on the primary cluster will be replicated asynchronously to the secondary cluster.

### Readable secondary cluster

The secondary cluster is in the read-only mode. If you have any read-only workload with low real-time data requirements, you can distribute it to the secondary cluster.

To satisfy read-intensive scenarios in the same region, you can use **TiDB Cloud Replication** to create a readable secondary cluster in the same region as the primary cluster. However, because a secondary cluster in the same region does not provide additional resiliency for large-scale outages or catastrophic failures, do not use it as a failover target for regional disaster recovery purposes.

### Planned Detach

**Planned Detach** can be triggered by you manually. It is used for planned maintenance in most cases, such as disaster recovery drills. **Planned detach** makes sure that all data changes are replicated to the secondary cluster without data loss (RPO=0). For RTO, it depends on the replication lag between primary and secondary clusters. In most cases, the RTO is at a level of minutes.

**Planned Detach** detaches the secondary cluster from the primary cluster into an individual cluster. When **Planned Detach** is triggered, it performs the following steps:

1. Sets the primary cluster as read-only, to prevent any new transaction from being committed to the primary cluster.
2. Waits until the secondary cluster is fully synced with the primary cluster.
3. Stops the replication from the primary to the secondary cluster.
4. Sets the original secondary cluster as writable, which makes it available to serve your business.

After **Planned Detach** is finished, the original primary cluster is set as read-only. If you still need to write to the original primary cluster, you can do one of the following to set the cluster as writable explicitly:

- Go to the cluster details page, click **Settings**, and then click the **Make Writable** drop-down button.
- Connect to the SQL port of the original primary cluster and execute the following statement:

    {{< copyable "sql" >}}

    ```sql
    set global tidb_super_read_only=OFF;
    ```

### Force Detach

To recover from an unplanned outage, use **Force Detach**. In the event of a catastrophic failure in the region where the primary cluster is located, you should use **Force Detach** so that the secondary cluster can serve the business as quickly as possible, ensuring business continuity. Because this operation makes the secondary cluster serve as an individual cluster immediately and does not wait for any unreplicated data, the RPO depends on the Primary-Secondary replication lag, while the RTO depends on how quickly **Force Detach** is triggered by you.

**Force Detach** detaches the secondary cluster from the primary cluster into an individual cluster. When **Force Detach** is triggered, it performs the following steps:

1. Stops data replication from the primary to the secondary cluster immediately.
2. Sets the original secondary cluster as writable so that it can start serving your workload.
3. If the original primary cluster is still accessible, or when the original primary cluster recovers, TiDB Cloud sets it as read-only to avoid any new transaction being committed to it.

Once the original primary cluster is recovered from the outage, you still have the opportunity to review transactions that have been executed in the original primary cluster but not in the original secondary cluster by comparing the data in the two clusters, and decide whether to manually replicate these unsynchronized transactions to the original secondary cluster based on your business situation.

The data replication topology between primary and secondary clusters does not exist anymore after you detach the secondary cluster. The original primary cluster is set to the read-only mode and the original secondary cluster becomes writable. If any DML or DDL is planned on the original primary cluster, you need to disable the read-only mode manually on it by doing one of the following:

- Go to the cluster details page, click **Settings**, and then click the **Make Writable** drop-down button.
- Connect to the SQL port of the original primary cluster and execute the following statement:

    {{< copyable "sql" >}}

    ```sql
    set global tidb_super_read_only=OFF;
    ```

## Configure TiDB Cloud Replication

To configure TiDB Cloud Replication, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of your TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Click **Create a replica of your TiDB Cluster**.
3. Fill in the username and password of your database.
4. Choose the region of the secondary cluster.
5. Click **Create**. After a while, the sink will begin its work, and the status of the sink will be changed to "**Producing**".

To trigger a **Planned Detach** or **Force Detach**, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of your TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Click **Create a replica of your TiDB Cluster**.
3. Click **Planned Detach** or **Force Detach**.

## Scale the primary cluster

You can scale out or scale in the primary cluster without disconnecting the secondary cluster. When the primary cluster is scaled, the secondary cluster follows the same scaling automatically.

## Monitor the primary-secondary lag

To monitor lag concerning the RPO, do the following:

1. In the [TiDB Cloud console](https://tidbcloud.com), navigate to the cluster overview page of your TiDB cluster, and then click **Changefeed** in the left navigation pane.
2. Click **Create a replica of your TiDB Cluster**.
3. You can see the lag of the primary-secondary cluster.
