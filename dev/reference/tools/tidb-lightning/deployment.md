---
title: TiDB Lightning Deployment
summary: Deploy TiDB Lightning to quickly import large amounts of new data.
category: reference
---

# TiDB Lightning Deployment

This document describes the hardware requirements of TiDB Lightning on separate deployment and mixed deployment, and how to deploy it using Ansible or manually.

## Notes

Before starting TiDB Lightning, note that:

- During the import process, the cluster cannot provide normal services.
- If `tidb-lightning` crashes, the cluster is left in "import mode". Forgetting to switch back to "normal mode" can lead to a high amount of uncompacted data on the TiKV cluster, and cause abnormally high CPU usage and stall. You can manually switch the cluster back to "normal mode" via the `tidb-lightning-ctl` tool:

    ```sh
    bin/tidb-lightning-ctl -switch-mode=normal
    ```

- TiDB Lightning is required to have the following privileges in the downstream TiDB:

    | Privilege | Scope |
    |----:|:------|
    | SELECT | Tables |
    | INSERT | Tables |
    | UPDATE | Tables |
    | DELETE | Tables |
    | CREATE | Databases, tables |
    | DROP | Databases, tables |
    | ALTER | Tables |

    If the `checksum` configuration item of TiDB Lightning is set to `true`, then the admin user privileges in the downstream TiDB need to be granted to TiDB Lightning.

## Hardware requirements

`tidb-lightning` and `tikv-importer` are both resource-intensive programs. It is recommended to deploy them into two separate machines.

To achieve the best performance, it is recommended to use the following hardware configuration:

- `tidb-lightning`:

    - 32+ logical cores CPU
    - An SSD large enough to store the entire data source, preferring higher read speed
    - 10 Gigabit network card (capable of transferring at ≥300 MB/s)
    - `tidb-lightning` fully consumes all CPU cores when running,
        and deploying on a dedicated machine is highly recommended.
        If not possible, `tidb-lightning` could be deployed together with other components like
        `tidb-server`, and the CPU usage could be limited via the `region-concurrency` setting.

- `tikv-importer`:

    - 32+ logical cores CPU
    - 40 GB+ memory
    - 1 TB+ SSD, preferring higher IOPS (≥ 8000 is recommended)
        * The disk should be larger than the total size of the top N tables, where N = max(index-concurrency, table-concurrency).
    - 10 Gigabit network card (capable of transferring at ≥300 MB/s)
    - `tikv-importer` fully consumes all CPU, disk I/O and network bandwidth when running,
        and deploying on a dedicated machine is strongly recommended.

If you have sufficient machines, you can deploy multiple Lightning/Importer servers, with each working on a distinct set of tables, to import the data in parallel.

> **Note:**
>
> - `tidb-lightning` is a CPU intensive program. In an environment with mixed components, the resources allocated to `tidb-lightning` must be limited. Otherwise, other components might not be able to run. It is recommended to set the `region-concurrency` to 75% of CPU logical cores. For instance, if the CPU has 32 logical cores, you can set the `region-concurrency` to 24.
>
> - `tikv-importer` stores intermediate data on the RAM to speed up the import process. The typical memory usage can be calculated by using **(`max-open-engines` × `write-buffer-size` × 2) + (`num-import-jobs` × `region-split-size` × 2)**. If the speed of writing to disk is slow, the memory usage could be even higher due to buffering.

Additionally, the target TiKV cluster should have enough space to absorb the new data.
Besides [the standard requirements](/dev/how-to/deploy/hardware-recommendations.md), the total free space of the target TiKV cluster should be larger than **Size of data source × [Number of replicas](/dev/faq/tidb.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it) × 2**.

With the default replica count of 3, this means the total free space should be at least 6 times the size of data source.

## Export data

Use the [`mydumper` tool](/dev/reference/tools/mydumper.md) to export data from MySQL by using the following command:

```sh
./bin/mydumper -h 127.0.0.1 -P 3306 -u root -t 16 -F 256 -B test -T t1,t2 --skip-tz-utc -o /data/my_database/
```

In this command,

- `-B test`: means the data is exported from the `test` database.
- `-T t1,t2`: means only the `t1` and `t2` tables are exported.
- `-t 16`: means 16 threads are used to export the data.
- `-F 256`: means a table is partitioned into chunks and one chunk is 256 MB.
- `--skip-tz-utc`: the purpose of adding this parameter is to ignore the inconsistency of time zone setting between MySQL and the data exporting machine, and to disable automatic conversion.

If the data source consists of CSV files, see [CSV support](/dev/reference/tools/tidb-lightning/csv.md) for configuration.

## Deploy TiDB Lightning

This section describes two deployment methods of TiDB Lightning:

- [Deploy TiDB Lightning using Ansible](#deploy-tidb-lightning-using-ansible)
- [Deploy TiDB Lightning manually](#deploy-tidb-lightning-manually)

### Deploy TiDB Lightning using Ansible

You can deploy TiDB Lightning using Ansible together with the [deployment of the TiDB cluster itself using Ansible](/dev/how-to/deploy/orchestrated/ansible.md).

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
        tikv_importer_port: 8287
        ...
        ```

    * `group_vars/lightning_server.yml`

        ```yaml
        ---
        dummy:

        # The listening port for metrics gathering. Should be open to the monitoring servers.
        tidb_lightning_pprof_port: 8289

        # The file path that tidb-lightning reads the data source (Mydumper SQL dump or CSV) from.
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

### Deploy TiDB Lightning manually

#### Step 1: Deploy a TiDB cluster

Before importing data, you need to have a deployed TiDB cluster, with the cluster version 2.0.9 or above. It is highly recommended to use the latest version.

You can find deployment instructions in [TiDB Quick Start Guide](https://pingcap.com/docs/QUICKSTART/).

#### Step 2: Download the TiDB Lightning installation package

Follow the link to download the TiDB Lightning package (choose the same version as that of the TiDB cluster):

- [**v3.0**](/v3.0/reference/tools/download.md#tidb-lightning)
- [**v2.1**](/v2.1/reference/tools/download.md#tidb-binlog-and-tidb-lightning)
- [Latest unstable version](/dev/reference/tools/download.md#tidb-lightning)

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
    addr = "0.0.0.0:8287"

    [metric]
    # The Prometheus client push job name.
    job = "tikv-importer"
    # The Prometheus client push interval.
    interval = "15s"
    # The Prometheus Pushgateway address.
    address = ""

    [import]
    # The directory to store engine files.
    import-dir = "/mnt/ssd/data.import/"
    ```

    The above only shows the essential settings. See the [Configuration](/dev/reference/tools/tidb-lightning/config.md#tikv-importer) section for the full list of settings.

3. Run `tikv-importer`.

    ```sh
    nohup ./tikv-importer -C tikv-importer.toml > nohup.out &
    ```

#### Step 4: Start `tidb-lightning`

1. Upload `bin/tidb-lightning` and `bin/tidb-lightning-ctl` from the tool set.

2. Mount the data source onto the same machine.

3. Configure `tidb-lightning.toml`. For configurations that do not appear in the template below, TiDB Lightning writes a configuration error to the log file and exits.

    ```toml
    [lightning]
    # The concurrency number of data. It is set to the number of logical CPU
    # cores by default. When deploying together with other components, you can
    # set it to 75% of the size of logical CPU cores to limit the CPU usage.
    # region-concurrency =

    # Logging
    level = "info"
    file = "tidb-lightning.log"

    [tikv-importer]
    # The listening address of tikv-importer. Change it to the actual address.
    addr = "172.16.31.10:8287"

    [mydumper]
    # mydumper local source data directory
    data-source-dir = "/data/my_database"

    [tidb]
    # Configuration of any TiDB server from the cluster
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    ```

    The above only shows the essential settings.
    See the [Configuration](/dev/reference/tools/tidb-lightning/config.md#tidb-lightning-global) section for the full list of settings.

4. Run `tidb-lightning`.

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```
