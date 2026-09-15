---
title: ti db update-db-cluster
summary: 修改 TiDB Cloud Starter 集群。
---

# ti db update-db-cluster

修改 TiDB Cloud Starter 实例的显示名称或每月支出上限。`--db-cluster-name` 和 `--monthly-spending-limit-usd-cents` 中至少需要指定一个。此命令仅接受 Starter 实例。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti db update-db-cluster
  --db-cluster-id <string>
  [--db-cluster-name <string>]
  [--dry-run]
  [--help]
  [--monthly-spending-limit-usd-cents <int32>]
  [--version]
```

## 选项 {#options}

- `--db-cluster-id <string>`：Starter DB 集群 ID。\[必需]
- `--db-cluster-name <string>`：新的 Starter DB 集群显示名称。
- `--dry-run`：验证请求但不应用更改。
- `--help`：显示帮助信息。
- `--monthly-spending-limit-usd-cents <int32>`：以美分为单位的每月支出上限；省略则保持不变。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 重命名集群：

    ```bash
    # Change the TiDB Cloud Starter instance display name without recreating it.
    ti db update-db-cluster --db-cluster-id "<cluster-id>" --db-cluster-name app-db-v2
    ```

- 预览支出上限修改：

    ```bash
    # Validate a new monthly limit without applying the change.
    ti db update-db-cluster --db-cluster-id "<cluster-id>" --monthly-spending-limit-usd-cents 1000 --dry-run
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)