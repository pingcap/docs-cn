---
title: 使用 TiUP 部署 TiDB 集群
aliases: ['/zh/tidb/v5.0/production-offline-deployment-using-tiup','/zh/tidb/v5.0/deploy-test-cluster-using-docker-compose','/zh/tidb/v5.0/test-deployment-using-docker','/zh/tidb/stable/deploy-test-cluster-using-docker-compose','/zh/tidb/stable/test-deployment-using-docker']
---

# 使用 TiUP 部署 TiDB 集群

[TiUP](https://github.com/pingcap/tiup) 是 TiDB 4.0 版本引入的集群运维工具，[TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster) 是 TiUP 提供的使用 Golang 编写的集群管理组件，通过 TiUP cluster 组件就可以进行日常的运维工作，包括部署、启动、关闭、销毁、弹性扩缩容、升级 TiDB 集群，以及管理 TiDB 集群参数。

目前 TiUP 可以支持部署 TiDB、TiFlash、TiDB Binlog、TiCDC，以及监控系统。本文将介绍不同集群拓扑的具体部署步骤。

## 第 1 步：软硬件环境需求及前置检查

[软硬件环境需求](/hardware-and-software-requirements.md)

[环境与系统配置检查](/check-before-deployment.md)

## 第 2 步：在中控机上安装 TiUP 组件

在中控机上安装 TiUP 组件有两种方式：在线部署和离线部署。

### 方式一：在线部署 TiUP 组件

使用普通用户登录中控机，以 `tidb` 用户为例，后续安装 TiUP 及集群管理操作均通过该用户完成：

1. 执行如下命令安装 TiUP 工具：

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 按如下步骤设置 TiUP 环境变量：

    重新声明全局环境变量：

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

    确认 TiUP 工具是否安装：

    {{< copyable "shell-regular" >}}

    ```shell
    which tiup
    ```

3. 安装 TiUP cluster 组件

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

4. 如果已经安装，则更新 TiUP cluster 组件至最新版本：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup update --self && tiup update cluster
    ```

    预期输出 `“Update successfully!”` 字样。

5. 验证当前 TiUP cluster 版本信息。执行如下命令查看 TiUP cluster 组件版本：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup --binary cluster
    ```

### 方式二：离线部署 TiUP 组件

离线部署 TiUP 组件的操作步骤如下。

#### 准备 TiUP 离线组件包

方式一：在[官方下载页面](https://pingcap.com/zh/product#SelectProduct)选择对应版本的 TiDB server 离线镜像包（包含 TiUP 离线组件包）。

方式二：使用 `tiup mirror clone` 命令手动打包离线组件包，步骤如下：

1. 在线环境中安装 TiUP 包管理器工具

    1. 执行如下命令安装 TiUP 工具：

        {{< copyable "shell-regular" >}}

        ```shell
        curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
        ```

    2. 重新声明全局环境变量：

        {{< copyable "shell-regular" >}}

        ```shell
        source .bash_profile
        ```

    3. 确认 TiUP 工具是否安装：

        {{< copyable "shell-regular" >}}

        ```shell
        which tiup
        ```

2. 使用 TiUP 制作离线镜像

    1. 在一台和外网相通的机器上拉取需要的组件：

        {{< copyable "shell-regular" >}}

        ```bash
        tiup mirror clone tidb-community-server-${version}-linux-amd64 ${version} --os=linux --arch=amd64
        ```

        该命令会在当前目录下创建一个名叫 `tidb-community-server-${version}-linux-amd64` 的目录，里面包含 TiUP 管理的组件包。

    2. 通过 tar 命令将该组件包打包然后发送到隔离环境的中控机：

        {{< copyable "shell-regular" >}}

        ```bash
        tar czvf tidb-community-server-${version}-linux-amd64.tar.gz tidb-community-server-${version}-linux-amd64
        ```

        此时，`tidb-community-server-${version}-linux-amd64.tar.gz` 就是一个独立的离线环境包。

#### 部署离线环境 TiUP 组件

将离线包发送到目标集群的中控机后，执行以下命令安装 TiUP 组件：

{{< copyable "shell-regular" >}}

```bash
tar xzvf tidb-community-server-${version}-linux-amd64.tar.gz && \
sh tidb-community-server-${version}-linux-amd64/local_install.sh && \
source /home/tidb/.bash_profile
```

`local_install.sh` 脚本会自动执行 `tiup mirror set tidb-community-server-${version}-linux-amd64` 命令将当前镜像地址设置为 `tidb-community-server-${version}-linux-amd64`。

若需将镜像切换到其他目录，可以通过手动执行 `tiup mirror set <mirror-dir>` 进行切换。如果需要切换到在线环境，可执行 `tiup mirror set https://tiup-mirrors.pingcap.com`。

## 第 3 步：初始化集群拓扑文件

请根据不同的集群拓扑，编辑 TiUP 所需的集群初始化配置文件。

集群初始化配置文件可以通过 TiUP 工具在中控机上面创建 YAML 格式配置文件，例如 `topology.yaml`:

{{< copyable "shell-regular" >}}

```shell
tiup cluster template > topology.yaml
```

> **注意：**
>
> 混合部署场景也可以使用 `tiup cluster template --full > topology.yaml` 生成的建议拓扑模板，跨机房部署场景可以使用 `tiup cluster template --multi-dc > topology.yaml` 生成的建议拓扑模板。

执行 `vi topology.yaml`，查看配置文件的内容：

```shell
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"
server_configs: {}
pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6
tidb_servers:
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9
tikv_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3
monitoring_servers:
  - host: 10.0.1.4
grafana_servers:
  - host: 10.0.1.4
alertmanager_servers:
  - host: 10.0.1.4
```

这里举出常见的 6 种场景，请根据链接中的拓扑说明，以及给出的配置文件模板，修改配置文件 `topology.yaml`。如果有其他组合场景的需求，请根据标准模板自行调整。

- [最小拓扑架构](/minimal-deployment-topology.md)

    最基本的集群拓扑，包括 tidb-server、tikv-server、pd-server，适合 OLTP 业务。

- [增加 TiFlash 拓扑架构](/tiflash-deployment-topology.md)

    包含最小拓扑的基础上，同时部署 TiFlash。TiFlash 是列式的存储引擎，已经逐步成为集群拓扑的标配。适合 Real-Time HTAP 业务。

- [增加 TiCDC 拓扑架构](/ticdc-deployment-topology.md)

    包含最小拓扑的基础上，同时部署 TiCDC。TiCDC 是 4.0 版本开始支持的 TiDB 增量数据同步工具，支持多种下游 (TiDB/MySQL/MQ)。相比于 TiDB Binlog，TiCDC 有延迟更低、天然高可用等优点。在部署完成后，需要启动 TiCDC，[通过 `cdc cli` 创建同步任务](/ticdc/manage-ticdc.md)。

- [增加 TiDB Binlog 拓扑架构](/tidb-binlog-deployment-topology.md)

    包含最小拓扑的基础上，同时部署 TiDB Binlog。TiDB Binlog 是目前广泛使用的增量同步组件，可提供准实时备份和同步功能。

- [增加 TiSpark 拓扑架构](/tispark-deployment-topology.md)

    包含最小拓扑的基础上，同时部署 TiSpark 组件。TiSpark 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。TiUP cluster 组件对 TiSpark 的支持目前为实验性特性。

- [混合部署拓扑架构](/hybrid-deployment-topology.md)

    适用于单台机器，混合部署多个实例的情况，也包括单机多实例，需要额外增加目录、端口、资源配比、label 等配置。

- [跨机房部署拓扑架构](/geo-distributed-deployment-topology.md)

    以典型的 `两地三中心` 架构为例，介绍跨机房部署架构，以及需要注意的关键设置。

> **注意：**
>
> - 对于需要全局生效的参数，请在配置文件中 `server_configs` 的对应组件下配置。
>
> - 对于需要某个节点生效的参数，请在具体节点的 `config` 中配置。
>
> - 配置的层次结构使用 `.` 表示。如：`log.slow-threshold`。更多格式参考 [TiUP 配置参数模版](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)。
>
> - 更多参数说明，请参考 [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/release-5.0/config/config.toml.example)、[TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/release-5.0/etc/config-template.toml) 、 [PD `config.toml.example`](https://github.com/pingcap/pd/blob/release-5.0/conf/config.toml) 和 [TiFlash 配置参数](/tiflash/tiflash-configuration.md)。

## 第 4 步：执行部署命令

> **注意：**
>
> 通过 TiUP 进行集群部署可以使用密钥或者交互密码方式来进行安全认证：
>
> - 如果是密钥方式，可以通过 `-i` 或者 `--identity_file` 来指定密钥的路径；
> - 如果是密码方式，可以通过 `-p` 进入密码交互窗口；
> - 如果已经配置免密登录目标机，则不需填写认证。
>
> 一般情况下 TiUP 会在目标机器上创建 `topology.yaml` 中约定的用户和组，以下情况例外：
>
> - `topology.yaml` 中设置的用户名在目标机器上已存在。
> - 在命令行上使用了参数 `--skip-create-user` 明确指定跳过创建用户的步骤。

执行 deploy 命令前，先使用 `check` 及 `check --apply` 命令，检查和自动修复集群存在的潜在风险：

{{< copyable "shell-regular" >}}

```shell
tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

然后执行 `deploy` 命令部署 TiDB 集群：

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy tidb-test v5.0.4 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

以上部署命令中：

- 通过 TiUP cluster 部署的集群名称为 `tidb-test`
- 可以通过执行 `tiup list tidb` 来查看 TiUP 支持的最新可用版本，后续内容以版本 `v5.0.4` 为例
- 初始化配置文件为 `topology.yaml`
- --user root：通过 root 用户登录到目标主机完成集群部署，该用户需要有 ssh 到目标机器的权限，并且在目标机器有 sudo 权限。也可以用其他有 ssh 和 sudo 权限的用户完成部署。
- [-i] 及 [-p]：非必选项，如果已经配置免密登录目标机，则不需填写。否则选择其一即可，[-i] 为可登录到目标机的 root 用户（或 --user 指定的其他用户）的私钥，也可使用 [-p] 交互式输入该用户的密码
- 如果需要指定在目标机创建的用户组名，可以参考[这个例子](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml#L7)。

预期日志结尾输出会有 ```Deployed cluster `tidb-test` successfully``` 关键词，表示部署成功。

## 第 5 步：查看 TiUP 管理的集群情况

{{< copyable "shell-regular" >}}

```shell
tiup cluster list
```

TiUP 支持管理多个 TiDB 集群，该命令会输出当前通过 TiUP cluster 管理的所有集群信息，包括集群名称、部署用户、版本、密钥信息等：

```log
Starting /home/tidb/.tiup/components/cluster/v1.3.0/cluster list
Name              User  Version        Path                                                        PrivateKey
----              ----  -------        ----                                                        ----------
tidb-test         tidb  v5.0.4      /home/tidb/.tiup/storage/cluster/clusters/tidb-test         /home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa
```

## 第 6 步：检查部署的 TiDB 集群情况

例如，执行如下命令检查 `tidb-test` 集群情况：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

预期输出包括 `tidb-test` 集群中实例 ID、角色、主机、监听端口和状态（由于还未启动，所以状态为 Down/inactive）、目录信息。

## 第 7 步：启动集群

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test
```

预期结果输出 ```Started cluster `tidb-test` successfully``` 标志启动成功。

## 第 8 步：验证集群运行状态

操作步骤见[验证集群运行状态](/post-installation-check.md)。

## 探索更多

如果你已同时部署了 [TiFlash](/tiflash/tiflash-overview.md)，接下来可参阅以下文档：

- [使用 TiFlash](/tiflash/use-tiflash.md)
- [TiFlash 集群运维](/tiflash/maintain-tiflash.md)
- [TiFlash 报警规则与处理方法](/tiflash/tiflash-alert-rules.md)
- [TiFlash 常见问题](/tiflash/troubleshoot-tiflash.md)

如果你已同时部署了 [TiCDC](/ticdc/ticdc-overview.md)，接下来可参阅以下文档：

- [TiCDC 任务管理](/ticdc/manage-ticdc.md)
- [TiCDC 常见问题](/ticdc/troubleshoot-ticdc.md)

> **注意：**
>
> TiDB、TiUP 及 TiDB Dashboard 默认会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品。若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)。
