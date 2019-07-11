# TiDB Documentation

## Documentation List

+ About TiDB
  - [TiDB Introduction](overview.md)
  - [TiDB Architecture](architecture.md)
+ Quick Start
  - [TiDB Quick Start Guide](QUICKSTART.md)
  - [Basic SQL Statements](try-tidb.md)
  - [Bikeshare Example Database](bikeshare-example-database.md)
+ TiDB User Guide
  + TiDB Server Administration
    - [The TiDB Server](sql/tidb-server.md)
    - [The TiDB Command Options](sql/server-command-option.md)
    - [The TiDB Data Directory](sql/tidb-server.md#tidb-data-directory)
    - [The TiDB System Database](sql/system-database.md)
    - [The TiDB System Variables](sql/variable.md)
    - [The TiDB Specific System Variables](sql/tidb-specific.md)
    - [The TiDB Server Logs](sql/tidb-server.md#tidb-server-logs)
    - [The TiDB Access Privilege System](sql/privilege.md)
    - [TiDB User Account Management](sql/user-account-management.md)
    - [Use Encrypted Connections](sql/encrypted-connections.md)
  + SQL Optimization and Execution
    - [SQL Optimization Process](sql/sql-optimizer-overview.md)
    - [Understand the Query Execution Plan](sql/understanding-the-query-execution-plan.md)
    - [Introduction to Statistics](sql/statistics.md)
  + Language Structure
    - [Literal Values](sql/literal-values.md)
    - [Schema Object Names](sql/schema-object-names.md)
    - [Keywords and Reserved Words](sql/keywords-and-reserved-words.md)
    - [User-Defined Variables](sql/user-defined-variables.md)
    - [Expression Syntax](sql/expression-syntax.md)
    - [Comment Syntax](sql/comment-syntax.md)
  + Globalization
    - [Character Set Support](sql/character-set-support.md)
    - [Character Set Configuration](sql/character-set-configuration.md)
    - [Time Zone Support](sql/time-zone.md)
  + Data Types
    - [Numeric Types](sql/datatype.md#numeric-types)
    - [Date and Time Types](sql/datatype.md#date-and-time-types)
    - [String Types](sql/datatype.md#string-types)
    - [JSON Types](sql/datatype.md#json-types)
    - [The ENUM data type](sql/datatype.md#the-enum-data-type)
    - [The SET Type](sql/datatype.md#the-set-type)
    - [Data Type Default Values](sql/datatype.md#data-type-default-values)
  + Functions and Operators
    - [Function and Operator Reference](sql/functions-and-operators-reference.md)
    - [Type Conversion in Expression Evaluation](sql/type-conversion-in-expression-evaluation.md)
    - [Operators](sql/operators.md)
    - [Control Flow Functions](sql/control-flow-functions.md)
    - [String Functions](sql/string-functions.md)
    - [Numeric Functions and Operators](sql/numeric-functions-and-operators.md)
    - [Date and Time Functions](sql/date-and-time-functions.md)
    - [Bit Functions and Operators](sql/bit-functions-and-operators.md)
    - [Cast Functions and Operators](sql/cast-functions-and-operators.md)
    - [Encryption and Compression Functions](sql/encryption-and-compression-functions.md)
    - [Information Functions](sql/information-functions.md)
    - [JSON Functions](sql/json-functions.md)
    - [Aggregate (GROUP BY) Functions](sql/aggregate-group-by-functions.md)
    - [Miscellaneous Functions](sql/miscellaneous-functions.md)
    - [Precision Math](sql/precision-math.md)
  + SQL Statement Syntax
    - [Data Definition Statements](sql/ddl.md)
    - [Data Manipulation Statements](sql/dml.md)
    - [Transactions](sql/transaction.md)
    - [Database Administration Statements](sql/admin.md)
    - [Prepared SQL Statement Syntax](sql/prepare.md)
    - [Utility Statements](sql/util.md)
    - [TiDB SQL Syntax Diagram](https://pingcap.github.io/sqlgram/)
  - [Generated Columns](sql/generated-columns.md)
  - [Connectors and APIs](sql/connection-and-APIs.md)
  - [TiDB Transaction Isolation Levels](sql/transaction-isolation.md)
  - [Error Codes and Troubleshooting](sql/error.md)
  - [Compatibility with MySQL](sql/mysql-compatibility.md)
  - [TiDB Memory Control](sql/tidb-memory-control.md)
  - [Slow Query Log](sql/slow-query.md)
  + Advanced Usage
    - [Read Data From History Versions](op-guide/history-read.md)
    - [Garbage Collection (GC)](op-guide/gc.md)
+ TiDB Operations Guide
  - [Hardware and Software Requirements](op-guide/recommendation.md)
  + Deploy
    - [Ansible Deployment (Recommended)](op-guide/ansible-deployment.md)
    - [Offline Deployment Using Ansible](op-guide/offline-ansible-deployment.md)
    - [Docker Deployment](op-guide/docker-deployment.md)
    - [Docker Compose Deployment](op-guide/docker-compose.md)
    - [Cross-DC Deployment Solutions](op-guide/cross-dc-deployment.md)
    - [Kubernetes Deployment](op-guide/kubernetes.md)
  + Configure
    - [Configuration Flags](op-guide/configuration.md)
    - [Configuration File Description](op-guide/tidb-config-file.md)
    - [Modify Component Configuration Using Ansible](op-guide/ansible-deployment-rolling-update.md#modify-component-configuration)
    - [Enable TLS Authentication](op-guide/security.md)
    - [Generate Self-signed Certificates](op-guide/generate-self-signed-certificates.md)
    - [Cluster Topology Configuration](op-guide/location-awareness.md)
  + Monitor
    - [Monitoring Framework Overview](op-guide/monitor-overview.md)
    + Key Monitoring Metrics
      - [Overview](op-guide/dashboard-overview-info.md)
      - [TiDB](op-guide/tidb-dashboard-info.md)
      - [PD](op-guide/dashboard-pd-info.md)
      - [TiKV](op-guide/dashboard-tikv-info.md)
    - [Monitor a TiDB Cluster](op-guide/monitor.md)
  + Scale
    - [Scale a TiDB Cluster](op-guide/horizontal-scale.md)
    - [Scale Using Ansible](op-guide/ansible-deployment-scale.md)
  + Upgrade
    - [Upgrade the Component Version](op-guide/ansible-deployment-rolling-update.md#upgrade-the-component-version)
    - [TiDB 2.0 Upgrade Guide](op-guide/tidb-v2.0-upgrade-guide.md)
    - [TiDB 2.1 Upgrade Guide](op-guide/tidb-v2.1-upgrade-guide.md)
    - [FAQs After Upgrade](op-guide/upgrade-faq.md)
  - [Tune Performance](op-guide/tune-tikv.md)
  + Backup and Migrate
    - [Backup and Restore](op-guide/backup-restore.md)
    + Migrate
      - [Migration Overview](op-guide/migration-overview.md)
      - [Migrate All the Data](op-guide/migration.md#use-the-mydumper--loader-tool-to-export-and-import-all-the-data)
      - [Migrate the Data Incrementally](op-guide/migration.md#use-the-syncer-tool-to-import-data-incrementally-optional)
  - [TiDB-Ansible Common Operations](op-guide/ansible-operation.md)
  - [Troubleshoot](trouble-shooting.md)
+ TiDB Enterprise Tools
  - [Syncer](tools/syncer.md)
  - [mydumper](tools/mydumper.md)
  - [Loader](tools/loader.md)
  + Data Migration
    - [Overview](tools/data-migration-overview.md)
    - [Deploy](tools/data-migration-deployment.md)
    - [Replicate Data](tools/data-migration-practice.md)
    + Configure
      - [Configuration Overview](tools/dm-configuration-file-overview.md)
      - [Task Configuration File](tools/dm-task-configuration-file-intro.md)
      - [Configuration Options](tools/dm-task-config-argument-description.md)
    + Sharding Data Solution
      - [Overview and Design Details](tools/dm-sharding-solution.md)
      - [Sharding DDL Usage Restrictions](tools/dm-sharding-solution.md#sharding-ddl-usage-restrictions)
      - [Troubleshoot Sharding DDL Locks](tools/troubleshooting-sharding-ddl-locks.md)
    - [Monitor](tools/dm-monitor.md)
    - [Manage the Task](tools/data-migration-manage-task.md)
    - [Cluster Operations](tools/data-migration-cluster-operations.md)
    - [Upgrade Loader or Syncer to DM](tools/upgrade-loader-or-syncer-to-dm.md)
    - [Troubleshoot](tools/data-migration-troubleshooting.md)
  + TiDB-Lightning
    - [Overview](tools/lightning/overview-architecture.md)
    - [Deployment](tools/lightning/deployment.md)
    - [Checkpoints](tools/lightning/checkpoints.md)
    - [Table Filter](tools/lightning/filter.md)
    - [Monitor](tools/lightning/monitor.md)
    - [Troubleshooting](tools/lightning/errors.md)
    - [FAQs](tools/lightning/faq.md)
  - [TiDB-Binlog](tools/tidb-binlog-cluster.md)
  - [PD Control](tools/pd-control.md)
  - [PD Recover](tools/pd-recover.md)
  - [TiKV Control](https://github.com/tikv/tikv/blob/master/docs/reference/tools/tikv-control.md)
  - [TiDB Controller](tools/tidb-controller.md)
+ [TiKV Documentation](https://github.com/tikv/tikv/wiki)
+ TiSpark Documentation
  - [Quick Start Guide](tispark/tispark-quick-start-guide.md)
  - [User Guide](tispark/tispark-user-guide.md)
- [Frequently Asked Questions (FAQ)](FAQ.md)
- [TiDB Best Practices](https://pingcap.com/blog/2017-07-24-tidbbestpractice/)
+ [Releases](releases/rn.md)
  - [2.0.11](releases/2.0.11.md)
  - [2.1.2](releases/2.1.2.md)
  - [2.0.10](releases/2.0.10.md)
  - [2.1.1](releases/2.1.1.md)
  - [2.1 GA](releases/2.1ga.md)
  - [2.0.9](releases/209.md)
  - [2.1 RC5](releases/21rc5.md)
  - [2.1 RC4](releases/21rc4.md)
  - [2.0.8](releases/208.md)
  - [2.1 RC3](releases/21rc3.md)
  - [2.1 RC2](releases/21rc2.md)
  - [2.0.7](releases/207.md)
  - [2.1 RC1](releases/21rc1.md)
  - [2.0.6](releases/206.md)
  - [2.0.5](releases/205.md)
  - [2.1 Beta](releases/21beta.md)
  - [2.0.4](releases/204.md)
  - [2.0.3](releases/203.md)
  - [2.0.2](releases/202.md)
  - [2.0.1](releases/201.md)
  - [2.0](releases/2.0ga.md)
  - [2.0 RC5](releases/2rc5.md)
  - [2.0 RC4](releases/2rc4.md)
  - [2.0 RC3](releases/2rc3.md)
  - [2.0 RC1](releases/2rc1.md)
  - [1.1 Beta](releases/11beta.md)
  - [1.0.8](releases/108.md)
  - [1.0.7](releases/107.md)
  - [1.1 Alpha](releases/11alpha.md)
  - [1.0.6](releases/106.md)
  - [1.0.5](releases/105.md)
  - [1.0.4](releases/104.md)
  - [1.0.3](releases/103.md)
  - [1.0.2](releases/102.md)
  - [1.0.1](releases/101.md)
  - [1.0](releases/ga.md)
  - [Pre-GA](releases/prega.md)
  - [RC4](releases/rc4.md)
  - [RC3](releases/rc3.md)
  - [RC2](releases/rc2.md)
  - [RC1](releases/rc1.md)
- [TiDB Adopters](adopters.md)
- [TiDB Roadmap](ROADMAP.md)
- [Connect with us](community.md)
+ More Resources
  - [PingCAP Blog](https://pingcap.com/blog/)
  - [Weekly Update](https://pingcap.com/weekly/)

## TiDB Introduction

TiDB (The pronunciation is: /'taɪdiːbi:/ tai-D-B, etymology: titanium) is an open-source distributed scalable Hybrid Transactional and Analytical Processing (HTAP) database. It features infinite horizontal scalability, strong consistency, and high availability. TiDB is MySQL compatible and serves as a one-stop data warehouse for both OLTP (Online Transactional Processing) and OLAP (Online Analytical Processing) workloads.

- __Horizontal scalability__

    TiDB provides horizontal scalability simply by adding new nodes. Never worry about infrastructure capacity ever again.

- __MySQL compatibility__

    Easily replace MySQL with TiDB to power your applications without changing a single line of code in most cases and still benefit from the MySQL ecosystem.

- __Distributed transaction__

    TiDB is your source of truth, guaranteeing ACID compliance, so your data is accurate and reliable anytime, anywhere.

- __Cloud Native__

    TiDB is designed to work in the cloud -- public, private, or hybrid -- making deployment, provisioning, and maintenance drop-dead simple.

- __Minimize ETL__

    ETL (Extract, Transform and Load) is no longer necessary with TiDB's hybrid OLTP/OLAP architecture, enabling you to create new values for your users, easier and faster.

- __High availability__

    With TiDB, your data and applications are always on and continuously available, so your users are never disappointed.

TiDB is designed to support both OLTP and OLAP scenarios. For complex OLAP scenarios, use [TiSpark](tispark/tispark-user-guide.md).

Read the following three articles to understand TiDB techniques:

- [Data Storage](https://pingcap.github.io/blog/2017/07/11/tidbinternal1/)
- [Computing](https://pingcap.github.io/blog/2017/07/11/tidbinternal2/)
- [Scheduling](https://pingcap.github.io/blog/2017/07/20/tidbinternal3/)

## Roadmap

Read the [Roadmap](https://github.com/pingcap/docs/blob/master/ROADMAP.md).

## Connect with us

- **Twitter**: [@PingCAP](https://twitter.com/PingCAP)
- **Reddit**: https://www.reddit.com/r/TiDB/
- **Stack Overflow**: https://stackoverflow.com/questions/tagged/tidb
- **Mailing list**: [Google Group](https://groups.google.com/forum/#!forum/tidb-user)

## TiDB architecture

To better understand TiDB’s features, you need to understand the TiDB architecture.

![image alt text](media/tidb-architecture.png)

The TiDB cluster has three components: the TiDB server, the PD server,  and the TiKV server.

### TiDB server

The TiDB server is in charge of the following operations:

1. Receiving the SQL requests

2. Processing the SQL related logics

3. Locating the TiKV address for storing and computing data through Placement Driver (PD)

4. Exchanging data with TiKV

5. Returning the result

The TiDB server is stateless. It does not store data and it is for computing only. TiDB is horizontally scalable and provides the unified interface to the outside through the load balancing components such as Linux Virtual Server (LVS), HAProxy, or F5.

### Placement Driver server

The Placement Driver (PD) server is the managing component of the entire cluster and is in charge of the following three operations:

1. Storing the metadata of the cluster such as the region location of a specific key.

2. Scheduling and load balancing regions in the TiKV cluster, including but not limited to data migration and Raft group leader transfer.

3. Allocating the transaction ID that is globally unique and monotonic increasing.

As a cluster, PD needs to be deployed to an odd number of nodes. Usually it is recommended to deploy to 3 online nodes at least.

### TiKV server

The TiKV server is responsible for storing data. From an external view, TiKV is a distributed transactional Key-Value storage engine. Region is the basic unit to store data. Each Region stores the data for a particular Key Range which is a left-closed and right-open interval from StartKey to EndKey. There are multiple Regions in each TiKV node. TiKV uses the Raft protocol for replication to ensure the data consistency and disaster recovery. The replicas of the same Region on different nodes compose a Raft Group. The load balancing of the data among different TiKV nodes are scheduled by PD. Region is also the basic unit for scheduling the load balance.

## Features

### Horizontal Scalability

Horizontal scalability is the most important feature of TiDB. The scalability includes two aspects: the computing capability and the storage capacity. The TiDB server processes the SQL requests. As the business grows, the overall processing capability and higher throughput can be achieved by simply adding more TiDB server nodes. Data is stored in TiKV. As the size of the data grows, the scalability of data can be resolved by adding more TiKV server nodes. PD schedules data in Regions among the TiKV nodes and migrates part of the data to the newly added node. So in the early stage, you can deploy only a few service instances. For example, it is recommended to deploy at least 3 TiKV nodes, 3 PD nodes and 2 TiDB nodes. As business grows, more TiDB and TiKV instances can be added on-demand.

### High availability

High availability is another important feature of TiDB. All of the three components, TiDB, TiKV and PD, can tolerate the failure of some instances without impacting the availability of the entire cluster. For each component, See the following for more details about the availability, the consequence of a single instance failure and how to recover.

#### TiDB

TiDB is stateless and it is recommended to deploy at least two instances. The front-end provides services to the outside through the load balancing components. If one of the instances is down, the Session on the instance will be impacted. From the application’s point of view, it is a single request failure but the service can be regained by reconnecting to the TiDB server. If a single instance is down, the service can be recovered by restarting the instance or by deploying a new one.

#### PD

PD is a cluster and the data consistency is ensured using the Raft protocol. If an instance is down but the instance is not a Raft Leader, there is no impact on the service at all. If the instance is a Raft Leader, a new Leader will be elected to recover the service. During the election which is approximately 3 seconds, PD cannot provide service. It is recommended to deploy three instances. If one of the instances is down, the service can be recovered by restarting the instance or by deploying a new one.

#### TiKV

TiKV is a cluster and the data consistency is ensured using the Raft protocol. The number of the replicas can be configurable and the default is 3 replicas. The load of TiKV servers are balanced through PD. If one of the node is down, all the Regions in the node will be impacted. If the failed node is the Leader of the Region, the service will be interrupted and a new election will be initiated. If the failed node is a Follower of the Region, the service will not be impacted. If a TiKV node is down for a period of time (default 30 minutes), PD will move the data to another TiKV node.
