---
title: TiDB 2.0 Release Notes
category: Releases
aliases: ['/docs/releases/2.0ga/']
---

# TiDB 2.0 Release Notes

On April 27, 2018, TiDB 2.0 GA is released! Compared with TiDB 1.0, this release has great improvement in MySQL compatibility, SQL optimizer, executor, and stability.

## TiDB

- SQL Optimizer
    - Use more compact data structure to reduce the memory usage of statistics information
    - Speed up loading statistics information when starting a tidb-server process
    - Support updating statistics information dynamically [experimental]
    - Optimize the cost model to provide more accurate query cost evaluation
    - Use `Count-Min Sketch` to estimate the cost of point queries more accurately
    - Support analyzing more complex conditions to make full use of indexes
    - Support manually specifying the `Join` order using the `STRAIGHT_JOIN` syntax
    - Use the Stream Aggregation operator when the `GROUP BY` clause is empty to improve the performance
    - Support using indexes for the `MAX/MIN` function
    - Optimize the processing algorithms for correlated subqueries to support decorrelating more types of correlated subqueries and transform them to `Left Outer Join`
    - Extend `IndexLookupJoin` to be used in matching the index prefix
- SQL Execution Engine
    - Refactor all operators using the Chunk architecture, improve the execution performance of analytical queries, and reduce memory usage. There is a significant improvement in the TPC-H benchmark result.
    - Support the Streaming Aggregation operators pushdown
    - Optimize the `Insert Into Ignore` statement to improve the performance by over 10 times
    - Optimize the `Insert On Duplicate Key Update` statement to improve the performance by over 10 times
    - Optimize `Load Data` to improve the performance by over 10 times
    - Push down more data types and functions to TiKV
    - Support computing the memory usage of physical operators, and specifying the processing behavior in the configuration file and system variables when the memory usage exceeds the threshold
    - Support limiting the memory usage by a single SQL statement to reduce the risk of OOM
    - Support using implicit RowID in CRUD operations
    - Improve the performance of point queries
- Server
    - Support the Proxy Protocol
    - Add more monitoring metrics and refine the log
    - Support validating the configuration files
    - Support obtaining the information of TiDB parameters through HTTP API
    - Resolve Lock in the Batch mode to speed up garbage collection
    - Support multi-threaded garbage collection
    - Support TLS
- Compatibility
    - Support more MySQL syntaxes
    - Support modifying the `lower_case_table_names` system variable in the configuration file to support the OGG data replication tool
    - Improve compatibility with the Navicat management tool
    - Support displaying the table creating time in `Information_Schema`
    - Fix the issue that the return types of some functions/expressions differ from MySQL
    - Improve compatibility with JDBC
    - Support more SQL Modes
- DDL
    - Optimize the `Add Index` operation to greatly improve the execution speed in some scenarios
    - Attach a lower priority to the `Add Index` operation to reduce the impact on online business
    - Output more detailed status information of the DDL jobs in `Admin Show DDL Jobs`
    - Support querying the original statements of currently running DDL jobs using `Admin Show DDL Job Queries JobID`
    - Support recovering the index data using `Admin Recover Index` for disaster recovery
    - Support modifying Table Options using the `Alter` statement

## PD

- Support `Region Merge`, to merge empty Regions after deleting data [experimental]
- Support `Raft Learner` [experimental]
- Optimize the scheduler
    - Make the scheduler to adapt to different Region sizes
    - Improve the priority and speed of restoring data during TiKV outage
    - Speed up data transferring when removing a TiKV node
    - Optimize the scheduling policies to prevent the disks from becoming full when the space of TiKV nodes is insufficient
    - Improve the scheduling efficiency of the balance-leader scheduler
    - Reduce the scheduling overhead of the balance-region scheduler
    - Optimize the execution efficiency of the the hot-region scheduler
- Operations interface and configuration
    - Support TLS
    - Support prioritizing the PD leaders
    - Support configuring the scheduling policies based on labels
    - Support configuring stores with a specific label not to schedule the Raft leader
    - Support splitting Region manually to handle the hotspot in a single Region
    - Support scattering a specified Region to manually adjust Region distribution in some cases
    - Add check rules for configuration parameters and improve validity check of the configuration items
- Debugging interface
    - Add the `Drop Region` debugging interface
    - Add the interfaces to enumerate the health status of each PD
- Statistics
    - Add statistics about abnormal Regions
    - Add statistics about Region isolation level
    - Add scheduling related metrics
- Performance
    - Keep the PD leader and the etcd leader together in the same node to improve write performance
    - Optimize the performance of Region heartbeat

## TiKV

- Features
    - Protect critical configuration from incorrect modification
    - Support `Region Merge` [experimental]
    - Add the `Raw DeleteRange` API
    - Add the `GetMetric` API
    - Add `Raw Batch Put`, `Raw Batch Get`, `Raw Batch Delete` and `Raw Batch Scan`
    - Add Column Family options for the RawKV API and support executing operation on a specific Column Family
    - Support Streaming and Streaming Aggregation in Coprocessor
    - Support configuring the request timeout of Coprocessor
    - Carry timestamps with Region heartbeats
    - Support modifying some RocksDB parameters online, such as `block-cache-size`
    - Support configuring the behavior of Coprocessor when it encounters some warnings or errors
    - Support starting in the importing data mode to reduce write amplification during the data importing process
    - Support manually splitting Region in halves
    - Improve the data recovery tool `tikv-ctl`
    - Return more statistics in Coprocessor to guide the behavior of TiDB
    - Support the `ImportSST` API to import SST files [experimental]
    - Add the TiKV Importer binary to integrate with TiDB Lightning to import data quickly [experimental]
- Performance
    - Optimize read performance using `ReadPool` and increase the `raw_get/get/batch_get` by 30%
    - Improve metrics performance
    - Inform PD immediately once the Raft snapshot process is completed to speed up balancing
    - Solve performance jitter caused by RocksDB flushing
    - Optimize the space reclaiming mechanism after deleting data
    - Speed up garbage cleaning while starting the server
    - Reduce the I/O overhead during replica migration using `DeleteFilesInRanges`
- Stability
    - Fix the issue that gRPC call does not get returned when the PD leader switches
    - Fix the issue that it is slow to offline nodes caused by snapshots
    - Limit the temporary space usage consumed by migrating replicas
    - Report the Regions that cannot elect a leader for a long time
    - Update the Region size information in time according to compaction events
    - Limit the size of scan lock to avoid request timeout
    - Limit the memory usage when receiving snapshots to avoid OOM
    - Increase the speed of CI test
    - Fix the OOM issue caused by too many snapshots
    - Configure `keepalive` of gRPC
    - Fix the OOM issue caused by an increase of the Region number

## TiSpark

TiSpark uses a separate version number. The current TiSpark version is 1.0 GA. The components of TiSpark 1.0 provide distributed computing of TiDB data using Apache Spark.

- Provide a gRPC communication framework to read data from TiKV
- Provide encoding and decoding of TiKV component data and communication protocol
- Provide calculation pushdown, which includes:
    - Aggregate pushdown
    - Predicate pushdown
    - TopN pushdown
    - Limit pushdown
- Provide index related support
    - Transform predicate into Region key range or secondary index
    - Optimize `Index Only` queries
    - Adaptively downgrade index scan to table scan per Region
- Provide cost-based optimization
    - Support statistics
    - Select index
    - Estimate broadcast table cost
- Provide support for multiple Spark interfaces
    - Support Spark Shell
    - Support ThriftServer/JDBC
    - Support Spark-SQL interaction
    - Support PySpark Shell
    - Support SparkR
