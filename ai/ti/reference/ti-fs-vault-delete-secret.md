---
title: ti fs-vault delete-secret
summary: 从 file system Vault 中删除一个 Secret。
---

# ti fs-vault delete-secret

删除一个 file system Vault Secret。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault delete-secret
  --secret-name <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--secret-name <string>`：Vault Secret 名称。\[必需]
- `--dry-run`：验证请求，但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 删除一个 Secret：

    ```bash
    # Remove the selected secret and its fields from the Vault.
    ti fs-vault delete-secret --file-system-id <file-system-id> --secret-name db-prod
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)