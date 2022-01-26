---
title: 使用 TiUP 离线镜像部署 DM 集群（实验特性）
summary: 学习如何使用 TiUP DM 组件来离线部署 TiDB Data Migration 工具。
---

# 使用 TiUP 离线镜像部署 DM 集群（实验特性）

> **警告：**
>
> 本文描述特性仍为实验特性，不建议在生产环境下使用 TiUP 离线镜像部署 DM 集群。

本文介绍如何使用 TiUP 离线部署 DM 集群，具体的操作步骤如下。

## 第 1 步：准备 TiUP 离线组件包

- 在线环境中安装 TiUP 包管理器工具。

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

- 使用 TiUP 制作离线镜像。

    1. 在一台和外网相通的机器上拉取需要的组件：

        {{< copyable "shell-regular" >}}

        ```bash
        # 将 ${version} 修改成实际需要的版本
        tiup mirror clone tidb-dm-${version}-linux-amd64 --os=linux --arch=amd64 \
            --dm-master=${version} --dm-worker=${version} --dmctl=${version} \
            --alertmanager=v0.17.0 --grafana=v4.0.3 --prometheus=v4.0.3 \
            --tiup=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}') --dm=v$(tiup --version|grep 'tiup'|awk -F ' ' '{print $1}')
        ```

        该命令会在当前目录下创建一个名叫 `tidb-dm-${version}-linux-amd64` 的目录，里面包含 TiUP 管理的组件包。

    2. 通过 tar 命令将该组件包打包然后发送到隔离环境的中控机：

        {{< copyable "shell-regular" >}}

        ```bash
        tar czvf tidb-dm-${version}-linux-amd64.tar.gz tidb-dm-${version}-linux-amd64
        ```

        此时，`tidb-dm-${version}-linux-amd64.tar.gz` 就是一个独立的离线环境包。

## 第 2 步: 部署离线环境 TiUP 组件

将离线包发送到目标集群的中控机后，执行以下命令安装 TiUP 组件：

{{< copyable "shell-regular" >}}

```bash
# 将 ${version} 修改成实际需要的版本
tar xzvf tidb-dm-${version}-linux-amd64.tar.gz
sh tidb-dm-${version}-linux-amd64/local_install.sh
source /home/tidb/.bash_profile
```

`local_install.sh` 脚本会自动执行 `tiup mirror set tidb-dm-${version}-linux-amd64` 命令将当前镜像地址设置为 `tidb-dm-${version}-linux-amd64`。

若需将镜像切换到其他目录，可以通过手动执行 `tiup mirror set <mirror-dir>` 进行切换，切换后如果再想切换成官方镜像，可执行 `tiup mirror set https://tiup-mirrors.pingcap.com`。

## 第 3 步：编辑初始化配置文件

请根据不同的集群拓扑，编辑 TiUP 所需的集群初始化配置文件。

请根据[配置文件模板](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)，新建一个配置文件 `topology.yaml`。如果有其他组合场景的需求，请根据多个模板自行调整。

部署 3 个 DM-master、3 个 DM-worker 与 1 个监控组件的配置如下：

```yaml
---
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/home/tidb/dm/deploy"
  data_dir: "/home/tidb/dm/data"
  # arch: "amd64"

master_servers:
  - host: 172.19.0.101
  - host: 172.19.0.102
  - host: 172.19.0.103

worker_servers:
  - host: 172.19.0.101
  - host: 172.19.0.102
  - host: 172.19.0.103

monitoring_servers:
  - host: 172.19.0.101

grafana_servers:
  - host: 172.19.0.101

alertmanager_servers:
  - host: 172.19.0.101
```

> **注意：**
>
> - 如果不需要确保 DM 集群高可用，则可只部署 1 个 DM-master 节点，且部署的 DM-worker 节点数量不少于上游待迁移的 MySQL/MariaDB 实例数。
>
> - 如果需要确保 DM 集群高可用，则推荐部署 3 个 DM-master 节点，且部署的 DM-worker 节点数量大于上游待迁移的 MySQL/MariaDB 实例数（如 DM-worker 节点数量比上游实例数多 2 个）。
>
> - 对于需要全局生效的参数，请在配置文件中 `server_configs` 的对应组件下配置。
>
> - 对于需要某个节点生效的参数，请在具体节点的 `config` 中配置。
>
> - 配置的层次结构使用 `.` 表示。如：`log.slow-threshold`。更多格式说明，请参考 [TiUP 配置参数模版](https://github.com/pingcap/tiup/blob/master/embed/examples/dm/topology.example.yaml)。
>
> - 更多参数说明，请参考 [master `config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/master/dm-master.toml)、[worker `config.toml.example`](https://github.com/pingcap/dm/blob/master/dm/worker/dm-worker.toml)。
>
> - 需要确保以下组件间端口可正常连通：
>
>     - 各 DM-master 节点间的 `peer_port`（默认为 `8291`）可互相连通。
>
>     - 各 DM-master 节点可连通所有 DM-worker 节点的 `port`（默认为 `8262`）。
>
>     - 各 DM-worker 节点可连通所有 DM-master 节点的 `port`（默认为 `8261`）。
>
>     - TiUP 节点可连通所有 DM-master 节点的 `port`（默认为 `8261`）。
>
>     - TiUP 节点可连通所有 DM-worker 节点的 `port`（默认为 `8262`）。

## 第 4 步：执行部署命令

> **注意：**
>
> 通过 TiUP 进行集群部署可以使用密钥或者交互密码方式来进行安全认证：
>
> - 如果是密钥方式，可以通过 `-i` 或者 `--identity_file` 来指定密钥的路径；
> - 如果是密码方式，可以通过 `-p` 进入密码交互窗口；
> - 如果已经配置免密登录目标机，则不需填写认证。

{{< copyable "shell-regular" >}}

```shell
tiup dm deploy dm-test ${version} ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
```

以上部署命令中：

- 通过 TiUP DM 部署的集群名称为 `dm-test`。
- 部署版本为 `${version}`，可以通过执行 `tiup list dm-master` 来查看 TiUP 支持的最新版本。
- 初始化配置文件为 `topology.yaml`。
- `--user root`：通过 root 用户登录到目标主机完成集群部署，该用户需要有 ssh 到目标机器的权限，并且在目标机器有 sudo 权限。也可以用其他有 ssh 和 sudo 权限的用户完成部署。
- `-i` 及 `-p`：非必选项，如果已经配置免密登录目标机，则不需填写，否则选择其一即可。`-i` 为可登录到目标机的 root 用户（或 `--user` 指定的其他用户）的私钥，也可使用 `-p` 交互式输入该用户的密码。
- TiUP DM 使用内置的 SSH 客户端，如需使用系统自带的 SSH 客户端，请参考 TiUP DM 文档中[使用中控机系统自带的 SSH 客户端连接集群](/dm/maintain-dm-using-tiup.md#使用中控机系统自带的-ssh-客户端连接集群)章节进行设置。

预期日志结尾输出会有 ```Deployed cluster `dm-test` successfully``` 关键词，表示部署成功。

## 第 5 步：查看 TiUP 管理的集群情况 

{{< copyable "shell-regular" >}}

```shell
tiup dm list
```

TiUP 支持管理多个 DM 集群，该命令会输出当前通过 TiUP DM 管理的所有集群信息，包括集群名称、部署用户、版本、密钥信息等：

```log
Name  User  Version  Path                                  PrivateKey
----  ----  -------  ----                                  ----------
dm-test  tidb  ${version}  /root/.tiup/storage/dm/clusters/dm-test  /root/.tiup/storage/dm/clusters/dm-test/ssh/id_rsa
```

## 第 6 步：检查部署的 DM 集群情况

例如，执行如下命令检查 `dm-test` 集群情况：

{{< copyable "shell-regular" >}}

```shell
tiup dm display dm-test
```

预期输出包括 `dm-test` 集群中实例 ID、角色、主机、监听端口和状态（由于还未启动，所以状态为 Down/inactive）、目录信息。

## 第 7 步：启动集群

{{< copyable "shell-regular" >}}

```shell
tiup dm start dm-test
```

预期结果输出 ```Started cluster `dm-test` successfully``` 表示启动成功。

## 第 8 步：验证集群运行状态

通过以下 TiUP 命令检查集群状态：

{{< copyable "shell-regular" >}}

```shell
tiup dm display dm-test
```

在输出结果中，如果 Status 状态信息为 `Up`，说明集群状态正常。
