---
title: TiFlash 集群扩缩容
aliases: ['/docs-cn/v3.1/tiflash/scale-tiflash/','/docs-cn/v3.1/reference/tiflash/scale/']
---

# TiFlash 集群扩缩容

本文介绍扩缩容 TiFlash 集群节点的步骤。

## 扩容 TiFlash 节点

以在节点 192.168.1.1 上部署 TiFlash 为例，扩容该 TiFlash 节点的步骤如下。

1. 编辑 `inventory.ini` 文件，添加该 TiFlash 节点信息（目前只支持 ip，不支持域名）：

    {{< copyable "" >}}

    ```ini
    [tiflash_servers]
    192.168.1.1
    ```

2. 编辑 `hosts.ini` 文件，添加节点信息：

    {{< copyable "" >}}

    ```ini
    [servers]
    192.168.1.1

    [all:vars]
    username = tidb
    ntp_server = pool.ntp.org
    ```

3. 初始化新增节点：

    - 在中控机上配置部署机器 SSH 互信及 sudo 规则：

        {{< copyable "shell-regular" >}}

        ```shell
        ansible-playbook -i hosts.ini create_users.yml -l 192.168.1.1 -u root -k
        ```

    - 在部署目标机器上安装 NTP 服务：

        {{< copyable "shell-regular" >}}

        ```shell
        ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b
        ```

    - 在部署目标机器上初始化节点：

        {{< copyable "shell-regular" >}}

        ```shell
        ansible-playbook bootstrap.yml -l 192.168.1.1
        ```

4. 部署新增节点：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook deploy.yml -l 192.168.1.1
    ```

5. 启动新节点服务：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook start.yml -l 192.168.1.1
    ```

6. 更新 Prometheus 配置并重启：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

7. 打开浏览器访问监控平台，监控整个集群和新增节点的状态。

## 缩容 TiFlash 节点

以停止 192.168.1.1 节点的服务为例，缩容该 TiFlash 节点的步骤如下。

> **注意：**
>
> 本节介绍的下线流程不会删除下线节点上的数据文件，如需再次上线，请先手动删除。

1. 首先参考[下线 TiFlash 节点](/tiflash/maintain-tiflash.md#下线-tiflash-节点)章节，对要进行缩容的 TiFlash 节点进行下线操作。

2. 使用 Grafana 或者 pd-ctl 检查节点是否下线成功（下线需要一定时间）。

3. 等待 TiFlash 对应的 `store` 消失，或者 `state_name` 变成 `Tombstone` 后，执行如下命令关闭 TiFlash 进程：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook stop.yml -l 192.168.1.1
    ```

    如果该节点仍有其他服务，只希望停止 TiFlash 则请注明 TiFlash 服务：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook stop.yml -t tiflash -l 192.168.1.1
    ```

4. 编辑 `inventory.ini` 和 `hosts.ini` 文件，移除节点信息。

5. 更新 Prometheus 配置并重启：

    {{< copyable "shell-regular" >}}

    ```shell
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

6. 打开浏览器访问监控平台，监控整个集群的状态。
