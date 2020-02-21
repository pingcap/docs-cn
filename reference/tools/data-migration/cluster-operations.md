---
title: Data Migration Cluster Operations
summary: This document introduces the DM cluster operations and considerations when you administer a DM cluster using DM-Ansible.
category: reference
---

# Data Migration Cluster Operations

This document introduces the DM cluster operations and considerations when you administer a DM cluster using DM-Ansible.

## Start a cluster

Run the following command to start all the components (including DM-master, DM-worker and the monitoring component) of the whole DM cluster:

{{< copyable "shell-regular" >}}

```bash
ansible-playbook start.yml
```

## Stop a cluster

Run the following command to stop all the components (including DM-master, DM-worker and the monitoring component) of the whole DM cluster:

{{< copyable "shell-regular" >}}

```bash
ansible-playbook stop.yml
```

## Restart cluster components

You need to update the DM cluster components in the following cases:

- You want to [upgrade the component version](#upgrade-the-component-version).
- A serious bug occurs and you have to restart the component for temporary recovery.
- The machine that the DM cluster is located in is restarted for certain reasons.

### Restarting considerations

This sections describes the considerations that you need to know when you restart DM components.

#### Restarting DM-worker considerations

**In the process of full data loading:**

For the SQL files during full data import, DM uses the downstream database to record the checkpoint information, and DM-worker records the subtask information in the local meta file. When DM-worker is restarted, it checks the checkpoint information and the subtask information in the local record, and the running task before restarting recovers the data replication automatically.

**In the process of incremental data replication:**

For the binlog during incremental data import, DM uses the downstream database to record the checkpoint information, and enables the safe mode within the first 5 minutes after the replication task is started or recovered.

+ Sharding DDL statements replication is not enabled

    If the sharding DDL statements replication is not enabled in the task running on DM-worker, when DM-worker is restarted, it checks the checkpoint information and the subtask information in the local record, and the running task before restarting recovers the data replication automatically.

+ Sharding DDL statements replication is enabled

    - When DM is replicating the sharding DDL statements, if DM-worker successfully executes (or skips) the sharding DDL binlog event, then the checkpoints of all tables related to sharding DDL in the DM-worker are updated to the position after the binlog event corresponding to the DDL statement.

    - When DM-worker is restarted before or after replicating sharding DDL statements, it recovers the data replication automatically according to the checkpoint information and the subtask information in the local record.

    - When DM-worker is restarted during the process of replicating sharding DDL statements, the issue might occur that the owner (one of DM-worker instances) has executed the DDL statement and successfully changed the downstream database table schema, while other DM-worker instances are restarted but fail to skip the DDL statement and update the checkpoints.

        At this time, DM tries again to replicate these DDL statements that are not skipped. However, the restarted DM-worker instances will be blocked at the position of the binlog event corresponding to the DDL binlog event, because the DM-worker instance that is not restarted has executed to the place after this DDL binlog event.

        To resolve this issue, follow the steps described in [Handle Sharding DDL Locks Manually](/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md#scenario-2-some-dm-workers-restart-during-the-ddl-unlocking-process).

**Conclusion:** Try to avoid restarting DM-worker in the process of sharding DDL replication.

#### Restarting DM-master considerations

The information maintained by DM-master includes the following two major types, and these data is not being persisted when you restart DM-master.

- The corresponding relationship between the task and DM-worker
- The sharding DDL lock related information

When DM-master is restarted, it automatically requests the task information from each DM-worker instance, rebuilds the corresponding relationship between the task and DM-worker, and also re-fetches the sharding DDL information from each DM-worker instance. So the corresponding DDL lock can be correctly rebuilt and the sharding DDL lock can be automatically resolved.

### Restart DM-worker

> **Note:**
>
> Try to avoid restarting DM-worker during the process of replicating sharding DDL statements.

To restart the DM-worker component, you can use either of the following two approaches:

- Perform a rolling update on DM-worker

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=dm-worker
    ```

- Stop DM-worker first and then restart it

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml --tags=dm-worker &&
    ansible-playbook start.yml --tags=dm-worker
    ```

### Restart DM-master

To restart the DM-master component, you can use either of the following two approaches:

- Perform a rolling update on DM-master

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=dm-master
    ```

- Stop DM-master first and then restart it

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml --tags=dm-master &&
    ansible-playbook start.yml --tags=dm-master
    ```

## Upgrade the component version

1. Download the DM binary file.

    1. Delete the existing file in the `downloads` directory.

        {{< copyable "shell-regular" >}}

        ```bash
        cd /home/tidb/dm-ansible &&
        rm -rf downloads
        ```

    2. Use Playbook to download the version of DM binary file as specified in `inventory.ini`, and replace the existing binary in the `/home/tidb/dm-ansible/resource/bin/` directory with it automatically.

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook local_prepare.yml
        ```

2. Use Ansible to perform the rolling update.

    1. Perform a rolling update on the DM-worker instance:

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook rolling_update.yml --tags=dm-worker
        ```

    2. Perform a rolling update on the DM-master instance:

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook rolling_update.yml --tags=dm-master
        ```

    3. Upgrade dmctl:

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook rolling_update.yml --tags=dmctl
        ```

    4. Perform a rolling update on DM-worker, DM-master and dmctl:

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook rolling_update.yml
        ```

## Add a DM-worker instance

Assuming that you want to add a DM-worker instance on the `172.16.10.74` machine and the alias of the instance is `dm_worker3`, perform the following steps:

1. Configure the SSH mutual trust and sudo rules on the Control Machine.

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](/how-to/deploy/data-migration-with-ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account and add `172.16.10.74` to the `[servers]` section of the `hosts.ini` file.

        {{< copyable "shell-regular" >}}

        ```bash
        cd /home/tidb/dm-ansible &&
        vi hosts.ini
        ```

        ```
        [servers]
        172.16.10.74

        [all:vars]
        username = tidb
        ```

    2. Run the following command and enter the `root` user password for deploying `172.16.10.74` according to the prompt.

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook -i hosts.ini create_users.yml -u root -k
        ```

        This step creates a `tidb` user on the `172.16.10.74` machine, and configures sudo rules and the SSH mutual trust between the Control Machine and the `172.16.10.74` machine.

2. Edit the `inventory.ini` file and add the new DM-worker instance `dm_worker3`.

    ```
    [dm_worker_servers]
    dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 source_id="mysql-replica-02" ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker3 source_id="mysql-replica-03" ansible_host=172.16.10.74 server_id=103 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

3. Deploy the new DM-worker instance.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook deploy.yml --tags=dm-worker -l dm_worker3
    ```

4. Start the new DM-worker instance.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook start.yml --tags=dm-worker -l dm_worker3
    ```

5. Configure and restart the DM-master service.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=dm-master
    ```

6. Configure and restart the Prometheus service.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

## Remove a DM-worker instance

Assuming that you want to remove the `dm_worker3` instance, perform the following steps:

1. Stop the DM-worker instance that you need to remove.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml --tags=dm-worker -l dm_worker3
    ```

2. Edit the `inventory.ini` file and comment or delete the line where the `dm_worker3` instance exists.

    ```
    [dm_worker_servers]
    dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 source_id="mysql-replica-02" ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    # dm_worker3 source_id="mysql-replica-03" ansible_host=172.16.10.74 server_id=103 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306 # Comment or delete this line
    ```

3. Configure and restart the DM-master service.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=dm-master
    ```

4. Configure and restart the Prometheus service.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

## Replace/migrate a DM-master instance

Assuming that the `172.16.10.71` machine needs to be maintained or this machine breaks down, and you need to migrate the DM-master instance from `172.16.10.71` to `172.16.10.80`, perform the following steps:

1. Configure the SSH mutual trust and sudo rules on the Control machine.

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](/how-to/deploy/data-migration-with-ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account, and add `172.16.10.80` to the `[servers]` section of the `hosts.ini` file.

        {{< copyable "shell-regular" >}}

        ```bash
        cd /home/tidb/dm-ansible &&
        vi hosts.ini
        ```

        ```
        [servers]
        172.16.10.80

        [all:vars]
        username = tidb
        ```

    2. Run the following command and enter the `root` user password for deploying `172.16.10.80` according to the prompt.

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook -i hosts.ini create_users.yml -u root -k
        ```

        This step creates the `tidb` user account on `172.16.10.80`, configures the sudo rules and the SSH mutual trust between the Control Machine and the `172.16.10.80` machine.

2. Stop the DM-master instance that you need to replace.

    > **Note:**
    >
    > If the `172.16.10.71` machine breaks down and you cannot log in via SSH, ignore this step.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml --tags=dm-master
    ```

3. Edit the `inventory.ini` file, comment or delete the line where the DM-master instance that you want to replace exists, and add the information of the new DM-master instance.

    ```ini
    [dm_master_servers]
    # dm_master ansible_host=172.16.10.71
    dm_master ansible_host=172.16.10.80
    ```

4. Deploy the new DM-master instance.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook deploy.yml --tags=dm-master
    ```

5. Start the new DM-master instance.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook start.yml --tags=dm-master
    ```

6. Update the dmctl configuration file.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=dmctl
    ```

## Replace/migrate a DM-worker instance

Assuming that the `172.16.10.72` machine needs to be maintained or this machine breaks down, and you need to migrate `dm_worker1` from `172.16.10.72` to `172.16.10.75`, perform the following steps:

1. Configure the SSH mutual trust and sudo rules on the Control Machine.

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](/how-to/deploy/data-migration-with-ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account, and add `172.16.10.75` to the `[servers]` section of the `hosts.ini` file.

        {{< copyable "shell-regular" >}}

        ```bash
        cd /home/tidb/dm-ansible &&
        vi hosts.ini
        ```

        ```
        [servers]
        172.16.10.75

        [all:vars]
        username = tidb
        ```

    2. Run the following command and enter the `root` user password for deploying `172.16.10.75` according to the prompt.

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook -i hosts.ini create_users.yml -u root -k
        ```

        This step creates the `tidb` user account on `172.16.10.75`, and configures the sudo rules and the SSH mutual trust between the Control Machine and the `172.16.10.75` machine.

2. Stop the DM-worker instance that you need to replace.

    > **Note:**
    >
    > If the `172.16.10.72` machine breaks down and you cannot log in via SSH, ignore this step.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml --tags=dm-worker -l dm_worker1
    ```

3. Edit the `inventory.ini` file and add the new DM-worker instance.

    Edit the `inventory.ini` file, comment or delete the line where the original `dm_worker1` instance (`172.16.10.72`) that you want to replace exists, and add the information for the new `dm_worker1` instance (`172.16.10.75`).

    To pull the relay log from a different binlog position or GTID Sets, you also need to update corresponding `{relay_binlog_name}` or `{relay_binlog_gtid}`.

    ```ini
    [dm_worker_servers]
    dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.75 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    # dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 source_id="mysql-replica-02" ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

4. Deploy the new DM-worker instance.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook deploy.yml --tags=dm-worker -l dm_worker1
    ```

5. Migrate the relay log.

    - If the `172.16.10.72` machine is still accessible, you can directly copy all data from the `{dm_worker_relay_dir}` directory to the corresponding directory of the new DM-worker instance.

    - If `172.16.10.72` machine is no longer accessible, you may need to manually recover data such as the relay log directories in Step 9.

6. Start the new DM-worker instance.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook start.yml --tags=dm-worker -l dm_worker1
    ```

7. Configure and restart the DM-master service.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update.yml --tags=dm-master
    ```

8. Configure and restart the Prometheus service.

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

9. Start and verify data migration task.

    Execute `start-task` command to start data migration task. If no error is reported, then DM-worker migration completes successfully. If the following error is reported, you need to manually fix the relay log directory.

    ```log
    fail to initial unit Sync of subtask test-task : UUID suffix 000002 with UUIDs [1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000001] not found
    ```

    This error occurs because the upstream MySQL of the DM-worker instance to be replaced has been switched. You can fix this by following these steps:

    1. Use `stop-task` to stop data migration task.

    2. Use `ansible-playbook stop.yml --tags=dm-worker -l dm_worker1` to stop the DM-worker instance.

    3. Update the suffix of the subdirectory of the relay log, such as renaming `1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000001` to `1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000002`.

    4. Update the index file `server-uuid.index` in the subdirectory of the relay log, such as changing `1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000001` to `1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000002`.

    5. Use `ansible-playbook start.yml --tags=dm-worker -l dm_worker1` to start the DM-worker instance.

    6. Restart and verify data migration task.

## Switch DM-worker connection between upstream MySQL instances

When the upstream MySQL instance that DM-worker connects to needs downtime maintenance or when the instance crashes unexpectedly, you need to switch the DM-worker connection to another MySQL instance within the same replication group.

> **Note:**
>
> - You can switch the DM-worker connection to only an instance within the same master-slave replication cluster.
> - The MySQL instance to be newly connected to must have the binlog required by DM-worker.
> - DM-worker must operate in the GTID sets mode, which means you must specify `enable_gtid=true` when you deploy DM using DM-Ansible.
> - The connection switch only supports the following two scenarios. Strictly follow the procedures for each scenario. Otherwise, you might have to re-deploy the DM cluster according to the newly connected MySQL instance and perform the data replication task all over again.

For more details on GTID set, refer to [MySQL documentation](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html#replication-gtids-concepts-gtid-sets).

### Switch DM-worker connection via virtual IP

When DM-worker connects the upstream MySQL instance via a virtual IP (VIP), switching the VIP connection to another MySQL instance means switching the MySQL instance actually connected to DM-worker, without the upstream connection address changed.

> **Note:**
>
> Make necessary changes to DM in this scenario. Otherwise, when you switch the VIP connection to another MySQL instance, DM might connect to the new and old MySQL instances at the same time in different connections. In this situation, the binlog replicated to DM is not consistent with other upstream status that DM receives, causing unpredictable anomalies and even data damage.

To switch one upstream MySQL instance (when DM-worker connects to it via a VIP) to another, perform the following steps:

1. Use the `query-status` command to get the GTID sets (`relayBinlogGtid`) corresponding to the binlog that relay log has replicated from the old MySQL instance. Mark the sets as `gtid-W`.
2. Use the `SELECT @@GLOBAL.gtid_purged;` command on the new MySQL instance to get the GTID sets corresponding to the purged binlogs. Mark the sets as `gtid-P`.
3. Use the `SELECT @@GLOBAL.gtid_executed;` command on the new MySQL instance to get the GTID sets corresponding to all successfully executed transactions. Mark the sets as `gtid-E`.
4. Make sure that the following conditions are met. Otherwise, you cannot switch the DM-work connection to the new MySQL instance:
    - `gtid-W` contains `gtid-P`. `gtid-P` can be empty.
    - `gtid-E` contains `gtid-W`.
5. Use `pause-relay` to pause relay.
6. Use `pause-task` to pause all running tasks of data replication.
7. Change the VIP for it to direct at the new MySQL instance.
8. Use `switch-relay-master` to tell relay to execute the master-slave switch.
9. Use `resume-relay` to make relay resume to read binlog from the new MySQL instance.
10. Use `resume-task` to resume the previous replication task.

### Change the address of the upstream MySQL instance that DM-worker connects to

To make DM-worker connect to a new MySQL instance in the upstream by modifying the DM-worker configuration, perform the following steps:

1. Use the `query-status` command to get the GTID sets (`relayBinlogGtid`) corresponding to the binlog that relay log has replicated from the old MySQL instance. Mark this sets as `gtid-W`.
2. Use the `SELECT @@GLOBAL.gtid_purged;` command on the new MySQL instance to get the GTID sets corresponding to the purged binlogs. Mark this sets as `gtid-P`.
3. Use the `SELECT @@GLOBAL.gtid_executed;` command on the new MySQL instance to get the GTID sets corresponding to all successfully executed transactions. Mark this sets as `gtid-E`.
4. Make sure that the following conditions are met. Otherwise, you cannot switch the DM-work connection to the new MySQL instance:
    - `gtid-W` contains `gtid-P`. `gtid-P` can be empty.
    - `gtid-E` contains `gtid-W`.
5. Use `stop-task` to stop all running tasks of data replication.
6. Update the DM-worker configuration in the `inventory.ini` file and use DM-Ansible to perform a rolling upgrade on DM-worker.
7. Use `start-task` to restart the replication task.
