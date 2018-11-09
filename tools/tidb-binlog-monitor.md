---
title: TiDB-Binlog Monitoring Metrics
summary: Learn about three levels of monitoring metrics of TiDB-Binlog.
category: tools
---

# TiDB-Binlog Monitoring Metrics

Currently, the monitoring metrics of TiDB-Binlog has three levels:

- Emergency
- Critical
- Warning

## Emergency

### binlog_pump_storage_error_count

- Description: Pump fails to write the binlog data to the local storage
- Monitoring rule: `changes(binlog_pump_storage_error_count[1m])` > 0
- Solution: Check whether an error exists in the `pump_storage_error` monitoring and check the Pump log to find the causes

## Critical

### binlog_drainer_checkpoint_high_delay

- Description: The delay of Drainer synchronization exceeds one hour
- Monitoring rule: `(time() - binlog_drainer_checkpoint_tso / 1000)` > 3600
- Solutions:

    - Check whether it is too slow to obtain the data from Pump:
        
        You can check `handle tso` of Pump to get the time for the latest message of each Pump. Check whether a high latency exists for Pump and make sure the corresponding Pump is running normally 
    
    - Check whether it is too slow to synchronize data in the downstream based on Drainer `event` and Drainer `execute latency`:
        
        - If Drainer `execute time` is too large, check the network bandwidth and latency between the machine with Drainer deployed and the machine with the target database deployed, and the state of the target database
        - If Drainer `execute time` is not too large and Drainer `event` is too small, add `work count` and `batch` and retry

    - If the two solutions above cannot work, contact [support@pingcap.com](mailto:support@pingcap.com)

## Warning

### binlog_pump_write_binlog_rpc_duration_seconds_bucket

- Description: It takes too much time for Pump to handle the TiDB request of writing binlog
- Monitoring rule: `histogram_quantile(0.9, rate(binlog_pump_rpc_duration_seconds_bucket{method="WriteBinlog"}[5m]))` > 1
- Solution: 
    
    - Verify the disk performance pressure and check the disk performance monitoring via `node exported`
    - If both `disk latency` and `util` are low, contact [support@pingcap.com](mailto:support@pingcap.com)

### binlog_pump_storage_write_binlog_duration_time_bucket

- Description: The time it takes for Pump to write the local binlog to the local disk
- Monitoring rule: `histogram_quantile(0.9, rate(binlog_pump_storage_write_binlog_duration_time_bucket{type="batch"}[5m]))` > 1
- Solution: Check the state of the local disk of Pump and fix the problem

### binlog_pump_storage_available_size_less_than_20G

- Description: The available disk space of Pump is less than 20G
- Monitoring rule: `binlog_pump_storage_storage_size_bytes{type="available"}` < 20 * 1024 * 1024 * 1024
- Solution: Check whether Pump `gc_tso` is normal. If not, adjust the GC time configuration of Pump or get the corresponding Pump offline

### binlog_drainer_checkpoint_tso_no_change_for_1m

- Description: Drainer `checkpoint` has not been updated for one minute
- Monitoring rule: `changes(binlog_drainer_checkpoint_tso[1m])` < 1
- Solution: Check whether all the Pumps that are not offline are running normally

### binlog_drainer_execute_duration_time_more_than_10s

- Description: The transaction time it takes Drainer to synchronize data to TiDB. If it is too large, the Drainer synchronization of data is affected
- Monitoring rule: `histogram_quantile(0.9, rate(binlog_drainer_execute_duration_time_bucket[1m]))` > 10
- Solutions:
    
    - Check the TiDB cluster state
    - Check the Drainer log or monitor. If a DDL operation causes this problem, you can ignore it
