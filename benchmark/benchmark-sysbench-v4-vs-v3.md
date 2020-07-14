---
title: TiDB Sysbench Performance Test Report -- v4.0 vs. v3.0
summary: Compare the Sysbench performance of TiDB 4.0 and TiDB 3.0.
aliases: ['/docs/dev/benchmark/benchmark-sysbench-v4-vs-v3/']
---

# TiDB Sysbench Performance Test Report -- v4.0 vs. v3.0

## Test purpose

This test aims to compare the Sysbench performance of TiDB 4.0 and TiDB 3.0 in the Online Transactional Processing (OLTP) scenario.

## Test environment (AWS EC2）

### Hardware configuration

| Service type         | EC2 type     | Instance count |
|:----------|:----------|:----------|
| PD        | m5.xlarge |     3     |
| TiKV      | i3.4xlarge|     3     |
| TiDB      | c5.4xlarge|     3     |
| Sysbench  | m5.4xlarge|     1     |

### Software version

| Service type   | Software version    |
|:----------|:-----------|
| PD        | 3.0 and 4.0   |
| TiDB      | 3.0 and 4.0   |
| TiKV      | 3.0 and 4.0   |
| Sysbench  | 1.0.20     |

### Parameter configuration

#### TiDB v3.0 configuration

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV v3.0 configuration

{{< copyable "" >}}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 3
raftdb.max-background-jobs: 3
raftdb.allow-concurrent-memtable-write: true
server.grpc-concurrency: 6
readpool.storage.normal-concurrency: 10
readpool.coprocessor.normal-concurrency: 5
```

#### TiDB v4.0 configuration

{{< copyable "" >}}

```yaml
log.level: "error"
performance.max-procs: 20
prepared-plan-cache.enabled: true
tikv-client.max-batch-wait-time: 2000000
```

#### TiKV v4.0 configuration

{{< copyable "" >}}

```yaml
storage.scheduler-worker-pool-size: 5
raftstore.store-pool-size: 3
raftstore.apply-pool-size: 3
rocksdb.max-background-jobs: 3
raftdb.max-background-jobs: 3
raftdb.allow-concurrent-memtable-write: true
server.request-batch-enable-cross-command: false
server.grpc-concurrency: 6
readpool.unifiy-read-pool: true
readpool.unified.min-thread-count: 5
readpool.unified.max-thread-count: 20
readpool.storage.normal-concurrency: 10
pessimistic-txn.pipelined: true
```

#### Global variable configuration

{{< copyable "sql" >}}

```sql
set global tidb_hashagg_final_concurrency=1;
set global tidb_hashagg_partial_concurrency=1;
set global tidb_disable_txn_auto_retry=0;
```

## Test plan

1. Deploy TiDB v4.0 and v3.0 using TiUP.
2. Use Sysbench to import 16 tables, each table with 10 million rows of data.
3. Execute the `analyze table` statement on each table.
4. Back up the data used for restore before different concurrency tests, which ensures data consistency for each test.
5. Start the Sysbench client to perform the `point_select`, `read_write`, `update_index`, and `update_non_index` tests. Perform stress tests on TiDB via AWS NLB. In each type of test, the warm-up takes 1 minute and the test takes 5 minutes.
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

Execute the following command to perform the test.

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

Compared with v3.0, the Point Select performance of TiDB v4.0 has increased by 14%.

![Point Select](/media/sysbench-v4vsv3-point-select.png)

### Update Non-index performance

Compared with v3.0, the Update Non-index performance of TiDB v4.0 has increased by 15%.

![Update Non-index](/media/sysbench-v4vsv3-update-non-index.png)

### Update Index performance

Compared with v3.0, the Update Index performance of TiDB v4.0 has increased by 17%.

![Update Index](/media/sysbench-v4vsv3-update-index.png)

### Read-write performance

Compared with v3.0, the read-write performance of TiDB v4.0 has increased by 31%.

![Read Write](/media/sysbench-v4vsv3-read-write.png)
