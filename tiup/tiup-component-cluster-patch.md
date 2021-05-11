---
title: tiup cluster patch
---

# tiup cluster patch

在集群运行过程中，如果需要动态替换某个服务的二进制文件（即替换过程中保持集群可用），那么可以使用 `tiup cluster patch` 命令，它会完成以下几件事情：

- 将用于替换的二进制包上传到目标机器
- 如果目标服务是 TiKV、TiFlash 或者 TiDB Binlog 之类的存储服务，则先通过 API 下线节点
- 停止目标服务
- 解压二进制包，替换服务
- 启动目标服务

## 语法

```shell
tiup cluster patch <cluster-name> <package-path> [flags]
```

- `<cluster-name>` 代表要操作的集群名
- `<package-path>` 为用于替换的二进制包，其打包方式如下：
    - 确定当前要替换的组件名称 `${component}` (tidb, tikv, pd...) 以及其版本 `${version}` (v4.0.0, v4.0.1 ...)，以及其运行的平台 `${os}` (linux) 和 `${arch}` (amd64, arm64)
    - 下载当前的组件包：`wget https://tiup-mirrors.pingcap.com/${component}-${version}-${os}-${arch}.tar.gz -O /tmp/${component}-${version}-${os}-${arch}.tar.gz`
    - 建立临时打包目录：`mkdir -p /tmp/package && cd /tmp/package`
    - 解压原来的二进制包：`tar xf /tmp/${component}-${version}-${os}-${arch}.tar.gz`
    - 查看临时打包目录中的文件结构：`find .`
    - 将要替换的二进制文件或配置文件复制到临时目录的对应位置
    - 重新打包 `tar czf /tmp/${component}-hotfix-${os}-${arch}.tar.gz *`
    - 通过以上步骤之后，`/tmp/${component}-hotfix-${os}-${arch}.tar.gz` 就可以用于 patch 命令了

## 选项

### --overwrite

- 对某个组件（比如 TiDB，TiKV）进行 patch 后，如果要在该集群扩容该组件，tiup-cluster 会默认使用 patch 前的版本。如果希望后续扩容的时候也使用 patch 之后的版本，需要指定 `--overwrite` 选项。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --transfer-timeout（uint，默认 300）

在重启 PD 或 TiKV 时，会先将被重启节点的 leader 迁移到其他节点，迁移过程会需要一定时间，可以通过设置 `--transfer-timeout` 设置最长等待时间（单位为秒），超时之后会跳过等待直接重启服务。

> **注意：**
>
> 若出现跳过等待直接重启的情况，服务性能可能会出现抖动。

### -N, --node（strings，默认为 []，未选中任何节点）

指定要替换的节点，该选项的值为以逗号分割的节点 ID 列表，节点 ID 为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第一列。

> **注意：**
>
> 若同时指定了 `-R, --role`，那么将替换它们的交集中的服务。

### -R, --role（strings，默认为 []，未选中任何角色）

指定要替换的角色，该选项的值为以逗号分割的节点角色列表，角色为[集群状态](/tiup/tiup-component-cluster-display.md)表格的第二列。

> **注意：**
>
> 若同时指定了 `-N, --node`，那么将替换它们的交集中的服务。

### --offline

- 声明当前集群处于停止状态。指定该选项时，TiUP Cluster 仅原地替换集群组件的二进制文件，不执行迁移 Leader 以及重启服务等操作。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

tiup-cluster 的执行日志。
