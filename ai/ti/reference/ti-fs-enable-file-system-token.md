---
title: ti fs enable-file-system-token
summary: 启用已禁用的 TiDB Cloud Filesystem 令牌。
---

# ti fs enable-file-system-token

重新启用已禁用的 Filesystem 访问令牌。该令牌大约需要 10 秒后才能恢复可用。使用所有者令牌进行身份验证时，只能启用范围受限令牌；TiDB Cloud API key 则可以启用任意类型的令牌。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于 public preview 阶段。其功能和命令行接口可能会在不另行通知的情况下发生变更。

## 语法 {#syntax}

```text
ti fs enable-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
  [--help]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：指定拥有该令牌的 Filesystem。使用 TiDB Cloud API 凭据时为必需；当由所有者令牌提供该 ID 时则为可选。
- `--token-id <string>`：指定由 list 命令返回的不可变令牌 ID。此选项为必需。
- `--fs-token <string>`：使用 Filesystem 所有者令牌为该请求授予权限。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 在本地存储的令牌。如果没有可用的 Filesystem 访问令牌，命令会使用已配置的 TiDB Cloud API keys。
- `--dry-run`：验证请求，但不更改远端令牌状态。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 启用一个已知令牌：

    ```bash
    # Allow about 10 seconds for all authentication caches to observe the change.
    ti fs enable-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<token-id>"
    ```

- 使用所有者令牌启用范围受限令牌：

    ```bash
    # The owner token identifies and authorizes token management for its Filesystem.
    TI_FS_TOKEN="<owner-fs-token>" ti fs enable-file-system-token \
      --token-id "<scoped-token-id>"
    ```

## 相关文档 {#related-documentation}

- [令牌管理授权](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md)
- [`ti fs disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md)