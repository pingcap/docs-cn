---
title: Migrate Data from Amazon Aurora to TiDB
summary: Learn how to migrate data from Amazon Aurora to TiDB using DB snapshot.
aliases: ['/tidb/dev/migrate-from-aurora-using-lightning','/docs/dev/migrate-from-aurora-mysql-database/','/docs/dev/how-to/migrate/from-mysql-aurora/','/docs/dev/how-to/migrate/from-aurora/', '/tidb/dev/migrate-from-aurora-mysql-database/', '/tidb/dev/migrate-from-mysql-aurora/','/tidb/stable/migrate-from-aurora-using-lightning/']
---

# Migrate Data from Amazon Aurora to TiDB

This document describes how to migrate data from Amazon Aurora to TiDB. The migration process uses [DB snapshot](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Managing.Backups.html), which saves a lot of space and time.

The whole migration has two processes:

- Import full data to TiDB using TiDB Lightning
- Replicate incremental data to TiDB using DM (optional)

## Prerequisites

- [Install Dumpling and TiDB Lightning](/migration-tools.md). If you want to create the corresponding tables manually on the target side, do not install Dumpling.
- [Get the upstream database privileges required by Dumpling](/dumpling-overview.md#required-privileges).
- [Get the target database privileges required for TiDB Lightning](/tidb-lightning/tidb-lightning-faq.md#what-are-the-privilege-requirements-for-the-target-database).

## Import full data to TiDB

### Step 1. Export and import the schema file

This section describes how to export the schema file from Amazon Aurora and import it to TiDB. If you have manually created the table in the target database, you can skip this step.

#### 1.1 Export the schema file from Amazon Aurora

Because the snapshot file from Amazon Aurora does not contain the DDL statements, you need to export the schema using Dumpling and create the schema in the target database using TiDB Lightning.

Export the schema using Dumpling by running the following command. The command includes the `--filter` parameter to only export the desired table schema. For more information about the parameters, see the [Option list of Dumpling](/dumpling-overview.md#option-list-of-dumpling).

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
tiup dumpling --host ${host} --port 3306 --user root --password ${password} --filter 'my_db1.table[12],mydb.*' --consistency none --no-data --output 's3://my-bucket/schema-backup'
```

Record the URI of the schema exported in the above command, such as 's3://my-bucket/schema-backup', which will be used when importing the schema file later.

To get access to Amazon S3, you can pass the secret access key and access key of the account that has access to this Amazon S3 storage path into the Dumpling or TiDB Lightning node as environment variables. Dumpling and TiDB Lightning also support reading credential files from `~/.aws/credentials`. This method eliminates the need to provide the secret access key and access key again for all tasks on that Dumpling or TiDB Lightning node.

#### 1.2 Create the TiDB Lightning configuration file for the schema file

Create a new `tidb-lightning-schema.toml` file, copy the following content into the file, and replace the corresponding content.

```toml
[tidb]

# The target TiDB cluster information.
host = ${host}
port = ${port}
user = "${user_name}
password = "${password}"
status-port = ${status-port}  # The TiDB status port. Usually the port is 10080.
pd-addr = "${ip}:${port}"     # The cluster PD address. Usually the port is 2379.

[tikv-importer]
# "local": Use the default Physical Import Mode (the "local" backend).
# During the import, the target TiDB cluster cannot provide any service.
# For more information about import modes, see https://docs.pingcap.com/tidb/stable/tidb-lightning-overview
backend = "local"

# Set the temporary storage directory for the sorted Key-Value files.
# The directory must be empty, and the storage space must be greater than the size of the dataset to be imported.
# For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage,
# which can use I/O exclusively.
sorted-kv-dir = "${path}"

[mydumper]
# Set the directory of the schema file exported from Amazon Aurora
data-source-dir = "s3://my-bucket/schema-backup"
```

If you need to enable TLS in the TiDB cluster, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

#### 1.3 Import the schema file to TiDB

Use TiDB Lightning to import the schema file to the downstream TiDB.

```shell
export AWS_ACCESS_KEY_ID=${access_key}
export AWS_SECRET_ACCESS_KEY=${secret_key}
nohup tiup tidb-lightning -config tidb-lightning-schema.toml > nohup.out 2>&1 &
```

### Step 2. Export and import an Amazon Aurora snapshot to Amazon S3

This section describes how to export an Amazon Aurora snapshot to Amazon S3 and import it into TiDB by TiDB Lightning.

#### 2.1 Export an Amazon Aurora snapshot to Amazon S3

1. Get the name and location of the Amazon Aurora binlog for subsequent incremental migration. In Amazon Aurora, run the `SHOW MASTER STATUS` command and record the current binlog position:

    ```sql
    SHOW MASTER STATUS;
    ```

    The output is similar to the following. Record the binlog name and position for later use.

    ```
    +----------------------------+----------+--------------+------------------+-------------------+
    | File                       | Position | Binlog_Do_DB | Binlog_Ignore_DB | Executed_Gtid_Set |
    +----------------------------+----------+--------------+------------------+-------------------+
    | mysql-bin-changelog.018128 |    52806 |              |                  |                   |
    +----------------------------+----------+--------------+------------------+-------------------+
    1 row in set (0.012 sec)
    ```

2. Export the Amazon Aurora snapshot. For detailed steps, refer to [Exporting DB snapshot data to Amazon S3](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/USER_ExportSnapshot.html). After you obtain the binlog position, export the snapshot within 5 minutes. Otherwise, the recorded binlog position might be outdated and thus cause data conflict during the incremental replication.

#### 2.2 Create the TiDB Lightning configuration file for the data file

Create a new `tidb-lightning-data.toml` configuration file, copy the following content into the file, and replace the corresponding content.

```toml
[tidb]

# The target TiDB cluster information.
host = ${host}
port = ${port}
user = "${user_name}
password = "${password}"
status-port = ${status-port}  # The TiDB status port. Usually the port is 10080.
pd-addr = "${ip}:${port}"     # The cluster PD address. Usually the port is 2379.

[tikv-importer]
# "local": Use the default Physical Import Mode (the "local" backend).
# During the import, the target TiDB cluster cannot provide any service.
# For more information about import modes, see https://docs.pingcap.com/tidb/stable/tidb-lightning-overview
backend = "local"

# Set the temporary storage directory for the sorted Key-Value files.
# The directory must be empty, and the storage space must be greater than the size of the dataset to be imported.
# For better import performance, it is recommended to use a directory different from `data-source-dir` and use flash storage,
# which can use I/O exclusively.
sorted-kv-dir = "${path}"

[mydumper]
# Set the directory of the snapshot file exported from Amazon Aurora
data-source-dir = "${s3_path}"  # eg: s3://my-bucket/sql-backup

[[mydumper.files]]
# The expression that parses the parquet file.
pattern = '(?i)^(?:[^/]*/)*([a-z0-9_]+)\.([a-z0-9_]+)/(?:[^/]*/)*(?:[a-z0-9\-_.]+\.(parquet))$'
schema = '$1'
table = '$2'
type = '$3'
```

If you need to enable TLS in the TiDB cluster, refer to [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md).

#### 2.3 Import full data to TiDB

1. Use TiDB Lightning to import data from an Amazon Aurora snapshot to TiDB.

    ```shell
    export AWS_ACCESS_KEY_ID=${access_key}
    export AWS_SECRET_ACCESS_KEY=${secret_key}
    nohup tiup tidb-lightning -config tidb-lightning-data.toml > nohup.out 2>&1 &
    ```

2. After the import starts, you can check the progress of the import by either of the following methods:

    - `grep` the keyword `progress` in the log. The progress is updated every 5 minutes by default.
    - Check progress in [the monitoring dashboard](/tidb-lightning/monitor-tidb-lightning.md).
    - Check progress in [the TiDB Lightning web interface](/tidb-lightning/tidb-lightning-web-interface.md).

3. After TiDB Lightning completes the import, it exits automatically. Check whether `tidb-lightning.log` contains `the whole procedure completed` in the last lines. If yes, the import is successful. If no, the import encounters an error. Address the error as instructed in the error message.

> **Note:**
>
> Whether the import is successful or not, the last line of the log shows `tidb lightning exit`. It means that TiDB Lightning exits normally, but does not necessarily mean that the import is successful.

If you encounter any problem during the import, refer to [TiDB Lightning FAQ](/tidb-lightning/tidb-lightning-faq.md) for troubleshooting.

## Replicate incremental data to TiDB (optional)

### Prerequisites

- [Install DM](/dm/deploy-a-dm-cluster-using-tiup.md).
- [Get the source database and target database privileges required for DM](/dm/dm-worker-intro.md).

### Step 1: Create the data source

1. Create the `source1.yaml` file as follows:

    ```yaml
    # Must be unique.
    source-id: "mysql-01"
    # Configures whether DM-worker uses the global transaction identifier (GTID) to pull binlogs. To enable this mode, the upstream MySQL must also enable GTID. If the upstream MySQL service is configured to switch master between different nodes automatically, GTID mode is required.
    enable-gtid: false

    from:
      host: "${host}"         # e.g.: 172.16.10.81
      user: "root"
      password: "${password}" # Supported but not recommended to use plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.
      port: 3306
    ```

2. Load the data source configuration to the DM cluster using `tiup dmctl` by running the following command:

    ```shell
    tiup dmctl --master-addr ${advertise-addr} operate-source create source1.yaml
    ```

    The parameters used in the command above are described as follows:

    |Parameter              |Description    |
    |-                      |-              |
    |`--master-addr`        |The `{advertise-addr}` of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
    |`operate-source create`|Loads the data source to the DM cluster.|

### Step 2: Create the migration task

Create the `task1.yaml` file as follows:

```yaml
# Task name. Multiple tasks that are running at the same time must each have a unique name.
name: "test"
# Task mode. Options are:
# - full: only performs full data migration.
# - incremental: only performs binlog real-time replication.
# - all: full data migration + binlog real-time replication.
task-mode: "incremental"
# The configuration of the target TiDB database.
target-database:
  host: "${host}"                   # e.g.: 172.16.10.83
  port: 4000
  user: "root"
  password: "${password}"           # Supported but not recommended to use a plaintext password. It is recommended to use `dmctl encrypt` to encrypt the plaintext password before using it.

# Global configuration for block and allow lists. Each instance can reference the configuration by name.
block-allow-list:                     # If the DM version is earlier than v2.0.0-beta.2, use black-white-list.
  listA:                              # Name.
    do-tables:                        # Allow list for the upstream tables to be migrated.
    - db-name: "test_db"              # Name of databases to be migrated.
      tbl-name: "test_table"          # Name of tables to be migrated.

# Configures the data source.
mysql-instances:
  - source-id: "mysql-01"               # Data source ID, i.e., source-id in source1.yaml
    block-allow-list: "listA"           # References the block-allow-list configuration above.
#       syncer-config-name: "global"    # Name of the syncer configuration.
    meta:                               # The position where the binlog replication starts when `task-mode` is `incremental` and the downstream database checkpoint does not exist. If the checkpoint exists, the checkpoint is used. If neither the `meta` configuration item nor the downstream database checkpoint exists, the migration starts from the latest binlog position of the upstream.
      binlog-name: "mysql-bin.000004"   # The binlog position recorded in "Step 1. Export an Amazon Aurora snapshot to Amazon S3". When the upstream database has source-replica switching, GTID mode is required.
      binlog-pos: 109227
      # binlog-gtid: "09bec856-ba95-11ea-850a-58f2b4af5188:1-9"

# (Optional) If you need to incrementally replicate data that has already been migrated in the full data migration, you need to enable the safe mode to avoid the incremental data replication error.
   # This scenario is common in the following case: the full migration data does not belong to the data source's consistency snapshot, and after that, DM starts to replicate incremental data from a position earlier than the full migration.
   # syncers:            # The running configurations of the sync processing unit.
   #   global:            # Configuration name.
   #     safe-mode: true  # If this field is set to true, DM changes INSERT of the data source to REPLACE for the target database, and changes UPDATE of the data source to DELETE and REPLACE for the target database. This is to ensure that when the table schema contains a primary key or unique index, DML statements can be imported repeatedly. In the first minute of starting or resuming an incremental replication task, DM automatically enables the safe mode.
```

The YAML file above is the minimum configuration required for the migration task. For more configuration items, refer to [DM Advanced Task Configuration File](/dm/task-configuration-file-full.md).

### Step 3. Run the migration task

Before you start the migration task, to reduce the probability of errors, it is recommended to confirm that the configuration meets the requirements of DM by running the `check-task` command:

```shell
tiup dmctl --master-addr ${advertise-addr} check-task task.yaml
```

After that, start the migration task by running `tiup dmctl`:

```shell
tiup dmctl --master-addr ${advertise-addr} start-task task.yaml
```

The parameters used in the command above are described as follows:

|Parameter              |Description    |
|-                      |-              |
|`--master-addr`        |The `{advertise-addr}` of any DM-master in the cluster where `dmctl` is to be connected, e.g.: 172.16.10.71:8261|
|`start-task`           |Starts the migration task.|

If the task fails to start, check the prompt message and fix the configuration. After that, you can re-run the command above to start the task.

If you encounter any problem, refer to [DM error handling](/dm/dm-error-handling.md) and [DM FAQ](/dm/dm-faq.md).

### Step 4. Check the migration task status

To learn whether the DM cluster has an ongoing migration task and the task status, run the `query-status` command using `tiup dmctl`:

```shell
tiup dmctl --master-addr ${advertise-addr} query-status ${task-name}
```

For a detailed interpretation of the results, refer to [Query Status](/dm/dm-query-status.md).

### Step 5. Monitor the task and view logs

To view the history status of the migration task and other internal metrics, take the following steps.

If you have deployed Prometheus, Alertmanager, and Grafana when you deployed DM using TiUP, you can access Grafana using the IP address and port specified during the deployment. You can then select DM dashboard to view DM-related monitoring metrics.

When DM is running, DM-worker, DM-master, and dmctl print the related information in logs. The log directories of these components are as follows:

- DM-master: specified by the DM-master process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-master-8261/log/` by default.
- DM-worker: specified by the DM-worker process parameter `--log-file`. If you deploy DM using TiUP, the log directory is `/dm-deploy/dm-worker-8262/log/` by default.

## What's next

- [Pause the migration task](/dm/dm-pause-task.md).
- [Resume the migration task](/dm/dm-resume-task.md).
- [Stop the migration task](/dm/dm-stop-task.md).
- [Export and import the cluster data source and task configuration](/dm/dm-export-import-config.md).
- [Handle failed DDL statements](/dm/handle-failed-ddl-statements.md).
