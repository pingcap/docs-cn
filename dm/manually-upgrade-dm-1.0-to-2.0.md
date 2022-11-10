---
title: Manually Upgrade TiDB Data Migration from v1.0.x to v2.0+
summary: Learn how to manually upgrade TiDB data migration from v1.0.x to v2.0+.
---

# Manually Upgrade TiDB Data Migration from v1.0.x to v2.0+

This document introduces how to manually upgrade the TiDB DM tool from v1.0.x to v2.0+. The main idea is to use the global checkpoint information in v1.0.x to start a new data migration task in the v2.0+ cluster.

For how to automatically upgrade the TiDB DM tool from v1.0.x to v2.0+, refer to [Using TiUP to automatically import the 1.0 cluster deployed by DM-Ansible](/dm/maintain-dm-using-tiup.md#import-and-upgrade-a-dm-10-cluster-deployed-using-dm-ansible).

> **Note:**
>
> - Currently, upgrading DM from v1.0.x to v2.0+ is not supported when the data migration task is in the process of full export or full import.
> - As the gRPC protocol used for interaction between the components of the DM cluster is updated greatly, you need to make sure that the DM components (including dmctl) use the same version before and after the upgrade.
> - Because the metadata storage of the DM cluster (such as checkpoint, shard DDL lock status, and online DDL metadata) is updated greatly, the metadata of v1.0.x cannot be reused automatically in v2.0+. So you need to make sure the following requirements are satisfied before performing the upgrade operation:
>     - All data migration tasks are not in the process of shard DDL coordination.
>     - All data migration tasks are not in the process of online DDL coordination.

The steps for manual upgrade are as follows.

## Step 1: Prepare v2.0+ configuration file

The prepared configuration files of v2.0+ include the configuration files of the upstream database and the configuration files of the data migration task.

### Upstream database configuration file

In v2.0+, the [upstream database configuration file](/dm/dm-source-configuration-file.md) is separated from the process configuration of the DM-worker, so you need to obtain the source configuration based on the [v1.0.x DM-worker configuration](/dm/dm-worker-configuration-file.md).

> **Note:**
>
> If `enable-gtid` in the source configuration is enabled during the upgrade from v1.0.x to v2.0+, you need to parse the binlog or relay log file to obtain the GTID sets corresponding to the binlog position.

#### Upgrade a v1.0.x cluster deployed by DM-Ansible

Assume that the v1.0.x DM cluster is deployed by DM-Ansible, and the following `dm_worker_servers` configuration is in the `inventory.ini` file:

```ini
[dm_master_servers]
dm_worker1 ansible_host=172.16.10.72 server_id=101 source_id="mysql-replica-01" mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
dm_worker2 ansible_host=172.16.10.73 server_id=102 source_id="mysql-replica-02" mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
```

Then you can convert it to the following two source configuration files:

```yaml
# The source configuration corresponding to the original dm_worker1. For example, it is named as source1.yaml.
server-id: 101                                   # Corresponds to the original `server_id`.
source-id: "mysql-replica-01"                    # Corresponds to the original `source_id`.
from:
  host: "172.16.10.81"                           # Corresponds to the original `mysql_host`.
  port: 3306                                     # Corresponds to the original `mysql_port`.
  user: "root"                                   # Corresponds to the original `mysql_user`.
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # Corresponds to the original `mysql_password`.
```

```yaml
# The source configuration corresponding to the original dm_worker2. For example, it is named as source2.yaml.
server-id: 102                                   # Corresponds to the original `server_id`.
source-id: "mysql-replica-02"                    # Corresponds to the original `source_id`.
from:
  host: "172.16.10.82"                           # Corresponds to the original `mysql_host`.
  port: 3306                                     # Corresponds to the original `mysql_port`.
  user: "root"                                   # Corresponds to the original `mysql_user`.
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # Corresponds to the original `mysql_password`.
```

#### Upgrade a v1.0.x cluster deployed by binary

Assume that the v1.0.x DM cluster is deployed by binary, and the corresponding DM-worker configuration is as follows:

```toml
log-level = "info"
log-file = "dm-worker.log"
worker-addr = ":8262"
server-id = 101
source-id = "mysql-replica-01"
flavor = "mysql"
[from]
host = "172.16.10.81"
user = "root"
password = "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="
port = 3306
```

Then you can convert it to the following source configuration file:

```yaml
server-id: 101                                   # Corresponds to the original `server-id`.
source-id: "mysql-replica-01"                    # Corresponds to the original `source-id`.
flavor: "mysql"                                  # Corresponds to the original `flavor`.
from:
  host: "172.16.10.81"                           # Corresponds to the original `from.host`.
  port: 3306                                     # Corresponds to the original `from.port`.
  user: "root"                                   # Corresponds to the original `from.user`.
  password: "VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU="   # Corresponds to the original `from.password`.
```

### Data migration task configuration file

For [data migration task configuration guide](/dm/dm-task-configuration-guide.md), v2.0+ is basically compatible with v1.0.x. You can directly copy the configuration of v1.0.x.

## Step 2: Deploy the v2.0+ cluster

> **Note:**
>
> Skip this step if you have other v2.0+ clusters available.

[Use TiUP](/dm/deploy-a-dm-cluster-using-tiup.md) to deploy a new v2.0+ cluster according to the required number of nodes.

## Step 3: Stop the v1.0.x cluster

If the original v1.0.x cluster is deployed by DM-Ansible, you need to use [DM-Ansible to stop the v1.0.x cluster](https://docs.pingcap.com/tidb-data-migration/v1.0/cluster-operations#stop-a-cluster).

If the original v1.0.x cluster is deployed by binary, you can stop the DM-worker and DM-master processes directly.

## Step 4: Upgrade data migration task

1. Use the [`operate-source`](/dm/dm-manage-source.md#operate-data-source) command to load the upstream database source configuration from [step 1](#step-1-prepare-v20-configuration-file) into the v2.0+ cluster.

2. In the downstream TiDB cluster, obtain the corresponding global checkpoint information from the incremental checkpoint table of the v1.0.x data migration task.

    - Assume that the v1.0.x data migration configuration does not specify `meta-schema` (or specify its value as the default `dm_meta`), and the corresponding task name is `task_v1`, the corresponding checkpoint information is in the ``` `dm_meta`.`task_v1_syncer_checkpoint` ``` table of the downstream TiDB.
    - Use the following SQL statements to obtain the global checkpoint information of all upstream database sources corresponding to the data migration task.

        ```sql
        > SELECT `id`, `binlog_name`, `binlog_pos` FROM `dm_meta`.`task_v1_syncer_checkpoint` WHERE `is_global`=1;
        +------------------+-------------------------+------------+
        | id               | binlog_name             | binlog_pos |
        +------------------+-------------------------+------------+
        | mysql-replica-01 | mysql-bin|000001.000123 | 15847      |
        | mysql-replica-02 | mysql-bin|000001.000456 | 10485      |
        +------------------+-------------------------+------------+
        ```

3. Update the v1.0.x data migration task configuration file to start a new v2.0+ data migration task.

    - If the data migration task configuration file of v1.0.x is `task_v1.yaml`, copy it and rename it to `task_v2.yaml`.
    - Make the following changes to `task_v2.yaml`:
        - Modify `name` to a new name, such as `task_v2`.
        - Change `task-mode` to `incremental`.
        - Set the starting point of incremental replication for each source according to the global checkpoint information obtained in step 2. For example:

            ```yaml
            mysql-instances:
              - source-id: "mysql-replica-01"        # Corresponds to the `id` of the checkpoint information.
                meta:
                  binlog-name: "mysql-bin.000123"    # Corresponds to the `binlog_name` in the checkpoint information, excluding the part of `|000001`.
                  binlog-pos: 15847                  # Corresponds to `binlog_pos` in the checkpoint information.

              - source-id: "mysql-replica-02"
                meta:
                  binlog-name: "mysql-bin.000456"
                  binlog-pos: 10485
            ```

            > **Note:**
            >
            > If `enable-gtid` is enabled in the source configuration, currently you need to parse the binlog or relay log file to obtain the GTID sets corresponding to the binlog position, and set it to `binlog-gtid` in the `meta`.

4. Use the [`start-task`](/dm/dm-create-task.md) command to start the upgraded data migration task through the v2.0+ data migration task configuration file.

5. Use the [`query-status`](/dm/dm-query-status.md) command to confirm whether the data migration task is running normally.

If the data migration task runs normally, it indicates that the DM upgrade to v2.0+ is successful.
