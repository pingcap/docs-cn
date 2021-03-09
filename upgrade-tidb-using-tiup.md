---
title: 使用 TiUP 升级 TiDB
aliases: ['/docs-cn/dev/upgrade-tidb-using-tiup/','/docs-cn/dev/how-to/upgrade/using-tiup/','/zh/tidb/dev/upgrade-tidb-using-ansible/','/docs-cn/dev/upgrade-tidb-using-ansible/','/docs-cn/dev/how-to/upgrade/from-previous-version/','/docs-cn/dev/how-to/upgrade/to-tidb-3.0/','/docs-cn/dev/how-to/upgrade/rolling-updates-with-ansible/']
---

# 使用 TiUP 升级 TiDB

本文档适用于使用 TiUP 从 TiDB 4.0 版本升级至 TiDB 5.0 版本，以及从 5.0 版本升级至后续修订版本。

如果原集群是 3.0 或 3.1 以及更老的版本，需要先升级到 4.0 后再升级到 5.0, 不可跨主版本升级。

> **注意：**
>
> 从 TiDB v4.0 起，PingCAP 不再提供 TiDB Ansible 的支持。从 v5.0 起，不再提供 TiDB Ansible 的文档。如需阅读使用 TiDB Ansible 升级 TiDB 集群的文档，可参阅 [v4.0 版使用 TiDB Ansible 升级 TiDB](https://docs.pingcap.com/zh/tidb/v4.0/upgrade-tidb-using-ansible)。

## 1. 升级兼容性说明

- 不支持在升级后回退至 4.0 或更旧版本。
- 3.0 之前的版本，需要先通过 TiDB Ansible 升级到 3.0 版本，然后按照 [4.0 版本文档的说明](https://docs.pingcap.com/zh/tidb/v4.0/upgrade-tidb-using-tiup)，使用 TiUP 将 TiDB Ansible 配置导入，并升级到 4.0 版本，再按本文档说明升级到 5.0 版本。
- 支持 TiDB Binlog，TiCDC，TiFlash 等组件版本的升级。

> **注意：**
>
> 在升级的过程中不要执行 DDL 请求，否则可能会出现行为未定义的问题。

## 2. 升级前准备

本部分介绍实际开始升级前需要进行的准备工作，如安装或更新 TiUP 版本等。

### 2.1 在中控机器上安装 TiUP 和 TiUP Cluster

1. 在中控机上执行如下命令安装 TiUP：

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
> **注意：**
>
> 如果 `tiup --version` 显示 `tiup` 版本低于 `v1.4.0`，请在执行 `tiup update cluster` 之前先执行 `tiup update --self` 命令更新 `tiup` 版本。

4. 安装 TiUP 的 cluster 工具：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup install cluster
    ```

如果之前安装过 TiUP 及 TiUP Cluster 组件，使用如下命令更新至最新版本即可：

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

### 2.2 编辑 TiUP Cluster 拓扑配置文件

> **注意：**
>
> 以下情况可跳过该步骤：
>
> - 原集群没有修改过配置参数，或通过 tiup cluster 修改过参数但不需要调整。
> - 升级后对未修改过的配置项希望使用 `5.0` 默认参数。

1. 进入拓扑文件的 `vi` 编辑模式：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

2. 参考 [topology](https://github.com/pingcap/tiup/blob/release-1.4/embed/templates/examples/topology.example.yaml) 配置模板的格式，将希望修改的参数填到拓扑文件的 `server_configs` 下面。

修改完成后 `:wq` 保存并退出编辑模式，输入 `Y` 确认变更。

> **注意：**
>
> 升级到 5.0 版本前，请确认已在 4.0 修改的参数在 5.0 版本中是兼容的，可参考[配置模板](/tikv-configuration-file.md)。


### 2.3 更新 TiUP 离线镜像

> **注意：**
>
> 如果原集群不是通过[离线部署](/production-offline-deployment-using-tiup.md)方式部署的，可忽略此步骤。

如果用户希望升级更新本地的 TiUP 离线镜像，可以参考[使用 TiUP 离线部署 TiDB 集群](/production-offline-deployment-using-tiup.md)的步骤 1 与步骤 2 下载部署新版本的 TiUP 离线镜像。在执行 `local_install.sh` 后，TiUP 会完成覆盖升级。

覆盖升级完成后使用 `tiup update cluster` 升级 Cluster 组件。

此时离线镜像已经更新成功。如果覆盖后发现 TiUP 运行报错，可能是 manifest 未更新导致，可尝试 `rm -rf ~/.tiup/manifests` 后再使用。

## 3. 滚动升级 TiDB 集群

本部分介绍如何滚动升级 TiDB 集群以及升级后的验证。

### 3.1 将集群升级到指定版本

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> <version>
```

以升级到 v5.0.0 版本为例：

{{< copyable "shell-regular" >}}

```
tiup cluster upgrade <cluster-name> v5.0.0
```

滚动升级会逐个升级所有的组件。升级 TiKV 期间，会逐个将 TiKV 上的所有 leader 切走再停止该 TiKV 实例。默认超时时间为 5 分钟，超过后会直接停止实例。

如果不希望驱逐 leader，而希望立刻升级，可以在上述命令中指定 `--force`，该方式会造成性能抖动，不会造成数据损失。

如果希望保持性能稳定，则需要保证 TiKV 上的所有 leader 驱逐完成后再停止该 TiKV 实例，可以指定 `--transfer-timeout` 为一个超大值，如 `--transfer-timeout 100000000`，单位为秒。

### 3.2 升级后验证

执行 `display` 命令来查看最新的集群版本 `TiDB Version`：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

```
Cluster type:       tidb
Cluster name:       <cluster-name>
Cluster version:    v5.0.0
...
```

> **注意：**
>
> TiUP 及 TiDB（v4.0.2 起）默认会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品。若要了解所收集的信息详情及如何禁用该行为，请参见[遥测](/telemetry.md)。

## 4. 升级 FAQ

本部分介绍使用 TiUP 升级 TiDB 集群遇到的常见问题。

### 4.1 升级时报错中断，处理完报错后，如何继续升级

重新执行 `tiup cluster upgrade` 命令进行升级，升级操作会重启之前已经升级完成的节点。如果不希望重启已经升级过的节点，可以使用 `replay` 子命令来重试操作，具体方法如下：

1. 使用 `tiup cluster audit` 命令查看操作记录：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster audit
    ```

    在其中找到失败的升级操作记录，并记下该操作记录的 ID，下一步中将使用 `<audit-id>` 表示操作记录 ID 的值。

2. 使用 `tiup cluster replay <audit-id>` 命令重试对应操作：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster replay <audit-id>
    ```

### 4.2 升级过程中 evict leader 等待时间过长，如何跳过该步骤快速升级

可以指定 `--force`，升级时会跳过 `PD transfer leader` 和 `TiKV evict leader` 过程，直接重启并升级版本，对线上运行的集群影响较大。命令如下：

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v5.0.0 --force
```

### 4.3 升级完成后，如何更新 pd-ctl 等周边工具版本

可通过 TiUP 安装对应版本的 `ctl` 组件来调用相关工具：

{{< copyable "" >}}

```
tiup install ctl:v5.0.0
```

## 5. TiDB 5.0 兼容性变化

TBD
