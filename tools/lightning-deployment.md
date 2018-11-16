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

`tidb-lightning` and `tikv-importer` are both resource-intensive programs. It is recommended to deploy them into two separate machines. If your hardware resources are limited, you can deploy `tidb-lightning` and `tikv-importer` on the same machine.

### Hardware requirements of separate deployment

To achieve the best performance, it is recommended to use the following hardware configuration:

- `tidb-lightning`:

    - 32+ logical cores CPU
    - 16 GB+ memory
    - 1 TB+ SSD, preferring higher read speed
    - 10 Gigabit network card
    - `tidb-lightning` fully consumes all CPU cores when running,
        and deploying on a dedicated machine is highly recommended.
        If not possible, `tidb-lightning` could be deployed together with other components like
        `tidb-server`, and the CPU usage could be limited via the `region-concurrency` setting.

- `tikv-importer`:

    - 32+ logical cores CPU
    - 32 GB+ memory
    - 1 TB+ SSD, preferring higher IOPS
    - 10 Gigabit network card
    - `tikv-importer` fully consumes all CPU, disk I/O and network bandwidth when running,
        and deploying on a dedicated machine is strongly recommended.
        If not possible, `tikv-importer` could be deployed together with other components like
        `tikv-server`, but the import speed might be affected.

If you have sufficient machines, you can deploy multiple Lightning/Importer servers, with each working on a distinct set of tables, to import the data in parallel.

### Hardware requirements of mixed deployment

If your hardware resources are severely under constraint, it is possible to deploy `tidb-lightning` and `tikv-importer` and other components on the same machine, but the import performance is affected.

It is recommended to use the following configuration of the single machine:

- 32+ logical cores CPU
- 32 GB+ memory
- 1 TB+ SSD, preferring higher IOPS
- 10 Gigabit network card

> **Notes:** `tidb-lightning` is a CPU intensive program. In an environment with mixed components, the resources allocated to `tidb-lightning` must be limited. Otherwise, other components might not be able to run. It is recommended to set the `region-concurrency` to 75% of CPU logical cores. For instance, if the CPU has 32 logical cores, you can set the `region-concurrency` to 24.

## Deploy TiDB-Lightning

This section describes two deployment methods of TiDB-Lightning:

- [Deploy TiDB-Lightning using Ansible](#deploy-tidb-lightning-using-ansible)
- [Deploy TiDB-Lightning manually](#deploy-tidb-lightning-manually)

### Deploy TiDB-Lightning using Ansible

You can deploy TiDB-Lightning using Ansible together with the [deployment of the TiDB cluster itself using Ansible](../op-guide/ansible-deployment.md).

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

- **v2.1**: https://download.pingcap.org/tidb-lightning-release-2.1-linux-amd64.tar.gz
- **v2.0**: https://download.pingcap.org/tidb-lightning-release-2.0-linux-amd64.tar.gz

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
    import-dir = "/tmp/tikv/import"
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
    # The data source name (DSN) in the form of "USER:PASS@tcp(HOST:PORT)/".
    # If not specified, the TiDB server from the [tidb] section will be used to
    # store the checkpoints. You could also specify a different MySQL-compatible
    # database server to reduce the load of the target TiDB cluster.
    #dsn = "root@tcp(127.0.0.1:4000)/"
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
    read-block-size = 4096 # Byte (default = 4 KB)
    # Each data file is split into multiple chunks of this size. Each chunk
    # is processed in parallel.
    region-min-size = 268435456 # Byte (default = 256 MB)
    # mydumper local source data directory
    data-source-dir = "/data/my_database"
    # If no-schema is set to true, tidb-lightning assumes that the table skeletons
    # already exist on the target TiDB cluster, and will not execute the `CREATE
    # TABLE` statements
    no-schema = false

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
    distsql-scan-concurrency = 16

    # When data importing is complete, tidb-lightning can automatically perform
    # the Checksum, Compact and Analyze operations. It is recommended to leave
    # these as true in the production environment.
    # The execution order: Checksum -> Compact -> Analyze
    [post-restore]
    # Performs `ADMIN CHECKSUM TABLE <table>` for each table to verify data integrity.
    checksum = true
    # Performs compaction on the TiKV cluster.
    compact = true
    # Performs `ANALYZE TABLE <table>` for each table.
    analyze = true
    ```

4. Run `tidb-lightning`.

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```