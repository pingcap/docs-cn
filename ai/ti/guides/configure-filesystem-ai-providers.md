---
title: 配置 TiDB Cloud Filesystem AI 提供方
summary: 了解如何使用 CLI 检查并配置 TiDB Cloud Filesystem 的媒体内容提取和向量嵌入 provider。
---

# 配置 TiDB Cloud Filesystem AI 提供方

TiDB Cloud Filesystem 可以选择性地从媒体文件中提取文本，并为存储的内容生成向量嵌入。要启用这些能力，你可以通过 CLI 配置一个或多个 AI provider。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 获取目标 Filesystem ID。
- 获取所选 AI provider 所需的 API key。

配置命令需要 TiDB Cloud API 凭证以及明确指定的 Filesystem ID。通过 `TI_FS_AI_PROVIDER_API_KEY` 设置 provider key。CLI 不会在本地持久化保存该 key。Filesystem 服务会将其加密存储，并且在后续配置输出中仅返回脱敏后的值。

对于交互式 shell，可按如下方式读取并导出 provider key，以避免其进入 shell 历史记录：

```bash
printf 'Provider API key: ' >&2
read -r -s TI_FS_AI_PROVIDER_API_KEY
printf '\n' >&2
export TI_FS_AI_PROVIDER_API_KEY
```

在 CI 中，请通过 masked secret 注入 `TI_FS_AI_PROVIDER_API_KEY`。完成 provider 配置后，请取消设置该变量。

> **Note:**
>
> 当你启用、重新启用或替换 provider 配置时，Filesystem 服务会向 provider endpoint 发送一个内置的小型请求，以验证凭证、连通性以及模型响应。此验证请求可能会产生 provider 费用。仅禁用或仅修改 prompt 的更新不会发起验证请求。

## 检查媒体内容提取配置 {#inspect-media-extraction-configuration}

读取某种媒体类型的生效媒体内容提取配置：

```shell
ti fs describe-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image
```

## 修改媒体内容提取配置 {#update-media-extraction-configuration}

使用 [`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md) 启用、修改或禁用 image、audio 或 video 的媒体内容提取。例如，通过兼容 OpenAI 的 provider 配置 image 提取：

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model "<vision-model>" \
  --provider-protocol openai
```

`openai` 协议支持 image、audio 和 video 的媒体内容提取。`qwen-asr` 协议仅支持通过 Alibaba Cloud Model Studio 进行 audio 提取。如果其他 provider 的 endpoint 实现了所需的 OpenAI-compatible API contract，也可能可以正常工作。当前不支持 Anthropic、Gemini、Vertex AI、Amazon Bedrock 和 Azure OpenAI 的原生接口。

如需禁用某种媒体类型的媒体内容提取：

```shell
ti fs update-file-system-extract-configuration \
  --file-system-id "<file-system-id>" \
  --media-type image \
  --enabled false
```

## 检查向量嵌入配置 {#inspect-embedding-configuration}

查看向量嵌入是由应用程序还是数据库管理：

```shell
ti fs describe-file-system-embedding-configuration \
  --file-system-id "<file-system-id>"
```

## 修改向量嵌入配置 {#update-embedding-configuration}

使用 [`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md) 修改可选的应用程序管理向量嵌入配置。例如：

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled true \
  --provider-api-base https://api.openai.com/v1 \
  --provider-model text-embedding-3-small
```

应用程序管理的向量嵌入要求使用兼容 OpenAI 的 endpoint，并返回 1024 维向量。该功能适用于 Shared Filesystems，以及生效 embedding mode 为 `fts_only` 的 Native Filesystems。如果某个 Native Filesystem 使用数据库管理的自动向量嵌入，服务会拒绝此修改，并报告 `source=database_auto`。

完成 provider 配置后，请从当前 shell 中移除该 key：

```shell
unset TI_FS_AI_PROVIDER_API_KEY
```

如需禁用该配置：

```shell
ti fs update-file-system-embedding-configuration \
  --file-system-id "<file-system-id>" \
  --enabled false
```

## 配置后的数据流 {#data-flow-after-configuration}

启用媒体内容提取后，Filesystem 服务会将媒体内容发送到已配置的提取 provider。然后，它会将提取出的文本或描述发送到已配置的向量嵌入 provider。请根据你的数据选择合适的 provider 账户和数据保留策略。

如果由于超时、响应丢失或其他不明确的网络错误导致修改失败，请在重试前先运行对应的 `describe-file-system-*-configuration` 命令。即使 CLI 没有收到响应，provider 验证请求也可能已经成功并产生费用。

## 下一步 {#what-s-next}

- [使用 TiDB Cloud Filesystem 数据](/ai/ti/guides/work-with-filesystem-data.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)