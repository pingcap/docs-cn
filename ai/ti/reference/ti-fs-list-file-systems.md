---
title: ti fs list-file-systems
summary: 列出指定 Region 中的远程文件系统。
---

# ti fs list-file-systems

列出在所选 Region 中，使用当前所选 TiDB Cloud 凭证可访问的所有 文件系统。结果包括显示名称、标签、状态、配额与使用量，以及 `has_local_token`，该字段表示此机器上是否存在匹配的本地 token。结果中绝不会包含 token 值。

在可用时，配额数据还包括媒体和视频内容提取限制及使用量。

CLI 会自动检索服务的所有分页结果，并返回一份完整且有序的结果，因此此命令不提供分页选项。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs list-file-systems
  [--display-name <string>]
  [--help]
  [--label <string>]
  [--version]
```

## 选项 {#options}

- `--display-name <string>`：按大小写敏感的 display-name 子字符串进行过滤。这不是精确的资源查找。
- `--help`：显示帮助信息。
- `--label <string>`：按一个精确的 `key=value` 标签进行过滤。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 列出远程管理的 文件系统：

    ```bash
    # Return the remote inventory for the profile's region without exposing tokens.
    ti fs list-file-systems
    ```

- 按显示元信息过滤 文件系统：

    ```bash
    # Match a display-name substring and one exact organization-visible label.
    ti fs list-file-systems \
      --display-name workspace \
      --label environment=production
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)