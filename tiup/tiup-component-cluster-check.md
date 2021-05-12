---
title: tiup cluster check
---

# tiup cluster check

对于严肃的生产环境，在正式上线之前需要进行一系列检查，来确保集群拥有最好的表现。为了简化人工检查的步骤，TiUP Cluster 提供了 `check` 子命令，用于检查指定集群的机器硬件和软件环境是否满足正常运行条件。

## 检查项列表

### 操作系统版本

检查部署机操作系统发行版和版本：目前仅支持部署在 CentOS 7 的操作系统上，之后随兼容性改进可能支持更多系统版本。

### CPU EPOLLEXCLUSIVE

检查部署机 CPU 是否支持 EPOLLEXCLUSIVE。

### numactl

检查部署机是否安装 numactl，若用户配置绑核，则必须安装 numactl。

### 系统时间

检查部署器系统时间是否同步：将部署机系统时间与中控机对比，偏差超出某一阈值（500ms）后报错。

### 时间同步服务

检查部署机是否配置了时间同步服务：即 ntpd 是否在运行

### Swap 分区

检查部署机是否启用 Swap 分区：建议禁用 Swap 分区

### 内核参数

检查各项内核参数的值：

- net.ipv4.tcp_tw_recycle: 0
- net.ipv4.tcp_syncookies: 0
- net.core.somaxconn: 32768
- vm.swappiness: 0
- vm.overcommit_memory: 0 或 1
- fs.file-max: 1000000

### THP（透明大页）

检查部署机是否启用透明大页：建议禁用透明大页。

### 系统限制

检查 /etc/security/limits.conf 中各项 limit 值：

```
<deploy-user>    soft   nofile    1000000
<deploy-user>    hard   nofile    1000000
<deploy-user>    soft   stack     10240
```

其中 `<deploy-user>` 为部署、运行 TiDB 集群的用户，最后一列的数值为要求达到的最小值。

### SELinux

检查 SELinux 是否启用：建议用户禁用 SELinux。

### 防火墙

检查 FirewallD 服务是否启用：建议用户禁用 FirewallD 或为 TiDB 集群各服务添加允许规则。

### irqbalance

检查 irqbalance 服务是否启用：建议用户启用 irqbalance 服务。

### 磁盘挂载参数

检查 ext4 分区的挂载参数：确保挂载参数包含 nodelalloc,noatime 选项。

### 端口占用

检查部署机上是否已有进程占用了端口：检查拓扑中定义的端口（包括自动补全的默认端口）在部署机上是否已被占用。

> **注意：**
>
> 端口占用检查假设集群尚未启动，如果检查的是已经部署并启动的集群，那么端口占用检查一定会失败，因为端口确实被占用了。

### CPU 核心数

检查部署机 CPU 信息：建议生产集群 CPU 逻辑核心数 >= 16

> **注意：**
>
> 默认不检查 CPU 核心数，需要通过选项 `--enable-cpu` 启用。

### 内存大小

检查部署机的内存大小：建议生产集群总内存容量 >= 32Gb。

> **注意：**
>
> 默认不检查内存大小，需要通过选项 `--enable-mem` 启用。

### fio 磁盘性能测试

使用 fio 测试 data_dir 所在磁盘的性能，包括三个测试项目：

- fio_randread_write_latency
- fio_randread_write
- fio_randread

> **注意：**
>
> 默认不进行 fio 磁盘性能测试，需要通过选项 `--enable-disk` 启用。

## 语法

```shell
tiup cluster check <topology.yml | cluster-name> [flags]
```

若集群尚未部署，需要传递将用于部署集群的 [topology.yml](/tiup/tiup-cluster-topology-reference.md) 文件，tiup-cluster 会根据该文件的内容连接到对应机器去检查。若集群已经部署，则可以使用集群的名字 `<cluster-name>` 作为检查对象。

> **注意：**
>
> 若传递的是集群名字，则需要配合 `--cluster` 选项使用。

## 选项

### --apply

- 尝试自动修复失败的检查项，目前仅会尝试修复以下项目：

    - SELinux
    - 防火墙
    - irqbalance
    - 内核参数
    - 系统 Limits
    - THP（透明大页）

- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --cluster

tiup-cluster 支持对未部署的集群进行检查，也支持对已部署的集群进行检查，命令格式：

```shell
tiup cluster check <topology.yml | cluster-name> [flags]
```

若选择的格式为 `tiup cluster check <cluster-name>` 则必须加上该选项：`tiup cluster check <cluster-name> --cluster`。

该选项的数据类型为 `BOOLEAN`。该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -N, --node

- 指定要检查的节点。该选项的值为以逗号分割的节点 ID 列表，节点 ID 为 [`tiup-component-cluster-display`](/tiup/tiup-component-cluster-display.md) 命令返回的集群状态表格的第一列。
- 数据类型：`STRINGS`
- 如果不指定该选项，默认检查所有节点，即 `[]`。

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将检查它们的交集中的服务。

### -R, --role

- 指定要检查的角色。该选项的值为以逗号分割的节点角色列表，角色为 [`tiup-component-cluster-display`](/tiup/tiup-component-cluster-display.md) 命令返回的集群状态表格的第二列。
- 数据类型：`STRINGS`
- 如果不指定该选项，默认检查所有角色。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将检查它们的交集中的服务。

### --enable-cpu

- 默认情况下 tiup-cluster 不检查 CPU 核心数，该选项用于启用 CPU 核心数检查。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --enable-disk

- 默认情况下 tiup-cluster 不进行 fio 磁盘性能测试，该选项用于启用 fio 磁盘性能测试。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --enable-mem

默认情况下 tiup-cluster 不检查内存大小，该选项用于启用内存大小检查。

### -u, --user（string，默认为当前执行命令的用户）

指定连接目标机器的用户名，该用户在目标机器上需要有免密 sudo root 的权限。

> **注意：**
>
> 仅当 `--cluster` 选项为 false 时该选项有效，否则该值固定为部署集群时拓扑文件中指定的用户名。

### -i, --identity_file（string，默认 ~/.ssh/id_rsa）

指定连接目标机器的密钥文件。

> **注意：**
>
> 仅当 `--cluster` 选项为 false 时该选项有效，否则该值固定为 `${TIUP_HOME}/storage/cluster/clusters/<cluster-name>/ssh/id_rsa`

### -p, --password

- 在连接目标机器时使用密码登陆：

    - 对于指定了 `--cluster` 的集群，密码为部署集群时拓扑文件中指定的用户的密码
    - 对于未指定 `--cluster` 的集群，密码为 `-u/--user` 参数指定的用户的密码

- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

输出含有以下字段的表格：

- Node：目标节点
- Check：检查项
- Result：检查结果（Pass/Warn/Fail）
- Message：结果描述

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)