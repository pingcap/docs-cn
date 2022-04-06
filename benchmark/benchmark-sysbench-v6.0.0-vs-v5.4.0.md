---
title: TiDB Sysbench Performance Test Report -- v6.0.0 vs. v5.4.0
---

# TiDB Sysbench Performance Test Report -- v6.0.0 vs. v5.4.0

## Test overview

This test aims at comparing the Sysbench performance of TiDB v6.0.0 and TiDB v5.4.0 in the Online Transactional Processing (OLTP) scenario. The results show that performance of v6.0.0 is significantly improved by 16.17% in the read-write workload. The performance of other workload is basically the same as in v5.4.0.

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
| PD        | v5.4.0 and v6.0.0 |
| TiDB      | v5.4.0 and v6.0.0 |
| TiKV      | v5.4.0 and v6.0.0 |
| Sysbench  | 1.1.0-df89d34   |

### Parameter configuration

TiDB v6.0.0 and TiDB v5.4.0 use the same configuration.

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
raftdb.max-background-jobs: 4
raftdb.allow-concurrent-memtable-write: true
server.grpc-concurrency: 6
readpool.storage.normal-concurrency: 10
pessimistic-txn.pipelined: true
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

1. Deploy TiDB v6.0.0 and v5.4.0 using TiUP.
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

| Threads   | v5.4.0 TPS | v6.0.0 TPS  | v5.4.0 95% latency (ms) | v6.0.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|260085.19|265207.73|1.82|1.93|1.97|
|600|378098.48|365173.66|2.48|2.61|-3.42|
|900|441294.61|424031.23|3.75|3.49|-3.91|

Compared with v5.4.0, the Point Select performance of v6.0.0 is slightly dropped by 1.79%.

![Point Select](/media/sysbench_v540vsv600_point_select.png)

### Update Non-index performance

| Threads   | v5.4.0 TPS | v6.0.0 TPS  | v5.4.0 95% latency (ms) | v6.0.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|41528.7|40814.23|11.65|11.45|-1.72|
|600|53220.96|51746.21|19.29|20.74|-2.77|
|900|59977.58|59095.34|26.68|28.16|-1.47|

Compared with v5.4.0, the Update Non-index performance of v6.0.0 is slightly dropped by 1.98%.

![Update Non-index](/media/sysbench_v540vsv600_update_non_index.png)

### Update Index performance

| Threads   | v5.4.0 TPS | v6.0.0 TPS  | v5.4.0 95% latency (ms) | v6.0.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|18659.11|18187.54|23.95|25.74|-2.53|
|600|23195.83|22270.81|40.37|44.17|-3.99|
|900|25798.31|25118.78|56.84|57.87|-2.63|

Compared with v5.4.0, the Update Index performance of v6.0.0 is dropped by 3.05%.

![Update Index](/media/sysbench_v540vsv600_update_index.png)

### Read Write performance

| Threads   | v5.4.0 TPS  | v6.0.0 TPS | v5.4.0 95% latency (ms) | v6.0.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|4141.72|4829.01|97.55|82.96|16.59|
|600|4892.76|5693.12|173.58|153.02|16.36|
|900|5217.94|6029.95|257.95|235.74|15.56|

Compared with v5.4.0, the Read Write performance of v6.0.0 is significantly improved by 16.17%.

![Read Write](/media/sysbench_v540vsv600_read_write.png)
