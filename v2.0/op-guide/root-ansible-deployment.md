---
title: 使用 root 用户远程连接 TiDB Ansible 部署方案
category: deployment
---

# 使用 root 用户远程连接 TiDB Ansible 部署方案

> Ansible 远程连接用户(即 incentory.ini 文件中的 ansible_user)，从中控机使用 root 用户 SSH 到部署目标机器部署，不推荐采用该方式安装。

1.  修改 `inventory.ini`, 本例使用 `tidb` 帐户作为服务运行用户：

    取消 `ansible_user = root` 、`ansible_become = true` 及 `ansible_become_user` 注释，给 `ansible_user = tidb` 添加注释：

    ```ini
    ## Connection
    # ssh via root:
    ansible_user = root
    ansible_become = true
    ansible_become_user = tidb

    # ssh via normal user
    # ansible_user = tidb
    ```

2.  使用 `local_prepare.yml` playbook, 联网下载 TiDB binary 到中控机：

    ```
    ansible-playbook local_prepare.yml
    ```

3.  初始化系统环境，修改内核参数

    > 如服务运行用户尚未建立，此初始化操作会自动创建该用户。

    ```
    ansible-playbook bootstrap.yml
    ```

    如果 ansible 使用 root 用户远程连接需要密码, 使用 -k 参数，执行其他 playbook 同理：

    ```
    ansible-playbook bootstrap.yml -k
    ```

4.  部署 TiDB 集群软件

    ```
    ansible-playbook deploy.yml -k
    ```

5.  启动 TiDB 集群

    ```
    ansible-playbook start.yml -k
    ```
