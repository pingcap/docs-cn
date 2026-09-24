---
title: ti fs-journal create-journal
summary: 创建一个仅追加的文件系统日志（Journal）。
---

# ti fs-journal create-journal

创建一个日志（Journal）。如果省略 `--journal-id`，则由服务生成一个。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-journal create-journal
  [--actor <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--journal-id <string>]
  [--journal-kind <string>]
  [--label <string>]
  [--title <string>]
  [--version]
```

## 选项 {#options}

- `--actor <string>`：Actor，格式为 `type:id`。两部分都是用户定义的非空字符串；CLI 会将 `type` 转换为小写。
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，该命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，则该命令会使用为所选文件系统在本地存储的令牌。
- `--help`：显示帮助信息。
- `--journal-id <string>`：日志（Journal）ID；省略时自动生成。
- `--journal-kind <string>`：用户定义的日志（Journal）类别。必须包含 1 到 64 个字符，以小写字母开头，并且只能使用小写字母、数字、下划线（`_`）、句点（`.`）或连字符（`-`）。\\[default: agent]
- `--label <string>`：日志（Journal）标签，格式为 `key=value`；可重复指定。
- `--title <string>`：日志（Journal）标题。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建一个 agent 日志（Journal）：

    ```bash
    # Create an append-only journal for one agent task.
    ti fs-journal create-journal --file-system-id <file-system-id> --journal-id jrn-demo --journal-kind agent --title "demo task"
    ```

- 创建一个带标签的 deployment 日志（Journal）：

    ```bash
    # Attach actor and environment metadata for later searches.
    ti fs-journal create-journal --file-system-id <file-system-id> --journal-kind deployment --actor agent:ti --label env=dev
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)