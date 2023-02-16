---
title: TiFlash Alert Rules
summary: Learn the alert rules of the TiFlash cluster.
aliases: ['/docs/dev/tiflash/tiflash-alert-rules/','/docs/dev/reference/tiflash/alert-rules/']
---

# TiFlash Alert Rules

This document introduces the alert rules of the TiFlash cluster.

## `TiFlash_schema_error`

- Alert rule:

    `increase(tiflash_schema_apply_count{type="failed"}[15m]) > 0`

- Description:

    When the schema apply error occurs, an alert is triggered.

- Solution:

    The error might be caused by some wrong logic. [Get support](/support.md) from PingCAP or the community.

## `TiFlash_schema_apply_duration`

- Alert rule:

    `histogram_quantile(0.99, sum(rate(tiflash_schema_apply_duration_seconds_bucket[1m])) BY (le, instance)) > 20`

- Description:

    When the probability that the apply duration exceeds 20 seconds is over 99%, an alert is triggered.

- Solution:

    It might be caused by the internal problems of the TiFlash storage engine. [Get support](/support.md) from PingCAP or the community.

## `TiFlash_raft_read_index_duration`

- Alert rule:

    `histogram_quantile(0.99, sum(rate(tiflash_raft_read_index_duration_seconds_bucket[1m])) BY (le, instance)) > 3`

- Description:

    When the probability that the read index duration exceeds 3 seconds is over 99%, an alert is triggered.

    > **Note:**
    >
    > `read index` is the kvproto request sent to the TiKV leader. TiKV region retries, busy store, or network problems might lead to long request time of `read index`.

- Solution:

    The frequent retries might be caused by frequent splitting or migration of the TiKV cluster. You can check the TiKV cluster status to identify the retry reason.

## `TiFlash_raft_wait_index_duration`

- Alert rule:

    `histogram_quantile(0.99, sum(rate(tiflash_raft_wait_index_duration_seconds_bucket[1m])) BY (le, instance)) > 2`

- Description:

    When the probability that the waiting time for Region Raft Index in TiFlash exceeds 2 seconds is over 99%, an alert is triggered.

- Solution:

    It might be caused by a communication error between TiKV and the proxy. [Get support](/support.md) from PingCAP or the community.
