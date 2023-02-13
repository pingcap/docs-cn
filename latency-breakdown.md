---
title: Latency Breakdown
summary: Introduce more details about TiDB latency and how to analyze latency in real use cases.
---

# Latency Breakdown

This document breaks down the latency into metrics and then analyzes it from the user's perspective from the following aspects:

- [General SQL layer](#general-sql-layer)
- [Read queries](#read-queries)
- [Write queries](#write-queries)
- [Batch client](#batch-client)
- [TiKV snapshot](#tikv-snapshot)
- [Async write](#async-write)

These analyses provide you with a deep insight into time cost during TiDB SQL queries. This is a guide to TiDB's critical path diagnosis. Besides, the [Diagnosis use cases](#diagnosis-use-cases) section introduces how to analyze latency in real use cases.

It's better to read [Performance Analysis and Tuning](/performance-tuning-methods.md) before this document. Note that when breaking down latency into metrics, the average value of duration or latency is calculated instead of some specific slow queries. Many metrics are shown as histogram, which is a distribution of the duration or latency. To calculate the average latency, you need to use the following sum and count counter.

```
avg = ${metric_name}_sum / ${metric_name}_count
```

Metrics described in this document can be read directly from the Prometheus dashboard of TiDB.

## General SQL layer

This general SQL layer latency exists on the top level of TiDB and is shared by all SQL queries. The following is the time cost diagram of general SQL layer operation:

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

The general SQL layer latency can be observed as the `e2e duration` metric and is calculated as:

```text
e2e duration =
    tidb_server_get_token_duration_seconds +
    tidb_session_parse_duration_seconds +
    tidb_session_compile_duration_seconds +
    tidb_session_execute_duration_seconds{type="general"}
```

- `tidb_server_get_token_duration_seconds` records the duration of Token waiting. This is usually less than 1 millisecond and is small enough to be ignored.
- `tidb_session_parse_duration_seconds` records the duration of parsing SQL queries to an Abstract Syntax Tree (AST), which can be skipped by [`PREPARE/EXECUTE` statements](/develop/dev-guide-optimize-sql-best-practices.md#use-prepare).
- `tidb_session_compile_duration_seconds` records the duration of compiling an AST to an execution plan, which can be skipped by [SQL prepare execution plan cache](/sql-prepared-plan-cache.md).
- `tidb_session_execute_duration_seconds{type="general"}` records the duration of execution, which mixes all types of user queries. This needs to be broken down into fine-grained durations for analyzing performance issues or bottlenecks.

Generally, OLTP (Online Transactional Processing) workload can be divided into read and write queries, which share some critical code. The following sections describe latency in [read queries](#read-queries) and [write queries](#write-queries), which are executed differently.

## Read queries

Read queries have only a single process form.

### Point get

The following is the time cost diagram of [point get](/glossary.md#point-get) operations:

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

During point get, the `tidb_session_execute_duration_seconds{type="general"}` duration is calculated as:

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    read handle duration +
    read value duration
```

`pd_client_cmd_handle_cmds_duration_seconds{type="wait"}` records the duration of fetching [TSO (Timestamp Oracle)](/glossary.md#tso) from PD. When reading in an auto-commit transaction mode with a clustered primary index or from a snapshot, the value will be zero.

The `read handle duration` and `read value duration` are calculated as:

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

The `tidb_tikvclient_request_seconds{type="Get"}` records a duration of get requests which are sent directly to TiKV via a batched gRPC wrapper. For more details about the preceding batch client duration, such as `tidb_tikvclient_batch_wait_duration`, `tidb_tikvclient_batch_send_latency`, and `tidb_tikvclient_rpc_net_latency_seconds{store="?"}`, refer to the [Batch client](#batch-client) section.

The `tikv_grpc_msg_duration_seconds{type="kv_get"}` duration is calculated as:

```text
tikv_grpc_msg_duration_seconds{type="kv_get"} =
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    tikv_engine_seek_micro_seconds{type="seek_average"} +
    read value duration +
    read value duration(non-short value)
```

At this time, requests are in TiKV. TiKV processes get requests by one seek and one or two read actions (short values are encoded in a write column family, and reading it once is enough). TiKV gets a snapshot before processing the read request. For more details about the TiKV snapshot duration, refer to the [TiKV snapshot](#tikv-snapshot) section.

The `read value duration(from disk)` is calculated as:

```text
read value duration(from disk) =
    sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="get/batch_get_command"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="get/batch_get_command"}))
```

TiKV uses RocksDB as its storage engine. When the required value is missing from the block cache, TiKV needs to load the value from the disk. For `tikv_storage_rocksdb_perf`, the get request can be either `get` or `batch_get_command`.

### Batch point get

The following is the time cost diagram of batch point get operations:

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

During batch point get, the `tidb_session_execute_duration_seconds{type="general"}` is calculated as:

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    read handles duration +
    read values duration
```

The process of batch point get is almost the same as [Point get](#point-get) except that batch point get reads multiple values at the same time.

The `read handles duration` and `read values duration` are calculated as:

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

For more details about the preceding batch client duration, such as `tidb_tikvclient_batch_wait_duration(transaction)`, `tidb_tikvclient_batch_send_latency(transaction)`, and `tidb_tikvclient_rpc_net_latency_seconds{store="?"}(transaction)`, refer to the [Batch client](#batch-client) section.

The `tikv_grpc_msg_duration_seconds{type="kv_batch_get"}` duration is calculated as:

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

After getting a snapshot, TiKV reads multiple values from the same snapshot. The read duration is the same as [Point get](#point-get). When TiKV loads data from disk, the average duration can be calculated by `tikv_storage_rocksdb_perf` with `req="batch_get"`.

### Table scan & Index scan

The following is the time cost diagram of table scan and index scan operations:

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

During table scan and index scan, the `tidb_session_execute_duration_seconds{type="general"}` duration is calculated as:

```text
tidb_session_execute_duration_seconds{type="general"} =
    pd_client_cmd_handle_cmds_duration_seconds{type="wait"} +
    req_per_copr * (
        tidb_distsql_handle_query_duration_seconds{sql_type="general"}
    )
    tidb_distsql_handle_query_duration_seconds{sql_type="general"} <= send request duration
```

Table scan and index scan are processed in the same way. `req_per_copr` is the distributed task count. Because coprocessor execution and data responding to client are in different threads, `tidb_distsql_handle_query_duration_seconds{sql_type="general"}` is the wait time and it is less than the `send request duration`.

The `send request duration` and `req_per_copr` are calculated as:

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

In TiKV, the table scan type is `select` and the index scan type is `index`. The details of `select` and `index` type duration are the same.

### Index look up

The following is the time cost diagram of index look up operations:

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

During index look up, the `tidb_session_execute_duration_seconds{type="general"}` duration is calculated as:

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

An index look up combines index scan and table scan, which are processed in a pipeline.

## Write queries

Write queries are much more complex than read queries. There are some variants of write queries. The following is the time cost diagram of write queries operations:

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

|                 | Pessimistic transaction | Optimistic transaction |
|-----------------|-------------------------|------------------------|
| Auto-commit     | execute + lock + commit | execute + commit       |
| Non-auto-commit | execute + lock          | execute                |

A write query is divided into the following three phases:

- execute phase: execute and write mutation into the memory of TiDB.
- lock phase: acquire pessimistic locks for the execution result.
- commit phase: commit the transaction via the two-phase commit protocol (2PC).

In the execute phase, TiDB manipulates data in memory and the main latency comes from reading the required data. For update and delete queries, TiDB reads data from TiKV first, and then updates or deletes the row in memory.

The exception is lock-time read operations (`SELECT FOR UPDATE`) with point get and batch point get, which perform read and lock in a single Remote Procedure Call (RPC).

### Lock-time point get

The following is the time cost diagram of lock-time point get operations:

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

During lock-time point get, the `execution(clustered PK)` and `execution(non-clustered PK or UK)` duration are calculated as:

```text
execution(clustered PK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
execution(non-clustered PK or UK) =
    2 * tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
```

Lock-time point get locks the key and returns its value. Compared with the lock phase after execution, this saves 1 round trip. The duration of the lock-time point get can be treated the same as [Lock duration](#lock).

### Lock-time batch point get

The following is the time cost diagram of lock-time batch point get operations:

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

During lock-time batch point get, the `execution(clustered PK)` and `execution(non-clustered PK or UK)` duration are calculated as:

```text
execution(clustered PK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
execution(non-clustered PK or UK) =
    tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"} +
    tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"}
```

The execution of the lock-time batch point get is similar to the [Lock-time point get](#lock-time-point-get) except that the lock-time batch point get reads multiple values in a single RPC. For more details about the `tidb_tikvclient_txn_cmd_duration_seconds{type="batch_get"}` duration, refer to the [Batch point get](#batch-point-get) section.

### Lock

This section describes the lock duration.

```text
round = ceil(
    sum(rate(tidb_tikvclient_txn_regions_num_sum{type="2pc_pessimistic_lock"})) /
    sum(rate(tidb_tikvclient_txn_regions_num_count{type="2pc_pessimistic_lock"})) /
    committer-concurrency
)

lock = tidb_tikvclient_txn_cmd_duration_seconds{type="lock_keys"} =
    round * tidb_tikvclient_request_seconds{type="PessimisticLock"}
```

Locks are acquired through the 2PC structure, which has a flow control mechanism. The flow control limits concurrent on-the-fly requests by `committer-concurrency` (default value is `128`). For simplicity, the flow control can be treated as an amplification of request latency (`round`).

The `tidb_tikvclient_request_seconds{type="PessimisticLock"}` is calculated as:

```text
tidb_tikvclient_request_seconds{type="PessimisticLock"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

For more details about the preceding batch client duration, such as `tidb_tikvclient_batch_wait_duration`, `tidb_tikvclient_batch_send_latency`, and `tidb_tikvclient_rpc_net_latency_seconds{store="?"}`, refer to the [Batch client](#batch-client) section.

The `tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"}` duration is calculated as:

```text
tikv_grpc_msg_duration_seconds{type="kv_pessimistic_lock"} =
    tikv_scheduler_latch_wait_duration_seconds{type="acquire_pessimistic_lock"} +
    tikv_storage_engine_async_request_duration_seconds{type="snapshot"} +
    (lock in-mem key count + lock on-disk key count) * lock read duration +
    lock on-disk key count / (lock in-mem key count + lock on-disk key count) *
    lock write duration
```

- Since TiDB v6.0, TiKV uses [in-memory pessimistic lock](/pessimistic-transaction.md#in-memory-pessimistic-lock) by default. In-memory pessimistic lock bypass the async write process.
- `tikv_storage_engine_async_request_duration_seconds{type="snapshot"}` is a snapshot type duration. For more details, refer to the [TiKV Snapshot](#tikv-snapshot) section.
- The `lock in-mem key count` and `lock on-disk key count` are calculated as:

    ```text
    lock in-mem key count =
        sum(rate(tikv_in_memory_pessimistic_locking{result="success"})) /
        sum(rate(tikv_grpc_msg_duration_seconds_count{type="kv_pessimistic_lock"}}))

    lock on-disk key count =
        sum(rate(tikv_in_memory_pessimistic_locking{result="full"})) /
        sum(rate(tikv_grpc_msg_duration_seconds_count{type="kv_pessimistic_lock"}}))
    ```

    The count of in-memory and on-disk locked keys can be calculated by the in-memory lock counter. TiKV reads the keys' values before acquiring locks, and the read duration can be calculated by RocksDB performance context.

    ```text
    lock read duration(from disk) =
        sum(rate(tikv_storage_rocksdb_perf{metric="block_read_time",req="acquire_pessimistic_lock"})) / sum(rate(tikv_storage_rocksdb_perf{metric="block_read_count",req="acquire_pessimistic_lock"}))
    ```

- `lock write duration` is the duration of writing on-disk lock. For more details, refer to the [Async write](#async-write) section.

### Commit

This section describes the commit duration. The following is the time cost diagram of commit operations:

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
                    NonTerminal("Check schema"),
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

The duration of the commit phase is calculated as:

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

The commit duration can be broken down into four metrics:

- `Get_latest_ts_time` records the duration of getting latest TSO in async-commit or single-phase commit (1PC) transaction.
- `Prewrite_time` records the duration of the prewrite phase.
- `Get_commit_ts_time` records the duration of common 2PC transaction.
- `Commit_time` records the duration of the commit phase. Note that an async-commit or 1PC transaction does not have this phase.

Like pessimistic lock, flow control acts as an amplification of latency (`prewrite_round` and `commit_round` in the preceding formula).

The `tidb_tikvclient_request_seconds{type="Prewrite"}` and `tidb_tikvclient_request_seconds{type="Commit"}` duration are calculated as:

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

For more details about the preceding batch client duration, such as `tidb_tikvclient_batch_wait_duration`, `tidb_tikvclient_batch_send_latency`, and `tidb_tikvclient_rpc_net_latency_seconds{store="?"}`, refer to the [Batch client](#batch-client) section.

The `tikv_grpc_msg_duration_seconds{type="kv_prewrite"}` is calculated as:

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

Like locks in TiKV, prewrite is processed in read and write phases. The read duration can be calculated from the RocksDB performance context. For more details about the write duration, refer to the [Async write](#async-write) section.

The `tikv_grpc_msg_duration_seconds{type="kv_commit"}` is calculated as:

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

The duration of `kv_commit` is almost the same as `kv_prewrite`. For more details about the write duration, refer to the [Async write](#async-write) section.

## Batch client

The following is the time cost diagram of the batch client:

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

- The overall duration of sending a request is observed as `tidb_tikvclient_request_seconds`.
- RPC client maintains connection pools (named ConnArray) to each store, and each pool has a BatchConn with a batch request (send) channel.
- Batch is enabled when the store is TiKV and batch size is positive, which is true in most cases.
- The size of batch request channel is [`tikv-client.max-batch-size`](/tidb-configuration-file.md#max-batch-size) (default is `128`), the duration of enqueue is observed as `tidb_tikvclient_batch_wait_duration`.
- There are three kinds of stream requests: `CmdBatchCop`, `CmdCopStream`, and `CmdMPPConn`, which involve an additional `recv()` call to fetch the first response from the stream.

Though there is still some latency missed observed, the `tidb_tikvclient_request_seconds` can be calculated approximately as:

```text
tidb_tikvclient_request_seconds{type="?"} =
    tidb_tikvclient_batch_wait_duration +
    tidb_tikvclient_batch_send_latency +
    tikv_grpc_msg_duration_seconds{type="kv_?"} +
    tidb_tikvclient_rpc_net_latency_seconds{store="?"}
```

- `tidb_tikvclient_batch_wait_duration` records the waiting duration in the batch system.
- `tidb_tikvclient_batch_send_latency` records the encode duration in the batch system.
- `tikv_grpc_msg_duration_seconds{type="kv_?"}` is the TiKV processing duration.
- `tidb_tikvclient_rpc_net_latency_seconds` records the network latency.

## TiKV snapshot

The following is the time cost diagram of TiKV snapshot operations:

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

The overall duration of a TiKV snapshot is observed as `tikv_storage_engine_async_request_duration_seconds{type="snapshot"}` and is calculated as:

```text
tikv_storage_engine_async_request_duration_seconds{type="snapshot"} =
    tikv_coprocessor_request_wait_seconds{type="snapshot"} =
    tikv_raftstore_request_wait_time_duration_secs +
    tikv_raftstore_commit_log_duration_seconds +
    get snapshot from rocksdb duration
```

When leader lease is expired, TiKV proposes a read index command before getting a snapshot from RocksDB. `tikv_raftstore_request_wait_time_duration_secs` and `tikv_raftstore_commit_log_duration_seconds` are the duration of committing read index command.

Since getting a snapshot from RocksDB is usually a fast operation, the `get snapshot from rocksdb duration` is ignored.

## Async write

Async write is the process that TiKV writes data into the Raft-based replicated state machine asynchronously with a callback.

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

The duration of the propose phase is calculated as:

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

The duration of the commit phase is calculated as:

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

The difference between with and without Async IO is the duration of persisting logs locally. With Async IO, the duration of persisting log locally can be calculated from the waterfall metrics directly (skip the batch wait duration).

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

Because `commit log wait duration` is the longest duration of quorum peers, it might be larger than `raft db write duration`.

Since v6.1.0, TiKV uses [Raft Engine](/glossary.md#raft-engine) as its default log storage engine, which changes the process of writing log.

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

In the async write process, committed logs need to be applied to the KV DB. The applying duration can be calculated from the RocksDB performance context.

## Diagnosis use cases

The preceding sections explain the details about time cost metrics during querying. This section introduces common procedures of metrics analysis when you encounter slow read or write queries. All metrics can be checked in the Database Time panel of [Performance Overview Dashboard](/grafana-performance-overview-dashboard.md).

### Slow read queries

If `SELECT` statements account for a significant portion of the database time, you can assume that TiDB is slow at read queries.

The execution plans of slow queries can be found in the [Top SQL statements](/dashboard/dashboard-overview.md#top-sql-statements) panel of TiDB Dashboard. To investigate the time costs of slow read queries, you can analyze [Point get](#point-get), [Batch point get](#batch-point-get) and some [simple coprocessor queries](#table-scan--index-scan) according to the preceding descriptions.

### Slow write queries

Before investigating slow writes, you need to troubleshoot the cause of the conflicts by checking `tikv_scheduler_latch_wait_duration_seconds_sum{type="acquire_pessimistic_lock"} by (instance)`:

- If this metric is high in some specific TiKV instances, there might be conflicts in hot Regions.
- If this metric is high across all instances, there might be conflicts in the application.

After confirming the cause of conflicts from the application, you can investigate slow write queries by analyzing the duration of [Lock](#lock) and [Commit](#commit).
