---
title: ti fs update-file-system-extract-configuration
summary: 修改文件系统的媒体内容提取配置。
---

# ti fs update-file-system-extract-configuration

修改单个文件系统的可选镜像、音频或视频媒体内容提取配置。启用或替换 provider 时，会执行一次真实的 provider 验证请求，这可能会产生少量 provider 费用。启用后，文件系统中的媒体文件会被发送到所选 provider 进行媒体内容提取。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti fs update-file-system-extract-configuration
  --file-system-id <string>
  --media-type <string>
  [--dry-run]
  [--enabled <boolean>]
  [--help]
  [--prompt <string>]
  [--provider-api-base <string>]
  [--provider-model <string>]
  [--provider-protocol <string>]
  [--version]
```

## 选项 {#options}

- `--file-system-id <string>`：设置不可变的文件系统 ID。\[required]
- `--media-type <string>`：选择 `image`、`audio` 或 `video`。\[required]
- `--dry-run`：在不联系文件系统后端或 AI provider 的情况下验证该请求。
- `--enabled <boolean>`：显式启用或禁用媒体内容提取。输入 `true` 或 `false`。
- `--prompt <string>`：设置一个最大为 8 KiB 的 prompt。传入空字符串可恢复后端默认 prompt 行为。
- `--provider-api-base <string>`：设置有效的 HTTPS provider 基础 URL。
- `--provider-model <string>`：设置 provider 模型名称。
- `--provider-protocol <string>`：设置为 `openai`，或仅用于音频的 `qwen-asr`。默认值为 `openai`。
- `--help`：显示帮助信息。
- `--version`：显示版本信息。

有关所有命令共享的选项，请参见[全局选项](/ai/ti/reference/ti-cli-reference.md#global-options)。

provider API key 仅接受通过 `TI_FS_AI_PROVIDER_API_KEY` 提供。它会被发送到文件系统后端进行验证和加密存储，`ti` 不会在本地存储它，并且返回时只会以掩码形式显示。`openai` 支持镜像、音频和视频。Alibaba Cloud Model Studio Qwen ASR 可通过 `qwen-asr` 用于音频。其他服务仅在其实现了完全符合要求的 OpenAI-compatible contract 时才可用。不支持原生 Anthropic、Gemini、Vertex AI、Bedrock 和 Azure OpenAI 接口。

在发生超时或响应丢失后，不要盲目重试修改操作。provider 可能已经对验证收费，后端也可能已经保存了配置。请先运行对应的 describe 命令。

在交互式 shell 中启用 provider 之前，请先读取并导出其 API key，避免将其写入 shell history：

```bash
printf 'Provider API key: ' >&2
read -r -s TI_FS_AI_PROVIDER_API_KEY
printf '\n' >&2
export TI_FS_AI_PROVIDER_API_KEY
```

在 CI 中，请通过 masked secret 注入 `TI_FS_AI_PROVIDER_API_KEY`。命令执行完成后，取消设置该变量。

## 示例 {#examples}

- 使用 OpenAI-compatible provider 启用镜像媒体内容提取：

    ```bash
    # Configure extraction using the provider key from TI_FS_AI_PROVIDER_API_KEY.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --enabled true \
      --provider-api-base https://api.openai.com/v1 \
      --provider-model <vision-model>
    ```

- 为音频启用 Alibaba Cloud Model Studio Qwen ASR：

    ```bash
    # Use the DashScope OpenAI-compatible endpoint with the qwen-asr protocol.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type audio \
      --enabled true \
      --provider-api-base https://dashscope.aliyuncs.com/compatible-mode/v1 \
      --provider-model qwen3-asr-flash \
      --provider-protocol qwen-asr
    ```

- 仅修改已启用镜像配置的 prompt：

    ```bash
    # Keep the existing provider credentials and update only extraction instructions.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --prompt "Describe the image and return searchable attributes."
    ```

- 禁用镜像媒体内容提取：

    ```bash
    # Remove the custom image provider configuration without changing normal file access.
    ti fs update-file-system-extract-configuration \
      --file-system-id <file-system-id> \
      --media-type image \
      --enabled false
    ```

## 相关文档 {#related-documentation}

- [`ti fs describe-file-system-extract-configuration`](/ai/ti/reference/ti-fs-describe-file-system-extract-configuration.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)