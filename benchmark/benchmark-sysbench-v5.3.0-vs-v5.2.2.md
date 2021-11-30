---
title: TiDB Sysbench Performance Test Report -- v5.3.0 vs. v5.2.2
---

# TiDB Sysbench Performance Test Report -- v5.3.0 vs. v5.2.2

## Test overview

This test aims at comparing the Sysbench performance of TiDB v5.3.0 and TiDB v5.2.2 in the Online Transactional Processing (OLTP) scenario. The results show that the performance of v5.3.0 is nearly the same as that of v5.2.2.

## Test environment (AWS EC2）

### Hardware configuration

| Service type         | EC2 type     | Instance count |
|:----------|:----------|:----------|
| PD        | m5.xlarge |     3     |
| TiKV      | i3.4xlarge|     3     |
| TiDB      | c5.4xlarge|     3     |
| Sysbench  | c5.9xlarge|     1     |

### Software version

| Service type   | Software version    |
|:----------|:-----------|
| PD        | v5.2.2 and v5.3.0   |
| TiDB      | v5.2.2 and v5.3.0   |
| TiKV      | v5.2.2 and v5.3.0   |
| Sysbench  | 1.1.0-ead2689   |

### Parameter configuration

TiDB v5.3.0 and TiDB v5.2.2 use the same configuration.

#### TiDB parameter configuration

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
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
readpool.unified.min-thread-count: 5
readpool.unified.max-thread-count: 20
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

```yaml
global                                     # Global configuration.
   chroot      /var/lib/haproxy            # Changes the current directory and sets superuser privileges for the startup process to improve security.
   pidfile     /var/run/haproxy.pid        # Writes the PIDs of HAProxy processes into this file.
   maxconn     4000                        # The maximum number of concurrent connections for a single HAProxy process.
   user        haproxy                     # Same with the UID parameter.
   group       haproxy                     # Same with the GID parameter. A dedicated user group is recommended.
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
   balance roundrobin                      # The server with the fewest connections receives the connection. "leastconn" is recommended where long sessions are expected, such as LDAP, SQL and TSE, rather than protocols using short sessions, such as HTTP. The algorithm is dynamic, which means that server weights might be adjusted on the fly for slow starts for instance.
   server tidb-1 10.9.18.229:4000 check inter 2000 rise 2 fall 3       # Detects port 4000 at a frequency of once every 2000 milliseconds. If it is detected as successful twice, the server is considered available; if it is detected as failed three times, the server is considered unavailable.
   server tidb-2 10.9.39.208:4000 check inter 2000 rise 2 fall 3
   server tidb-3 10.9.64.166:4000 check inter 2000 rise 2 fall 3
```

## Test plan

1. Deploy TiDB v5.3.0 and v5.2.2 using TiUP.
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

| Threads   | v5.2.2 TPS | v5.3.0 TPS | v5.2.2 95% latency (ms) | v5.3.0 95% latency (ms) | TPS improvement (%) |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|267673.17|267516.77|1.76|1.67|-0.06|
|600|369820.29|361672.56|2.91|2.97|-2.20|
|900|417143.31|416479.47|4.1|4.18|-0.16|

Compared with v5.2.2, the Point Select performance of v5.3.0 is reduced slightly by 0.81%.

![Point Select](/media/sysbench_v522vsv530_point_select.png)

### Update Non-index performance

| Threads   | v5.2.2 TPS | v5.3.0 TPS  | v5.2.2 95% latency (ms) | v5.3.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|39715.31|40041.03|11.87|12.08|0.82|
|600|50239.42|51110.04|20.74|20.37|1.73|
|900|57073.97|57252.74|28.16|27.66|0.31|

Compared with v5.2.2, the Update Non-index performance of v5.3.0 is improved slightly by 0.95%.

![Update Non-index](/media/sysbench_v522vsv530_update_non_index.png)

### Update Index performance

| Threads   | v5.2.2 TPS | v5.3.0 TPS  | v5.2.2 95% latency (ms) | v5.3.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|17634.03|17821.1|25.74|25.74|1.06|
|600|20998.59|21534.13|46.63|45.79|2.55|
|900|23420.75|23859.64|64.47|62.19|1.87|

Compared with v5.2.2, the Update Index performance of v5.3.0 is improved slightly by 1.83%.

![Update Index](/media/sysbench_v522vsv530_update_index.png)

### Read Write performance

| Threads   | v5.2.2 TPS  | v5.3.0 TPS | v5.2.2 95% latency (ms) | v5.3.0 95% latency (ms)   | TPS improvement (%)  |
|:----------|:----------|:----------|:----------|:----------|:----------|
|300|3872.01|3848.63|106.75|106.75|-0.60|
|600|4514.17|4471.77|200.47|196.89|-0.94|
|900|4877.05|4861.45|287.38|282.25|-0.32|

Compared with v5.2.2, the Read Write performance of v5.3.0 is reduced slightly by 0.62%.

![Read Write](/media/sysbench_v522vsv530_read_write.png)