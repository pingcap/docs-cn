---
title: 使用 TiDB Cloud Filesystem 在可丢弃沙箱之间持久化 Agent 状态
summary: 在替换 agent 沙箱时，将计划、检查点、输出和工作流历史保存在文件系统中。
---

# 使用 TiDB Cloud Filesystem 在可丢弃沙箱之间持久化 Agent 状态

此工作流会将计划、中间结果、诊断文件和工作流历史保存在 TiDB Cloud Filesystem 中，同时让 agent 的计算环境保持可丢弃。这样，在无需保留先前沙箱仅为保存其本地磁盘的情况下，替换后的沙箱也可以继续执行任务。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 工作原理 {#how-it-works}

一台受信任的机器负责预配一个文件系统。每个沙箱只会接收到文件系统访问令牌和 region code。该访问令牌用于标识文件系统，因此 agent 可以将持久化的任务状态写入远程命名空间，并在日志（Journal）中记录工作流状态变更，而无需获得 TiDB Cloud 控制平面的密钥。

## 前提条件 {#prerequisites}

- 在受信任的机器上安装并配置 TiDB Cloud CLI。
- 在每个沙箱中安装 TiDB Cloud CLI。
- 在受信任的机器上安装 `jq`。
- 使用安全的 Secret 管理器或加密的沙箱输入来传输访问令牌。

## 步骤 1：预配状态文件系统 {#step-1-provision-the-state-file-system}

在受信任的机器上执行：

```bash
umask 077
ti fs create-file-system --wait > ./filesystem.json
export FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

将 `TI_FS_TOKEN` 存储到 Secret 管理器中，记录 `FILE_SYSTEM_ID` 以便后续清理，并记录已配置的 region code。在安全保存这些值后，删除 `filesystem.json`。

## 步骤 2：启动第一个沙箱 {#step-2-start-the-first-sandbox}

注入以下环境变量：

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
```

写入计划并创建工作流日志（Journal）：

```bash
printf '%s\n' '# Plan' '1. inspect' '2. change' '3. verify' \
  | ti fs copy-file --from-stdin --to-remote /tasks/task-42/plan.md

ti fs-journal create-journal \
  --journal-id task-42 \
  --journal-kind agent \
  --title "task 42" \
  --actor agent:worker-1

ti fs-journal append-journal-entries \
  --journal-id task-42 \
  --entry-json '{"type":"task.checkpoint","step":"inspection-complete"}'
```

`agent` journal kind 会将该日志归类为 agent 工作流，并且在省略 `--journal-kind` 时也是默认值。当你需要不同的工作流分类时，该选项也接受自定义字符串。

## 步骤 3：在替换后的沙箱中恢复 {#step-3-resume-in-a-replacement-sandbox}

将相同的两个 FS 变量注入到新沙箱中，然后恢复持久化状态：

```bash
ti fs read-file --path /tasks/task-42/plan.md
ti fs-journal read-journal-entries --journal-id task-42 --after-seq 0
```

继续在相同的任务路径下写入结果。请使用唯一的任务 ID，以避免并行运行的 agent 相互覆盖文件。

## 清理 {#cleanup}

当沙箱不再使用该文件系统后，在受信任的机器上将其删除：

```bash
rm -f ./filesystem.json
ti fs delete-file-system --file-system-id "$FILE_SYSTEM_ID"
```

删除文件系统也会同时删除其中的任务文件和日志（Journal）。

## 安全与运维说明 {#security-and-operational-notes}

- 文件系统访问令牌是 owner 凭证。请将其保存在运行时 Secret 存储中，不要将其包含在镜像或任务提示中。
- 已完成的直接数据平面写入会立即在远端可见。对于挂载的 FUSE 写入，在删除沙箱之前请先优雅地卸载。
- 日志（Journal）用于保留有序的工作流证据；任务文件用于保留可变的工作状态。当你既需要状态又需要历史记录时，请同时使用两者。

## 后续内容 {#what-s-next}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)
- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)