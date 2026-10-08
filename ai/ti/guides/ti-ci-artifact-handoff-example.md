---
title: 使用 TiDB Cloud Filesystem 在隔离的作业之间交接 CI 制品
summary: 将构建输出持久化到 TiDB Cloud Filesystem，并在后续的 CI 作业中使用，而无需复制完整的 TiDB Cloud CLI 配置（Profile）。
---

# 使用 TiDB Cloud Filesystem 在隔离的作业之间交接 CI 制品

此工作流使用文件系统作为隔离的 CI 作业或 runner 之间的持久交接点。当构建输出需要在生产者作业结束后继续保留，并在后续消费者作业中可用，同时又不想引入特定于提供商的制品 API、保留模型和下载工作流时，可以使用此方案。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 工作原理 {#how-it-works}

该流水线会将一个文件系统访问令牌和 Region 同时注入到两个作业中。该令牌用于标识文件系统。生产者会将输出上传到特定于运行的路径下，例如 `/ci/${RUN_ID}/`，而消费者则会在另一台 runner 上从该精确路径下载或流式读取数据。两个作业都不需要 TiDB Cloud API key，也不需要复制 `~/.ti/` 目录。

## 前提条件 {#prerequisites}

在一台受信任的机器上[创建一个文件系统](/tidb-cloud-filesystem/manage-filesystem-resources.md#create-a-file-system)，并将以下值保存为受保护的 CI Secret 或变量：

```text
TI_FS_TOKEN
TI_REGION_CODE
```

使用 CI 生成的运行标识符（例如 `RUN_ID`）来隔离并发流水线。

## 生产者作业 {#producer-job}

构建制品，然后上传：

```bash
tar -czf app.tar.gz ./dist
ti fs copy-file \
  --from-local ./app.tar.gz \
  --to-remote "/ci/${RUN_ID}/app.tar.gz" \
  --tag pipeline=build \
  --description "artifact for run ${RUN_ID}"
```

## 消费者作业 {#consumer-job}

在另一台 runner 上下载并验证该制品：

```bash
ti fs copy-file \
  --from-remote "/ci/${RUN_ID}/app.tar.gz" \
  --to-local ./app.tar.gz \
  --create-parents

tar -tzf app.tar.gz
```

对于接受 stdin 的命令，可以避免使用中间本地文件：

```bash
ti fs copy-file --from-remote "/ci/${RUN_ID}/app.tar.gz" --to-stdout \
  | tar -tzf -
```

## 清理与隔离 {#cleanup-and-isolation}

在所有消费者完成后，仅删除特定于该次运行的目录：

```bash
ti fs delete-file --path "/ci/${RUN_ID}" --recursive
```

使用唯一的运行 ID，并且不要在单个作业中删除整个文件系统。删除文件系统需要受信任的控制平面配置，因此应保持为单独所有者执行的操作。

## 后续内容 {#what-s-next}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud CLI Regions、安全性与限制](/ai/ti/reference/ti-regions-security-and-limitations.md)