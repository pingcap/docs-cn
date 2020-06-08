---
title: 使用 TiUP 离线部署 TiDB 集群
category: how-to
---

# 使用 TiUP 离线部署 TiDB 集群

本文介绍如何使用 TiUP 离线部署 TiDB 集群，具体的操作步骤如下。

## 1. 准备 TiUP 离线组件包

### 方式一：下载官方 TiUP 离线组件包

在 `download.pingcap.org` 有官方预先打好的离线镜像包，下载指令为：

{{< copyable "shell-regular" >}}

```shell
wget http://download.pingcap.org/tidb-community-server-${version}-linux-amd64.tar.gz
mv tidb-community-server-${version}-linux-amd64.tar.gz package.tar.gz
```

其中 ${version} 处填入希望下载的离线镜像包版本，例如 v4.0.0。

此时，`package.tar.gz` 就是一个独立的离线环境包。

### 方式二：使用 `tiup mirror clone` 命令手动打包离线组件包

#### 1.1 部署在线环境 TiUP 组件

使用普通用户登录一台开放外网访问的机器：

1. 执行如下命令安装 TiUP 工具：

    {{< copyable "shell-regular" >}}

    ```shell
    curl --proto '=https' --tlsv1.2 -sSf https://tiup-mirrors.pingcap.com/install.sh | sh
    ```

2. 重新声明全局环境变量：

    {{< copyable "shell-regular" >}}

    ```shell
    source .bash_profile
    ```

3. 确认 TiUP 工具是否安装：

    {{< copyable "shell-regular" >}}

    ```shell
    which tiup
    ```

#### 1.2 使用 TiUP 拉取镜像

以 tidb 用户在隔离的环境中安装一个 v4.0.0 的 TiDB 集群为例，可以执行以下步骤：

1. 在一台和外网相通的机器上拉取需要的组件：

    {{< copyable "shell-regular" >}}

    ```bash
    tiup mirror clone package v4.0.0 --os=linux --arch=amd64
    ```

    该命令会在当前目录下创建一个名叫 `package` 的目录，里面有启动一个集群必要的组件包。

2. 通过 tar 命令将该组件包打包然后发送到隔离环境的中控机：

    {{< copyable "shell-regular" >}}

    ```bash
    tar czvf package.tar.gz package
    ```

    此时，`package.tar.gz` 就是一个独立的离线环境包。

## 2. 部署离线环境 TiUP 组件

将包发送到目标集群的中控机后，执行以下命令安装 TiUP 组件：

{{< copyable "shell-regular" >}}

```bash
tar xzvf package.tar.gz &&
cd package &&
sh local_install.sh &&
source /home/tidb/.bash_profile
```

## 3. TiKV 数据盘挂载

> **注意：**
>
> 推荐 TiKV 部署目标机器的数据目录使用 EXT4 文件系统格式。相比于 XFS 文件系统格式，EXT4 文件系统格式在 TiDB 集群部署案例较多，生产环境优先选择使用 EXT4 文件系统格式。

使用 `root` 用户登录目标机器，将部署目标机器数据盘格式化成 ext4 文件系统，挂载时添加 `nodelalloc` 和 `noatime` 挂载参数。`nodelalloc` 是必选参数，否则 TiUP 安装时检测无法通过；`noatime` 是可选建议参数。

> **注意：**
>
> 如果你的数据盘已经格式化成 ext4 并挂载了磁盘，可先执行 `umount /dev/nvme0n1p1` 命令卸载，从编辑 `/etc/fstab` 文件步骤开始执行，添加挂载参数重新挂载即可。

以 `/dev/nvme0n1` 数据盘为例，具体操作步骤如下：

1. 查看数据盘。

    {{< copyable "shell-root" >}}

    ```bash
    fdisk -l
    ```

    ```
    Disk /dev/nvme0n1: 1000 GB
    ```

2. 创建分区表。

    {{< copyable "shell-root" >}}

    ```bash
    parted -s -a optimal /dev/nvme0n1 mklabel gpt -- mkpart primary ext4 1 -1
    ```

    > **注意：**
    >
    > 使用 `lsblk` 命令查看分区的设备号：对于 nvme 磁盘，生成的分区设备号一般为 `nvme0n1p1`；对于普通磁盘（例如 `/dev/sdb`），生成的的分区设备号一般为 `sdb1`。

3. 格式化文件系统。

    {{< copyable "shell-root" >}}

    ```bash
    mkfs.ext4 /dev/nvme0n1p1
    ```

4. 查看数据盘分区 UUID。

    本例中 `nvme0n1p1` 的 UUID 为 `c51eb23b-195c-4061-92a9-3fad812cc12f`。

    {{< copyable "shell-root" >}}

    ```bash
    lsblk -f
    ```

    ```
    NAME    FSTYPE LABEL UUID                                 MOUNTPOINT
    sda
    ├─sda1  ext4         237b634b-a565-477b-8371-6dff0c41f5ab /boot
    ├─sda2  swap         f414c5c0-f823-4bb1-8fdf-e531173a72ed
    └─sda3  ext4         547909c1-398d-4696-94c6-03e43e317b60 /
    sr0
    nvme0n1
    └─nvme0n1p1 ext4         c51eb23b-195c-4061-92a9-3fad812cc12f
    ```

5. 编辑 `/etc/fstab` 文件，添加 `nodelalloc` 挂载参数。

    {{< copyable "shell-root" >}}

    ```bash
    vi /etc/fstab
    ```

    ```
    UUID=c51eb23b-195c-4061-92a9-3fad812cc12f /data1 ext4 defaults,nodelalloc,noatime 0 2
    ```

6. 挂载数据盘。

    {{< copyable "shell-root" >}}

    ```bash
    mkdir /data1 && \
    mount -a
    ```

7. 执行以下命令，如果文件系统为 ext4，并且挂载参数中包含 `nodelalloc`，则表示已生效。

    {{< copyable "shell-root" >}}

    ```bash
    mount -t ext4
    ```

    ```
    /dev/nvme0n1p1 on /data1 type ext4 (rw,noatime,nodelalloc,data=ordered)
    ```

## 4. 配置初始化参数文件 `topology.yaml`

集群初始化配置文件需要手动编写，完整的全配置参数模版可以参考 [Github TiUP 项目配置参数模版](https://github.com/pingcap/tiup/blob/master/examples/topology.example.yaml)。需要在中控机上面创建 YAML 格式配置文件，例如 `topology.yaml`:

{{< copyable "shell-regular" >}}

```shell
cat topology.yaml
```

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global:
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/tidb-deploy"
  data_dir: "/tidb-data"

server_configs:
  pd:
    replication.enable-placement-rules: true

pd_servers:
  - host: 10.0.1.4
  - host: 10.0.1.5
  - host: 10.0.1.6
tidb_servers:
  - host: 10.0.1.7
  - host: 10.0.1.8
  - host: 10.0.1.9
tikv_servers:
  - host: 10.0.1.1
  - host: 10.0.1.2
  - host: 10.0.1.3
tiflash_servers:
  - host: 10.0.1.10
    data_dir: /data1/tiflash/data,/data2/tiflash/data
cdc_servers:
  - host: 10.0.1.6
  - host: 10.0.1.7
  - host: 10.0.1.8
monitoring_servers:
  - host: 10.0.1.4
grafana_servers:
  - host: 10.0.1.4
alertmanager_servers:
  - host: 10.0.1.4
```

## 5. 部署 TiDB 集群

`/path/to/mirror` 是执行 `local_install.sh` 命令时输出的离线镜像包的位置:

{{< copyable "shell-regular" >}}

```bash
export TIUP_MIRRORS=/path/to/mirror &&
tiup cluster deploy tidb-test v4.0.0 topology.yaml --user tidb [-p] [-i /home/root/.ssh/gcp_rsa] &&
tiup cluster start tidb-test
```

> **参数说明：**
>
> - 通过 TiUP cluster 部署的集群名称为 `tidb-test`
> - 部署版本为 `v4.0.0`，其他版本可以执行 `tiup list tidb` 获取
> - 初始化配置文件为 `topology.yaml`
> - --user tidb：通过 tidb 用户登录到目标主机完成集群部署，该用户需要有 ssh 到目标机器的权限，并且在目标机器有 sudo 权限。也可以用其他有 ssh 和 sudo 权限的用户完成部署。
> - [-i] 及 [-p]：非必选项，如果已经配置免密登陆目标机，则不需填写。否则选择其一即可，[-i] 为可登录到部署机 root 用户（或 --user 指定的其他用户）的私钥，也可使用 [-p] 交互式输入该用户的密码

预期日志结尾输出会有 ```Deployed cluster `tidb-test` successfully``` 关键词，表示部署成功。

部署完成后，集群相关操作可参考 [cluster 命令](/tiup/tiup-cluster.md)。
