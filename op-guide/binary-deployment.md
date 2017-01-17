# TiDB Binary 部署方案

## 概述

一个完整的 TiDB 集群包括 PD，TiKV 以及 TiDB。启动顺序依次是 PD，TiKV 以及 TiDB。

阅读本章前，请先确保阅读 [TiDB 整体架构](../overview.md#tidb-整体架构) 及 [部署建议](../op-guide/recommendation.md)

快速了解和试用 TiDB，推荐使用[单节点方式快速部署](#单节点方式快速部署)。

功能性测试 TiDB，推荐使用[功能性测试部署](#功能性测试部署)。

生产环境使用 TiDB，推荐使用[多节点集群模式部署](#多节点集群模式部署)。

## 下载官方 Binary

### Linux (CentOS 7+, Ubuntu 14.04+)

```bash
# 下载压缩包
wget http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-latest-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-latest-linux-amd64.sha256

# 解开压缩包
tar -xzf tidb-latest-linux-amd64.tar.gz
cd tidb-latest-linux-amd64
```
### CentOS 6
> 注意：我们大部分开发和测试都是在 CentOS 7+, Ubuntu 14.04+ 上进行，CentOS 6 上面并没有经过严格测试，所以不推荐在 CentOS 6 上部署 TiDB 集群

```bash
# 下载 CentOS6 压缩包
wget http://download.pingcap.org/tidb-latest-linux-amd64-centos6.tar.gz
wget http://download.pingcap.org/tidb-latest-linux-amd64-centos6.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-latest-linux-amd64-centos6.sha256

# 解开压缩包
tar -xzf tidb-latest-linux-amd64-centos6.tar.gz
cd tidb-latest-linux-amd64-centos6
```

## 单节点方式快速部署

我们可以在单机上面，运行和测试 TiDB 集群，请按如下步骤**依次启动** PD，TiKV，TiDB：

1. 启动 PD

    ```bash
    ./bin/pd-server --data-dir=pd
    ```

2. 启动 TiKV

    ```bash
    ./bin/tikv-server --pd="127.0.0.1:2379" \
                      --store=tikv
    ```

3. 启动 TiDB

    ```bash
    ./bin/tidb-server --store=tikv \
                      --path="127.0.0.1:2379"
    ```

4. 使用官方的 `mysql` 客户端连接 TiDB

    ```bash
    mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```

## 多节点集群模式部署
在生产环境中，我们推荐多节点部署 TiDB 集群，首先请参考[部署建议](./recommendation.md)。

这里我们使用六个节点，部署三个 PD，三个 TiKV，以及一个 TiDB，各个节点以及所运行服务信息如下：

|Name|Host IP|Services|
|----|-------|--------|
|node1|192.168.199.113|PD1, TiDB|
|node2|192.168.199.114|PD2|
|node3|192.168.199.115|PD3|
|node4|192.168.199.116|TiKV1|
|node5|192.168.199.117|TiKV2|
|node6|192.168.199.118|TiKV3|

请按如下步骤 **依次启动** PD 集群，TiKV 集群以及 TiDB：

1. 在 node1，node2，node3 启动 PD

    ```bash
    ./bin/pd-server --name=pd1 \
                    --data-dir=pd1 \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"

    ./bin/pd-server --name=pd2 \
                    --data-dir=pd2 \
                    --client-urls="http://192.168.199.114:2379" \
                    --peer-urls="http://192.168.199.114:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"

    ./bin/pd-server --name=pd3 \
                    --data-dir=pd3 \
                    --client-urls="http://192.168.199.115:2379" \
                    --peer-urls="http://192.168.199.115:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
    ```

2. 在 node4，node5，node6 启动 TiKV

    ```bash
    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.116:20160" \
                      --store=tikv1

    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.117:20160" \
                      --store=tikv2

    ./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                      --addr="192.168.199.118:20160" \
                      --store=tikv3
    ```

3. 在 node1 启动 TiDB

    ```bash
    ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379"
    ```

4. 使用官方 `mysql` 客户端连接 TiDB

    ```bash
    mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```

> 注意：在生产环境中启动 TiKV 时，建议使用 [\-\-config](op-guide/configuration.md#-c---config) 参数指定配置文件路径，如果不设置这个参数，TiKV 不会读取配置文件。同样，在生产环境中部署 PD 时，也建议使用 [\-\-config](op-guide/configuration.md#--config) 参数指定配置文件路径。
> 
> 注意：如果使用 `nohup` 在生产环境中启动集群，需要将启动命令放到一个脚本文件里面执行，否则会出现因为 Shell 退出导致 `nohup` 启动的进程也收到异常信号退出的问题，具体参考[进程异常退出](../trouble-shooting.md#tidbtikvpd-进程异常退出)。

## 功能性测试部署

如果只是对 TiDB 进行测试，并且机器数量有限，我们可以只启动一台 PD 测试 整个集群。

这里我们使用四个节点，部署一个 PD，三个 TiKV，以及一个 TiDB，各个节点以及所运行服务信息如下：

|Name|Host IP|Services|
|----|-------|--------|
|node1|192.168.199.113|PD1, TiDB|
|node2|192.168.199.114|TiKV1|
|node3|192.168.199.115|TiKV2|
|node4|192.168.199.116|TiKV3|


请按如下步骤 **依次启动** PD 集群，TiKV 集群以及 TiDB：

1. 在 node1 启动 PD

    ```bash
    ./bin/pd-server --name=pd1 \
                    --data-dir=pd1 \
                    --client-urls="http://192.168.199.113:2379" \
                    --peer-urls="http://192.168.199.113:2380" \
                    --initial-cluster="pd1=http://192.168.199.113:2380"
    ```

2. 在 node2，node3，node4 启动 TiKV

    ```bash
    ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.114:20160" \
                      --store=tikv1

    ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.115:20160" \
                      --store=tikv2

    ./bin/tikv-server --pd="192.168.199.113:2379" \
                      --addr="192.168.199.116:20160" \
                      --store=tikv3
    ```

3. 在 node1 启动 TiDB

    ```bash
    ./bin/tidb-server --store=tikv \
                      --path="192.168.199.113:2379"
    ```

4. 使用官方 `mysql` 客户端连接 TiDB

    ```bash
    mysql -h 192.168.199.113 -P 4000 -u root -D test
    ```
