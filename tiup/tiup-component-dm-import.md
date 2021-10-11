---
title: tiup dm import
---

# tiup dm import

在 DM 1.0 版本，集群基本是通过 TiDB Ansible 部署的，TiUP DM 提供了 `import` 命令导入 v1.0 的集群并重新部署 v2.0 的集群。

> **注意：**
>
> - 不支持导入 v1.0 集群中的 DM Portal 组件
> - 导入前请先停止原集群
> - 对于需要升级到 v2.0 的数据迁移任务，请不要执行 `stop-task`
> - 仅支持导入到 v2.0.0-rc.2 或更高版本
> - `import` 命令用于将 DM v1.0 集群导入到全新的 v2.0 集群。如果需要将数据迁移任务导入到已有的 v2.0 集群，请参考 [TiDB Data Migration 1.0.x 到 2.0.x 手动升级](https://docs.pingcap.com/zh/tidb-data-migration/stable/manually-upgrade-dm-1.0-to-2.0)
> - 部分组件生成的部署目录会跟原集群不一样，具体可以使用 `display` 命令查看
> - 导入前运行 `tiup update --self && tiup update dm` 确认升级 TiUP DM 组件到最新版本
> - 导入后集群中仅会有一个 DM-master 节点，可参考[扩容节点](/tiup/tiup-component-dm-scale-out.md)对 DM-master 进行扩容

## 语法

```shell
tiup dm import [flags]
```

## 选项

### -v, --cluster-version（string，required）

重新部署的版本号，必须指定 v2.0.0-rc.2 或更高版本。

### -d, --dir string（string, 默认 当前目录）

指定 TiDB Ansible 所在目录。

### --inventory string（string，默认 "inventory.ini"）

指定 Ansible inventory 文件的名字。

### --rename（string，默认为空）

重命名导入的集群。默认集群名为 inventory 中指定的 `cluster_name`。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

导入过程的日志信息。

[<< 返回上一页 - TiUP DM 命令清单](/tiup/tiup-component-dm.md#命令清单)