---
title: TiDB Sysbench Performance Test Report -- v5.1.0 vs. v5.0.2
---

# TiDB Sysbench Performance Test Report -- v5.1.0 vs. v5.0.2

## Test overview

This test aims at comparing the Sysbench performance of TiDB v5.1.0 and TiDB v5.0.2 in the Online Transactional Processing (OLTP) scenario. The results show that compared with v5.0.2, the Point Select performance of v5.1.0 is improved by 19.4%, and the performance of the Read Write and Update Index is slightly reduced.

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
| PD        | v5.0.2 and v5.1.0   |
| TiDB      | v5.0.2 and v5.1.0   |
| TiKV      | v5.0.2 and v5.1.0   |
| Sysbench  | 1.0.20     |

### Parameter configuration

TiDB v5.1.0 and TiDB v5.0.2 use the same configuration.

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
server.enable-request-batch: false
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

## Test plan

1. Deploy TiDB v5.1.0 and v5.0.2 using TiUP.
2. Use Sysbench to import 16 tables, each table with 10 million rows of data.
3. Execute the `analyze table` statement on each table.
4. Back up the data used for restore before different concurrency tests, which ensures data consistency for each test.
5. Start the Sysbench client to perform the `point_select`, `read_write`, `update_index`, and `update_non_index` tests. Perform stress tests on TiDB via HAProxy. The test takes 5 minutes.
6. After each type of test is completed, stop the cluster, overwrite the cluster with the backup data in step 4, and restart the cluster.

### Prepare test data

Execute the following command to prepare the test data:

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

Execute the following command to perform the test:

{{< copyable "shell-regular" >}}

```bash
sysbench $testname \
    --threads=$threads \
    --time=300 \
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

| Threads   | v5.0.2 QPS   | v5.0.2 95% latency (ms)   | v5.1.0 QPS   | v5.1.0 95% latency (ms)   | QPS improvement   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|137732.27|1.86|158861.67|2|15.34%|
|300|201420.58|2.91|238038.44|2.71|18.18%|
|600|303631.52|3.49|428573.21|2.07|41.15%|
|900|383628.13|3.55|464863.22|3.89|21.18%|
|1200|391451.54|5.28|413656.74|13.46|5.67%|
|1500|410276.93|7.43|471418.78|10.65|14.90%|

Compared with v5.0.2, the Point Select performance of v5.1.0 is improved by 19.4%.

![Point Select](/media/sysbench_v510vsv502_point_select.png)

### Update Non-index performance

| Threads   | v5.0.2 QPS   | v5.0.2 95% latency (ms)   | v5.1.0 QPS   | v5.1.0 95% latency (ms)   | QPS improvement   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|29248.2|7.17|29362.7|8.13|0.39%|
|300|40316.09|12.52|39651.52|13.7|-1.65%|
|600|51011.11|22.28|47047.9|27.66|-7.77%|
|900|58814.16|27.66|59331.84|28.67|0.88%|
|1200|65286.52|32.53|67745.39|31.37|3.77%|
|1500|68300.86|39.65|67899.17|44.17|-0.59%|

Compared with v5.0.2, the Update Non-index performance of v5.1.0 is reduced by 0.8%.

![Update Non-index](/media/sysbench_v510vsv502_update_non_index.png)

### Update Index performance

| Threads   | v5.0.2 QPS   | v5.0.2 95% latency (ms)   | v5.1.0 QPS   | v5.1.0 95% latency (ms)   | QPS improvement   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|15066.54|14.73|14829.31|14.73|-1.57%|
|300|18535.92|24.83|17401.01|29.72|-6.12%|
|600|22862.73|41.1|21923.78|44.98|-4.11%|
|900|25286.74|57.87|24916.76|58.92|-1.46%|
|1200|27566.18|70.55|27800.62|69.29|0.85%|
|1500|28184.76|92.42|28679.72|86|1.76%|

Compared with v5.0.2, the Update Index performance of v5.1.0 is reduced by 1.8%.

![Update Index](/media/sysbench_v510vsv502_update_index.png)

### Read Write performance

| Threads   | v5.0.2 QPS   | v5.0.2 95% latency (ms)   | v5.1.0 QPS   | v5.1.0 95% latency (ms)   | QPS improvement   |
|:----------|:----------|:----------|:----------|:----------|:----------|
|150|66415.33|56.84|66591.49|57.87|0.27%|
|300|82488.39|97.55|81226.41|101.13|-1.53%|
|600|99195.36|173.58|97357.86|179.94|-1.85%|
|900|107382.76|253.35|101665.95|267.41|-5.32%|
|1200|112389.23|337.94|107426.41|350.33|-4.42%|
|1500|113548.73|450.77|109805.26|442.73|-3.30%|

Compared with v5.0.2, the Read Write performance of v5.1.0 is reduced by 2.7%.

![Read Write](/media/sysbench_v510vsv502_read_write.png)
