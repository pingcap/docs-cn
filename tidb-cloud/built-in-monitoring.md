---
title: TiDB Cloud Built-in Monitoring
summary: Learn how to view TiDB Cloud built-in monitoring metrics and understand the meanings of these metrics.
---

# TiDB Cloud Built-in Monitoring

TiDB Cloud collects and displays a full set of standard metrics of your cluster on the Monitoring page. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

> **Note:**
>
> Currently, the Monitoring page is unavailable for [Developer Tier clusters](/tidb-cloud/select-cluster-tier.md#developer-tier).

## View the Monitoring page

To view the metrics on the Monitoring page, take the following steps:

1. Navigate to the **Diagnosis** tab of a cluster.

2. Click the **Monitoring** tab.

## Monitoring metrics

The following sections illustrate the metrics on the Monitoring page.

### Database Time

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Database Time by SQL types | database time, {SQL type} | database time: total database time per second. <br/> {SQL type}: database time consumed by SQL statements per second, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Database Time by SQL Phase | database time, get token, parse, compile, execute | Database time consumed in four SQL processing phases: get token, parse, compile, and execute. The SQL execution phase is in green and other phases are in red on general. If non-green areas take a large proportion, it means most database time is consumed by other phases than the execution phase and further cause analysis is required. |
| SQL Execute Time Overview | tso_wait, Get, Cop, Commit, etc. | Green metrics stand for common KV write requests (such as prewrite and commit), blue metrics stand for common read requests, and metrics in other colors stand for unexpected situations which you need to pay attention to. For example, pessimistic lock KV requests are marked red and TSO waiting is marked dark brown. If non-blue or non-green areas take a large proportion, it means there is a bottleneck during SQL execution. For example, if serious lock conflicts occur, the red area will take a large proportion. If excessive time is consumed in waiting TSO, the dark brown area will take a large proportion. |

### Application Connection

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Connection Count | Total, active connection | Total: the number of connections to all TiDB instances. <br/> Active connections: the number of active connections to all TiDB instances. |
| Disconnection | Instances | The number of clients disconnected to each TiDB instance. |

### SQL Count

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Query Per Second | {SQL type} | The number of SQL statements executed per second in all TiDB instances, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Failed Queries | Error types | The statistics of error types (such as syntax errors and primary key conflicts) according to the SQL statement execution errors per minute on each TiDB instance. It contains the module in which an error occurs and the error code. |
| Command Per Second | Query, StmtExecute, StmtPrepare, etc. | The number of commands processed by all TiDB instances per second based on command types. |
| Queries Using Plan Cache OPS | hit, miss | hit: the number of queries using plan cache per second in all TiDB instances. <br/> miss: the number of queries missing plan cache per second in all TiDB instances. |

### Latency Break Down

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Query Duration | avg-{SQL Types}, 99-{SQL Types} | The duration from receiving a request from the client to TiDB till TiDB executing the request and returning the result to the client. In general, client requests are sent in the form of SQL statements; however, this duration can include the execution time of commands such as `COM_PING`, `COM_SLEEP`, `COM_STMT_FETCH`, and `COM_SEND_LONG_DATA`. TiDB supports Multi-Query, which means the client can send multiple SQL statements at one time, such as `select 1; select 1; select 1;`. In this case, the total execution time of this query includes the execution time of all SQL statements. |
| Average Idle Connection Duration | avg-in-txn, avg-not-in-txn | The connection idle duration indicates the duration of a connection being idle.<br/> avg-in-txn: The average connection idle duration when a connection is within a transaction. <br/>avg-not-in-txn: The average connection idle duration when a connection is not within a transaction. |
| Get Token Duration | avg, 99 | The average time or P99 duration consumed in getting tokens of SQL statements. |
| Parse Duration | avg, 99 | The average time or P99 duration consumed in parsing SQL statements. |
| Compile Duration | avg, 99 | The average time or P99 duration consumed in compiling the parsed SQL AST to execution plans. |
| Execute Duration | avg, 99 | The average time or P99 duration consumed in executing execution plans of SQL statements. |

### Transaction

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Transaction Per Second | {types}-{transaction model} | The number of transactions executed per second. |
| Transaction Duration | avg-{transaction model}, 99-{transaction model} | The execution duration of a transaction. |

### Core Path Duration

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Avg TiDB KV Request Duration | Get, Prewirite, Commit, PessimisticLock, etc. | The average time consumed in executing KV requests in all TiDB instances based on request types, including `Get`, `Prewrite`, and `Commit`. |
| Avg TiKV GRPC Duration | kv_get, kv_prewirite, kv_commit, kv_pessimisticLock, etc. | The average time consumed in executing gRPC requests in all TiKV instances based request types, including `kv_get`, `kv_prewrite`, and `kv_commit`. |
| Average / P99 PD TSO Wait/RPC Duration | wait-avg/99, rpc-avg/99 | Wait: the average time or P99 duration in waiting for PD to return TSO in all TiDB instances. <br/> RPC: the average time or P99 duration from sending TSO requests to PD to receiving TSO in all TiDB instances. |
| Average / P99 Storage Async Write Duration | avg, 99 | The average time or P99 duration consumed in asynchronous writing. Average storage async write duration = Average store duration + Average apply duration. |
| Average / P99 Store Duration | avg, 99 | The average time or P99 duration consumed in storing loop during asynchronously writing. |
| Average / P99 Apply Duration | avg, 99 | The average time or P99 duration consumed in applying loop during asynchronously writing. |
| Average / P99 Append Log Duration | avg, 99 | The average time or P99 duration consumed by Raft to append logs. |
| Average / P99 Commit Log Duration | avg, 99 | The average time or P99 duration consumed by Raft to commit logs. |
| Average / P99 Apply Log Duration | avg, 99 | The average time or P99 duration consumed by Raft to apply logs. |

### Server

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| TiDB Uptime | instances | The runtime of each TiDB instance since last restart. |
| TiDB CPU Usage | instances | The statistics of CPU usage of each TiDB instance. |
| TiDB Memory Usage | instances | The memory usage statistics of each TiDB instance. |
| TiKV Uptime | instances | The runtime of each TiKV instance since last restart. |
| TiKV CPU Usage | instances | The statistics of CPU usage of each TiKV instance. |
| TiKV Memory Usage | instances | The memory usage statistics of each TiKV instance. |
| TiKV IO MBps | instances-write, instances-read | The total bytes of read and write in each TiKV instance. |
| TiKV Storage Usage | instances | The storage size per TiKV instance. |
| TiFlash Uptime | instances | The runtime of each TiFlash instance since last restart. |
| TiFlash CPU Usage | instances | The statistics of CPU usage of each TiFlash instance. |
| TiFlash Memory  | instances | The memory usage statistics of each TiFlash instance. |
| TiFlash IO MBps | instances-write, instances-read | The total bytes of read and write in each TiFlash instance. |
| TiFlash Storage Usage | instances | The storage size per TiFlash instance. |

## FAQ

**1. Why are some panes empty on this page?**

If a pane does not provide any metrics, the possible reasons are as follows:

- The workload of the corresponding cluster does not trigger this metric. For example, the failed query metric is always empty in the case of no failed queries.
- The cluster version is low. You need to upgrade it to the latest version of TiDB to see these metrics.

If all these reasons are excluded, you can contact the [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.
