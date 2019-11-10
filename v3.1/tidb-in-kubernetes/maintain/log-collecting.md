---
title: Collect TiDB Logs in Kubernetes
summary: Learn how to collect TiDB logs in Kubernetes.
category: how-to
---

# Collect TiDB Logs in Kubernetes

Runtime logs of the system and program can be very useful for troubleshooting problems and automating some operations. This document introduces the methods to collect logs of TiDB and its related components.

## Collect logs of TiDB components in Kubernetes

The TiDB components deployed by TiDB Operator output the logs in the `stdout` and `stderr` of the container by default. For Kubernetes, these logs are stored in the host's `/var/log/containers` directory, and the file name contains information such as the Pod name and the container name. For this reason, you can collect the logs of the application in the container directly on the host.

If you already have a system for collecting logs in your existing infrastructure, you only need to add the `/var/log/containers/*.log` file on the host that holds Kubernetes in the collection scope by conventional means; if there is no available log collection system, or you want to deploy a separate system for collecting relevant logs, you are free to use any system or solution that you are familiar with.

[ElasticSearch](https://kubernetes.io/docs/tasks/debug-application-cluster/logging-elasticsearch-kibana/) and [Stackdriver](https://kubernetes.io/docs/tasks/debug-application-cluster/logging-stackdriver/) are provided as two log collection methods for reference in the Kubernetes official documentation.

Common open source tools that can be used to collect Kubernetes logs are:

- [Fluentd](https://www.fluentd.org/)
- [Fluent-bit](https://fluentbit.io/)
- [Filebeat](https://www.elastic.co/products/beats/filebeat)
- [Logstash](https://www.elastic.co/products/logstash)

Collected Logs can usually be aggregated and stored on a specific server or in a dedicated storage and analysis system such as ElasticSearch.

Some cloud service providers or specialized performance monitoring service providers also have their own free or chargeable log collection options that you can choose from.

If you do not aggregate logs via a separate log collection tool, you can also use the `kubectl` tool directly to view the runtime log of a specific container, but this method does not allow you to view the log of a destroyed container:

{{< copyable "shell-regular" >}}

```shell
kubectl logs -n <namespace> <tidbPodName>
```

> **Note:**
>
> To view the log before the container restarts, you can add the `-p` parameter when executing the above command.

If you need to collect logs from multiple Pods, you can use [`stern`](https://github.com/wercker/stern):

{{< copyable "shell-regular" >}}

```shell
stern -n <namespace> tidb -c slowlog
```

## Collect TiDB slow query logs

For versions prior to 3.0, by default, TiDB prints slow query logs to standard output, mixed with application logs.

- For the TiDB version <= 2.1.7, you can filter the slow query logs with the keyword `SLOW_QUERY`, for example:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl logs -n <namespace> <tidbPodName> | grep SLOW_QUERY
    ```

- For the TiDB version >= 2.1.8, it is not so easy to separate the slow query log due to changes to the slow query log format. For this reason, it is recommended to configure `separateSlowLog: true` as described below to view the slow query log separately.

In some cases, you may want to use some tools or automated systems to analyze and process the log content. The application log of each TiDB component uses [unified log format](https://github.com/tikv/rfcs/blob/master/text/2018-12-19-unified-log-format.md), which facilitates parsing with other programs. However, because slow query logs use a multi-line format that is compatible with MySQL, it might be difficult to parse slow query logs when they are mixed with application logs.

If you want to separate the slow query logs from the application logs, you can configure the `separateSlowLog` parameter in the `values.yaml` file. This outputs the slow query log to a dedicated bypass container so that it can be stored in a separate file on the host.

To do this, follow the steps below:

1. Modify the `values.yaml` file and set the `separateSlowLog` parameter to `true`:

    ```yaml
    # Uncomment the following line to enable separate output of the slow query log
        separateSlowLog: true
    ```

2. Run `helm upgrade` to apply the configuration.

3. Then you can view the slow query log through the sidecar container named `slowlog`:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl logs -n <namespace> <tidbPodName> -c slowlog
    ```

For 3.0 and the later versions, TiDB outputs slow query logs to a separate `slowlog.log` file, and `separateSlowLog` is enabled by default, so you can view slow query logs directly from the sidecar container without additional settings.

> **Note:**
>
> The format of TiDB slow query logs is the same as that of MySQL slow query logs. However, due to the characteristics of TiDB itself, some of the specific fields may be different. For this reason, the tool for parsing MySQL slow query logs may not be fully compatible with TiDB slow query logs.

## Collect system logs

System logs can be collected on Kubernetes hosts in the usual way. If you already have a system for collecting logs in your existing infrastructure, you only need to add the relevant servers and log files in the collection scope by conventional means; if there is no available log collection system, or you want to deploy a separate set of systems for collecting relevant logs, you are free to use any system or solution that you are familiar with.

All of the common log collection tools mentioned above support collecting system logs. Some cloud service providers or specialized performance monitoring service providers also have their own free or chargeable log collection options that you can choose from.
