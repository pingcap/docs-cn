---
title: 使用 TiUP 部署 TiDB 集群
aliases: ['/docs-cn/dev/production-offline-deployment-using-tiup/', '/zh/tidb/dev/production-offline-deployment-using-tiup','/docs-cn/dev/production-deployment-using-tiup/','/docs-cn/dev/how-to/deploy/orchestrated/tiup/','/docs-cn/dev/tiflash/deploy-tiflash/','/docs-cn/dev/reference/tiflash/deploy/','/zh/tidb/dev/deploy-test-cluster-using-docker-compose','/zh/tidb/dev/test-deployment-using-docker']
---

# 使用 TiUP 部署 TiDB 集群

[TiUP](https://github.com/pingcap/tiup) 是 TiDB 4.0 版本引入的集群运维工具，[TiUP cluster](https://github.com/pingcap/tiup/tree/master/components/cluster) 是 TiUP 提供的使用 Golang 编写的集群管理组件，通过 TiUP cluster 组件就可以进行日常的运维工作，包括部署、启动、关闭、销毁、弹性扩缩容、升级 TiDB 集群，以及管理 TiDB 集群参数。

目前 TiUP 可以支持部署 TiDB、TiFlash、TiDB Binlog、TiCDC 以及监控系统。本文将介绍不同集群拓扑的具体部署步骤。

## 第 1 步：软硬件环境需求及前置检查

[软硬件环境需求](/hardware-and-software-requirements.md)

[环境与系统配置检查](/check-before-deployment.md)

## 第 2 步：在中控机上部署 TiUP 组件

在中控机上部署 TiUP 组件有两种方式：在线部署和离线部署。

<SimpleTab>
<div label="在线部署">

### 在线部署

以普通用户身份登录中控机。以 `tidb` 用户为例，后续安装 TiUP 及集群管理操作均通过该用户完成：

1. 执行如下命令安装 TiUP 工具：

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 按如下步骤设置 TiUP 环境变量：

    1. 重新声明全局环境变量：

        {{< copyable "shell-regular" >}}

        ```shell
        source .bash_profile
         ```

    2. 确认 TiUP 工具是否安装：

        {{< copyable "shell-regular" >}}

        ```shell
        which tiup
        ```

3. 安装 TiUP cluster 组件：

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

</div>

<div label="离线部署">

### 离线部署

离线部署 TiUP 组件的操作步骤如下。

#### 准备 TiUP 离线组件包

方式一：在[官方下载页面](https://pingcap.com/zh/product#SelectProduct)选择对应版本的 TiDB server 离线镜像包（包含 TiUP 离线组件包）。

方式二：使用 `tiup mirror clone` 命令手动打包离线组件包。步骤如下：

1. 在在线环境中安装 TiUP 包管理器工具

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

3. 自定义制作的离线镜像，或调整已有离线镜像中的内容

    如果从官网下载的离线镜像不满足你的具体需求，或者希望对已有的离线镜像内容进行调整，例如增加某个组件的新版本等，可以采取以下步骤进行操作：

    1. 在制作离线镜像时，可通过参数指定具体的组件和版本等信息，获得不完整的离线镜像。例如，要制作一个只包括 v1.7.0 版本 TiUP 和 TiUP Cluster 的离线镜像，可执行如下命令：

        {{< copyable "shell-regular" >}}

        ```bash
        tiup mirror clone tiup-custom-mirror-v1.7.0 --tiup v1.7.0 --cluster v1.7.0
        ```

        如果只需要某一特定平台的组件，也可以通过 `--os` 和 `--arch` 参数来指定。

    2. 参考上文“使用 TiUP 制作离线镜像”第 2 步的方式，将此不完整的离线镜像传输到隔离环境的中控机。

    3. 在隔离环境的中控机上，查看当前使用的离线镜像路径。较新版本的 TiUP 可以直接通过命令获取当前的镜像地址：

        {{< copyable "shell-regular" >}}

        ```bash
        tiup mirror show
        ```

        以上命令如果提示 `show` 命令不存在，可能当前使用的是较老版本的 TiUP。此时可以通过查看 `$HOME/.tiup/tiup.toml` 获得正在使用的镜像地址。将此镜像地址记录下来，后续步骤中将以变量 `${base_mirror}` 指代此镜像地址。

    4. 将不完整的离线镜像合并到已有的离线镜像中：

        首先将当前离线镜像中的 `keys` 目录复制到 `$HOME/.tiup` 目录中：

        {{< copyable "shell-regular" >}}

        ```bash
        cp -r ${base_mirror}/keys $HOME/.tiup/
        ```

        然后使用 TiUP 命令将不完整的离线镜像合并到当前使用的镜像中：

        {{< copyable "shell-regular" >}}

        ```bash
        tiup mirror merge tiup-custom-mirror-v1.7.0
        ```

    5. 上述步骤完成后，通过 `tiup list` 命令检查执行结果。在本文例子中，使用 `tiup list tiup` 和 `tiup list cluster` 均应能看到对应组件的 `v1.7.0` 版本出现在结果中。

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

</div>
</SimpleTab>

## 第 3 步：初始化集群拓扑文件

1. 创建集群拓扑文件。

    根据不同的集群拓扑，编辑 TiUP 所需的集群初始化配置文件。可以通过 TiUP 工具在中控机上面创建 YAML 格式集群配置文件，例如 `topology.yaml`:

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster template > topology.yaml
    ```

    > **注意：**
    >
    > 混合部署场景也可以使用 `tiup cluster template --full > topology.yaml` 生成的建议拓扑模板，跨机房部署场景可以使用 `tiup cluster template --multi-dc > topology.yaml` 生成的建议拓扑模板。

2. 配置集群拓扑文件。

   执行 `vi topology.yaml`，按实际场景配置以下参数：

    - Global 参数
        - user
        - ssh_port
        - deploy_dir
        - data_dir
    - Server 参数
        - PD servers
        - TiDB servers
        - TiKV servers
        - Monitoring servers
        - Grafana servers
        - ......

    下表列出了常用的 7 种场景，请根据链接中的拓扑说明以及配置文件模板配置`topology.yaml`。如果有其他组合场景的需求，请根据多个模板自行调整。

    | 场景 | 配置任务 | 配置文件模板 | 拓扑说明 |
    | :-- | :-- | :-- | :-- |
    | OLTP 业务 | [最小拓扑架构](/minimal-deployment-topology.md) | [简单最小配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-mini.yaml)<br/>[详细最小配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-mini.yaml) | 最基本的集群拓扑，包括 tidb-server、tikv-server、pd-server。 |
    | HTAP 业务 | [增加 TiFlash 拓扑架构](/tiflash-deployment-topology.md) | [简单 TiFlash 配置模版](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-tiflash.yaml)<br/>[详细 TiFlash 配置模版](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tiflash.yaml) | 在最小拓扑的基础上部署 TiFlash。TiFlash 是列式存储引擎，已经逐步成为集群拓扑的标配。|
    | 使用 [TiCDC](/ticdc/ticdc-overview.md) 进行增量同步 | [增加 TiCDC 拓扑架构](/ticdc-deployment-topology.md) | [简单 TiCDC 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-cdc.yaml)<br/>[详细 TiCDC 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-cdc.yaml) | 在最小拓扑的基础上部署 TiCDC。TiCDC 支持多种下游 (TiDB/MySQL/MQ)。 |
    | 使用 [TiDB Binlog](/tidb-binlog/tidb-binlog-overview.md) 进行增量同步 | [增加 TiDB Binlog 拓扑架构](/tidb-binlog-deployment-topology.md) | [简单 TiDB Binlog 配置模板（下游为 MySQL）](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-tidb-binlog.yaml)<br/>[简单 TiDB Binlog 配置模板（下游为 file）](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-file-binlog.yaml)<br/>[详细 TiDB Binlog 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tidb-binlog.yaml) | 在最小拓扑的基础上部署 TiDB Binlog。 |
    | 使用 Spark 的 OLAP 业务 | [增加 TiSpark 拓扑架构](/tispark-deployment-topology.md) | [简单 TiSpark 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-tispark.yaml)<br/>[详细 TiSpark 配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-tispark.yaml) | 在最小拓扑的基础上部署 TiSpark 组件。TiSpark 是 PingCAP 为解决用户复杂 OLAP 需求而推出的产品。TiUP cluster 组件对 TiSpark 的支持目前为实验特性。 |
    | 单台机器，多个实例 | [混合部署拓扑架构](/hybrid-deployment-topology.md) | [简单混部配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/simple-multi-instance.yaml)<br/>[详细混部配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/complex-multi-instance.yaml) | 也适用于单机多实例需要额外增加目录、端口、资源配比、label 等配置的场景。 |
    | 跨机房部署 TiDB 集群 | [跨机房部署拓扑架构](/geo-distributed-deployment-topology.md) | [跨机房配置模板](https://github.com/pingcap/docs-cn/blob/master/config-templates/geo-redundancy-deployment.yaml) | 以典型的两地三中心架构为例，介绍跨机房部署架构，以及需要注意的关键设置。 |

> **注意：**
>
> - 对于需要全局生效的参数，请在配置文件中 `server_configs` 的对应组件下配置。
>
> - 对于需要某个节点生效的参数，请在具体节点的 `config` 中配置。
>
> - 配置的层次结构使用 `.` 表示。如：`log.slow-threshold`。更多格式参考 [TiUP 配置参数模版](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml)。
>
> - 如果需要指定在目标机创建的用户组名，可以参考[这个例子](https://github.com/pingcap/tiup/blob/master/embed/examples/cluster/topology.example.yaml#L7)。
>

更多参数说明，请参考 [TiDB `config.toml.example`](https://github.com/pingcap/tidb/blob/master/config/config.toml.example)、[TiKV `config.toml.example`](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)、[PD `config.toml.example`](https://github.com/pingcap/pd/blob/master/conf/config.toml) 和 [TiFlash 配置参数](/tiflash/tiflash-configuration.md)。

## 第 4 步：执行部署命令

> **注意：**
>
> 通过 TiUP 进行集群部署可以使用密钥或者交互密码方式来进行安全认证：
>
> - 如果是密钥方式，可以通过 -i 或者 --identity_file 来指定密钥的路径。
>
> - 如果是密码方式，可以通过 -p 进入密码交互窗口。
>
> - 如果已经配置免密登录目标机，则不需填写认证。
>
> 一般情况下 TiUP 会在目标机器上创建 topology.yaml 中约定的用户和组，以下情况例外：
>
> - `topology.yaml` 中设置的用户名在目标机器上已存在。
>
> - 在命令行上使用了参数 --skip-create-user 明确指定跳过创建用户的步骤。

执行部署命令前，先使用 `check` 及 `check --apply` 命令检查和自动修复集群存在的潜在风险：

1. 检查集群存在的潜在风险：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster check ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

2. 自动修复集群存在的潜在风险：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster check ./topology.yaml --apply --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

3. 部署 TiDB 集群：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster deploy tidb-test v5.3.0 ./topology.yaml --user root [-p] [-i /home/root/.ssh/gcp_rsa]
    ```

以上部署示例中：

- `tidb-test` 为部署的集群名称。
- `v5.3.0` 为部署的集群版本，可以通过执行 `tiup list tidb` 来查看 TiUP 支持的最新可用版本。
- 初始化配置文件为 `topology.yaml`。
- `--user root` 表示通过 root 用户登录到目标主机完成集群部署，该用户需要有 ssh 到目标机器的权限，并且在目标机器有 sudo 权限。也可以用其他有 ssh 和 sudo 权限的用户完成部署。
- [-i] 及 [-p] 为可选项，如果已经配置免密登录目标机，则不需填写。否则选择其一即可，[-i] 为可登录到目标机的 root 用户（或 --user 指定的其他用户）的私钥，也可使用 [-p] 交互式输入该用户的密码。

预期日志结尾输出 ```Deployed cluster `tidb-test` successfully``` 关键词，表示部署成功。

## 第 5 步：查看 TiUP 管理的集群情况

{{< copyable "shell-regular" >}}

```shell
tiup cluster list
```

TiUP 支持管理多个 TiDB 集群，该命令会输出当前通过 TiUP cluster 管理的所有集群信息，包括集群名称、部署用户、版本、密钥信息等。

## 第 6 步：检查部署的 TiDB 集群情况

例如，执行如下命令检查 `tidb-test` 集群情况：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

预期输出包括 `tidb-test` 集群中实例 ID、角色、主机、监听端口和状态（由于还未启动，所以状态为 Down/inactive）、目录信息。

## 第 7 步：启动集群

> **注意：**
>
> 安全启动方式是为 TiUP cluster v1.9.0 及后续版本提供的新部署方式，推荐使用安全启动方式启动集群：
>
> - 安全启动后会自动生成 TiDB root 用户的密码，并在命令行界面返回密码。
>
> - 使用安全启动方式后，不能通过无密码的 root 用户登录数据库，你需要记录命令行返回的密码进行后续操作。
>
> - 该自动生成的密码只会返回一次，如果没有记录或者忘记该密码，请参照[忘记 root 密码](/user-account-management.md#忘记-root-密码)修改密码。

方式一：安全启动方式

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test --init
```

预期结果如下，表示启动成功。

{{< copyable "shell-regular" >}}

```shell
Started cluster `tidb-test` successfully.
The root password of TiDB database has been changed.
The new password is: 'y_+3Hwp=*AWz8971s6'.
Copy and record it to somewhere safe, it is only displayed once, and will not be stored.
The generated password can NOT be got again in future.
```

你需要记录命令行返回结果中的密码信息，用于后续数据库登录。使用安全启动方式后，不能通过无密码的 root 用户登录数据库。

方式二：普通启动方式

{{< copyable "shell-regular" >}}

```shell
tiup cluster start tidb-test
```

预期结果输出 ```Started cluster `tidb-test` successfully``` ，表示启动成功。使用普通启动方式后，可通过无密码的 root 用户登录数据库。

## 第 8 步：验证集群运行状态

{{< copyable "shell-regular" >}}

```shell
tiup cluster display tidb-test
```

预期结果输出：各节点 Status 状态信息为 `Up` 说明集群状态正常。

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
