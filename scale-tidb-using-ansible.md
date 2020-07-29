---
title: 使用 TiDB Ansible 扩容缩容 TiDB 集群
aliases: ['/docs-cn/dev/how-to/scale/with-ansible/']
---

# 使用 TiDB Ansible 扩容缩容 TiDB 集群

TiDB 集群可以在不影响线上服务的情况下进行扩容和缩容。

> **注意：**
>
> 以下缩容示例中，被移除的节点没有混合部署其他服务；如果混合部署了其他服务，不能按如下操作。

假设拓扑结构如下所示：

| Name | Host IP | Services |
| ---- | ------- | -------- |
| node1 | 172.16.10.1 | PD1 |
| node2 | 172.16.10.2 | PD2 |
| node3 | 172.16.10.3 | PD3, Monitor |
| node4 | 172.16.10.4 | TiDB1 |
| node5 | 172.16.10.5 | TiDB2 |
| node6 | 172.16.10.6 | TiKV1 |
| node7 | 172.16.10.7 | TiKV2 |
| node8 | 172.16.10.8 | TiKV3 |
| node9 | 172.16.10.9 | TiKV4 |

## 扩容 TiDB/TiKV 节点

例如，如果要添加两个 TiDB 节点（node101、node102），IP 地址为 172.16.10.101、172.16.10.102，可以进行如下操作：

1. 编辑 `inventory.ini` 文件和 `hosts.ini` 文件，添加节点信息。

    - 编辑 `inventory.ini`：

        ```ini
        [tidb_servers]
        172.16.10.4
        172.16.10.5
        172.16.10.101
        172.16.10.102

        [pd_servers]
        172.16.10.1
        172.16.10.2
        172.16.10.3

        [tikv_servers]
        172.16.10.6
        172.16.10.7
        172.16.10.8
        172.16.10.9

        [monitored_servers]
        172.16.10.1
        172.16.10.2
        172.16.10.3
        172.16.10.4
        172.16.10.5
        172.16.10.6
        172.16.10.7
        172.16.10.8
        172.16.10.9
        172.16.10.101
        172.16.10.102

        [monitoring_servers]
        172.16.10.3

        [grafana_servers]
        172.16.10.3
        ```

    现在拓扑结构如下所示：

    | Name | Host IP | Services |
    | ---- | ------- | -------- |
    | node1 | 172.16.10.1 | PD1 |
    | node2 | 172.16.10.2 | PD2 |
    | node3 | 172.16.10.3 | PD3, Monitor |
    | node4 | 172.16.10.4 | TiDB1 |
    | node5 | 172.16.10.5 | TiDB2 |
    | **node101** | **172.16.10.101**|**TiDB3** |
    | **node102** | **172.16.10.102**|**TiDB4** |
    | node6 | 172.16.10.6 | TiKV1 |
    | node7 | 172.16.10.7 | TiKV2 |
    | node8 | 172.16.10.8 | TiKV3 |
    | node9 | 172.16.10.9 | TiKV4 |

    - 编辑 `hosts.ini`：

        ```ini
        [servers]
        172.16.10.1
        172.16.10.2
        172.16.10.3
        172.16.10.4
        172.16.10.5
        172.16.10.6
        172.16.10.7
        172.16.10.8
        172.16.10.9
        172.16.10.101
        172.16.10.102

        [all:vars]
        username = tidb
        ntp_server = pool.ntp.org
        ```

2. 初始化新增节点。

    1. 在中控机上配置部署机器 SSH 互信及 sudo 规则：

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook -i hosts.ini create_users.yml -l 172.16.10.101,172.16.10.102 -u root -k
        ```

    2. 在部署目标机器上安装 NTP 服务：

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook -i hosts.ini deploy_ntp.yml -u tidb -b
        ```

    3. 在部署目标机器上初始化节点：

        {{< copyable "shell-regular" >}}

        ```bash
        ansible-playbook bootstrap.yml -l 172.16.10.101,172.16.10.102
        ```

    > **注意：**
    >
    > 如果 `inventory.ini` 中为节点配置了别名，如 `node101 ansible_host=172.16.10.101`，执行 ansible-playbook 时 -l 请指定别名，以下步骤类似。例如：`ansible-playbook bootstrap.yml -l node101,node102`

3. 部署新增节点：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook deploy.yml -l 172.16.10.101,172.16.10.102
    ```

4. 启动新节点服务：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook start.yml -l 172.16.10.101,172.16.10.102
    ```

5. 更新 Prometheus 配置并重启：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

6. 打开浏览器访问监控平台：`http://172.16.10.3:3000`，监控整个集群和新增节点的状态。

    可使用同样的步骤添加 TiKV 节点。但如果要添加 PD 节点，则需手动更新一些配置文件。

## 扩容 PD 节点

例如，如果要添加一个 PD 节点（node103），IP 地址为 172.16.10.103，可以进行如下操作：

1. 编辑 `inventory.ini` 文件，添加节点信息置于 `[pd_servers]` 主机组最后一行：

    ```ini
    [tidb_servers]
    172.16.10.4
    172.16.10.5

    [pd_servers]
    172.16.10.1
    172.16.10.2
    172.16.10.3
    172.16.10.103

    [tikv_servers]
    172.16.10.6
    172.16.10.7
    172.16.10.8
    172.16.10.9

    [monitored_servers]
    172.16.10.4
    172.16.10.5
    172.16.10.1
    172.16.10.2
    172.16.10.3
    172.16.10.103
    172.16.10.6
    172.16.10.7
    172.16.10.8
    172.16.10.9

    [monitoring_servers]
    172.16.10.3

    [grafana_servers]
    172.16.10.3
    ```

    现在拓扑结构如下所示：

    | Name | Host IP | Services |
    | ---- | ------- | -------- |
    | node1 | 172.16.10.1 | PD1 |
    | node2 | 172.16.10.2 | PD2 |
    | node3 | 172.16.10.3 | PD3, Monitor |
    | **node103** | **172.16.10.103** | **PD4** |
    | node4 | 172.16.10.4 | TiDB1 |
    | node5 | 172.16.10.5 | TiDB2 |
    | node6 | 172.16.10.6 | TiKV1 |
    | node7 | 172.16.10.7 | TiKV2 |
    | node8 | 172.16.10.8 | TiKV3 |
    | node9 | 172.16.10.9 | TiKV4 |

2. 初始化新增节点：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook bootstrap.yml -l 172.16.10.103
    ```

3. 部署新增节点：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook deploy.yml -l 172.16.10.103
    ```

4. 登录新增的 PD 节点，编辑启动脚本：`{deploy_dir}/scripts/run_pd.sh`

    1. 移除 `--initial-cluster="xxxx" \` 配置，注意这里不能在行开头加注释符 #。

    2. 添加 `--join="http://172.16.10.1:2379" \`，IP 地址 （172.16.10.1） 可以是集群内现有 PD IP 地址中的任意一个。

    3. 在新增 PD 节点中启动 PD 服务：

        {{< copyable "shell-regular" >}}

        ```bash
        {deploy_dir}/scripts/start_pd.sh
        ```

        > **注意：**
        >
        > 启动前，需要通过 [PD Control](/pd-control.md) 工具确认当前 PD 节点的 `health` 状态均为 "true"，否则 PD 服务会启动失败，同时日志中报错 `["join meet error"] [error="etcdserver: unhealthy cluster"]`。

    4. 使用 `pd-ctl` 检查新节点是否添加成功：

        {{< copyable "shell-regular" >}}

        ```bash
        /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.16.10.1:2379" -d member
        ```

5. 启动监控服务：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook start.yml -l 172.16.10.103
    ```

    > **注意：**
    >
    > 如果使用了别名（inventory_name），则也需要使用 `-l` 指定别名。

6. 更新集群的配置：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook deploy.yml
    ```

7. 重启 Prometheus，新增扩容的 PD 节点的监控：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml --tags=prometheus
    ansible-playbook start.yml --tags=prometheus
    ```

8. 打开浏览器访问监控平台：`http://172.16.10.3:3000`，监控整个集群和新增节点的状态。

> **注意：**
>
> TiKV 中的 PD Client 会缓存 PD 节点列表，但目前不会定期自动更新，只有在 PD leader 发生切换或 TiKV 重启加载最新配置后才会更新；为避免 TiKV 缓存的 PD 节点列表过旧的风险，在扩缩容 PD 完成后，PD 集群中至少要包含两个扩缩容操作前就已经存在的 PD 节点成员，如果不满足该条件需要手动执行 PD transfer leader 操作，更新 TiKV 中的 PD 缓存列表。

## 缩容 TiDB 节点

例如，如果要移除一个 TiDB 节点（node5），IP 地址为 172.16.10.5，可以进行如下操作：

1. 停止 node5 节点上的服务：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml -l 172.16.10.5
    ```

2. 编辑 `inventory.ini` 文件，移除节点信息：

    ```ini
    [tidb_servers]
    172.16.10.4
    #172.16.10.5  # 注释被移除节点

    [pd_servers]
    172.16.10.1
    172.16.10.2
    172.16.10.3

    [tikv_servers]
    172.16.10.6
    172.16.10.7
    172.16.10.8
    172.16.10.9

    [monitored_servers]
    172.16.10.4
    #172.16.10.5  # 注释被移除节点
    172.16.10.1
    172.16.10.2
    172.16.10.3
    172.16.10.6
    172.16.10.7
    172.16.10.8
    172.16.10.9

    [monitoring_servers]
    172.16.10.3

    [grafana_servers]
    172.16.10.3
    ```

    现在拓扑结构如下所示：

    | Name | Host IP | Services |
    | ---- | ------- | -------- |
    | node1 | 172.16.10.1 | PD1 |
    | node2 | 172.16.10.2 | PD2 |
    | node3 | 172.16.10.3 | PD3, Monitor |
    | node4 | 172.16.10.4 | TiDB1 |
    | **node5** | **172.16.10.5** | **TiDB2 已删除** |
    | node6 | 172.16.10.6 | TiKV1 |
    | node7 | 172.16.10.7 | TiKV2 |
    | node8 | 172.16.10.8 | TiKV3 |
    | node9 | 172.16.10.9 | TiKV4 |

3. 更新 Prometheus 配置并重启：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

4. 打开浏览器访问监控平台：`http://172.16.10.3:3000`，监控整个集群的状态。

## 缩容 TiKV 节点

例如，如果要移除一个 TiKV 节点（node9），IP 地址为 172.16.10.9，可以进行如下操作：

1. 使用 `pd-ctl` 从集群中移除节点：

    1. 查看 node9 节点的 store id：

        {{< copyable "shell-regular" >}}

        ```bash
        /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.16.10.1:2379" -d store
        ```

    2. 从集群中移除 node9，假如 store id 为 10：

        {{< copyable "shell-regular" >}}

        ```bash
        /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.16.10.1:2379" -d store delete 10
        ```

2. 使用 Grafana 或者 `pd-ctl` 检查节点是否下线成功（下线需要一定时间，下线节点的状态变为 Tombstone 就说明下线成功了）：

    {{< copyable "shell-regular" >}}

    ```bash
    /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.16.10.1:2379" -d store 10
    ```

3. 下线成功后，停止 node9 上的服务：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml -l 172.16.10.9
    ```

4. 编辑 `inventory.ini` 文件，移除节点信息：

    ```ini
    [tidb_servers]
    172.16.10.4
    172.16.10.5

    [pd_servers]
    172.16.10.1
    172.16.10.2
    172.16.10.3

    [tikv_servers]
    172.16.10.6
    172.16.10.7
    172.16.10.8
    #172.16.10.9  # 注释被移除节点

    [monitored_servers]
    172.16.10.4
    172.16.10.5
    172.16.10.1
    172.16.10.2
    172.16.10.3
    172.16.10.6
    172.16.10.7
    172.16.10.8
    #172.16.10.9  # 注释被移除节点

    [monitoring_servers]
    172.16.10.3

    [grafana_servers]
    172.16.10.3
    ```

    现在拓扑结构如下所示：

    | Name | Host IP | Services |
    | ---- | ------- | -------- |
    | node1 | 172.16.10.1 | PD1 |
    | node2 | 172.16.10.2 | PD2 |
    | node3 | 172.16.10.3 | PD3, Monitor |
    | node4 | 172.16.10.4 | TiDB1 |
    | node5 | 172.16.10.5 | TiDB2 |
    | node6 | 172.16.10.6 | TiKV1 |
    | node7 | 172.16.10.7 | TiKV2 |
    | node8 | 172.16.10.8 | TiKV3 |
    | **node9** | **172.16.10.9** | **TiKV4 已删除** |

5. 更新 Prometheus 配置并重启：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook rolling_update_monitor.yml --tags=prometheus
    ```

6. 打开浏览器访问监控平台：`http://172.16.10.3:3000`，监控整个集群的状态。

## 缩容 PD 节点

例如，如果要移除一个 PD 节点（node2），IP 地址为 172.16.10.2，可以进行如下操作：

1. 使用 `pd-ctl` 从集群中移除节点：

    1. 查看 node2 节点的 name：

        {{< copyable "shell-regular" >}}

        ```bash
        /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.16.10.1:2379" -d member
        ```

    2. 从集群中移除 node2，假如 name 为 pd2：

        {{< copyable "shell-regular" >}}

        ```bash
        /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.16.10.1:2379" -d member delete name pd2
        ```

2. 使用 `pd-ctl` 检查节点是否下线成功（PD 下线会很快，结果中没有 node2 节点信息即为下线成功）：

    {{< copyable "shell-regular" >}}

    ```bash
    /home/tidb/tidb-ansible/resources/bin/pd-ctl -u "http://172.16.10.1:2379" -d member
    ```

3. 下线成功后，停止 node2 上的服务：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml -l 172.16.10.2
    ```

    > **注意：**
    >
    > 此示例中 `172.16.10.2` 服务器上只有 PD 节点才可以如上操作，如果该服务器上还有其他服务（例如 `TiDB`），则还需要使用 `-t` 来指定服务（例如 `-t tidb`）。

4. 编辑 `inventory.ini` 文件，移除节点信息：

    ```ini
    [tidb_servers]
    172.16.10.4
    172.16.10.5

    [pd_servers]
    172.16.10.1
    #172.16.10.2  # 注释被移除节点
    172.16.10.3

    [tikv_servers]
    172.16.10.6
    172.16.10.7
    172.16.10.8
    172.16.10.9

    [monitored_servers]
    172.16.10.4
    172.16.10.5
    172.16.10.1
    #172.16.10.2  # 注释被移除节点
    172.16.10.3
    172.16.10.6
    172.16.10.7
    172.16.10.8
    172.16.10.9

    [monitoring_servers]
    172.16.10.3

    [grafana_servers]
    172.16.10.3
    ```

    现在拓扑结构如下所示：

    | Name | Host IP | Services |
    | ---- | ------- | -------- |
    | node1 | 172.16.10.1 | PD1 |
    | **node2** | **172.16.10.2** | **PD2 已删除** |
    | node3 | 172.16.10.3 | PD3, Monitor |
    | node4 | 172.16.10.4 | TiDB1 |
    | node5 | 172.16.10.5 | TiDB2 |
    | node6 | 172.16.10.6 | TiKV1 |
    | node7 | 172.16.10.7 | TiKV2 |
    | node8 | 172.16.10.8 | TiKV3 |
    | node9 | 172.16.10.9 | TiKV4 |

5. 更新集群的配置：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook deploy.yml
    ```

6. 重启 Prometheus，移除缩容的 PD 节点的监控：

    {{< copyable "shell-regular" >}}

    ```bash
    ansible-playbook stop.yml --tags=prometheus
    ansible-playbook start.yml --tags=prometheus
    ```

7. 打开浏览器访问监控平台：`http://172.16.10.3:3000`，监控整个集群的状态。

> **注意：**
>
> TiKV 中的 PD Client 会缓存 PD 节点列表，但目前不会定期自动更新，只有在 PD leader 发生切换或 TiKV 重启加载最新配置后才会更新；为避免 TiKV 缓存的 PD 节点列表过旧的风险，在扩缩容 PD 完成后，PD 集群中至少要包含两个扩缩容操作前就已经存在的 PD 节点成员，如果不满足该条件需要手动执行 PD transfer leader 操作，更新 TiKV 中的 PD 缓存列表。