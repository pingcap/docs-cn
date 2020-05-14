---
title: 使用 TiUP 升级 TiDB
category: how-to
aliases: ['/docs-cn/dev/how-to/upgrade/using-tiup/']
---

# 使用 TiUP 升级 TiDB

本文档适用于使用 TiUP 从 TiDB 3.0 版本升级至 TiDB 4.0 版本，以及从 4.0 版本升级至后续版本。

如果原集群使用 TiDB Ansible 部署，TiUP 也支持将 TiDB Ansible 配置导入，并完成升级。

## 1. 升级兼容性说明

- 不支持在升级后回退至 3.0 版本。
- 3.0 之前的版本，需要先通过 TiDB Ansible 升级到 3.0 版本，然后按照本文档的说明，使用 TiUP 将 TiDB Ansible 配置导入，再升级到 4.0 版本。
- TiDB Ansible 配置导入到 TiUP 中管理后，不能再通过 TiDB Ansible 对集群进行操作，否则可能因元信息不一致造成冲突。
- 对于满足以下情况之一的 TiDB Ansible 部署的集群，暂不支持导入：
    - 启用了 `TLS` 加密功能的集群
    - 纯 KV 集群（没有 TiDB 实例的集群）
    - 启用了 `Kafka` 的集群
    - 启用了 `Spark` 的集群
    - 启用了 `Lightning` / `Importer` 的集群
    - 仍使用老版本 `'push'` 的方式收集监控指标（从 3.0 默认为 `'pull'` 模式，如果没有特意调整过则可以支持）
    - 在 `inventory.ini` 配置文件中单独为机器的 node_exporter / blackbox_exporter 通过 `node_exporter_port` / `blackbox_exporter_port` 设置了非默认端口（在 `group_vars` 目录中统一配置的可以兼容）

## 2. 在中控机器上安装 TiUP

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

4. 安装 TiUP 的 cluster 工具：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

如果之前安装过 TiUP，使用如下命令更新至最新版本即可：

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

## 3. 将 TiDB Ansible 及 `inventory.ini` 配置导入到 TiUP

> **注意：**
>
> + 如果原集群已经是 TiUP 部署，可以跳过此步骤。
> + 目前默认识别 `inventory.ini` 配置文件，如果你的配置为其他名称，请指定。
> + 你需要确保当前集群的状态与 `inventory.ini` 中的拓扑一致，并确保集群的组件运行正常，否则导入后会导致集群元信息异常。

### 3.1 将 TiDB Ansible 集群导入到 TiUP 中

1. 以 `/home/tidb/tidb-ansible` 为示例路径，使用如下命令将 TiDB Ansible 集群导入到 TiUP 中（不要在 Ansible 的目录下执行该命令，否则会报错）：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster import -d /home/tidb/tidb-ansible
    ```

2. 执行导入命令后，若集群 `Inventory` 信息解析成功，将出现如下提示：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster import -d /home/tidb/tidb-ansible/
    ```

    ```
    Found inventory file /home/tidb/tidb-ansible/inventory.ini, parsing...
    Found cluster "ansible-cluster" (v3.0.12), deployed with user tidb.
    Prepared to import TiDB v3.0.12 cluster ansible-cluster.
    Do you want to continue? [y/N]:
    ```

3. 核对解析得到的集群名和版本无误后，输入`y` 确认继续执行。

    + 若 `Inventory` 信息解析出错，导入过程将会终止，终止不会对原 Ansible 部署方式有任何影响，之后需根据错误提示调整并重试。

    + 若 Ansible 中原集群名与 TiUP 中任一已有集群的名称重复，将会给出警示信息并提示输入一个新的集群名。因此，请注意**不要重复对同一个集群执行导入**，导致 TiUP 中同一个集群有多个名字

导入完成后，可以通过 `tiup cluster display <cluster-name>` 查看当前集群状态以验证导入结果。由于 `display` 命令会查询各结点的实时状态，所以命令执行可能需要等待少许时间。

### 3.2 编辑 TiUP 拓扑配置文件

> **注意：**
>
> 以下情况可跳过该步骤：
>
> - 原集群没有修改过配置参数。
> - 升级后希望使用 `4.0` 默认参数。

1. 进入 TiDB Ansible 的备份目录 `~/.tiup/storage/cluster/clusters/{cluster_name}/config`，确认配置模板中修改过的参数。

2. 进入拓扑文件的 `vi` 编辑模式：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster edit-config <cluster-name>
    ```

3. 参考 [topology](https://github.com/pingcap-incubator/tiup-cluster/blob/master/examples/topology.example.yaml) 配置模板的格式，将原集群修改过的参数填到拓扑文件的 `server_configs` 下面。
如果集群有配置 label，目前也需要按模板中的格式在配置中补充，后续版本会自动导入 label。

修改完成后 `wq` 保存并退出编辑模式，输入 `Y` 确认变更。

> **注意：**
>
> 升级到 4.0 版本前，请确认 3.0 修改的参数在 4.0 版本中是兼容的，可参考[配置模板](/tikv-configuration-file.md)。

## 4. 滚动升级 TiDB 集群

本部分介绍如何滚动升级 TiDB 集群以及升级后的验证。

### 4.1 将集群升级到 v4.0.0-rc 版本

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0-rc
```

滚动升级会逐个升级所有的组件。升级 TiKV 期间，会逐个将 TiKV 上的所有 leader 切走再停止该 TiKV 实例。默认超时时间为 5 分钟，超过后会直接停止实例。

如果不希望驱逐 leader，而希望立刻升级，可以在上述命令中指定 `--force`，该方式会造成性能抖动，不会造成数据损失。

如果希望保持性能稳定，则需要保证 TiKV 上的所有 leader 驱逐完成后再停止该 TiKV 实例，可以指定 `--transfer-timeout` 为一个超大值，如 `--transfer-timeout 100000000`，单位为 s。

### 4.2 升级后验证

执行 `display` 命令来查看最新的集群版本 `TiDB Version`：

{{< copyable "shell-regular" >}}

```shell
tiup cluster display <cluster-name>
```

```
Starting /home/tidblk/.tiup/components/cluster/v0.4.3/cluster display <cluster-name>
TiDB Cluster: <cluster-name>
TiDB Version: v4.0.0-rc
```

## 5. 升级 FAQ

本部分介绍使用 TiUP 升级 TiDB 集群遇到的常见问题。

### 5.1 升级时报错中断，处理完报错后，如何从中断的节点继续升级

可以指定 `--role` 或 `--node` 对指定的组件或节点进行升级。命令如下：

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0-rc --role tidb
```

或者

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0-rc --node <ID>
```

### 5.2 升级过程中 evict leader 等待时间过长，如何跳过该步骤快速升级

可以指定 `--force`，升级时会跳过 `PD transfer leader` 和 `TiKV evict leader` 过程，直接重启并升级版本，对线上运行的集群影响较大。命令如下：

{{< copyable "shell-regular" >}}

```shell
tiup cluster upgrade <cluster-name> v4.0.0-rc --force
```

### 5.3 升级完成后，如何更新 pd-ctl 等周边工具版本

目前 TiUP 没有对周边工具的版本进行管理更新，如需下载最新版本的工具包，直接下载 TiDB 安装包即可，将 `{version}` 替换为对应的版本如 `v4.0.0-rc`，下载地址如下：

{{< copyable "" >}}

```
https://download.pingcap.org/tidb-{version}-linux-amd64.tar.gz
```

## 6. TiDB 4.0 兼容性变化

- `oom-action` 参数设置为 `cancel` 时，当查询语句触发 OOM 阈值后会被 kill 掉，升级到 4.0 版本后除了 `select` 语句，还可能 kill 掉 `insert`/`update`/`delete` 等 DML 语句。
- 4.0 版本增加了 `rename` 时对表名长度的检查，长度限制为 `64` 个字符。升级后 `rename` 后的表名长度超过这个限制会报错，3.0 及之前的版本则不会报错。
- 4.0 版本对 `explain` 执行计划的输出格式做了改进，需要注意是否有针对 `explain` 制订了自动化的分析程序。
