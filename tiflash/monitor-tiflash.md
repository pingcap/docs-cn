---
title: TiFlash 集群监控
aliases: ['/docs-cn/v3.1/tiflash/monitor-tiflash/','/docs-cn/v3.1/reference/tiflash/monitor/']
---

# TiFlash 集群监控

本文介绍 TiFlash 集群的相关监控项及说明。

## COPROCESSOR 相关监控

| 监控指标名称       | 监控指标说明             |
|-------------------|-------------------------------------|
| tiflash_coprocessor_request_count  | 收到的 coprocessor 请求数量，其中 batch 是 batch 请求数量，batch_cop 是 batch 请求中的 coprocessor 请求数量，cop 是直接通过 coprocessor 接口发送的 coprocessor 请求数量，cop_dag 是所有 coprocessor 请求中 dag 请求数量            |
| tiflash_coprocessor_executor_count   | 每种 dag 算子的数量，其中 table_scan 是扫表算子，selection 是过滤算子，aggregation 是聚合算子，top_n 是 TopN 算子，limit 是 limit 算子                 |
| tiflash_coprocessor_request_duration_seconds | 每个 coprocessor request 总时间直方图，总时间为接收到该 coprocessor 请求至请求应答完毕的时间，其中 batch 是 batch 请求的总时间，cop 是直接通过 coprocessor 接口发送的 coprocessor 请求总时间                  |
| tiflash_coprocessor_request_error  | coprocessor 请求的错误数量，其中 meet_lock 为读取的数据有锁，region_not_found 为 Region 不存在，epoch_not_match 为读取的 Region epoch 与本地不一致，kv_client_error 为与 TiKV 通信产生的错误，internal_error 为 TiFlash 内部系统错误，other 为其他错误 |
| tiflash_coprocessor_request_handle_seconds   | 每个 coprocessor 请求处理时间直方图，处理时间为该 coprocessor 请求开始执行到执行结束的时间，其中 batch 是 batch 请求的处理时间，cop 是直接通过 coprocessor 接口发送的 coprocessor 请求处理时间           |
| tiflash_coprocessor_response_bytes   | 应答总字节数         |

## DDL 相关监控

| 监控指标名称         | 监控指标说明                           |
|-------------------------------|-------------------------|
| tiflash_schema_version  | TiFlash 目前缓存的 schema 版本 |
| tiflash_schema_apply_count  | 分为 diff apply、full apply 和 failed apply：diff apply 是正常的单次 apply 过程，如果 diff apply 失败，则 failed apply +1，并回退到 full apply |
| tiflash_schema_internal_ddl_count  | TiFlash 内部进行的具体 DDL 操作的总数  |
| tiflash_schema_apply_duration_seconds | 单次 apply schema 消耗的时间 |

## Raft 相关监控

| 监控指标名称     | 监控指标说明  |
|---------------------------|------------------------|
| tiflash_raft_read_index_count  | coprocessor 触发 read_index 请求的次数，等于一个 coprocessor 触发的 Region 总数   |
| tiflash_raft_read_index_duration_seconds | read_index 消耗的时间，主要消耗时间在于和 leader 的交互和重试时间  |
| tiflash_raft_wait_index_duration_seconds | wait_index 消耗的时间，即拿到 read_index 请求后，等待 local index >= read_index 所花费的时间 |
