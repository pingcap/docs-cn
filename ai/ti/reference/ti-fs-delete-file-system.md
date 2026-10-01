---
title: ti fs delete-file-system
summary: 删除文件系统。
---

# ti fs delete-file-system

开始删除一个文件系统。删除操作会在命令返回后以异步方式运行。你必须指定 `--file-system-id`；显示名称、标签和文件系统令牌都不能用于标识要删除的文件系统。此命令需要 TiDB Cloud API 凭证。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs delete-file-system
  --file-system-id <string>
  [--dry-run]
  [--help]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：设置不可变的文件系统 ID。文件系统令牌不能替代此选项，也不能用于授予删除文件系统的权限。\[required]
- `--dry-run`：验证请求而不应用更改。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 删除一个文件系统：

    ```bash
    # Request asynchronous deletion and remove only the matching local credential after acceptance.
    ti fs delete-file-system --file-system-id <file-system-id>
    ```

- 预览文件系统删除：

    ```bash
    # Validate the selected file system without sending the deletion request.
    ti fs delete-file-system --file-system-id <file-system-id> --dry-run
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)