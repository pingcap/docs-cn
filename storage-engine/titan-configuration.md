---
title: Titan Configuration
summary: Learn how to configure Titan.
---

# Titan Configuration

This document introduces how to enable and disable [Titan](/storage-engine/titan-overview.md) using the corresponding configuration items, data conversion mechanism, the relevant parameters, and the Level Merge feature.

## Enable Titan

> **Note:**
>
> - Starting from TiDB v7.6.0, Titan is enabled by default for new clusters to enhance the performance of writing wide tables and JSON data. The default value of the [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) threshold is changed from `1KB` to `32KB`.
> - Existing clusters upgraded to v7.6.0 or later versions retain the original configuration, which means that if Titan is not explicitly enabled, it still uses RocksDB.
> - If you have enabled Titan before upgrading a cluster to TiDB v7.6.0 or later versions, Titan will be enabled after the upgrade, and the configuration of [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) before the upgrade will also be retained. If you do not explicitly configure the value before the upgrade, the default value of the old version `1KB` will be retained to ensure the stability of the cluster configuration after the upgrade.

Titan is compatible with RocksDB, so you can directly enable Titan on the existing TiKV instances that use RocksDB. You can use one of the following methods to enable Titan:

+ Method 1: If you have deployed the cluster using TiUP, you can execute the `tiup cluster edit-config ${cluster-name}` command and edit the TiKV configuration file as the following example shows:

    ```shell
    tikv:
      rocksdb.titan.enabled: true
    ```

    Reload the configuration and TiKV will be rolling restarted dynamically:

    ```shell
    tiup cluster reload ${cluster-name} -R tikv
    ```

    For the detailed command, see [Modify the configuration using TiUP](/maintain-tidb-using-tiup.md#modify-the-configuration).

+ Method 2: Directly edit the TiKV configuration file to enable Titan (**NOT** recommended for the production environment).

    ```toml
    [rocksdb.titan]
    enabled = true
    ```

+ Method 3: Edit the `${cluster_name}/tidb-cluster.yaml` configuration file for TiDB Operator:

    ```yaml
    spec:
      tikv:
        ## Base image of the component
        baseImage: pingcap/tikv
        ## tikv-server configuration
        ## Ref: https://docs.pingcap.com/tidb/stable/tikv-configuration-file
        config: |
          log-level = "info"
          [rocksdb]
            [rocksdb.titan]
              enabled = true
    ```

    Apply the configuration to trigger an online rolling restart of the TiDB cluster for the changes to take effect:

    ```shell
    kubectl apply -f ${cluster_name} -n ${namespace}
    ```

    For more information, refer to [Configuring a TiDB Cluster in Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster).

## Data conversion

> **Warning:**
>
> When Titan is disabled, RocksDB cannot read data that has been moved to Titan. If Titan is incorrectly disabled on a TiKV instance with Titan already enabled (mistakenly set `rocksdb.titan.enabled` to `false`), TiKV will fail to start, and the `You have disabled titan when its data directory is not empty` error appears in the TiKV log. To correctly disabled Titan, see [Disable Titan](#disable-titan).

After Titan is enabled, the existing data stored in RocksDB is not immediately moved to the Titan engine. As new data is written to the TiKV and RocksDB performs compaction, **the values are progressively separated from keys and written to Titan**. Similarly, the data restored through BR snapshot/log, the data converted during scaling, or the data imported by TiDB Lightning Physical Import Mode, is not written directly into Titan. As compaction proceeds, the large values exceeding the default value (`32KB`) of [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) in the processed SST files are separated into Titan. You can monitor the size of files stored in Titan by observing the **TiKV Details > Titan kv > blob file size** panel to estimate the data size.

If you want to speed up the writing process, you can use tikv-ctl to compact data of the whole TiKV cluster manually. For details, see [manual compaction](/tikv-control.md#compact-data-of-the-whole-tikv-cluster-manually). The data access is continuous during the conversion from RocksDB to Titan, therefore the block cache of RocksDB significantly accelerates the data conversion process. In the test, by using tikv-ctl, a volume of 670 GiB TiKV data can be converted to Titan in one hour.

Note that the values in Titan Blob files are not continuous, and Titan's cache is at the value level, so the Blob Cache does not help during compaction. The conversion speed from Titan to RocksDB is an order of magnitude slower than that from RocksDB to Titan. In the test, it takes 12 hours to convert a volume of 800 GiB Titan data on a TiKV node to RocksDB by tikv-ctl in a full compaction.

## Parameters

By properly configuring Titan parameters, you can effectively improve database performance and resource utilization. This section introduces some key parameters you can use.

### `min-blob-size`

You can use [`min-blob-size`](/tikv-configuration-file.md#min-blob-size) to set the threshold for the value size to determine which data is stored in RocksDB and which in Titan's blob files. According to the test, `32KB` is an appropriate threshold. It ensures that Titan's performance does not regress compared with RocksDB. However, in many scenarios, this value is not optimal. It is recommended that you refer to [Impact of `min-blob-size` on performance](/storage-engine/titan-overview.md#impact-of-min-blob-size-on-performance) to choose an appropriate value. If you want to further improve write performance and can tolerate scan performance regression, you can set it to the minimum value `1KB`.

### `blob-file-compression` and `zstd-dict-size`

You can use [`blob-file-compression`](/tikv-configuration-file.md#blob-file-compression) to specify the compression algorithm used for values in Titan. You can also enable the `zstd` dictionary compression through [`zstd-dict-size`](/tikv-configuration-file.md#zstd-dict-size) to improve the compression rate.

### `blob-cache-size`

You can use [`blob-cache-size`](/tikv-configuration-file.md#blob-cache-size) to control the cache size of values in Titan. Larger cache size means higher read performance of Titan. However, too large a cache size causes Out of Memory (OOM) issues.

It is recommended to set the value of `storage.block-cache.capacity` to the store size minus the blob file size, and set `blob-cache-size` to `memory size * 50% - block cache size` according to the monitoring metrics when the database is running stably. This maximizes the blob cache size when the block cache is large enough for the whole RocksDB engine.

### `discardable-ratio` and `max-background-gc`

The [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio) parameter and [`max-background-gc`](/tikv-configuration-file.md#max-background-gc) parameter significantly impact Titan's read performance and garbage collection process.

When the ratio of obsolete data (the corresponding key has been updated or deleted) in a blob file exceeds the threshold set by [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio), Titan GC is triggered. Reducing this threshold can reduce space amplification but can cause more frequent Titan GC. Increasing this value can reduce Titan GC, I/O bandwidth, and CPU consumption, but increase disk space usage.

If you observe that the Titan GC thread is in full load for a long time from **TiKV Details** - **Thread CPU** - **RocksDB CPU**, consider adjusting [`max-background-gc`](/tikv-configuration-file.md#max-background-gc) to increase the Titan GC thread pool size.

### `rate-bytes-per-sec`

You can adjust [`rate-bytes-per-sec`](/tikv-configuration-file.md#rate-bytes-per-sec) to limit the I/O rate of RocksDB compaction, reducing its impact on foreground read and write performance during high traffic.

### Titan configuration example

The following is an example of the Titan configuration file. You can either [use TiUP to modify the configuration](/maintain-tidb-using-tiup.md#modify-the-configuration) or [configure a TiDB cluster on Kubernetes](https://docs.pingcap.com/tidb-in-kubernetes/stable/configure-a-tidb-cluster).

```toml
[rocksdb]
rate-bytes-per-sec = 0

[rocksdb.titan]
enabled = true
max-background-gc = 1

[rocksdb.defaultcf.titan]
min-blob-size = "32KB"
blob-file-compression = "zstd"
zstd-dict-size = "16KB"
blob-cache-size = "0GB"
discardable-ratio = 0.5
blob-run-mode = "normal"
level-merge = false
```

## Disable Titan

To disable Titan, you can configure the `rocksdb.defaultcf.titan.blob-run-mode` option. The optional values for `blob-run-mode` are as follows:

- When the option is set to `normal`, Titan performs read and write operations normally.
- When the option is set to `read-only`, all newly written values are written into RocksDB, regardless of the value size.
- When the option is set to `fallback`, all newly written values are written into RocksDB, regardless of the value size. Also, all compacted values stored in the Titan blob file are automatically moved back to RocksDB.

To fully disable Titan for all existing and future data, you can follow these steps. Note that you can skip Step 2 because it greatly impacts online traffic performance. In fact even without Step 2, the data compaction consumes extra I/O and CPU resources when it moves data from Titan to RocksDB, and performance will degrade (sometimes as much as 50%) when TiKV I/O or CPU resources are limited.

1. Update the configuration of the TiKV nodes you wish to disable Titan for. You can update configuration in two methods:

    + Execute `tiup cluster edit-config`, edit the configuration file, and execute `tiup cluster reload -R tikv`.
    + Manually update the configuration file and restart TiKV.

        ```toml
        [rocksdb.defaultcf.titan]
        blob-run-mode = "fallback"
        discardable-ratio = 1.0
        ```

    > **Note:**
    >
    > When there is insufficient disk space to accommodate both Titan and RocksDB data, it is recommended to use the default value of `0.5` for [`discardable-ratio`](/tikv-configuration-file.md#discardable-ratio). In general, the default value is recommended when available disk space is less than 50%. This is because when `discardable-ratio = 1.0`, the RocksDB data continues to increase. At the same time, the recycling of existing blob files in Titan requires all the data in that file to be converted to RocksDB, which is a slow process. However, if the disk size is large enough, setting `discardable-ratio = 1.0` can reduce the GC of the blob file itself during compaction, which saves bandwidth.

2. (Optional) Perform a full compaction using tikv-ctl. This process will consume a large amount of I/O and CPU resources.

    ```bash
    tikv-ctl --pd <PD_ADDR> compact-cluster --bottommost force
    ```

3. After the compaction is finished, wait for the **Blob file count** metrics under **TiKV-Details**/**Titan - kv** to decrease to `0`.

4. Update the configuration of these TiKV nodes to disable Titan.

    ```toml
    [rocksdb.titan]
    enabled = false
    ```

## Level Merge (experimental)

In TiKV 4.0, [Level Merge](/storage-engine/titan-overview.md#level-merge), a new algorithm, is introduced to improve the performance of range query and to reduce the impact of Titan GC on the foreground write operations. You can enable Level Merge using the following option:

```toml
[rocksdb.defaultcf.titan]
level-merge = true
```

Enabling Level Merge has the following benefits:

- Greatly improve the performance of Titan range query.
- Reduce the impact of Titan GC on the foreground write operations and improve write performance.
- Reduce space amplification of Titan and the disk usage (compared to the disk usage with the default configuration).

Accordingly, the write amplification with Level Merge enabled is slightly higher than that of Titan but is still lower than that of the native RocksDB.
