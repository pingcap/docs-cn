---
title: 部署和使用 TiCDC
category: reference
aliases: ['/docs-cn/dev/reference/tools/ticdc/deploy/']
---

# 部署和使用 TiCDC

本文介绍如何部署和使用 TiCDC 进行增量数据同步。

## 第 1 步：部署 TiCDC 集群

本节介绍了在不同场景下如何安装部署 TiCDC，包括以下场景：

- [使用 TiUP 全新部署 TiCDC](#使用-tiup-全新部署-ticdc)
- [使用 TiUP 在原有 TiDB 集群上新增 TiCDC 组件](#使用-tiup-在原有-tidb-集群上新增-ticdc-组件)
- [手动在原有 TiDB 集群上新增 TiCDC 组件](#手动在原有-tidb-集群上新增-ticdc-组件)

### 使用 TiUP 全新部署 TiCDC

TiUP cluster 是适用于 TiDB 4.0 及以上版本的部署工具，部署运行 TiCDC 必须使用 TiDB v4.0.0-rc.1 或更新版本，部署流程如下：

1. 参考 [TiUP 部署文档](/production-deployment-using-tiup.md)安装 TiUP。

2. 安装 TiUP cluster 组件

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster
    ```

3. 编写 topology 配置文件，保存为 `topology.yaml`。

    可以参考[全量的配置文件模版](https://github.com/pingcap-incubator/tiup-cluster/blob/master/examples/topology.example.yaml)。

    除了部署 TiDB 集群的配置，需要额外在 `cdc_servers` 下配置 CDC 服务器所在的 ip（目前只支持 ip，不支持域名）。

    {{< copyable "" >}}

    ```ini
    pd_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103

    tidb_servers:
      - host: 172.19.0.101

    tikv_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103

    cdc_servers:
      - host: 172.19.0.101
      - host: 172.19.0.102
      - host: 172.19.0.103
    ```

4. 按照 TiUP 部署流程完成集群部署的剩余步骤，包括：

    部署 TiDB 集群，其中 test 为集群名：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster deploy test v4.0.0-rc.1 topology.yaml -i ~/.ssh/id_rsa
    ```

    启动 TiDB 集群：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster start test
    ```

5. 查看集群状态

    {{< copyable "shell-regular" >}}

    ```shell
    tiup cluster display test
    ```

### 使用 TiUP 在原有 TiDB 集群上新增 TiCDC 组件

1. 首先确认当前 TiDB 的版本支持 TiCDC，否则需要先升级 TiDB 集群至 4.0.0 rc.1 或更新版本。

2. 参考 [扩容 TiDB/TiKV/PD/TiCDC 节点](/scale-tidb-using-tiup.md#1-扩容-tidbtikvpdticdc-节点) 章节对 TiCDC 进行部署。

   示例的扩容配置文件为：

   ```shell
   vi scale-out.yaml
   ```

   ```
   cdc_servers:
    - host: 10.0.1.5
    - host: 10.0.1.6
    - host: 10.0.1.7
   ```

   随后执行扩容命令即可：
   {{< copyable "shell-regular" >}}

   ```shell
   tiup cluster scale-out <cluster-name> scale-out.yaml
   ```

### 手动在原有 TiDB 集群上新增 TiCDC 组件

假设 PD 集群有一个可以提供服务的 PD 节点（client URL 为 `10.0.10.25:2379`）。若要部署三个 TiCDC 节点，可以按照以下命令启动集群。只需要指定相同的 PD 地址，新启动的节点就可以自动加入 TiCDC 集群。

{{< copyable "shell-regular" >}}

```shell
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_1.log --addr=0.0.0.0:8301 --advertise-addr=127.0.0.1:8301
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_2.log --addr=0.0.0.0:8302 --advertise-addr=127.0.0.1:8302
cdc server --pd=http://10.0.10.25:2379 --log-file=ticdc_3.log --addr=0.0.0.0:8303 --advertise-addr=127.0.0.1:8303
```

对于 `cdc server` 命令中可用选项解释如下：

- `gc-ttl`: TiCDC 在 PD 设置的服务级别 GC safepoint 的 TTL (Time To Live) 时长，单位为秒，默认值为 `86400`，即 24 小时。
- `pd`: PD client 的 URL。
- `addr`: TiCDC 的监听地址，提供服务的 HTTP API 查询地址和 Prometheus 查询地址。
- `advertise-addr`: TiCDC 对外访问地址。
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
- `sink-uri`: sink 地址，目前支持 `mysql`/`tidb` 和 `kafka`。关于 sink URI 的写法请参考 [sink URI 配置规则](/ticdc/sink-url.md)
- `config`: 同步任务的配置。目前提供黑白名单配置和跳过特定 `commit-ts` 的事务。

执行该命令后，TiCDC 就会从指定的 start-ts (`415238226621235200`) 开始同步数据到下游 MySQL (`127.0.0.1:3306`) 中。

如果希望同步数据到 Kafka 集群，需要先在 Kafka 集群中创建好 topic（比如以下示例创建了名为 `cdc-test` 的 topic），划分好 partition，并通过以下命令创建到 Kafka 集群的同步任务：

{{< copyable "shell-regular" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --start-ts=415238226621235200 --sink-uri="kafka://10.0.10.30:9092/cdc-test"
```

执行命令以上后，TiCDC 会从指定 `start-ts` 开始同步数据到下游 Kafka (`10.0.10.30:9092`) 中。
