---
title: Ansible Deployment Using the Root User Account
category: operations
---

# Ansible Deployment Using the Root User Account

> **Note:** The remote Ansible user (the `ansible_user` in the `incentory.ini` file) can use the root user account to deploy TiDB, but it is not recommended.

The following example uses the `tidb` user account as the user running the service.

To deploy TiDB using a root user account, take the following steps:

1. Edit `inventory.ini` as follows.

    Remove the code comments for `ansible_user = root`, `ansible_become = true` and `ansible_become_user`. Add comments for `ansible_user = tidb`.

    ```
    ## Connection
    # ssh via root:
    ansible_user = root
    ansible_become = true
    ansible_become_user = tidb

    # ssh via normal user
    # ansible_user = tidb
    ```

2. Connect to the network and download TiDB binary to the Control Machine.

    ```
    ansible-playbook local_prepare.yml
    ```

3. Initialize the system environment and edit the kernel parameters.

    ```
    ansible-playbook bootstrap.yml
    ```

    > **Note**: If the service user does not exist, the initialization operation will automatically create the user.

    If the remote connection using the root user requires a password, use the `-k` (lower case) parameter. This applies to other playbooks as well:

    ```
    ansible-playbook bootstrap.yml -k
    ```

4. Deploy the TiDB cluster.

    ```
    ansible-playbook deploy.yml -k
    ```

5. Start the TiDB cluster.

    ```
    ansible-playbook start.yml -k
    ```