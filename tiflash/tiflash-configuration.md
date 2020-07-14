---
title: Configure TiFlash
summary: Learn how to configure TiFlash.
aliases: ['/docs/dev/tiflash/tiflash-configuration/','/docs/dev/reference/tiflash/configuration/']
---

# Configure TiFlash

This document introduces the configuration parameters related to the deployment and use of TiFlash.

## PD scheduling parameters

You can adjust the PD scheduling parameters using [pd-ctl](/pd-control.md). Note that you can use `tiup ctl pd` to replace `pd-ctl -u <pd_ip:pd_port>` when using tiup to deploy and manage your cluster.

- [`replica-schedule-limit`](/pd-configuration-file.md#replica-schedule-limit): determines the rate at which the replica-related operator is generated. The parameter affects operations such as making nodes offline and add replicas.

    > **Notes:**
    >
    > The value of this parameter should be less than that of `region-schedule-limit`. Otherwise, the normal Region scheduling among TiKV nodes is affected.

- [`store-balance-rate`](/pd-configuration-file.md#store-balance-rate): limits the rate at which Regions of each TiKV/TiFlash store are scheduled. Note that this parameter takes effect only when the stores have newly joined the cluster. If you want to change the setting for existing stores, use the following command.
    - Execute the `pd-ctl -u <pd_ip:pd_port> store limit <store_id> <value>` command to set the scheduling rate of a specified store. (To get `store_id`, you can execute the `pd-ctl -u <pd_ip:pd_port> store` command. 
    - If you do not set the scheduling rate for Regions of a specified store, this store inherits the setting of `store-balance-rate`. 
    - You can execute the `pd-ctl -u <pd_ip:pd_port> store limit` command to view the current setting value of `store-balance-rate`.

## TiFlash configuration parameters

This section introduces the configuration parameters of TiFlash.

### Configure the `tiflash.toml` file

```
tmp_path = The path in which the TiFlash temporary files are stored.
path = The TiFlash data storage path.     # If there are multiple directories, separate each directory with a comma.
path_realtime_mode = false # The default value is `false`. If you set it to `true` and multiple directories are deployed in the path, the latest data is stored in the first directory and older data is stored in the rest directories.
listen_host = The TiFlash service listening host. # Generally, it is configured as `0.0.0.0`.
tcp_port = The TiFlash TCP service port.
http_port = The TiFlash HTTP service port.
mark_cache_size = 5368709120 # The cache size limit of the metadata of a data block. Generally, you do not need to change this value.
minmax_index_cache_size = 5368709120 # The cache size limit of the min-max index of a data block. Generally, you do not need to change this value.
```

```
[flash]
    tidb_status_addr = TiDB status port and address. # Multiple addresses are separated with commas.
    service_addr = The listening address of TiFlash Raft services and coprocessor services.
```

Multiple TiFlash nodes elect a master to add or delete placement rules to PD, and you need three parameters to control this process.

```
[flash.flash_cluster]
    refresh_interval = Master regularly refreshes the valid period.
    update_rule_interval = Master regularly gets the status of TiFlash replicas and interacts with PD.
    master_ttl = The valid period of the elected master.
    cluster_manager_path = The absolute path of the pd buddy directory.
    log = The pd buddy log path.

[flash.proxy]
    addr = The listening address of proxy.
    advertise-addr = The external access address of proxy.
    data-dir = The data storage path of proxy.
    config = The proxy configuration file path.
    log-file = The proxy log path.

[logger]
    level = log level (available options: trace, debug, information, warning, error).
    log = The TiFlash log path.
    errorlog = The TiFlash error log path.
    size = The size of a single log file.
    count = The maximum number of log files to save.
[raft]
    kvstore_path = The storage path of the kvstore data. # The default setting: "{the first directory of the path}/kvstore"
    pd_addr = PD service address. # Multiple addresses are separated with commas.
[status]
    metrics_port = The port through which Prometheus pulls metrics information.
[profiles]
[profiles.default]
    dt_enable_logical_split = true # The default value is `true`. This parameter determines whether the segment of DeltaTree Storage Engine uses logical split. Using the logical split can reduce the write amplification, and improve the write speed. However, these are at the cost of disk space waste.
    max_memory_usage = 10000000000 # The memory usage limit for the generated intermediate data when a single coprocessor query is executed. The default value is 10,000,000,000 (in bytes). If set to 0, it means no limit.
    max_memory_usage_for_all_queries = 0 # The memory usage limit for the generated intermediate data when all queries are executed. The default value is 0 (in bytes), which means no limit.
```

### Configure the `tiflash-learner.toml` file

```
[server]
    engine-addr = The listening address of the TiFlash coprocessor service.
    status-addr = The port and IP through which Prometheus pulls proxy metrics information.
```

### Multi-disk deployment

TiFlash supports multi-disk deployment, controlled by the `path` and `path_realtime_mode` parameters in the [`tiflash.toml` file](#configure-the-tiflashtoml-file).

If there are multiple data storage directories in `path`, separate each with a comma. For example, `/ssd_a/data/tiflash,/hdd_b/data/tiflash,/hdd_c/data/tiflash`. If there are multiple disks in your environment, it is recommended that each directory corresponds to one disk and you put disks with the best performance at the front to maximize the performance of all disks.

The default value of the `path_realtime_mode` parameter is `false`, which means that data are evenly distributed on all storage directories. If the parameter is set to `true`, and `path` contains multiple directories, it means that the first directory only stores the latest data, and the older data are evenly distributed on other directories.
