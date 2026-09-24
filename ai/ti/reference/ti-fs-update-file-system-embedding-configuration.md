---
title: ti fs update-file-system-embedding-configuration
summary: 替换文件系统的向量嵌入配置。
---

# ti fs update-file-system-embedding-configuration

为某个文件系统启用或禁用可选的应用管理向量嵌入。启用时会执行一次真实的提供方验证请求，这可能会产生少量提供方费用。启用后，文本或提取出的描述会发送到所选的嵌入提供方。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs update-file-system-embedding-configuration
  --enabled <boolean>
  --file-system-id <string>
  [--dry-run]
  [--help]
  [--provider-api-base <string>]
  [--provider-model <string>]
  [--version]
```

## 选项 {#options}

- `--enabled <boolean>`：输入 `true` 并提供完整的提供方配置，或输入 `false` 且不带提供方选项。\[required]
- `--file-system-id <string>`：设置不可变的文件系统 ID。\[required]
- `--dry-run`：在不联系文件系统后端或嵌入提供方的情况下验证请求。
- `--provider-api-base <string>`：设置有效的、兼容 OpenAI 的 HTTPS 提供方基础 URL。
- `--provider-model <string>`：设置一个恰好返回 1024 维的嵌入模型。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

提供方 API 密钥仅接受通过 `TI_FS_AI_PROVIDER_API_KEY` 传入。它会被发送到文件系统后端以进行验证和加密存储，`ti` 不会在本地存储该密钥，并且返回时只会以掩码形式显示。向量嵌入要求严格兼容 OpenAI 的 `/v1/embeddings` 协议。原生提供方接口不受支持。

如果某个文件系统的 `source` 为 `database_auto`，则它使用数据库管理的向量嵌入，无法通过此命令进行更改。在发生超时或响应丢失后，请不要盲目重试修改。请先运行 describe 命令，以确定修改是否已成功。

## 示例 {#examples}

- 启用应用管理的向量嵌入：

    ```bash
    # Read the provider key without echoing it or storing it in shell history.
    printf 'Provider API key: ' >&2
    read -r -s TI_FS_AI_PROVIDER_API_KEY
    printf '\n' >&2
    export TI_FS_AI_PROVIDER_API_KEY

    # Configure a model that returns exactly 1024 dimensions.
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model text-embedding-3-small
    unset TI_FS_AI_PROVIDER_API_KEY
    ```

- 在不验证或保存提供方配置的情况下预览启用操作：

    ```bash
    # Read the provider key without echoing it or storing it in shell history.
    printf 'Provider API key: ' >&2
    read -r -s TI_FS_AI_PROVIDER_API_KEY
    printf '\n' >&2
    export TI_FS_AI_PROVIDER_API_KEY

    # Validate local inputs and show a redacted request plan.
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model text-embedding-3-small \
      --dry-run
    unset TI_FS_AI_PROVIDER_API_KEY
    ```

- 禁用应用管理的向量嵌入：

    ```bash
    # Remove custom embedding configuration without changing normal file access.
    ti fs update-file-system-embedding-configuration \
      --file-system-id <file-system-id> \
      --enabled false
    ```

## 相关文档 {#related-documentation}

- [`ti fs describe-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-describe-file-system-embedding-configuration.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)