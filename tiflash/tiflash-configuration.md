---
title: Configure TiFlash
summary: Learn how to configure TiFlash.
aliases: ['/docs/dev/tiflash/tiflash-configuration/','/docs/dev/reference/tiflash/configuration/']
---

# Configure TiFlash

This document introduces the configuration parameters related to the deployment and use of TiFlash.

## PD scheduling parameters

You can adjust the PD scheduling parameters using [pd-ctl](/pd-control.md). Note that you can use `tiup ctl:v<CLUSTER_VERSION> pd` to replace `pd-ctl -u <pd_ip:pd_port>` when using tiup to deploy and manage your cluster.

- [`replica-schedule-limit`](/pd-configuration-file.md#replica-schedule-limit): determines the rate at which the replica-related operator is generated. The parameter affects operations such as making nodes offline and add replicas.

  > **Note:**
  >
  > The value of this parameter should be less than that of `region-schedule-limit`. Otherwise, the normal Region scheduling among TiKV nodes is affected.

- `store-balance-rate`: limits the rate at which Regions of each TiKV/TiFlash store are scheduled. Note that this parameter takes effect only when the stores have newly joined the cluster. If you want to change the setting for existing stores, use the following command.

  > **Note:**
  >
  > Since v4.0.2, the `store-balance-rate` parameter has been deprecated and changes have been made to the `store limit` command. See [store-limit](/configure-store-limit.md) for details.

    - Execute the `pd-ctl -u <pd_ip:pd_port> store limit <store_id> <value>` command to set the scheduling rate of a specified store. (To get `store_id`, you can execute the `pd-ctl -u <pd_ip:pd_port> store` command.
    - If you do not set the scheduling rate for Regions of a specified store, this store inherits the setting of `store-balance-rate`.
    - You can execute the `pd-ctl -u <pd_ip:pd_port> store limit` command to view the current setting value of `store-balance-rate`.

- [`replication.location-labels`](/pd-configuration-file.md#location-labels): indicates the topological relationship of TiKV instances. The order of the keys indicates the layering relationship of different labels. If TiFlash is enabled, you need to use [`pd-ctl config placement-rules`](/pd-control.md#config-show--set-option-value--placement-rules) to set the default value. For details, see [geo-distributed-deployment-topology](/geo-distributed-deployment-topology.md).

## TiFlash configuration parameters

This section introduces the configuration parameters of TiFlash.

### Configure the `tiflash.toml` file

```toml
## The listening host for supporting services such as TPC/HTTP. It is recommended to configure it as "0.0.0.0", which means to listen on all IP addresses of this machine.
listen_host = "0.0.0.0"
## The TiFlash TCP service port.
tcp_port = 9000
## The TiFlash HTTP service port.
http_port = 8123
## The cache size limit of the metadata of a data block. Generally, you do not need to change this value.
mark_cache_size = 5368709120
## The cache size limit of the min-max index of a data block. Generally, you do not need to change this value.
minmax_index_cache_size = 5368709120
## The cache size limit of the DeltaIndex. The default value is 0, which means no limit.
delta_index_cache_size = 0

## The storage path of TiFlash data. If there are multiple directories, separate each directory with a comma.
## path and path_realtime_mode are deprecated since v4.0.9. Use the configurations
## in the [storage] section to get better performance in the multi-disk deployment scenarios
## Since TiDB v5.2.0, if you need to use the storage.io_rate_limit configuration, you need to set the storage path of TiFlash data to storage.main.dir at the same time.
## When the [storage] configurations exist, both path and path_realtime_mode configurations are ignored.
# path = "/tidb-data/tiflash-9000"
## or
# path = "/ssd0/tidb-data/tiflash,/ssd1/tidb-data/tiflash,/ssd2/tidb-data/tiflash"
## The default value is false. If you set it to true and multiple directories
## are set in the path, the latest data is stored in the first directory and older
## data is stored in the rest directories.
# path_realtime_mode = false

## The path in which the TiFlash temporary files are stored. By default it is the first directory in path
## or in storage.latest.dir appended with "/tmp".
# tmp_path = "/tidb-data/tiflash-9000/tmp"

## Storage paths settings take effect starting from v4.0.9
[storage]

    ## DTFile format
    ## * format_version = 2, the default format for versions < v6.0.0.
    ## * format_version = 3, the default format for v6.0.0 and v6.1.x, which provides more data validation features.
    ## * format_version = 4, the default format for v6.2.0 and later versions, which reduces write amplification and background task resource consumption
    # format_version = 4

    [storage.main]
    ## The list of directories to store the main data. More than 90% of the total data is stored in
    ## the directory list.
    dir = [ "/tidb-data/tiflash-9000" ]
    ## or
    # dir = [ "/ssd0/tidb-data/tiflash", "/ssd1/tidb-data/tiflash" ]

    ## The maximum storage capacity of each directory in storage.main.dir.
    ## If it is not set, or is set to multiple 0, the actual disk (the disk where the directory is located) capacity is used.
    ## Note that human-readable numbers such as "10GB" are not supported yet.
    ## Numbers are specified in bytes.
    ## The size of the capacity list should be the same with the dir size.
    ## For example:
    # capacity = [ 10737418240, 10737418240 ]

    [storage.latest]
    ## The list of directories to store the latest data. About 10% of the total data is stored in
    ## the directory list. The directories (or directory) listed here require higher IOPS
    ## metrics than those in storage.main.dir.
    ## If it is not set (by default), the values of storage.main.dir are used.
    # dir = [ ]
    ## The maximum storage capacity of each directory in storage.latest.dir.
    ## If it is not set, or is set to multiple 0, the actual disk (the disk where the directory is located) capacity is used.
    # capacity = [ 10737418240, 10737418240 ]

    ## [storage.io_rate_limit] settings are new in v5.2.0.
    [storage.io_rate_limit]
    ## This configuration item determines whether to limit the I/O traffic, which is disabled by default. This traffic limit in TiFlash is suitable for cloud storage that has the disk bandwidth of a small and specific size.
    ## The total I/O bandwidth for disk reads and writes. The unit is bytes and the default value is 0, which means the I/O traffic is not limited by default.
    # max_bytes_per_sec = 0
    ## max_read_bytes_per_sec and max_write_bytes_per_sec have similar meanings to max_bytes_per_sec. max_read_bytes_per_sec means the total I/O bandwidth for disk reads, and max_write_bytes_per_sec means the total I/O bandwidth for disk writes.
    ## These configuration items limit I/O bandwidth for disk reads and writes separately. You can use them for cloud storage that calculates the limit of I/O bandwidth for disk reads and writes separately, such as the Persistent Disk provided by Google Cloud Platform.
    ## When the value of max_bytes_per_sec is not 0, max_bytes_per_sec is prioritized.
    # max_read_bytes_per_sec = 0
    # max_write_bytes_per_sec = 0

    ## The following parameters control the bandwidth weights assigned to different I/O traffic types. Generally, you do not need to adjust these parameters.
    ## TiFlash internally divides I/O requests into four types: foreground writes, background writes, foreground reads, background reads.
    ## When the I/O traffic limit is initialized, TiFlash assigns the bandwidth according to the following weight ratio.
    ## The following  default configurations indicate that each type of traffic gets a weight of 25% (25 / (25 + 25 + 25 + 25) = 25%).
    ## If the weight is configured to 0, the corresponding I/O traffic is not limited.
    # foreground_write_weight = 25
    # background_write_weight = 25
    # foreground_read_weight = 25
    # background_read_weight = 25
    ## TiFlash supports automatically tuning the traffic limit for different I/O types according to the current I/O load. Sometimes, the tuned bandwidth might exceed the weight ratio set above.
    ## auto_tune_sec indicates the interval of automatic tuning. The unit is seconds. If the value of auto_tune_sec is 0, the automatic tuning is disabled.
    # auto_tune_sec = 5

[flash]
    tidb_status_addr = TiDB status port and address. # Multiple addresses are separated with commas.
    service_addr = The listening address of TiFlash Raft services and coprocessor services.

## Multiple TiFlash nodes elect a master to add or delete placement rules to PD,
## and the configurations in flash.flash_cluster control this process.
[flash.flash_cluster]
    refresh_interval = Master regularly refreshes the valid period.
    update_rule_interval = Master regularly gets the status of TiFlash replicas and interacts with PD.
    master_ttl = The valid period of the elected master.
    cluster_manager_path = The absolute path of the pd buddy directory.
    log = The pd buddy log path.

[flash.proxy]
    addr = The listening address of proxy. If it is left empty, 127.0.0.1:20170 is used by default.
    advertise-addr = The external access address of addr. If it is left empty, "addr" is used by default.
    data-dir = The data storage path of proxy.
    config = The configuration file path of proxy.
    log-file = The log path of proxy.
    log-level = The log level of proxy. "info" is used by default.
    status-addr = The listening address from which the proxy pulls metrics | status information. If it is left empty, 127.0.0.1:20292 is used by default.
    advertise-status-addr = The external access address of status-addr. If it is left empty, "status-addr" is used by default.

[logger]
    ## log level (available options: trace, debug, information, warning, error). The default value is `debug`.
    level = debug
    log = TiFlash log path
    errorlog = TiFlash error log path
    ## Size of a single log file. The default value is "100M".
    size = "100M"
    ## Maximum number of log files to save. The default value is 10.
    count = 10

[raft]
    ## PD service address. Multiple addresses are separated with commas.
    pd_addr = "10.0.1.11:2379,10.0.1.12:2379,10.0.1.13:2379"

[status]
    ## The port through which Prometheus pulls metrics information. The default value is 8234.
    metrics_port = 8234

[profiles]

[profiles.default]
    ## The default value is false. This parameter determines whether the segment
    ## of DeltaTree Storage Engine uses logical split.
    ## Using the logical split can reduce the write amplification.
    ## However, these are at the cost of disk space waste.
    ## It is strongly recommended to keep the default value `false` and
    ## not to change it to `true` in v6.2.0 and later versions. For details,
    ## see known issue [#5576](https://github.com/pingcap/tiflash/issues/5576).
    # dt_enable_logical_split = false

    ## The memory usage limit for the generated intermediate data in a single query.
    ## When the value is an integer, the unit is byte. For example, 34359738368 means 32 GiB of memory limit, and 0 means no limit.
    ## When the value is a floating-point number in the range of [0.0, 1.0), it means the ratio of the allowed memory usage to the total memory of the node. For example, 0.8 means 80% of the total memory, and 0.0 means no limit.
    ## The default value is 0, which means no limit.
    ## When a query attempts to consume memory that exceeds this limit, the query is terminated and an error is reported.
    max_memory_usage = 0

    ## The memory usage limit for the generated intermediate data in all queries.
    ## When the value is an integer, the unit is byte. For example, 34359738368 means 32 GiB of memory limit, and 0 means no limit.
    ## When the value is a floating-point number in the range of [0.0, 1.0), it means the ratio of the allowed memory usage to the total memory of the node. For example, 0.8 means 80% of the total memory, and 0.0 means no limit.
    ## The default value is 0.8, which means 80% of the total memory.
    ## When the queries attempt to consume memory that exceeds this limit, the queries are terminated and an error is reported.
    max_memory_usage_for_all_queries = 0.8

    ## New in v5.0. This item specifies the maximum number of cop requests that TiFlash Coprocessor executes at the same time. If the number of requests exceeds the specified value, the exceeded requests will queue. If the configuration value is set to 0 or not set, the default value is used, which is twice the number of physical cores.
    cop_pool_size = 0
    ## New in v5.0. This item specifies the maximum number of batch requests that TiFlash Coprocessor executes at the same time. If the number of requests exceeds the specified value, the exceeded requests will queue. If the configuration value is set to 0 or not set, the default value is used, which is twice the number of physical cores.
    batch_cop_pool_size = 0
    ## New in v6.1.0. This item specifies the number of requests that TiFlash can concurrently process when it receives ALTER TABLE ... COMPACT from TiDB.
    ## If the value is set to 0, the default value 1 prevails.
    manual_compact_pool_size = 1
    ## New in v5.4.0. This item enables or disables the elastic thread pool feature, which significantly improves CPU utilization in high concurrency scenarios of TiFlash. The default value is true.
    enable_elastic_threadpool = true
    ## Compression algorithm of the TiFlash storage engine. The value can be LZ4, zstd, or LZ4HC, and is case-insensitive. By default, LZ4 is used.
    dt_compression_method = "LZ4"
    ## Compression level of the TiFlash storage engine. The default value is 1.
    ## It is recommended that you set this value to 1 if dt_compression_method is LZ4.
    ## It is recommended that you set this value to -1 (smaller compression rate, but better read performance) or 1 if dt_compression_method is zstd.
    ## It is recommended that you set this value to 9 if dt_compression_method is LZ4HC.
    dt_compression_level = 1

    ## New in v6.2.0. This item specifies the minimum ratio of valid data in a PageStorage data file. When the ratio of valid data in a PageStorage data file is less than the value of this configuration, GC is triggered to compact data in the file. The default value is 0.5.
    dt_page_gc_threshold = 0.5


## Security settings take effect starting from v4.0.5.
[security]
    ## New in v5.0. This configuration item enables or disables log redaction. If the configuration value
    ## is set to true, all user data in the log will be replaced by ?.
    ## Note that you also need to set security.redact-info-log for tiflash-learner's logging in tiflash-learner.toml.
    # redact_info_log = false

    ## Path of the file that contains a list of trusted SSL CAs. If set, the following settings
    ## cert_path and key_path are also needed.
    # ca_path = "/path/to/ca.pem"
    ## Path of the file that contains X509 certificate in PEM format.
    # cert_path = "/path/to/tiflash-server.pem"
    ## Path of the file that contains X509 key in PEM format.
    # key_path = "/path/to/tiflash-server-key.pem"
```

### Configure the `tiflash-learner.toml` file

```toml
[server]
    engine-addr = The external access address of the TiFlash coprocessor service.
[raftstore]
    ## The allowable number of threads in the pool that flushes Raft data to storage.
    apply-pool-size = 4

    ## The allowable number of threads that process Raft, which is the size of the Raftstore thread pool.
    store-pool-size = 4

    ## The number of threads that handle snapshots.
    ## The default number is 2.
    ## If you set it to 0, the multi-thread optimization is disabled.
    snap-handle-pool-size = 2

    ## The shortest interval at which Raft store persists WAL.
    ## You can properly increase the latency to reduce IOPS usage.
    ## The default value is "4ms".
    ## If you set it to 0ms, the optimization is disabled.
    store-batch-retry-recv-timeout = "4ms"
[security]
    ## New in v5.0. This configuration item enables or disables log redaction.
    ## If the configuration value is set to true,
    ## all user data in the log will be replaced by ?. The default value is false.
    redact-info-log = false

[security.encryption]
    ## The encryption method for data files.
    ## Value options: "aes128-ctr", "aes192-ctr", "aes256-ctr", "sm4-ctr" (supported since v6.4.0), and "plaintext".
    ## Default value: `"plaintext"`, which means encryption is disabled by default. A value other than "plaintext" means that encryption is enabled, in which case the master key must be specified.
    data-encryption-method = "aes128-ctr"
    ## Specifies how often the data encryption key is rotated. Default value: `7d`.
    data-key-rotation-period = "168h" # 7 days

[security.encryption.master-key]
    ## Specifies the master key if encryption is enabled. To learn how to configure a master key, see Configure encryption: https://docs.pingcap.com/tidb/dev/encryption-at-rest#configure-encryption .

[security.encryption.previous-master-key]
    ## Specifies the old master key when rotating the new master key. The configuration format is the same as that of `master-key`. To learn how to configure a master key, see  Configure encryption: https://docs.pingcap.com/tidb/dev/encryption-at-rest#configure-encryption .
```

In addition to the items above, other parameters are the same as those of TiKV. Note that the `label` whose key is `engine` is reserved and cannot be configured manually.

### Schedule replicas by topology labels

See [Set available zones](/tiflash/create-tiflash-replicas.md#set-available-zones).

### Multi-disk deployment

TiFlash supports multi-disk deployment. If there are multiple disks in your TiFlash node, you can make full use of those disks by configuring the parameters described in the following sections. For TiFlash's configuration template to be used for TiUP, see [The complex template for the TiFlash topology](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml).

#### Multi-disk deployment with TiDB version earlier than v4.0.9

For TiDB clusters earlier than v4.0.9, TiFlash only supports storing the main data of the storage engine on multiple disks. You can set up a TiFlash node on multiple disks by specifying the `path` (`data_dir` in TiUP) and `path_realtime_mode` configuration.

If there are multiple data storage directories in `path`, separate each with a comma. For example, `/nvme_ssd_a/data/tiflash,/sata_ssd_b/data/tiflash,/sata_ssd_c/data/tiflash`. If there are multiple disks in your environment, it is recommended that each directory corresponds to one disk and you put disks with the best performance at the front to maximize the performance of all disks.

If there are multiple disks with similar I/O metrics on your TiFlash node, you can leave the `path_realtime_mode` parameter to the default value (or you can explicitly set it to `false`). It means that data will be evenly distributed among all storage directories. However, the latest data is written only to the first directory, so the corresponding disk is busier than other disks.

If there are multiple disks with different I/O metrics on your TiFlash node, it is recommended to set `path_realtime_mode` to `true` and put disks with the best I/O metrics at the front of `path`. It means that the first directory only stores the latest data, and the older data are evenly distributed among the other directories. Note that in this case, the capacity of the first directory should be planned as 10% of the total capacity of all directories.

#### Multi-disk deployment with TiDB v4.0.9 or later

For TiDB clusters with v4.0.9 or later versions, TiFlash supports storing the main data and the latest data of the storage engine on multiple disks. If you want to deploy a TiFlash node on multiple disks, it is recommended to specify your storage directories in the `[storage]` section to make full use of your node. Note that the configurations earlier than v4.0.9 (`path` and `path_realtime_mode`) are still supported.

If there are multiple disks with similar I/O metrics on your TiFlash node, it is recommended to specify corresponding directories in the `storage.main.dir` list and leave `storage.latest.dir` empty. TiFlash will distribute I/O pressure and data among all directories.

If there are multiple disks with different I/O metrics on your TiFlash node, it is recommended to specify directories with higher metrics in the `storage.latest.dir` list, and specify directories with lower metrics in the `storage.main.dir` list. For example, for one NVMe-SSD and two SATA-SSDs, you can set `storage.latest.dir` to `["/nvme_ssd_a/data/tiflash"]` and `storage.main.dir` to `["/sata_ssd_b/data/tiflash", "/sata_ssd_c/data/tiflash"]`. TiFlash will distribute I/O pressure and data among these two directories list respectively. Note that in this case, the capacity of `storage.latest.dir` should be planned as 10% of the total planned capacity.

> **Warning:**
>
> The `[storage]` configuration is supported in TiUP since v1.2.5. If your TiDB cluster version is v4.0.9 or later, make sure that your TiUP version is v1.2.5 or later. Otherwise, the data directories defined in `[storage]` will not be managed by TiUP.
