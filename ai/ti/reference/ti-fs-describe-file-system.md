---
title: ti fs describe-file-system
summary: 描述远程 TiDB Cloud Filesystem。
---

# ti fs describe-file-system

显示 Filesystem 的详细信息，包括其显示名称、标签、放置位置、状态、配额和使用情况。此命令需要 TiDB Cloud API 凭证，不使用 Filesystem 访问令牌。

输出中包含 `has_local_token`，用于指示此机器是否具有匹配的本地令牌。可用时，配额数据还包括媒体和视频媒体内容提取限制及使用情况。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs describe-file-system
  --file-system-id <string>
  [--help]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：设置不可变的文件系统 ID。\[必需]
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 描述一个文件系统：

    ```bash
    # Return remote status and whether this machine has a matching local token.
    ti fs describe-file-system --file-system-id <file-system-id>
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)