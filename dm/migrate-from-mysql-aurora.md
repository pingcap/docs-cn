---
title: Migrate from a MySQL-compatible Database - Taking Amazon Aurora MySQL as an Example
summary: Learn how to migrate from MySQL (using a case of Amazon Aurora) to TiDB by using TiDB Data Migration (DM).
aliases: ['/docs/tidb-data-migration/dev/migrate-from-mysql-aurora/']
---

# Migrate from a MySQL-compatible Database - Taking Amazon Aurora MySQL as an Example

This document describes how to migrate from [Amazon Aurora MySQL](https://aws.amazon.com/rds/aurora/details/mysql-details/?nc1=h_ls) to TiDB by using TiDB Data Migration (DM).

The information of the Aurora cluster in the example is as follows:

| Cluster | Endpoint | Port | Role | Version |
|:-------- |:--- | :--- | :--- |:---|
| Aurora-1 | test-dm-2-0.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com | 3306 | Writer | Aurora (MySQL)-5.7.12 |
| Aurora-1 | test-dm-2-0.cluster-ro-czrtqco96yc6.us-east-2.rds.amazonaws.com | 3306 | Reader | Aurora (MySQL)-5.7.12 |
| Aurora-2 | test-dm-2-0-2.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com | 3306 | Writer | Aurora (MySQL)-5.7.12 |
| Aurora-2 | test-dm-2-0-2.cluster-ro-czrtqco96yc6.us-east-2.rds.amazonaws.com | 3306 | Reader | Aurora (MySQL)-5.7.12 |

The data and migration plan of the Aurora cluster are as follows:

| Cluster | Database | Table | Migration |
|:---- |:---- | :--- | :--- |
| Aurora-1 | migrate_me | t1 | Yes |
| Aurora-1 | ignore_me | ignore_table | No |
| Aurora-2 | migrate_me | t2 | Yes |
| Aurora-2 | ignore_me | ignore_table | No |

The Aurora users in this migration are as follows:

| Cluster | User | Password |
|:---- |:---- | :--- |
| Aurora-1 | root | 12345678 |
| Aurora-2 | root | 12345678 |

The TiDB cluster information in the example is as follows. The TiDB cluster is deployed using [TiDB Cloud](https://tidbcloud.com/).

| Node | Port | Version |
|:--- | :--- | :--- |
| tidb.6657c286.23110bc6.us-east-1.prod.aws.tidbcloud.com | 4000 | v4.0.2 |

The TiDB users in this migration are as follows:

| User | Password |
|:---- | :--- |
| root | 87654321 |

After migration, the ``` `migrate_me`.`t1` ``` and ``` `migrate_me`.`t2` ``` tables are expected to exist in the TiDB cluster. The data of these tables is consistent with that of the Aurora cluster.

> **Note:**
>
> This migration does not involve the DM Shard Merge feature. To use this feature, see [DM Shard Merge Scenario](/dm/scenarios.md#shard-merge-scenario).

## Step 1: Precheck

To ensure a successful migration, you need to do prechecks before starting the migration. This section provides the precheck list and solutions to DM and Aurora components.

### DM nodes deployment

As the hub of data migration, DM needs to connect to the upstream Aurora cluster and the downstream TiDB cluster. Therefore, you need to use the MySQL client to check whether the nodes in which DM is to be deployed can connect to the upstream and downstream. In addition, for details of DM requirements on hardware, software, and the node number, see [DM Cluster Software and Hardware Recommendations](/dm/dm-hardware-and-software-requirements.md).

### Aurora

DM relies on the `ROW`-formatted binlog for incremental replication. See [Enable binary for an Aurora Cluster](https://aws.amazon.com/premiumsupport/knowledge-center/enable-binary-logging-aurora/?nc1=h_ls) for the configuration instruction.

If GTID is enabled in Aurora, you can migrate data based on GTID. For how to enable it, see [Configuring GTID-Based Replication for an Aurora MySQL Cluster](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.html#mysql-replication-gtid.configuring-aurora). To migrate data based on GTID, you need to set `enable-gtid` to `true` in the configuration file of data source in [step 3](#step-3-configure-the-data-source).

> **Note:**
>
> + GTID-based data migration requires MySQL 5.7 (Aurora 2.04) version or later.
> + In addition to the Aurora-specific configuration above, the upstream database must meet other requirements for migrating from MySQL, such as table schemas, character sets, and privileges. See [Checking Items](/dm/dm-precheck.md#checking-items) for details.

## Step 2: Deploy the DM cluster

DM can be deployed in multiple ways. Currently, it is recommended to use TiUP to deploy a DM cluster. For the specific deployment method, see [Deploy DM cluster using TiUP](/dm/deploy-a-dm-cluster-using-tiup.md). This example has two data sources, so at least two DM-worker nodes need to be deployed.

After deployment, you need to record the IP and service port of any DM-master node (`8261` by default) for `dmctl` to connect. This example uses `127.0.0.1:8261`. Check the DM status through TiUP using `dmctl`:

> **Note:**
>
> When using other methods to deploy DM, you can call `dmctl` in a similar way. See [Introduction to dmctl](/dm/dmctl-introduction.md).

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 list-member
```

The number of `master`s and `worker`s in the returned result is consistent with the number of deployed nodes:

```bash
{
    "result": true,
    "msg": "",
    "members": [
        {
            "leader": {
                ...
            }
        },
        {
            "master": {
                "msg": "",
                "masters": [
                    ...
                ]
            }
        },
        {
            "worker": {
                "msg": "",
                "workers": [
                    ...
                ]
            }
        }
    ]
}
```

## Step 3: Configure the data source

> **Note:**
>
> The configuration file used by DM supports database passwords in plaintext or ciphertext. It is recommended to use password encrypted using dmctl. To obtain the ciphertext password, see [Encrypt the database password using dmctl](/dm/dm-manage-source.md#encrypt-the-database-password).

Save the following configuration files of data source according to the example, in which the value of `source-id` will be used in the task configuration in [step 4](#step-4-configure-the-task).

The content of `source1.yaml`:

```yaml
# Aurora-1
source-id: "aurora-replica-01"

# To migrate data based on GTID, you need to set this item to true.
enable-gtid: false

from:
  host: "test-dm-2-0.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com"
  user: "root"
  password: "12345678"
  port: 3306
```

The content of `source2.yaml`:

```yaml
# Aurora-2
source-id: "aurora-replica-02"

enable-gtid: false

from:
  host: "test-dm-2-0-2.cluster-czrtqco96yc6.us-east-2.rds.amazonaws.com"
  user: "root"
  password: "12345678"
  port: 3306
```

See [Migrate Data Using Data Migration - Create Data Source](/dm/migrate-data-using-dm.md#step-3-create-data-source), and use `dmctl` to add two data sources through TiUP.

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 operate-source create dm-test/source1.yaml
tiup dmctl --master-addr 127.0.0.1:8261 operate-source create dm-test/source2.yaml
```

When the data sources are successfully added, the return information of each data source includes a DM-worker bound to it.

```bash
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "aurora-replica-01",
            "worker": "one-dm-worker-ID"
        }
    ]
}
```

## Step 4: Configure the task

> **Note:**
>
> Because Aurora does not support FTWRL, write operations have to be paused when you only perform the full data migration to export data. See [AWS documentation](https://aws.amazon.com/premiumsupport/knowledge-center/mysqldump-error-rds-mysql-mariadb/?nc1=h_ls) for details. In this example, both full data migration and incremental replication are performed, and DM automatically enables the [`safe mode`](/dm/dm-glossary.md#safe-mode) to solve this pause issue. To ensure data consistency in other combinations of task mode, see [AWS documentation](https://aws.amazon.com/premiumsupport/knowledge-center/mysqldump-error-rds-mysql-mariadb/?nc1=h_ls).

This example migrates the existing data in Aurora and replicates incremental data to TiDB in real time, which is the **full data migration plus incremental replication** mode. According to the TiDB cluster information above, the added `source-id`, and the table to be migrated, save the following task configuration file `task.yaml`:

```yaml
# The task name. You need to use a different name for each of the multiple tasks that run simultaneously.
name: "test"
# The full data migration plus incremental replication task mode.
task-mode: "all"
# The downstream TiDB configuration information.
target-database:
  host: "tidb.6657c286.23110bc6.us-east-1.prod.aws.tidbcloud.com"
  port: 4000
  user: "root"
  password: "87654321"

# Configuration of all the upstream MySQL instances required by the current data migration task.
mysql-instances:
- source-id: "aurora-replica-01"
  # The configuration items of the block and allow lists of the schema or table to be migrated, used to quote the global block and allow lists configuration. For global configuration, see the `block-allow-list` below.
  block-allow-list: "global"
  mydumper-config-name: "global"

- source-id: "aurora-replica-02"
  block-allow-list: "global"
  mydumper-config-name: "global"

# The configuration of block and allow lists.
block-allow-list:
  global:                             # Quoted by block-allow-list: "global" above
    do-dbs: ["migrate_me"]            # The allow list of the upstream table to be migrated. Database tables that are not in the allow list will not be migrated.

# The configuration of the dump unit.
mydumpers:
   global:                            # Quoted by mydumper-config-name: "global" above
    extra-args: "--consistency none"  # Aurora does not support FTWRL, you need to configure this option to bypass FTWRL.
```

## Step 5: Start the task

Start the task using `dmctl` through TiUP.

> **Note:**
>
> Currently, when using `dmctl` in TiUP, you need to use the absolute path of `task.yaml`. TiUP will support the relative path in later versions.

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 start-task /absolute/path/to/task.yaml --remove-meta
```

If the task is successfully started, the following information is returned:

```
{
    "result": true,
    "msg": "",
    "sources": [
        {
            "result": true,
            "msg": "",
            "source": "aurora-replica-01",
            "worker": "one-dm-worker-ID"
        },
        {
            "result": true,
            "msg": "",
            "source": "aurora-replica-02",
            "worker": "another-dm-worker-ID"
        }
    ]
}
```

If `source db replication privilege checker` and `source db dump privilege checker` errors are in the returned information, check whether unrecognized privileges exsit in the `errorMsg` field. For example:

```
line 1 column 287 near \"INVOKE LAMBDA ON *.* TO...
```

The returned information above shows that the `INVOKE LAMBDA` privilege causes an error. If the privilege is Aurora-specific, add the following content to the configuration file to skip the check. DM will improve the automatic handling of Aurora privileges in later versions.

```
ignore-checking-items: ["replication_privilege","dump_privilege"]
```

## Step 6: Query the task and validate the data

Use `dmctl` through TiUP to query information of the on-going migration task and the task status.

{{< copyable "shell-regular" >}}

```bash
tiup dmctl --master-addr 127.0.0.1:8261 query-status
```

If the task is running normally, the following information is returned.

```
{
    "result": true,
    "msg": "",
    "tasks": [
        {
            "taskName": "test",
            "taskStatus": "Running",
            "sources": [
                "aurora-replica-01",
                "aurora-replica-02"
            ]
        }
    ]
}
```

You can query data in the downstream, modify data in Aurora, and validate the data migrated to TiDB.
