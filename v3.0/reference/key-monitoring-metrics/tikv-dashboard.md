---
title: Key Monitoring Metrics of TiKV
summary: Learn some key metrics displayed on the Grafana TiKV dashboard.
category: reference
aliases: ['/docs/op-guide/dashboard-tikv-info/','/docs/dev/reference/key-monitoring-metrics/tikv/']
---

# Key Monitoring Metrics of TiKV

If you use Ansible to deploy the TiDB cluster, the monitoring system is deployed at the same time. For more information, see [Overview of the Monitoring Framework](/v3.0/how-to/monitor/overview.md).

The Grafana dashboard is divided into a series of sub dashboards which include Overview, PD, TiDB, TiKV, Node\_exporter, Disk Performance, and so on. A lot of metrics are there to help you diagnose.

You can get an overview of the component TiKV status from the TiKV dashboard, where the key metrics are displayed. This document provides a detailed description of these key metrics.

## Key metrics description

To understand the key metrics displayed on the Overview dashboard, check the following table:

Service | Panel name | Description | Normal range
---------------- | ---------------- | ---------------------------------- | --------------
Cluster | Store size | The storage size per TiKV instance |
Cluster | Available size | The available capacity per TiKV instance |
Cluster | Capacity size | The capacity size per TiKV instance |
Cluster | CPU | The CPU usage per TiKV instance |
Cluster | Memory | The memory usage per TiKV instance |
Cluster | IO utilization | The I/O utilization per TiKV instance |
Cluster | MBps | The total bytes of read and write in each TiKV instance |
Cluster | QPS | The QPS per command in each TiKV instance |
Cluster | Errors-gRPC | The total number of gRPC message failures |
Cluster | Leaders | The number of leaders per TiKV instance |
Cluster | Regions | The number of Regions per TiKV instance |
Errors | Server is busy | Indicates occurrences of events that make the TiKV instance unavailable temporarily, such as Write Stall, Channel Full, Scheduler Busy, and Coprocessor Full|
Errors | Server message failures | The number of failed messages between TiKV instances | It should be `0` in normal case.
Errors | Raftstore errors | The number of Raftstore errors per type on each TiKV instance |
Errors | Scheduler errors | The number of scheduler errors per type on each TiKV instance |
Errors | Coprocessor errors | The number of coprocessor errors per type on each TiKV instance |
Errors | gRPC message errors | The number of gRPC message errors per type on each TiKV instance |
Errors | Leader drop | The count of dropped leaders per TiKV instance |
Errors | Leader missing | The count of missing leaders per TiKV instance |
Server | Leaders | The number of leaders per TiKV instance |
Server | Regions | The number of Regions per TiKV instance |
Server | CF size | The size of each column family |
Server | Store size | The storage size per TiKV instance |
Server | Channel full | The number of Channel Full errors per TiKV instance | It should be `0` in normal case.
Server | Server message failures  | The number of failed messages between TiKV instances |
Server | Average Region written keys | The average rate of written keys to Regions per TiKV instance |
Server | Average Region written bytes | The average rate of writing bytes to Regions per TiKV instance |
Server | Active written leaders | The number of leaders being written on each TiKV instance |
Server | Approximate Region size | The approximate Region size |
Raft IO | Apply log duration | The time consumed for Raft to apply logs |
Raft IO | Apply log duration per server | The time consumed for Raft to apply logs per TiKV instance |
Raft IO | Append log duration | The time consumed for Raft to append logs |
Raft IO | Append log duration per server | The time consumed for Raft to append logs per TiKV instance |
Raft process | Ready handled | The count of handled ready buckets per region |
Raft process | Process ready duration per server | The time consumed for peer processes to be ready in Raft | It should be less than `2s` (P99.99).
Raft process | Process tick duration per server | The peer processes in Raft |
Raft process | 99% Duration of raftstore events | The time consumed by raftstore events (P99) |
Raft message | Sent messages per server | The number of Raft messages sent by each TiKV instance |
Raft message | Flush messages per server | The number of Raft messages flushed by each TiKV instance |
Raft message | Receive messages per server | The number of Raft messages received by each TiKV instance |
Raft message | Messages | The number of Raft messages sent per type |
Raft message | Vote | The number of Vote messages sent in Raft |
Raft message | Raft dropped messages | The number of dropped Raft messages per type|
Raft proposal | Raft proposals per ready | The number of Raft proposals of all Regions per ready handled bucket|
Raft proposal | Raft read/write proposals | The number of proposals per type|
Raft proposal | Raft read proposals per server | The number of read proposals made by each TiKV instance |
Raft proposal | Raft write proposals per server | The number of write proposals made by each TiKV instance |
Raft proposal | Proposal wait duration | The wait time of each proposal |
Raft proposal | Proposal wait duration per server | The wait time of each proposal per TiKV instance |
Raft proposal | Raft log speed | The rate at which peers propose logs |
Raft admin | Admin proposals | The number of admin proposals |
Raft admin | Admin apply | The number of processed apply commands |
Raft admin | Check split | The number of raftstore split checks |
Raft admin | 99.99% Check split duration | The time consumed when running split checks (P99.99) |
Local reader | Local reader requests | The number of total requests and the number of rejections from the local read thread |
Local reader | Local read requests duration | The wait time of local read requests |
Local reader | Local read requests batch size | The batch size of local read requests |
Storage | Storage command total | The total number of received commands per type |
Storage | Storage async request error | The total number of engine asynchronous request errors |
Storage | Storage async snapshot duration | The time consumed by processing asynchronous snapshot requests | It should be less than `1s` in `.99`.
Storage | Storage async write duration | The time consumed by processing asynchronous write requests | It should be less than `1s` in `.99`.
Scheduler | Scheduler stage total | The total number of commands at each stage | There should not be lots of errors in a short time.
Scheduler | Scheduler priority commands | The count of different priority commands |
Scheduler | Scheduler pending commands | The count of pending commands per TiKV instance |
Scheduler - XX | Scheduler stage total | The total number of commands at each stage when executing the batch_get command | There should not be lots of errors in a short time.
Scheduler - XX | Scheduler command duration | The time consumed when executing the batch_get command | It should be less than `1s`.
Scheduler - XX | Scheduler latch wait duration | The wait time caused by latch when executing the batch_get command | It should be less than `1s`.
Scheduler - XX | Scheduler keys read | The count of keys read by a batch_get command |
Scheduler - XX | Scheduler keys written | The count of keys written by a batch_get command |
Scheduler - XX | Scheduler scan details | The keys scan details of each CF when executing the batch_get command |
Scheduler - XX | Scheduler scan details [lock] | The keys scan details of lock CF when executing the batch_get command |
Scheduler - XX | Scheduler scan details [write] | The keys scan details of write CF when executing the batch_get command |
Scheduler - XX | Scheduler scan details [default] | The keys scan details of default CF when executing the batch_get command |
Coprocessor | Request duration | The time consumed to handle coprocessor read requests |
Coprocessor | Wait duration | The time consumed when coprocessor requests are waiting to be handled | It should be less than `10s` (P99.99).
Coprocessor | Processing duration | The time consumed to handle coprocessor requests |
Coprocessor | 95% Request duration by store | The time consumed to handle coprocessor read requests per TiKV instance (P95) |
Coprocessor | 95% Wait duration by store | The time consumed when coprocessor requests are waiting to be handled per TiKV instance (P95)|
Coprocessor | 95% Handling duration by store | The time consumed to handle coprocessor requests per TiKV instance (P95) |
Coprocessor | Request errors | The total number of the push down request errors | There should not be lots of errors in a short time.
Coprocessor | DAG executors | The total number of DAG executors |
Coprocessor | Scan keys | The number of keys that each request scans |
Coprocessor | Scan details | The scan details for each CF |
Coprocessor | Table Scan - Details by CF | The table scan details for each CF |
Coprocessor | Index Scan - Details by CF | The index scan details for each CF |
Coprocessor | Table Scan - Perf Statistics | The total number of RocksDB internal operations from PerfContext when executing table scan |
Coprocessor | Index Scan - Perf Statistics | The total number of RocksDB internal operations from PerfContext when executing index scan |
GC | MVCC versions | The number of versions for each key |
GC | MVCC deleted versions | The number of versions deleted by GC for each key |
GC | GC tasks | The count of GC tasks processed by gc_worker |
GC | GC tasks Duration | The time consumed when executing GC tasks |
GC | GC keys (write CF) | The count of keys in write CF affected during GC |
GC | TiDB GC actions result | The TiDB GC action result on Region level |
GC | TiDB GC worker actions | The count of TiDB GC worker actions |
GC | TiDB GC seconds | The GC duration |
GC | TiDB GC failure | The count of failed TiDB GC jobs |
GC | GC lifetime | The lifetime of TiDB GC |
GC | GC interval | The interval of TiDB GC |
Snapshot | Rate snapshot message | The rate at which Raft snapshot messages are sent |
Snapshot | 99% Handle snapshot duration | The time consumed to handle snapshots (P99) |
Snapshot | Snapshot state count | The number of snapshots per state |
Snapshot | 99.99% Snapshot size | The snapshot size (P99.99)  |
Snapshot | 99.99% Snapshot KV count | The number of KV within a snapshot (P99.99)  |
Task | Worker handled tasks | The number of tasks handled by worker |
Task | Worker pending tasks | Current number of pending and running tasks of worker | It should be less than `1000`.
Task | FuturePool handled tasks | The number of tasks handled by future_pool |
Task | FuturePool pending tasks | Current number of pending and running tasks of future_pool |
Thread CPU | Raft store CPU | The CPU utilization of the raftstore thread | The CPU usage should be less than `80%`.
Thread CPU | Async apply CPU | The CPU utilization of async apply | The CPU usage should be less than `90%`.
Thread CPU | Scheduler CPU | The CPU utilization of scheduler | The CPU usage should be less than `80%`.
Thread CPU | Scheduler Worker CPU | The CPU utilization of scheduler worker |
Thread CPU | Storage ReadPool CPU | The CPU utilization of readpool |
Thread CPU | Coprocessor CPU | The CPU utilization of coprocessor |
Thread CPU | Snapshot worker CPU | The CPU utilization of snapshot worker |
Thread CPU | Split check CPU | The CPU utilization of split check |
Thread CPU | RocksDB CPU | The CPU utilization of RocksDB |
Thread CPU | gRPC poll CPU | The CPU utilization of gRPC | The CPU usage should be less than `80%`.
RocksDB - XX | Get operations | The count of get operations |
RocksDB - XX | Get duration | The time consumed when executing get operations |
RocksDB - XX | Seek operations | The count of seek operations |
RocksDB - XX | Seek duration | The time consumed when executing seek operations |
RocksDB - XX | Write operations | The count of write operations |
RocksDB - XX | Write duration | The time consumed when executing write operations |
RocksDB - XX | WAL sync operations | The count of WAL sync operations |
RocksDB - XX | WAL sync duration | The time consumed when executing WAL sync operations |
RocksDB - XX | Compaction operations | The count of compaction and flush operations |
RocksDB - XX | Compaction duration | The time consumed when executing the compaction and flush operations |
RocksDB - XX | SST read duration | The time consumed when reading SST files |
RocksDB - XX | Write stall duration | Write stall duration | It should be `0` in normal case.
RocksDB - XX | Memtable size | The memtable size of each column family |
RocksDB - XX | Memtable hit | The hit rate of memtable |
RocksDB - XX | Block cache size | The block cache size. Broken down by column family if shared block cache is disabled. |
RocksDB - XX | Block cache hit | The hit rate of block cache |
RocksDB - XX | Block cache flow | The flow rate of block cache operations per type |
RocksDB - XX | Block cache operations | The count of block cache operations per type |
RocksDB - XX | Keys flow | The flow rate of operations on keys per type |
RocksDB - XX | Total keys | The count of keys in each column family |
RocksDB - XX | Read flow | The flow rate of read operations per type |
RocksDB - XX | Bytes / Read | The bytes per read operation|
RocksDB - XX | Write flow | The flow rate of write operations per type|
RocksDB - XX | Bytes / Write | The bytes per write operation |
RocksDB - XX | Compaction flow | The flow rate of compaction operations per type |
RocksDB - XX | Compaction pending bytes | The pending bytes to be compacted |
RocksDB - XX | Read amplification | The read amplification per TiKV instance |
RocksDB - XX | Compression ratio | The compression ratio of each level |
RocksDB - XX | Number of snapshots | The number of snapshots per TiKV instance |
RocksDB - XX | Oldest snapshots duration | The time that the oldest unreleased snapshot survivals |
RocksDB - XX | Number files at each level | The number of SST files for different column families in each level |
RocksDB - XX | Ingest SST duration seconds | The time consumed to ingest SST files |
RocksDB - XX | Stall conditions changed of each CF | Stall conditions changed of each column family |
gRPC | gRPC messages | The count of gRPC messages per type |
gRPC | gRPC message failed | The count of failed gRPC messages per type|
gRPC | 99% gRPC message duration | The gRPC message duration per message type (P99) |
gRPC | gRPC GC message count | The count of gRPC GC messages |
gRPC | 99% gRPC KV GC message duration | The execution time of gRPC GC messages (P99) |
PD | PD requests | The count of requests that TiKV sends to PD |
PD | PD request duration (average) | The time consumed by requests that TiKV sends to PD |
PD | PD heartbeats | The total number of PD heartbeat messages |
PD | PD validated peers | The total number of peers validated by the PD worker |

## TiKV dashboard interface

This section shows images of the service panels on the TiKV dashboard.

### Cluster

![TiKV Dashboard - Cluster metrics](/media/tikv-dashboard-cluster.png)

### Errors

![TiKV Dashboard - Errors metrics](/media/tikv-dashboard-errors.png)

### Server

![TiKV Dashboard - Server metrics](/media/tikv-dashboard-server.png)

### Raft IO

![TiKV Dashboard - Raft IO metrics](/media/tikv-dashboard-raftio.png)

### Raft process

![TiKV Dashboard - Raft process metrics](/media/tikv-dashboard-raft-process.png)

### Raft message

![TiKV Dashboard - Raft message metrics](/media/tikv-dashboard-raft-message.png)

### Raft proposal

![TiKV Dashboard - Raft proposal metrics](/media/tikv-dashboard-raft-propose.png)

### Raft admin

![TiKV Dashboard - Raft admin metrics](/media/tikv-dashboard-raft-admin.png)

### Local reader

![TiKV Dashboard - Local reader metrics](/media/tikv-dashboard-local-reader.png)

### Storage

![TiKV Dashboard - Storage metrics](/media/tikv-dashboard-storage.png)

### Scheduler

![TiKV Dashboard - Scheduler metrics](/media/tikv-dashboard-scheduler.png)

### Scheduler - batch_get

![TiKV Dashboard - Scheduler - batch_get metrics](/media/tikv-dashboard-scheduler-batch-get.png)

### Scheduler - cleanup

![TiKV Dashboard - Scheduler - cleanup metrics](/media/tikv-dashboard-scheduler-cleanup.png)

### Scheduler - commit

![TiKV Dashboard - Scheduler commit metrics](/media/tikv-dashboard-scheduler-commit.png)
