---
title: TiDB Cluster Alert Rules
summary: Learn the alert rules in a TiDB cluster.
category: reference
---

<!-- markdownlint-disable MD024 -->

# TiDB Cluster Alert Rules

This document describes the alert rules for different components in a TiDB cluster, including the rule descriptions and solutions of the alert items in TiDB, TiKV, PD, TiDB Binlog, Node_exporter and Blackbox_exporter.

According to the severity level, alert rules are divided into three categories (from high to low): emergency-level, critical-level and warning-level.

## TiDB alert rules

This section gives the alert rules for the TiDB component.

### Emergency-level alerts

Emergency-level alerts are often caused by a service or node failure. Manual intervention is required immediately.

#### `TiDB_schema_error`

* Alert rule:

    `increase(tidb_session_schema_lease_error_total{type="outdated"}[15m]) > 0`

* Description:

    The latest schema information is not reloaded in TiDB within one lease. When TiDB fails to continue providing services, an alert is triggered.

* Solution:

    It is often caused by an unavailable Region or a TiKV timeout. You need to locate the issue by checking the TiKV monitoring items.

#### `TiDB_tikvclient_region_err_total`

* Alert rule:

    `increase(tidb_tikvclient_region_err_total[10m]) > 6000`

* Description:

    When TiDB accesses TiKV, a Region error occurs. When the error is reported over 6000 times in 10 minutes, an alert is triggered.

* Solution:

    View the monitoring status of TiKV.

#### `TiDB_domain_load_schema_total`

* Alert rule:

    `increase(tidb_domain_load_schema_total{type="failed"}[10m]) > 10`

* Description:

    The total number of failures to reload the latest schema information in TiDB. If the reloading failure occurs over 10 times in 10 minutes, an alert is triggered.

* Solution:

    Same as [`TiDB_schema_error`](#tidb-schema-error).

#### `TiDB_monitor_keep_alive`

* Alert rule:

    `increase(tidb_monitor_keep_alive_total[10m]) < 100`

* Description:

    Indicates whether the TiDB process still exists. If the number of times for `tidb_monitor_keep_alive_total` increases less than 100 in 10 minutes, the TiDB process might already exit and an alert is triggered.

* Solution:

    * Check whether the TiDB process is out of memory.
    * Check whether the machine has restarted.

### Critical-level alerts

For the critical-level alerts, a close watch on the abnormal metrics is required.

#### `TiDB_server_panic_total`

* Alert rule:

    `increase(tidb_server_panic_total[10m]) > 0`

* Description:

    The number of panicked TiDB threads. When a panic occurs, an alert is triggered. The thread is often recovered, otherwise, TiDB will frequently restart.

* Solution:

    Collect the panic logs to locate the issue.

### Warning-level alerts

Warning-level alerts are a reminder for an issue or error.

#### `TiDB_memory_abnormal`

* Alert rule:

    `go_memstats_heap_inuse_bytes{job="tidb"} > 1e+10`

* Description:

    The monitoring on the TiDB memory usage. If the usage exceeds 10 G, an alert is triggered.

* Solution:

    Use the HTTP API to troubleshoot the goroutine leak issue.

#### `TiDB_query_duration`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tidb_server_handle_query_duration_seconds_bucket[1m])) BY (le, instance)) > 1`

* Description:

    The latency of handling a request in TiDB. If the 99th percentile latency exceeds 1 second, an alert is triggered.

* Solution:

    View TiDB logs and search for the `SLOW_QUERY` and `TIME_COP_PROCESS` keywords to locate the slow SQL queries.

#### `TiDB_server_event_error`

* Alert rule:

    `increase(tidb_server_server_event{type=~"server_start|server_hang"}[15m]) > 0`

* Description:

    The number of events that happen in the TiDB service. An alert is triggered when the following events happen:

    1. start: The TiDB service starts.
    2. hang: When a critical-level event (currently there is only one scenario: TiDB cannot write binlog) happens, TiDB enters the `hang` mode and waits to be killed manually.

* Solution:

    * Restart TiDB to recover the service.
    * Check whether the TiDB Binlog service is normal.

#### `TiDB_tikvclient_backoff_count`

* Alert rule:

    `increase(tidb_tikvclient_backoff_count[10m]) > 10`

* Description:

    The number of retries when TiDB fails to access TiKV. When the retry times is over 10 in 10 minutes, an alert is triggered.

* Solution:

    View the monitoring status of TiKV.

#### `TiDB_monitor_time_jump_back_error`

* Alert rule:

    `increase(tidb_monitor_time_jump_back_total[10m]) > 0`

* Description:

    When the time of the machine that holds TiDB rewinds, an alert is triggered.

* Solution:

    Troubleshoot the NTP configurations.

#### `TiDB_ddl_waiting_jobs`

* Alert rule:

    `sum(tidb_ddl_waiting_jobs) > 5`

* Description:

    When the number of DDL tasks pending for execution in TiDB exceeds 5, an alert is triggered.

* Solution:

    Check whether there is any time-consuming `add index` operation that is being executed by running `admin show ddl`.

## PD alert rules

This section gives the alert rules for the PD component.

### Emergency-level alerts

Emergency-level alerts are often caused by a service or node failure. Manual intervention is required immediately.

#### `PD_cluster_offline_tikv_nums`

* Alert rule:

    `sum(pd_cluster_status{type="store_down_count"}) > 0`

* Description:

    PD has not received a TiKV heartbeat for a long time (the default configuration is 30 minutes).

* Solution:

    * Check whether the TiKV process is normal, the network is isolated or the load is too high, and recover the service as much as possible.
    * If the TiKV instance cannot be recovered, you can make it offline.

### Critical-level alerts

For the critical-level alerts, a close watch on the abnormal metrics is required.

#### `PD_etcd_write_disk_latency`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(etcd_disk_wal_fsync_duration_seconds_bucket[1m])) by (instance,job,le)) > 1`

* Description:

    etcd writes data to disk at a lower speed than normal. It might lead to PD leader timeout or failure to store TSO on disk in time, which will shut down the service of the entire cluster.

* Solution:

    * Find the cause of slow writes. It might be other services that overload the system. You can check whether PD itself occupies a large amount of CPU or I/O resources.
    * Try to restart PD or manually transfer leader to another PD to recover the service.
    * If the problematic PD instance cannot be recovered due to environmental factors, make it offline and replace it.

#### `PD_miss_peer_region_count`

* Alert rule:

    `sum(pd_regions_status{type="miss_peer_region_count"}) > 100`

* Description:

    The number of Region replicas is smaller than the value of `max-replicas`. When a TiKV machine is down and its downtime exceeds `max-down-time`, it usually leads to missing replicas for some Regions during a period of time. When a TiKV node is made offline, it might result in a small number of Regions with missing replicas.

* Solution:

    * Find the cause of the issue by checking whether there is any TiKV machine that is down or being made offline.
    * Watch the Region health panel and see whether `miss_peer_region_count` is continuously decreasing.

### Warning-level alerts

Warning-level alerts are a reminder for an issue or error.

#### `PD_cluster_lost_connect_tikv_nums`

* Alert rule:

    `sum(pd_cluster_status{type="store_disconnected_count"}) > 0`

* Description:

    PD does not receive a TiKV heartbeat within 20 seconds. Normally a TiKV heartbeat comes in every 10 seconds.

* Solution:

    * Check whether the TiKV instance is being restarted.
    * Check whether the TiKV process is normal, the network is isolated, and the load is too high, and recover the service as much as possible.
    * If you confirm that the TiKV instance cannot be recovered, you can make it offline.
    * If you confirm that the TiKV instance can be recovered, but not in the short term, you can consider increasing the value of `max-down-time`. It will prevent the TiKV instance from being considered as irrecoverable and the data from being removed from the TiKV.

#### `PD_cluster_low_space`

* Alert rule:

    `sum(pd_cluster_status{type="store_low_space_count"}) > 0`

* Description:

    Indicates that there is no sufficient space on the TiKV node.

* Solution:

    * Check whether the space in the cluster is generally insufficient. If so, increase its capacity.
    * Check whether there is any issue with Region balance scheduling. If so, it will lead to uneven data distribution.
    * Check whether there is any file that occupies a large amount of disk space, such as the log, snapshot, core dump, etc.
    * Lower the Region weight of the node to reduce the data volume.
    * When it is not possible to release the space, consider proactively making the node offline. This prevents insufficient disk space that leads to downtime.

#### `PD_etcd_network_peer_latency`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(etcd_network_peer_round_trip_time_seconds_bucket[1m])) by (To,instance,job,le)) > 1`

* Description:

    The network latency between PD nodes is high. It might lead to the leader timeout and TSO disk storage timeout, which impacts the service of the cluster.

* Solution:

    * Check the network and system load status.
    * If the problematic PD instance cannot be recovered due to environmental factors, make it offline and replace it.

#### `PD_tidb_handle_requests_duration`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(pd_client_request_handle_requests_duration_seconds_bucket{type="tso"}[1m])) by (instance,job,le)) > 0.1`

* Description:

    It takes a longer time for PD to handle the TSO request. It is often caused by a high load.

* Solution:

    * Check the load status of the server.
    * Use pprof to analyze the CPU profile of PD.
    * Manually switch the PD leader.
    * If the problematic PD instance cannot be recovered due to environmental factors, make it offline and replace it.

#### `PD_down_peer_region_nums`

* Alert rule:

    `sum(pd_regions_status{type="down_peer_region_count"}) > 0`

* Description:

    The number of Regions with an unresponsive peer reported by the Raft leader.

* Solution:

    * Check whether there is any TiKV that is down, or that was just restarted, or that is busy.
    * Watch the Region health panel and see whether `down_peer_region_count` is continuously decreasing.
    * Check the network between TiKV servers.

#### `PD_pending_peer_region_count`

* Alert rule:

    `sum(pd_regions_status{type="pending_peer_region_count"}) > 100`

* Description:

    There are too many Regions that have lagged Raft logs. It is normal that scheduling leads to a small number of pending peers, but if the number remains high, there might be an issue.

* Solution:

    * Watch the Region health panel and see whether `pending_peer_region_count` is continuously decreasing.
    * Check the network between TiKV servers, especially whether there is enough bandwidth.

#### `PD_leader_change`

* Alert rule:

    `count(changes(pd_server_tso{type="save"}[10m]) > 0) >= 2`

* Description:

    The PD leader is recently switched.

* Solution:

    * Exclude the human factors, such as restarting PD, manually transferring leader, adjusting leader priority, etc.
    * Check the network and system load status.
    * If the problematic PD instance cannot be recovered due to environmental factors, make it offline and replace it.

#### `TiKV_space_used_more_than_80%`

* Alert rule:

    `sum(pd_cluster_status{type="storage_size"}) / sum(pd_cluster_status{type="storage_capacity"}) * 100 > 80`

* Description:

    Over 80% of the cluster space is occupied.

* Solution:

    * Check whether it is needed to increase capacity.
    * Check whether there is any file that occupies a large amount of disk space, such as the log, snapshot, core dump, etc.

#### `PD_system_time_slow`

* Alert rule:

    `changes(pd_server_tso{type="system_time_slow"}[10m]) >= 1`

* Description:

    The system time rewind might happen.

* Solution:

    Check whether the system time is configured correctly.

#### `PD_no_store_for_making_replica`

* Alert rule:

    `increase(pd_checker_event_count{type="replica_checker", name="no_target_store"}[1m]) > 0`

* Description:

    There is no appropriate store for additional replicas.

* Solution:

    * Check whether there is enough space in the store.
    * Check whether there is any store for additional replicas according to the label configuration if it is configured.

## TiKV alert rules

This section gives the alert rules for the TiKV component.

### Emergency-level alerts

Emergency-level alerts are often caused by a service or node failure. Manual intervention is required immediately.

#### `TiKV_memory_used_too_fast`

* Alert rule:

    `process_resident_memory_bytes{job=~"tikv",instance=~".*"} - (process_resident_memory_bytes{job=~"tikv",instance=~".*"} offset 5m) > 5*1024*1024*1024`

* Description:

    Currently, there are no TiKV monitoring items about memory. You can monitor the memory usage of the machines in the cluster by Node_exporter. The above rule indicates that when the memory usage exceeds 5 GB within 5 minutes (the memory is occupied too fast in TiKV), an alert is triggered.

* Solution:

    Adjust the `block-cache-size` value of both `rockdb.defaultcf` and `rocksdb.writecf`.

#### `TiKV_GC_can_not_work`

* Alert rule:

    `sum(increase(tidb_tikvclient_gc_action_result{type="success"}[6h])) < 1`

* Description:

    GC is not performed successfully in a Region within 6 hours, which indicates that GC is not working properly. If GC does not run in a short term, it will not cause much trouble; but if GC keeps down, more and more versions are retained, which slows down the query.

* Solution:

    1. Perform `select VARIABLE_VALUE from mysql.tidb where VARIABLE_NAME = "tikv_gc_leader_desc"` to locate the `tidb-server` corresponding to the GC leader;
    2. View the log of the `tidb-server`, and grep gc_worker tidb.log;
    3. If you find that the GC worker has been resolving locks (the last log is "start resolve locks") or deleting ranges (the last log is “start delete {number} ranges”) during this time, it means the GC process is running normally. Otherwise, contact [support@pingcap.com](mailto:support@pingcap.com) to resolve this issue.

### Critical-level alerts

For the critical-level alerts, a close watch on the abnormal metrics is required.

#### `TiKV_server_report_failure_msg_total`

* Alert rule:

    `sum(rate(tikv_server_report_failure_msg_total{type="unreachable"}[10m])) BY (store_id) > 10`

* Description:

    Indicates that the remote TiKV cannot be connected.

* Solution:

    1. Check whether the network is clear.
    2. Check whether the remote TiKV is down.
    3. If the remote TiKV is not down, check whether the pressure is too high. Refer to the solution in [`TiKV_channel_full_total`](#tikv-channel-full-total).

#### `TiKV_channel_full_total`

* Alert rule:

    `sum(rate(tikv_channel_full_total[10m])) BY (type, instance) > 0`

* Description:

    This issue is often caused by the stuck Raftstore thread and high pressure on TiKV.

* Solution:

    1. Watch the Raft Propose monitor, and see whether the alerted TiKV node has a much higher Raft propose than other TiKV nodes. If so, it means that there are one or more hot spots on this TiKV. You need to check whether the hot spot scheduling can work properly.
    2. Watch the Raft I/O monitor, and see whether the latency increases. If the latency is high, it means a bottleneck might exist in the disk. One feasible but unsafe solution is setting `sync-log` to `false`.
    3. Watch the Raft Process monitor, and see whether the tick duration is high. If so, you need to add `raft-base-tick-interval = "2s"` under the `[raftstore]` configuration.

#### `TiKV_write_stall`

* Alert rule:

    `delta(tikv_engine_write_stall[10m]) > 0`

* Description:

    The write pressure on RocksDB is too high, and a stall occurs.

* Solution:

    1. View the disk monitor, and troubleshoot the disk issues;
    2. Check whether there is any write hot spot on the TiKV;
    3. Set `max-sub-compactions` to a larger value under the `[rocksdb]` and `[raftdb]` configurations.

#### `TiKV_raft_log_lag`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_log_lag_bucket[1m])) by (le, instance)) > 5000`

* Description:

    If this value is relatively large, it means Follower has lagged far behind Leader, and Raft cannot be replicated normally. It is possibly because the TiKV machine where Follower is located is stuck or down.

#### `TiKV_async_request_snapshot_duration_seconds`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="snapshot"}[1m])) by (le, instance, type)) > 1`

* Description:

    If this value is relatively large, it means the load pressure on Raftstore is too high, and it might be stuck already.

* Solution:

    Refer to the solution in [`TiKV_channel_full_total`](#tikv-channel-full-total).

#### `TiKV_async_request_write_duration_seconds`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tikv_storage_engine_async_request_duration_seconds_bucket{type="write"}[1m])) by (le, instance, type)) > 1`

* Description:

    If this value is relatively large, it means the Raft write takes a long time.

* Solution:

    1. Check the pressure on Raftstore. See the solution in [`TiKV_channel_full_total`](#tikv-channel-full-total).
    2. Check the pressure on the apply worker thread.

#### `TiKV_coprocessor_request_wait_seconds`

* Alert rule:

    `histogram_quantile(0.9999, sum(rate(tikv_coprocessor_request_wait_seconds_bucket[1m])) by (le, instance, req)) > 10`

* Description:

    If this value is relatively large, it means the pressure on the Coprocessor worker is high. There might be a slow task that makes the Coprocessor thread stuck.

* Solution:

    1. View the slow query log from the TiDB log to see whether the index or full table scan is used in a query, or see whether it is needed to analyze;
    2. Check whether there is a hot spot;
    3. View the Coprocessor monitor and see whether `total` and `process` in `coprocessor table/index scan` match. If they differ a lot, it indicates too many invalid queries are performed. You can see whether there is `over seek bound`. If so, there are too many versions that GC does not handle in time. Then you need to increase the number of parallel GC threads.

#### `TiKV_raftstore_thread_cpu_seconds_total`

* Alert rule:

    `sum(rate(tikv_thread_cpu_seconds_total{name=~"raftstore_.*"}[1m])) by (instance, name) > 1.6`

* Description:

    The pressure on the Raftstore thread is too high.

* Solution:

    Refer to the solution in [`TiKV_channel_full_total`](#tikv-channel-full-total).

#### `TiKV_raft_append_log_duration_secs`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_append_log_duration_seconds_bucket[1m])) by (le, instance)) > 1`

* Description:

    Indicates the time cost of appending Raft log. If it is high, it usually means I/O is too busy.

#### `TiKV_raft_apply_log_duration_secs`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_apply_log_duration_seconds_bucket[1m])) by (le, instance)) > 1`

* Description:

    Indicates the time cost of applying Raft log. If it is high, it usually means I/O is too busy.

#### `TiKV_scheduler_latch_wait_duration_seconds`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tikv_scheduler_latch_wait_duration_seconds_bucket[1m])) by (le, instance, type)) > 1`

* Description:

    The waiting time for the write operations to obtain the memory lock in Scheduler. If it is high, there might be many write conflicts, or that some operations that lead to conflicts take a long time to finish and block other operations that wait for the same lock.

* Solution:

    1. View the scheduler command duration in the Scheduler-All monitor and see which command is most time-consuming;
    2. View the scheduler scan details in the Scheduler-All monitor and see whether `total` and `process` match. If they differ a lot, there are many invalid scans. You can also see whether there is `over seek bound`. If there is too much, it indicates GC does not work in time;
    3. View the storage async snapshot/write duration in the Storage monitor and see whether the Raft operation is performed in time.

#### `TiKV_thread_apply_worker_cpu_seconds`

* Alert rule:

    `sum(rate(tikv_thread_cpu_seconds_total{name="apply_worker"}[1m])) by (instance) > 1.8`

* Description:

    The pressure on the apply Raft log thread is too high. It is often caused by a burst of writes.

#### `TiDB_tikvclient_gc_action_fail` (only happen when in special configurations)

* Alert rule:

    `sum(increase(tidb_tikvclient_gc_action_result{type="fail”}[1m])) > 10`

* Description:

    There are many Regions where GC fails to work.

* Solution:

    1. It is normally because the GC concurrency is set too high. You can moderately lower the GC concurrency degree, and you need to first confirm that the failed GC is caused by the busy server.
    2. You can moderately lower the concurrency degree by running `update set VARIABLE_VALUE="{number}” where VARIABLE_NAME=”tikv_gc_concurrency”`.

### Warning-level alerts

Warning-level alerts are a reminder for an issue or error.

#### `TiKV_leader_drops`

* Alert rule:

    `delta(tikv_pd_heartbeat_tick_total{type="leader"}[30s]) < -10`

* Description:

    It is often caused by a stuck Raftstore thread.

* Solution:

    1. Refer to [`TiKV_channel_full_total`](#tikv-channel-full-total).
    2. It there is low pressure on TiKV, consider whether the PD scheduling is too frequent. You can view the Operator Create panel on the PD page, and check the types and number of the PD scheduling.

#### `TiKV_raft_process_ready_duration_secs`

* Alert rule:

    `histogram_quantile(0.999, sum(rate(tikv_raftstore_raft_process_duration_secs_bucket{type='ready'}[1m])) by (le, instance, type)) > 2`

* Description:

    Indicates the time cost of handling Raft ready. If this value is large, it is often caused by the stuck appending log task.

#### `TiKV_raft_process_tick_duration_secs`

* Alert rule:

    `histogram_quantile(0.999, sum(rate(tikv_raftstore_raft_process_duration_secs_bucket{type=’tick’}[1m])) by (le, instance, type)) > 2`

* Description:

    Indicates the time cost of handling Raft tick. If this value is large, it is often caused by too many Regions.

* Solution:

    1. Consider using a higher-level log such as `warn` or `error`.
    2. Add `raft-base-tick-interval = "2s"` under the `[raftstore]` configuration.

#### `TiKV_scheduler_context_total`

* Alert rule:

    `abs(delta( tikv_scheduler_context_total[5m])) > 1000`

* Description:

    The number of write commands that are being executed by Scheduler. If this value is large, it means the task is not finished timely.

* Solution:

    Refer to [`TiKV_scheduler_latch_wait_duration_seconds`](#tikv-scheduler-latch-wait-duration-seconds).

#### `TiKV_scheduler_command_duration_seconds`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tikv_scheduler_command_duration_seconds_bucket[1m])) by (le, instance, type)  / 1000) > 1`

* Description:

    Indicates the time cost of executing the Scheduler command.

* Solution:

    Refer to [`TiKV_scheduler_latch_wait_duration_seconds`](#tikv-scheduler-latch-wait-duration-seconds).

#### `TiKV_coprocessor_outdated_request_wait_seconds`

* Alert rule:

    `delta(tikv_coprocessor_outdated_request_wait_seconds_count[10m]) > 0`

* Description:

    The waiting time of the expired requests by Coprocessor. If this value is large, it means there is high pressure on Coprocessor.

* Solution:

    Refer to [`TiKV_coprocessor_request_wait_seconds`](#tikv-coprocessor-request-wait-seconds).

#### `TiKV_coprocessor_request_error`

* Alert rule:

    `increase(tikv_coprocessor_request_error{reason!="lock"}[10m]) > 100`

* Description:

    The request error of Coprocessor.

* Solution:

    The reasons for the Coprocessor error can be divided into three types: "lock", “outdated” and “full”. “outdated” indicates that the request has a timeout. It might be caused by a long queue time or a long time to handle a single request. “full” indicates that the request queue is full. It is possibly because the running request is time-consuming, which sends all new requests in the queue. You need to check whether the time-consuming query’s execution plan is correct.

#### `TiKV_coprocessor_request_lock_error`

* Alert rule:

    `increase(tikv_coprocessor_request_error{reason="lock"}[10m]) > 10000`

* Description:

    The lock requesting error of Coprocessor.

* Solution:

    The reasons for the Coprocessor error can be divided into three types: "lock", “outdated” and “full”. “lock” indicates that the read data is being written and you need to wait a while and read again (the automatic retry happens inside TiDB). If just a few errors of this kind occur, you can ignore them; but if there are a lot of them, you need to check whether there is a conflict between the write and the query.

#### `TiKV_coprocessor_pending_request`

* Alert rule:

    `delta(tikv_coprocessor_pending_request[10m]) > 5000`

* Description:

    The queuing requests of Coprocessor.

* Solution:

    Refer to [`TiKV_coprocessor_request_wait_seconds`](#tikv-coprocessor-request-wait-seconds).

#### `TiKV_batch_request_snapshot_nums`

* Alert rule:

    `sum(rate(tikv_thread_cpu_seconds_total{name=~"cop_.*"}[1m])) by (instance) / (count(tikv_thread_cpu_seconds_total{name=~"cop_.*"}) * 0.9) / count(count(tikv_thread_cpu_seconds_total) by (instance)) > 0`

* Description:

    The Coprocessor CPU usage of a TiKV machine exceeds 90%.

#### `TiKV_pending_task`

* Alert rule:

    `sum(tikv_worker_pending_task_total) BY (instance,name)  > 1000`

* Description:

    The number of pending tasks of TiKV.

* Solution:

    Check which kind of tasks has a higher value. You can normally find a solution to the Coprocessor and apply worker tasks from other metrics.

#### `TiKV_low_space_and_add_region`

* Alert rule:

    `count((sum(tikv_store_size_bytes{type="available"}) by (instance) / sum(tikv_store_size_bytes{type="capacity"}) by (instance) < 0.2) and (sum(tikv_raftstore_snapshot_traffic_total{type="applying"}) by (instance) > 0)) > 0`

#### `TiKV_approximate_region_size`

* Alert rule:

    `histogram_quantile(0.99, sum(rate(tikv_raftstore_region_size_bucket[1m])) by (le)) > 1073741824`

* Description:

    The maximum Region approximate size that is scanned by the TiKV split checker is continually larger than 1 GB within one minute.

* Solution:

    The speed of splitting Regions is slower than the write speed. To alleviate this issue, you’d better update TiDB to a version that supports batch-split (>= 2.1.0-rc1). If it is not possible to update temporarily, you can use `pd-ctl operator add split-region <region_id> --policy=approximate` to manually split Regions.

## TiDB Binlog alert rules

This section gives the alert rules for the TiDB Binlog component.

### Emergency-level alerts

Emergency-level alerts are often caused by a service or node failure. Manual intervention is required immediately.

#### `binlog_pump_storage_error_count`

* Alert rule:

    `changes(binlog_pump_storage_error_count[1m]) > 0`

* Description:

    Pump fails to write the binlog data to the local storage.

* Solution:

    Check whether an error exists in the `pump_storage_error` monitoring and check the Pump log to find the cause.

### Critical-level alerts

For the critical-level alerts, a close watch on the abnormal metrics is required.

#### `binlog_drainer_checkpoint_high_delay`

* Alert rule:

    `(time() - binlog_drainer_checkpoint_tso / 1000) > 3600`

* Description:

    The latency of the lagged drainer replication exceeds one hour.

* Solution:

    * Check whether it is too slow to obtain the data from Pump. You can check `handle tso` of Pump to get the time of the latest message for each Pump. Check whether any Pump with high latency exists, and make sure the corresponding Pump is running normally.
    * Check whether it is too slow to replicate data in the downstream based on Drainer `event` and Drainer `execute latency`.
        * If Drainer `execute time` is too large, check the network bandwidth and latency between the machine with Drainer deployed and the machine with the target database deployed, and the state of the target database.
        * If Drainer `execute time` is not too large and Drainer `event` is too small, add `work count` and `batch` and retry.
    * If the two solutions above cannot work, contact [support@pingcap.com](mailto:support@pingcap.com).

### Warning-level alerts

Warning-level alerts are a reminder for an issue or error.

#### `binlog_pump_write_binlog_rpc_duration_seconds_bucket`

* Alert rule:

    `histogram_quantile(0.9, rate(binlog_pump_rpc_duration_seconds_bucket{method="WriteBinlog"}[5m])) > 1`

* Description:

    It takes a long time for Pump to handle the TiDB request of writing binlog.

* Solution:

    * Verify the disk performance pressure and check the disk performance monitoring via `node exported`.
    * If both `disk latency` and `util` are low, contact [support@pingcap.com](mailto:support@pingcap.com).

#### `binlog_pump_storage_write_binlog_duration_time_bucket`

* Alert rule:

    `histogram_quantile(0.9, rate(binlog_pump_storage_write_binlog_duration_time_bucket{type="batch"}[5m])) > 1`

* Description:

    The time it takes for Pump to write the local binlog to the local disk.

* Solution:

    Check the status of the local disk of Pump and fix the issue.

#### `binlog_pump_storage_available_size_less_than_20G`

* Alert rule:

    `binlog_pump_storage_storage_size_bytes{type="available"} < 20 * 1024 * 1024 * 1024`

* Description:

    The available disk space of Pump is less than 20 G.

* Solution:

    Check whether Pump `gc_tso` is normal. If not, adjust the GC time of Pump or make the corresponding Pump offline.

#### `binlog_drainer_checkpoint_tso_no_change_for_1m`

* Alert rule:

    `changes(binlog_drainer_checkpoint_tso[1m]) < 1`

* Description:

    Drainer `checkpoint` has not been updated for one minute.

* Solution:

    Check whether all the Pumps that are not offline are running normally.

#### `binlog_drainer_execute_duration_time_more_than_10s`

* Alert rule:

    `histogram_quantile(0.9, rate(binlog_drainer_execute_duration_time_bucket[1m])) > 10`

* Description:

    The transaction time it takes Drainer to replicate data to TiDB. If it is too large, the Drainer replication of data is affected.

* Solution:

    * Check the TiDB cluster status.
    * Check the Drainer log or monitor. If a DDL operation causes this problem, you can ignore it.

## Node_exporter host alert rules

This section gives the alert rules for the Node_exporter host.

### Emergency-level alerts

Emergency-level alerts are often caused by a service or node failure. Manual intervention is required immediately.

#### `NODE_disk_used_more_than_80%`

* Alert rule:

    `node_filesystem_avail_bytes{fstype=~"(ext.|xfs)", mountpoint!~"/boot"} / node_filesystem_size_bytes{fstype=~"(ext.|xfs)", mountpoint!~"/boot"} * 100 <= 20`

* Description:

    The disk space usage of the machine exceeds 80%.

* Solution:

    * Log in to the machine, run the `df -h` command to check the disk space usage.
    * Make a plan to increase the disk capacity or delete some data or increase cluster node depending on different situations.

#### `NODE_disk_inode_more_than_80%`

* Alert rule:

    `node_filesystem_files_free{fstype=~"(ext.|xfs)"} / node_filesystem_files{fstype=~"(ext.|xfs)"} * 100 < 20`

* Description:

    The inode usage of the filesystem on the machine exceeds 80%.

* Solution:

    * Log in to the machine and run the `df -i` command to view the inode usage of the filesystem.
    * Make a plan to increase the disk capacity or delete some data or increase cluster node depending on different situations.

#### `NODE_disk_readonly`

* Alert rule:

    `node_filesystem_readonly{fstype=~"(ext.|xfs)"} == 1`

* Description:

    The filesystem is read-only and data cannot be written in it. It is often caused by disk failure or filesystem corruption.

* Solution:

    * Log in to the machine and create a file to test whether it is normal.
    * Check whether the disk LED is normal. If not, replace the disk and repair the filesystem of the machine.

### Critical-level alerts

For the critical-level alerts, a close watch on the abnormal metrics is required.

#### `NODE_memory_used_more_than_80%`

* Alert rule:

    `(((node_memory_MemTotal_bytes-node_memory_MemFree_bytes-node_memory_Cached_bytes)/(node_memory_MemTotal_bytes)*100)) >= 80`

* Description:

    The memory usage of the machine exceeds 80%.

* Solution:

    * View the Memory panel of the host in the Grafana Node Exporter dashboard, and see whether Used memory is too high and Available memory is too low.
    * Log in to the machine and run the `free -m` command to view the memory usage. You can run `top` to check whether there is any abnormal process that has an overly high memory usage.

### Warning-level alerts

Warning-level alerts are a reminder for an issue or error.

#### `NODE_node_overload`

* Alert rule:

    `(node_load5 / count without (cpu, mode) (node_cpu_seconds_total{mode="system"})) > 1`

* Description:

    The CPU load on the machine is relatively high.

* Solution:

    * View the CPU Usage and Load Average of the host in the Grafana Node Exporter dashboard to check whether they are too high.
    * Log in to the machine and run `top` to check the load average and the CPU usage, and see whether there is any abnormal process that has an overly high CPU usage.

#### `NODE_cpu_used_more_than_80%`

* Alert rule:

    `avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by(instance) * 100 <= 20`

* Description:

    The CPU usage of the machine exceeds 80%.

* Solution:

    * View the CPU Usage and Load Average of the host on the Grafana Node Exporter dashboard to check whether they are too high.
    * Log in to the machine and run `top` to check the Load Average and the CPU Usage, and see whether there is any abnormal process that has an overly high CPU usage.

#### `NODE_tcp_estab_num_more_than_50000`

* Alert rule:

    `node_netstat_Tcp_CurrEstab > 50000`

* Description:

    There are more than 50,000 TCP links in the "establish" status on the machine.

* Solution:

    * Log in to the machine and run `ss -s` to check the number of TCP links in the "estab" status in the current system.
    * Run `netstat` to check whether there is any abnormal link.

#### `NODE_disk_read_latency_more_than_32ms`

* Alert rule:

    `((rate(node_disk_read_time_seconds_total{device=~".+"}[5m]) / rate(node_disk_reads_completed_total{device=~".+"}[5m])) or (irate(node_disk_read_time_seconds_total{device=~".+"}[5m]) / irate(node_disk_reads_completed_total{device=~".+"}[5m])) ) * 1000 > 32`

* Description:

    The read latency of the disk exceeds 32 ms.

* Solution:

    * Check the disk status by viewing the Grafana Disk Performance dashboard.
    * Check the read latency of the disk by viewing the Disk Latency panel.
    * Check the I/O usage by viewing the Disk I/O Utilization panel.

#### `NODE_disk_write_latency_more_than_16ms`

* Alert rule:

    `((rate(node_disk_write_time_seconds_total{device=~".+"}[5m]) / rate(node_disk_writes_completed_total{device=~".+"}[5m])) or (irate(node_disk_write_time_seconds_total{device=~".+"}[5m]) / irate(node_disk_writes_completed_total{device=~".+"}[5m]))) * 1000 > 16`

* Description:

    The write latency of the disk exceeds 16ms.

* Solution:

    * Check the disk status by viewing the Grafana Disk Performance dashboard.
    * Check the write latency of the disk by viewing the Disk Latency panel.
    * Check the I/O usage by viewing the Disk I/O Utilization panel.

## Blackbox_exporter TCP, ICMP, and HTTP alert rules

This section gives the alert rules for the Blackbox_exporter TCP, ICMP, and HTTP.

### Emergency-level alerts

Emergency-level alerts are often caused by a service or node failure. Manual intervention is required immediately.

#### `TiDB_server_is_down`

* Alert rule:

    `probe_success{group="tidb"} == 0`

* Description:

    Failure to probe the TiDB service port.

* Solution:

    * Check whether the machine that provides the TiDB service is down.
    * Check whether the TiDB process exists.
    * Check whether the network between the monitoring machine and the TiDB machine is normal.

#### `Pump_server_is_down`

* Alert rule:

    `probe_success{group="pump"} == 0`

* Description:

    Failure to probe the pump service port.

* Solution:

    * Check whether the machine that provides the pump service is down.
    * Check whether the pump process exists.
    * Check whether the network between the monitoring machine and the pump machine is normal.

#### `Drainer_server_is_down`

* Alert rule:

    `probe_success{group="drainer"} == 0`

* Description:

    Failure to probe the Drainer service port.

* Solution:

    * Check whether the machine that provides the Drainer service is down.
    * Check whether the Drainer process exists.
    * Check whether the network between the monitoring machine and the Drainer machine is normal.

#### `TiKV_server_is_down`

* Alert rule:

    `probe_success{group="tikv"} == 0`

* Description:

    Failure to probe the TiKV service port.

* Solution:

    * Check whether the machine that provides the TiKV service is down.
    * Check whether the TiKV process exists.
    * Check whether the network between the monitoring machine and the TiKV machine is normal.

#### `PD_server_is_down`

* Alert rule:

    `probe_success{group="pd"} == 0`

* Description:

    Failure to probe the PD service port.

* Solution:

    * Check whether the machine that provides the PD service is down.
    * Check whether the PD process exists.
    * Check whether the network between the monitoring machine and the PD machine is normal.

#### `Node_exporter_server_is_down`

* Alert rule:

    `probe_success{group="node_exporter"} == 0`

* Description:

    Failure to probe the Node_exporter service port.

* Solution:

    * Check whether the machine that provides the Node_exporter service is down.
    * Check whether the Node_exporter process exists.
    * Check whether the network between the monitoring machine and the Node_exporter machine is normal.

#### `Blackbox_exporter_server_is_down`

* Alert rule:

    `probe_success{group="blackbox_exporter"} == 0`

* Description:

    Failure to probe the Blackbox_Exporter service port.

* Solution:

    * Check whether the machine that provides the Blackbox_Exporter service is down.
    * Check whether the Blackbox_Exporter process exists.
    * Check whether the network between the monitoring machine and the Blackbox_Exporter machine is normal.

#### `Grafana_server_is_down`

* Alert rule:

    `probe_success{group="grafana"} == 0`

* Description:

    Failure to probe the Grafana service port.

* Solution:

    * Check whether the machine that provides the Grafana service is down.
    * Check whether the Grafana process exists.
    * Check whether the network between the monitoring machine and the Grafana machine is normal.

#### `Pushgateway_server_is_down`

* Alert rule:

    `probe_success{group="pushgateway"} == 0`

* Description:

    Failure to probe the Pushgateway service port.

* Solution:

    * Check whether the machine that provides the Pushgateway service is down.
    * Check whether the Pushgateway process exists.
    * Check whether the network between the monitoring machine and the Pushgateway machine is normal.

#### `Kafka_exporter_is_down`

* Alert rule:

    `probe_success{group="kafka_exporter"} == 0`

* Description:

    Failure to probe the Kafka_Exporter service port.

* Solution:

    * Check whether the machine that provides the Kafka_Exporter service is down.
    * Check whether the Kafka_Exporter process exists.
    * Check whether the network between the monitoring machine and the Kafka_Exporter machine is normal.

#### `Pushgateway_metrics_interface`

* Alert rule:

    `probe_success{job="blackbox_exporter_http"} == 0`

* Description:

    Failure to probe the Pushgateway service http interface.

* Solution:

    * Check whether the machine that provides the Pushgateway service is down.
    * Check whether the Pushgateway process exists.
    * Check whether the network between the monitoring machine and the Pushgateway machine is normal.

### Warning-level alerts

Warning-level alerts are a reminder for an issue or error.

#### `BLACKER_ping_latency_more_than_1s`

* Alert rule:

    `max_over_time(probe_duration_seconds{job=~"blackbox_exporter.*_icmp"}[1m]) > 1`

* Description:

    The ping latency exceeds 1 second.

* Solution:

    * View the ping latency between the two nodes on the Grafana Blackbox Exporter dashboard to check whether it is too high.
    * Check the tcp panel on the Grafana Node Exporter dashboard to check whether there is any packet loss.
