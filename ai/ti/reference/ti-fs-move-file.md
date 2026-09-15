---
title: ti fs move-file
summary: 在 TiDB Cloud Filesystem 中移动文件。
---

# ti fs move-file

移动或重命名远程路径。该命令的别名是 `ti fs mv`。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs move-file
  --from-remote <string>
  --to-remote <string>
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--overwrite]
  [--version]
```

## 选项 {#options}

- `--from-remote <string>`：源文件路径。\[必需]
- `--to-remote <string>`：目标文件路径。\[必需]
- `--dry-run`：验证请求，但不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置 Filesystem 访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 在本地存储的令牌。
- `--help`：显示帮助信息。
- `--overwrite`：替换已存在的目标文件。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 移动远程文件：

    ```bash
    # Rename or relocate an object entirely within the selected Filesystem.
    ti fs move-file --file-system-id <file-system-id> --from-remote /draft.md --to-remote /reports/final.md
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)