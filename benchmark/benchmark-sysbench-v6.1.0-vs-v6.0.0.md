---
title: TiDB Sysbench Performance Test Report -- v6.1.0 vs. v6.0.0
---

# TiDB Sysbench Performance Test Report -- v6.1.0 vs. v6.0.0

## Test overview

This test aims at comparing the Sysbench performance of TiDB v6.1.0 and TiDB v6.0.0 in the Online Transactional Processing (OLTP) scenario. The results show that performance of v6.1.0 is improved in the write workload. The performance of write-heavy workload is improved by 2.33% ~ 4.61%.

## Test environment (AWS EC2）

### Hardware configuration

| Service type | EC2 type | Instance count |
|:----------|:----------|:----------|
| PD        | m5.xlarge |     3     |
| TiKV      | i3.4xlarge|     3     |
| TiDB      | c5.4xlarge|     3     |
| Sysbench  | c5.9xlarge|     1     |

### Software version

| Service type | Software version |
|:----------|:-----------|
| PD        | v6.0.0 and v6.1.0 |
| TiDB      | v6.0.0 and v6.1.0 |
| TiKV      | v6.0.0 and v6.1.0 |
| Sysbench  | 1.1.0-df89d34   |

### Parameter configuration

TiDB v6.1.0 and TiDB v6.0.0 use the same configuration.

#### TiDB parameter configuration

{{< copyable "" >}}

```yaml
log.level: "error"
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV parameter configuration

{{< copyable "" >}}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 8
server.grpc-concurrency: 6
readpool.storage.normal-concurrency: 10
```

#### TiDB global variable configuration

{{< copyable "sql" >}}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_enable_async_commit = 1;
set global tidb_enable_1pc = 1;
set global tidb_guarantee_linearizability = 0;
set global tidb_enable_clustered_index = 1;
set global tidb_prepared_plan_cache_size=1000;
```

#### HAProxy configuration - haproxy.cfg

For more details about how to use HAProxy on TiDB, see [Best Practices for Using HAProxy in TiDB](/best-practices/haproxy-best-practices.md).

{{< copyable "" >}}

```yaml
global                                     # Global configuration.
   pidfile     /var/run/haproxy.pid        # Writes the PIDs of HAProxy processes into this file.
   maxconn     4000                        # The maximum number of concurrent connections for a single HAProxy process.
   user        haproxy                     # The same with the UID parameter.
   group       haproxy                     # The same with the GID parameter. A dedicated user group is recommended.
   nbproc      64                          # The number of processes created when going daemon. When starting multiple processes to forward requests, ensure that the value is large enough so that HAProxy does not block processes.
   daemon                                  # Makes the process fork into background. It is equivalent to the command line "-D" argument. It can be disabled by the command line "-db" argument.

defaults                                   # Default configuration.
   log global                              # Inherits the settings of the global configuration.
   retries 2                               # The maximum number of retries to connect to an upstream server. If the number of connection attempts exceeds the value, the backend server is considered unavailable.
   timeout connect  2s                     # The maximum time to wait for a connection attempt to a backend server to succeed. It should be set to a shorter time if the server is located on the same LAN as HAProxy.
   timeout client 30000s                   # The maximum inactivity time on the client side.
   timeout server 30000s                   # The maximum inactivity time on the server side.

listen tidb-cluster                        # Database load balancing.
   bind 0.0.0.0:3390                       # The Floating IP address and listening port.
   mode tcp                                # HAProxy uses layer 4, the transport layer.
   balance leastconn                      # The server with the fewest connections receives the connection. "leastconn" is recommended where long sessions are expected, such as LDAP, SQL and TSE, rather than protocols using short sessions, such as HTTP. The algorithm is dynamic, which means that server weights might be adjusted on the fly for slow starts for instance.
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## Test plan

1. Deploy TiDB v6.1.0 and v6.0.0 using TiUP.
2. Use Sysbench to import 16 tables, each table with 10 million rows of data.
3. Execute the `analyze table` statement on each table.
4. Back up the data used for restore before different concurrency tests, which ensures data consistency for each test.
5. Start the Sysbench client to perform the `point_select`, `read_write`, `update_index`, and `update_non_index` tests. Perform stress tests on TiDB via HAProxy. For each concurrency under each workload, the test takes 20 minutes.
6. After each type of test is completed, stop the cluster, overwrite the cluster with the backup data in step 4, and restart the cluster.

### Prepare test data

Run the following command to prepare the test data:

{{< copyable "shell-regular" >}}

```bash
sysbench oltp_common \
    --threads=16 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$aws_nlb_host \
    --mysql-port=$aws_nlb_port \
    --mysql-user=root \
    --mysql-password=password \
    prepare --tables=16 --table-size=10000000
```

### Perform the test

Run the following command to perform the test:

{{< copyable "shell-regular" >}}

```bash
sysbench $testname \
    --threads=$threads \
    --time=1200 \
    --report-interval=1 \
    --rand-type=uniform \
    --db-driver=mysql \
    --mysql-db=sbtest \
    --mysql-host=$aws_nlb_host \
    --mysql-port=$aws_nlb_port \
    run --tables=16 --table-size=10000000
```

## Test results

### Point Select performance

| Threads   | v6.0.0 TPS | v6.1.0 TPS  | v6.0.0 95% latency (ms) | v6.1.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|268934.84|265353.15|1.89|1.96|-1.33|
|600|365217.96|358976.94|2.57|2.66|-1.71|
|900|420799.64|407625.11|3.68|3.82|-3.13|

Compared with v6.0.0, the Point Select performance of v6.1.0 slightly drops by 2.1%.

![Point Select](/media/sysbench_v600vsv610_point_select.png)

### Update Non-index performance

| Threads   | v6.0.0 TPS | v6.1.0 TPS  | v6.0.0 95% latency (ms) | v6.1.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|41778.95|42991.9|11.24|11.45|2.90 |
|600|52045.39|54099.58|20.74|20.37|3.95|
|900|59243.35|62084.65|27.66|26.68|4.80|

Compared with v6.0.0, the Update Non-index performance of v6.1.0 is improved by 3.88%.

![Update Non-index](/media/sysbench_v600vsv610_update_non_index.png)

### Update Index performance

| Threads   | v6.0.0 TPS | v6.1.0 TPS  | v6.0.0 95% latency (ms) | v6.1.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|18085.79|19198.89|25.28|23.95|6.15|
|600|22210.8|22877.58|42.61|41.85|3.00|
|900|25249.81|26431.12|55.82|53.85|4.68|

Compared with v6.0.0, the Update Index performance of v6.1.0 is improved by 4.61%.

![Update Index](/media/sysbench_v600vsv610_update_index.png)

### Read Write performance

| Threads   | v6.0.0 TPS  | v6.1.0 TPS | v6.0.0 95% latency (ms) | v6.1.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|4856.23|4914.11|84.47|82.96|1.19|
|600|5676.46|5848.09|161.51|150.29|3.02|
|900|6072.97|6223.95|240.02|223.34|2.49|

Compared with v6.0.0, the Read Write performance of v6.1.0 is improved by 2.23%.

![Read Write](/media/sysbench_v600vsv610_read_write.png)
