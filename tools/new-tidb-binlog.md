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

### 修改 tidb-ansible/inventory.ini 文件

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

请确保部署目录有足够空间存储 binlog，也可为 pump 设置单独的部署目录，详见：[部署目录调整](../op-guide/ansible-deployment.md#部署目录调整)

```
## Binlog Part
[pump_servers]
pump1 ansible_host=172.16.10.72 deploy_dir=/data1/pump
pump2 ansible_host=172.16.10.73 deploy_dir=/data1/pump
pump3 ansible_host=172.16.10.74 deploy_dir=/data1/pump
```

3. 部署并启动 TiDB 集群。

使用 ansible 部署 TiDB 集群的具体方法参考 [TiDB Ansible 部署方案](../op-guide/ansible-deployment.md)

