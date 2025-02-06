---
title: TiCDC 集群监控报警规则
summary: 了解 TiCDC 集群监控报警规则以及处理方法。
---

# TiCDC 集群监控报警规则

本文介绍了 TiCDC 组件的报警项及相应的报警规则。根据严重级别，报警项按照严重程度由高到低依次为：重要级别 (Critical)、警告级别 (Warning)。

## 重要级别报警项

对于重要级别的报警，需要密切关注异常指标。

### `cdc_checkpoint_high_delay`

* 报警规则：

    `ticdc_owner_checkpoint_ts_lag > 600`

* 规则描述：

    TiCDC 某个同步任务延迟超过 10 分钟。

* 处理方法：

    参考 [TiCDC 同步任务出现中断](/ticdc/troubleshoot-ticdc.md#ticdc-同步任务出现中断)的处理方法。

### `cdc_resolvedts_high_delay`

* 报警规则：

    `ticdc_owner_resolved_ts_lag > 300`

* 规则描述：

    TiCDC 某个同步任务的 resolved ts 延迟超过 5 分钟。

* 处理方法：

    该告警与同步任务中断类似，可参考 [TiCDC 同步任务出现中断](/ticdc/troubleshoot-ticdc.md#ticdc-同步任务出现中断)的处理方法。

### `ticdc_changefeed_failed`

* 报警规则：

    `(max_over_time(ticdc_owner_status[1m]) == 2) > 0`

* 规则描述：

    TiCDC 某个同步任务遇到无法自动恢复的错误，进入 failed 状态。

* 处理方法：

    该告警与同步任务中断类似，可参考 [TiCDC 同步任务出现中断](/ticdc/troubleshoot-ticdc.md#ticdc-同步任务出现中断)的处理方法。

## 警告级别报警项

警告级别的报警是对某一问题或错误的提醒。

### `cdc_multiple_owners`

* 报警规则：

    `sum(rate(ticdc_owner_ownership_counter[30s])) >= 2`

* 规则描述：

    TiCDC 集群有多个 owner。

* 处理方法：

    收集 TiCDC 日志，定位原因。

### `cdc_no_owner`

* 报警规则：

    `sum(rate(ticdc_owner_ownership_counter[240s])) < 0.5`

* 规则描述：
    
    TiCDC 集群超过 10 分钟没有 owner。

* 处理方法：

    收集 TiCDC 日志，定位原因。

### `ticdc_changefeed_meet_error`

* 报警规则：

    `(max_over_time(ticdc_owner_status[1m]) == 1 or max_over_time(ticdc_owner_status[1m]) == 6) > 0`

* 规则描述：

    TiCDC 某个同步任务遇到错误。

* 处理方法：

    参考 [TiCDC 同步任务出现中断](/ticdc/troubleshoot-ticdc.md#ticdc-同步任务出现中断)的处理方法。

### `ticdc_processor_exit_with_error_count`

* 报警规则：

    `changes(ticdc_processor_exit_with_error_count[1m]) > 0`

* 规则描述：

    TiCDC 某个同步任务报错退出。

* 处理方法：

    参考 [TiCDC 同步任务出现中断](/ticdc/troubleshoot-ticdc.md#ticdc-同步任务出现中断)的处理方法。

### `tikv_cdc_min_resolved_ts_no_change_for_1m`

* 报警规则：

    `changes(tikv_cdc_min_resolved_ts[1m]) < 1 and ON (instance) tikv_cdc_region_resolve_status{status="resolved"} > 0 and ON (instance) tikv_cdc_captured_region_total > 0`

* 规则描述：

    TiKV CDC 模块最小的 resolved ts 1 分钟没推进。

* 处理方法：

    收集 TiKV 日志，定位原因。

### `tikv_cdc_scan_duration_seconds_more_than_10min`

* 报警规则：

    `histogram_quantile(0.9, rate(tikv_cdc_scan_duration_seconds_bucket{}[1m])) > 600`

* 规则描述：

    TiKV CDC 模块的增量扫描耗时超过 10 分钟。

* 处理方法：

    收集 TiCDC 监控和 TiKV 日志，定位原因。

### `ticdc_sink_execution_error`

* 报警规则：

    `changes(ticdc_sink_execution_error[1m]) > 0`

* 规则描述：

    TiCDC 某一同步任务写下游时遇到错误。

* 处理方法：

    MySQL 报错的情况较多，参考 [TiCDC 故障处理](/ticdc/troubleshoot-ticdc.md)。

### `ticdc_memory_abnormal`

* 报警规则：

    `go_memstats_heap_alloc_bytes{job="ticdc"} > 1e+10`

* 规则描述：

    TiCDC 堆内存使用量超过 10 GiB。

* 处理方法：

    收集 TiCDC 日志，定位原因。
