---
title: Common Operations of DM-Ansible
summary: This document introduces the common operations when you administer a DM cluster using DM-Ansible. 
category: tools
---

# DM Common Operations

This document introduces the common operations when you administer a DM cluster using DM-Ansible. 

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

## Upgrade the component version

1. Download the DM binary file.

    1. Delete the existing file in the `downloads` directory.

        ```
        $ cd /home/tidb/dm-ansible
        $ rm -rf downloads
        ```

    2. Use Playbook to download the latest DM binary file and replace the existing binary in the `/home/tidb/dm-ansible/resource/bin/` directory with it automatically.

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

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](../tools/data-migration-deployment.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account and add `172.16.10.74` to the `[servers]` section of the `hosts.ini` file.

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
    dm_worker1 ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker3 ansible_host=172.16.10.74 server_id=103 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
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
    dm_worker1 ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    # dm_worker3 ansible_host=172.16.10.74 server_id=103 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306 # Comment or delete this line
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

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](../tools/data-migration-deployment.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account, and add `172.16.10.80` to the `[servers]` section of the `hosts.ini` file.

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

    > **Note:** If the `172.16.10.71` machine breaks down and you cannot log in via SSH, ignore this step.  

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

    1. Refer to [Configure the SSH mutual trust and sudo rules on the Control Machine](../tools/data-migration-deployment.md#step-5-configure-the-ssh-mutual-trust-and-sudo-rules-on-the-control-machine), log in to the Control Machine using the `tidb` user account, and add `172.16.10.75` to the `[servers]` section of the `hosts.ini` file.

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

    > **Note:** If the `172.16.10.72` machine breaks down and you cannot log in via SSH, ignore this step. 

    ```
    $ ansible-playbook stop.yml --tags=dm-worker -l dm_worker1
    ```

3. Edit the `inventory.ini` file and add the new DM-worker instance.

    Edit the `inventory.ini` file, comment or delete the line where the `dm_worker1` instance `172.16.10.72` that you want to replace exists, and add the `172.16.10.75` information of the new `dm_worker1` instance.

    ```ini
    [dm_worker_servers]
    dm_worker1 ansible_host=172.16.10.75 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    # dm_worker1 ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
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
