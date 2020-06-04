---
title: 使用 TiUP 部署 TiDB 集群
category: how-to
aliases: ['/docs-cn/dev/how-to/deploy/orchestrated/tiup/']
---

# 使用 TiUP 部署 TiDB 集群

[TiUP](https://github.com/pingcap/tiup) 是 TiDB 4.0 版本引入的集群运维工具，[TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster) 是 TiUP 提供的使用 Golang 编写的集群管理组件，通过 TiUP cluster 组件就可以进行日常的运维工作，包括部署、启动、关闭、销毁、弹性扩缩容、升级 TiDB 集群；管理 TiDB 集群参数。

目前 TiUP 可以支持部署 TiDB、TiFlash、TiDB Binlog、TiCDC，以及监控系统。本文将介绍不同集群拓扑的具体部署步骤。

## 第 1 步：软硬件环境需求及前置检查

[软硬件环境需求](/hardware-and-software-requirements.md)

[环境与系统配置检查](/check-before-deployment.md)

## 第 2 步：在中控机上安装 TiUP 组件

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

## 第 3 步：编辑初始化配置文件

请根据不同的集群拓扑，编辑 TiUP 所需的集群初始化配置文件。

这里举出常见的 6 种场景，请根据链接中的拓扑说明，以及给出的配置文件模板，新建一个配置文件 `topology.yaml`。如果有其他组合场景的需求，请根据多个模板自行调整。

- [最小拓扑架构](/minimal-deployment-topology.md)

    最基本的集群拓扑，包括 tidb-server、tikv-server、pd-server，适合 OLTP 业务。

- [增加 TiFlash 拓扑架构](/tiflash-deployment-topology.md)

    包含最小拓扑的基础上，同时部署 TiFlash。TiFlash 是列式的存储引擎，已经逐步成为集群拓扑的标配。适合 Real-Time HTAP 业务。

- [增加 TiCDC 拓扑架构](/ticdc-deployment-topology.md)

    包含最小拓扑的基础上，同时部署 TiCDC。TiCDC 是 4.0 版本开始支持的 TiDB 增量数据同步工具，支持多种下游 (TiDB/MySQL/MQ)。相比于 TiDB Binlog，TiCDC 有延迟更低、天然高可用等优点。在部署完成后，需要启动 TiCDC，[通过 `cdc cli` 创建同步任务](/ticdc/manage-ticdc.md)。

- [增加 TiDB Binlog 拓扑架构](/tidb-binlog-deployment-topology.md)

    包含最小拓扑的基础上，同时部署 TiDB Binlog。TiDB Binlog 是目前广泛使用的增量同步组件，可提供准实时备份和同步功能。

- [混合部署拓扑架构](/hybrid-deployment-topology.md)

    适用于单台机器，混合部署多个实例的情况，也包括单机多实例，需要额外增加目录、端口、资源配比、label 等配置。

- [跨机房部署拓扑架构](/geo-distributed-deployment-topology.md)

    以典型的 `两地三中心` 架构为例，介绍跨机房部署架构，以及需要注意的关键设置。

### 第 4 步：执行部署命令

> **注意：**
>
> 通过 TiUP 进行集群部署可以使用密钥或者交互密码方式来进行安全认证：
>
> - 如果是密钥方式，可以通过 `-i` 或者 `--identity_file` 来指定密钥的路径；
> - 如果是密码方式，无需添加其他参数，`Enter` 即可进入密码交互窗口。

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy tidb-test v4.0.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

以上部署命令中：

- 通过 TiUP cluster 部署的集群名称为 `tidb-test`
- 部署版本为 `v4.0.0`，最新版本可以通过执行 `tiup list tidb` 来查看 TiUP 支持的版本
- 初始化配置文件为 `topology.yaml`
- --user root：通过 root 用户登录到目标主机完成集群部署，该用户需要有 ssh 到目标机器的权限，并且在目标机器有 sudo 权限。也可以用其他有 ssh 和 sudo 权限的用户完成部署。
- [-i] 及 [-p]：非必选项，如果已经配置免密登陆目标机，则不需填写。否则选择其一即可，[-i] 为可登录到部署机的 root 用户（或 --user 指定的其他用户）的私钥，也可使用 [-p] 交互式输入该用户的密码

预期日志结尾输出会有 ```Deployed cluster `tidb-test` successfully``` 关键词，表示部署成功。

### 第 5 步：查看 TiUP 管理的集群情况

{{< copyable "shell-regular" >}}

```shell
tiup cluster list
```

TiUP 支持管理多个 TiDB 集群，该命令会输出当前通过 TiUP cluster 管理的所有集群信息，包括集群名称、部署用户、版本、密钥信息等：

```log
Starting /home/tidb/.tiup/components/cluster/v1.0.0/cluster list
Name              User  Version        Path                                                        PrivateKey
----              ----  -------        ----                                                        ----------
tidb-test         tidb  v4.0.0      /home/tidb/.tiup/storage/cluster/clusters/tidb-test         /home/tidb/.tiup/storage/cluster/clusters/tidb-test/ssh/id_rsa
```

### 第 6 步：检查部署的 TiDB 集群情况

例如，执行如下命令检查 `tidb-test` 集群情况：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

预期输出包括 `tidb-test` 集群中实例 ID、角色、主机、监听端口和状态（由于还未启动，所以状态为 Down/inactive）、目录信息。

### 第 7 步：启动集群

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test
```

预期结果输出 ```Started cluster `tidb-test` successfully``` 标志启动成功。

### 第 8 步：验证集群运行状态

- 通过 TiUP 检查集群状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

预期结果输出，注意 Status 状态信息为 `Up` 说明集群状态正常

- 执行如下命令登录数据库：

{{< copyable "shell-regular" >}}

```shell
mysql -u root -h 10.0.1.4 -P 4000
```

此外，也需要验证监控系统、TiDB Dashboard 的运行状态，以及简单命令的执行，验证方式可参考[验证集群运行状态](/post-installation-check.md)。
