---
title: ti fs fork-layer
summary: 在文件系统中派生一个写时复制的子层。
---

# ti fs fork-layer

从父层的当前状态或其某个检查点创建一个可写的子层。对子层的更改不会修改父层。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs fork-layer
  --parent-layer-ref <string>
  [--actor-id <string>]
  [--checkpoint-id <string>]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--layer-id <string>]
  [--layer-name <string>]
  [--version]
```

## 选项 {#options}

- `--parent-layer-ref <string>`：父层 ID、唯一名称，或[标签引用](/ai/ti/reference/ti-filesystem.md#layer-references)。\[必需]
- `--actor-id <string>`：用于标识子层所有者的 Actor ID。
- `--checkpoint-id <string>`：将子层固定到父层的此检查点。如果省略，则固定到已序列化的父层 tip。
- `--dry-run`：验证请求而不应用更改。
- `--file-system-id <string>`：选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`：设置文件系统访问令牌。如果省略，此命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，此命令会使用为所选文件系统在本地存储的令牌。
- `--help`：显示帮助信息。
- `--layer-id <string>`：稳定的子层 ID。如果省略，则由服务生成。
- `--layer-name <string>`：便于人类识别的子层名称。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 从父层 tip 派生：

    ```bash
    # Start an independent writable timeline at the parent's current serialized tip.
    ti fs fork-layer --file-system-id <file-system-id> --parent-layer-ref research-base --layer-name experiment-a --actor-id agent-a
    ```

- 从稳定的检查点派生：

    ```bash
    # Continue from an earlier review boundary without changing the original timeline.
    ti fs fork-layer --file-system-id <file-system-id> --parent-layer-ref research-base --checkpoint-id seed --layer-name experiment-b --actor-id agent-b
    ```

> **Note:**
>
> 层名称在逻辑删除后仍然可见，因此可能会产生歧义。自动化程序应捕获并使用返回的层 ID。

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [`ti fs mount-file-system`](/ai/ti/reference/ti-fs-mount-file-system.md)