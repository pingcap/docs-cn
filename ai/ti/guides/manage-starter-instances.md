---
title: 管理 TiDB Cloud Starter 实例
summary: 了解如何使用 TiDB Cloud CLI 创建和管理 Starter 实例、分支、SQL 用户、连接和 SQL 语句。
---

# 管理 TiDB Cloud Starter 实例

本文介绍如何在终端或自动化工作流中使用 TiDB Cloud CLI 的 `ti db` 命令来管理 TiDB Cloud Starter 实例、分支以及 SQL 访问。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 配置一个具有 TiDB Cloud Starter 访问权限凭证的配置（Profile）。

## 创建 TiDB Cloud Starter 实例 {#create-a-tidb-cloud-starter-instance}

创建一个 TiDB Cloud Starter 实例，并等待其变为活动状态：

```shell
ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --wait
```

## 列出实例 {#list-instances}

列出当前生效 Region 中的 TiDB Cloud Starter 实例：

```shell
ti db list-db-clusters --db-cluster-type starter --output text
```

如需获取某个 TiDB Cloud Starter 实例的信息，请将其实例 ID 传递给 [`describe-db-cluster`](/ai/ti/reference/ti-db-describe-db-cluster.md)。

## 管理分支 {#manage-branches}

从一个实例创建开发分支：

```shell
ti db create-db-cluster-branch \
  --db-cluster-id "<instance-id>" \
  --db-cluster-branch-name dev \
  --wait
```

你可以使用分支的列表、描述和删除命令来管理其生命周期。有关这些命令的完整选项，请参阅 [`ti db` 命令参考](/ai/ti/reference/ti-starter-database.md)。

## 配置 SQL 访问 {#configure-sql-access}

为实例创建或修复只读、读写和 admin SQL 用户：

```shell
ti db create-db-sql-users --db-cluster-id "<instance-id>"
```

将已存储的凭证格式化为应用程序可用的形式：

```shell
ti db format-db-connection-string \
  --db-cluster-id "<instance-id>" \
  --read-only \
  --format env
```

## 执行 SQL {#execute-sql}

使用显式 SQL 角色执行一条语句：

```shell
ti db execute-sql-statement \
  --db-cluster-id "<instance-id>" \
  --read-only \
  --sql "SELECT 1"
```

如需了解将只读、读写和管理操作分离的工作流，请参阅[使用显式 SQL 角色查询 TiDB Cloud Starter](/ai/ti/guides/ti-query-sql-with-roles-example.md)。

## 删除实例 {#delete-an-instance}

当你不再需要该实例时，删除它并等待直到可以观察到删除结果：

```shell
ti db delete-db-cluster --db-cluster-id "<instance-id>" --wait
```

## 后续操作 {#what-s-next}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)
- [运行日常 TiDB Cloud CLI 工作流](/ai/ti/guides/ti-daily-workflow-example.md)