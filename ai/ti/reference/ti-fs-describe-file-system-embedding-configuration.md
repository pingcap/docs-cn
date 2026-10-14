---
title: ti fs describe-file-system-embedding-configuration
summary: 描述文件系统的向量嵌入配置。
---

# ti fs describe-file-system-embedding-configuration

显示文件系统的向量嵌入配置。此配置为可选项；如果未自定义，不会影响文件系统的正常操作。此命令需要 TiDB Cloud API 凭证，不使用文件系统访问令牌。

`source` 字段用于报告该配置是 `custom`、`default`、`none` 还是 `database_auto`。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs describe-file-system-embedding-configuration
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

- 查看生效中的嵌入配置：

    ```bash
    # Show provider metadata, masked credentials, source, and generation.
    ti fs describe-file-system-embedding-configuration \
      --file-system-id <file-system-id>
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)