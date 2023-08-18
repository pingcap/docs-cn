---
title: Physical Import Mode
summary: Learn about the physical import mode in TiDB Lightning.
---

# Physical Import Mode

Physical import mode is an efficient and fast import mode that inserts data directly into TiKV nodes as key-value pairs without going through the SQL interface. When using the physical import mode, a single instance of Lightning can import up to 10 TiB of data. The supported amount of imported data theoretically increases as the number of Lightning instances increases. It is verified by users that [parallel importing](/tidb-lightning/tidb-lightning-distributed-import.md) based on Lightning can effectively handle up to 20 TiB of data.

Before you use the physical import mode, make sure to read [Requirements and restrictions](#requirements-and-restrictions).

The backend for the physical import mode is `local`. You can modify it in `tidb-lightning.toml`:

 ```toml
 [tikv-importer]
 # Set the import mode to "local" to use the physical import mode.
 backend = "local"
 ```

## Implementation

1. Before importing data, TiDB Lightning automatically switches the TiKV nodes to "import mode", which improves write performance and stops auto-compaction. TiDB Lightning determines whether to pause global scheduling according to the TiDB Lightning version.

    - Starting from v7.1.0, you can you can control the scope of pausing scheduling by using the TiDB Lightning parameter [`pause-pd-scheduler-scope`](/tidb-lightning/tidb-lightning-configuration.md).
    - For TiDB Lightning versions between v6.2.0 and v7.0.0, the behavior of pausing global scheduling depends on the TiDB cluster version. When the TiDB cluster >= v6.1.0, TiDB Lightning pauses scheduling for the Region that stores the target table data. After the import is completed, TiDB Lightning recovers scheduling. For other versions, TiDB Lightning pauses global scheduling.
    - When TiDB Lightning < v6.2.0, TiDB Lightning pauses global scheduling.

2. TiDB Lightning creates table schemas in the target database and fetches the metadata.

    If you set `add-index-by-sql` to `true`, `tidb-lightning` adds indexes via the SQL interface, and drops all secondary indexes from the target table before importing the data. The default value is `false`, which is consistent with earlier versions.

3. Each table is divided into multiple contiguous **blocks**, so that TiDB Lightning can import data from large tables (greater than 200 GB) in parallel.

4. TiDB Lightning prepares an "engine file" for each block to handle key-value pairs. TiDB Lightning reads the SQL dump in parallel, converts the data source to key-value pairs in the same encoding as TiDB, sorts the key-value pairs and writes them to a local temporary storage file.

5. When an engine file is written, TiDB Lightning starts to split and schedule data on the target TiKV cluster, and then imports data to TiKV cluster.

    The engine file contains two types of engines: **data engine** and **index engine**. Each engine corresponds to a type of key-value pairs: row data and secondary index. Normally, row data is completely ordered in the data source, and the secondary index is unordered. Therefore, the data engine files are imported immediately after the corresponding block is written, and all index engine files are imported only after the entire table is encoded.

    Note that when `tidb-lightning` adds indexes via the SQL interface (that is, you set `add-index-by-sql` to `true`), the index engine will not write data because the secondary indexes of the target table have already been dropped in step 2.

6. After all engine files are imported, TiDB Lightning compares the checksum between the local data source and the downstream cluster, and ensures that the imported data is not corrupted. Then TiDB Lightning adds the previously dropped secondary indexes in step 2, or lets TiDB analyze the new data (`ANALYZE`) to optimize future operations. Meanwhile, `tidb-lightning` adjusts the `AUTO_INCREMENT` value to prevent conflicts in the future.

    The auto-increment ID is estimated by the **upper bound** of the number of rows, and is proportional to the total size of the table data file. Therefore, the auto-increment ID is usually larger than the actual number of rows. This is normal because the auto-increment ID [is not necessarily contiguous](/mysql-compatibility.md#auto-increment-id).

7. After all steps are completed, TiDB Lightning automatically switches the TiKV nodes to "normal mode". If global scheduling is paused, TiDB Lightning also recovers global scheduling. After that, the TiDB cluster can provide services normally.

## Requirements and restrictions

### Environment requirements

**Operating system**:

It is recommended to use fresh CentOS 7 instances. You can deploy a virtual machine either on your local host or in the cloud. Because TiDB Lightning consumes as much CPU resources as needed by default, it is recommended that you deploy it on a dedicated server. If this is not possible, you can deploy it on a single server together with other TiDB components (for example, tikv-server) and then configure `region-concurrency` to limit the CPU usage from TiDB Lightning. Usually, you can configure the size to 75% of the logical CPU.

**Memory and CPU**:

It is recommended that you allocate CPU more than 32 cores and memory greater than 64 GiB to get better performance.

> **Note:**
>
> When you import a large amount of data, one concurrent import may consume about 2 GiB memory. The total memory usage can be `region-concurrency * 2 GiB`. `region-concurrency` is the same as the number of logical CPUs by default. If the memory size (GiB) is less than twice of the CPU or OOM occurs during the import, you can decrease `region-concurrency` to avoid OOM.

**Storage**: The `sorted-kv-dir` configuration item specifies the temporary storage directory for the sorted key-value files. The directory must be empty, and the storage space must be greater than the size of the dataset to be imported. For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage and exclusive I/O for the directory.

**Network**: A 10Gbps Ethernet card is recommended.

### Version requirements

- TiDB Lightning >= v4.0.3.
- TiDB >= v4.0.0.
- If the target TiDB cluster is v3.x or earlier, you need to use Importer-backend to complete the data import. In this mode, `tidb-lightning` needs to send the parsed key-value pairs to `tikv-importer` via gRPC, and `tikv-importer` will complete the data import.

### Limitations

- Do not use the physical import mode to directly import data to TiDB clusters in production. It has severe performance implications. If you need to do so, refer to [Pause scheduling on the table level](/tidb-lightning/tidb-lightning-physical-import-mode-usage.md#scope-of-pausing-scheduling-during-import).
- If your TiDB cluster has a latency-sensitive application and a low concurrency, it is strongly recommended that you **do not** use the physical import mode to import data into the cluster. This mode might have significant impact on the online application.
- Do not use multiple TiDB Lightning instances to import data to the same TiDB cluster by default. Use [Parallel Import](/tidb-lightning/tidb-lightning-distributed-import.md) instead.
- When you use multiple TiDB Lightning to import data to the same target cluster, do not mix the import modes. That is, do not use the physical import mode and the logical import mode at the same time.
- During the process of importing data, do not perform DDL and DML operations in the target table. Otherwise the import will fail or the data will be inconsistent. At the same time, it is not recommended to perform read operations, because the data you read might be inconsistent. You can perform read and write operations after the import operation is completed.
- A single Lightning process can import a single table of 10 TB at most. Parallel import can use 10 Lightning instances at most.

### Tips for using with other components

- When you use TiDB Lightning with TiFlash, note the following:

    - Whether you have created a TiFlash replica for a table, you can use TiDB Lightning to import data to the table. However, the import might take longer than the normal import. The import time is influenced by the network bandwidth of the server TiDB Lightning is deployed on, the CPU and disk load on the TiFlash node, and the number of TiFlash replicas.

- TiDB Lightning character sets:

    - TiDB Lightning earlier than v5.4.0 cannot import tables of `charset=GBK`.

- When you use TiDB Lightning with TiCDC, note the following:

    - TiCDC cannot capture the data inserted in the physical import mode.
