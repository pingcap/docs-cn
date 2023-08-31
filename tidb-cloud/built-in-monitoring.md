---
title: TiDB Cloud Built-in Metrics
summary: Learn how to view TiDB Cloud built-in metrics and understand the meanings of these metrics.
---

# TiDB Cloud Built-in Metrics

TiDB Cloud collects and displays a full set of standard metrics of your cluster on the Metrics page. By viewing these metrics, you can easily identify performance issues and determine whether your current database deployment meets your requirements.

## View the Metrics page

To view the metrics on the Metrics page, take the following steps:

1. In the [TiDB Cloud console](https://tidbcloud.com/), navigate to the [**Clusters**](https://tidbcloud.com/console/clusters) page of your project.

    > **Tip:**
    >
    > If you have multiple projects, you can click <MDSvgIcon name="icon-left-projects" /> in the lower-left corner and switch to another project.

2. Click the name of the target cluster. The cluster overview page is displayed.
3. Click **Metrics** in the left navigation pane.

## Metrics retention policy

For TiDB Dedicated clusters and TiDB Serverless clusters, the metrics data is kept for 7 days.

## Metrics for TiDB Dedicated clusters

The following sections illustrate the metrics on the Metrics page for TiDB Dedicated clusters.

### Overview

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Database Time by SQL types | database time, {SQL type} | database time: total database time per second. <br/> {SQL type}: database time consumed by SQL statements per second, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Query Per Second | {SQL type} | The number of SQL statements executed per second in all TiDB instances, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Query Duration | avg-{SQL type}, 99-{SQL type} | The duration from receiving a request from the client to TiDB until TiDB executes the request and returns the result to the client. In general, client requests are sent in the form of SQL statements; however, this duration can include the execution time of commands such as `COM_PING`, `COM_SLEEP`, `COM_STMT_FETCH`, and `COM_SEND_LONG_DATA`. TiDB supports Multi-Query, which means the client can send multiple SQL statements at one time, such as `select 1; select 1; select 1;`. In this case, the total execution time of this query includes the execution time of all SQL statements. |
| Failed Queries | All, {Error type} @ {instance} | The statistics of error types (such as syntax errors and primary key conflicts) according to the SQL statement execution errors per minute on each TiDB instance. It contains the module in which an error occurs and the error code. |
| Command Per Second | Query, StmtExecute, and StmtPrepare | The number of commands processed by all TiDB instances per second based on command types. |
| Queries Using Plan Cache OPS | hit, miss | hit: the number of queries using plan cache per second in all TiDB instances. <br/> miss: the number of queries missing plan cache per second in all TiDB instances. |
| Transaction Per Second | {types}-{transaction model} | The number of transactions executed per second. |
| Transaction Duration | avg-{transaction model}, 99-{transaction model} | The average or the 99th percentile duration of transactions. |
| Connection Count | All, active connection | All: the number of connections to all TiDB instances. <br/> Active connections: the number of active connections to all TiDB instances. |
| Disconnection Count | {instance}-{result} | The number of clients disconnected to each TiDB instance. |

### Advanced

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Average Idle Connection Duration | avg-in-txn, avg-not-in-txn | The connection idle duration indicates the duration of a connection being idle.<br/> avg-in-txn: The average connection idle duration when a connection is within a transaction. <br/>avg-not-in-txn: The average connection idle duration when a connection is not within a transaction. |
| Get Token Duration | avg, 99 | The average or the 99th percentile duration consumed in getting tokens of SQL statements. |
| Parse Duration | avg, 99 | The average or the 99th percentile duration consumed in parsing SQL statements. |
| Compile Duration | avg, 99 | The average or the 99th percentile duration consumed in compiling the parsed SQL AST to execution plans. |
| Execute Duration | avg, 99 | The average or the 99th percentile duration consumed in executing execution plans of SQL statements. |
| Average TiDB KV Request Duration | {Request Type} | The average time consumed in executing KV requests in all TiDB instances based on request types, such as `Get`, `Prewrite`, and `Commit`. |
| Average TiKV gRPC Duration | {Request Type} | The average time consumed in executing gRPC requests in all TiKV instances based on request types, such as `kv_get`, `kv_prewrite`, and `kv_commit`. |
| Average / P99 PD TSO Wait/RPC Duration | wait-avg/99, rpc-avg/99 | Wait: the average or the 99th percentile duration in waiting for PD to return TSO in all TiDB instances. <br/> RPC: the average time or the 99th percentile of duration from sending TSO requests to PD to receiving TSO in all TiDB instances. |
| Average / P99 Storage Async Write Duration | avg, 99 | The average or the 99th percentile duration consumed in asynchronous writing. Average storage async write duration = Average store duration + Average apply duration. |
| Average / P99 Store Duration | avg, 99 | The average or the 99th percentile duration consumed in storing loop during asynchronous writing. |
| Average / P99 Apply Duration | avg, 99 | The average or the 99th percentile duration consumed in applying loop during asynchronous writing. |
| Average / P99 Append Log Duration | avg, 99 | The average or the 99th percentile duration consumed by Raft to append logs. |
| Average / P99 Commit Log Duration | avg, 99 | The average or the 99th percentile duration consumed by Raft to commit logs. |
| Average / P99 Apply Log Duration | avg, 99 | The average or the 99th percentile duration consumed by Raft to apply logs. |

### Server

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| TiDB Uptime | node | The runtime of each TiDB node since last restart. |
| TiDB CPU Usage | node | The CPU usage statistics of each TiDB node. |
| TiDB Memory Usage | node | The memory usage statistics of each TiDB node. |
| TiKV Uptime | node | The runtime of each TiKV node since last restart. |
| TiKV CPU Usage | node | The CPU usage statistics of each TiKV node. |
| TiKV Memory Usage | node | The memory usage statistics of each TiKV node. |
| TiKV IO Bps | node-write, node-read | The total input/output bytes per second of read and write in each TiKV node. |
| TiKV Storage Usage | node | The storage usage statistics of each TiKV node. |
| TiFlash Uptime | node | The runtime of each TiFlash node since last restart. |
| TiFlash CPU Usage | node | The CPU usage statistics of each TiFlash node. |
| TiFlash Memory  | node | The memory usage statistics of each TiFlash node. |
| TiFlash IO MBps | node-write, node-read | The total bytes of read and write in each TiFlash node. |
| TiFlash Storage Usage | node | The storage usage statistics of each TiFlash node. |

## Metrics for TiDB Serverless clusters

The Metrics page provides two tabs for metrics of TiDB Serverless clusters:

- Cluster Status: displays the cluster-level main metrics.
- Database Status: displays the database-level main metrics.

### Cluster Status

The following table illustrates the cluster-level main metrics under the **Cluster Status** tab.

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| Request Units | RU per second | The Request Unit (RU) is a unit of measurement used to track the resource consumption of a query or transaction. In addition to queries that you run, Request Units can be consumed by background activities, so when the QPS is 0, the Request Units per second might not be zero. |
| Used Storage Size | Row-based storage, Columnar storage | The size of the row store and the size of the column store. |
| Query Per Second | All, {SQL type} | The number of SQL statements executed per second, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Average Query Duration | All, {SQL type} | The duration from receiving a request from the client to the TiDB Serverless cluster until the cluster executes the request and returns the result to the client. |
| Failed Query | All | The number of SQL statement execution errors per second. |
| Transaction Per Second | All | The number of transactions executed per second. |
| Average Transaction Duration | All | The average execution duration of transactions. |
| Total Connection | All | The number of connections to the TiDB Serverless cluster. |

### Database Status

The following table illustrates the database-level main metrics under the **Database Status** tab.

| Metric name  | Labels | Description                                   |
| :------------| :------| :-------------------------------------------- |
| QPS Per DB | All, {Database name} | The number of SQL statements executed per second on every database, which are collected by SQL types, such as `SELECT`, `INSERT`, and `UPDATE`. |
| Average Query Duration Per DB | All, {Database name} | The duration from receiving a request from the client to a database until the database executes the request and returns the result to the client.|
| Failed Query Per DB | All, {Database name} | The statistics of error types according to the SQL statement execution errors per second on every database.|

## FAQ

**1. Why are some panes empty on this page?**

If a pane does not provide any metrics, the possible reasons are as follows:

- The workload of the corresponding cluster does not trigger this metric. For example, the failed query metric is always empty in the case of no failed queries.
- The cluster version is low. You need to upgrade it to the latest version of TiDB to see these metrics.

If all these reasons are excluded, you can contact the [PingCAP support team](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.

**2. Why might metrics be discontinuous in rare cases?**

In some rare cases, metrics might be lost, such as when the metrics system experiences high pressure.

If you encounter this problem, you can contact [PingCAP Support](/tidb-cloud/tidb-cloud-support.md) for troubleshooting.
