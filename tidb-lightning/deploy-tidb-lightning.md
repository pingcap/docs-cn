---
title: TiDB Lightning Deployment
summary: Deploy TiDB Lightning to quickly import large amounts of new data.
aliases: ['/docs/dev/tidb-lightning/deploy-tidb-lightning/','/docs/dev/reference/tools/tidb-lightning/deployment/']
---

# TiDB Lightning Deployment

This document describes the hardware requirements of TiDB Lightning using the Local-backend, and how to deploy it using TiDB Ansible or manually.

If you do not want the TiDB services to be impacted, read [TiDB Lightning TiDB-backend](/tidb-lightning/tidb-lightning-backends.md#tidb-lightning-tidb-backend) for the changes to the deployment steps.

## Notes

Before starting TiDB Lightning, note that:

- During the import process, the cluster cannot provide normal services.
- If `tidb-lightning` crashes, the cluster is left in "import mode". Forgetting to switch back to "normal mode" can lead to a high amount of uncompacted data on the TiKV cluster, and cause abnormally high CPU usage and stall. You can manually switch the cluster back to "normal mode" via the `tidb-lightning-ctl` tool:

    ```sh
    bin/tidb-lightning-ctl --switch-mode=normal
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

`tidb-lightning` is a resource-intensive program. It is recommended to deploy it as follows.

- 32+ logical cores CPU
- 20GB+ memory
- An SSD large enough to store the entire data source, preferring higher read speed
- 10 Gigabit network card (capable of transferring at ≥1 GB/s)
- `tidb-lightning` fully consumes all CPU cores when running, and deploying on a dedicated machine is highly recommended. If not possible, `tidb-lightning` could be deployed together with other components like `tidb-server`, and the CPU usage could be limited via the `region-concurrency` setting.

> **Note:**
>
> - `tidb-lightning` is a CPU intensive program. In an environment with mixed components, the resources allocated to `tidb-lightning` must be limited. Otherwise, other components might not be able to run. It is recommended to set the `region-concurrency` to 75% of CPU logical cores. For instance, if the CPU has 32 logical cores, you can set the `region-concurrency` to 24.

Additionally, the target TiKV cluster should have enough space to absorb the new data.
Besides [the standard requirements](/hardware-and-software-requirements.md), the total free space of the target TiKV cluster should be larger than **Size of data source × [Number of replicas](/faq/deploy-and-maintain-faq.md#is-the-number-of-replicas-in-each-region-configurable-if-yes-how-to-configure-it) × 2**.

With the default replica count of 3, this means the total free space should be at least 6 times the size of data source.

## Export data

Use the [`dumpling` tool](/dumpling-overview.md) to export data from MySQL by using the following command:

```sh
./bin/dumpling -h 127.0.0.1 -P 3306 -u root -t 16 -F 256MB -B test -f 'test.t[12]' -o /data/my_database/
```

In this command,

- `-B test`: means the data is exported from the `test` database.
- `-f test.t[12]`: means only the `test.t1` and `test.t2` tables are exported.
- `-t 16`: means 16 threads are used to export the data.
- `-F 256MB`: means a table is partitioned into chunks and one chunk is 256 MB.

If the data source consists of CSV files, see [CSV support](/tidb-lightning/migrate-from-csv-using-tidb-lightning.md) for configuration.

## Deploy TiDB Lightning

This section describes two deployment methods of TiDB Lightning:

- [Deploy TiDB Lightning using TiDB Ansible](#deploy-tidb-lightning-using-tidb-ansible)
- [Deploy TiDB Lightning manually](#deploy-tidb-lightning-manually)

### Deploy TiDB Lightning using TiDB Ansible

You can deploy TiDB Lightning using TiDB Ansible together with the [deployment of the TiDB cluster itself using TiDB Ansible](/online-deployment-using-ansible.md).

1. Edit `inventory.ini` to configure an IP address for `tidb-lightning`.

    ```ini
    ...

    [lightning_server]
    192.168.20.10

    ...
    ```

2. Configure `tidb-lightning` by editing the settings under `group_vars/*.yml`.

    * `group_vars/lightning_server.yml`

        ```yaml
        ---
        dummy:

        # The listening port for metrics gathering. Should be open to the monitoring servers.
        tidb_lightning_pprof_port: 8289

        # The file path that tidb-lightning reads the data source (Dumpling SQL dump or CSV) from.
        data_source_dir: "{{ deploy_dir }}/mydumper"
        ```

3. Deploy the cluster.

    ```sh
    ansible-playbook bootstrap.yml &&
    ansible-playbook deploy.yml
    ```

4. Mount the data source to the path specified in the `data_source_dir` setting.

5. Log in to the `tidb-lightning` server and edit the `conf/tidb-lighting.toml` file as follows:

    ```
    [tikv-importer]
    # Uses the Local-backend.
    backend = "local"
    # Sets the directory for temporarily storing the sorted key-value pairs.
    # The target directory must be empty.
    "sorted-kv-dir" = "/mnt/ssd/sorted-kv-dir"

    [tidb]
    # An address of pd-server.
    pd-addr = "172.16.31.4:2379
    ```

6. Log in to the `tidb-lightning` server, and manually run the following command to start Lightning and import the data into the TiDB cluster.

    ```sh
    scripts/start_lightning.sh
    ```

### Deploy TiDB Lightning manually

#### Step 1: Deploy a TiDB cluster

Before importing data, you need to have a deployed TiDB cluster, with the cluster version 2.0.9 or above. It is highly recommended to use the latest version.

You can find deployment instructions in [TiDB Quick Start Guide](/quick-start-with-tidb.md).

#### Step 2: Download the TiDB Lightning installation package

Refer to the [TiDB enterprise tools download page](/download-ecosystem-tools.md#tidb-lightning) to download the TiDB Lightning package (choose the same version as that of the TiDB cluster).

#### Step 3: Start `tidb-lightning`

1. Upload `bin/tidb-lightning` and `bin/tidb-lightning-ctl` from the tool set.

2. Mount the data source onto the same machine.

3. Configure `tidb-lightning.toml`. For configurations that do not appear in the template below, TiDB Lightning writes a configuration error to the log file and exits. `sorted-kv-dir` must be an empty directory and the disk where the directory is located must have a lot of free space.

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
    # Sets the backend to the "local" mode.
    backend = "local"
    # Sets the directory of temporary local storage.
    sorted-kv-dir = "/mnt/ssd/sorted-kv-dir"

    [mydumper]
    # Local source data directory
    data-source-dir = "/data/my_database"

    [tidb]
    # Configuration of any TiDB server from the cluster
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    # Table schema information is fetched from TiDB via this status-port.
    status-port = 10080
    # An address of pd-server.
    pd-addr = "172.16.31.4:2379"
    ```

    The above only shows the essential settings.
    See the [Configuration](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global) section for the full list of settings.

4. Run `tidb-lightning`.

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## Upgrading TiDB Lightning

You can upgrade TiDB Lightning by replacing the binaries alone. No further configuration is needed. See [FAQ](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning) for the detailed instructions of restarting TiDB Lightning.

If an import task is running, we recommend you to wait until it finishes before upgrading TiDB Lightning. Otherwise, there might be chances that you need to reimport from scratch, because there is no guarantee that checkpoints work across versions.
