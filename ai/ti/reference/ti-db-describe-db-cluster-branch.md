---
title: ti db describe-db-cluster-branch
summary: 描述 TiDB Cloud Starter 集群的一个分支。
---

# ti db describe-db-cluster-branch

根据集群 ID 和分支 ID 描述一个分支。默认的 `FULL` 视图会返回 TiDB Cloud API 提供的完整分支详细信息；使用 `--view BASIC` 可仅请求基本信息。该命令会在读取分支前验证父集群是否为 Starter。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti db describe-db-cluster-branch
  --db-cluster-branch-id <string>
  --db-cluster-id <string>
  [--help]
  [--version]
  [--view <string>]
```

## 选项 {#options}

- `--db-cluster-branch-id <string>`: Starter DB cluster branch ID。\[required]
- `--db-cluster-id <string>`: Starter DB cluster ID。\[required]
- `--help`: 显示帮助信息。
- `--version`: 显示版本信息。
- `--view <string>`: 详细级别：`BASIC` 或 `FULL`。如果省略，TiDB Cloud API 使用 `FULL`。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 描述一个分支：

    ```bash
    # Return full lifecycle and connection details for one branch.
    ti db describe-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>" --view FULL
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)