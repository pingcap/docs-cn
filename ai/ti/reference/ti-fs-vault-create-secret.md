---
title: ti fs-vault create-secret
summary: 在 Filesystem Vault 中创建 Secret。
---

# ti fs-vault create-secret

通过一个或多个 `NAME=value` 或 `NAME=@file` 字段创建 Secret。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs-vault create-secret
  --field <string>
  --secret-name <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--field <string>`：Secret 字段赋值，格式为 `key=value`、`key=@file` 或 `key=-`；可重复使用。`key=-` 表示从标准输入读取。如果多个字段都使用 `-`，则每个字段都会接收相同的标准输入值。\[必需]
- `--secret-name <string>`：Vault Secret 名称。\[必需]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略此选项，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 通过值和文件创建 Secret：

    ```bash
    # Keep the password out of the command line by reading it from a local file.
    ti fs-vault create-secret --file-system-id <file-system-id> --secret-name db-prod --field DB_URL=mysql://example --field PASSWORD=@./password.txt
    ```

- 从标准输入读取 Secret 字段：

    ```bash
    # Supply a sensitive token through a pipe instead of a process argument.
    printf '%s' "$API_TOKEN" | ti fs-vault create-secret --file-system-id <file-system-id> --secret-name api-dev --field TOKEN=-
    ```

- 预览 Secret 创建：

    ```bash
    # Validate field assignments without storing secret material.
    ti fs-vault create-secret --file-system-id <file-system-id> --secret-name api-dev --field TOKEN=@./token.txt --dry-run
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)