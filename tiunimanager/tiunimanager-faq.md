---
title: TiUniManager 常见问题
summary: 了解 TiUniManager 的常见问题以及回答。
---

# TiUniManager 常见问题

本文档介绍 TiUniManager 的常见问题，帮助用户更好了解 TiUniManager。

## 产品基本 FAQ

### TiUniManager 管理的集群可以部署在哪里？

TiUniManager 管理的集群可以部署在用户自建的数据中心或公有云。

### TiUniManager 面向哪几类用户？

TiUniManager 面向三类用户：IT 系统管理员、数据库管理员 DBA、数据库应用开发人员。

### TiUniManager 支持的 TiDB 版本有哪些？

见 [TiUniManager 支持的 TiDB 版本](/tiunimanager/tiunimanager-release-notes.md#tiunimanager-支持的-tidb-版本)。

### TiUniManager 与 TiUP 的关系是什么？

TiUniManager 使用 TiDB 及其生态工具、API 提供数据库管理产品功能，TiUP 是 TiUniManager 使用的工具之一。TiUniManager 产品架构图如下：

![TiUniManager 架构图](/media/tiunimanager/tiunimanager-architecture.png)

## 主机资源管理 FAQ

### 何时导入主机资源到 TiUniManager？

在创建新集群或导入现有集群前，你需要将集群所需的主机资源导入到 TiUniManager。具体步骤参见 [TiUniManager 资源管理](/tiunimanager/tiunimanager-manage-host-resources.md)。

## TiUniManager 安装部署 FAQ

### TiUniManager 支持离线安装吗？

支持

### TiUniManager 首次部署后，需要如何做产品初始化吗？

TiUniManager 首次部署后，需要对 TiDB 组件规格、数据中心 Zone 信息、主机规格信息进行初始化。

### 如何在命令行查看 EM 服务和 EM 部署的 TiDB 集群信息？

首先请先通过 `su - tidb` 命令切换到 `tidb` 账号下。

所有与 EM 工具相关的命令，请以 `TIUP_HOME=/home/tidb/.em tiup em <cmd>` 的方式执行，例如 `TIUP_HOME=/home/tidb/.em tiup em list`。

所有与 EM 部署的 TiDB 集群相关的命令，请以直接以 `tiup cluster <cmd>` 的方式执行，例如 `tiup cluster list`。

## 集群部署 FAQ

### TiUniManager 支持在离线环境中部署 TiDB 集群吗？

支持

### TiKV 实例数与 TiKV 的关系？

创建集群时，TiKV 副本数建议为 1 个、3 个、5 个、或 7 个。设置的 TiKV 实例数不能小于 TiKV  副本数。

### 建议的 PD 实例数量？

建议的 PD 实例数量为 1 个、3 个、5 个、或 7 个。

## 备份与恢复 FAQ

### 备份支持的存储类型有哪些？

TiUniManager 支持将数据备份至 S3 兼容存储和 NFS 共享存储。

### 如何设置 TiUniManager 的备份路径？

TiUniManager 目前不支持通过前端界面修改备份路径，修改备份路径方法参考 [TiUniManager 备份管理](/tiunimanager/tiunimanager-manage-clusters.md#备份管理---数据备份)。

## 数据导入与导出 FAQ

### 可以从哪些上游导入数据到 TiUniManager？

你可以从 S3 兼容存储、本地存储、或 TiUniManager 共享存储上导入集群。

### 导出的数据可以保存在哪些存储上？

导出的数据可以保存至 S3 兼容存储或 TiUniManager 共享存储，对于保存在 TiUniManager 共享存储上的导入数据，你可进一步下载至本地。

### 从本地上传的导入文件大小有限制吗？

从本地上传的源数据文件大小不能超过 2 GB。

### 什么是 TiUniManager 共享存储？

TiUniManager 共享存储是用户事先设定好用于保存导入导出文件的文件资源池，该文件资源池是一个可挂载于 TiUniManager 中控机的 NFS 目录，该 NFS 路径由用户在 TiUniManager 安装后进行设置。

### 如何修改 TiUniManager 共享存储路径？

参见 [TiUniManager 数据导入与导出](/tiunimanager/tiunimanager-import-and-export-data.md)。

## 集群扩容缩容 FAQ

### 对组件实例进行缩容时有何限制？

TiDB、PD、TiKV 的实例数量最小为 1。当实例数等于 1 时，不能进行缩容操作。

### TiKV 实例数与 TiKV 副本数有何关系？

TiKV 实例数量不能低于 TiKV 副本数。对 TiKV 进行缩容时，缩容后的 TiKV 实例数量不能小于 TiKV 副本数。

## 接管集群 FAQ

### TiUniManager 接管集群前有什么注意事项吗？

建议用户在 TiUniManager 接管集群前，对集群进行一次数据备份。

### 接管集群时需要用户填写的“TiUP 部署路径”是什么？

“TiUP 部署路径”是被接管集群中 TiUP 的 home 路径。填写该路径时，请勿填写路径结尾的 `/`。

例如，请勿填写为 `/root/.tiup/`。
