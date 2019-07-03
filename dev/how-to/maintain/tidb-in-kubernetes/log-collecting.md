---
title: 日志收集
category: how-to
---

# 日志收集

系统与程序的运行日志对排查问题以及实现一些自动化操作可能非常有用。本文将简要说明收集 TiDB 及相关组件日志的方法。

## TiDB 与 Kubernetes 组件运行日志

通过 TiDB Operator 部署的 TiDB 各组件默认将日志输出在容器的 `stdout` 和 `stderr` 中，对于 Kubernetes 而言，这些日志会被存放在宿主机的 `/var/log/containers` 目录下，并且文件名中包含了 Pod 和容器名称等信息。故而对容器中应用的日志收集可以直接在宿主机上完成。

如果在你的现有基础设施中已经有用于收集日志的系统，只需要通过常规方法将 Kubernetes 所在的宿主机上的 `/var/log/containers/*.log` 文件加入采集范围即可；如果没有可用的日志收集系统，或者希望部署一套独立的系统用于收集相关日志，也可以使用你熟悉的任意日志收集系统或方案。

Kubernetes 官方文档中提供了 [ElasticSearch](https://kubernetes.io/docs/tasks/debug-application-cluster/logging-elasticsearch-kibana/) 和 [Stackdriver](https://kubernetes.io/docs/tasks/debug-application-cluster/logging-stackdriver/) 两种日志收集方案可供参考。

常见的可用于收集 Kubernetes 日志的开源工具有：
 - [Fluentd](https://www.fluentd.org/)
 - [Fluent-bit](https://fluentbit.io/)
 - [Filebeat](https://www.elastic.co/products/beats/filebeat)
 - [Logstash](https://www.elastic.co/products/logstash)
 - ...

收集到的日志通常可以汇总存储在某一特定的服务器上，或存放到 ElasticSearch 等专用的存储、分析系统当中。

一些云服务商或专门的性能监控服务提供商也有各自的免费或收费的日志收集方案可以选择。

如果不通过单独的日志收集工具汇总日志，你也可以直接使用 `kubectl` 工具查看某个容器的运行日志，这一方法无法查看已销毁容器的日志：

{{< copyable "shell-regular" >}}

```shell
kubectl logs -n ${namespace} ${tidbPodName}
```

若需查看容器重启之前的日志，可以在执行上述命令时添加 `-p` 参数。

如果需要从多个 Pod 获取日志，可以使用 [`stern`](https://github.com/wercker/stern).

{{< copyable "shell-regular" >}}

```shell
stern -n ${namespace} tidb -c slowlog
```

## TiDB 慢查询日志

对于 3.0 之前的版本，在默认情况下，TiDB 会打印慢查询日志到标准输出，和应用日志混在一起。你可以通过关键字 `SLOW_QUERY` 来筛选慢查询日志，例如：

{{< copyable "shell-regular" >}}

```shell
kubectl logs -n ${namespace} ${tidbPodName} | grep SLOW_QUERY
```

在一些情况下，你可能希望使用一些工具或自动化系统对日志内容进行分析、处理。TiDB 各组件的应用日志使用了[统一的日志格式](https://github.com/tikv/rfcs/blob/master/text/2018-12-19-unified-log-format.md)以便于程序解析，但由于慢查询日志使用的是与 MySQL 兼容的多行格式，与应用日志混在一起时可能会对解析造成困难。

在 `values.yaml` 文件中配置 `separateSlowLog` 参数可以将慢查询日志输出到一个专用的旁路容器中，这样慢查询日志在宿主机上会被输出到一个单独的文件，和应用日志分开。

修改方法为编辑 `values.yaml` 文件，将 `separateSlowLog` 参数设置为 `true`:

```yaml
# Uncomment the following line to enable separate output of the slow query log
    separateSlowLog: true
```

之后再运行 `helm upgrade` 使配置生效，然后可以通过名为 `slowlog` 的 sidecar 容器查看慢查询日志：

{{< copyable "shell-regular" >}}

```shell
kubectl logs -n ${namespace} ${tidbPodName} -c slowlog
```

对于 3.0 及更新的版本，TiDB 将慢查询日志输出到独立的 `slowlog.log` 文件中，并且 `separateSlowLog` 是默认开启的，所以可以直接通过 sidecar 容器查看慢查询日志，无需额外设置。

> **注意：**
>
> 慢查询日志的格式与 MySQL 的慢查询日志相同，但由于 TiDB 自身的特点，其中的一些具体字段可能存在差异，故而解析 MySQL 慢查询日志的工具不一定能完全兼容 TiDB 的慢查询日志。

## 系统日志

系统日志可以通过常规方法在 Kubernetes 宿主机上收集，如果在你的现有基础设施中已经有用于收集日志的系统，只需要通过常规方法将相关服务器和日志文件添加到收集范围即可；如果没有可用的日志收集系统，或者希望部署一套独立的系统用于收集相关日志，也可以使用你熟悉的任意日志收集系统或方案。

上文提到的几种常见日志收集工具均支持对系统日志的收集，一些云服务商或专门的性能监控服务提供商也有各自的免费或收费的日志收集方案可以选择。

