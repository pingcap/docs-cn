---
title: Migrate Data from MySQL SQL Files
summary: Learn how to migrate data from MySQL SQL files to TiDB using TiDB Lightning.
aliases: ['/docs/dev/migrate-from-mysql-mydumper-files/']
---

# Migrate Data from MySQL SQL Files

This document describes how to migrate data from MySQL SQL files to TiDB using TiDB Lightning. For details on how to generate MySQL SQL files, refer to [Mydumper](/mydumper-overview.md) or [Dumpling](/dumpling-overview.md).

The data migration process described in this document uses TiDB Lightning. The steps are as follows.

## Step 1: Deploy TiDB Lightning

Before you start the migration, [deploy TiDB Lightning](/tidb-lightning/deploy-tidb-lightning.md).

> **Note:**
>
> - If you choose the Local-backend to import data, the TiDB cluster cannot provide services during the import process. This mode imports data quickly, which is suitable for importing a large amount of data (above the TB level).
> - If you choose the TiDB-backend, the cluster can provide services normally during the import, at a slower import speed.
> - For detailed differences between the two backend modes, see [TiDB Lightning Backends](/tidb-lightning/tidb-lightning-backends.md).

## Step 2: Configure data source of TiDB Lightning

This document takes the TiDB-backend as an example. Create the `tidb-lightning.toml` configuration file and add the following major configurations in the file:

1. Set the `data-source-dir` under `[mydumper]` to the path of the MySQL SQL file.

    ```
    [mydumper]
    # Data source directory
    data-source-dir = "/data/export"
    ```

    > **Note:**
    >
    > If a corresponding schema already exists in the downstream, set `no-schema=true` to skip the creation of the schema.

2. Add the configuration of the target TiDB cluster.

    ```
    [tidb]
    # The target cluster information. Fill in one address of tidb-server.
    host = "172.16.31.1"
    port = 4000
    user = "root"
    password = ""
    ```

For other configurations, see [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

## Step 3: Run TiDB Lightning to import data

Run TiDB Lightning to start the import operation. If you start TiDB Lightning by using `nohup` directly in the command line, the program might exit because of the `SIGHUP` signal. Therefore, it is recommended to write `nohup` in a script. For example:

```bash
# !/bin/bash
nohup ./tidb-lightning -config tidb-lightning.toml > nohup.out &
```

When the import operation is started, view the progress by the following two ways:

- `grep` the keyword `progress` in logs, which is updated every 5 minutes by default.
- Access the monitoring dashboard. See [Monitor TiDB Lightning](/tidb-lightning/monitor-tidb-lightning.md) for details.
