---
title: ti db create-db-cluster-branch
summary: 为 TiDB Cloud Starter 集群创建一个分支。
---

# ti db create-db-cluster-branch

为一个 TiDB Cloud Starter 实例创建分支。`--wait` 会等待分支变为 `ACTIVE`。该命令会在创建分支前验证父集群是否为 Starter。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti db create-db-cluster-branch
  --db-cluster-branch-name <string>
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## 选项 {#options}

- `--db-cluster-branch-name <string>`：Starter DB 集群分支显示名称。\[必需]
- `--db-cluster-id <string>`：Starter DB 集群 ID。\[必需]
- `--dry-run`：验证请求而不应用更改。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。
- `--wait`：等待创建的分支变为 `ACTIVE` 后再返回。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建一个分支并等待其变为活动状态：

    ```bash
    # Wait until the new database branch can accept connections.
    ti db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name dev --wait
    ```

- 预览分支创建：

    ```bash
    # Validate the parent cluster and branch request without creating it.
    ti db create-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-name preview --dry-run
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)