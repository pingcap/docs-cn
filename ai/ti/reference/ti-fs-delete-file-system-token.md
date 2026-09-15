---
title: ti fs delete-file-system-token
summary: 永久（权限）回收 TiDB Cloud Filesystem 访问令牌。
---

# ti fs delete-file-system-token

永久（权限）回收一个 Filesystem 访问令牌。变更传播完成后，该令牌将停止用于身份验证，并且不再出现在列表结果中。所有者令牌可以（权限）回收同一 Filesystem 中的任意一种令牌；范围受限令牌不能使用此命令。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs delete-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
  [--help]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：指定拥有该令牌的 Filesystem。使用 TiDB Cloud API 凭证时为必填；当由所有者令牌提供该 ID 时为可选。
- `--token-id <string>`：指定由 list 命令返回的不可变令牌 ID。此选项为必填。
- `--fs-token <string>`：使用所有者 Filesystem 访问令牌为该请求授予权限。如果省略，命令将使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令将使用为所选 Filesystem 本地存储的令牌。如果没有可用的 Filesystem 访问令牌，命令将使用已配置的 TiDB Cloud API keys。
- `--dry-run`：校验凭证、标识符以及已知的本地挂载冲突，而不（权限）回收该令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 在验证替代令牌后（权限）回收旧令牌：

    ```bash
    # Revocation is permanent; use disable first when you need a reversible rollout.
    ti fs delete-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<old-token-id>"
    ```

- 使用所有者令牌（权限）回收令牌：

    ```bash
    # The owner token identifies the Filesystem; use the immutable ID of the token being revoked.
    TI_FS_TOKEN="<owner-fs-token>" ti fs delete-file-system-token \
      --token-id "<old-token-id>"
    ```

## 相关文档 {#related-documentation}

- [令牌管理授权](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [`ti fs disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md)