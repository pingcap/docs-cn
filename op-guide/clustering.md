# 集群

## 概述

一个完整的 TiDB 集群包括 PD，TiKV 以及 TiDB。启动顺序依次是 PD，TiKV 以及 TiDB。

## 单节点集群

我们可以在单机上面，运行和测试 TiDB 集群。

1. 启动 PD.

    ```bash
    pd-server --cluster-id=1 \
              --data-dir=pd
    ```
    
2. 启动 TiKV.

    ```bash
    tikv-server -I 1 \
                -S raftkv \
                --pd 127.0.0.1:2379 \
                -s tikv
    ```

3. 启动 TiDB.

    ```bash
    tidb-server --store=tikv \
                --path="127.0.0.1:2379?cluster=1" 
    ```

4. 使用官方的 `mysql` 客户端连接 TiDB. 

    ```sh
    mysql -h 127.0.0.1 -P 4000 -u root -D test
    ```

## 多节点集群

在生产环境中，我们推荐多节点部署 TiDB 集群，最佳实践，可以参考[部署建议](./overview.md#部署建议)。

这里我们使用 3 个节点为例，各个节点信息如下：

|Name|Host IP|
|----|-------|
|node1|192.168.199.113|
|node2|192.168.199.114|
|node3|192.168.199.115|

我们在各个节点，都分别运行一个 PD 和 TiKV 服务，在 node1 上面启动 TiDB。

1. 在每个节点启动 PD.

    ```bash
    pd-server --cluster-id=1 \
              --name=pd1 \
              --data-dir=pd1 \
              --client-urls="http://192.168.199.113:2379" \
              --peer-urls="http://192.168.199.113:2380" \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
              
    pd-server --cluster-id=1 \
              --name=pd2 \
              --data-dir=pd2 \
              --client-urls="http://192.168.199.114:2379" \
              --peer-urls="http://192.168.199.114:2380" \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
              
    pd-server --cluster-id=1 \
              --name=pd3 \
              --data-dir=pd3 \
              --client-urls="http://192.168.199.115:2379" \
              --peer-urls="http://192.168.199.115:2380" \
              --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380"
    ```

2. 在每个节点启动 TiKV.

    ```bash
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                --addr 192.168.199.113:20160 \
                -s tikv1
    
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                --addr 192.168.199.114:20160 \
                -s tikv2
                
    tikv-server -S raftkv \
                -I 1 \
                --pd 192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379 \
                --addr 192.168.199.115:20160 \
                -s tikv3
    ```

3. 在 node1 启动 TiDB.

    ```bash
    tidb-server --store=tikv \
                --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379?cluster=1"
    ```

4. 使用官方 `mysql` 客户端连接 TiDB. 

    ```sh
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

```
pd-server --cluster-id=1 \
          --name=pd4 \
          --client-urls="http://host4:2379"
          --peer-urls="http://host4:2380"
          --join="http://host1:2379"
```

### TiKV

动态新加入一个新的 TiKV 服务是非常容易的，我们可以直接启动一个 TiKV 服务，PD 会自动检测到，
并开始做整个集群的 balance，将其他 TiKV 的数据移动到新加入的 TiKV 里面。

我们也能够显示的告诉 PD 去删除某个 TiKV。PD 会认为这个 TiKV 已经是 dead 了，如果某一个 region 
原先有数据属于这个 TiKV，PD 就会选择一个新的 TIKV 给这个 region，重新做 balance。

### TiDB

TiDB 是一个无状态的服务，这也就意味着我们能直接添加和删除 TiDB。需要注意的是如果我们在 TiDB 的服务的前面搭建了一个 proxy（譬如 HAProxy），我们需要更新 proxy 的配置并重新载入。
