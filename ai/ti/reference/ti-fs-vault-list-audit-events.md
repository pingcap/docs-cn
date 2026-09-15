---
title: ti fs-vault list-audit-events
summary: 列出 Filesystem Vault 审计事件。
---

# ti fs-vault list-audit-events

列出 Vault 审计事件，并可选择按 agent、Secret 和时间进行过滤。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault list-audit-events
  [--agent-id <string>]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--limit <int32>]
  [--secret-name <string>]
  [--since <duration>]
  [--version]
```

## 选项 {#options}

- `--agent-id <string>`：按 agent ID 过滤。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。
- `--help`：显示帮助信息。
- `--limit <int32>`：返回的最大事件数。\[default: 100]
- `--secret-name <string>`：按 Vault Secret 名称过滤。
- `--since <duration>`：客户端侧的相对时间过滤，例如 `24h`。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 列出某个 Secret 的事件：

    ```bash
    # Inspect recent access and mutation events for the selected secret.
    ti fs-vault list-audit-events --file-system-id <file-system-id> --secret-name db-prod --limit 20
    ```

- 列出某个 agent 的最近事件：

    ```bash
    # Filter the audit trail to one delegated identity and time range.
    ti fs-vault list-audit-events --file-system-id <file-system-id> --agent-id deploy-agent --since 24h
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)