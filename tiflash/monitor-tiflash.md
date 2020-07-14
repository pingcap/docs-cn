---
title: Monitor the TiFlash Cluster
summary: Learn the monitoring items of TiFlash.
aliases: ['/docs/dev/tiflash/monitor-tiflash/','/docs/dev/reference/tiflash/monitor/']
---

# Monitor the TiFlash Cluster

This document describes the monitoring items of TiFlash.

## Monitor the Coprocessor

| Monitoring items | Description |
|:---|:-----|
| `tiflash_coprocessor_request_count` | The number of coprocessor requests received. `batch` is the number of batch requests. `batch_cop` is the number of coprocessor requests in the batch requests. `cop` is the number of coprocessor requests that are sent directly via the coprocessor interface. `cop_dag` is the number of dag requests in all coprocessor requests. |
| `tiflash_coprocessor_executor_count` | The number of each type of dag executors. `table_scan` is the table scan executor. `selection` is the selection executor. `aggregation` is the aggregation executor. `top_n` is the `TopN` executor. `limit` is the limit executor. |
| `tiflash_coprocessor_request_duration_seconds` | The histogram of the duration of each coprocessor request, in which the duration is from the time that the coprocessor request is received to the time that the response to the request is completed. `batch` is the duration of batch requests. `cop` is the duration of coprocessor requests that are sent directly via the coprocessor interface. |
| `tiflash_coprocessor_request_error` | The number of errors of coprocessor requests. `meet_lock` means that the read data is locked. `region_not_found` means that the Region does not exist. `epoch_not_match` means the read Region epoch is inconsistent with the local epoch. `kv_client_error` means that the communication with TiKV returns an error. `internal_error` is the internal system error of TiFlash. `other` is other type of errors. |
| `tiflash_coprocessor_request_handle_seconds` | The histogram of the processing time of each coprocessor request, in which the processing time is from starting to execute the coprocessor request to completing the execution. `batch` is the processing time of batch request. `cop` is the processing time of coprocessor requests that are sent directly via the coprocessor interface. |
| `tiflash_coprocessor_response_bytes` | The total bytes of the response. |

## Monitor DDL operations

| Monitoring items | Description |
|:---|:-----|
| `tiflash_schema_version` | The version of the schema currently cached in TiFlash. |
| `tiflash_schema_apply_count` | This item includes the count of three types of `appy`: `diff apply`, `full apply`, and `failed apply`. `diff apply` is the normal process of a single apply. If `diff apply` fails, `failed apply` increases by `1`, and TiFlash rolls back to `full apply`. |
| `tiflash_schema_internal_ddl_count` | The number of specific DDL operations in TiFlash. |
| `tiflash_schema_apply_duration_seconds` | The time used for a single `apply schema` operation. |

## Monitor Raft

| Monitoring items | Description |
|:---|:-----|
| `tiflash_raft_read_index_count` | The number of times that the coprocessor triggers the `read_index` request, which equals to the number of Regions triggered by a coprocessor. |
| `tiflash_raft_read_index_duration_seconds` | The time used by `read_index`. Most time is used for interaction with Leader and retry. |
| `tiflash_raft_wait_index_duration_seconds` | The time used by `wait_index`, namely the time used to wait until local index >= read_index after the `read_index` request is received. |
