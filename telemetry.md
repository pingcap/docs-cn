---
title: 遥测
summary: 介绍遥测的场景，如何禁用功能和查看遥测状态。
aliases: ['/zh/tidb/v8.3/sql-statement-admin-show-telemetry']
---

# 遥测

开启遥测后，TiUP 和 TiSpark 会收集使用情况信息，并将这些信息分享给 PingCAP 用于改善产品。

> **注意：**
>
> - 从 TiUP v1.11.3 起，TiUP 遥测功能默认关闭，即 TiUP 默认不再收集使用情况信息。如果从 v1.11.3 之前的 TiUP 版本升级至 v1.11.3 或更高 TiUP 版本，遥测保持升级前的开启或关闭状态。
> - 从 TiSpark v3.0.3 开始，TiSpark 遥测功能默认关闭，即 TiSpark 默认不收集使用情况信息。
> - 从 TiDB v8.1.0 起，TiDB 和 TiDB Dashboard 移除了遥测功能。

## 开启遥测后哪些使用情况信息会被收集？

以下章节具体描述了 TiUP 和 TiSpark 收集并分享的使用情况信息。若收集的使用情况信息有变化，将在版本更新说明中告知。

> **注意：**
>
> 在**任何情况**下，集群中用户存储的数据都**不会**被收集。另请参阅 [PingCAP 隐私声明](https://pingcap.com/zh/privacy-policy/)。

### TiUP

当 TiUP 遥测功能开启时，执行 TiUP 命令时会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- TiUP 命令的执行情况，如命令执行是否成功、命令执行耗时等
- 使用 TiUP 进行部署的情况，如部署的目标机器硬件信息、组件版本号、修改过的部署配置名称等

使用 TiUP 时，可通过设置 `TIUP_CLUSTER_DEBUG=enable` 环境变量输出执行命令时收集的使用情况信息，例如：

```shell
TIUP_CLUSTER_DEBUG=enable tiup cluster list
```

### TiSpark

当 TiSpark 遥测功能开启时，Spark 在使用 TiSpark 时会发送会将使用情况信息分享给 PingCAP，包括（但不限于）：

- 随机生成的遥测标示符
- TiSpark 的部分配置信息，如读取引擎、是否开启流式读取等
- 用户集群部署情况，包括 TiSpark 所在节点的机器硬件信息、操作系统信息和组件版本号等

使用 TiSpark 时，可以通过查看 Spark 日志来了解 TiSpark 收集的使用情况，可将 Spark 日志级别调至 INFO 或更低，例如：

```shell
grep "Telemetry report" {spark.log} | tail -n 1
```

## 开启遥测功能

### 开启 TiUP 遥测

可通过执行以下命令开启 TiUP 遥测功能：

```shell
tiup telemetry enable
```

### 开启 TiSpark 遥测

可以通过在 Spark 配置文件设置 `spark.tispark.telemetry.enable = true` 来开启 TiSpark 的遥测功能。

## 禁用遥测功能

### 禁用 TiUP 遥测

可通过执行以下命令禁用 TiUP 遥测功能：

```shell
tiup telemetry disable
```

### 禁用 TiSpark 遥测

可以通过在 Spark 配置文件设置 `spark.tispark.telemetry.enable = false` 来禁用 TiSpark 的遥测功能。

## 查看遥测启用状态

对于 TiUP 遥测，可通过执行以下命令查看遥测状态：

```shell
tiup telemetry status
```

## 使用情况信息合规性

为了满足不同国家或地区对于此类信息的合规性要求，使用情况信息会按照不同的操作者 IP 地址发送到位于不同国家的服务器，具体如下：

- 若为中国大陆 IP 地址，使用情况信息将会发送并存储于中国大陆境内的公有云服务器。
- 若为中国大陆以外 IP 地址，使用情况信息将会发送并存储于美国的公有云服务器。

可参阅 [PingCAP 隐私声明](https://pingcap.com/zh/privacy-policy/)了解详情。
