---
title: What's New in TiDB 4.0
summary: Learn the new features of TiDB v4.0.
aliases: ['/docs/dev/whats-new-in-tidb-4.0/']
---

# What’s New in TiDB 4.0

TiDB v4.0 was officially released on May 28, 2020. In this release, we have made great improvements in stability, usability, performance, security, and features. This document briefly introduces the most notable improvements for you. You can decide whether to upgrade to v4.0 based on your needs. For the complete list of new features and bug fixes, you can check our [earlier v4.0 release notes](/releases/release-notes.md#40).

## Scheduling

+ Hotspot scheduling policy supports more dimensions. In addition to using write or read traffic as the scheduling basis, keys are introduced as a new dimension for the scheduling policy, which might, to a large extent, mitigate the CPU usage imbalance caused by the previous single-dimensional policy. See [TiDB Scheduling](/tidb-scheduling.md) for details.

## Storage engine

+ TiFlash is a key component that makes TiDB essentially a Hybrid Transactional/Analytical Processing (HTAP) database. Complying with the Multi-Raft Learner protocol, TiFlash replicates data from TiKV in real time, which ensures that data is strongly consistent between TiKV, a row-based storage engine, and TiFlash, a columnar storage engine. You can deploy TiKV and TiFlash on different machines to isolate HTAP resources. See [TiFlash](/tiflash/tiflash-overview.md) for details.
+ In v4.0, TiKV provides new storage formats to improve the efficiency of encoding and decoding in the wide-table scenario.

## TiDB Dashboard

Using [TiDB Dashboard](/dashboard/dashboard-intro.md), DBAs can quickly find out the cluster topology, cluster configuration, log information, hardware information, operating system, slow queries, SQL query information, diagnostics, and so on. These information helps them quickly learn and analyze various system metrics using SQL statements:

- Cluster Info, which is the running status of all components in the cluster (including TiDB, TiKV, and PD) and the running status of the machine on which these components are hosted.
- Key Visualizer, which visually displays the traffic of TiDB over a certain period of time and can be used by DBAs to analyze the usage mode of TiDB and the traffic hotspots.
- SQL Statements, which records all the SQL statements that have been executed and the related statistics, including the execution times and the total time of execution. This helps you quickly analyze the SQL execution in TiDB and find out the hot SQL statements.
- Slow Queries, which summarizes all slow queries in the cluster to help you locate some slow queries.
- Cluster Diagnostics. TiDB automatically and regularly diagnoses the potential problems of the cluster, and summarizes the diagnostic results and some cluster-related load monitoring information into a diagnostic report. The diagnostic report is displayed on a web page. You can browse and circulate the report offline after saving it using a browser.
- Search Logs, which enables DBAs to visually search and query the log information, helps them analyze system issues, and improves their maintenance efficiency.

## Deployment and maintenance tools

TiUP is a new package manager tool introduced in v4.0 that is used to manage all packages in the TiDB ecosystem. The tool provides package management, Playground, Cluster, TUF, and offline deployment, which makes the installation, deployment, and maintenance of TiDB manageable within a single tool. Therefore, DBAs can enjoy higher efficiency in deploying and maintaining TiDB. See [TiUP](/tiup/tiup-overview.md) for details. The features of TiUP are summarized as follows:

- Component management, which enables you to query the component information, and to easily install, upgrade, and uninstall the cluster. For DBAs, managing TiDB components can be much easier.
- Cluster management using the TiUP Cluster component, which enables you to deploy and maintain TiDB with a single command. The management includes installation, deployment, scaling, upgrade, configuration changes, starting and stopping a cluster, restarting a cluster, and querying the cluster information. The TiUP Cluster component supports managing multiple TiDB clusters.
- Local deployment using TiUP Playground, which enables you to quickly deploy a local TiDB cluster and learn the basic features of TiDB. Note that this feature is for quick start only and cannot be used for the production environment.
- Private mirror management using TiUP Mirror, which provides you a solution of building a private mirror and offline deployment when the official TiUP mirror is inaccessible via the public network.
- Benchmark test using TiUP Benchmark, which enables you to easily deploy the benchmark performance test tool, and provides workload for TPC-C and TPC-H tests.

## Transaction

- The pessimistic transaction is now provided for general availability as the default transaction mode. Support the Read Committed isolation level and the `SELECT FOR UPDATE NOWAIT` syntax. See [Pessimistic Transaction Model](/pessimistic-transaction.md) for details.
- Support large transactions. Increase the upper limit on transaction size from 10 MB to 10 GB. Support both the pessimistic transaction and optimistic transaction. See [Transaction size limit](/transaction-overview.md#transaction-size-limit) for details.

## SQL features

- Introduce the automatic capture and evolution of SQL Bind to SQL Plan Management, which improves the usability and stability of the execution plan. See [SQL Plan Management](/sql-plan-management.md) for details.
- Add 15 new SQL Hints to control the behavior of the optimizer that generates the execution plan and the behavior of the execution engine that executes queries. See [SQL Hint](/optimizer-hints.md) for details.
- Support the `SELECT INTO OUTFILE` statement which is used to export table data into the specified text file. Using this feature with Load Data, you can easily import and export data between databases.
- Support customizing the sequence object and provide the `CACHE/NO_CACHE` and `CYCLE/NO_CYCLE` options to define different sequence attributes. You can use the sequence to replace the third-party ID generation. See [Sequence](/sql-statements/sql-statement-create-sequence.md) for details.
- Add the `FLASHBACK` statement to support recovering the truncated tables. See [`Flashback Table`](/sql-statements/sql-statement-flashback-table.md) for details.
- Support writing the intermediate results of Join and Sort to the local disk when you make queries, which avoids the Out of Memory (OOM) issue because the queries occupy excessive memory. This also improves system stability.
- Optimize the output of `EXPLAIN` and `EXPLAIN ANALYZE`. More information is shown in the result, which improves troubleshooting efficiency. See [Explain Analyze](/sql-statements/sql-statement-explain-analyze.md) and [Explain](/sql-statements/sql-statement-explain.md) for details.
- Support using the Index Merge feature to access tables. When you make a query on a single table, the TiDB optimizer automatically reads multiple index data according to the query condition and makes a union of the result, which improves the performance of querying on a single table. See [Index Merge](/explain-index-merge.md) for details.
- Support `AUTO_RANDOM` keys as an extended syntax for the TiDB columnar attribute. `AUTO_RANDOM` is designed to address the hotspot issue caused by the auto-increment column and provides a low-cost migration solution from MySQL for users who work with auto-increment columns. See [`AUTO_RANDOM` Key](/auto-random.md) for details.
- Add system tables that provide information of cluster topology, configuration, logs, hardware, operating systems, and slow queries, which helps DBAs to quickly learn, analyze system metrics. See [Information Schema](/information-schema/information-schema.md) and [SQL Diagnosis](/information-schema/information-schema-sql-diagnostics.md) for details.

    - Add system tables that provide information of cluster topology, configuration, logs, hardware, operating systems to help DBAs quickly learn the cluster configuration and status:
        - The `cluster_info` table that stores the cluster topology information.
        - The `cluster_log` table that stores log information.
        - The `cluster_hardware` and `cluster_systeminfo` tables that save the server information of hardware and operating system.
    - Add information tables that provide information of slow queries, diagnostic results, and performance monitoring to help DBAs quickly analyze the system bottleneck:
        - The `cluster_slow_query` table that records the global slow query information.
        - The `cluster_processlist` table that records the global processlist.
        - The `inspection_result` table. The automatic performance diagnostics feature is introduced in v4.0 to automatically analyze the system bottleneck and output the performance analysis report for DBAs. Using this feature, DBAs can easily troubleshoot common issues and anomalies to improve maintenance efficiency.
        - The `metrics_summary` and `metric_summary_by_label` tables that records all monitoring metrics. Using this table, DBAs can use SQL statements to access all monitoring metrics and compare these metrics with historical metrics to locate and analyze anomalies.
        - The `inspection_summary` table that records the key monitoring metrics on  different data links or access links. This table makes it easier for DBAs to locate, access, and analyze common anomalies on data links, such as read links or write links.

## Character set and collation

Support case-insensitive and accent-insensitive `utf8mb4_general_ci` and `utf8_general_ci` collations. See [Character Set and Collation](/character-set-and-collation.md) for details.

## Security

+ Improve the encrypted communication between the client and server, and between components, which ensures data security and prevents any sent and received data from being read and modified by illegal hackers. Mainly support the certificate-based login authentication, updating certificate online, and verifying the CommonName attribute of the TLS certificate. See [Enable TLS Between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md) for details.

+ Transparent Data Encryption (TDE) is a new feature that provides protection for the entire database. This feature, when enabled, is transparent to applications that are connected to TiDB and does not require any change to the existing applications. Because this TDE feature operates at the file level, TiDB encrypts data before writing data to disk, and decrypts data before reading data from memory to ensure data security. Currently, the AES128-CTR, AES192-CTR, and AES256-CTR encryption algorithms are supported. You can manage keys via AWS KMS. See [Encryption at Rest](/encryption-at-rest.md) for details.

## Backup and Restore

Support the Backup & Restore (BR) feature to quickly back up and restore data of a single TiDB cluster to ensure data reliability and to meet enterprises’ needs of backup and restore or the graded protection of information security. Support quickly backing up and restoring all data or a certain range of sorted data. See [Backup & Restore](/br/backup-and-restore-tool.md) for details.

## Service level features

+ Support caching the execution plan of `Prepare` or `Execute` to improve the SQL execution efficiency.
+ Support self-adapting to the thread pool and streamlining the number of thread pools. Optimize the processing and scheduling of requests to improve product usability and performance.
+ The Follower Read feature refers to using any follower replica of a Region to serve a read request under the premise of strongly consistent reads. This feature improves the throughput of the TiDB cluster and reduces the load of the leader. It contains a series of load balancing mechanisms that offload TiKV read loads from the leader replica to the follower replica in a Region. TiKV's Follower Read implementation guarantees the consistency of data reading; combined with Snapshot Isolation in TiDB, this implementation provides users with strongly consistent reads. See [Follower Read](/follower-read.md) for details.

## TiCDC

TiCDC is a tool for replicating the incremental data of TiDB. This tool is implemented by pulling TiKV change logs, which ensures high reliability and availability of data. You can subscribe to the change information of data, and the system automatically sends data to the downstream. Currently, the downstream database must be MySQL compatible (such as MySQL and TiDB) or Kafka and Pulsar. You can also extend the supported downstream systems based on the [TiCDC Open Protocol](/ticdc/ticdc-open-protocol.md). See [TiCDC](/ticdc/ticdc-overview.md) for details.
