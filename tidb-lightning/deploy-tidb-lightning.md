---
title: Deploy TiDB Lightning
summary: Deploy TiDB Lightning to quickly import large amounts of new data.
aliases: ['/docs/dev/tidb-lightning/deploy-tidb-lightning/','/docs/dev/reference/tools/tidb-lightning/deployment/']
---

# Deploy TiDB Lightning

This document describes the hardware requirements of using TiDB Lightning to import data, and how to deploy it manually. Requirements on hardware resources vary with the import modes. For details, refer to the following docs:

- [Physical Import Mode Requirements and Limitations](/tidb-lightning/tidb-lightning-physical-import-mode.md#requirements-and-restrictions)
- [Logical Import Mode Requirements and Limitations](/tidb-lightning/tidb-lightning-logical-import-mode.md)

## Online deployment using TiUP (recommended)

1. Install TiUP using the following command:

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

    This command automatically adds TiUP to the `PATH` environment variable. You need to start a new terminal session or run `source ~/.bashrc` before you can use TiUP. (According to your environment, you may need to run `source ~/.profile`. For the specific command, check the output of TiUP.)

2. Install TiDB Lightning using TiUP:

    ```shell
    tiup install tidb-lightning
    ```

## Manual deployment

### Download TiDB Lightning binaries

Refer to [Download TiDB Tools](/download-ecosystem-tools.md) and download TiDB Lightning binaries. TiDB Lightning is completely compatible with early versions of TiDB. It is recommended to use the latest version of TiDB Lightning.

Unzip the TiDB Lightning binary package to obtain the `tidb-lightning` executable file:

```bash
tar -zxvf tidb-lightning-${version}-linux-amd64.tar.gz
chmod +x tidb-lightning
```

In this command,

- `-B test`: means the data is exported from the `test` database.
- `-f test.t[12]`: means only the `test.t1` and `test.t2` tables are exported.
- `-t 16`: means 16 threads are used to export the data.
- `-F 256MB`: means a table is partitioned into chunks and one chunk is 256 MB.

If the data source consists of CSV files, see [CSV support](/tidb-lightning/tidb-lightning-data-source.md#csv) for configuration.

## Deploy TiDB Lightning

This section describes how to [deploy TiDB Lightning manually](#deploy-tidb-lightning-manually).

### Deploy TiDB Lightning manually

#### Step 1: Deploy a TiDB cluster

Before importing data, you need to have a deployed TiDB cluster. It is highly recommended to use the latest stable version.

You can find deployment instructions in [TiDB Quick Start Guide](/quick-start-with-tidb.md).

#### Step 2: Download the TiDB Lightning installation package

Refer to the [Download TiDB Tools](/download-ecosystem-tools.md) document to download the TiDB Lightning package.

> **Note:**
>
> TiDB Lightning is compatible with TiDB clusters of earlier versions. It is recommended that you download the latest stable version of the TiDB Lightning installation package.

#### Step 3: Start `tidb-lightning`

1. Upload `bin/tidb-lightning` and `bin/tidb-lightning-ctl` from the tool set.

2. Mount the data source onto the same machine.

3. Configure `tidb-lightning.toml`. For configurations that do not appear in the template below, TiDB Lightning writes a configuration error to the log file and exits.

    `sorted-kv-dir` sets the temporary storage directory for the sorted Key-Value files. The directory must be empty, and the storage space **must be greater than the size of the dataset to be imported**. See [Downstream storage space requirements](/tidb-lightning/tidb-lightning-requirements.md#storage-space-of-the-target-database) for details.

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

    The above only shows the essential settings. See the [Configuration](/tidb-lightning/tidb-lightning-configuration.md#tidb-lightning-global) section for the full list of settings.

4. Run `tidb-lightning`.

    ```sh
    nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
    ```

## Upgrade TiDB Lightning

You can upgrade TiDB Lightning by replacing the binaries alone without further configurations. After the upgrade, you need to restart TiDB Lightning. For details, see [How to properly restart TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#how-to-properly-restart-tidb-lightning).

If an import task is running, we recommend you to wait until it finishes before upgrading TiDB Lightning. Otherwise, there might be chances that you need to reimport from scratch, because there is no guarantee that checkpoints work across versions.
