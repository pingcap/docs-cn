---
title: TiCDC 集群监控报警
---

# TiCDC 集群监控报警

本文介绍了 TiCDC 组件的报警项及相应的报警规则。根据严重级别，报警项按照严重程度由高到低依次为：重要级别 (Critical)、警告级别 (Warning)。

## 监控报警规则

### 重要级别报警项

对于重要级别的报警，需要密切关注异常指标。

#### `cdc_checkpoint_high_delay`

* 报警规则：

    (time() - ticdc_processor_checkpoint_ts / 1000) > 600

* 规则描述：

    cdc processor checkpoint延迟超过10分钟。

* 处理方法：


#### `cdc_resolvedts_high_delay`

* 报警规则：

    (time() - ticdc_processor_resolved_ts / 1000) > 300

* 规则描述：

    cdc processor resolved ts延迟超过5分钟。

* 处理方法：

#### `ticdc_processor_exit_with_error_count`

* 报警规则：

    `changes(ticdc_processor_exit_with_error_count[1m]) > 0`

* 规则描述：

    cdc processor异常退出。

* 处理方法：


### 警告级别报警项

警告级别的报警是对某一问题或错误的提醒。

#### `cdc_multiple_owners`

* 报警规则：
    
    `sum(rate(ticdc_owner_ownership_counter[30s])) >= 2`

* 规则描述：

    TiCDC集群有多个owner。

* 处理方法：


#### `ticdc_mounter_unmarshal_and_mount_time_more_than_1s`

* 报警规则：

    `histogram_quantile(0.9, rate(ticdc_mounter_unmarshal_and_mount_bucket[1m])) * 1000 > 1000`

* 规则描述：

    cdc_mounter unmarshall跟mount的时间超过1秒。

* 处理方法：


#### `cdc_sink_execute_duration_time_more_than_10s`

* 报警规则：

    `histogram_quantile(0.9, rate(ticdc_sink_txn_exec_duration_bucket[1m])) > 10`

* 规则描述：

    cdc sink操作执行时间超过10s。

* 处理方法：


#### `cdc_processor_checkpoint_tso_no_change_for_1m`

* 报警规则：

    `changes(ticdc_processor_checkpoint_ts[1m]) < 1`

* 规则描述：

    cdc processor checkpoint时间戳1分钟没有推进。

* 处理方法：


#### `ticdc_puller_entry_sorter_sort_bucket`

* 报警规则：

    `histogram_quantile(0.9, rate(ticdc_puller_entry_sorter_sort_bucket{}[1m])) > 1`

* 规则描述：

    ticdc puller entry sorter排序延迟太高。

* 处理方法：


#### `ticdc_puller_entry_sorter_merge_bucket`

* 报警规则：

    `histogram_quantile(0.9, rate(ticdc_puller_entry_sorter_merge_bucket{}[1m])) > 1`

* 规则描述：

    ticdc puller entry sorter merge延迟太高。

* 处理方法：


#### `tikv_cdc_min_resolved_ts_no_change_for_1m`

* 报警规则：

    `changes(tikv_cdc_min_resolved_ts[1m]) < 1 and ON (instance) tikv_cdc_region_resolve_status{status="resolved"} > 0`

* 规则描述：

    tikv cdc最小的resolved ts 1分钟没推进。

* 处理方法：


#### `tikv_cdc_scan_duration_seconds_more_than_10min`

* 报警规则：

    `histogram_quantile(0.9, rate(tikv_cdc_scan_duration_seconds_bucket{}[1m])) > 600`

* 规则描述：

    tikv cdc扫描耗时超过10分钟。

* 处理方法：


#### `ticdc_sink_mysql_execution_error`

* 报警规则：

    `changes(ticdc_sink_mysql_execution_error[1m]) > 0`

* 规则描述：

    cdc sink到下游mysql时遇到错误。

* 处理方法：


#### `ticdc_memory_abnormal`

* 报警规则：

    `go_memstats_heap_alloc_bytes{job="ticdc"} > 1e+10`

* 规则描述：

    TiCDC 堆内存使用量超过10GB。
    
* 处理方法：
