---
title: ti db describe-db-cluster
summary: 描述一个 TiDB Cloud Starter 集群。
---

# ti db describe-db-cluster

获取 TiDB Cloud Starter 实例的信息。默认的 `BASIC` 视图会返回基本实例信息。使用 `--view FULL` 可请求 TiDB Cloud API 提供的完整详细信息。如果集群的 API 元信息无法将其验证为 Starter，则该命令会拒绝该集群。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti db describe-db-cluster
  --db-cluster-id <string>
  [--help]
  [--version]
  [--view <string>]
```

## 选项 {#options}

- `--db-cluster-id <string>`：Starter DB 集群 ID。\[必需]
- `--help`：显示帮助信息。
- `--version`：显示版本信息。
- `--view <string>`：详细级别：`BASIC` 或 `FULL`。如果省略，TiDB Cloud API 使用 `BASIC`。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 获取 TiDB Cloud Starter 实例的信息：

    ```bash
    # Return the instance state, placement, and connection metadata.
    ti db describe-db-cluster --db-cluster-id "<cluster-id>" --view FULL
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)