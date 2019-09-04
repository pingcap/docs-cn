---
title: Data Migration Troubleshooting
summary: Learn how to diagnose and resolve issues when you use Data Migration.
category: how-to
---

# Data Migration Troubleshooting

This document summarizes some commonly encountered issues when you use Data Migration, and provides the solutions.

If you encounter errors while running Data Migration, try the following solution:

1. Check the log content related to the error you encountered. The log files are on the DM-master and DM-worker deployment nodes. You can then view [common errors](#common-errors) to find the corresponding solution.

2. If the error you encountered is not involved yet, and you cannot solve the problem yourself by checking the log or monitoring metrics, you can contact the corresponding sales support staff.

3. After the error is solved, restart the task using dmctl.

    ```bash
    resume-task ${task name}
    ```

However, you need to reset the data replication task in some cases. For details about when to reset and how to reset, see [Reset the data replication task](#reset-the-data-replication-task).

## Common errors

### `Access denied for user 'root'@'172.31.43.27' (using password: YES)` shows when you query the task or check the log

For database related passwords in all the DM configuration files, use the passwords encrypted by `dmctl`. If a database password is empty, it is unnecessary to encrypt it. For how to encrypt the plaintext password, see [Encrypt the upstream MySQL user password using dmctl](/dev/how-to/deploy/data-migration-with-ansible.md#encrypt-the-upstream-mysql-user-password-using-dmctl).

In addition, the user of the upstream and downstream databases must have the corresponding read and write privileges. Data Migration also [prechecks the corresponding privileges automatically](/dev/reference/tools/data-migration/precheck.md) while starting the data replication task.

### Incompatible DDL statements

When you encounter a DDL statement unsupported by TiDB, you need to manually handle it using dmctl (skipping the DDL statement or replacing the DDL statement with a specified DDL statement). For details, see [Skip or replace abnormal SQL statements](/dev/reference/tools/data-migration/skip-replace-sqls.md).

> **Note:**
>
> Currently, TiDB is not compatible with all the DDL statements that MySQL supports. See [MySQL Compatibility](/dev/reference/mysql-compatibility.md#ddl).

## Reset the data replication task

You need to reset the entire data replication task in the following cases:

- `RESET MASTER` is accidentally executed in the upstream database.
- The relay log or the upstream binlog is corrupted or lost.

Generally, at this time, the relay unit exits with an error and cannot be automatically restored gracefully. You need to manually restore the data replication and the steps are as follows:

1. Use the `stop-task` command to stop all the replication tasks that are currently running.
2. Use Ansible to [stop the entire DM cluster](/dev/how-to/deploy/data-migration-with-ansible.md#step-10-stop-the-dm-cluster).
3. Manually clean up the relay log directory of the DM-worker corresponding to the MySQL master whose binlog is reset.

    - If the cluster is deployed using DM-Ansible, the relay log is in the `<deploy_dir>/relay_log` directory.
    - If the cluster is manually deployed using the binary, the relay log is in the directory set in the `relay-dir` parameter.

4. Clean up downstream replicated data.
5. Use Ansible to [start the entire DM cluster](/dev/how-to/deploy/data-migration-with-ansible.md#step-9-deploy-the-dm-cluster).
6. Restart data replication with the new task name, or set `remove-meta` to `true` and `task-mode` to `all`.
