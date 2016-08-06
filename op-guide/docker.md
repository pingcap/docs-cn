# 在单机上使用 Docker 运行一个 TiDB 集群

本文档用于说明如何在单机上使用 Docker 部署一套完整的 TiDB 服务。

## 环境准备

#### 安装 Docker
使用 Docker 可以非常快速搭建一套 TiDB 环境。
Docker 可以方便地在 Linux / Mac OS X / Windows 平台安装，安装过程可参考 [Docker 官网](https://www.docker.com/products/docker)

#### 获取镜像
一个 TiDB 集群包含三种类型的服务组件，TiDB, TiKV 和 PD。

+ tidb-server 是 TiDB 的执行进程，负责客户端的接入，对用户的 SQL 进行解析、优化和执行，并转化为下层的 KV 操作，将执行结果进行聚合返回给客户端。TiDB 对外兼容 MySQL 协议，可以直接使用 MySQL Client 进行测试。
+ tikv-server，作为 TiDB 的分布式 KV 存储引擎，可以在网络互通的多机环境部署，使用 Raft 协议实现强一致性的数据复制，当多数派节点存活时 TiKV 保持可用状态。
+ pd-server，负责 TiKV 的 Region 路由信息的维护和存储，并协调处理数据的 rebalance 以及 merge 和 split 等操作。一个集群可部署多个 PD 实例。

获取 TiDB, TiKV, PD 的 Docker 镜像可以直接拉 Docker Hub 发布的 latest 镜像。

```
docker pull pingcap/tidb
docker pull pingcap/tikv
docker pull pingcap/pd
```

## 独立运行 tidb
tidb-server 默认运行在单机存储引擎，使用本机的 goleveldb 作为存储引擎，不依赖 TiKV。
使用 docker 可以直接启动：

```
docker run -d --name tidb \
  -v /etc/localtime:/etc/localtime:ro \
  -p 4000:4000 \
  -p 10080:10080 \
  pingcap/tidb
```

这样就在 4000 端口上启动了 tidb-server，可以使用 mysql client 连接 tidb-server:

```
mysql -h 127.0.0.1 -P 4000 -u root -D test
```

## 运行一个基于分布式 TiKV 的 TiDB 集群
接下来是一个例子, 在单机环境下, 使用 Docker 构建一个基于分布式 TiKV 引擎的 TiDB 集群。

#### 1. 创建一个 docker bridge network

```bash
net="isolated_nw"
docker network rm ${net}
docker network create --driver bridge ${net} 
```

使用 docker bridge network 非常方便地构建一个私有的局域网, 与 host 所在的网络环境是相互隔离的。
加入这个网络的 docker 容器之间可以用名字代替真实 IP 相互访问。
此外, 上面的网络名字可以自由替换。

#### 2. 启动一个仅用于数据存储的 docker 容器

```bash
docker run -d --name ti-storage \
  -v /tidata \
  busybox
```

#### 3. 启动 PD 服务
首先我们启动 3 个 pd-server, 分别命名为: **pd1**, **pd2**, **pd3**

**pd1:** 

```bash
docker run --net ${net} -d --name pd1 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd1" \
  --data-dir="/tidata/pd1" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd1:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd1:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
```

**pd2:**

```bash
docker run --net ${net} -d --name pd2 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd2" \
  --data-dir="/tidata/pd2" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd2:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd2:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
```

**pd3:**

```bash
docker run --net ${net} -d --name pd3 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd3" \
  --data-dir="/tidata/pd3" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd3:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd3:2380" \
  --initial-cluster="pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380" \
```

之后, 当如果需要加入两个新的 PD 节点到集群, 只需要用 --join 参数, 并指定上面任何一个可用的 advertise-client-urls。

**pd4:**

```bash
docker run --net ${net} -d --name pd4 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd4" \
  --data-dir="/tidata/pd4" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd4:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd4:2380" \
  --join="http://pd1:2379" \
```

**pd5:**

``bash
docker run --net ${net} -d --name pd5 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd \
  --cluster-id=1 \
  --name="pd5" \
  --data-dir="/tidata/pd5" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://pd5:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://pd5:2380" \
  --join="http://pd4:2379" \
```

#### 4. 启动 TiKV 服务
接下来你可以启动任意数量的 TiKV 实例

**tikv1:**

```bash
docker run --net ${net} -d --name tikv1 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv1:20160" \
  --store="/tidata/tikv1" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```

**tikv2:**

```bash
docker run --net ${net} -d --name tikv2 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv2:20160" \
  --store="/tidata/tikv2" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```

**tikv3:**

```bash
docker run --net ${net} -d --name tikv3 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/tikv \
  --addr="0.0.0.0:20160" \
  --advertise-addr="tikv3:20160" \
  --store="/tidata/tikv3" \
  --dsn=raftkv \
  --pd="pd1:2379,pd2:2379,pd3:2379" \
  --cluster-id=1
```


#### 5. 启动 TiDB 服务

```bash
docker run --net ${net} -d --name tidb \
  -p 4000:4000 \
  -v /etc/localtime:/etc/localtime:ro \
  pingcap/tidb \
  --store=tikv \
  --path="pd1:2379,pd2:2379,pd3:2379?cluster=1" \
  -L warn
```

#### 6. 使用客户端进行测试

```bash
mysql -h 127.0.0.1 -P 4000 -u root -D test
```

## 使用 `docker-compose`, 更方便地构建集群

只需要一个简单的 `docker-compose.yml`:

```bash
version: '2'

services:
  pd1:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --cluster-id=1 
      - --name=pd1 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd1:2379
      - --advertise-peer-urls=http://pd1:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380
      
    privileged: true

  pd2:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --cluster-id=1 
      - --name=pd2 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd2:2379
      - --advertise-peer-urls=http://pd2:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380
      
    privileged: true

  pd3:
    image: pingcap/pd
    ports:
      - "2379"
      - "2380"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --cluster-id=1 
      - --name=pd3 
      - --client-urls=http://0.0.0.0:2379
      - --peer-urls=http://0.0.0.0:2380
      - --advertise-client-urls=http://pd3:2379
      - --advertise-peer-urls=http://pd3:2380
      - --initial-cluster=pd1=http://pd1:2380,pd2=http://pd2:2380,pd3=http://pd3:2380 
      
    privileged: true

  tikv1:
    image: pingcap/tikv
    ports:
      - "20160"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv1:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tikv2:
    image: pingcap/tikv
    ports:
      - "20160"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv2:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tikv3:
    image: pingcap/tikv
    ports:
      - "20160"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --cluster-id=1
      - --addr=0.0.0.0:20160
      - --advertise-addr=tikv3:20160
      - --dsn=raftkv
      - --store=/var/tikv
      - --pd=pd1:2379,pd2:2379,pd3:2379

    depends_on:
      - "pd1"
      - "pd2"
      - "pd3"

    entrypoint: /tikv-server

    privileged: true

  tidb:
    image: pingcap/tidb
    ports:
      - "4000"
      - "10080"
    volumes:
      - /etc/localtime:/etc/localtime:ro

    command:
      - --store=tikv 
      - --path=pd1:2379,pd2:2379,pd3:2379?cluster=1
      - -L=warn

    depends_on:
      - "tikv1"
      - "tikv2"
      - "tikv3"

    privileged: true
```

+ 使用 `docker-compose up -d` 创建并启动集群
+ 使用 `docker-compose port tidb 4000` 获得 TiDB 的对外服务端口。由于 Docker 做了端口转发, 你可能会获得一个类似 `0.0.0.0:32966` 的结果, 那么就可以通过 `32966` 端口访问 TiDB
+ 运行 `mysql -h 127.0.0.1 -P 32966 -u root -D test` 连接到 TiDB 进行测试
+ 运行 `docker-compose down` 关闭并销毁集群
