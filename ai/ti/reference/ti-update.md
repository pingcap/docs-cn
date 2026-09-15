---
title: ti update
summary: 检查或安装 TiDB Cloud CLI 的版本更新。
---

# ti update

检查或安装 TiDB Cloud CLI 的版本更新。此命令不会读取或修改 `~/.ti/` 下的设置、配置（Profile）、凭证、操作日志或其他状态数据。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti update
  [--check]
  [--dry-run]
  [--fail-if-update-available]
  [--help]
  [--target-version <string>]
  [--version]
```

## 选项 {#options}

- `--check`：检查是否有较新的 `ti` 版本可用，但不执行更新。
- `--dry-run`：显示更新计划，但不修改本地二进制文件。
- `--fail-if-update-available`：与 `--check` 一起使用时，如果有可用更新，则以退出码 1 退出。
- `--help`：显示帮助信息。
- `--target-version <string>`：目标 `ti` 版本，例如 `latest` 或 `vX.Y.Z`。\[default: latest]
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 检查是否有可用更新：

    ```bash
    # Compare the installed version with the latest GitHub release without changing files.
    ti update --check
    ```

- 当有可用更新时使 CI 作业失败：

    ```bash
    # Exit with code 1 when a newer release is available, without changing files.
    ti update --check --fail-if-update-available
    ```

- 预览更新：

    ```bash
    # Show the files and versions that an update would change.
    ti update --dry-run
    ```

- 安装指定版本：

    ```bash
    # Replace an eligible installation with the requested release version.
    ti update --target-version <version>
    ```

## 相关文档 {#related-documentation}

- [安装、配置和更新 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)