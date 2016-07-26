# 使用 Docker 构建和运行 TiDB

本文档用于说明如何使用 Docker 部署 TiDB 服务

## Docker 安装和环境准备

#### 安装 Docker
使用 Docker 可以非常快速搭建起一套 TiDB 环境。Docker 可以方便地在 Linux / Mac OS X / Windows 环境上安装，安装过程可参考 Docker 官网 https://docs.docker.com/linux/

#### 准备环境
完整的 TiDB 运行需要三个组件，TiDB, TiKV 和 PD。
* tidb-server 是 TiDB 的执行进程，负责客户端的接入，对用户的 SQL 进行解析、优化和执行，分解成下层的 KV 操作，并将执行结果进行聚合返回给客户端。TiDB 对外兼容 MySQL 协议，可以直接使用 MySQL Client 进行测试
* tikv-server，作为 TiDB 的分布式 KV 存储引擎，可以在网络互通的多机环境部署，使用 Raft 协议实现强一致性的数据复制，因此推荐 tikv-server 的部署节点为奇数个，当多数派节点存活 TiKV 保持可用状态
* pd-server，负责 TiKV 的 region 路由信息的维护，依托于 etcd 作为元数据的存储。并协调处理 region 的 rebalance 以及 merge 和 split 等操作

获取 TiDB, TiKV, PD 的 Docker 镜像可以直接拉 Docker Hub 发布的 latest 镜像。

```
docker pull pingcap/tidb
docker pull pingcap/tikv
docker pull pingcap/pd
```

github.com/pingcap 中的 repo 都包含 Dockerfile，也可以自行 build 镜像

```
git clone https://github.com/pingcap/tidb.git
cd tidb && docker build -t pingcap/tidb .

git clone https://github.com/pingcap/tikv.git
cd tikv && docker build -t pingcap/tikv .

git clone https://github.com/pingcap/pd.git
cd pd && docker build -t pingcap/pd .
```

## 使用单机存储引擎
tidb-server 默认运行在单机存储引擎，使用本机的 goleveldb 作为存储引擎，不依赖 TiKV。
使用 docker 可以直接启动：
```
docker run -d --name tidb-server \
  -v /etc/localtime:/etc/localtime:ro \
  -p 4000:4000 \
  -p 10080:10080 \
  pingcap/tidb:latest \
  -L info --path /tmp/tidb

docker run -d --name tidb-server -v /etc/localtime:/etc/localtime:ro -p 4000:4000 -p 10080:10080 pingcap/tidb:latest -L info --path /tmp/tidb
```

这样就在 4000 端口上启动了 tidb-server，可以使用 mysql client 连接 tidb-server:
```
mysql -h 127.0.0.1 -P 4000 -u root -D test
```

## 使用 TiKV 存储引擎
使用 TiKV 作为存储引擎可以构建分布式数据库。
集群环境下多机部署 TiDB，可以使用端口映射，例如在三台机器上部署 1个 PD，3个 TiKV，1个 TiDB

#### 定义 host 机器 ip
```
host_ip1=192.168.1.100
host_ip2=192.168.1.101
host_ip3=192.168.1.102
```

#### 启动一个仅作为数据存储的 Docker 容器
三台机器上个启动一个存储用容器
```
docker run -d --name ti-storage \
  -v /ti-data \
  busybox:latest
```

#### 启动 pd-server
```
docker run -d --name pd \
  -p 1234:1234 \
  -p 9090:9090 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /usr/share/ca-certificates/:/etc/ssl/certs \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
  pingcap/pd:latest \
  --addr=0.0.0.0:1234 \
  --advertise-addr=${host_ip1}:1234 \
  --http-addr=0.0.0.0:9090 \
  --etcd-name=etcd \
  --etcd-data-dir=/ti­data/etcd \
  --etcd-advertise-client-url=http://${host_ip1}:2379 \
  --etcd-advertise-peer-url=http://${host_ip1}:2380 \
  --etcd-initial-cluster=etcd=http://${host_ip1}:2380 \
  --etcd-listen-peer-url=http://0.0.0.0:2380 \
  --etcd-listen-client-url=http://0.0.0.0:2379 \
  -L info \
  --cluster-id=1 \
  --max-peer-count=3
```

#### 启动 tikv-server
在三台机器上分别启动 TiKV 服务
```
# 机器1
docker run -d --name tikv1 \
  -p 20160:20160 \
  -v /etc/localtime:/etc/localtime:ro \
  --volumes-from ti-storage \
    pingcap/tikv:latest \
    -S raftkv \
    --addr=0.0.0.0:20160 \
    --advertise-addr=${host_ip1}:20160\
    --etcd=${host_ip1}:2379 \
    --store=/ti-data/tikv \
    --cluster-id=1

# 机器2
  docker run -d --name tikv2 \
    -p 20160:20160 \
    -v /etc/localtime:/etc/localtime:ro \
    --volumes-from ti-storage \
    pingcap/tikv:latest \
    -S raftkv \
    --addr=0.0.0.0:20160 \
    --advertise-addr=${host_ip2}:20160\
    --etcd=${host_ip1}:2379 \
    --store=/ti-data/tikv \
    --cluster-id=1

# 机器3
  docker run -d --name tikv3 \
    -p 20160:20160 \
    -v /etc/localtime:/etc/localtime:ro \
    --volumes-from ti-storage \
    pingcap/tikv:latest \
    -S raftkv \
    --addr=0.0.0.0:20160 \
    --advertise-addr=${host_ip3}:20160\
    --etcd=${host_ip1}:2379 \
    --store=/ti-data/tikv \
    --cluster-id=1
```

#### 启动 tidb-server
```
docker run -d --name tidb \
    -p 4000:4000 \
    -v /etc/localtime:/etc/localtime:ro \
    pingcap/tidb:latest \
    -L info \
    --store=tikv \
    --path="${host_ip1}:2379/pd?cluster=1" \
    -P 4000
```
