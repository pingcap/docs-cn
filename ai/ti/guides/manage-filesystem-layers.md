---
title: 管理 TiDB Cloud Filesystem Layers 和 Checkpoints
summary: 了解如何安全地创建、检查、派生、创建 checkpoints、回滚、提交、打包和恢复 TiDB Cloud Filesystem layers。
---

# 管理 TiDB Cloud Filesystem Layers 和 Checkpoints

使用 layers 可以在 Filesystem 基础路径之上记录隔离的变更，然后再决定提交还是丢弃这些变更。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 通过传入 `--file-system-id`、设置 `TI_FS_FILE_SYSTEM_ID`，或提供可标识该 Filesystem 的 FS token 来选择一个 Filesystem。
- 使用 `--fs-token`、`TI_FS_TOKEN` 或为所选 Filesystem 存储的本地凭证，提供具有所需读或写权限的 FS token。
- 选择该 layer 要叠加其数据的基础路径。

## 创建并检查 layer  {#create-and-inspect-a-layer}

```shell
ti fs create-layer \
  --base-root-path /workspace \
  --layer-name agent-task \
  --durability-mode restore-safe \
  --tag task=review
```

使用返回的 layer ID 来写入并检查变更：

```shell
ti fs copy-file \
  --from-local ./proposal.md \
  --to-remote /workspace/proposal.md \
  --layer-id "<layer-id>"

ti fs describe-layer --layer-id "<layer-id>"
ti fs diff-layer --layer-id "<layer-id>"
```

> **注意：**
>
> 带有 `--layer-id` 的 `copy-file` 不支持递归复制。要将一个目录树数据填充到 layer 中，请将该 layer 挂载为可写的 FUSE 挂载点，并通过挂载路径复制文件。

不要同时将同一个可写 layer 挂载到多个本地路径。请复用其现有挂载，或者先卸载后再将该 layer 挂载到其他位置。

## 创建 checkpoints 并派生 layer  {#create-a-checkpoint-and-fork-a-layer}

```shell
ti fs create-layer-checkpoint \
  --layer-id "<layer-id>" \
  --checkpoint-id seed \
  --label "before review"

ti fs fork-layer \
  --parent-layer-ref "<layer-id>" \
  --layer-name experiment \
  --checkpoint-id seed
```

使用 `list-layer-chain` 检查该派生 layer 被固定的祖先链：

```shell
ti fs list-layer-chain --layer-ref experiment
```

Checkpoints 挂载是只读的。要从 checkpoints 继续工作，请基于它派生一个新的可写 layer。

## 完成 layer 中的工作 {#finish-work-in-a-layer}

> **警告：**
>
> 在为具有可写 FUSE 挂载的 layer 创建 checkpoints 之前，请先运行 [`drain-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount)。Checkpoints 只包含已经到达服务的变更。在回滚或提交该 layer 之前，请先刷写，然后再执行 [`unmount-file-system`](/ai/ti/guides/mount-filesystem.md#drain-or-unmount)。CLI 不会自动执行这些步骤。

为一个 layer 选择以下其中一种结果：

- 回滚该 layer 以丢弃其变更：

    ```shell
    ti fs rollback-layer --layer-id "<layer-id>"
    ```

- 提交该 layer 以将其变更应用到基础路径：

    ```shell
    ti fs commit-layer --layer-id "<layer-id>"
    ```

> **注意：**
>
> 不要对同一个 layer 依次同时执行 `rollback-layer` 和 `commit-layer`。

## 将本地状态迁移到另一台机器 {#move-local-state-to-another-machine}

当 FUSE 挂载使用 write-back 缓存时，部分数据可能仍保留在其本地叠加 layer 目录中。要将这些本地状态迁移到另一台机器，请将其打包到一个显式指定的远程归档路径：

```shell
ti fs pack-file-system \
  --mount-path /path/to/workspace \
  --archive-path /workspace-overlay.tar.gz
```

在目标机器上，将该归档恢复到一个本地叠加 layer 根目录中：

```shell
ti fs unpack-file-system \
  --local-root /path/to/local-overlay \
  --remote-root /workspace \
  --mount-profile portable \
  --archive-path /workspace-overlay.tar.gz
```

在目标机器上挂载 Filesystem 时，请使用相同的本地叠加 layer 根目录。有关所有打包和解包选项，请参见 [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) 和 [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) 参考文档。

## 后续操作 {#what-s-next}

- [挂载 TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)