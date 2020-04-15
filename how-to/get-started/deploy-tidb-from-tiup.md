---
title: 如何快速体验 TiDB 集群
category: how-to
---

# 如何快速体验 TiDB 集群

本文档介绍如何快速地体验 TiDB 分布式数据库。有以下 3 种体验方式供用户选择。

- 第一种：使用 TiDB-Wasm 一键体验 TiDB 数据库
- 第二种：使用 TiUP Playground 快速部署本地测试环境
- 第三种：使用 TiUP Cluster 模拟单机下的准生产测试环境

> **警告：**
>
> 对于生产环境，不要使用本文介绍的方式进行部署，而应使用 [TiUP 部署 TiDB 集群](/how-to/deploy/orchestrated/tiup.md)。

## 第一种：使用 TiDB-Wasm 一键体验 TiDB 数据库

- 适用场景：初步极速体验 TiDB 数据库的语法、兼容性等基本功能
- 耗时：即时体验

TiDB-Wasm 是运行在浏览器中的 TiDB 数据库，打开网页即可使用。TiDB-Wasm 可直接进行 SQL 执行、兼容性验证等基本功能。

试用请点击网址：[https://tour.pingcap.com](https://tour.pingcap.com)，之后会在内存中构建 TiDB 数据库，预计消耗 10s 左右时间。

## 第二种：使用 TiUP Playground 快速部署本地测试环境

- 适用场景：利用本地 Mac 或者单机 Linux 环境快速部署 TiDB 集群。可以体验 TiDB 集群的基本架构，以及 TiDB、TiKV、PD、监控等基础组件的运行。
- 耗时：1 分钟

作为一个分布式系统，最基础的 TiDB 测试集群通常由 2 个 TiDB 组件、3 个 TiKV 组件和 3 个 PD 组件来构成。通过 TiUP Playground，可以快速搭建出上述的一套基础测试集群。

1. 下载并安装 TiUP

{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

2. 声明全局环境变量

> **建议：** TiUP 安装完成会提示对应的 profile 文件的绝对路径，source 操作请根据实际位置进行操作。

{{< copyable "shell-regular" >}}

```shell
source .bash_profile
``` 

3. 安装 Playground
  
{{< copyable "shell-regular" >}}

```shell
tiup install playground
``` 
  
- 如果曾经安装过，请升级至最新版
  
{{< copyable "shell-regular" >}}

```shell
tiup update playground
```

4. 在当前 session 启动集群

- 直接运行 tiup playground 会运行最新版本的 TiDB 集群，其中组件 tidb/tikv/pd 各 1 个。

{{< copyable "shell-regular" >}}

```shell
tiup playground
```

- 也可以指定版本以及组件个数

{{< copyable "shell-regular" >}}

```shell
tiup playground v4.0.0-rc --db 2 --pd 3 --kv 3 --monitor
```

会在本地下载并启动一个 v4.0.0-rc 版本的集群，--monitor 表示带监控。运行结果将显示集群的访问方式：

```log
CLUSTER START SUCCESSFULLY, Enjoy it ^-^
To connect TiDB: mysql --host 127.0.0.1 --port 4000 -u root
To connect TiDB: mysql --host 127.0.0.1 --port 4001 -u root
To view the dashboard: http://127.0.0.1:2379/dashboard
To view the monitor: http://127.0.0.1:9090
```

5. 新开启 session 访问 TiDB 数据库

{{< copyable "shell-regular" >}}

```shell
mysql --host 127.0.0.1 --port 4000 -u root
```

6. 访问 TiDB 的 Prometheus 管理界面：http://127.0.0.1:9090

7. 访问 TiDB 的 Dashboard 页面：http://127.0.0.1:2379/dashboard 默认用户名 root 密码为空。

8. 测试完成，清理集群，绿色环保。通过 `ctrl-c` 停掉进程后，执行 

{{< copyable "shell-regular" >}}

```shell
tiup clean --all
```

## 第三种：使用  TiUP Cluster 模拟单机下的准生产测试环境

- 适用场景：希望用单台 Linux  服务器，体验 TiDB 最小的完整拓扑的集群，并模拟生产的部署步骤。
- 耗时：10 分钟

本文档介绍如何参照 TiUP 最小拓扑 的一个 YAML 文件部署 TiDB 集群。

### 准备环境

准备一台部署主机，确保其软件满足需求：

- 推荐安装 CentOS 7.3 及以上版本 
- Linux 操作系统开放外网访问，用于下载 TiDB 及相关软件安装包

最小规模的 TiDB 集群拓扑

| 实例 | 个数 | IP | 配置 |
|:-- | :-- | :-- | :-- |
| TiKV | 3 | 10.0.1.1 <br> 10.0.1.1 <br> 10.0.1.1 | 避免端口和目录冲突 |
| TiDB | 1 | 10.0.1.1 | 默认端口 <br> 全局目录配置 |
| PD | 1 | 10.0.1.1 | 默认端口 <br> 全局目录配置 |
| TiFlash | 1 | 10.0.1.1 | 默认端口 <br> 全局目录配置 |
| Monitor | 1 | 10.0.1.1 | 默认端口 <br> 全局目录配置 |

部署主机软件和环境要求

- 部署需要使用部署主机的 root 用户及密码
- 部署主机关闭防火墙或者开放 TiDB 集群的节点间所需端口
- 目前 TiUP 仅支持在 x86_64 (AMD64) 架构上部署 TiDB 集群（TiUP 将在 4.0 GA 时支持在 ARM 架构上部署）
    - 在 AMD64 架构下，建议使用 CentOS 7.3 及以上版本 Linux 操作系统
    - 在 ARM 架构下，建议使用 CentOS 7.6 1810 版本 Linux 操作系操作步骤：

### 实施部署

1. 以下步骤使用 linux 系统的任一普通用户或 root 用户，以 root 用户为例

2. 下载并安装 TiUP


{{< copyable "shell-regular" >}}

```shell
curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
```

3. 安装 TiUP 的 cluster 组件

{{< copyable "shell-regular" >}}

```shell
tiup cluster
```

4. 如果已经安装 TiUP cluster 的机器更新软件版本

{{< copyable "shell-regular" >}}

```shell
tiup update cluster
```

5. 由于模拟多机部署，需要通过 `root` 用户调大 sshd 服务的连接数限制

- 修改 /etc/ssh/sshd_config 将 `MaxSessions` 调至 20
- 重启 sshd 服务 

{{< copyable "shell-regular" >}}

```shell
service sshd restart
```

6. 创建并启动集群

- 按下面的配置模板，编辑配置文件，命名为 topo.yaml ，其中：

  - `user: "tidb"` 表示通过 tidb 系统用户来做集群的内部管理（部署会自动创建），默认使用 22 端口通过 ssh 登陆目标机器

  - 设置 PD 参数 `replication.enable-placement-rules` 参数来确保 TiFlash 正常运行。

  - host 改为本部署主机的 IP

{{< copyable "shell-regular" >}}

```yaml
# # Global variables are applied to all deployments and as the default value of
# # them if the specific deployment value missing.
 
global:
 user: "tidb"
 ssh_port: 22
 deploy_dir: "/tidb-deploy"
 data_dir: "/tidb-data"
 
# # Monitored variables are used to all the machine
monitored:
 node_exporter_port: 9100
 blackbox_exporter_port: 9115
 
server_configs:
 tidb:
   log.slow-threshold: 300
 tikv:
   readpool.storage.use-unified-pool: true
   readpool.coprocessor.use-unified-pool: true
 pd:
   replication.enable-placement-rules: true
 tiflash:
   logger.level: "info"
 
pd_servers:
 - host: 10.0.1.1
 
tidb_servers:
 - host: 10.0.1.1
 
tikv_servers:
 - host: 10.0.1.1
   port: 20160
   status_port: 20180
 
 - host: 10.0.1.1
   port: 20161
   status_port: 20181
 
 - host: 10.0.1.1
   port: 20162
   status_port: 20182
 
tiflash_servers:
 - host: 10.0.1.1
 
monitoring_servers:
 - host: 10.0.1.1
 
grafana_servers:
 - host: 10.0.1.1
```

7. 执行部署集群

{{< copyable "shell-regular" >}}

```shell
tiup cluster deploy <cluster-name> <tidb-version> ./topo.yaml --user root 
```

- 参数 `<cluster-name>` 表示设置集群名称
- 参数 `<tidb-version>` 表示设置集群版本，可以通过 tiup list tidb --refresh 命令来选择当前支持部署的 TiDB 版本。

按照引导，输入”y” 及 root 密码，来完成部署

```log
Do you want to continue? [y/N]:  y
Input SSH password:
```

8. 启动集群

{{< copyable "shell-regular" >}}

```shell
tiup cluster start <cluster-name>
```

9. 访问集群

- 访问 TiDB 数据库，密码为空

  {{< copyable "shell-regular" >}}
  
  ```shell
  mysql -h 10.0.1.1 -P 4000 -u root
  ```

- 访问 TiDB 的 Grafana 监控

  访问集群 Grafana 监控页面：http://{grafana-ip}:3000 默认用户名和密码均为 admin。

- 访问 TiDB 的 Dashboard

  访问集群 TiDB-Dashboard 监控页面：http://{pd-ip}:2379/dashboard 默认用户名 root 密码为空。

- 通过 `tiup cluster list` 命令来确认当前已经部署的集群列表

  {{< copyable "shell-regular" >}}
  
  ```shell
  tiup cluster list
  ```

- `tiup cluster display <cluster-name>` 来查看集群的拓扑结构和状态

  {{< copyable "shell-regular" >}}
  
  ```shell
  tiup cluster display <cluster-name>
  ```
