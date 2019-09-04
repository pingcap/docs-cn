---
title: Data Migration Cluster Operations
summary: This document introduces the DM cluster operations and considerations when you administer a DM cluster using DM-Ansible.
category: reference
aliases: ['/docs/tools/dm/cluster-operations/']
---

# Data Migration Cluster Operations

This document introduces the DM cluster operations and considerations when you administer a DM cluster using DM-Ansible.

## Start a cluster

Run the following command to start all the components (including DM-master, DM-worker and the monitoring component) of the whole DM cluster:

```
$ ansible-playbook start.yml
```

## Stop a cluster

Run the following command to stop all the components (including DM-master, DM-worker and the monitoring component) of the whole DM cluster:

```
$ ansible-playbook stop.yml
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

        To resolve this issue, follow the steps described in [Handle Sharding DDL Locks Manually](/v3.0/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md#scenario-2-some-dm-workers-restart-during-the-ddl-unlocking-process).

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

    ```bash
    $ ansible-playbook rolling_update.yml --tags=dm-worker
    ```

- Stop DM-worker first and then restart it

    ```bash
    $ ansible-playbook stop.yml --tags=dm-worker
    $ ansible-playbook start.yml --tags=dm-worker
    ```

### Restart DM-master

To restart the DM-master component, you can use either of the following two approaches:

- Perform a rolling update on DM-master

    ```bash
    $ ansible-playbook rolling_update.yml --tags=dm-master
    ```

- Stop DM-master first and then restart it

    ```bash
    $ ansible-playbook stop.yml --tags=dm-master
    $ ansible-playbook start.yml --tags=dm-master
    ```

## Upgrade the component version

1. Download the DM binary file.

    1. Delete the existing file in the `downloads` directory.

        ```
        $ cd /home/tidb/dm-ansible
        $ rm -rf downloads
        ```

    2. Use Playbook to download the version of DM binary file as specified in `inventory.ini`, and replace the existing binary in the `/home/tidb/dm-ansible/resource/bin/` directory with it automatically.

        ```
        $ ansible-playbook local_prepare.yml
        ```

2. Use Ansible to perform the rolling update.

    1. Perform a rolling update on the DM-worker instance:

        ```
        ansible-playbook rolling_update.yml --tags=dm-worker
        ```

    2. Perform a rolling update on the DM-master instance:

        ```
        ansible-playbook rolling_update.yml --tags=dm-master
        ```

    3. Upgrade dmctl:

        ```
        ansible-playbook rolling_update.yml --tags=dmctl
        ```

    4. Perform a rolling update on DM-worker, DM-master and dmctl:

        ```
        ansible-playbook rolling_update.yml
        ```

## Add a DM-worker instance

Assuming that you want to add a DM-worker instance on the `172.16.10.74` machine and the alias of the instance is `dm_worker3`, perform the following steps:

1. Configure the SSH mutual trust and sudo rules on the Control Machine.

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](/v3.0/how-to/deploy/data-migration-with-ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account and add `172.16.10.74` to the `[servers]` section of the `hosts.ini` file.

        ```
        $ cd /home/tidb/dm-ansible
        $ vi hosts.ini
        [servers]
        172.16.10.74

        [all:vars]
        username = tidb
        ```

    2. Run the following command and enter the `root` user password for deploying `172.16.10.74` according to the prompt.

        ```
        $ ansible-playbook -i hosts.ini create_users.yml -u root -k
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

    ```
    $ ansible-playbook deploy.yml --tags=dm-worker -l dm_worker3
    ```

4. Start the new DM-worker instance.

    ```
    $ ansible-playbook start.yml --tags=dm-worker -l dm_worker3
    ```

5. Configure and restart the DM-master service.

    ```
    $ ansible-playbook rolling_update.yml --tags=dm-master
    ```

6. Configure and restart the Prometheus service.

    ```
    $ ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

## Remove a DM-worker instance

Assuming that you want to remove the `dm_worker3` instance, perform the following steps:

1. Stop the DM-worker instance that you need to remove.

    ```
    $ ansible-playbook stop.yml --tags=dm-worker -l dm_worker3
    ```

2. Edit the `inventory.ini` file and comment or delete the line where the `dm_worker3` instance exists.

    ```
    [dm_worker_servers]
    dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 source_id="mysql-replica-02" ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    # dm_worker3 source_id="mysql-replica-03" ansible_host=172.16.10.74 server_id=103 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306 # Comment or delete this line
    ```

3. Configure and restart the DM-master service.

    ```
    $ ansible-playbook rolling_update.yml --tags=dm-master
    ```

4. Configure and restart the Prometheus service.

    ```
    $ ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

## Replace a DM-master instance

Assuming that the `172.16.10.71` machine needs to be maintained or this machine breaks down, and you need to migrate the DM-master instance from `172.16.10.71` to `172.16.10.80`, perform the following steps:

1. Configure the SSH mutual trust and sudo rules on the Control machine.

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](/v3.0/how-to/deploy/data-migration-with-ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account, and add `172.16.10.80` to the `[servers]` section of the `hosts.ini` file.

        ```
        $ cd /home/tidb/dm-ansible
        $ vi hosts.ini
        [servers]
        172.16.10.80

        [all:vars]
        username = tidb
        ```

    2. Run the following command and enter the `root` user password for deploying `172.16.10.80` according to the prompt.

        ```
        $ ansible-playbook -i hosts.ini create_users.yml -u root -k
        ```

        This step creates the `tidb` user account on `172.16.10.80`, configures the sudo rules and the SSH mutual trust between the Control Machine and the `172.16.10.80` machine.

2. Stop the DM-master instance that you need to replace.

    > **Note:**
    >
    > If the `172.16.10.71` machine breaks down and you cannot log in via SSH, ignore this step.

    ```
    $ ansible-playbook stop.yml --tags=dm-master
    ```

3. Edit the `inventory.ini` file, comment or delete the line where the DM-master instance that you want to replace exists, and add the information of the new DM-master instance.

    ```ini
    [dm_master_servers]
    # dm_master ansible_host=172.16.10.71
    dm_master ansible_host=172.16.10.80
    ```

4. Deploy the new DM-master instance.

    ```
    $ ansible-playbook deploy.yml --tags=dm-master
    ```

5. Start the new DM-master instance.

    ```
    $ ansible-playbook start.yml --tags=dm-master
    ```

6. Update the dmctl configuration file.

    ```
    ansible-playbook rolling_update.yml --tags=dmctl
    ```

## Replace a DM-worker instance

Assuming that the `172.16.10.72` machine needs to be maintained or this machine breaks down, and you need to migrate `dm_worker1` from `172.16.10.72` to `172.16.10.75`, perform the following steps:

1. Configure the SSH mutual trust and sudo rules on the Control Machine.

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](/v3.0/how-to/deploy/data-migration-with-ansible.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account, and add `172.16.10.75` to the `[servers]` section of the `hosts.ini` file.

        ```
        $ cd /home/tidb/dm-ansible
        $ vi hosts.ini
        [servers]
        172.16.10.75

        [all:vars]
        username = tidb
        ```

    2. Run the following command and enter the `root` user password for deploying `172.16.10.75` according to the prompt.

        ```
        $ ansible-playbook -i hosts.ini create_users.yml -u root -k
        ```

        This step creates the `tidb` user account on `172.16.10.75`, and configures the sudo rules and the SSH mutual trust between the Control Machine and the `172.16.10.75` machine.

2. Stop the DM-worker instance that you need to replace.

    > **Note:**
    >
    > If the `172.16.10.72` machine breaks down and you cannot log in via SSH, ignore this step.

    ```
    $ ansible-playbook stop.yml --tags=dm-worker -l dm_worker1
    ```

3. Edit the `inventory.ini` file and add the new DM-worker instance.

    Edit the `inventory.ini` file, comment or delete the line where the original `dm_worker1` instance (`172.16.10.72`) that you want to replace exists, and add the information for the new `dm_worker1` instance (`172.16.10.75`).

    ```ini
    [dm_worker_servers]
    dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.75 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    # dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 source_id="mysql-replica-02" ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

4. Deploy the new DM-worker instance.

    ```
    $ ansible-playbook deploy.yml --tags=dm-worker -l dm_worker1
    ```

5. Start the new DM-worker instance.

    ```
    $ ansible-playbook start.yml --tags=dm-worker -l dm_worker1
    ```

6. Configure and restart the DM-master service.

    ```
    $ ansible-playbook rolling_update.yml --tags=dm-master
    ```

7. Configure and restart the Prometheus service.

    ```
    $ ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

## Switch between master and slave instances

This section describes how to switch between master and slave instances using dmctl in two conditions.

### Upstream master-slave switch behind the virtual IP

1. Use `query-status` to make sure that the relay unit has caught up with the binlog status of the master instance before the switch (`relayCatchUpMaster`).
2. Use `pause-relay` to pause relay.
3. Use `pause-task` to pause all running tasks.
4. The upstream master and slave instances behind the virtual IP execute the switch operation.
5. Use `switch-relay-master` to tell relay to execute the master-slave switch.
6. Use `resume-relay` to make relay resume to read binlog from the new master instance.
7. Use `resume-task` to resume the previous replication task.

### Master-slave switch after changing IP

1. Use `query-status` to make sure that the relay unit has caught up with the binlog status of the master instance before the switch (`relayCatchUpMaster`).
2. Use `stop-task` to stop all running tasks.
3. Modify the DM-worker configuration, and use DM-Ansible to perform a rolling update on DM-worker.
4. Use `start-task` to restart the replication task.
