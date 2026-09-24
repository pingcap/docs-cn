---
title: ti fs create-layer
summary: 在文件系统中创建一个 layer。
---

# ti fs create-layer

创建一个 layer，用于在文件系统基础路径之上记录隔离的变更。如果省略 `--layer-id`，则由服务生成一个。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于 public preview 阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs create-layer
  --base-root-path <string>
  [--actor-id <string>]
  [--dry-run]
  [--durability-mode <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--layer-name <string>]
  [--tag <string>]
  [--version]
```

## 选项 {#options}

- `--base-root-path <string>`: TiDB Cloud 文件系统中的基础根路径。\[必需]
- `--actor-id <string>`: 用于标识 layer 所有者的 Actor ID（例如 agent 名称）。
- `--dry-run`: 验证请求但不应用更改。
- `--durability-mode <string>`: 设置 layer 的持久性模式。唯一明确支持的值是 `restore-safe`，它会将变更保存在远程 layer 中，以便在本地环境结束后仍可恢复该 layer。如果省略，服务将使用 `restore-safe`。
- `--file-system-id <string>`: 选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`: 设置文件系统访问令牌。如果省略，该命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，该命令会使用为所选文件系统在本地存储的令牌。
- `--help`: 显示帮助信息。
- `--layer-id <string>`: layer ID。通常由服务自动生成。
- `--layer-name <string>`: layer 的名称。
- `--tag <string>`: layer 的标签，格式为 `key=value`；可重复指定。
- `--version`: 显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建一个 layer：

    ```bash
    # Start an isolated writable view over the selected base root.
    ti fs create-layer --file-system-id <file-system-id> --base-root-path /workspace --layer-name agent-task
    ```

- 创建一个带有 restore-safe 标签的 layer：

    ```bash
    # Request durable layer behavior and attach task metadata.
    ti fs create-layer --file-system-id <file-system-id> --base-root-path /workspace --durability-mode restore-safe --tag task=review
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)