---
title: 在线应用 Hotfix 到 DM 集群
summary: 了解如何应用 hotfix 补丁包到 DM 集群。
---

# 在线应用 Hotfix 到 DM 集群

在集群运行过程中，如果需要动态替换某个服务的二进制文件（即替换过程中保持集群可用），那么可以使用 `tiup dm patch` 命令，它会完成以下几件事情：

- 将用于替换的二进制包上传到目标机器
- 通过 API 下线节点
- 停止目标服务
- 解压二进制包，替换服务
- 启动目标服务

## 语法

```shell
tiup dm patch <cluster-name> <package-path> [flags]
```

- `<cluster-name>` 代表要操作的集群名。
- `<package-path>` 为用于替换的二进制包。

### 准备条件

执行 `tiup dm patch` 命令前，需要进行以下操作准备用于替换的二进制包：

- 确定当前要替换的组件名称 `${component}` (dm-master，dm-worker 等) 以及其版本 `${version}` (v2.0.0，v2.0.1 等)，以及其运行的平台 `${os}` (linux) 和 `${arch}` (amd64, arm64)
- 下载当前的组件包：`wget https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz -O /tmp/${component}-${version}-${os}-${arch}.tar.gz`
- 建立临时打包目录：`mkdir -p /tmp/package && cd /tmp/package`
- 解压原来的二进制包：`tar xf /tmp/${component}-${version}-${os}-${arch}.tar.gz`
- 查看临时打包目录中的文件结构：`find .`
- 将要替换的二进制文件或配置文件复制到临时目录的对应位置
- 重新打包 `tar czf /tmp/${component}-hotfix-${os}-${arch}.tar.gz *`

完成以上操作后，`/tmp/${component}-hotfix-${os}-${arch}.tar.gz` 就可以作为 `<package-path>` 用于 patch 命令中。

## 选项

### --overwrite

- 对某个组件（比如 TiDB，TiKV）进行 patch 之后，该集群扩容该组件时，tiup-dm 默认会用原来的版本。如果希望后续扩容的时候也使用 patch 之后的版本的话，就需要指定 `--overwrite` 选项。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -N, --node（strings，默认为 []，未选中任何节点）

指定要替换的节点，该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-dm-display.md)表格的第一列。

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将替换它们的交集中的服务。

### -R, --role（strings，默认为 []，未选中任何角色）

指定要替换的角色，该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-dm-display.md)表格的第二列。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将替换它们的交集中的服务。

### --offline

声明当前集群处于离线状态。指定该选项时，TiUP DM 仅原地替换集群组件的二进制文件，不重启服务。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 在线应用 Hotfix 示例

以下将在使用 TiUP 部署的 DM 环境中演示如何应用 `v5.3.0-hotfix` 到 `v5.3.0`集群，其他部署方式可能需要调整部分操作。

> **注意：**
>
> Hotfix 仅用于紧急修复，其日常维护较为复杂，建议在正式版本发布后及时升级。

### 准备工作

在开始应用 Hotfix 之前，请准备好 Hotfix 补丁包 `dm-linux-amd64.tar.gz`，并确认当前环境 DM 软件版本：

```shell
/home/tidb/dm/deploy/dm-master-8261/bin/dm-master/dm-master -V
```

输出示例：

```
Release Version: v5.3.0
Git Commit Hash: 20626babf21fc381d4364646c40dd84598533d66
Git Branch: heads/refs/tags/v5.3.0
UTC Build Time: 2021-11-29 08:29:49
Go Version: go version go1.16.4 linux/amd64
```

### 制作 Patch 补丁包并应用到 DM 集群

1. 准备当前环境版本的 DM 软件包：

    {{< copyable "shell-regular" >}}

    ```shell
    mkdir -p /tmp/package
    tar -zxvf /root/.tiup/storage/dm/packages/dm-master-v5.3.0-linux-amd64.tar.gz -C /tmp/package/
    tar -zxvf /root/.tiup/storage/dm/packages/dm-worker-v5.3.0-linux-amd64.tar.gz -C /tmp/package/
    ```

2. 替换新的二进制文件：

    {{< copyable "shell-regular" >}}

    ```shell
    # 解压 Hotfix 压缩包并替换
    cd /root; tar -zxvf dm-linux-amd64.tar.gz
    cp /root/dm-linux-amd64/bin/dm-master /tmp/package/dm-master/dm-master
    cp /root/dm-linux-amd64/bin/dm-worker /tmp/package/dm-worker/dm-worker

    # 重新打包
    # 注意，其他部署方式可能有所不同
    cd /tmp/package/ && tar -czvf dm-master-hotfix-linux-amd64.tar.gz dm-master/
    cd /tmp/package/ && tar -czvf dm-worker-hotfix-linux-amd64.tar.gz dm-worker/
    ```

3. 应用补丁。

    查询当前集群状态，以名称为 `dm-test` 的集群为例：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dm display dm-test
    ```

    输出示例：

    ```
    Cluster type:       dm
    Cluster name:       dm-test
    Cluster version:    v5.3.0
    Deploy user:        tidb
    SSH type:           builtin
    ID                  Role                 Host           Ports      OS/Arch       Status     Data Dir                              Deploy Dir
    --                  ----                 ----           -----      -------       ------     --------                              ----------
    172.16.100.21:9093  alertmanager         172.16.100.21  9093/9094  linux/x86_64  Up         /home/tidb/dm/data/alertmanager-9093  /home/tidb/dm/deploy/alertmanager-9093
    172.16.100.21:8261  dm-master            172.16.100.21  8261/8291  linux/x86_64  Healthy|L  /home/tidb/dm/data/dm-master-8261     /home/tidb/dm/deploy/dm-master-8261
    172.16.100.21:8262  dm-worker            172.16.100.21  8262       linux/x86_64  Free       /home/tidb/dm/data/dm-worker-8262     /home/tidb/dm/deploy/dm-worker-8262
    172.16.100.21:3000  grafana              172.16.100.21  3000       linux/x86_64  Up         -                                     /home/tidb/dm/deploy/grafana-3000
    172.16.100.21:9090  prometheus           172.16.100.21  9090       linux/x86_64  Up         /home/tidb/dm/data/prometheus-9090    /home/tidb/dm/deploy/prometheus-9090
    Total nodes: 5
    ```

    将补丁应用到指定节点或指定角色，若同时使用 `-R` 和 `-N`，将会取其交集。

    {{< copyable "shell-regular" >}}

    ```
    # 为指定节点应用补丁
    tiup dm patch dm-test dm-master-hotfix-linux-amd64.tar.gz -N 172.16.100.21:8261
    tiup dm patch dm-test dm-worker-hotfix-linux-amd64.tar.gz -N 172.16.100.21:8262

    # 为指定角色应用补丁
    tiup dm patch dm-test dm-master-hotfix-linux-amd64.tar.gz -R dm-master
    tiup dm patch dm-test dm-worker-hotfix-linux-amd64.tar.gz -R dm-worker
    ```

4. 查看补丁应用结果：

    {{< copyable "shell-regular" >}}

    ```shell
    /home/tidb/dm/deploy/dm-master-8261/bin/dm-master/dm-master -V
    ```

    输出示例：

    ```
    Release Version: v5.3.0-20211230
    Git Commit Hash: ca7070c45013c24d34bd9c1e936071253451d707
    Git Branch: heads/refs/tags/v5.3.0-20211230
    UTC Build Time: 2022-01-05 14:19:02
    Go Version: go version go1.16.4 linux/amd64
    ```

    集群信息也会有所变化：

    {{< copyable "shell-regular" >}}

    ```shell
    tiup dm display dm-test
    ```

    输出示例：

    ```
    Starting component `dm`: /root/.tiup/components/dm/v1.8.1/tiup-dm display dm-test
    Cluster type:       dm
    Cluster name:       dm-test
    Cluster version:    v5.3.0
    Deploy user:        tidb
    SSH type:           builtin
    ID                  Role                 Host           Ports      OS/Arch       Status     Data Dir                              Deploy Dir
    --                  ----                 ----           -----      -------       ------     --------                              ----------
    172.16.100.21:9093  alertmanager         172.16.100.21  9093/9094  linux/x86_64  Up         /home/tidb/dm/data/alertmanager-9093  /home/tidb/dm/deploy/alertmanager-9093
    172.16.100.21:8261  dm-master (patched)  172.16.100.21  8261/8291  linux/x86_64  Healthy|L  /home/tidb/dm/data/dm-master-8261     /home/tidb/dm/deploy/dm-master-8261
    172.16.100.21:8262  dm-worker (patched)  172.16.100.21  8262       linux/x86_64  Free       /home/tidb/dm/data/dm-worker-8262     /home/tidb/dm/deploy/dm-worker-8262
    172.16.100.21:3000  grafana              172.16.100.21  3000       linux/x86_64  Up         -                                     /home/tidb/dm/deploy/grafana-3000
    172.16.100.21:9090  prometheus           172.16.100.21  9090       linux/x86_64  Up         /home/tidb/dm/data/prometheus-9090    /home/tidb/dm/deploy/prometheus-9090
    Total nodes: 5
    ```

[<< 返回上一页 - TiUP DM 命令清单](/tiup/tiup-component-dm.md#命令清单)