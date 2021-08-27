---
title: tiup cluster import
---

# tiup cluster import

在 TiDB 4.0 以前的版本，集群多是通过 TiDB Ansible 部署的。TiUP Cluster 提供了 `import` 命令用于让这些集群过渡到使用 tiup-cluster 组件管理。

> **注意：**
>
> + TiDB Ansible 配置导入到 TiUP 中管理后，不能再通过 TiDB Ansible 对集群进行操作，否则可能因元信息不一致造成冲突
> + 如果使用 TiDB Ansible 部署的集群存在以下情况之一，暂不支持导入：
>     + 启用了 TLS 加密功能的集群
>     + 纯 KV 集群（没有 TiDB 实例的集群）
>     + 启用了 Kafka 的集群
>     + 启用了 Spark 的集群
>     + 启用了 TiDB Lightning/ Importer 的集群
>     + 仍使用老版本 `push` 的方式收集监控指标（从 v3.0 起默认为 `pull` 模式，如果没有特意调整过则可以支持）
>     + 在 `inventory.ini` 配置文件中单独为机器的 `node_exporter` / `blackbox_exporter` 通过 `node_exporter_port`/`blackbox_exporter_port` 设置了非默认端口（在 `group_vars` 目录中统一配置的可以兼容）
> + 如果使用 TiDB Ansible 部署的集群中有部分节点未部署监控，应当先使用 TiDB Ansible 在 `inventory.ini` 文件的 `monitored_servers` 分组中补充对应节点的信息，并通过 `deploy.yaml` playbook 将补充的监控组件部署完整。否则在集群导入 TiUP 后进行其他运维操作时，可能会因监控组件缺失而出错。

## 语法

```shell
tiup cluster import [flags]
```

## 选项

### -d, --dir string（string, 默认 当前目录）

指定 TiDB Ansible 所在目录。

### --ansible-config（string，默认 "./ansible.cfg"）

指定 Ansible 的配置文件路径。

### --inventory string（string，默认 "inventory.ini"）

指定 Ansible inventory 文件的名字。

### --no-backup

- 默认情况下，导入成功之后会将 `--dir` 指定的目录里所有内容备份到 `${TIUP_HOME}/.tiup/storage/cluster/clusters/{cluster-name}/ansible-backup` 下。该选项用于禁用默认的备份步骤，如果该目录下有多个 inventory 文件（部署了多个集群），推荐禁用默认备份。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

### --rename（string，默认为空）

重命名导入的集群。默认集群名为 inventory 中指定的 cluster_name。

### -h, --help

- 输出帮助信息。
- 数据类型：`BOOLEAN`
- 该选项默认关闭，默认值为 `false`。在命令中添加该选项，并传入 `true` 值或不传值，均可开启此功能。

## 输出

导入过程的日志信息。

[<< 返回上一页 - TiUP Cluster 命令清单](/tiup/tiup-component-cluster.md#命令清单)
