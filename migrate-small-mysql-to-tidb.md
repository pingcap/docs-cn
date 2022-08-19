---
title: Migrate MySQL of Small Datasets to TiDB
summary: Learn how to migrate MySQL of small datasets to TiDB.
aliases: ['/tidb/dev/usage-scenario-incremental-migration/']
---

# Migrate MySQL of Small Datasets to TiDB

This document describes how to use TiDB Data Migration (DM) to migrate MySQL of small datasets to TiDB in the full migration mode and incremental replication mode. "Small datasets" in this document mean data size less than 1 TiB.

The migration speed varies from 30 GB/h to 50 GB/h, depending on multiple factors such as the number of indexes in the table schema, hardware, and network environment. <!--The migration process using DM is shown in the figure below.-->

<!--/media/dm/migrate-with-dm.png-->

## Prerequisites

- [Deploy a DM Cluster Using TiUP](/dm/deploy-a-dm-cluster-using-tiup.md)
- [Grant the required privileges for the source database and the target database of DM](/dm/dm-worker-intro.md)

## Step 1. Create the data source

First, create the `source1.yaml` file as follows:

{{< copyable "" >}}

```yaml
# The ID must be unique.
source-id: "mysql-01"

# Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable GTID, the upstream MySQL must have enabled GTID. If the upstream MySQL has automatic source-replica switching, the GTID mode is required.
enable-gtid: true

from:
  host: "${host}"         # For example: 172.16.10.81
  user: "root"
  password: "${password}" # Plaintext password is supported but not recommended. It is recommended to use dmctl encrypt to encrypt the plaintext password before using the password.
  port: 3306
```

Then, load the data source configuration to the DM cluster using `tiup dmctl` by running the following command:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
```

The parameters used in the command above are described as follows:

|Parameter      |Description|
|  :-        |    :-           |
|`--master-addr`  |`{advertise-addr}` of any DM-master node in the cluster where `dmctl` is to connect. For example, 172.16.10.71:8261.
|`operate-source create`|Load the data source to the DM cluster.|

## Step 2. Create the migration task

Create the `task1.yaml` file as follows:

{{< copyable "" >}}

```yaml
# Task name. Each of the multiple tasks running at the same time must have a unique name.
name: "test"
# Task mode. Options are:
# full: only performs full data migration.
# incremental: only performs binlog real-time replication.
# all: full data migration + binlog real-time replication.
task-mode: "all"
# The configuration of the target TiDB database.
target-database:
  host: "${host}"                   # For example: 172.16.10.83
  port: 4000
  user: "root"
  password: "${password}"           # Plaintext password is supported but not recommended. It is recommended to use dmctl encrypt to encrypt the plaintext password before using the password.

# The configuration of all MySQL instances of source database required for the current migration task.
mysql-instances:
-
  # The ID of an upstream instance or a replication group
  source-id: "mysql-01"
  # The names of the block list and allow list configuration of the schema name or table name that is to be migrated. These names are used to reference the global configuration of the block and allowlist. For the global configuration, refer to the `block-allow-list` configuration below.
  block-allow-list: "listA"

# The global configuration of blocklist and allowlist. Each instance is referenced by a configuration item name.
block-allow-list:
  listA:                              # name
    do-tables:                        # The allowlist of upstream tables that need to be migrated.
    - db-name: "test_db"              # The schema name of the table to be migrated.
      tbl-name: "test_table"          # The name of the table to be migrated.

```

The above is the minimum task configuration to perform the migration. For more configuration items regarding the task, refer to [DM task complete configuration file introduction](/dm/task-configuration-file-full.md).

## Step 3. Start the migration task

To avoid errors, before starting the migration task, it is recommended to use the `check-task` command to check whether the configuration meets the requirements of DM configuration.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

Start the migration task by running the following command with `tiup dmctl`.

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

The parameters used in the command above are described as follows:

|Parameter|Description|
|     -    |     -     |
|`--master-addr`| `{advertise-addr}` of any DM-master node in the cluster where `dmctl` is to connect. For example: 172.16.10.71:8261. |
|`start-task`| Start the migration task |

If the task fails to start, after changing the configuration according to the returned result, you can run the `start-task task.yaml` command to restart the task. If you encounter problems, refer to [Handle Errors](/dm/dm-error-handling.md) and [FAQ](/dm/dm-faq.md).

## Step 4: Check the migration task status

To learn whether the DM cluster has an ongoing migration task, the task status and some other information, run the `query-status` command using `tiup dmctl`:

{{< copyable "shell-regular" >}}

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For a detailed interpretation of the results, refer to [Query Status](/dm/dm-query-status.md).

## Step 5. Monitor the task and view logs （optional)

To view the historical status of the migration task and other internal metrics, take the following steps.

If you have deployed Prometheus, Alertmanager, and Grafana when deploying DM using TiUP, you can access Grafana using the IP address and port specified during the deployment. You can then select the DM dashboard to view DM-related monitoring metrics.

- The log directory of DM-master: specified by the DM-master process parameter `--log-file`. If you have deployd DM using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/` by default.
- The log directory of DM-worker: specified by the DM-worker process parameter `--log-file`. If you have deployd DM using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/` by default.

## What's next

- [Pause the migration task](/dm/dm-pause-task.md)
- [Resume the migration task](/dm/dm-resume-task.md)
- [Stop the migration task](/dm/dm-stop-task.md)
- [Export and import the cluster data source and task configuration](/dm/dm-export-import-config.md)
- [Handle failed DDL statements](/dm/handle-failed-ddl-statements.md)
