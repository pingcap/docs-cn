---
title: 延迟的拆解分析
summary: 详细介绍 TiDB 运行各阶段中时间消耗带来的延迟，以及如何在真实场景中分析延迟。
---

# 延迟的拆解分析

本文将 TiDB 中 SQL 语句的延迟拆解成各项监控指标，并从用户角度对指标进行分析，包括：

- [通用 SQL 层](#通用-sql-层)
- [读请求](#读请求)
- [写请求](#写请求)
- [批量请求](#批量请求)
- [TiKV 快照](#tikv-快照)
- [异步写入](#异步写入)

这些分析可以让你深入了解 TiDB 在执行 SQL 查询时的耗时情况，有助于诊断 TiDB 关键运行路径的问题。除了延迟的指标拆解之外，[诊断场景](#诊断场景)小节介绍了如何在真实场景中分析延迟。

建议在阅读本文前，先阅读 [TiDB 性能分析和优化方法](/performance-tuning-methods.md)。需要注意的是，在将延迟拆解成监控指标时，延迟的耗时数值采用的是均值，而非某几个特定慢查询对应的数值。许多指标都会以直方图的形式展示，以更好地展现耗时或者延迟的分布情况。你需要按如下公式使用总和 (sum) 及数量 (count) 来计算均值 (avg)。

```
avg = ${metric_name}_sum / ${metric_name}_count
```

本文介绍的监控指标可以从 TiDB 的 Prometheus 管理界面中查询到。

## 通用 SQL 层

通用 SQL 层带来的延迟存在于 TiDB 的最顶部，所有 SQL 查询都具有这一部分的延迟。下面是通用 SQL 层操作的时间消耗图：

```railroad+diagram
Diagram(
    NonTerminal("Token wait duration"),
    Choice(
        0,
        Comment("Prepared statement"),
        NonTerminal("Parse duration"),
    ),
    OneOrMore(
        Sequence(
        Choice(
            0,
            NonTerminal("Optimize prepared plan duration"),
            Sequence(
            Comment("Plan cache miss"),
            NonTerminal("Compile duration"),
            ),
        ),
        NonTerminal("TSO wait duration"),
        NonTerminal("Execution duration"),
        ),
        Comment("Retry"),
    ),
)
```

通用 SQL 层的延迟可以使用 `e2e duration` 指标观察。它的计算方法是：

```text
e2e duration =
    tidb_server_get_token_duration_seconds +
    tidb_session_parse_duration_seconds +
    tidb_session_compile_duration_seconds +
    tidb_session_execute_duration_seconds{type="general"}
```

- `tidb_server_get_token_duration_seconds` 代表令牌 (Token) 等待耗时，它通常小于 1 微秒，因而足以被忽略。
- `tidb_session_parse_duration_seconds` 代表把 SQL 查询解析成抽象语法树 (AST, Abstract Syntax Tree) 的耗时。要跳过这部分的耗时，可以使用 [`PREPARE/EXECUTE` 语句](/develop/dev-guide-optimize-sql-best-practices.md#use-prepare)。
- `tidb_session_compile_duration_seconds` 记录了把 AST 编译成执行计划的耗时。要跳过这部分的耗时，可以使用[执行计划缓存](/sql-prepared-plan-cache.md)。
- `tidb_session_execute_duration_seconds{type="general"}` 记录了执行各种不同用户查询的耗时。这部分的耗时需要进行细粒度的拆解，以用来分析性能问题或瓶颈。

通常来说，OLTP (Online Transactional Processing) 工作负载可以分为读请求和写请求两类。下面的小节会分别对[读请求](#读请求)和[写请求](#写请求)进行介绍。这两类请求共享了一些关键代码，但执行方式是不一样的。

## 读请求

读请求只有一种处理形式。

### 点查

下面是点查操作的时间消耗图：

```railroad+diagram
Diagram(
    Choice(
        0,
        NonTerminal("Resolve TSO"),
        Comment("Read by clustered PK in auto-commit-txn mode or snapshot read"),
    ),
    Choice(
        0,
        NonTerminal("Read handle by index key"),
        Comment("Read by clustered PK, encode handle by key"),
    ),
    NonTerminal("Read value by handle"),
)
```

在点查过程中，`tidb_session_execute_duration_seconds{type="general"}` 使用如下方式计算：

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    read handle duration +
    read value duration
```

`pd_client_cmd_handle_cmds_duration_seconds{type="wait"}` 代表从 PD 中读取 [TSO (Timestamp Oracle)](/glossary.md#tso) 的耗时。在 auto-commit 事务模式下从聚簇索引主键中读取，或者从快照中读取时，该数值为 0。

`read handle duration` 和 `read value duration` 使用如下方式计算：

```text
read handle duration = read value duration =
    tidb_tikvclient_txn_cmd_duration_seconds{type="get"} =
    send request duration =
    tidb_tikvclient_request_seconds{type="Get"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_get"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

`tidb_tikvclient_request_seconds{type="Get"}` 代表通过 gRPC 发往 TiKV 的批量 get 请求耗时。要了解更多关于 `tidb_tikvclient_batch_wait_duration`、`tidb_tikvclient_batch_send_latency` 和 `tidb_tikvclient_rpc_net_latency_seconds{store="?"}` 等批量请求客户端耗时的细节，请参考[批量请求](#批量请求)小节。

`tikv_grpc_msg_duration_seconds{type="kv_get"}` 使用如下方式计算：

```text
tikv_grpc_msg_duration_seconds{type="kv_get"} =
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    tikv_engine_seek_micro_seconds{type="seek_average"} +
    read value duration +
    read value duration(non-short value)
```

此时，请求已经到达 TiKV。TiKV 在处理 get 请求时，会进行一次 seek 和一到两次 read 操作。其中，短数据的键和值被编码在一个写列族 (column family) 中，因而只需要进行一次 read 操作。TiKV 在处理读请求前会先获取一个快照。要了解更多关于 TiKV 快照的细节，请参考 [TiKV 快照](#tikv-快照)小节。

`read value duration(from disk)` 使用如下方式计算：

```text
read value duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="get/batch_get_command"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="get/batch_get_command"}))
```

TiKV 采用 RocksDB 作为存储引擎。如果块缓存中找不到要求的值，TiKV 需要从磁盘中读取。对于 `tikv_storage_rocksdb_perf`，获取请求可以是 `get` 或者 `batch_get_command`。

### 批量点查

下面是批量点查操作的时间消耗图：

```railroad+diagram
Diagram(
  NonTerminal("Resolve TSO"),
  Choice(
    0,
    NonTerminal("Read all handles by index keys"),
    Comment("Read by clustered PK, encode handle by keys"),
  ),
  NonTerminal("Read values by handles"),
)
```

在进行批量点查时，`tidb_session_execute_duration_seconds{type="general"}` 使用如下方式计算：

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    read handles duration +
    read values duration
```

批量点查的过程几乎与[点查](#点查)一致。不同的是，批量点查会同时得到多个值。

`read handles duration` 和 `read values duration` 使用如下方式计算：

```text
read handles duration = read values duration =
    tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"} =
    send request duration =
    tidb_tikvclient_request_seconds{type="BatchGet"} =
    tidb_tikvclient_batch_wait_duration(transaction) +
    tidb_tikvclient_batch_send_latency(transaction) +
    tikv_grpc_msg_duration_seconds{type="kv_batch_get"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}(transaction)
```

要了解更多关于 `tidb_tikvclient_batch_wait_duration`、`tidb_tikvclient_batch_send_latency` 和 `tidb_tikvclient_rpc_net_latency_seconds{store="?"}` 等批量请求客户端耗时的细节，请参考[批量请求](#批量请求)小节。

耗时 `tikv_grpc_msg_duration_seconds{type="kv_batch_get"}` 使用如下方式计算：

```text
tikv_grpc_msg_duration_seconds{type="kv_batch_get"} =
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    n * (
        tikv_engine_seek_micro_seconds{type="seek_max"} +
        read value duration +
        read value duration(non-short value)
    )

read value duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="batch_get"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="batch_get"}))
```

TiKV 会首先得到一个快照，然后从同一个快照中读取多个值。read 操作的耗时和[点查](#点查)中的一致。当数据从磁盘中读取时，其平均耗时可以通过带有 `req="batch_get"` 属性的 `tikv_storage_rocksdb_perf` 来计算。

### 表扫描和索引扫描

下面是表扫描和索引扫描的时间消耗图：

```railroad+diagram
Diagram(
    Stack(
        NonTerminal("Resolve TSO"),
        NonTerminal("Load region cache for related table/index ranges"),
        OneOrMore(
            NonTerminal("Wait for result"),
            Comment("Next loop: drain the result"),
        ),
    ),
)
```

在进行表扫描和索引扫描时，耗时 `tidb_session_execute_duration_seconds{type="general"}` 使用如下方式计算：

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    req_per_copr * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    )
    tidb_distsql_handle_query_duration_seconds{sql_type="general"} <= send request duration
```

表扫描和索引扫描采用相同的方式处理。`req_per_copr` 是被分配的任务数量。由于执行协处理器和返回数据在不同的线程中运行，`tidb_distsql_handle_query_duration_seconds{sql_type="general"}` 是等待时间，并且小于 `send request duration`。

`send request duration` 和 `req_per_copr` 使用如下方式计算：

```text
send request duration =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="coprocessor"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}

tikv_grpc_msg_duration_seconds{type="coprocessor"} =
    tikv_coprocessor_request_wait_seconds{type="snapshot"} +
    tikv_coprocessor_request_wait_seconds{type="schedule"} +
    tikv_coprocessor_request_handler_build_seconds{type="index/select"} +
    tikv_coprocessor_request_handle_seconds{type="index/select"}

req_per_copr = rate(tidb_distsql_handle_query_duration_seconds_count) / rate(tidb_distsql_scan_keys_partial_num_count)
```

在 TiKV 中，表扫描的类型是 `select`，而索引扫描的类型是 `index`。`select` 和 `index` 类型的内部耗时是一致的。

### 索引查找

下面是索引查找的时间消耗图：

```railroad+diagram
Diagram(
    Stack(
        NonTerminal("Resolve TSO"),
        NonTerminal("Load region cache for related index ranges"),
        OneOrMore(
            Sequence(
                NonTerminal("Wait for index scan result"),
                NonTerminal("Wait for table scan result"),
            ),
        Comment("Next loop: drain the result"),
        ),
    ),
)
```

在索引查找的过程中，耗时 `tidb_session_execute_duration_seconds{type="general"}` 使用如下方式计算:

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    req_per_copr * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    ) +
    req_per_copr * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    )

req_per_copr = rate(tidb_distsql_handle_query_duration_seconds_count) / rate(tidb_distsql_scan_keys_partial_num_count)
```

一次索引查找结合了索引查找和表查找。索引查找和表查找使用流水线方式处理。

## 写请求

写请求有多个变种，因而比读请求复杂得多。下面是写请求的时间消耗图：

```railroad+diagram
Diagram(
    NonTerminal("Execute write query"),
    Choice(
        0,
        NonTerminal("Pessimistic lock keys"),
        Comment("bypass in optimistic transaction"),
    ),
    Choice(
        0,
        NonTerminal("Auto Commit Transaction"),
        Comment("bypass in non-auto-commit or explicit transaction"),
    ),
)
```

|                | 悲观事务        | 乐观事务   |
|----------------|----------------|------------|
| Auto-commit    | 执行 + 锁 + 提交 | 执行 + 提交 |
| 非 auto-commit | 执行 + 锁        | 执行       |

一次写请求可以被分解成以下三个阶段：

- 执行阶段：执行并把更改写入 TiDB 的内存中
- 锁定阶段：获取执行结果的悲观锁
- 提交阶段：通过两阶段提交协议 (2PC) 来提交事务

在执行阶段，TiDB 在内存中修改数据，其延迟主要源自读取所需的数据。对于更新和删除查询，TiDB 先从 TiKV 读取数据，再更新或删除内存中的数据。

带有点查和批量点查的锁定时读取操作 (`SELECT FOR UPDATE`) 是一个例外。该操作会在单个 RPC (Remote Procedure Call) 请求中完成读取和锁定操作。

### 锁定时点查

下面是锁定时点查的时间消耗图：

```railroad+diagram
Diagram(
    Choice(
        0,
        Sequence(
            NonTerminal("Read handle key by index key"),
            NonTerminal("Lock index key"),
        ),
        Comment("Clustered index"),
    ),
    NonTerminal("Lock handle key"),
    NonTerminal("Read value from pessimistic lock cache"),
)
```

在锁定时点查过程中，耗时 `execution(clustered PK)` 和 `execution(non-clustered PK or UK)` 使用如下方式计算：

```text
execution(clustered PK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
execution(non-clustered PK or UK) =
    2 * tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
```

锁定时点查会锁定键并获取其对应的值。相比先执行再获取锁的方式，该操作可以节省一次来回通信。锁定时点查的耗时可以看作与[锁定耗时](#锁定)是一样的。

### 锁定时批量点查

下面是锁定时批量点查的时间消耗图：

```railroad+diagram
Diagram(
    Choice(
        0,
        NonTerminal("Read handle keys by index keys"),
        Comment("Clustered index"),
    ),
    NonTerminal("Lock index and handle keys"),
    NonTerminal("Read values from pessimistic lock cache"),
)
```

在锁定时批量点查过程中，耗时 `execution(clustered PK)` 和 `execution(non-clustered PK or UK)` 使用如下方式计算：

```text
execution(clustered PK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
execution(non-clustered PK or UK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"} +
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
```

锁定时批量点查的执行过程与[锁定时点查](#锁定时点查)相似。不同的点在于，锁定时批量点查会在单个 RPC 请求中读取多个值。要了解更多关于耗时 `tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"}` 的细节，请参考[批量点查](#批量点查)小节。

### 锁定阶段

本小节介绍锁定阶段的耗时。

```text
round = ceil(
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_pessimistic_lock"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_pessimistic_lock"})) /
    committer-concurrency
)

lock = tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"} =
    round * tidb_tikvclient_request_seconds{type="PessimisticLock"}
```

锁是按照两阶段锁的结构来获取的，带有流量控制机制。流量控制会按照 `committer-concurrency`（默认值为 `128`）来限制并发在线请求的数量。为了简单说明，流量控制可以看作是请求延迟 (`round`) 的倍增。

`tidb_tikvclient_request_seconds{type="PessimisticLock"}` 使用如下方式计算：

```text
tidb_tikvclient_request_seconds{type="PessimisticLock"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

要了解关于 `tidb_tikvclient_batch_wait_duration`、`tidb_tikvclient_batch_send_latency` 和 `tidb_tikvclient_rpc_net_latency_seconds{store="?"}` 等批量请求客户端耗时的更多信息，请参考[批量请求](#批量请求)小节。

耗时 `tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"}` 使用如下方式计算：

```text
tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"} =
    tikv_scheduler_latch_wait_duration_seconds{type="acquire_pessimistic_lock"} +
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    (lock in-mem key count + lock on-disk key count) * lock read duration +
    lock on-disk key count / (lock in-mem key count + lock on-disk key count) *
    lock write duration
```

- 自 TiDB v6.0 起，TiKV 默认使用[内存悲观锁](/pessimistic-transaction.md#in-memory-pessimistic-lock)。内存悲观锁会跳过异步写入的过程。
- `lock in-mem key count` 和 `lock on-disk key count` 使用如下方式计算：

    ```text
    lock in-mem key count =
        sum(rate(tikv_in_memory_pessimistic_locking{result="success"})) /
        sum(rate(tikv_grpc_msg_duration_seconds_count{type="kv_pessimistic_lock"}}))

    lock on-disk key count =
        sum(rate(tikv_in_memory_pessimistic_locking{result="full"})) /
        sum(rate(tikv_grpc_msg_duration_seconds_count{type="kv_pessimistic_lock"}}))
    ```

    内存和磁盘中被锁定的键数量可以从内存锁计数中计算得出。TiKV 在得到锁之前会读取键对应的值，其读取耗时可以从 RocksDB 的性能上下文中计算得出：

    ```text
    lock read duration(from disk) =
        sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="acquire_pessimistic_lock"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="acquire_pessimistic_lock"}))
    ```

- `lock write duration` 是写入磁盘锁的耗时。要了解更多关于此的细节，请参考[异步写入](#异步写入)小节。

### 提交阶段

本小节介绍提交阶段的耗时。下面是提交操作的时间消耗图：

```railroad+diagram
Diagram(
    Stack(
        Sequence(
            Choice(
                0,
                Comment("use 2pc or causal consistency"),
                NonTerminal("Get min-commit-ts"),
            ),
            Optional("Async prewrite binlog"),
            NonTerminal("Prewrite mutations"),
            Optional("Wait prewrite binlog result"),
        ),
        Sequence(
            Choice(
                1,
                Comment("1pc"),
                Sequence(
                    Comment("2pc"),
                    NonTerminal("Get commit-ts"),
                    NonTerminal("Check schema, try to amend if needed"),
                    NonTerminal("Commit PK mutation"),
                ),
                Sequence(
                    Comment("async-commit"),
                    NonTerminal("Commit mutations asynchronously"),
                ),
            ),
            Choice(
                0,
                Comment("committed"),
                NonTerminal("Async cleanup"),
            ),
            Optional("Commit binlog"),
        ),
    ),
)
```

提交的耗时使用如下方式计算：

```text
commit =
    Get_latest_ts_time +
    Prewrite_time +
    Get_commit_ts_time +
    Commit_time

Get_latest_ts_time = Get_commit_ts_time =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"}

prewrite_round = ceil(
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_prewrite"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_prewrite"})) /
    committer-concurrency
)

commit_round = ceil(
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_commit"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_commit"})) /
    committer-concurrency
)

Prewrite_time =
    prewrite_round * tidb_tikvclient_request_seconds{type="Prewrite"}

Commit_time =
    commit_round * tidb_tikvclient_request_seconds{type="Commit"}
```

提交的耗时可以拆解为以下四个指标：

- `Get_latest_ts_time` 代表异步提交或单阶段 (1PC) 提交事务中获取最新 TSO 的耗时。
- `Prewrite_time` 代表预先写阶段的耗时。
- `Get_commit_ts_time` 代表普通两阶段 (2PC) 事务的耗时。
- `Commit_time` 代表提交阶段的耗时。需要注意的是，异步提交和单阶段 (1PC) 事务没有此阶段。

与悲观锁一样，流量控制充当延迟的放大，即上述公式中的 `prewrite_round` 和 `commit_round`。

`tidb_tikvclient_request_seconds{type="Prewrite"}` 和 `tidb_tikvclient_request_seconds{type="Commit"}` 的耗时使用如下方式计算：

```text
tidb_tikvclient_request_seconds{type="Prewrite"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_prewrite"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}

tidb_tikvclient_request_seconds{type="Commit"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_commit"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

要了解关于 `tidb_tikvclient_batch_wait_duration`、`tidb_tikvclient_batch_send_latency` 和 `tidb_tikvclient_rpc_net_latency_seconds{store="?"}` 等批量请求客户端耗时的更多信息，请参考[批量请求](#批量请求)小节。

`tikv_grpc_msg_duration_seconds{type="kv_prewrite"}` 使用如下方式计算：

```text
tikv_grpc_msg_duration_seconds{type="kv_prewrite"} =
    prewrite key count * prewrite read duration +
    prewrite write duration

prewrite key count =
    sum(rate(tikv_scheduler_kv_command_key_write_sum{type="prewrite"})) /
    sum(rate(tikv_scheduler_kv_command_key_write_count{type="prewrite"}))

prewrite read duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="prewrite"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="prewrite"}))
```

与 TiKV 中的锁一样，预先写在读取和写入阶段均进行了处理。读取阶段的耗时可以从 RocksDB 性能上下文计算。有关写入阶段耗时的更多信息，请参考[异步写入](#异步写入)部分。

`tikv_grpc_msg_duration_seconds{type="kv_commit"}`使用如下方式计算：

```text
tikv_grpc_msg_duration_seconds{type="kv_commit"} =
    commit key count * commit read duration +
    commit write duration

commit key count =
    sum(rate(tikv_scheduler_kv_command_key_write_sum{type="commit"})) /
    sum(rate(tikv_scheduler_kv_command_key_write_count{type="commit"}))

commit read duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="commit"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="commit"})) (storage)
```

`kv_commit` 的耗时与 `kv_prewrite` 几乎一致。要了解更多关于写入耗时的细节，请参考[异步写入](#异步写入)小节。

## 批量请求

下面是批量请求客户端的时间消耗图：

```railroad+diagram
Diagram(
    NonTerminal("Get conn pool to the target store"),
    Choice(
        0,
        Sequence(
            Comment("Batch enabled"),
                NonTerminal("Push request to channel"),
                NonTerminal("Wait response"),
            ),
            Sequence(
            NonTerminal("Get conn from pool"),
            NonTerminal("Call RPC"),
            Choice(
                0,
                Comment("Unary call"),
                NonTerminal("Recv first"),
            ),
        ),
    ),
)
```

- 总体的发送请求耗时看作 `tidb_tikvclient_request_seconds`。
- RPC 客户端为每个存储维护各自的连接池（称为 ConnArray），每个连接池都包含带有一个批量请求（发送）通道的 BatchConn。
- 批量请求会在存储是 TiKV 并且 batch 大小为正数时开启。这符合绝大多数的情况。
- 批量请求通道的大小是 [`tikv-client.max-batch-size`](/tidb-configuration-file.md#max-batch-size)（默认值为 `128`。请求入队的耗时看作 `tidb_tikvclient_batch_wait_duration`。
- 一共有 `CmdBatchCop`、`CmdCopStream` 和 `CmdMPPConn` 三种流式请求。流式请求会引入一个额外的 `recv()` 调用来获取流中的第一个相应。

尽管有一些延迟没有被考虑，`tidb_tikvclient_request_seconds` 大致使用如下方式计算：

```text
tidb_tikvclient_request_seconds{type="?"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_?"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

- `tidb_tikvclient_batch_wait_duration` 记录批量请求系统的等待耗时。
- `tidb_tikvclient_batch_send_latency` 记录批量请求系统的编码耗时。
- `tikv_grpc_msg_duration_seconds{type="kv_?"}` 是 TiKV 的处理耗时。
- `tidb_tikvclient_rpc_net_latency_seconds` 记录网络延迟。

## TiKV 快照

下面是 TiKV 快照操作的时间消耗图：

```railroad+diagram
Diagram(
    Choice(
        0,
        Comment("Local Read"),
        Sequence(
            NonTerminal("Propose Wait"),
            NonTerminal("Read index Read Wait"),
        ),
    ),
    NonTerminal("Fetch A Snapshot From KV Engine"),
)
```

一个 TiKV 快照的总体耗时可以使用 `tikv_storage_engine_async_request_duration_seconds{type="snapshot"}` 指标观察，它的计算方式如下：

```text
tikv_storage_engine_async_request_duration_seconds{type="snapshot"} =
    tikv_coprocessor_request_wait_seconds{type="snapshot"} =
    tikv_raftstore_request_wait_time_duration_secs +
    tikv_raftstore_commit_log_duration_seconds +
    get snapshot from rocksdb duration
```

当 leader lease 过期时，TiKV 会在从 RocksDB 获取快照之前提出读索引命令。`tikv_raftstore_request_wait_time_duration_secs` 和 `tikv_raftstore_commit_log_duration_seconds` 是提交读索引命令的耗时。

从 RocksDB 获取快照通常是一个快速操作，因此 `get snapshot from rocksdb duration` 的耗时可以被忽略。

## 异步写入

Async write is the process that TiKV writes data into the Raft-based replicated state machine asynchronously with callback.

- The following is the time cost diagram of async write operations when the asynchronous IO is disabled:

    ```railroad+diagram
    Diagram(
        NonTerminal("Propose Wait"),
        NonTerminal("Process Command"),
        Choice(
            0,
            Sequence(
                NonTerminal("Wait Current Batch"),
                NonTerminal("Write to Log Engine"),
            ),
            Sequence(
                NonTerminal("RaftMsg Send Wait"),
                NonTerminal("Commit Log Wait"),
            ),
        ),
        NonTerminal("Apply Wait"),
        NonTerminal("Apply Log"),
    )
    ```

- The following is the time cost diagram of async write operations when the asynchronous IO is enabled:

    ```railroad+diagram
    Diagram(
        NonTerminal("Propose Wait"),
        NonTerminal("Process Command"),
        Choice(
            0,
            NonTerminal("Wait Until Persisted by Write Worker"),
            Sequence(
                NonTerminal("RaftMsg Send Wait"),
                NonTerminal("Commit Log Wait"),
            ),
        ),
        NonTerminal("Apply Wait"),
        NonTerminal("Apply Log"),
    )
    ```

The async write duration is calculated as:

```text
async write duration(async io disabled) =
    propose +
    async io disabled commit +
    tikv_raftstore_apply_wait_time_duration_secs +
    tikv_raftstore_apply_log_duration_seconds

async write duration(async io enabled) =
    propose +
    async io enabled commit +
    tikv_raftstore_apply_wait_time_duration_secs +
    tikv_raftstore_apply_log_duration_seconds
```

Async write can be broken down into the following three phases:

- Propose
- Commit
- Apply: `tikv_raftstore_apply_wait_time_duration_secs + tikv_raftstore_apply_log_duration_seconds` in the preceding formula

The duration of propose phase is calculated as:

```text
propose =
    propose wait duration +
    propose duration

propose wait duration =
    tikv_raftstore_store_wf_batch_wait_duration_seconds

propose duration =
    tikv_raftstore_store_wf_send_to_queue_duration_seconds -
    tikv_raftstore_store_wf_batch_wait_duration_seconds
```

The Raft process is recorded in a waterfall manner. So the propose duration is calculated from the difference between the two metrics.

The duration of commit phase is calculated as:

```text
async io disabled commit = max(
    persist log locally duration,
    replicate log duration
)

async io enabled commit = max(
    wait by write worker duration,
    replicate log duration
)
```

Since v5.3.0, TiKV supports Async IO Raft (write Raft log by a StoreWriter thread pool). The Async IO Raft is only enabled when the [`store-io-pool-size`](/tikv-configuration-file.md#store-io-pool-size-new-in-v530) is set to a positive value, which changes the process of commit. The `persist log locally duration` and `wait by write worker duration` are calculated as:

```text
persist log locally duration =
    batch wait duration +
    write to raft db duration

batch wait duration =
    tikv_raftstore_store_wf_before_write_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds

write to raft db duration =
    tikv_raftstore_store_wf_write_end_duration_seconds -
    tikv_raftstore_store_wf_before_write_duration_seconds

wait by write worker duration =
    tikv_raftstore_store_wf_persist_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds
```

The difference between with and without Async IO is the duration of persisting log locally. With Async IO, the duration of persisting log locally can be calculated from the waterfall metrics directly (skip the batch wait duration).

The replicate log duration records the duration of log persisted in quorum peers, which contains an RPC duration and the duration of log persisting in the majority. The `replicate log duration` is calculated as:

```text
replicate log duration =
    raftmsg send wait duration +
    commit log wait duration

raftmsg send wait duration =
    tikv_raftstore_store_wf_send_proposal_duration_seconds -
    tikv_raftstore_store_wf_send_to_queue_duration_seconds

commit log wait duration =
    tikv_raftstore_store_wf_commit_log_duration -
    tikv_raftstore_store_wf_send_proposal_duration_seconds
```

### Raft DB

The following is the time cost diagram of Raft DB operations:

```railroad+diagram
Diagram(
    NonTerminal("Wait for Writer Leader"),
    NonTerminal("Write and Sync Log"),
    NonTerminal("Apply Log to Memtable"),
)
```

```text
write to raft db duration = raft db write duration
commit log wait duration >= raft db write duration

raft db write duration(raft engine enabled) =
    raft_engine_write_preprocess_duration_seconds +
    raft_engine_write_leader_duration_seconds +
    raft_engine_write_apply_duration_seconds

raft db write duration(raft engine disabled) =
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_thread_wait"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_scheduling_flushes_compactions_time"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_wal_time"} +
    tikv_raftstore_store_perf_context_time_duration_secs{type="write_memtable_time"}
```

Because `commit log wait duration` is the slowest duration of quorum peers, it might be larger than `raft db write duration`.

Since v6.1.0, TiKV uses [Raft Engine](/tikv-configuration-file.md#raft-engine) as its default log storage engine, which changes the process of writing log.

### KV DB

The following is the time cost diagram of KV DB operations:

```railroad+diagram
Diagram(
    NonTerminal("Wait for Writer Leader"),
    NonTerminal("Preprocess"),
    Choice(
        0,
        Comment("No Need to Switch"),
        NonTerminal("Switch WAL or Memtable"),
    ),
    NonTerminal("Write and Sync WAL"),
    NonTerminal("Apply to Memtable"),
)
```

```text
tikv_raftstore_apply_log_duration_seconds =
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_thread_wait"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_scheduling_flushes_compactions_time"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_wal_time"} +
    tikv_raftstore_apply_perf_context_time_duration_secs{type="write_memtable_time"}
```

In the async write process, committed logs need to be applied into the KV DB. The applying duration can be calculated from the RocksDB performance context.

## 诊断场景

The preceding sections explain the details about time cost metrics during querying. This section introduces common procedures of metrics analysis when you encounter slow read or write queries. All metrics can be checked in the DB Time panel of [Performance Overview Dashboard](/grafana-performance-overview-dashboard.md).

### Slow read queries

If `SELECT` statements account for a significant portion of the DB time, you can assume that TiDB is slow at read queries.

The execution plans of slow queries can be found in the [Top SQL statements](/dashboard/dashboard-overview.md#top-sql-statements) panel of TiDB Dashboard. To investigate the time costs of slow read queries, you can analyze [Point get](#point-get), [Batch point get](#batch-point-get) and some [simple coprocessor queries](#table-scan--index-scan) according to the preceding descriptions.

### Slow write queries

Before investigating slow writes, you need to troubleshoot the cause of the conflicts by checking `tikv_scheduler_latch_wait_duration_seconds_sum{type="acquire_pessimistic_lock"} by (instance)`:

- If this metric is high in some specific TiKV instances, there might be conflicts in hot Regions.
- If this metric is high across all instances, there might be conflicts in the application.

After confirming the cause of conflicts from application, you can investigate slow write queries by analyzing the duration of [Lock](#lock) and [Commit](#commit).
