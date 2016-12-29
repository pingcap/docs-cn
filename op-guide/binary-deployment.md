# TiDB Binary 部署方案

## 概述

一个完整的 TiDB 集群包括 PD，TiKV 以及 TiDB。启动顺序依次是 PD，TiKV 以及 TiDB。

阅读本章前，请先确保阅读 [TiDB 整体架构](../README.md#tidb-总览) 及 [部署建议](../op-guide/recommendation.md)

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
#### CentOS 6（不推荐）

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

1. 启动 PD.

```bash
./bin/pd-server --data-dir=pd
```

2. 启动 TiKV.

```bash
./bin/tikv-server --pd="127.0.0.1:2379" \
                  --store=tikv
```

3. 启动 TiDB.

```bash
./bin/tidb-server --store=tikv \
                  --path="127.0.0.1:2379"
```

4. 使用官方的 `mysql` 客户端连接 TiDB.

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

请按如下步骤**依次启动** PD 集群，TiKV 集群以及 TiDB：

1. 在 node1，node2，node3 启动 PD.

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

2. 在 node4，node5，node6 启动 TiKV.

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

3. 在 node1 启动 TiDB.

```bash
./bin/tidb-server --store=tikv \
                    --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379"
```

4. 使用官方 `mysql` 客户端连接 TiDB.

```bash
mysql -h 192.168.199.113 -P 4000 -u root -D test
```

**注意：在生产环境中启动 TiKV 时，建议使用 [--config](https://github.com/pingcap/docs-cn/blob/master/op-guide/configuration.md#-c---config) 参数指定配置文件路径，如果不设置这个参数，TiKV 不会读取配置文件。同样，在生产环境中部署 PD 时，也建议使用 [--config](https://github.com/pingcap/docs-cn/blob/master/op-guide/configuration.md#--config) 参数指定配置文件路径。**

## 功能性测试部署

如果只是对 TiDB 进行测试，并且机器数量有限，我们可以只启动一台 PD 测试 整个集群。

这里我们使用四个节点，部署一个 PD，三个 TiKV，以及一个 TiDB，各个节点以及所运行服务信息如下：

|Name|Host IP|Services|
|----|-------|--------|
|node1|192.168.199.113|PD1, TiDB|
|node2|192.168.199.114|TiKV1|
|node3|192.168.199.115|TiKV2|
|node4|192.168.199.116|TiKV3|


请按如下步骤**依次启动** PD 集群，TiKV 集群以及 TiDB：

1. 在 node1 启动 PD.

```bash
./bin/pd-server --name=pd1 \
                --data-dir=pd1 \
                --client-urls="http://192.168.199.113:2379" \
                --peer-urls="http://192.168.199.113:2380" \
                --initial-cluster="pd1=http://192.168.199.113:2380"
```

2. 在 node2，node3，node4 启动 TiKV.

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

3. 在 node1 启动 TiDB.

```bash
./bin/tidb-server --store=tikv \
                    --path="192.168.199.113:2379"
```

4. 使用官方 `mysql` 客户端连接 TiDB.

```bash
mysql -h 192.168.199.113 -P 4000 -u root -D test
```

## 动态添加节点

### PD

我们可以使用 `join` 参数，方便的将一个 PD 服务加入到现有的 PD 集群里面。假设现在我们有三个 PD 服务，详细信息如下：

|Name|ClientUrls|PeerUrls|
|----|----------|--------|
|pd1|http://host1:2379|http://host1:2380|
|pd2|http://host2:2379|http://host2:2380|
|pd3|http://host3:2379|http://host3:2380|

如果我们需要添加 `pd4`，只需要在 `join` 参数里面填入当前 PD 集群某一个 PD 服务的 `ClientUrls` 就可以了，如下：

```bash
./bin/pd-server --name=pd4 \
                --client-urls="http://host4:2379"
                --peer-urls="http://host4:2380"
                --join="http://host1:2379"
```

如果我们需要删除 `pd4`，可以通过 PD 的 HTTP API 来完成：

```bash
curl -X DELETE http://host1:2379/pd/api/v1/members/pd4
```

最后我们可以查看当前 PD 的所有节点来确定是否添加或者删除成功：

```bash
curl http://host1:2379/pd/api/v1/members
```

### TiKV

动态新加入一个新的 TiKV 服务是非常容易的，我们可以直接启动一个 TiKV 服务，PD 会自动检测到，
并开始做整个集群的 balance，将其他 TiKV 的数据移动到新加入的 TiKV 里面。

我们也能够显式的告诉 PD 去删除某个 TiKV。PD 会先把这个 TiKV 标记为正在下线的状态，
然后把这个 TiKV 上的数据均匀地迁移到其他 TiKV 上面。当这个 TiKV 上的数据已经迁移
完了，PD 会把这个 TiKV 标记为完成下线的状态，这时候就可以安全地把这个 TiKV 从集
群中去掉。

假设我们要删除一个 store id 为 1 的 TiKV，可以调用 PD 的 HTTP API 来操作：

```bash
curl -X DELETE http://host:port/pd/api/v1/store/1
```

然后可以查看这个 TiKV 的当前状态：

```bash
curl http://host:port/pd/api/v1/store/1
```

如果这个 TiKV 正在下线，对应的 state=1，如果这个 TiKV 完成下线，对应的 state=2，
否则 state=0。

更详细的 API 文档可以参考 [PD APIv1](https://cdn.rawgit.com/pingcap/docs/master/op-guide/pd-api-v1.html)。

### TiDB

TiDB 是一个无状态的服务，这也就意味着我们能直接添加和删除 TiDB。需要注意的是如果我们在 TiDB 的服务的前面搭建了一个 proxy（譬如 HAProxy），我们需要更新 proxy 的配置并重新载入。
