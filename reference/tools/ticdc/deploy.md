---
title: 部署和使用 TiCDC
category: reference
---

# 部署和使用 TiCDC

本文介绍如何部署和使用 TiCDC 进行增量数据同步。

## 第 1 步：部署 TiCDC 集群

假设 PD 集群有一个可以提供服务的 PD 节点（client URL 为 `10.0.10.25:2379`）。若要部署三个 TiCDC 节点，可以按照以下命令启动集群。只需要指定相同的 PD 地址，新启动的节点就可以自动加入 TiCDC 集群。

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --status-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --status-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --status-addr=127.0.0.1:8303
```

对于 `cdc server` 命令中可用选项解释如下：

- `gc-ttl`: TiCDC 在 PD 设置的服务级别 GC safepoint 的 TTL (Time To Live) 时长，单位为秒，默认值为 `86400`，即 24 小时。
- `pd`: PD client 的 URL。
- `status-addr`: TiCDC 服务的 HTTP API 查询地址和 Prometheus 查询地址。
- `tz`: TiCDC 服务使用的时区。TiCDC 在内部转换 timestamp 等时间数据类型和向下游同步数据时使用该时区，默认为进程运行本地时区。
- `log-file`: TiCDC 进程运行日志的地址，默认为 `cdc.log`。
- `log-level`: TiCDC 进程运行时默认的日志级别，默认为 `info`。

## 第 2 步：创建同步任务

假设需要将上游所有的库表（系统表除外）同步到下游的 MySQL，可以通过以下命令创建同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="mysql://root:123456@127.0.0.1:3306/"
```

以上命令中的选项解释如下：

- `pd`: PD client 的 URL。
- `start-ts`: 指定开始同步的 TSO，不指定或指定为 `0` 时将使用当前 TSO 作为同步的起始 TSO。
- `target-ts`: 指定同步结束的 TSO，不指定默认会永久同步。
- `sink-uri`: sink 地址，目前支持 `mysql`/`tidb` 和 `kafka`。关于 sink URI 的写法请参考 [sink URI 配置规则](/reference/tools/ticdc/sink.md)
- `config`: 同步任务的配置。目前提供黑白名单配置和跳过特定 `commit-ts` 的事务。

执行该命令后，TiCDC 就会从指定的 start-ts (`415238226621235200`) 开始同步数据到下游 MySQL (`127.0.0.1:3306`) 中。

如果希望同步数据到 Kafka 集群，需要先在 Kafka 集群中创建好 topic（比如以下示例创建了名为 `cdc-test` 的 topic），划分好 partition，并通过以下命令创建到 Kafka 集群的同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="kafka://10.0.10.30:9092/cdc-test"
```

执行命令以上后，TiCDC 会从指定 `start-ts` 开始同步数据到下游 Kafka (`10.0.10.30:9092`) 中。
