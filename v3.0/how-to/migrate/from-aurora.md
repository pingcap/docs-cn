---
title: Migrate from Amazon Aurora MySQL to TiDB
summary: Learn how to migrate from Amazon Aurora MySQL to TiDB by using TiDB Data Migration (DM).
category: how-to
---

# Migrate from Amazon Aurora MySQL to TiDB

This document describes how to migrate from [Amazon Aurora MySQL](https://aws.amazon.com/rds/aurora/details/mysql-details/?nc1=h_ls) to TiDB by using TiDB Data Migration (DM).

## Step 1: Enable binlog in the Aurora cluster

Assuming that you want to migrate data from two Aurora clusters to TiDB, the information of the Aurora clusters is listed in the following table. The Aurora-1 cluster contains a seperate reader endpoint.

| Cluster | Endpoint | Port | Role |
|:-------- |:--- | :--- | :--- |
| Aurora-1 | pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | Writer |
| Aurora-1 | pingcap-1-us-east-2a.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | Reader |
| Aurora-2 | pingcap-2.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | Writer |

DM relies on the `ROW` format of binlog during the incremental replication process, so you need to set the binlog format as `ROW`. If binlog is not enabled or is incorrectly configured, DM cannot replicate data normally. For more details, see [Checking items](/reference/tools/data-migration/precheck.md#checking-items).

> **Note:**
>
> Because binlog cannot be enabled in the Aurora reader, it cannot be taken as the upstream master server when you use DM to migrate data.

If you need to migrate data based on GTID (Global Transaction Identifier), enable GTID for the Aurora cluster.

> **Note:**
>
> GTID-based data migration requires MySQL 5.7 (Aurora 2.04.1) version or later.

### Modify binlog related parameters in the Aurora cluster

In the Aurora cluster, binlog related parameters are cluster level parameters among cluster parameter groups. For more information about binlog in the Aurora cluster, see [Enable Binary Logging on the Replication Master](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/AuroraMySQL.Replication.MySQL.html#AuroraMySQL.Replication.MySQL.EnableBinlog). You need to set the `binlog_format` to `ROW` when using DM for data migration.

To migrate data based on GTID, set both `gtid-mode` and `enforce_gtid_consistency` to `ON`. See [Configuring GTID-Based Replication for an Aurora MySQL Cluster](https://docs.aws.amazon.com/zh_cn/AmazonRDS/latest/AuroraUserGuide/mysql-replication-gtid.html#mysql-replication-gtid.configuring-aurora) for more information about enabling GTID-based migration for Aurora cluster.

> **Note:**
>
> In the AWS Management Console, the `gtid_mode` parameter appears as `gtid-mode`.

## Step 2: Deploy the DM cluster

It is recommended to use DM-Ansible to deploy a DM cluster. See [Deploy Data Migration Using DM-Ansible](https://pingcap.com/docs/dev/how-to/deploy/data-migration-with-ansible/).

> **Note:**
>
> - Use password encrypted with dmctl in all the DM configuration files. If the database password is empty, it is unnecessary to encrypt it. For how to use dmctl to encrypt a cleartext password, see [Encrypt the upstream MySQL user password using dmctl](https://pingcap.com/docs/dev/how-to/deploy/data-migration-with-ansible/#encrypt-the-upstream-mysql-user-password-using-dmctl).
> - Both the upstream and downstream users must have the corresponding read and write privileges.

## Step 3: Check the cluster informtaion

After a DM cluster is deployed using DM-Ansible, the configuration information is as follows:

- DM cluster components

    | Component | Host | Port |
    |:------|:---- |:---- |
    | dm_worker1 | 172.16.10.72 | 8262 |
    | dm_worker2 | 172.16.10.73 | 8262 |
    | dm_master | 172.16.10.71 | 8261 |

- Upstream and downstream database instances

    | Database instance | Host | Port | Username | Encrypted password |
    |:-------- |:--- | :--- | :--- | :--- |
    | Upstream Aurora-1 | pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | root | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | Upstream Aurora-2 | pingcap-2.h8emfqdptyc4.us-east-2.rds.amazonaws.com | 3306 | root | VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU= |
    | Downstream TiDB | 172.16.10.83 | 4000 | root | |

- Configuration in the `{ansible deploy}/conf/dm-master.toml` DM-master process configuration file

    ```toml
    # DM-Master Configuration

    [[deploy]]
    source-id = "mysql-replica-01"
    dm-worker = "172.16.10.72:8262"

    [[deploy]]
    source-id = "mysql-replica-02"
    dm-worker = "172.16.10.73:8262"
    ```

## Step 4: Configure the task

This section assumes that you need to replicate data of the `test_table` table in the `test_db` schema of Aurora-1 and Aurora-2 instances, in both full data migration and incremental replication modes, to the `test_table` table of the `test_db` schema in one downstream TiDB instance.

Copy and edit `{ansible deploy}/conf/task.yaml.example` to generate the following `task.yaml` configuration file:

```yaml
# The task name. You need to use a different name for each of the multiple tasks that run simultaneously.
name: "test"
# The full data migration plus incremental replication task mode.
task-mode: "all"
# The downstream TiDB configuration information.
target-database:
  host: "172.16.10.83"
  port: 4000
  user: "root"
  password: ""

# Configuration of all the upstream MySQL instances required by the current data replication task.
mysql-instances:
-
  # ID of the upstream instance or the replication group. Refer to the configuration of `source_id` in the `inventory.ini` file or configuration of `source-id` in the `dm-master.toml` file.
  source-id: "mysql-replica-01"
  # The configuration item name of the black and white lists of the schema or table to be replicated, used to quote the global black and white lists configuration. For global configuration, see the `black-white-list` below.
  black-white-list: "global"
  # The configuration item name of Mydumper, used to quote the global Mydumper configuration.
  mydumper-config-name: "global"

-
  source-id: "mysql-replica-02"
  black-white-list: "global"
  mydumper-config-name: "global"

# The global configuration of black and white lists. Each instance can quote it by the configuration item name.
black-white-list:
  global:
    do-tables:                        # The white list of the upstream table to be replicated
    - db-name: "test_db"              # The database name of the table to be replicated
      tbl-name: "test_table"          # The name of the table to be replicated

# Mydumper global configuration. Each instance can quote it by the configuration item name.
mydumpers:
  global:
    extra-args: "-B test_db -T test_table"  # Only outputs the `test_table` table of the `test_db` schema and can configure any parameter of Mydumper.
```

## Step 5: Start the task

1. Go to the dmctl directory: `/home/tidb/dm-ansible/resources/bin/`.

2. Start dmctl using the following command:

    ```bash
    ./dmctl --master-addr 172.16.10.71:8261
    ```

3. Start data replication task using the following command:

    ```bash
    # `task.yaml` is the previously edited configuration file.
    start-task ./task.yaml
    ```

    - If the returned results do not contain any error, it indicates the task is successfully started.
    - If the returned results contain the following error information, it indicates the upstream Aurora user might have privileges unsupported by TiDB:

        ```json
        {
            "id": 4,
            "name": "source db dump privilege chcker",
            "desc": "check dump privileges of source DB",
            "state": "fail",
            "errorMsg": "line 1 column 285 near \"LOAD FROM S3, SELECT INTO S3 ON *.* TO 'root'@'%' WITH GRANT OPTION\" ...",
            "instruction": "",
            "extra": "address of db instance - pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com"
        },
        {
            "id": 5,
            "name": "source db replication privilege chcker",
            "desc": "check replication privileges of source DB",
            "state": "fail",
            "errorMsg": "line 1 column 285 near \"LOAD FROM S3, SELECT INTO S3 ON *.* TO 'root'@'%' WITH GRANT OPTION\" ...",
            "instruction": "",
            "extra": "address of db instance - pingcap-1.h8emfqdptyc4.us-east-2.rds.amazonaws.com"
        }
        ```

        To resolve this issue, use either of the following two solutions to handle it and then use the `start-task` command to restart the task:
        1. Remove the unnecessary privileges unsupported by TiDB for the Aurora user that is used to migrate data.
        2. If you can make sure that the Aurora user has the privileges required by DM, add the following configuration item to the `task.yaml` configuration file to skip the privileges precheck when starting the task.

            ```yaml
            ignore-checking-items: ["dump_privilege", "replication_privilege"]
            ```

## Step 6: Query the task

To view the on-going data replication task(s) in the DM cluster or the task status, run the following command in dmctl to query:

```bash
query-status
```

> **Note:**
>
> If the following error message is in the returned results of the above query command, it indicates the corresponding lock cannot be obtained during the phase of the full data migration.
>
>   ```bash
>   Couldn't acquire global lock, snapshots will not be consistent: Access denied for user 'root'@'%' (using password: YES)
>   ```
>
> If it is acceptable to not use FTWL to guarantee that the dump file is consistent with metadata or the upstream can pause writing data, you can skip the above error by adding the `--no-locks` argument for `extra-args` under `mydumpers`. The steps are as follows:
>
> 1. Use the `stop-task` command to stop the paused task caused by the failure of nomarl dumping.
> 2. In the `task.yaml` file, modify `extra-args: "-B test_db -T test_table"` to `extra-args: "-B test_db -T test_table --no-locks"`.
> 3. Use the `start-task` command to restart the task.
