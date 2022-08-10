---
title: TiDB Dashboard Monitoring Page
summary: Learn how to view the Performance Overview dashboard on TiDB Dashboard and understand key metrics displayed on the Performance Overview dashboard.
---

# TiDB Dashboard Monitoring Page

On the monitoring page, you can view the Performance Overview dashboard, a performance analysis and tuning tool introduced in TiDB v6.1.0. With the Performance Overview dashboard, you can analyze performance efficiently, and confirm whether the bottleneck of user response time is in the database. If the bottleneck is in the database, you can identify the bottleneck inside the database, with database time overview, workload profile and SQL latency breakdown. For details, see [Performance Analysis and Tuning](/performance-tuning-methods.md).

## Access the page

Log in to TiDB dashboard and click **Monitoring** from the left navigation bar. The Performance Overview dashboard is displayed.

![Monitoring page](/media/dashboard/dashboard-monitoring.png)

If the TiDB cluster is deployed using TiUP, you can also view the Performance Overview dashboard on Grafana. In this deployment mode, the monitoring system (Prometheus & Grafana) is deployed at the same time. For more information, see [TiDB Monitoring Framework Overview](/tidb-monitoring-framework.md).

![performance overview](/media/performance/grafana_performance_overview.png)

## Key Metrics on Performance Overview

The Performance Overview dashboard orchestrates the metrics of TiDB, PD, and TiKV, and presents each of them in the following sections:

- Overview: Database time and SQL execution time summary. By checking different colors in the overview, you can quickly identify the database workload profile and the performance bottleneck.

- Load profile: Key metrics and resource usage, including database QPS, connection information, the MySQL command types the application interacts with TiDB, database internal TSO and KV request OPS, and resource usage of the TiKV and TiDB.

- Top-down latency breakdown: Query latency versus connection idle time ratio, query latency breakdown, TSO/KV request latency during execution, breakdown of write latency within TiKV.

The following sections illustrate the metrics on the Performance Overview dashboard.

### Database Time by SQL Type

- database time: Total database time per second
- sql_type: Database time consumed by each type of SQL statements per second

### Database Time by SQL Phase

- database time: Total database time per second
- get token/parse/compile/execute: Database time consumed in four SQL processing phases

The SQL execution phase is in green and other phases are in red on general. If non-green areas are large, it means much database time is consumed in other phases than the execution phase and further cause analysis is required.

### SQL Execute Time Overview

- execute time: Database time consumed during SQL execution per second
- tso_wait: Concurrent TSO waiting time per second during SQL execution
- kv request type: Time waiting for each KV request type per second during SQL execution. The total KV request wait time might exceed SQL execution time, because KV requests are concurrent.

Green metrics stand for common KV write requests (such as prewrite and commit), blue metrics stand for common read requests, and metrics in other colors stand for unexpected situations which you need to pay attention to. For example, pessimistic lock KV requests are marked red and TSO waiting is marked dark brown.

If non-blue or non-green areas are large, it means there is a bottleneck during SQL execution. For example:

- If serious lock conflicts occur, the red area will take a large proportion.
- If excessive time is consumed in waiting TSO, the dark brown area will take a large proportion.

### QPS

Number of SQL statements executed per second in all TiDB instances, collected by type: such as `SELECT`, `INSERT`, and `UPDATE`

### CPS By Type

Number of commands processed by all TiDB instances per second based on type

### Queries Using Plan Cache OPS

Number of queries using plan cache per second in all TiDB instances

### KV/TSO Request OPS

- kv request total: Total number of KV requests per second in all TiDB instances
- kv request by type: Number of KV requests per second in all TiDB instances based on such types as `Get`, `Prewrite`, and `Commit`.
- tso - cmd: Number of `tso cmd` requests per second in all TiDB instances
- tso - request: Number of `tso request` requests per second in all TiDB instances

Generally, dividing `tso - cmd` by `tso - request` yields the average batch size of requests per second.

### Connection Count

- total: Number of connections to all TiDB instances
- active connections: Number of active connections to all TiDB instances
- Number of connections to each TiDB instance

### TiDB CPU

- avg: Average CPU utilization across all TiDB instances
- delta: Maximum CPU utilization of all TiDB instances minus minimum CPU utilization of all TiDB instances
- max: Maximum CPU utilization across all TiDB instances

### TiKV CPU/IO MBps

- CPU-Avg: Average CPU utilization of all TiKV instances
- CPU-Delta: Maximum CPU utilization of all TiKV instances minus minimum CPU utilization of all TiKV instances
- CPU-MAX: Maximum CPU utilization among all TiKV instances
- IO-Avg: Average MBps of all TiKV instances
- IO-Delt: Maximum MBps of all TiKV instances minus minimum MBps of all TiKV instances
- IO-MAX: Maximum MBps of all TiKV instances

### Duration

- Duration: Execution time

    - The duration from receiving a request from the client to TiDB till TiDB executing the request and returning the result to the client. In general, client requests are sent in the form of SQL statements; however, this duration can include the execution time of commands such as `COM_PING`, `COM_SLEEP`, `COM_STMT_FETCH`, and `COM_SEND_LONG_DATA`.
    - TiDB supports Multi-Query, which means the client can send multiple SQL statements at one time, such as `select 1; select 1; select 1;`. In this case, the total execution time of this query includes the execution time of all SQL statements.

- avg: Average time to execute all requests
- 99: P99 duration to execute all requests
- avg by type: Average time to execute all requests in all TiDB instances, collected by type: `SELECT`, `INSERT`, and `UPDATE`

### Connection Idle Duration

Connection Idle Duration indicates the duration of a connection being idle.

- avg-in-txn: Average connection idle duration when the connection is within a transaction
- avg-not-in-txn: Average connection idle duration when the connection is not within a transaction
- 99-in-txn: P99 connection idle duration when the connection is within a transaction
- 99-not-in-txn: P99 connection idle duration when the connection is not within a transaction

### Parse Duration, Compile Duration, and Execute Duration

- Parse Duration: Time consumed in parsing SQL statements
- Compile Duration: Time consumed in compiling the parsed SQL AST to execution plans
- Execution Duration: Time consumed in executing execution plans of SQL statements

All these three metrics include the average duration and the 99th percentile duration in all TiDB instances.

### Avg TiDB KV Request Duration

Average time consumed in executing KV requests in all TiDB instances based on the type, including `Get`, `Prewrite`, and `Commit`.

### Avg TiKV GRPC Duration

Average time consumed in executing gRPC requests in all TiKV instances based on the type, including `kv_get`, `kv_prewrite`, and `kv_commit`.

### PD TSO Wait/RPC Duration

- wait - avg: Average time in waiting for PD to return TSO in all TiDB instances
- rpc - avg: Average time from sending TSO requests to PD to receiving TSO in all TiDB instances
- wait - 99: P99 time in waiting for PD to return TSO in all TiDB instances
- rpc - 99: P99 time from sending TSO requests to PD to receiving TSO in all TiDB instances

### Storage Async Write Duration, Store Duration, and Apply Duration

- Storage Async Write Duration: Time consumed in asynchronous write
- Store Duration: Time consumed in store loop during asynchronously write
- Apply Duration: Time consumed in apply loop during asynchronously write

All these three metrics include the average duration and P99 duration in all TiKV instances.

Average storage async write duration = Average store duration + Average apply duration

### Append Log Duration, Commit Log Duration, and Apply Log Duration

- Append Log Duration: Time consumed by Raft to append logs
- Commit Log Duration: Time consumed by Raft to commit logs
- Apply Log Duration: Time consumed by Raft to apply logs

All these three metrics include the average duration and P99 duration in all TiKV instances.
