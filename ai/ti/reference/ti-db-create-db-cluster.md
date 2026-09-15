---
title: ti db create-db-cluster
summary: 创建一个 TiDB Cloud Starter 集群。
---

# ti db create-db-cluster

创建一个 TiDB Cloud Starter 实例。必需的 `--db-cluster-type` 必须为 `starter`；不存在隐式类型。`--wait` 会等待集群变为 `ACTIVE`。

该请求不会选择项目。TiDB Cloud 会根据其服务端的项目规则分配实例，而 `ti` 会保留响应中的任何项目元信息。你无法通过 `ti` 选择或配置项目。

TiDB Cloud CLI 会验证返回的服务计划。如果在创建请求被接受后验证失败，`ti` 会报告集群 ID，并保留该实例以供检查。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti db create-db-cluster
  --db-cluster-name <string>
  --db-cluster-type <string>
  [--dry-run]
  [--help]
  [--monthly-spending-limit-usd-cents <int32>]
  [--version]
  [--wait]
```

## 选项 {#options}

- `--db-cluster-name <string>`：Starter DB 集群显示名称。\[必需]
- `--db-cluster-type <string>`：DB 集群类型；必须为 `starter`。\[必需]
- `--dry-run`：验证请求而不应用更改。
- `--help`：显示帮助信息。
- `--monthly-spending-limit-usd-cents <int32>`：每月支出上限，单位为美分（USD cents）。如果省略，`ti` 不会发送支出上限，TiDB Cloud 会应用其默认规则。详情请参见 [管理 TiDB Cloud Starter 实例的支出上限](https://docs.pingcap.com/tidbcloud/manage-serverless-spend-limit)。
- `--version`：显示版本信息。
- `--wait`：等待创建的集群变为 `ACTIVE` 后再返回。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建一个集群并等待其变为活动状态：

    ```bash
    # Wait until the new TiDB Cloud Starter instance reaches the ACTIVE state.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --wait
    ```

- 异步创建一个集群：

    ```bash
    # Return after TiDB Cloud accepts creation so another process can poll the cluster.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name background-db
    ```

- 预览集群创建：

    ```bash
    # Validate the request and resolved defaults without creating a cluster.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name app-db --dry-run
    ```

- 设置每月支出上限：

    ```bash
    # Create a paid TiDB Cloud Starter instance with a monthly limit expressed in US dollar cents.
    ti db create-db-cluster --db-cluster-type starter --db-cluster-name production-db --monthly-spending-limit-usd-cents 1000 --wait
    ```

## 如果创建后验证失败 {#if-post-creation-verification-fails}

如果 TiDB Cloud 接受了创建请求，但 `ti` 无法将返回的资源验证为 Starter 实例，请记下错误中的集群 ID。使用以下命令检查保留的资源：

```bash
ti db describe-db-cluster --db-cluster-id "<cluster-id>"
```

如果 `ti` 仍然无法验证服务计划，请在 TiDB Cloud 控制台中检查或删除该资源。在确认第一次请求是否已创建实例之前，请勿重复执行创建命令。

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)