---
title: Explore HTAP
summary: Learn how to explore and use the features of TiDB HTAP.
---

# Explore HTAP

This guide describes how to explore and use the features of TiDB Hybrid Transactional and Analytical Processing (HTAP).

> **Note:**
>
> If you are new to TiDB HTAP and want to start using it quickly, see [Quick start with HTAP](/quick-start-with-htap.md).

## Use cases

TiDB HTAP can handle the massive data that increases rapidly, reduce the cost of DevOps, and be deployed in either on-premises or cloud environments easily, which brings the value of data assets in real time.

The following are the typical use cases of HTAP:

- Hybrid workload

    When using TiDB for real-time Online Analytical Processing (OLAP) in hybrid load scenarios, you only need to provide an entry point of TiDB to your data. TiDB automatically selects different processing engines based on the specific business.

- Real-time stream processing

    When using TiDB in real-time stream processing scenarios, TiDB ensures that all the data flowed in constantly can be queried in real time. At the same time, TiDB also can handle highly concurrent data workloads and Business Intelligence (BI) queries.

- Data hub

    When using TiDB as a data hub, TiDB can meet specific business needs by seamlessly connecting the data for the application and the data warehouse.

For more information about use cases of TiDB HTAP, see [blogs about HTAP on the PingCAP website](https://en.pingcap.com/blog/tag/HTAP).

## Architecture

In TiDB, a row-based storage engine [TiKV](/tikv-overview.md) for Online Transactional Processing (OLTP) and a columnar storage engine [TiFlash](/tiflash/tiflash-overview.md) for Online Analytical Processing (OLAP) co-exist, replicate data automatically, and keep strong consistency. 

For more information about the architecture, see [architecture of TiDB HTAP](/tiflash/tiflash-overview.md#architecture).

## Environment preparation 

Before exploring the features of TiDB HTAP, you need to deploy TiDB and the corresponding storage engines according to the data volume. If the data volume is large (for example, 100 T), it is recommended to use TiFlash Massively Parallel Processing (MPP) as the primary solution and TiSpark as the supplementary solution.

- TiFlash

    - If you have deployed a TiDB cluster with no TiFlash node, add the TiFlash nodes in the current TiDB cluster. For detailed information, see [Scale out a TiFlash cluster](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster).
    - If you have not deployed a TiDB cluster, see [Deploy a TiDB Cluster using TiUP](/production-deployment-using-tiup.md).  Based on the minimal TiDB topology, you also need to deploy the [topology of TiFlash](/tiflash-deployment-topology.md).
    - When deciding how to choose the number of TiFlash nodes, consider the following scenarios:

        - If your use case requires OLTP with small-scale analytical processing and Ad-Hoc queries, deploy one or several TiFlash nodes. They can dramatically increase the speed of analytic queries.
        - If the OLTP throughput does not cause significant pressure to I/O usage rate of the TiFlash nodes, each TiFlash node uses more resources for computation, and thus the TiFlash cluster can have near-linear scalability. The number of TiFlash nodes should be tuned based on expected performance and response time.
        - If the OLTP throughput is relatively high (for example, the write or update throughput is higher than 10 million lines/hours), due to the limited write capacity of network and physical disks, the I/O between TiKV and TiFlash becomes a bottleneck and is also prone to read and write hotspots. In this case, the number of TiFlash nodes has a complex non-linear relationship with the computation volume of analytical processing, so you need to tune the number of TiFlash nodes based on the actual status of the system.

- TiSpark

    - If your data needs to be analyzed with Spark, deploy TiSpark (Spark 3.x is not currently supported). For specific process, see [TiSpark User Guide](/tispark-overview.md).

<!--    - Real-time stream processing
  - If you want to build an efficient and easy-to-use real-time data warehouse with TiDB and Flink, you are welcome to participate in Apache Flink x TiDB meetups.-->

## Data preparation 

After TiFlash is deployed, TiKV does not replicate data to TiFlash automatically. You need to manually specify which tables need to be replicated to TiFlash. After that, TiDB creates the corresponding TiFlash replicas.

- If there is no data in the TiDB Cluster, migrate the data to TiDB first. For detailed information, see [data migration](/migration-overview.md).
- If the TiDB cluster already has the replicated data from upstream, after TiFlash is deployed, data replication does not automatically begin. You need to manually specify the tables to be replicated to TiFlash. For detailed information, see [Use TiFlash](/tiflash/use-tiflash.md).

## Data processing

With TiDB, you can simply enter SQL statements for query or write requests. For the tables with TiFlash replicas, TiDB uses the front-end optimizer to automatically choose the optimal execution plan.

> **Note:**
> 
> The MPP mode of TiFlash is enabled by default. When an SQL statement is executed, TiDB automatically determines whether to run in the MPP mode through the optimizer.
>
> - To disable the MPP mode of TiFlash, set the value of the [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50) system variable to `OFF`.
> - To forcibly enable MPP mode of TiFlash for query execution, set the values of [tidb_allow_mpp](/system-variables.md#tidb_allow_mpp-new-in-v50) and [tidb_enforce_mpp](/system-variables.md#tidb_enforce_mpp-new-in-v51) to `ON`.
> - To check whether TiDB chooses the MPP mode to execute a specific query, see [Explain Statements in the MPP Mode](/explain-mpp.md#explain-statements-in-the-mpp-mode). If the output of `EXPLAIN` statement includes the `ExchangeSender` and `ExchangeReceiver` operators, the MPP mode is in use.

## Performance monitoring

When using TiDB, you can monitor the TiDB cluster status and performance metrics in either of the following ways:

- [TiDB Dashboard](/dashboard/dashboard-intro.md): you can see the overall running status of the TiDB cluster, analyse distribution and trends of read and write traffic, and learn the detailed execution information of slow queries.
- [Monitoring system (Prometheus & Grafana)](/grafana-overview-dashboard.md): you can see the monitoring parameters of TiDB cluster-related componants including PD, TiDB, TiKV, TiFlash,TiCDC, and Node_exporter.

To see the alert rules of TiDB cluster and TiFlash cluster, see [TiDB cluster alert rules](/alert-rules.md) and [TiFlash alert rules](/tiflash/tiflash-alert-rules.md).

## Troubleshooting

If any issue occurs during using TiDB, refer to the following documents:

- [Analyze slow queries](/analyze-slow-queries.md)
- [Identify expensive queries](/identify-expensive-queries.md)
- [Troubleshoot hotspot issues](/troubleshoot-hot-spot-issues.md)
- [TiDB cluster troubleshooting guide](/troubleshoot-tidb-cluster.md)
- [Troubleshoot a TiFlash Cluster](/tiflash/troubleshoot-tiflash.md)

You are also welcome to create [Github Issues](https://github.com/pingcap/tiflash/issues) or submit your questions on [AskTUG](https://asktug.com/).

## What's next

- To check the TiFlash version, critical logs, system tables, see [Maintain a TiFlash cluster](/tiflash/maintain-tiflash.md).
- To remove a specific TiFlash node, see [Scale out a TiFlash cluster](/scale-tidb-using-tiup.md#scale-out-a-tiflash-cluster).
