---
title: 管理 TiDB Cloud Filesystem 资源
summary: 了解如何使用 TiDB Cloud CLI 安全地创建、检查、验证、选择和删除 TiDB Cloud Filesystem 资源。
---

# 管理 TiDB Cloud Filesystem 资源

TiDB Cloud Filesystem 是一种面向 AI agent 和自动化工作负载设计的无服务器分布式文件系统。它提供持久且可共享的文件命名空间，并且无论访问它的是本地机器、沙箱还是 CI runner，该命名空间都能独立持续可用。

你可以直接通过 TiDB Cloud CLI 命令访问文件，也可以将 Filesystem 挂载到受支持的环境中，并像使用本地文件系统一样操作它。这使其非常适合用于保留 agent 状态、在隔离环境之间共享文件、交接 CI 制品，以及维护可复用的工作空间。

本文介绍如何使用 [`ti fs` 命令](/ai/ti/reference/ti-filesystem.md) 来创建、检查、选择和删除 Filesystem 资源。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 使用 TiDB Cloud API 凭证配置一个配置（Profile）。
- 安装 `jq`，或使用其他 JSON 处理工具来安全地捕获命令输出。

## 创建 Filesystem {#create-a-filesystem}

创建一个 Filesystem，并将返回的 ID 和一次性的所有者令牌保存到一个非全局可读的文件中。`--wait` 标记会让 CLI 在返回之前持续轮询，直到数据平面访问准备就绪：

```shell
umask 077
ti fs create-file-system \
  --display-name agent-workspace \
  --label environment=development \
  --wait > ./filesystem.json

export TI_FS_FILE_SYSTEM_ID="$(jq -r '.file_system_id' ./filesystem.json)"
export TI_FS_TOKEN="$(jq -r '.fs_token' ./filesystem.json)"
```

> **Warning:**
>
> JSON 响应中的 `fs_token` 只会出现一次。CLI 也会自动将此令牌存储到其本地凭证目录中。但是，如果本地存储丢失，你将无法再次取回该令牌。请将其备份副本存储到 Secret 管理器中，然后删除 `filesystem.json`。

> **Note:**
>
> 不要在 Filesystem 标签中放入凭证、连接字符串、私有路径或个人数据。

## 列出并检查 Filesystem {#list-and-inspect-filesystems}

列出当前生效 Region 中可用的 Filesystem：

```shell
ti fs list-file-systems --output text
```

读取某个 Filesystem 的权威元信息：

```shell
ti fs describe-file-system --file-system-id "<file-system-id>"
```

如果你有权访问多个 Filesystem，请显式传入 `--file-system-id`，或设置 `TI_FS_FILE_SYSTEM_ID` 环境变量。CLI 不会自动为你选择 Filesystem。

## 检查访问权限 {#check-access}

验证资源选择、端点解析、凭证以及配套访问：

```shell
ti fs check-file-system --file-system-id "<file-system-id>"
```

## 删除 Filesystem {#delete-a-filesystem}

> **Warning:**
>
> 删除 Filesystem 之前，请先对刷写并卸载其所有活动的本地挂载。CLI 不会自动执行此操作。

通过显式 ID 删除 Filesystem：

```shell
ti fs delete-file-system --file-system-id "<file-system-id>"
```

Filesystem 删除是异步的。在服务接受该请求后，CLI 会将 Filesystem 状态报告为 `deleting`，并移除匹配的本地凭证。此输出并不表示远程删除已经完成。

## 后续操作 {#what-s-next}

- [管理 TiDB Cloud Filesystem 令牌](/ai/ti/guides/manage-filesystem-tokens.md)
- [使用 TiDB Cloud Filesystem 数据](/ai/ti/guides/work-with-filesystem-data.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)