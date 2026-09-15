---
title: ti fs describe-file-system-extract-configuration
summary: 描述 TiDB Cloud Filesystem 的媒体内容提取配置。
---

# ti fs describe-file-system-extract-configuration

显示 Filesystem 的 image、audio 或 video 媒体内容提取配置。此配置为可选项；如果未自定义，不会影响 Filesystem 的正常操作。此命令需要 TiDB Cloud API 凭证，不使用 Filesystem 访问令牌。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs describe-file-system-extract-configuration
  --file-system-id <string>
  --media-type <string>
  [--help]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：设置不可变的 Filesystem ID。\[必需]
- `--media-type <string>`：选择 `image`、`audio` 或 `video`。\[必需]
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 查看 image 媒体内容提取：

    ```bash
    # Show whether image extraction uses a custom, default, or absent provider configuration.
    ti fs describe-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image
    ```

- 仅输出生效的 provider 来源：

    ```bash
    # Return custom, default, or none for use in a script.
    ti fs describe-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type audio \
      --query source \
      --output text
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)