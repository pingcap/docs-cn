---
title: tiup dm patch
---

# tiup dm patch

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

- `<cluster-name>` 代表要操作的集群名
- `<package-path>` 为用于替换的二进制包

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

## 输出

tiup-dm 的执行日志。
