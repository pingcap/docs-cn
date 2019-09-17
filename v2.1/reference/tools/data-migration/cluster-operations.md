---
title: DM 集群操作
category: reference
---

# DM 集群操作

本文介绍 DM 集群操作以及使用 DM-Ansible 管理 DM 集群时需要注意的事项。

## 启动集群

运行以下命令以启动整个集群的所有组件（包括 DM-master、DM-worker 和监控组件）：

```
$ ansible-playbook start.yml
```

## 下线集群

运行以下命令以下线整个集群的所有组件（包括 DM-master、DM-worker 和监控组件）：

```
$ ansible-playbook stop.yml
```

## 重启集群组件

在以下情况下，需要更新 DM 集群组件：

- 您想要[更新组件版本](#更新组件版本)。
- 发生了严重的错误，您需要重启组件完成临时恢复。
- DM 集群所在的机器由于某种原因重启。

### 重启注意事项

该部分描述重启 DM 各组件时需要了解的事项。

#### DM-worker 重启事项

**全量数据导入过程中：**

对于全量数据导入时的 SQL 文件，DM 使用下游数据库记录断点信息，DM-worker 会在本地 meta 文件记录子任务信息。DM-worker 重启时会检查断点信息和本地记录的子任务信息，重启前处于运行中状态的任务会自动恢复数据同步。

**增量数据同步过程中：**

对于增量数据导入过程中的 binlog，DM 使用下游数据库记录断点信息，并会在同步任务开始或恢复后的第一个五分钟之内开启安全模式。

+ 未启用 sharding DDL 同步

    如果 DM-worker 上运行的任务未启用 sharding DDL 同步功能，DM-worker 重启时会检查断点信息和本地记录的子任务信息，重启前处于运行中状态的任务会自动恢复数据同步。

+ 已启用 sharding DDL 同步

    - DM 同步 sharding DDL 语句时，如果 DM-worker 成功执行（或跳过）sharding DDL 的 binlog event，与 DM-worker 中的 sharding DDL 语句相关的所有表的断点信息都会被更新至 DDL 语句对应的 binlog event 之后的位置。

    - 当 DM-worker 重启发生在 sharding DDL 语句同步开始前或完成后，DM-worker 会根据断点信息和本地记录的子任务信息自动恢复数据同步。

    - 当 DM-worker 重启发生在 sharding DDL 语句同步过程中，可能会出现作为 DDL lock owner 的 DM-worker 实例已执行了 DDL 语句并成功变更了下游数据库表结构，但其他 DM-worker 实例重启而无法跳过 DDL 语句也无法更新断点的情况。

      此时 DM 会再次尝试同步这些未跳过执行的 DDL 语句。然而，由于未重启的 DM-worker 实例已经执行到了此 DDL 对应的 binlog event 之后，重启的 DM-worker 实例会被阻滞在重启前 DDL binlog event 对应的位置。

      要解决这个问题，请按照[手动处理 Sharding DDL Lock](/v2.1/reference/tools/data-migration/features/manually-handling-sharding-ddl-locks.md#场景二unlock-过程中部分-dm-worker-重启) 中描述的步骤操作。

**总结**：尽量避免在 sharding DDL 同步过程中重启 DM-worker。

#### DM-master 重启事项

由 DM-master 维护的信息包括以下两种。重启 DM-master 不会持久化保存这些信息的相关数据。

- 任务信息
- Sharding DDL lock 信息

DM-master 重启时会自动向每个 DM-worker 实例请求任务信息，重建任务与 DM-worker 之间的对应关系，并从每个 DM-worker 实例获取 sharding DDL 信息。这样，就可以准确重建相应的 DDL lock，也可以自动解除 sharding DDL lock。

### 重启 DM-worker

> **注意：**
>
> 尽量避免在 sharding DDL 同步过程中重启 DM-worker。

使用以下两种方法中任一种重启 DM-worker 组件：

- 对 DM-worker 执行滚动升级。

    ```bash
    $ ansible-playbook rolling_update.yml --tags=dm-worker
    ```

- 先停止 DM-worker，然后重启。

    ```bash
    $ ansible-playbook stop.yml --tags=dm-worker
    $ ansible-playbook start.yml --tags=dm-worker
    ```

### 重启 DM-master

在以下两种方法中任选一种，重启 DM-master 组件：

- 对 DM-master 执行滚动升级。

    ```bash
    $ ansible-playbook rolling_update.yml --tags=dm-master
    ```

- 停止 DM-master，然后重启。

    ```bash
    $ ansible-playbook stop.yml --tags=dm-master
    $ ansible-playbook start.yml --tags=dm-master
    ```

## 更新组件版本

1. 下载 DM 二进制文件。

    1. 从 `downloads` 目录删除已有文件。

        ```
        $ cd /home/tidb/dm-ansible
        $ rm -rf downloads
        ```

    2. 用 Playbook 下载 inventory.ini 文件中指定版本的最新 DM 二进制文件。这会自动替换 `/home/tidb/dm-ansible/resource/bin/` 中已有文件。

        ```
        $ ansible-playbook local_prepare.yml
        ```

2. 使用 Ansible 执行滚动升级。

    1. 对 DM-worker 实例执行滚动升级：

        ```
        ansible-playbook rolling_update.yml --tags=dm-worker
        ```

    2. 对 DM-master 实例执行滚动升级：

        ```
        ansible-playbook rolling_update.yml --tags=dm-master
        ```

    3. 升级 dmctl：

        ```
        ansible-playbook rolling_update.yml --tags=dmctl
        ```

    4. 对 DM-worker， DM-master， 以及 dmctl 整体执行滚动升级：

        ```
        ansible-playbook rolling_update.yml
        ```

## 创建 DM-worker 实例

假设您想要在机器 `172.16.10.74` 上创建一个名为 `dm_worker3` 的 DM-worker 实例，按以下步骤操作：

1. 为中控机设置 SSH 互信以及 sudo 规则。

    1. 参考[在中控机上配置 SSH 互信和 sudo 规则](/v2.1/how-to/deploy/data-migration-with-ansible.md#第-5-步-在中控机上配置-ssh-互信和-sudo-规则)，使用 `tidb` 用户登录至中控机，并将 `172.16.10.74` 添加至 `hosts.ini` 文件中的 `[servers]` 部分。

        ```
        $ cd /home/tidb/dm-ansible
        $ vi hosts.ini
        [servers]
        172.16.10.74

        [all:vars]
        username = tidb
        ```

    2. 运行以下命令。根据屏幕提示，输入 `root` 用户密码以部署 `172.16.10.74`。

        ```
        $ ansible-playbook -i hosts.ini create_users.yml -u root -k
        ```

        该步在 `172.16.10.74` 机器上创建了一个 `tidb` 用户，设置了 sudo 规则，并为中控机与该机器配置了 SSH 互信。

2. 修改 `inventory.ini` 文件，创建新 DM-worker 实例 `dm_worker3`。

    ```
    [dm_worker_servers]
    dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2  source_id="mysql-replica-02" ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker3 source_id="mysql-replica-03" ansible_host=172.16.10.74 server_id=103 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

3. 部署新 DM-worker 实例。

    ```
    $ ansible-playbook deploy.yml --tags=dm-worker -l dm_worker3
    ```

4. 启用新 DM-worker 实例。

    ```
    $ ansible-playbook start.yml --tags=dm-worker -l dm_worker3
    ```

5. 配置并重启 DM-master 服务。

    ```
    $ ansible-playbook rolling_update.yml --tags=dm-master
    ```

6. 配置并重启 Prometheus 服务。

    ```
    $ ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

## 下线 DM-worker 实例

假设您想要下线的 DM-worker 实例为 `dm_worker3`。按以下步骤操作：

1. 关闭您想要下线的 DM-worker 实例。

    ```
    $ ansible-playbook stop.yml --tags=dm-worker -l dm_worker3
    ```

2. 修改 `inventory.ini` 文件，注释或删除 `dm_worker3` 实例所在行。

    ```
    [dm_worker_servers]
    dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 source_id="mysql-replica-02" ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    # dm_worker3 source_id="mysql-replica-03" ansible_host=172.16.10.74 server_id=103 mysql_host=172.16.10.83 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306 # Comment or delete this line
    ```

3. 配置并重启 DM-master 服务。

    ```
    $ ansible-playbook rolling_update.yml --tags=dm-master
    ```

4. 配置并重启 Prometheus 服务。

    ```
    $ ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

## 替换/迁移 DM-master 实例

假设机器 `172.16.10.71` 需要进行维护或者已崩溃，需要将 DM-master 实例从 `172.16.10.71` 迁移至 `172.16.10.80`。按以下步骤操作：

1. 为中控机设置 SSH 互信以及 sudo 规则。

    1. 参考[在中控机上配置 SSH 互信和 sudo 规则](/v2.1/how-to/deploy/data-migration-with-ansible.md#第-5-步-在中控机上配置-ssh-互信和-sudo-规则)，使用 `tidb` 账户登录至中控机，并将 `172.16.10.80` 添加至 `hosts.ini` 文件中的 `[servers]` 部分。

        ```
        $ cd /home/tidb/dm-ansible
        $ vi hosts.ini
        [servers]
        172.16.10.80

        [all:vars]
        username = tidb
        ```

     2. 运行以下命令。根据屏幕提示，输入 `root` 用户密码以部署 `172.16.10.80`。

        ```
        $ ansible-playbook -i hosts.ini create_users.yml -u root -k
        ```

        该步在 `172.16.10.80` 机器上创建了一个 `tidb` 用户，设置了 sudo 规则，并为中控机与该机器配置了 SSH 互信。

2. 关闭待替换的 DM-master 实例。

    > **注意：**
    >
    > 如果机器 `172.16.10.71` 宕机，无法通过 SSH 登录，请忽略此步。

    ```
    $ ansible-playbook stop.yml --tags=dm-master
    ```

3. 修改 `inventory.ini` 文件。注释或删除待替换实例所在行，同时为新 DM-master 实例添加相关信息。

    ```ini
    [dm_master_servers]
    # dm_master ansible_host=172.16.10.71
    dm_master ansible_host=172.16.10.80
    ```

4. 部署新 DM-master 实例。

    ```
    $ ansible-playbook deploy.yml --tags=dm-master
    ```

5. 启用新 DM-master 实例。

    ```
    $ ansible-playbook start.yml --tags=dm-master
    ```

6. 更新 dmctl 配置文件。

    ```
    ansible-playbook rolling_update.yml --tags=dmctl
    ```

## 替换/迁移 DM-worker 实例

假设机器 `172.16.10.72` 需要进行维护或者已崩溃，您需要将 `dm_worker1` 实例从 `172.16.10.72` 迁移至 `172.16.10.75`。按以下步骤操作：

1. 为中控机设置 SSH 互信以及 sudo 规则。

    1. 参考[在中控机上配置 SSH 互信和 sudo 规则](/v2.1/how-to/deploy/data-migration-with-ansible.md#第-5-步-在中控机上配置-ssh-互信和-sudo-规则)，使用 `tidb` 账户登录至中控机，并将 `172.16.10.75` 添加至 `hosts.ini` 文件中的 `[servers]` 部分。

        ```
        $ cd /home/tidb/dm-ansible
        $ vi hosts.ini
        [servers]
        172.16.10.75

        [all:vars]
        username = tidb
        ```

    2. 运行以下命令。根据屏幕提示，输入 `root` 用户密码以部署 `172.16.10.85`。

        ```
        $ ansible-playbook -i hosts.ini create_users.yml -u root -k
        ```

        该步在 `172.16.10.75` 上创建了一个 `tidb` 用户，设置了 sudo 规则，并为中控机与该机器配置了 SSH 互信。

2. 下线待替换 DM-worker 实例。

    > **注意：**
    >
    > 如果机器 `172.16.10.71` 宕机，无法通过 SSH 登录，请忽略此步。

    ```
    $ ansible-playbook stop.yml --tags=dm-worker -l dm_worker1
    ```

3. 修改 `inventory.ini` 文件，为新 DM-worker 实例添加相关信息。

    修改 `inventory.ini` 文件。注释或删除旧 `dm_worker1` 实例所在行；同时为新 `dm_worker1` 实例添加相关信息。

    如果希望从不同的 binlog position 或 GTID Sets 拉取 relay log，则也需要更新对应的 `{relay_binlog_name}` 或 `{relay_binlog_gtid}`。

    ```ini
    [dm_worker_servers]
    dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.75 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    # dm_worker1 source_id="mysql-replica-01" ansible_host=172.16.10.72 server_id=101 mysql_host=172.16.10.81 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306

    dm_worker2 source_id="mysql-replica-02" ansible_host=172.16.10.73 server_id=102 mysql_host=172.16.10.82 mysql_user=root mysql_password='VjX8cEeTX+qcvZ3bPaO4h0C80pe/1aU=' mysql_port=3306
    ```

4. 部署新 DM-worker 实例。

    ```
    $ ansible-playbook deploy.yml --tags=dm-worker -l dm_worker1
    ```

5. 迁移 relay log 数据。

    - 如果待替换 DM-worker 实例所在机器仍能访问，则可直接将该实例的 `{dm_worker_relay_dir}` 目录下的所有数据复制到新 DM-worker 实例的对应目录。

    - 如果待替换 DM-worker 实例所在机器已无法访问，可能需在第 9 步中手动恢复 relay log 目录等信息。

6. 启动新 DM-worker 实例。

    ```bash
    $ ansible-playbook start.yml --tags=dm-worker -l dm_worker1
    ```

7. 配置并重启 DM-master 服务。

    ```bash
    $ ansible-playbook rolling_update.yml --tags=dm-master
    ```

8. 配置并重启 Prometheus 服务。

    ```bash
    $ ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

9. 启动并验证数据迁移任务。

    使用 `start-task` 命令启动数据迁移任务，如果任务运行正常，则表示 DM-worker 迁移顺利完成；如果报类似如下错误，则需要对 relay log 目录进行手动修复。

    ```log
    fail to initial unit Sync of subtask test-task : UUID suffix 000002 with UUIDs [1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000001] not found
    ```

    如果待替换 DM-worker 所连接的上游 MySQL 已发生过切换，则会产生如上错误。此时可通过如下步骤手动修复：

    1. 使用 `stop-task` 命令停止数据迁移任务。

    2. 通过 `$ ansible-playbook stop.yml --tags=dm-worker -l dm_worker1` 停止 DM-worker 实例。

    3. 更新 relay log 子目录的后缀，例如将 `1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000001` 重命名为 `1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000002`。

    4. 更新 relay log 子目录索引文件 `server-uuid.index`，例如将其中的内容由 `1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000001` 变更为 `1ddbf6d3-d3b2-11e9-a4e9-0242ac140003.000002`。

    5. 通过 `$ ansible-playbook start.yml --tags=dm-worker -l dm_worker1` 启动 DM-worker 实例。

    6. 再次启动并验证数据迁移任务。

## 切换主从实例

该部分分两种情况描述如何使用 dmctl 完成主从实例切换。

### 虚拟 IP 环境下的上游主从切换

1. 使用 `query-status` 命令确认 relay 处理单元已获取主从切换前 master 实例的所有 binlog（`relayCatchUpMaster`）。
2. 使用 `pause-relay` 命令暂停 relay 处理。
3. 使用 `pause-task` 命令暂停所有运行任务。
4. 虚拟 IP 环境下的上游主从实例执行切换。
5. 使用 `switch-relay-master` 命令通知 relay 处理单元进行主从切换。
6. 使用 `resume-relay` 命令恢复 relay 处理，从新 master 实例读取 binlog。
7. 使用 `resume-task` 命令恢复之前的同步任务。

### 变更 IP 后的主从切换

1. 使用 `query-status` 命令确认 relay 处理单元已获取主从切换前 master 实例的所有 binlog（`relayCatchUpMaster`）。
2. 使用 `stop-task` 停止所有运行任务。
3. 修改 DM-worker 配置，并使用 DM-Ansible 对 DM-worker 进行滚动升级操作。
4. 使用 `start-task` 命令重新启动同步任务。
