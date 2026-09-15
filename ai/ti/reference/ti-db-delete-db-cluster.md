---
title: ti db delete-db-cluster
summary: 删除一个 TiDB Cloud Starter 集群。
---

# ti db delete-db-cluster

删除一个 TiDB Cloud Starter 实例。使用 `--wait` 可等待删除完成。此命令仅接受 TiDB Cloud Starter 实例，并会拒绝其他类型的集群。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti db delete-db-cluster
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
  [--wait]
```

## 选项 {#options}

- `--db-cluster-id <string>`：Starter DB 集群 ID。\[必需]
- `--dry-run`：验证请求而不应用更改。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。
- `--wait`：在 TiDB Cloud 接受删除请求后，持续轮询直到实例状态变为 `DELETED`。后续返回 `not found` 或 `permission denied` 响应也会被视为删除已完成，因为该实例已无法再被读取。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 删除一个集群并等待完成：

    ```bash
    # Wait until TiDB Cloud reports the cluster deleted or no longer accessible.
    ti db delete-db-cluster --db-cluster-id "<cluster-id>" --wait
    ```

- 异步删除一个集群：

    ```bash
    # Return after TiDB Cloud accepts deletion while cleanup continues remotely.
    ti db delete-db-cluster --db-cluster-id "<cluster-id>"
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)