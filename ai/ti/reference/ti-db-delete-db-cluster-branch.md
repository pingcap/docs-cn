---
title: ti db delete-db-cluster-branch
summary: 从 TiDB Cloud Starter 集群中删除一个分支。
---

# ti db delete-db-cluster-branch

从 TiDB Cloud Starter 实例中删除一个分支。该命令会先验证父集群是否为 Starter，然后再读取或删除该分支。它会直接返回删除响应而不进行轮询；此命令不提供 `--wait` 选项。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti db delete-db-cluster-branch
  --db-cluster-branch-id <string>
  --db-cluster-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## 选项 {#options}

- `--db-cluster-branch-id <string>`: Starter DB cluster branch ID。\[required]
- `--db-cluster-id <string>`: Starter DB cluster ID。\[required]
- `--dry-run`: 验证请求而不应用更改。
- `--help`: 显示帮助信息。
- `--version`: 显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 删除一个分支：

    ```bash
    # Delete only the selected branch from its parent TiDB Cloud Starter instance.
    ti db delete-db-cluster-branch --db-cluster-id "<cluster-id>" --db-cluster-branch-id "<branch-id>"
    ```

要验证该分支是否已不再显示，请运行 `ti db list-db-cluster-branches --db-cluster-id "<cluster-id>"`。

## 相关文档 {#related-documentation}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)