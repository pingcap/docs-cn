---
title: TiFlash 报警规则
---

# TiFlash 报警规则

本文介绍了 TiFlash 集群的报警规则。

## `TiFlash_schema_error`

- 报警规则：

    `increase(tiflash_schema_apply_count{type="failed"}[15m]) > 0`

- 规则描述：

    出现 schema apply 错误时报警。

- 处理方法：

    可能是逻辑问题，联系 TiFlash 开发人员。

## `TiFlash_schema_apply_duration`

- 报警规则：

    `histogram_quantile(0.99, sum(rate(tiflash_schema_apply_duration_seconds_bucket[1m])) BY (le, instance)) > 20`

- 规则描述：

    apply 时间超过 20 秒的概率超过 99% 时报警。

- 处理方法：

    可能是 TiFlash TMT 引擎内部问题，联系 TiFlash 开发人员。

## `TiFlash_raft_read_index_duration`

- 报警规则：

    `histogram_quantile(0.99, sum(rate(tiflash_raft_read_index_duration_seconds_bucket[1m])) BY (le, instance)) > 3`

- 规则描述：

    read index 时间超过 3 秒的概率超过 99% 时报警。

    > **注意：**
    >
    > read index 请求是发送给 TiKV leader 的 kvproto 请求，TiKV region 的重试，或 Store 的繁忙/网络问题都可能导致 read index 请求时间过长。

- 处理方法：

    可能 TiKV 集群分裂/迁移频繁，导致频繁重试，可以查看 TiKV 集群状态确认。

## `TiFlash_raft_wait_index_duration`

- 报警规则：

    `histogram_quantile(0.99, sum(rate(tiflash_raft_wait_index_duration_seconds_bucket[1m])) BY (le, instance)) > 2`

- 规则描述：

    TiFlash 等待 Region Raft Index 的时间超过 2 秒的概率超过 99% 时报警。

- 处理方法：

    可能 TiKV 和 Proxy 的通信出现问题，联系 TiFlash 开发人员确认。
