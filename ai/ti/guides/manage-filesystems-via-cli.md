---
title: 管理 TiDB Cloud Filesystem
summary: 了解如何使用 `ti fs` 创建文件系统并写入和读取文件，然后查找其他文件系统任务的指南。
---

# 管理 TiDB Cloud Filesystem

使用 TiDB Cloud CLI (`ti`)，你可以在 TiDB Cloud Filesystem 中创建和管理文件系统资源，并通过终端或自动化工作流处理其中的文件。

## 创建并使用文件系统 {#create-and-use-a-file-system}

开始之前，请先[安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)，并使用能够在你的组织中创建文件系统的 API 密钥。在运行 `ti configure` 时，选择一个受支持的文件系统 Region。

创建一个文件系统并等待其就绪：

```shell
ti fs create-file-system --display-name my-workspace --wait
```

复制返回的 `file_system_id`，并在以下命令中将 `<file-system-id>` 替换为该值。CLI 会在本地存储文件系统令牌。请将返回的 `fs_token`（文件系统令牌）视为 Secret；不要公开分享命令输出。

```shell
echo "Hello from my workspace" | ti fs copy-file --file-system-id "<file-system-id>" --from-stdin --to-remote /hello.txt
ti fs read-file --file-system-id "<file-system-id>" --path /hello.txt
```

读取结果会返回 `Hello from my workspace`。有关受支持的 Region、详细设置和清理说明，请参阅[TiDB Cloud Filesystem 快速开始](/tidb-cloud-filesystem/filesystem-quick-start.md)。

## 更多文件系统任务 {#more-file-system-tasks}

创建文件系统后，可参考以下指南完成相关文件系统任务：

| 你想执行的操作 | 指南 |
| --- | --- |
| 从另一台机器、CI 作业或代理环境访问现有文件系统 | [访问现有文件系统](/tidb-cloud-filesystem/access-filesystem.md) |
| 上传、下载、读取、整理、检查或搜索文件和目录 | [使用文件和目录](/tidb-cloud-filesystem/work-with-filesystem-data.md) |
| 生成、导入、限定作用域、检查、禁用、刷新或回收访问令牌 | [管理文件系统令牌](/tidb-cloud-filesystem/manage-filesystem-tokens.md) |
| 与其他用户、机器、CI 作业或代理共享文件系统中的文件 | [共享文件系统](/tidb-cloud-filesystem/filesystem-sharing.md) |
| 通过本地文件路径访问文件系统中的文件 | [挂载文件系统](/tidb-cloud-filesystem/filesystem-mount.md) |
| 使用 layer 和 checkpoint 隔离变更 | [管理文件系统 layer 和 checkpoint](/tidb-cloud-filesystem/manage-filesystem-layers.md) |
| 在已挂载的文件系统上使用 Git 仓库 | [管理 Git 工作区](/tidb-cloud-filesystem/manage-git-workspaces.md) |
| 记录并验证有序的工作流事件 | [在文件系统中使用日志（Journal）](/tidb-cloud-filesystem/use-filesystem-journals.md) |
| 存储、委派、注入、审计和回收 Secret | [管理文件系统的 Vault Secret](/tidb-cloud-filesystem/manage-filesystem-vault-secrets.md) |
| 为媒体内容提取或语义搜索配置 AI 提供方 | [为文件系统配置 AI 提供方](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md) |

有关语法、（命令行）标记/参数和输出字段，请参阅[`ti fs` 命令参考](/ai/ti/reference/ti-filesystem.md)。