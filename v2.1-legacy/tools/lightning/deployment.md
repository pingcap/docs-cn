---
title: TiDB-Lightning Deployment
summary: Deploy TiDB-Lightning to quickly import large amounts of new data.
category: tools
---

# TiDB-Lightning Deployment

This document describes the hardware requirements of TiDB-Lightning on separate deployment and mixed deployment, and how to deploy it using Ansible or manually.

## Notes

Before starting TiDB-Lightning, note that:

- During the import process, the cluster cannot provide normal services.
- If `tidb-lightning` crashes, the cluster is left in "import mode". Forgetting to switch back to "normal mode" can lead to a high amount of uncompacted data on the TiKV cluster, and cause abnormally high CPU usage and stall. You can manually switch the cluster back to "normal mode" via the `tidb-lightning-ctl` tool:

    ```sh
    bin/tidb-lightning-ctl -switch-mode=normal
    ```

## Hardware requirements

`tidb-lightning` and `tikv-importer` are both resource-intensive programs. It is recommended to deploy them into two separate machines.

To achieve the best performance, it is recommended to use the following hardware configuration:

- `tidb-lightning`:

    - 32+ logical cores CPU
    - An SSD large enough to store the entire SQL dump, preferring higher read speed
    - 10 Gigabit network card (capable of transferring at ≥300 MB/s)
    - `tidb-lightning` fully consumes all CPU cores when running,
        and deploying on a dedicated machine is highly recommended.
        If not possible, `tidb-lightning` could be deployed together with other components like
        `tidb-server`, and the CPU usage could be limited via the `region-concurrency` setting.

- `tikv-importer`:

    - 32+ logical cores CPU
    - 32 GB+ memory
    - 1 TB+ SSD, preferring higher IOPS (≥ 8000 is recommended)
    - 10 Gigabit network card (capable of transferring at ≥300 MB/s)
    - `tikv-importer` fully consumes all CPU, disk I/O and network bandwidth when running,
        and deploying on a dedicated machine is strongly recommended.

If you have sufficient machines, you can deploy multiple Lightning/Importer servers, with each working on a distinct set of tables, to import the data in parallel.

> **Note:**
>
> `tidb-lightning` is a CPU intensive program. In an environment with mixed components, the resources allocated to `tidb-lightning` must be limited. Otherwise, other components might not be able to run. It is recommended to set the `region-concurrency` to 75% of CPU logical cores. For instance, if the CPU has 32 logical cores, you can set the `region-concurrency` to 24.

Additionally, the target TiKV cluster should have enough space to absorb the new data.
Besides [the standard requirements](../../op-guide/recommendation.md), the total free space of the target TiKV cluster should be larger than **Size of SQL dump × [Number of replicas](../../FAQ.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it) × 2**.
With the default replica count of 3, this means the total free space should be at least 6 times the size of SQL dump.

## Export data

Use the [`mydumper` tool](../../tools/mydumper.md) to export data from MySQL by using the following command:

```sh
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 256 -B test -T t1,t2 --skip-tz-utc -o /data/my_database/
```

In this command,

- `-B test`: means the data is exported from the `test` database.
- `-T t1,t2`: means only the `t1` and `t2` tables are exported.
- `-t 16`: means 16 threads are used to export the data.
- `-F 256`: means a table is partitioned into chunks and one chunk is 256 MB.
- `--skip-tz-utc`: the purpose of adding this parameter is to ignore the inconsistency of time zone setting between MySQL and the data exporting machine, and to disable automatic conversion.

## Deploy TiDB-Lightning

This section describes two deployment methods of TiDB-Lightning:

- [Deploy TiDB-Lightning using Ansible](#deploy-tidb-lightning-using-ansible)
- [Deploy TiDB-Lightning manually](#deploy-tidb-lightning-manually)

### Deploy TiDB-Lightning using Ansible

You can deploy TiDB-Lightning using Ansible together with the [deployment of the TiDB cluster itself using Ansible](../../op-guide/ansible-deployment.md).

1. Edit `inventory.ini` to add the addresses of the `tidb-lightning` and `tikv-importer` servers.

    ```ini
    ...

    [importer_server]
    192.168.20.9

    [lightning_server]
    192.168.20.10

    ...
    ```

2. Configure these tools by editing the settings under `group_vars/*.yml`.

    * `group_vars/all.yml`

        ```yaml
        ...
        # The listening port of tikv-importer. Should be open to the tidb-lightning server.
        tikv_importer_port: 20170
        ...
        ```

    * `group_vars/lightning_server.yml`

        ```yaml
        ---
        dummy:

        # The listening port for metrics gathering. Should be open to the monitoring servers.
        tidb_lightning_pprof_port: 10089

        # The file path that tidb-lightning reads the mydumper SQL dump from.
        data_source_dir: "{{ deploy_dir }}/mydumper"
        ```

    * `group_vars/importer_server.yml`

        ```yaml
        ---
        dummy:

        # The file path to store engine files. Should reside on a partition with a large capacity.
        import_dir: "{{ deploy_dir }}/data.import"
        ```

3. Deploy the cluster.

    ```sh
    ansible-playbook bootstrap.yml
    ansible-playbook deploy.yml
    ```

4. Mount the data source to the path specified in the `data_source_dir` setting.

5. Log in to the `tikv-importer` server, and manually run the following command to start Importer.

    ```sh
    scripts/start_importer.sh
    ```

6. Log in to the `tidb-lightning` server, and manually run the following command to start Lightning and import the data into the TiDB cluster.

    ```sh
    scripts/start_lightning.sh
    ```

7. After completion, run `scripts/stop_importer.sh` on the `tikv-importer` server to stop Importer.

### Deploy TiDB-Lightning manually

#### Step 1: Deploy a TiDB cluster

Before importing data, you need to have a deployed TiDB cluster, with the cluster version 2.0.9 or above. It is highly recommended to use the latest version.

You can find deployment instructions in [TiDB Quick Start Guide](https://pingcap.com/docs/QUICKSTART/).

#### Step 2: Download the TiDB-Lightning installation package

Download the TiDB-Lightning package (choose the same version as that of the TiDB cluster):

- **v2.1.2**: https://download.pingcap.org/tidb-lightning-v2.1.2-linux-amd64.tar.gz
- **v2.0.9**: https://download.pingcap.org/tidb-lightning-v2.0.9-linux-amd64.tar.gz
- Latest unstable version: https://download.pingcap.org/tidb-lightning-latest-linux-amd64.tar.gz

#### Step 3: Start `tikv-importer`

1. Upload `bin/tikv-importer` from the installation package.

2. Configure `tikv-importer.toml`.

    ```toml
    # TiKV Importer configuration file template

    # Log file
    log-file = "tikv-importer.log"
    # Log level: trace, debug, info, warn, error, off.
    log-level = "info"

    [server]
    # The listening address of tikv-importer. tidb-lightning needs to connect to
    # this address to write data.
    addr = "0.0.0.0:20170"
    # Size of the thread pool for the gRPC server.
    grpc-concurrency = 16

    [metric]
    # The Prometheus client push job name.
    job = "tikv-importer"
    # The Prometheus client push interval.
    interval = "15s"
    # The Prometheus Pushgateway address.
    address = ""

    [rocksdb]
    # The maximum number of concurrent background jobs.
    max-background-jobs = 32

    [rocksdb.defaultcf]
    # Amount of data to build up in memory before flushing data to the disk.
    write-buffer-size = "1GB"
    # The maximum number of write buffers that are built up in memory.
    max-write-buffer-number = 8

    # The compression algorithms used in different levels.
    # The algorithm at level-0 is used to compress KV data.
    # The algorithm at level-6 is used to compress SST files.
    # The algorithms at level-1 to level-5 are unused for now.
    compression-per-level = ["lz4", "no", "no", "no", "no", "no", "zstd"]

    [import]
    # The directory to store engine files.
    import-dir = "/mnt/ssd/data.import/"
    # Number of threads to handle RPC requests.
    num-threads = 16
    # Number of concurrent import jobs.
    num-import-jobs = 24
    # Maximum duration to prepare Regions.
    #max-prepare-duration = "5m"
    # Split Regions into this size according to the importing data.
    #region-split-size = "96MB"
    # Stream channel window size. The stream will be blocked on channel full.
    #stream-channel-window = 128
    # Maximum number of open engines.
    max-open-engines = 8
    ```

3. Run `tikv-importer`.

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

#### Step 4: Start `tidb-lightning`

1. Upload `bin/tidb-lightning` and `bin/tidb-lightning-ctl` from the tool set.

2. Mount the mydumper SQL dump onto the same machine.

3. Configure `tidb-lightning.toml`.

    ```toml
    ### tidb-lightning configuration

    [lightning]
    # the HTTP port for debugging and Prometheus metrics pulling (0 to disable)
    pprof-port = 10089

    # Checks if the cluster satisfies the minimum requirement before starting.
    #check-requirements = true

    # The maximum number of tables to be handled concurrently.
    # This value affects the memory usage of tikv-importer.
    # Must not exceed the max-open-engines setting for tikv-importer.
    table-concurrency = 8

    # The concurrency number of data. It is set to the number of logical CPU
    # cores by default. When deploying together with other components, you can
    # set it to 75% of the size of logical CPU cores to limit the CPU usage.
    #region-concurrency =

    # The maximum I/O concurrency. Excessive I/O concurrency causes an increase in
    # I/O latency because the disk's internal buffer is frequently refreshed,
    # which causes the cache miss and slows down the read speed. Depending on the storage
    # medium, this value might need to be adjusted for optimal performance.
    io-concurrency = 5

    # Logging
    level = "info"
    file = "tidb-lightning.log"
    max-size = 128 # MB
    max-days = 28
    max-backups = 14

    [checkpoint]
    # Whether to enable checkpoints.
    # While importing, Lightning records which tables have been imported, so
    # even if Lightning or other component crashed, you could start from a known
    # good state instead of redoing everything.
    enable = true
    # The schema name (database name) to store the checkpoints
    schema = "tidb_lightning_checkpoint"
    # Where to store the checkpoints.
    #  - file:  store as a local file.
    #  - mysql: store into a remote MySQL-compatible database
    driver = "file"
    # The data source name (DSN) indicating the location of the checkpoint storage.
    # For the "file" driver, the DSN is a path. If the path is not specified, Lightning would
    # default to "/tmp/CHECKPOINT_SCHEMA.pb".
    # For the "mysql" driver, the DSN is a URL in the form of "USER:PASS@tcp(HOST:PORT)/".
    # If the URL is not specified, the TiDB server from the [tidb] section is used to
    # store the checkpoints. You should specify a different MySQL-compatible
    # database server to reduce the load of the target TiDB cluster.
    #dsn = "/tmp/tidb_lightning_checkpoint.pb"
    # Whether to keep the checkpoints after all data are imported. If false, the
    # checkpoints will be deleted. Keeping the checkpoints can aid debugging but
    # will leak metadata about the data source.
    #keep-after-success = false

    [tikv-importer]
    # The listening address of tikv-importer. Change it to the actual address.
    addr = "172.16.31.10:20170"

    [mydumper]
    # Block size for file reading. Keep it longer than the longest string of
    # the data source.
    read-block-size = 65536 # Byte (default = 64 KB)
    # mydumper local source data directory
    data-source-dir = "/data/my_database"
    # If no-schema is set to true, tidb-lightning assumes that the table skeletons
    # already exist on the target TiDB cluster, and will not execute the `CREATE
    # TABLE` statements
    no-schema = false
    # the character set of the schema files, containing CREATE TABLE statements;
    # only supports one of:
    #  - utf8mb4: the schema files must be encoded as UTF-8, otherwise Lightning
    #             will emit errors
    #  - gb18030: the schema files must be encoded as GB-18030, otherwise
    #             Lightning will emit errors
    #  - auto:    (default) automatically detects whether the schema is UTF-8 or
    #             GB-18030. An error is reported if the encoding is neither.
    #  - binary:  do not try to decode the schema files
    # note that the *data* files are always parsed as binary regardless of
    # schema encoding.
    character-set = "auto"

    [tidb]
    # Configuration of any TiDB server from the cluster
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    # Address of any PD server from the cluster
    pd-addr = "172.16.31.4:2379"
    # tidb-lightning imports TiDB as a library and generates some logs itself.
    # This setting controls the log level of the TiDB library.
    log-level = "error"

    # Sets the TiDB session variable to speed up the Checksum and Analyze operations.
    # See https://pingcap.com/docs/sql/statistics/#control-analyze-concurrency
    # for the meaning of each setting
    build-stats-concurrency = 20
    distsql-scan-concurrency = 100
    index-serial-scan-concurrency = 20
    checksum-table-concurrency = 16

    # When data importing is complete, tidb-lightning can automatically perform
    # the Checksum, Compact and Analyze operations. It is recommended to leave
    # these as true in the production environment.
    # The execution order: Checksum -> Analyze
    [post-restore]
    # Performs `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity.
    checksum = true
    # Performs compaction on the TiKV cluster.
    compact = true
    # Performs `ANALYZE TABLE <table>` for each table.
    analyze = true

    # Configures the background periodic actions
    # Supported units: h (hour), m (minute), s (second).
    [cron]
    # Duration between which Lightning automatically refreshes the import mode
    # status. Should be shorter than the corresponding TiKV setting.
    switch-mode = "5m"
    # Duration between which an import progress is printed to the log.
    log-progress = "5m"

    # Table filter options. See the corresponding section for details.
    #[black-white-list]
    # ...
    ```

4. Run `tidb-lightning`.

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```
