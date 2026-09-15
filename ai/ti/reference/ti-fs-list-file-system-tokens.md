---
title: ti fs list-file-system-tokens
summary: 列出单个 TiDB Cloud Filesystem 的令牌元信息。
---

# ti fs list-file-system-tokens

列出某个 Filesystem 的令牌。输出中绝不会包含令牌值。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公开预览阶段。其功能和命令行接口如有变更，恕不另行通知。

## 语法 {#syntax}

```text
ti fs list-file-system-tokens
  [--file-system-id <string>]
  [--fs-token <string>]
  [--include-expired]
  [--help]
  [--limit <int32>]
  [--offset <int32>]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：指定要列出其令牌的 Filesystem。使用 TiDB Cloud API 凭据时为必填；当 `--fs-token` 或 `TI_FS_TOKEN` 提供所有者令牌时为可选，因为 `ti` 会从该令牌中推导出 ID。
- `--fs-token <string>`：使用 Filesystem 所有者令牌为请求授予权限。如果省略，命令会使用 `TI_FS_TOKEN` 环境变量。如果两者都未提供，命令会使用为所选 Filesystem 本地存储的令牌。如果没有可用的 Filesystem 令牌，命令会使用已配置的 TiDB Cloud API 密钥。范围受限令牌不能列出令牌元信息。
- `--include-expired`：包含已过期的令牌元信息。已被（权限）回收的令牌不会由服务返回。
- `--help`：显示帮助信息。
- `--offset <int32>`：设置从 0 开始的令牌偏移 [default: 0]。
- `--limit <int32>`：设置返回的最大令牌数量，范围为 1 到 200 [default: 50]。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

## 示例 {#examples}

- 以文本格式列出当前令牌元信息：

    ```bash
    # Use token_id, not the non-unique token name, for later mutations.
    ti fs list-file-system-tokens \
      --file-system-id "<file-system-id>" \
      --output text
    ```

- 使用分页查看已过期的令牌元信息：

    ```bash
    # Request up to 100 rows starting at offset 0.
    ti fs list-file-system-tokens \
      --file-system-id "<file-system-id>" \
      --include-expired \
      --offset 0 \
      --limit 100
    ```

- 使用所有者令牌列出令牌元信息：

    ```bash
    # The owner token identifies the Filesystem, so --file-system-id is not needed.
    TI_FS_TOKEN="<owner-fs-token>" ti fs list-file-system-tokens --output text
    ```

## 相关文档 {#related-documentation}

- [`ti fs generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md)
- [`ti fs generate-file-system-scoped-token`](/ai/ti/reference/ti-fs-generate-file-system-scoped-token.md)
- [TiDB Cloud CLI Regions、安全性与限制](/ai/ti/reference/ti-regions-security-and-limitations.md)