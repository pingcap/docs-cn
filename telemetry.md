---
title: 遥测
summary: 介绍遥测的场景，如何禁用功能和查看遥测状态。
aliases: ['/docs-cn/dev/telemetry/']
---

# 遥测

开启遥测后，TiDB、TiUP 及 TiDB Dashboard 会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品，例如，通过这些使用信息，PingCAP 可以了解常见的 TiDB 集群操作，从而确定新功能优先级。

> **注意：**
>
> - 自 2023 年 2 月 20 日起，新发布的 TiDB 和 TiDB Dashboard 版本（含 v6.6.0），默认关闭遥测功能，即默认不再收集使用情况信息分享给 PingCAP。如果集群在升级至这些版本前使用默认的遥测配置，则升级后遥测功能处于关闭状态。具体的版本可参考 [TiDB 版本发布时间线](/releases/release-timeline.md)。
> - 从 v1.11.3 起，新部署的 TiUP 默认关闭遥测功能，即默认不再收集使用情况信息。如果从 v1.11.3 之前的 TiUP 版本升级至 v1.11.3 或更高 TiUP 版本，遥测保持升级前的开启或关闭状态。

## 哪些使用情况信息会被收集？

以下章节具体描述了各个组件收集并分享的使用情况信息。若收集的使用情况信息有变化，将在版本更新说明中告知。

> **注意：**
>
> 在**任何情况**下，集群中用户存储的数据都**不会**被收集。另请参阅 [PingCAP 隐私声明](https://pingcap.com/zh/privacy-policy/)。

### TiDB

当 TiDB 遥测功能开启时，TiDB 集群将会以 6 小时为周期收集使用情况信息并分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- 集群的部署情况，包括各个组件所在的硬件信息（CPU、内存、磁盘）、组件版本号、操作系统版本号等
- 系统的查询请求状态，例如查询请求次数、持续时长等
- 系统组件的使用情况，例如 Async Commit 功能是否有被使用
- 去识别化处理后的产品遥测数据发送端的 IP 地址

可以通过执行以下 SQL 语句查看 TiDB 收集的使用情况信息内容：

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY;
```

### TiDB Dashboard

当 TiDB Dashboard 遥测功能开启时，用户在 TiDB Dashboard 网页界面上进行操作时会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- 界面访问情况，如访问的 TiDB Dashboard 功能页面名称
- 用户浏览器及操作系统信息，如浏览器名称和版本号、操作系统名称、屏幕分辨率等

可以使用 [Chrome 开发者工具](https://developers.google.com/web/tools/chrome-devtools)的[网络功能](https://developers.google.com/web/tools/chrome-devtools/network)或 [Firefox 开发者工具](https://developer.mozilla.org/zh-CN/docs/Tools)的[网络监视器功能](https://developer.mozilla.org/zh-CN/docs/Tools/Network_Monitor)查看 TiDB Dashboard 发送的使用情况信息内容。

### TiUP

当 TiUP 遥测功能开启时，执行 TiUP 命令时会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- TiUP 命令的执行情况，如命令执行是否成功、命令执行耗时等
- 使用 TiUP 进行部署的情况，如部署的目标机器硬件信息、组件版本号、修改过的部署配置名称等

使用 TiUP 时，可通过设置 `TIUP_CLUSTER_DEBUG=enable` 环境变量输出执行命令时收集的使用情况信息，例如：

{{< copyable "shell-regular" >}}

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

### TiSpark

> **注意：**
>
> 从 TiSpark v3.0.3 开始，默认关闭遥测功能，即 TiSpark 默认不收集使用情况信息，不将这些信息分享给 PingCAP 用于改善产品。

当 TiSpark 遥测功能开启时，Spark 在使用 TiSpark 时会发送会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- TiSpark 的部分配置信息，如读取引擎、是否开启流式读取等
- 用户集群部署情况，包括 TiSpark 所在节点的机器硬件信息、操作系统信息和组件版本号等

使用 TiSpark 时，可以通过查看 Spark 日志来了解 TiSpark 收集的使用情况，可将 Spark 日志级别调至 INFO 或更低，例如：

{{< copyable "shell-regular" >}}

```shell
grep "Telemetry report" {spark.log} | tail -n 1
```

## 开启遥测功能

### 开启 TiDB 遥测

#### 第 1 步：修改配置文件中的遥测配置

在已有 TiDB 集群上开启遥测功能，需要为集群设置 [`enable-telemetry = true`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入)，但需要重启集群后才能生效。

以下是在各个部署工具中修改遥测配置的具体步骤。

<details>
  <summary>通过二进制手工部署</summary>

创建配置文件 `tidb_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
enable-telemetry = true
```

启动 TiDB 时指定命令行参数 `--config=tidb_config.toml` 使得该配置生效。

详情参见 [TiDB 配置参数](/command-line-flags-for-tidb-configuration.md#--config)、[TiDB 配置文件描述](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入)。

</details>

<details>
  <summary>通过 TiUP Playground 试用</summary>

创建配置文件 `tidb_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
enable-telemetry = true
```

启动 TiUP Playground 时，指定命令行参数 `--db.config tidb_config.toml` 使得该配置生效，如：

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.config tidb_config.toml
```

详情参见 [TiUP - 本地快速部署 TiDB 集群](/tiup/tiup-playground.md)。

</details>

<details>
  <summary>通过 TiUP Cluster 部署</summary>

修改部署拓扑文件 `topology.yaml`，新增（或在现有项中添加）以下内容：

{{< copyable "" >}}

```yaml
server_configs:
  tidb:
    enable-telemetry: true
```

</details>

<details>
  <summary>通过 TiDB Operator 在 Kubernetes 上部署</summary>

在 `tidb-cluster.yaml` 中或者 TidbCluster Custom Resource 中配置 `spec.tidb.config.enable-telemetry: true`。

详情参见[在标准 Kubernetes 上部署 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-general-kubernetes)。

> **注意：**
>
> 该配置需使用 TiDB Operator v1.1.3 或更高版本才能生效。

</details>

#### 第 2 步：修改系统全局变量的遥测配置

在步骤 1 完成后，还需要修改系统全局变量 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入)，才能打开 TiDB 遥测功能：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_telemetry = 1;
```

配置文件和全局变量都开启后，遥测功能才能处于开启状态。

### 开启 TiDB Dashboard 遥测

可以修改 PD 配置中 [`dashboard.enable-telemetry = true`](/pd-configuration-file.md#enable-telemetry) 启动 TiDB Dashboard 遥测功能。对于已启动的集群，该配置需要重启后才能生效。

以下列出在各个部署工具中修改遥测配置的具体步骤。

<details>
  <summary>通过二进制手工部署</summary>

创建配置文件 `pd_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = true
```

启动 PD 时指定命令行参数 `--config=pd_config.toml` 使得该配置生效。

详情参见 [PD 配置参数](/command-line-flags-for-pd-configuration.md#--config)、[PD 配置文件描述](/pd-configuration-file.md#enable-telemetry)。

</details>

<details>
  <summary>通过 TiUP Playground 试用</summary>

创建配置文件 `pd_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = true
```

启动 TiUP Playground 时，指定命令行参数 `--pd.config pd_config.toml` 使得该配置生效，如：

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config pd_config.toml
```

详情参见 [TiUP - 本地快速部署 TiDB 集群](/tiup/tiup-playground.md)。

</details>

<details>
  <summary>通过 TiUP Cluster 部署</summary>

修改部署拓扑文件 `topology.yaml`，新增（或在现有项中添加）以下内容：

{{< copyable "" >}}

```yaml
server_configs:
  pd:
    dashboard.enable-telemetry: true
```

</details>

<details>
  <summary>通过 TiDB Operator 在 Kubernetes 上部署</summary>

在 `tidb-cluster.yaml` 中或者 TidbCluster Custom Resource 中配置 `spec.pd.config.dashboard.enable-telemetry: true`。

详情参见[在标准 Kubernetes 上部署 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-general-kubernetes)。

> **注意：**
>
> 该配置需使用 TiDB Operator v1.1.3 或更高版本才能生效。

</details>

### 开启 TiUP 遥测

可通过执行以下命令开启 TiUP 遥测功能：

{{< copyable "shell-regular" >}}

```shell
tiup telemetry enable
```

### 开启 TiSpark 遥测

可以通过在 Spark 配置文件设置 `spark.tispark.telemetry.enable = true` 来开启 TiSpark 的遥测功能。

## 禁用遥测功能

### 部署 TiDB 时禁用 TiDB 遥测

在已有 TiDB 集群上开启遥测后，可以为每个集群设置 [`enable-telemetry = false`](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入) 以禁用 TiDB 遥测功能，但需要重启集群后才能生效。

以下是在各个部署工具中修改遥测配置的具体步骤。

<details>
  <summary>通过二进制手工部署</summary>

创建配置文件 `tidb_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
enable-telemetry = false
```

启动 TiDB 时指定命令行参数 `--config=tidb_config.toml` 使得该配置生效。

详情参见 [TiDB 配置参数](/command-line-flags-for-tidb-configuration.md#--config)、[TiDB 配置文件描述](/tidb-configuration-file.md#enable-telemetry-从-v402-版本开始引入)。

</details>

<details>
  <summary>通过 TiUP Playground 试用</summary>

创建配置文件 `tidb_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
enable-telemetry = false
```

启动 TiUP Playground 时，指定命令行参数 `--db.config tidb_config.toml` 使得该配置生效，如：

{{< copyable "shell-regular" >}}

```shell
tiup playground --db.config tidb_config.toml
```

详情参见 [TiUP - 本地快速部署 TiDB 集群](/tiup/tiup-playground.md)。

</details>

<details>
  <summary>通过 TiUP Cluster 部署</summary>

修改部署拓扑文件 `topology.yaml`，新增（或在现有项中添加）以下内容：

{{< copyable "" >}}

```yaml
server_configs:
  tidb:
    enable-telemetry: false
```

</details>

<details>
  <summary>通过 TiDB Operator 在 Kubernetes 上部署</summary>

在 `tidb-cluster.yaml` 中或者 TidbCluster Custom Resource 中配置 `spec.tidb.config.enable-telemetry: false`。

详情参见[在标准 Kubernetes 上部署 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-general-kubernetes)。

> **注意：**
>
> 该配置需使用 TiDB Operator v1.1.3 或更高版本才能生效。

</details>

### 动态禁用 TiDB 遥测

对于已部署的 TiDB 集群，还可以修改系统全局变量 [`tidb_enable_telemetry`](/system-variables.md#tidb_enable_telemetry-从-v402-版本开始引入) 动态禁用 TiDB 遥测功能：

{{< copyable "sql" >}}

```sql
SET GLOBAL tidb_enable_telemetry = 0;
```

配置文件的禁用优先级高于全局变量。若通过配置文件禁用了遥测功能，则全局变量的配置将不起作用，遥测功能总是处于关闭状态。

### 禁用 TiDB Dashboard 遥测

可以修改 PD 配置中 [`dashboard.enable-telemetry = false`](/pd-configuration-file.md#enable-telemetry) 禁用 TiDB Dashboard 遥测功能。对于已启动的集群，该配置需要重启后才能生效。

以下列出在各个部署工具中修改遥测配置的具体步骤。

<details>
  <summary>通过二进制手工部署</summary>

创建配置文件 `pd_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = false
```

启动 PD 时指定命令行参数 `--config=pd_config.toml` 使得该配置生效。

详情参见 [PD 配置参数](/command-line-flags-for-pd-configuration.md#--config)、[PD 配置文件描述](/pd-configuration-file.md#enable-telemetry)。

</details>

<details>
  <summary>通过 TiUP Playground 试用</summary>

创建配置文件 `pd_config.toml` 包含如下内容：

{{< copyable "" >}}

```toml
[dashboard]
enable-telemetry = false
```

启动 TiUP Playground 时，指定命令行参数 `--pd.config pd_config.toml` 使得该配置生效，如：

{{< copyable "shell-regular" >}}

```shell
tiup playground --pd.config pd_config.toml
```

详情参见 [TiUP - 本地快速部署 TiDB 集群](/tiup/tiup-playground.md)。

</details>

<details>
  <summary>通过 TiUP Cluster 部署</summary>

修改部署拓扑文件 `topology.yaml`，新增（或在现有项中添加）以下内容：

{{< copyable "" >}}

```yaml
server_configs:
  pd:
    dashboard.enable-telemetry: false
```

</details>

<details>
  <summary>通过 TiDB Operator 在 Kubernetes 上部署</summary>

在 `tidb-cluster.yaml` 中或者 TidbCluster Custom Resource 中配置 `spec.pd.config.dashboard.enable-telemetry: false`。

详情参见[在标准 Kubernetes 上部署 TiDB 集群](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/deploy-on-general-kubernetes)。

> **注意：**
>
> 该配置需使用 TiDB Operator v1.1.3 或更高版本才能生效。

</details>

### 禁用 TiUP 遥测

可通过执行以下命令禁用 TiUP 遥测功能：

{{< copyable "shell-regular" >}}

```shell
tiup telemetry disable
```

### 禁用 TiSpark 遥测

可以通过在 Spark 配置文件设置 `spark.tispark.telemetry.enable = false` 来禁用 TiSpark 的遥测功能。

## 查看遥测启用状态

对于 TiDB 遥测，可通过执行以下 SQL 语句查看遥测状态：

{{< copyable "sql" >}}

```sql
ADMIN SHOW TELEMETRY;
```

若 `DATA_PREVIEW` 列为空，说明遥测没有开启，否则说明遥测已开启。还可以从 `LAST_STATUS` 列了解上次分享使用情况信息的时间、是否成功等。

对于 TiUP 遥测，可通过执行以下命令查看遥测状态：

{{< copyable "shell-regular" >}}

```shell
tiup telemetry status
```

## 使用情况信息合规性

为了满足不同国家或地区对于此类信息的合规性要求，使用情况信息会按照不同的操作者 IP 地址发送到位于不同国家的服务器，具体如下：

- 若为中国大陆 IP 地址，使用情况信息将会发送并存储于中国大陆境内的公有云服务器。
- 若为中国大陆以外 IP 地址，使用情况信息将会发送并存储于美国的公有云服务器。

可参阅 [PingCAP 隐私声明](https://pingcap.com/zh/privacy-policy/)了解详情。
