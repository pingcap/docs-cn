---
title: ti fs create-file-system
summary: 创建一个 TiDB Cloud Filesystem。
---

# ti fs create-file-system

创建一个 Filesystem，并返回其 ID 和所有者令牌。CLI 会在当前配置（Profile）中存储并选择该令牌。使用 `--wait` 可等待 Filesystem 准备就绪后再返回。

你还可以选择设置显示名称和标签。这些值会显示在 `list-file-systems` 和 `describe-file-system` 的输出中，但不会在后续命令中用于选择该 Filesystem。

> **重要：**
>
> 服务不会再次显示初始所有者令牌。如果 CLI 警告无法存储该令牌，请在关闭终端前保存返回的值。如果本地凭证之后丢失，请使用 TiDB Cloud API 凭证配合 [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md) 创建一个替代的所有者令牌。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs create-file-system
  [--display-name <string>]
  [--dry-run]
  [--help]
  [--label <string>]
  [--version]
  [--wait]
```

## 选项 {#options}

- `--display-name <string>`：设置一个长度为 4 到 64 个字符的显示名称，供 Filesystem 清单命令显示。该值不会在后续命令中用于选择该 Filesystem。
- `--dry-run`：验证请求，但不应用更改。
- `--help`：显示帮助信息。
- `--label <string>`：添加一个组织内可见的 `key=value` 标签。重复此选项最多可添加 30 个标签。请勿在标签中放入 Secret 或个人数据。
- `--version`：显示版本信息。
- `--wait`：等待创建的文件系统变为活动状态。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 创建一个 Filesystem，并等待其准备就绪：

    ```bash
    # Wait until the new Filesystem root is readable before returning.
    ti fs create-file-system \
      --display-name agent-workspace \
      --label environment=development \
      --label team=ai \
      --wait
    ```

- 异步创建一个 Filesystem：

    ```bash
    # Return after provisioning is accepted so work can continue in parallel.
    ti fs create-file-system
    ```

- 预览 Filesystem 创建：

    ```bash
    # Validate credentials, placement, and the request without provisioning storage.
    ti fs create-file-system --dry-run
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)