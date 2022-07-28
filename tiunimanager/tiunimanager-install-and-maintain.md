---
title: TiUniManager 安装和运维指南
summary: 了解 TiUniManager 安装部署流程，指导数据库管理员完成 TiUniManager 的部署和配置。
---

# TiUniManager 安装和运维指南

本文档介绍 TiUniManager 的安装部署流程以及运维方法，指导数据库管理员完成 TiUniManager 的部署和配置。

## 软硬件环境配置

本节介绍部署 TiUniManager 前需要满足的软硬件环境配置要求。

### Linux 操作系统版本

要部署和运行 TiUniManager 服务，确保 Linux 操作系统的版本满足以下要求：

| Linux 操作系统 | 版本 |
| :--- | :--- |
| Red Hat Enterprise Linux | 7.3 及以上的 7.x 版本 |
| CentOS  | 7.3 及以上的 7.x 版本 |

### 中控机软件配置

TiUniManager 中控机是运行 TiUniManager 服务的中央控制节点。你可通过登录 TiUniManager 中控机上的 Web console 或 OpenAPI 完成对 TiDB 集群的日常管理。中控机的软件配置要求如下：

| 软件 | 版本 |
| :--- | :--- |
| sshpass | 1.06 及以上
| TiUP | 1.9.0 及以上 |

### 服务器配置

TiUniManager 支持部署和运行在 Intel x86-64 架构的 64 位通用硬件服务器平台上。对于开发、测试、及生产环境的服务器硬件配置（不包含操作系统 OS 本身的占用）有以下要求：

#### 开发及测试环境

在开发及测试环境中，对服务器硬件配置要求如下：

| 组件 | CPU   | 内存   | 硬盘类型 | 网络                 | 实例数量（最低要求） |
| ---- | ----- | ------ | -------- | -------------------- | -------------------- |
| TiUniManager | 8 核+ | 16 GB+ | SAS      | 万兆网卡（2 块最佳） | 1                    |

#### 生产环境

在生产环境中，对服务器硬件配置要求如下：

| 组件 | CPU    | 内存    | 硬盘类型 | 网络                 | 实例数量（最低要求） |
| ---- | ------ | ------- | -------- | -------------------- | -------------------- |
| TiUniManager | 48 核+ | 128 GB+ | SAS/SSD  | 万兆网卡（2 块最佳） | 1                    |

### 网络要求

TiUniManager 正常运行需要网络环境提供如下端口配置，管理员可根据实际环境中 TiUniManager 组件部署的方案，在网络侧和主机侧开放相关端口：

| 组件       | 默认端口     | 说明                                   |
| ---------- | ------------ | -------------------------------------- |
| Web server | 4180 或 4183 | HTTP 端口：4180<br />HTTPS 端口：4183 |
| OpenAPI server| 4100 或 4103 | OpenAPI 服务端口: 4100<br />OpenAPI 监控端口：4103 |
| Cluster server | 4101 或 4104 | 集群服务端口 |
| File server | 4102 或 4105 | 文件上传或下载的服务器端口 |
| etcd | 4106 或 4107 | etcd 服务端口 |
| Elasticsearch server | 4108 | Elasticsearch 服务端口 |
| Kibana server | 4109 | Kibana 服务端口 |
| Prometheus | 4110 | Prometheus 服务端口 |
| Grafana server | 4111 | Grafana 服务端口 |
| Alertmanager server | 4112 或 4113 | 告警管理服务端口 |
| Jaeger(tracer server ) | 4114 到 4123 | Jaeger 服务端口 |
| node_exporter | 4124 | TiUniManager 主机系统上报信息的通信端口 |

## 客户端 Web 浏览器要求

你可在较新版本的常见桌面浏览器中使用 TiUniManager，浏览器的版本要求如下：

- Chrome \> 79
- Firefox \> 72
- Microsoft Edge \> 79
- Safari \> 14

> **注意：**
>
> 若使用旧版本浏览器或其他浏览器访问 TiUniManager，部分界面可能无法正常工作。

## 拓扑模板

在线部署 TiUniManager 前，你需要准备好 YAML 拓扑文件。TiUniManager 离线包中包含 YAML 拓扑文件模板。本节介绍用于部署 TiUniManager 拓扑配置模版。见 [TiUniManager 拓扑配置模版 config.yaml（单机版）](https://github.com/pingcap/docs-cn/blob/master/config-templates/em-topology-config.yaml)。

如果 TiUniManager 中控机通过用户名密钥访问 TiDB 资源机，需要参照指定 TiUniManager 中控机登录 TiDB 资源机的用户名和密钥，在配置文件 `config.yaml` 中指定用户名和密钥。

## 离线部署 TiUniManager

本节介绍如何在离线环境部署 TiUniManager。当前 TiUniManager 只支持通过离线部署。

1. 通过 `https://download.pingcap.org/em-enterprise-server-${version}-linux-amd64.tar.gz` 下载 TiUniManager 离线安装包。

    下载链接中的 `${version}` 为 TiUniManager 的版本号。例如，`v1.0.2` 版本的下载链接为 `https://download.pingcap.org/em-enterprise-server-v1.0.2-linux-amd64.tar.gz`。在下载时，你需要将链接中的 `${version}` 替换为目标版本号。

2. 发送 TiUniManager 离线安装包至 TiUniManager 中控机。

    离线安装包放置于 TiUniManager 中控机，使用具有 sudo 权限的账号执行后续操作。

3. 解压 TiUniManager 离线包。

    {{< copyable "shell-regular" >}}

    ```shell
    tar xzvf em-enterprise-server-${version}-linux-amd64.tar.gz
    ```

4. 安装 TiUniManager。进入解压后的目录，执行 `install.sh` 脚本。

    {{< copyable "shell-regular" >}}

    ```shell
    sudo sh em-enterprise-server-${version}-linux-amd64/install.sh <TiUniManager 中控机 IP>
    ```

5. 声明环境变量。

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 声明环境变量，使 tiup 工具生效
    source /home/tidb/.bash_profile
    ```

6. 生成 tidb 帐户下的密钥。

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 生成 rsa 密钥
    ssh-keygen -t rsa

    # 复制密钥到 tiup_rsa
    cp /home/tidb/.ssh/id_rsa /home/tidb/.ssh/tiup_rsa
    ```

7. 编辑拓扑配置文件。根据实际环境，你可编辑位于 `/home/tidb/` 下的拓扑配置文件 `config.yaml`。

8. 导入 TiDB Server 离线镜像包。

    离线环境下，需要在 TiUniManager 中控机本地目录上导入 TiDB 离线镜像包，否则无法通过 TiUniManager 中控机完成对 TiDB 集群的日常管理。

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 下载解压 TiDB Server 离线镜像包，将 ${version} 手动替换为实际的 TiDB 版本号。

    wget https://download.pingcap.org/tidb-community-server-${version}-linux-amd64.tar.gz
    tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz

    # 导入离线镜像包
    TIUP_HOME=/home/tidb/.tiup tiup mirror merge tidb-community-server-${version}-linux-amd64
    ```

    在 TiUniManager 中控机上查看本地 TiDB 镜像源。

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 查看 TiDB 镜像源地址
    tiup mirror show
    ```

9. 执行命令部署 TiUniManager。

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 部署名称为 "em-test" 的 TiUniManager，注意这里的版本号不带 v，比如 v1.0.0 的版本号，正确的输入是 1.0.0
    TIUP_HOME=/home/tidb/.em tiup em deploy em-test <版本号> config.yaml -u <具有sudo权限的账号> -p

    # 启动 TiUniManager
    TIUP_HOME=/home/tidb/.em tiup em start em-test
    ```

## 指定 TiUniManager 中控机登录 TiDB 资源机的帐户和密钥

默认情况下，你可以通过 TiUniManager Web 控制台**资源管理** > **导入主机**页面提供的主机资源模板填写 TiDB 资源机帐户和密码。

如果用户环境中不允许帐号密码方式登录 TiDB 资源机，可在 `config.yaml` 文件中进行配置，以帐户密钥方式登录 TiDB 资源机。`config.yaml` 中相关配置项如下：

| 配置描述 | 配置参数名 | 示例值 |
| --- | --- | --- |
| login-host-user | 登录 TiDB 资源机的用户名 | tidb |
| login-private-key-path | 位于 TiUniManager 中控机上登录 TiDB 资源机使用的私钥路径 | /home/tidb/.ssh/id_rsa |
| login-public-key-path | 位于 TiUniManager 中控机登录 TiDB 资源机使用的公钥路径 | /home/tidb/.ssh/id_rsa.pub |

## 升级 TiUniManager（适用于 v1.0.1 及以上版本）

本节适用于安装过 TiUniManager v1.0.1 及以上版本，并打算升级 TiUniManager 的用户。如首次安装可跳过本节。

> **注意：**
>
> - 本节介绍的方法仅适用于从 TiUniManager v1.0.1 升级至 v1.0.2 及以上版本，不适用于从 v1.0.0 升级至 v1.0.1 及以上版本。
> - 如果你已安装 TiUniManager v1.0.0 版本，想要升级至 v1.0.1 及以上版本，则需要先参考[升级 TiUniManager v1.0.0 至 v1.0.1](#升级-tiunimanager-v100-至-v101) 进行升级，再参考本节内容从 v1.0.1 升级至较新的目标版本。
> - 在 v1.0.0 和 v1.0.1 中，TiUniManager 原名为 TiDB Enterprise Manager。自 v1.0.2 起正式更名为 TiUniManager。

1. 升级 TiUniManager 离线包。

    参考[离线部署 TiUniManager](#离线部署-tiunimanager) 中第 1-3 步：通过 TiUniManager 产品团队获得最新 TiUniManager 离线包，发送 TiUniManager 离线安装包至目标集群的 TiUniManager 中控机，解压离线包。然后执行下面命令更新 TiUniManager 离线包。

    {{< copyable "shell-regular" >}}

    ```shell
    # user 为之前部署 TiUniManager 的帐户，默认为 tidb。${version} 为 TiUniManager 的版本号，需要手动替换为实际的版本号。
    sudo sh em-enterprise-server-${version}-linux-amd64/update.sh <user>
    ```

2. 执行升级 TiUniManager 命令。

    {{< copyable "shell-regular" >}}

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 将集群 <cluster-name> 升级到特定版本 <version>
    # 目前仅支持原地停机升级，并且暂不支持版本降级和回退。为安全起见，请按照 停止集群 > 备份 tiunimanager 元数据 > 升级集群的流程操作
    TIUP_HOME=/home/tidb/.em tiup em upgrade <cluster-name> <version>
    ```

## 升级 TiUniManager v1.0.0 至 v1.0.1

本节介绍的方法适用于 从 v1.0.0 升级至 v1.0.1。如需升级至更高版本，请先升级至 v1.0.1，再参考[升级 TiUniManager（适用于 v1.0.1 及以上版本）](#升级-tiunimanager适用于-v101-及以上版本)进行升级。如首次安装可跳过本节。

> **注意：**
>
> 在 v1.0.0 和 v1.0.1 中，TiUniManager 原名为 TiDB Enterprise Manager。自 v1.0.2 起正式更名为 TiUniManager。

1. 升级 TiUniManager 离线包。

    参考[离线部署 TiUniManager](#离线部署-tiunimanager) 中第 1-3 步：通过 TiUniManager 产品团队获得最新 TiUniManager 离线包，发送 TiUniManager 离线安装包至目标集群的 TiUniManager 中控机，解压离线包。然后执行下面命令更新 TiUniManager 离线包。

    {{< copyable "shell-regular" >}}

    ```shell
    # user 为之前部署 TiUniManager 的帐户，默认为 tidb
    sudo sh em-enterprise-server-v1.0.1-linux-amd64/update.sh <user>
    ```

2. 做升级 TiUniManager 之前的准备。

    执行以下命令为 TiUniManager 升级做准备。以下命令会自动备份 TiUniManager v1.0.0 中的数据。请注意，执行完此命令后直至升级完成，请不要再通过 TiUniManager 界面做其它操作，以避免备份未包含最新数据导致升级后数据丢失的情况。

    {{< copyable "shell-regular" >}}

    ```shell
    # user 为之前部署 TiUniManager v1.0.0 的帐户，默认为 tidb
    # cluster-name 为当前部署的 TiUniManager 名称，默认为 em-test
    sudo sh em-enterprise-server-v1.0.1-linux-amd64/prepare_upgrade.sh <user> <TiUniManager 中控机 IP> <cluster-name>
    ```

3. 检查新的 TiUniManager 部署拓扑文件。

    如果你在部署 TiUniManager v1.0.0 时曾对 `config.yaml` 文件做了自定义修改，请参考下列子步骤查看 v1.0.0 的配置文件 `config.yaml` 和待部署 v1.0.1 配置文件 `config-v1.0.1.yaml` 的区别，并做相应修改。

    1. 切换至 `tidb` 账号。

        {{< copyable "shell-regular" >}}

        ```shell
        su - tidb
        ```

    2. 查看配置变更。

        对比 `config.yaml` 和 `config-v1.0.1.yaml` 生效内容的差异。如果差异仅为 `db_path` 所在行，则可跳过本步骤，无须执行后续子步骤（备份 `db_path` 以及更新 `config-v1.0.1.yaml`），可直接进入删除 TiUniManager v1.0.0 的步骤。如果差异不仅有 `db_path` 所在行，还存在其它差异，则需要继续执行后续子步骤（备份 `db_path` 以及更新 `config-v1.0.1.yaml`）。

        {{< copyable "shell-regular" >}}

        ```shell
        diff config.yaml config-v1.0.1.yaml
        ```

    3. 记下 `config-v1.0.1.yaml` 中的数据备份路径 `db_path`。

       `db_path` 为 TiUniManager 备份数据的路径。在“升级 TiUniManager 之前的准备”这一步中 TiUniManager 已经自动在 `config-v1.0.1.yaml` 中写好了默认的 v1.0.1 数据备份路径，此前已备份的 v1.0.0 数据将恢复到该路径下。

        查看 `config-v1.0.1.yaml` 中的 `db_path`，记下该行内容，在以下子步骤 5 中更新 `config-v1.0.1.yaml` 时需要用到该行内容。示例如下：

        ```yaml
        db_path: "/home/tidb/em-backup-20220511-154415/em.db"
        ```

    4. 覆盖 `config-v1.0.1.yaml`。

       将 TiUniManager v1.0.0 的 `config.yaml` 文件复制一份并覆盖 v1.0.1 的 `config-v1.0.1.yaml`。

        ```shell
        cp config.yaml config-v1.0.1.yaml
        ```

    5. 更新 `config-v1.0.1.yaml`。

        覆盖配置文件后，将子步骤 3 中拷贝的 `db_path` 填写至 `config-v1.0.1.yaml`，注意空格的缩进。示例如下：

        ```yaml
        em_cluster_servers:
          - host: 127.0.0.1
            db_path: "/home/tidb/em-backup-20220511-154415/em.db"
        ```

4. 删除 TiUniManager v1.0.0。

    {{< copyable "shell-regular" >}}

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 查看现有 TiUniManager 服务
    TIUP_HOME=/home/tidb/.em tiup em list

    # 删除指定的 TiUniManager 服务
    TIUP_HOME=/home/tidb/.em tiup em destroy <cluster-name>
    ```

5. 部署 TiUniManager v1.0.1。

    {{< copyable "shell-regular" >}}

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 更新 em 工具
    TIUP_HOME=/home/tidb/.em tiup update em
    TIUP_HOME=/home/tidb/.em tiup update --all

    # 部署名称为 "em-test" 的 TiUniManager
    TIUP_HOME=/home/tidb/.em tiup em deploy em-test 1.0.1 config-v1.0.1.yaml -u <具有sudo权限的账号> -p

    # 启动 TiUniManager
    TIUP_HOME=/home/tidb/.em tiup em start em-test

    # 将 db_path 注释掉。如果不注释，后续对 em 进行重启、扩容等操作时 TiUniManager 可能会将数据变更还原
    sed -i "s/  db_path:/# db_path:/" /home/tidb/.em/storage/em/clusters/em-test/meta.yaml
    ```

6. 重建资源机器的 filebeat。

    {{< copyable "shell-regular" >}}

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 重建资源机器 filebeat
    TIUP_HOME=/home/tidb/.em tiup em scale-out em-test /home/tidb/em-v1.0.0-backup/resource-filebeat-scale-out-topology.yaml --user tidb -i /home/tidb/.ssh/tiup_rsa --wait-timeout 360 --yes
    ```

7. 使集群日志功能生效。

    待所有上述步骤完成后，大部分的升级已完成。由于在升级过程中，TiUniManager 对资源机器的 filebeat 进行了重装。为了使得查看 TiDB 集群日志功能在 TiUniManager 中生效，你需要手动在 TiUniManager 界面操作重启 TiDB 集群以刷新配置。为避免影响用户服务，请尽量在业务低峰期操作。

## 备份恢复 TiUniManager 元信息

为提高 TiUniManager 可用性，应对容灾场景，你可对 TiUniManager 元信息进行备份，并恢复元信息到新的 TiUniManager 中控机。

1. 备份 TiUniManager 元信息。

    {{< copyable "shell-regular" >}}

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    # 将当前 TiUniManager 系统 <cluster-name> 的元数据备份到中控机的 <target-path>
    TIUP_HOME=/home/tidb/.em tiup em backup <cluster-name> <target-path> -N <tiunimanager-ip>
    ```

2. 恢复 TiUniManager 元信息。

    {{< copyable "shell-regular" >}}

    ```shell
    # 切换到 tidb 账号下
    su - tidb

    db_path: "/home/tidb/em.db"
    ```

    从备份的元数据中恢复到新集群，流程和部署新集群相同。唯一的区别是在集群 yaml 配置中，`em_cluster_servers` 里增加了 `db_path: "/home/tidb/em.db"`，详细见 [TiUniManager 根据元数据恢复新集群拓扑配置模版 em.yaml（单机版）](https://github.com/pingcap/docs-cn/blob/master/config-templates/em-metadata-restore-config.yaml)。

## 修改默认的集群备份路径

TiUniManager 默认的集群备份路径相关配置参数如下：

| 配置描述 | 配置参数名 | 参考值 |
| --- | --- | --- |
| TiDB 集群备份的存储类型（仅支持 NFS 或 S3） | BackupStorageType | 's3' 或 'nfs' |
| TiDB 集群备份的存储路径（S3 bucket 路径，或 NFS share 的绝对路径） | BackupStoragePath | 'bucketPath/backup' (S3 路径示例）<br />'/mnt/nfspath'（NFS 路径示例）|
| TiDB 集群备份在 S3 共享存储时，S3 的 AccessKey | BackupS3AccessKey | '' |
| TiDB 集群备份在 S3 共享存储时，S3 的 SecretAccessKey | BackupS3SecretAccessKey | '' |
| TiDB 集群备份在 S3 共享存储时，S3 的 Endpoint（域名） | BackupS3Endpoint | '' |

当前不支持通过 TiUniManager 界面修改备份路径。如需修改备份路径，需要通过 OpenAPI 修改配置参数，以修改配置参数 "BackupS3AccessKey" 为例：

1. 登录获取 user token。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X 'POST' \ 'http://172.16.6.206:4180/api/v1/user/login' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "userName": "admin", "userPassword": "admin" }'
    ```

    > **注意：**
    >
    > 你需要将以上命令中 `172.16.6.206:4180` 替换为实际环境中 TiUniManager 中控机的 IP 地址和 WebServer 服务端口。

2. 查看配置参数值。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X GET "http://172.16.6.206:4100/api/v1/config/?configKey=BackupS3AccessKey" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

3. 修改配置参数值 `BackupS3AccessKey` 的值为 `newValue`。你可以将 `newValue` 替换为你期待的备份路径。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST "http://172.16.6.206:4100/api/v1/config/update" -d "{ \"configKey\": \"BackupS3AccessKey\", \"configValue\": \"newValue\"}" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

## 修改默认的数据导入导出路径

TiUniManager 默认的导入导出路径在 TiUniManager 中控机上，细节如下：

| 配置描述 | 配置参数名 | 参考值 |
| --- | --- | --- |
| TiUniManager 共享存储中导入文件存储位置（建议配置为 NFS 共享存储） | ImportShareStoragePath | `/home/tidb/import`（备注：中控机 `tidb` 账号拥有该路径的读写权限）|
| TiUniManager 共享存储中导出文件存储的位置（建议配置为 NFS 共享存储） | ExportShareStoragePath | `/home/tidb/export`（备注：中控机 `tidb` 账号拥有该路径的读写权限）|

当前 TiUniManager 不支持通过 TiUniManager 界面修改导入导出的路径。如需修导入导出路径，需要通过 OpenAPI 对配置进行修改，以修改 “ImportShareStoragePath” 为例：

1. 登录获取 user token。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X 'POST' \ 'http://172.16.6.206:4180/api/v1/user/login' \ -H 'accept: application/json' \ -H 'Content-Type: application/json' \ -d '{ "userName": "admin", "userPassword": "admin" }'
    ```

    > **注意：**
    >
    > 你需要将以上命令中 `172.16.6.206:4180` 替换为实际环境中 TiUniManager 中控机的 IP 地址和 WebServer 服务端口。

2. 查看配置参数值。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X GET "http://172.16.6.206:4100/api/v1/config/?configKey=ImportShareStoragePath" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

3. 修改配置参数 `ImportShareStoragePath` 的值为 `newValue`，你可以将 `newValue` 替换为你期待的导入导出路径。

    {{< copyable "shell-regular" >}}

    ```shell
    curl -X POST "http://172.16.6.206:4100/api/v1/config/update" -d "{ \"configKey\": \"ImportShareStoragePath\", \"configValue\": \"newValue\"}" -H "Authorization: Bearer 6ea768e4-c0ec-4d48-b401-0f114ddc994c"
    ```

## 删除 TiUniManager

如要删除 TiUniManager 服务，请执行以下命令：

```shell
su - tidb

# 查看现有 TiUniManager 服务
TIUP_HOME=/home/tidb/.em tiup em list

# 删除指定的 TiUniManager 服务
TIUP_HOME=/home/tidb/.em tiup em destroy <cluster-name>
```

## 指定外部的 Elasticsearch 服务

Elasticsearch 是一个分布式、高扩展、高实时的搜索与数据分析引擎。它能很方便的使大量数据具有搜索、分析和探索的能力。目前 TiUniManager 主要依赖 Elasticsearch 来做日志数据的存储和检索。

TiUniManager 可以通过 `config.yaml` 文件中全局的 `external_elasticsearch_url` 参数来指定外部的 Elasticsearch 服务。默认值为空。

`external_elasticsearch_url` 参数值格式为 `<IP:Port>`，例如：`127.0.0.1:9200`。

在 `config.yaml` 文件中，`external_elasticsearch_url` 和 `elasticsearch_servers` 都是用来指定 Elasticsearch 部署信息的，不能同时指定。如果指定了 `external_elasticsearch_url` 的值，则需要注释掉 `elasticsearch_servers` 组件的配置信息注释。

配置格式参考 [TiUniManager 拓扑配置模版 config.yaml（单机版）](https://github.com/pingcap/docs-cn/blob/master/config-templates/em-topology-config.yaml)。

## 手动指定部署的 Elasticsearch 组件堆内存大小

部署 TiUniManager 的拓扑文件支持根据真实部署中控机资源大小指定 Elasticsearch 组件的堆内存大小。通过 `elasticsearch_servers` 下的 `heap_size` 参数进行指定。例如 `16g`。

`heap_size` 是选填参数，不手工指定会使用默认值。默认值为 `4g`。

配置格式参考 [TiUniManager 拓扑配置模版 config.yaml（单机版）](https://github.com/pingcap/docs-cn/blob/master/config-templates/em-topology-config.yaml)。

## 安装 Kibana 组件（可选）

Kibana 是一个针对 Elasticsearch 的开源分析及可视化平台，用来搜索、查看交互存储在 Elasticsearch 索引中的数据。使用 Kibana，可以通过各种图表进行高级数据分析及展示。

目前 TiUniManager 默认安装 Kibana， 集成 Kibana 主要是做日志的展示，在控制台页面系统管理下的系统日志进行查看。

如果不想安装 kibana 组件，则直接在 `config.yaml` 文件中将 `kibana_servers` 组件相关的配置注释掉即可。

## 安全加固

完成 TiUniManager 安装后，建议用户通过系统防火墙为 Elasticsearch 和 Kibana 添加网络访问控制，仅允许 TiUniManager 中控机与上述组件通信，参考命令如下所示：

```shell
# 允许来自 TiUniManager 中控机的连接
iptables -A INPUT -p tcp -s <tiunimanager addr> --dport <elasticsearch port> -j ACCEPT
# 拒绝其它 IP 的访问
iptables -A INPUT -p tcp --dport <elasticsearch port> -j DROP
```
