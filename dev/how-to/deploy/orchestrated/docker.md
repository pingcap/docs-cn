---
title: TiDB Docker 部署方案
category: how-to
---

# TiDB Docker 部署方案

本文介绍如何使用 Docker 部署一个多节点的 TiDB 集群。

> **警告：**
>
> 对于生产环境，不要使用 Docker 进行部署，而应[使用 Ansible 部署 TiDB 集群](/how-to/deploy/orchestrated/ansible.md)。

## 环境准备

### 安装 Docker

Docker 可以方便地在 Linux / Mac OS / Windows 平台安装，安装方法请参考 [Docker 官方文档](https://www.docker.com/products/docker)。

### 拉取 TiDB 的 Docker 镜像

部署 TiDB 集群主要包括 3 个服务组件:

- TiDB
- TiKV
- PD

对应的最新 Docker 镜像可以通过 [Docker 官方镜像仓库](https://hub.docker.com) 获取：

{{< copyable "shell-regular" >}}

```bash
docker pull pingcap/tidb:latest
```

{{< copyable "shell-regular" >}}

```bash
docker pull pingcap/tikv:latest
```

{{< copyable "shell-regular" >}}

```bash
docker pull pingcap/pd:latest
```

## 部署一个多节点集群

假设我们打算在 6 台主机上部署一个 TiDB 集群:

| 主机名       | IP            | 部署服务       | 数据盘挂载 |
| --------- | ------------- | ---------- | ----- |
| host1 | 192.168.1.101 | PD1 & TiDB | /data |
| host2 | 192.168.1.102 | PD2        | /data |
| host3 | 192.168.1.103 | PD3        | /data |
| host4 | 192.168.1.104 | TiKV1      | /data |
| host5 | 192.168.1.105 | TiKV2      | /data |
| host6 | 192.168.1.106 | TiKV3      | /data |

### 启动 PD

登录 **host1** 执行：

{{< copyable "shell-regular" >}}

```bash
docker run -d --name pd1 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /data:/data \
  pingcap/pd:latest \
  --name="pd1" \
  --data-dir="/data/pd1" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://192.168.1.101:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://192.168.1.101:2380" \
  --initial-cluster="pd1=http://192.168.1.101:2380,pd2=http://192.168.1.102:2380,pd3=http://192.168.1.103:2380"
```

登录 **host2** 执行：

{{< copyable "shell-regular" >}}

```bash
docker run -d --name pd2 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /data:/data \
  pingcap/pd:latest \
  --name="pd2" \
  --data-dir="/data/pd2" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://192.168.1.102:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://192.168.1.102:2380" \
  --initial-cluster="pd1=http://192.168.1.101:2380,pd2=http://192.168.1.102:2380,pd3=http://192.168.1.103:2380"
```

登录 **host3** 执行：

{{< copyable "shell-regular" >}}

```bash
docker run -d --name pd3 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /data:/data \
  pingcap/pd:latest \
  --name="pd3" \
  --data-dir="/data/pd3" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://192.168.1.103:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://192.168.1.103:2380" \
  --initial-cluster="pd1=http://192.168.1.101:2380,pd2=http://192.168.1.102:2380,pd3=http://192.168.1.103:2380"
```

### 启动 TiKV

登录 **host4** 执行：

{{< copyable "shell-regular" >}}

```bash
docker run -d --name tikv1 \
  -p 20160:20160 \
  --ulimit nofile=1000000:1000000 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /data:/data \
  pingcap/tikv:latest \
  --addr="0.0.0.0:20160" \
  --advertise-addr="192.168.1.104:20160" \
  --data-dir="/data/tikv1" \
  --pd="192.168.1.101:2379,192.168.1.102:2379,192.168.1.103:2379"
```

登录 **host5** 执行：

{{< copyable "shell-regular" >}}

```bash
docker run -d --name tikv2 \
  -p 20160:20160 \
  --ulimit nofile=1000000:1000000 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /data:/data \
  pingcap/tikv:latest \
  --addr="0.0.0.0:20160" \
  --advertise-addr="192.168.1.105:20160" \
  --data-dir="/data/tikv2" \
  --pd="192.168.1.101:2379,192.168.1.102:2379,192.168.1.103:2379"
```

登录 **host6** 执行：

{{< copyable "shell-regular" >}}

```bash
docker run -d --name tikv3 \
  -p 20160:20160 \
  --ulimit nofile=1000000:1000000 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /data:/data \
  pingcap/tikv:latest \
  --addr="0.0.0.0:20160" \
  --advertise-addr="192.168.1.106:20160" \
  --data-dir="/data/tikv3" \
  --pd="192.168.1.101:2379,192.168.1.102:2379,192.168.1.103:2379"
```

### 启动 TiDB

登录 **host1** 执行：

{{< copyable "shell-regular" >}}

```bash
docker run -d --name tidb \
  -p 4000:4000 \
  -p 10080:10080 \
  -v /etc/localtime:/etc/localtime:ro \
  pingcap/tidb:latest \
  --store=tikv \
  --path="192.168.1.101:2379,192.168.1.102:2379,192.168.1.103:2379"
```

### 使用 MySQL 标准客户端连接 TiDB 测试

登录 **host1** 并确保已安装 [MySQL 命令行客户端](http://dev.mysql.com/downloads/mysql/)，执行：

{{< copyable "shell-regular" >}}

```bash
mysql -h 127.0.0.1 -P 4000 -u root -D test
```

{{< copyable "sql" >}}

```sql
show databases;
```

```
+--------------------+
| Database           |
+--------------------+
| INFORMATION_SCHEMA |
| PERFORMANCE_SCHEMA |
| mysql              |
| test               |
+--------------------+
4 rows in set (0.00 sec)
```

### 如何自定义配置文件

TiKV 和 PD 可以通过指定配置文件的方式来加载更加丰富的启动参数，用于性能调优。

假定配置文件在宿主机上的存放路径 `/path/to/config/pd.toml` 和 `/path/to/config/tikv.toml`。启动 Docker 时需要调整相应的启动参数，以 tikv1 和 pd1 为例：

{{< copyable "shell-regular" >}}

```bash
docker run -d --name tikv1 \
  -p 20160:20160 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /data:/data \
  -v /path/to/config/tikv.toml:/tikv.toml:ro \
  pingcap/tikv:latest \
  --addr="0.0.0.0:20160" \
  --advertise-addr="192.168.1.104:20160" \
  --data-dir="/data/tikv1" \
  --pd="192.168.1.101:2379,192.168.1.102:2379,192.168.1.103:2379" \
  --config="/tikv.toml"
```

{{< copyable "shell-regular" >}}

```bash
docker run -d --name pd1 \
  -p 2379:2379 \
  -p 2380:2380 \
  -v /etc/localtime:/etc/localtime:ro \
  -v /data:/data \
  -v /path/to/config/pd.toml:/pd.toml:ro \
  pingcap/pd:latest \
  --name="pd1" \
  --data-dir="/data/pd1" \
  --client-urls="http://0.0.0.0:2379" \
  --advertise-client-urls="http://192.168.1.101:2379" \
  --peer-urls="http://0.0.0.0:2380" \
  --advertise-peer-urls="http://192.168.1.101:2380" \
  --initial-cluster="pd1=http://192.168.1.101:2380,pd2=http://192.168.1.102:2380,pd3=http://192.168.1.103:2380" \
  --config="/pd.toml"
```
