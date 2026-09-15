---
title: ti db list-db-cluster-branches
summary: 列出一个 TiDB Cloud Starter 集群的分支。
---

# ti db list-db-cluster-branches

列出一个 TiDB Cloud Starter 实例的分支，并可选择使用分页。该命令会在列出分支前验证父集群是否为 Starter。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti db list-db-cluster-branches
  --db-cluster-id <string>
  [--help]
  [--page-size <int32>]
  [--page-token <string>]
  [--version]
```

## 选项 {#options}

- `--db-cluster-id <string>`: Starter DB 集群 ID。\[必需]
- `--help`: 显示帮助信息。
- `--page-size <int32>`: 要请求的分支数量。如果省略或设置为 `0`，API 最多返回 `10` 个。API 的最大值为 `100`；大于 `100` 的值会被设置为 `100`。
- `--page-token <string>`: 上一次调用 list-db-cluster-branches 返回的分页令牌。
- `--version`: 显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 列出集群分支：

    ```bash
    # Return all branches that belong to the selected TiDB Cloud Starter instance.
    ti db list-db-cluster-branches --db-cluster-id "<cluster-id>"
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)