---
title: TiCDC Alert Rules
summary: Learn about TiCDC alert rules and how to handle the alerts.
---
# TiCDC Alert Rules

This document describes the TiCDC alert rules and the corresponding solutions. In descending order, the severity levels are: **Critical**, **Warning**.

## Critical alerts

This section introduces critical alerts and solutions.

### `cdc_checkpoint_high_delay`

For critical alerts, you need to pay close attention to abnormal monitoring metrics.

- Alert rule:

    (time() - ticdc_processor_checkpoint_ts / 1000) > 600

- Description:

    A replication task is delayed more than 10 minutes.

- Solution:

    See [TiCDC Handle Replication Interruption](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions).

## `cdc_resolvedts_high_delay`

- Alert rule:

    (time() - ticdc_processor_resolved_ts / 1000) > 300

- Description:

     The Resolved TS of a replication task is delayed more than 5 minutes.

- Solution:

    See [TiCDC Handle Replication Interruption](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions).

### `ticdc_processor_exit_with_error_count`

- Alert rule:

    `changes(ticdc_processor_exit_with_error_count[1m]) > 0`

- Description:

    A replication task reports an error and exits.

- Solution:

    See [TiCDC Handle Replication Interruption](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions).

## Warning alerts

Warning alerts are a reminder for an issue or error.

### `cdc_multiple_owners`

- Alert rule:

    `sum(rate(ticdc_owner_ownership_counter[30s])) >= 2`

- Description:

    There are multiple owners in the TiCDC cluster.

- Solution:

    Collect TiCDC logs to locate the root cause.

### `ticdc_mounter_unmarshal_and_mount_time_more_than_1s`

- Alert rule:

`histogram_quantile(0.9, rate(ticdc_mounter_unmarshal_and_mount_bucket[1m])) * 1000 > 1000`

- Description:

    It takes a replication task more than 1 second to unmarshal the data changes.

- Solution:

    Collect TiCDC logs to locate the root cause.

### `cdc_sink_execute_duration_time_more_than_10s`

- Alert rule:

    `histogram_quantile(0.9, rate(ticdc_sink_txn_exec_duration_bucket[1m])) > 10`

- Description:

    It takes a replication task more than 10 seconds to write data to the downstream database.

- Solution:

    Check whether there are problems in the downstream database.

### `cdc_processor_checkpoint_tso_no_change_for_1m`

- Alert rule:

    `changes(ticdc_processor_checkpoint_ts[1m]) < 1`

- Description:

    A replication task has not advanced for more than 1 minute.

- Solution:

    See [TiCDC Handle Replication Interruption](/ticdc/troubleshoot-ticdc.md#how-do-i-handle-replication-interruptions).

### `ticdc_puller_entry_sorter_sort_bucket`

- Alert rule:

    `histogram_quantile(0.9, rate(ticdc_puller_entry_sorter_sort_bucket{}[1m])) > 1`

- Description:

    The delay of TiCDC puller entry sorter is too high.

- Solution:

    Collect TiCDC logs to locate the root cause.

### `ticdc_puller_entry_sorter_merge_bucket`

- Alert rule:

    `histogram_quantile(0.9, rate(ticdc_puller_entry_sorter_merge_bucket{}[1m])) > 1`

- Description:

    The delay of TiCDC puller entry sorter merge is too high.

- Solution:

    Collect TiCDC logs to locate the root cause.

### `tikv_cdc_min_resolved_ts_no_change_for_1m`

- Alert rule:

    `changes(tikv_cdc_min_resolved_ts[1m]) < 1 and ON (instance) tikv_cdc_region_resolve_status{status="resolved"} > 0`

- Description:

    The minimum Resolved TS 1 of TiKV CDC has not advanced for 1 minute.

- Solution:

    Collect TiKV logs to locate the root cause.

### `tikv_cdc_scan_duration_seconds_more_than_10min`

- Alert rule:

    `histogram_quantile(0.9, rate(tikv_cdc_scan_duration_seconds_bucket{}[1m])) > 600`

- Description:

    The TiKV CDC module has scanned for incremental replication for more than 10 minutes.

- Solution:

    Collect TiCDC monitoring metrics and TiKV logs to locate the root cause.

### `ticdc_sink_mysql_execution_error`

- Alert rule:

    `changes(ticdc_sink_mysql_execution_error[1m]) > 0`

- Description:

    An error occurs when a replication task writes data to the downstream MySQL.

- Solution:

    There are many possible root causes. See [Troubleshoot TiCDC](/ticdc/troubleshoot-ticdc.md).

### `ticdc_memory_abnormal`

- Alert rule:

    `go_memstats_heap_alloc_bytes{job="ticdc"} > 1e+10`

- Description:

    The TiCDC heap memory usage exceeds 10 GiB.

- Solution:

    Collect TiCDC logs to locate the root cause.