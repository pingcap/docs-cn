---
title: ti fs delete-layer
summary: 放弃一个文件系统 layer。
---

# ti fs delete-layer

放弃一个 layer，但不会擦除其历史记录。如果该 layer 有存活的后代，除非指定 `--cascade`，否则该命令会失败；指定后会先放弃这些后代。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs delete-layer
  --layer-ref <string>
  [--cascade]
  [--dry-run]
  [--file-system-id <string>]
  [--fs-token <string>]
  [--help]
  [--version]
```

## 选项 {#options}

- `--layer-ref <string>`: layer ID、唯一名称或[标签引用](/ai/ti/reference/ti-filesystem.md#layer-references)。\[必需]
- `--cascade`: 在放弃所选 layer 之前，先放弃仍存活的后代。
- `--dry-run`: 验证请求但不应用更改。
- `--file-system-id <string>`: 选择文件系统。你也可以设置 `TI_FS_FILE_SYSTEM_ID`。
- `--fs-token <string>`: 设置文件系统访问令牌。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选文件系统本地存储的令牌。
- `--help`: 显示帮助信息。
- `--version`: 显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 放弃一个被拒绝的叶子时间线：

    ```bash
    # Deletion fails when the selected layer still has live descendants.
    ti fs delete-layer --file-system-id <file-system-id> --layer-ref experiment-a
    ```

- 放弃一个由测试拥有的子树：

    ```bash
    # Cascade is explicit and abandons descendants before the selected layer.
    ti fs delete-layer --file-system-id <file-system-id> --layer-ref experiment-root --cascade
    ```

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [`ti fs list-layer-chain`](/ai/ti/reference/ti-fs-list-layer-chain.md)