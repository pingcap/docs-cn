---
title: 新版 TiDB-Binlog 部署方案
category: advanced
---

# 新版 TiDB-Binlog 部署方案

> 新版 TiDB-Binlog 尚未发布正式版，本文档用于测试环境部署。

## 使用 tidb-ansible 部署 TiDB-Binlog 
### 下载 tidb-ansible

以 tidb 用户登录中控机并进入 `/home/tidb` 目录，使用以下命令 tidb-ansible `new-tidb-binlog` 分支，默认的文件夹名称为 tidb-ansible。

```
$ git clone -b new-tidb-binlog https://github.com/pingcap/tidb-ansible.git
```

### 部署 pump
#### 修改 tidb-ansible/inventory.ini 文件

1. 设置 `enable_binlog = True`，表示 TiDB 集群开启 binlog。

```
## binlog trigger
enable_binlog = True
```

2. 为 `pump_servers` 主机组添加部署机器 IP。

```
## Binlog Part
[pump_servers]
172.16.10.72
172.16.10.73
172.16.10.74
```

默认 pump 保留 5 天数据，如需修改可修改 `tidb-ansible/conf/pump.yml` 文件中 `gc` 变量值，并取消注释，如修改为 7。

```
global:
  # a integer value to control expiry date of the binlog data, indicates for how long (in days) the binlog data would be stored. 
  # must bigger than 0
  gc: 7
```

请确保部署目录有足够空间存储 binlog，详见：[部署目录调整](../op-guide/ansible-deployment.md#部署目录调整)，也可为 pump 设置单独的部署目录。

```
## Binlog Part
[pump_servers]
pump1 ansible_host=172.16.10.72 deploy_dir=/data1/pump
pump2 ansible_host=172.16.10.73 deploy_dir=/data1/pump
pump3 ansible_host=172.16.10.74 deploy_dir=/data1/pump
```

#### 部署并启动 TiDB 集群。

使用 ansible 部署 TiDB 集群的具体方法参考 [TiDB Ansible 部署方案](../op-guide/ansible-deployment.md)，开启 binlog 后默认会部署和启动 pump 服务。

#### 查看 pump 服务状态

使用 binlogctl 查看 pump 服务状态，pd-urls 参数请替换为集群 PD 地址，结果 State 为 online 表示 pump 启动成功。

```
$ cd /home/tidb/tidb-ansible
$ resources/bin/binlogctl -pd-urls=http://172.16.10.72:2379 -cmd pumps
2018/09/21 16:45:54 nodes.go:46: [info] pump: &{NodeID:ip-172-16-10-72:8250 Addr:172.16.10.72:8250 State:online IsAlive:false Score:0 Label:<nil> MaxCommitTS:0 UpdateTS:403051525690884099}
2018/09/21 16:45:54 nodes.go:46: [info] pump: &{NodeID:ip-172-16-10-73:8250 Addr:172.16.10.73:8250 State:online IsAlive:false Score:0 Label:<nil> MaxCommitTS:0 UpdateTS:403051525703991299}
2018/09/21 16:45:54 nodes.go:46: [info] pump: &{NodeID:ip-172-16-10-74:8250 Addr:172.16.10.74:8250 State:online IsAlive:false Score:0 Label:<nil> MaxCommitTS:0 UpdateTS:403051525717360643}
```

### 部署 drainer
#### 获取 initial_commit_ts

#### 修改 tidb-ansible/inventory.ini 文件

为 `drainer_servers` 主机组添加部署机器 IP，initial_commit_ts 请设置为获取的 initial_commit_ts，仅用于 drainer 第一次启动。

1. 以下游为 mysql 为例，别名为 `drainer_mysql`。

```
[drainer_servers]
drainer_mysql ansible_host=172.16.10.71 initial_commit_ts="402899541671542785"
```

2. 以下游为 pb 为例，别名为 `drainer_pb`。

```
[drainer_servers]
drainer_pb ansible_host=172.16.10.71 initial_commit_ts="402899541671542785"
```

#### 修改配置文件

1. 以下游为 mysql 为例

```
$ cd /home/tidb/tidb-ansible/conf
$ cp drainer.toml drainer_mysql_drainer.toml
$ vi drainer_mysql_drainer.toml
```

db-type 设置为 "mysql", 配置下游 mysql 信息。

```
# downstream storage, equal to --dest-db-type
# valid values are "mysql", "pb", "tidb", "flash", "kafka"
db-type = "mysql"

# the downstream mysql protocol database
[syncer.to]
host = "172.16.10.72"
user = "root"
password = "123456"
port = 3306
# Time and size limits for flash batch write
# time-limit = "30s"
# size-limit = "100000"
```

2. 以下游为 pd 为例

```
$ cd /home/tidb/tidb-ansible/conf
$ cp drainer.toml drainer_pd_drainer.toml
$ vi drainer_pd_drainer.toml
```

db-type 设置为 "pd"。

```
# downstream storage, equal to --dest-db-type
# valid values are "mysql", "pb", "tidb", "flash", "kafka"
db-type = "pd"

# Uncomment this if you want to use pb or sql as db-type.
# Compress compresses output file, like pb and sql file. Now it supports "gzip" algorithm only. 
# Values can be "gzip". Leave it empty to disable compression. 
[syncer.to]
compression = ""
```

#### 部署 drainer

```
$ ansible-playbook deploy_drainer.yml
```

#### 启动 drainer

```
$ ansible-playbook start_drainer.yml
```
