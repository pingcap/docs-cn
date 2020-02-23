---
title: TiDB Binary 部署方案详解
category: deployment
---

# TiDB Binary 部署指导

## 概述

一个完整的 TiDB 集群包括 PD，TiKV 以及 TiDB。启动顺序依次是 PD，TiKV 以及 TiDB。在关闭数据库服务时，请按照启动的相反顺序进行逐一关闭服务。

阅读本章前，请先确保阅读 [TiDB 整体架构](../overview.md#tidb-整体架构)及[部署建议](recommendation.md)。

本文档描述了三种场景的二进制部署方式：

- 快速了解和试用 TiDB，推荐使用[单节点方式快速部署](#单节点方式快速部署)。

- 功能性测试 TiDB，推荐使用[功能性测试部署](#功能性测试部署)。

- 生产环境使用 TiDB，推荐使用[多节点集群模式部署](#多节点集群模式部署)。

## TiDB 组件及默认端口

### 1. TiDB 数据库组件（必装）

| 组件 | 默认端口 | 协议 | 说明 |
| :-- | :-- | :-- | :--------------- |
| ssh | 22 | TCP | sshd 服务 |
| TiDB |  4000  | TCP |  应用及 DBA 工具访问通信端口 |
| TiDB | 10080  |  TCP | TiDB 状态信息上报通信端口 |
| TiKV |  20160 |  TCP | TiKV 通信端口  |
| PD | 2379 | TCP | 提供 TiDB 和 PD 通信端口 |
| PD | 2380 | TCP | PD 集群节点间通信端口 |

### 2. TiDB 数据库组件（选装）

| 组件 | 默认端口 | 协议 | 说明 |
| :-- | :-- | :-- | :------------------------ |
| Prometheus |  9090| TCP | Prometheus 服务通信端口 |
| Pushgateway |  9091 | TCP | TiDB, TiKV, PD 监控聚合和上报端口 |
| Node_exporter|  9100| TCP | TiDB 集群每个节点的系统信息上报通信端口 |
| Grafana | 3000 | TCP | Web 监控服务对外服务和客户端(浏览器)访问端口 |
| alertmanager | 9093 | TCP | 告警服务端口 |

## TiDB 安装前系统配置与检查

### 操作系统检查

| 配置 | 描述 |
| :-- | :---------------------------- |
|  支持平台  |   请查看和了解[系统部署建议](recommendation.md) |
|  文件系统  |  TiDB 部署环境推荐使用 ext4 文件系统 |
|  Swap 空间  |  TiDB 部署推荐关闭 Swap 空间 |
|  Disk Block Size  |  设置系统磁盘 Block 大小为 4096 |

### 网络与防火墙

| 配置| 描述 |
| :-- | :---------------------------- |
| 防火墙 / 端口 | 请查看 TiDB 所需端口在各个节点之间是否能正常访问 |

### 操作系统参数

| 配置 | 说明 |
| :-- | :---------------------------- |
| Nice Limits | 系统用户 tidb 的 nice 值设置为缺省值 0 |
| min_free_kbytes | 在 `sysctl.conf` 中关于 `vm.min_free_kbytes` 的设置需要足够高 |
| User Open Files Limit | 对数据库管理员 tidb 的 open 文件数设置为 `1000000` |
| System Open File Limits | 对系统的 open 文件数设置为 `1000000` |
| User Process Limits | 在 `limits.conf` 配置的 tidb 用户的 nproc 为 `4096` |
| Address Space Limits | 在 `limits.conf` 配置的 tidb 用户空间为 `unlimited` |
| File Size Limits | 在 `limits.conf` 配置的 tidb 用户 fsize 为 `unlimited` |
| Disk Readahead | 设置数据磁盘 `readahead` 至少为 `4096` |
| NTP 服务 | 为各个节点配置 NTP 时间同步服务 |
| SELinux  | 关闭各个节点的 SELinux 服务  |
| CPU Frequency Scaling |  TiDB 推荐打开 CPU 超频 |
| Transparent Hugepages | 针对 Red Hat 7+ 和 CentOS 7+ 系统, Transparent Hugepages 必须被设置为 `always` |
| I/O Scheduler | 设置数据磁盘 I/0 Schedule 设置为 `deadline` 模式 |
| vm.swappiness | 设置 `vm.swappiness = 0` |

> 注意：请联系系统管理员进行操作系统参数调整。

### 数据库运行用户设置

| 配置 | 说明 |
| :-- | :---------------------------- |
| LANG 环境设定 | 设置 `LANG = en_US.UTF8` |
| TZ 时区设定 | 确保所有节点的时区 TZ 设置为一样的值 |

## 创建系统数据库运行账户

在 Linux 环境下，在每台安装节点上创建 tidb 作为数据库系统运行用户并设置集群节点之间的 ssh 互信访问。以下是一个示例，具体创建用户与开通 ssh 互信访问请联系系统管理员进行。

```bash
# useradd tidb
# usermod -a -G tidb tidb
# su - tidb
Last login: Tue Aug 22 12:06:23 CST 2017 on pts/2
-bash-4.2$ ssh-keygen -t rsa
Generating public/private rsa key pair.
Enter file in which to save the key (/home/tidb/.ssh/id_rsa):
Created directory '/home/tidb/.ssh'.
Enter passphrase (empty for no passphrase):
Enter same passphrase again:
Your identification has been saved in /home/tidb/.ssh/id_rsa.
Your public key has been saved in /home/tidb/.ssh/id_rsa.pub.
The key fingerprint is:
5a:00:e6:df:9e:40:25:2c:2d:e2:6e:ee:74:c6:c3:c1 tidb@t001
The key's randomart image is:
+--[ RSA 2048]----+
|    oo. .        |
|  .oo.oo         |
| . ..oo          |
|  .. o o         |
| .  E o S        |
|  oo . = .       |
| o. * . o        |
| ..o .           |
| ..              |
+-----------------+

-bash-4.2$ cd .ssh
-bash-4.2$ cat id_rsa.pub >> authorized_keys
-bash-4.2$ chmod 644 authorized_keys
-bash-4.2$ ssh-copy-id -i ~/.ssh/id_rsa.pub 192.168.1.100
```

## 下载官方 Binary

TiDB 官方提供了支持 Linux 版本的二进制安装包，官方推荐使用 Redhat 7+、CentOS 7+ 以上版本的操作系统，不推荐在 Redhat 6、CentOS 6 上部署 TiDB 集群。

### 操作系统：Linux ( Redhat 7+，CentOS 7+ )

执行步骤：

```
# 下载压缩包

wget http://download.pingcap.org/tidb-latest-linux-amd64.tar.gz
wget http://download.pingcap.org/tidb-latest-linux-amd64.sha256

# 检查文件完整性，返回 ok 则正确
sha256sum -c tidb-latest-linux-amd64.sha256

# 解开压缩包
tar -xzf tidb-latest-linux-amd64.tar.gz
cd tidb-latest-linux-amd64
```

## 单节点方式快速部署

在获取 TiDB 二进制文件包后，我们可以在单机上面，运行和测试 TiDB 集群，请按如下步骤依次启动 PD，TiKV，TiDB。

> 注意：以下启动各个应用程序组件实例的时候，请选择后台启动，避免前台失效后程序自动退出。

步骤一. 启动 PD：

```
./bin/pd-server --data-dir=pd \
                --log-file=pd.log
```

步骤二. 启动 TiKV：

```
./bin/tikv-server --pd="127.0.0.1:2379" \
                  --data-dir=tikv \
                  --log-file=tikv.log
```

步骤三. 启动 TiDB：

```
./bin/tidb-server --store=tikv \
                  --path="127.0.0.1:2379" \
                  --log-file=tidb.log
```

步骤四. 使用 MySQL 客户端连接 TiDB:

```
mysql -h 127.0.0.1 -P 4000 -u root -D test
```

## 功能性测试部署

如果只是对 TiDB 进行测试，并且机器数量有限，我们可以只启动一台 PD 测试整个集群。

这里我们使用四个节点，部署一个 PD，三个 TiKV，以及一个 TiDB，各个节点以及所运行服务信息如下：

| Name | Host IP | Services |
| :-- | :-- | :------------------- |
| node1 | 192.168.199.113 | PD1, TiDB |
| node2 | 192.168.199.114 | TiKV1 |
| node3 | 192.168.199.115 | TiKV2 |
| node4 | 192.168.199.116 | TiKV3 |

请按如下步骤依次启动 PD 集群，TiKV 集群以及 TiDB：

> 注意：以下启动各个应用程序组件实例的时候，请选择后台启动，避免前台失效后程序自动退出。

步骤一. 在 node1 启动 PD：

```
./bin/pd-server --name=pd1 \
                --data-dir=pd1 \
                --client-urls="http://192.168.199.113:2379" \
                --peer-urls="http://192.168.199.113:2380" \
                --initial-cluster="pd1=http://192.168.199.113:2380" \
                --log-file=pd.log
```

步骤二. 在 node2，node3，node4 启动 TiKV：

```
./bin/tikv-server --pd="192.168.199.113:2379" \
                  --addr="192.168.199.114:20160" \
                  --data-dir=tikv1 \
                  --log-file=tikv.log

./bin/tikv-server --pd="192.168.199.113:2379" \
                  --addr="192.168.199.115:20160" \
                  --data-dir=tikv2 \
                  --log-file=tikv.log

./bin/tikv-server --pd="192.168.199.113:2379" \
                  --addr="192.168.199.116:20160" \
                  --data-dir=tikv3 \
                  --log-file=tikv.log
```

步骤三. 在 node1 启动 TiDB：

```
./bin/tidb-server --store=tikv \
                  --path="192.168.199.113:2379" \
                  --log-file=tidb.log
```

步骤四. 使用 MySQL 客户端连接 TiDB：

```
mysql -h 192.168.199.113 -P 4000 -u root -D test
```

## 多节点集群模式部署

在生产环境中，我们推荐多节点部署 TiDB 集群，首先请参考部署建议。

这里我们使用六个节点，部署三个 PD，三个 TiKV，以及一个 TiDB，各个节点以及所运行服务信息如下：

| Name  | Host IP | Services |
| :-- | :-- | :------------------- |
| node1 | 192.168.199.113| PD1, TiDB |
| node2 | 192.168.199.114| PD2 |
| node3 | 192.168.199.115| PD3 |
| node4 | 192.168.199.116| TiKV1 |
| node5 | 192.168.199.117| TiKV2 |
| node6 | 192.168.199.118| TiKV3 |

请按如下步骤依次启动 PD 集群，TiKV 集群以及 TiDB：

步骤一 . 在 node1，node2，node3 依次启动 PD：

```
./bin/pd-server --name=pd1 \
                --data-dir=pd1 \
                --client-urls="http://192.168.199.113:2379" \
                --peer-urls="http://192.168.199.113:2380" \
                --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                -L "info" \
                --log-file=pd.log

./bin/pd-server --name=pd2 \
                --data-dir=pd2 \
                --client-urls="http://192.168.199.114:2379" \
                --peer-urls="http://192.168.199.114:2380" \
                --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                --join="http://192.168.199.113:2379" \
                -L "info" \
                --log-file=pd.log

./bin/pd-server --name=pd3 \
                --data-dir=pd3 \
                --client-urls="http://192.168.199.115:2379" \
                --peer-urls="http://192.168.199.115:2380" \
                --initial-cluster="pd1=http://192.168.199.113:2380,pd2=http://192.168.199.114:2380,pd3=http://192.168.199.115:2380" \
                --join="http://192.168.199.113:2379" \
                -L "info" \
                --log-file=pd.log
```

步骤二. 在 node4，node5，node6 启动 TiKV：

```
./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                  --addr="192.168.199.116:20160" \
                  --data-dir=tikv1 \
                  --log-file=tikv.log

./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                  --addr="192.168.199.117:20160" \
                  --data-dir=tikv2 \
                  --log-file=tikv.log

./bin/tikv-server --pd="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                  --addr="192.168.199.118:20160" \
                  --data-dir=tikv3 \
                  --log-file=tikv.log
```

步骤三. 在 node1 启动 TiDB：

```
./bin/tidb-server --store=tikv \
                  --path="192.168.199.113:2379,192.168.199.114:2379,192.168.199.115:2379" \
                  --log-file=tidb.log

```

步骤四. 使用 MySQL 客户端连接 TiDB：

```
mysql -h 192.168.199.113 -P 4000 -u root -D test
```

> 注意：在生产环境中启动 TiKV 时，建议使用 `--config` 参数指定配置文件路径，如果不设置这个参数，TiKV 不会读取配置文件。同样，在生产环境中部署 PD 时，也建议使用 `--config` 参数指定配置文件路径。

TiKV 调优参见：[TiKV 性能参数调优](https://github.com/pingcap/docs-cn/blob/master/op-guide/tune-tikv.md)。

> 注意：如果使用 nohup 在生产环境中启动集群，需要将启动命令放到一个脚本文件里面执行，否则会出现因为 Shell 退出导致 nohup 启动的进程也收到异常信号退出的问题，具体参考进程异常退出。

## TiDB 监控和告警环境安装

安装部署监控和告警环境的系统信息如下：

| Name  | Host IP | Services |
| :-- | :-- | :------------- |
| node1 | 192.168.199.113 | node_export, pushgateway, Prometheus, Grafana |
| node2 | 192.168.199.114 | node_export |
| node3 | 192.168.199.115 | node_export |
| node4 | 192.168.199.116 | node_export |

### 获取二进制包

```
# 下载压缩包
wget https://github.com/prometheus/prometheus/releases/download/v1.5.2/prometheus-1.5.2.linux-amd64.tar.gz
wget https://github.com/prometheus/node_exporter/releases/download/v0.14.0-rc.2/node_exporter-0.14.0-rc.2.linux-amd64.tar.gz
wget https://grafanarel.s3.amazonaws.com/builds/grafana-4.1.2-1486989747.linux-x64.tar.gz
wget https://github.com/prometheus/pushgateway/releases/download/v0.3.1/pushgateway-0.3.1.linux-amd64.tar.gz

# 解开压缩包
tar -xzf prometheus-1.5.2.linux-amd64.tar.gz
tar -xzf node_exporter-0.14.0-rc.1.linux-amd64.tar.gz
tar -xzf grafana-4.1.2-1486989747.linux-x64.tar.gz
tar -xzf pushgateway-0.3.1.linux-amd64.tar.gz
```

### 启动监控服务

### 在 node1，node2，node3，node4 启动 `node_exporter`

```
$cd node_exporter-0.14.0-rc.1.linux-amd64

#启动 node_exporter 服务
./node_exporter --web.listen-address=":9100" \
    --log.level="info"
```

### 在 node1 启动 pushgateway

```
$cd pushgateway-0.3.1.linux-amd64

#启动 pushgateway 服务
./pushgateway \
    --log.level="info" \
    --web.listen-address=":9091"
```

### 在 node1 启动 Prometheus

```
$cd prometheus-1.5.2.linux-amd64

# 修改配置文件

vi prometheus.yml

...
global:
  scrape_interval:     15s # By default, scrape targets every 15 seconds.
  evaluation_interval: 15s # By default, scrape targets every 15 seconds.
  # scrape_timeout is set to the global default (10s).
  labels:
    cluster: 'test-cluster'
    monitor: "prometheus"

scrape_configs:
  - job_name: 'overwritten-cluster'
    scrape_interval: 3s
    honor_labels: true # don't overwrite job & instance labels
    static_configs:
      - targets: ['192.168.199.113:9091']

  - job_name: "overwritten-nodes"
    honor_labels: true # don't overwrite job & instance labels
    static_configs:
    - targets:
      - '192.168.199.113:9100'
      - '192.168.199.114:9100'
      - '192.168.199.115:9100'
      - '192.168.199.116:9100'
...

# 启动 Prometheus:
./prometheus \
    --config.file="/data1/tidb/deploy/conf/prometheus.yml" \
    --web.listen-address=":9090" \
    --web.external-url="http://192.168.199.113:9090/" \
    --log.level="info" \
    --storage.local.path="/data1/tidb/deploy/data.metrics" \
    --storage.local.retention="360h0m0s"
```

### 在 node1 启动 Grafana

```
cd grafana-4.1.2-1486989747.linux-x64

#编辑配置文件

vi grafana.ini

...

# The http port  to use
http_port = 3000

# The public facing domain name used to access grafana from a browser
domain = 192.168.199.113

...

#启动 Grafana 服务
./grafana-server \
    --homepath="/data1/tidb/deploy/opt/grafana" \
    --config="/data1/tidb/deploy/opt/grafana/conf/grafana.ini"
```
