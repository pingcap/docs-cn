---
title: ti fs-vault unmount-vault
summary: 卸载一个 Filesystem Vault 视图。
---

# ti fs-vault unmount-vault

卸载本地的 Filesystem Vault 文件系统。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs-vault unmount-vault
  --mount-path <string>
  [--dry-run]
  [--force]
  [--help]
  [--ignore-absent]
  [--timeout <duration>]
  [--version]
```

## 选项 {#options}

- `--mount-path <string>`：本地挂载路径。\[required]
- `--dry-run`：验证请求但不应用更改。
- `--force`：如果优雅卸载超时，则强制终止挂载进程。
- `--help`：显示帮助信息。
- `--ignore-absent`：当该路径不存在 `ti fs-vault` 挂载状态时，返回成功。
- `--timeout <duration>`：等待挂载进程退出的时间。\[default: `30s`]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 卸载一个 Vault 视图：

    ```bash
    # Detach the local read-only Vault mount.
    ti fs-vault unmount-vault --mount-path ./vault
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem Vault CLI 命令参考](/ai/ti/reference/ti-filesystem-vault.md)