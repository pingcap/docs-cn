---
title: 使用 TiDB Cloud Filesystem 在并行代理之间共享只读数据集
summary: 上传一份非结构化数据集，并将同一个只读挂载的命名空间暴露给多个代理工作进程。
---

# 使用 TiDB Cloud Filesystem 在并行代理之间共享只读数据集

此工作流让多个短生命周期的工作进程共享同一份语料，而无需将单独的副本下载到每个沙箱中。当并行的文档处理代理或评估代理需要一致地访问相同的 PDF、镜像、日志或模型工件时，可以使用此方案。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 工作原理 {#how-it-works}

所有者只需上传一次语料，并为每个工作进程创建一个范围受限的只读 Filesystem 访问令牌。每个工作进程都选择同一个 Filesystem，并以只读方式挂载该语料，因此普通工具无需存储 SDK 即可遍历同一个公共命名空间。这样可以减少启动时间，并避免生成彼此独立的时间点副本。如果工作进程需要产出结果，应将结果写入另一个可写的输出 Filesystem 中的不同路径，而不是写入数据集所在的 Filesystem。

## 前提条件 {#prerequisites}

- 在一台可信机器上安装并配置 TiDB Cloud CLI。
- 在每个工作进程中安装 TiDB Cloud CLI 以及所需的挂载依赖项。
- 在可信机器上安装 `jq`。
- 使用安全的 Secret 管理器或加密的工作进程输入来传输令牌。

## 第 1 步：上传语料 {#step-1-upload-the-corpus}

在可信机器上执行：

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export TI_FS_FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"

ti fs copy-file \
  --from-local ./corpus \
  --to-remote /datasets/corpus \
  --recursive

ti fs find-files \
  --path /datasets/corpus \
  --file-name-pattern "*.pdf" \
  --output text

# Create one short-lived, read-only scoped token per worker.
ti fs generate-file-system-scoped-token \
  --file-system-id "$TI_FS_FILE_SYSTEM_ID" \
  --subject worker-1 \
  --ttl 24h \
  --allow /datasets/corpus:read,list > ./worker-1-token.json
```

通过 Secret 管理器传输 `worker-1-token.json` 中的 `fs_token` 以及 Filesystem 的 Region 代码。对每个工作进程使用唯一的 subject 重复执行令牌生成命令。所有者令牌仅保留在可信机器上，并在安全存储这些令牌后删除这些 JSON 文件。

## 第 2 步：在每个工作进程中挂载 {#step-2-mount-in-each-worker}

> **Warning:**
>
> 为每个工作进程分配一个范围受限令牌，该令牌仅允许在语料路径下执行 `read` 和 `list`。`--read-only` 挂载选项可以防止通过挂载发生意外写入，但不会改变令牌本身的权限。

将工作进程的范围受限令牌注入为 `TI_FS_TOKEN`，并将 `TI_REGION_CODE` 设置为 Filesystem 所在 Region，然后执行：

```bash
mkdir -p "$HOME/corpus"
ti fs mount-file-system \
  --mount-path "$HOME/corpus" \
  --remote-path /datasets/corpus \
  --read-only
```

工作进程可以在无需存储 SDK 的情况下使用标准工具：

```bash
find "$HOME/corpus" -type f -name '*.pdf' -print
```

## 清理 {#cleanup}

在终止每个工作进程之前，先卸载其中挂载的 Filesystem：

```bash
ti fs unmount-file-system --mount-path "$HOME/corpus"
```

在所有工作进程都卸载 Filesystem 后，如果你不再需要该数据集，可在可信机器上将其删除：

```bash
rm -f ./filesystem.json ./worker-*-token.json
ti fs delete-file-system --file-system-id "$TI_FS_FILE_SYSTEM_ID"
```

## 安全与运维说明 {#security-and-operational-notes}

- 不要将所有者令牌分发给工作进程。应为每个工作进程生成单独的短期范围受限令牌，以便通过凭证强制执行只读访问。
- 如果工作进程要写入同一个输出 Filesystem，请按代理或运行 ID 对结果路径进行分区。
- 在无法使用 FUSE 或 WebDAV 挂载的平台上，可直接使用 `read-file`、`find-files` 和 `copy-file --to-local`。

## 后续内容 {#what-s-next}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [在代理沙箱中使用 Filesystem](/ai/ti/guides/ti-agent-sandbox-example.md)
- [TiDB Cloud CLI Regions、安全性与限制](/ai/ti/reference/ti-regions-security-and-limitations.md)