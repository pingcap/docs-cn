---
title: ti fs disable-file-system-token
summary: 临时禁用文件系统令牌而不删除它。
---

# ti fs disable-file-system-token

临时禁用一个文件系统令牌而不撤销它。你稍后可以使用 [`ti fs enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) 重新启用该令牌。对于已知被本地挂载使用的令牌，必须先执行刷写并卸载。使用所有者令牌进行身份验证时，只能禁用范围受限令牌；使用 TiDB Cloud API key 时，则可以禁用任意类型的令牌。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs disable-file-system-token
  --token-id <string>
  [--file-system-id <string>]
  [--fs-token <string>]
  [--dry-run]
  [--help]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：指定拥有该令牌的 文件系统。使用 TiDB Cloud API 凭证时为必需；当所有者令牌提供该 ID 时则为可选。
- `--token-id <string>`：指定由 list 命令返回的不可变令牌 ID。此选项为必需。
- `--fs-token <string>`：使用文件系统所有者令牌为该请求授予权限。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 文件系统 本地存储的令牌。如果没有可用的文件系统令牌，命令会使用已配置的 TiDB Cloud API keys。
- `--dry-run`：验证凭证、标识符以及已知的本地挂载冲突，但不禁用令牌。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 在下线其本地挂载后禁用令牌：

    ```bash
    # Drain and unmount first when this token backs a mount on the current machine.
    ti fs drain-file-system --mount-path /path/to/workspace
    ti fs unmount-file-system --mount-path /path/to/workspace
    ti fs disable-file-system-token \
      --file-system-id "<file-system-id>" \
      --token-id "<token-id>"
    ```

- 使用所有者令牌禁用范围受限令牌：

    ```bash
    # Inject TI_FS_TOKEN from a secret manager. The owner token identifies the file system.
    # Drain any local mount that uses the target token first.
    ti fs disable-file-system-token \
      --token-id "<scoped-token-id>"
    ```

## 相关文档 {#related-documentation}

- [令牌管理授权](/ai/ti/reference/ti-filesystem.md#token-management-authorization)
- [`ti fs enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md)
- [`ti fs delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md)