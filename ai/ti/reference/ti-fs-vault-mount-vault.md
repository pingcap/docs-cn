---
title: ti fs-vault mount-vault
summary: 挂载一个只读的文件系统 Vault 视图。
---

# ti fs-vault mount-vault

将可读的 Vault 字段挂载为本地只读 FUSE 文件系统。

在 Linux 上，请安装 FUSE3 并确保 `/dev/fuse` 可用。在 macOS 上，请安装 macFUSE 并批准其系统扩展。Windows 不支持 Vault 挂载；请改用 `read-secret`、`list-secrets` 或 `run-with-secret`。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault mount-vault
  --mount-path <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--ready-timeout <duration>]
  [--vault-token <string>]
  [--version]
```

## 选项 {#options}

- `--mount-path <string>`：本地挂载路径。\[必需]
- `--dry-run`：验证请求但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统所有者令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统在本地存储的令牌。对于委派认证，请改用 `--vault-token` 或 `TI_VAULT_TOKEN`。
- `--help`：显示帮助信息。
- `--ready-timeout <duration>`：等待后台挂载就绪的时间。\[默认值：`30s`]
- `--vault-token <string>`：委派的 `ti fs-vault` 令牌；推荐使用 `TI_VAULT_TOKEN`。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

在运行以下任一示例之前，请先注入一个 Vault 委派令牌。在交互式 shell 中，可以读取并导出该令牌，而不将其写入 shell 历史记录：

```bash
printf 'Delegated Vault token: ' >&2
read -r -s TI_VAULT_TOKEN
printf '\n' >&2
export TI_VAULT_TOKEN
```

当不再需要该挂载时，请将其卸载并运行 `unset TI_VAULT_TOKEN`。

- 挂载一个委派的 Vault 视图：

    ```bash
    # Expose only the paths allowed by TI_VAULT_TOKEN.
    ti fs-vault mount-vault --file-system-id <file-system-id> --mount-path ./vault
    ```

- 为 Vault 挂载就绪预留更多时间：

    ```bash
    # Increase the readiness timeout on a slower host or network.
    ti fs-vault mount-vault --file-system-id <file-system-id> --mount-path ./vault --ready-timeout 60s
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)