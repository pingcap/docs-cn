---
title: 使用 TiDB Cloud Filesystem Journals
summary: 了解如何在 Filesystem 中为代理和自动化事件创建、追加、读取、搜索和验证仅追加日志（Journal）。
---

# 使用 TiDB Cloud Filesystem Journals

Journals 为运行在 TiDB Cloud Filesystem 上的代理工作流和自动化流水线提供仅追加、基于哈希链的事件日志。你可以使用 [`ti fs-journal` 命令](/ai/ti/reference/ti-filesystem-journal.md) 创建日志（Journal）、追加有序事件、搜索或读取这些事件，以及验证哈希链。

## 前提条件 {#prerequisites}

- [安装并配置 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)。
- 通过传入 `--file-system-id`、设置 `TI_FS_FILE_SYSTEM_ID`，或提供可标识该 Filesystem 的 FS token 来选择一个 Filesystem。
- 通过 `--fs-token`、`TI_FS_TOKEN` 或为所选 Filesystem 本地存储的凭证，提供具有 journal 权限的 FS token。

## 创建 journal {#create-a-journal}

```shell
ti fs-journal create-journal \
  --journal-kind agent \
  --title "review task" \
  --actor agent:reviewer
```

保存返回的 journal ID。

## 追加条目 {#append-entries}

```shell
ti fs-journal append-journal-entries \
  --journal-id "<journal-id>" \
  --entry-json '{"type":"review_started"}'
```

关于支持的输入形式和条目字段，请参见 [`append-journal-entries` 参考文档](/ai/ti/reference/ti-fs-journal-append-journal-entries.md)。

## 读取和搜索条目 {#read-and-search-entries}

按顺序读取条目：

```shell
ti fs-journal read-journal-entries --journal-id "<journal-id>"
```

跨多个 journal 和条目进行搜索：

```shell
ti fs-journal search-journal-entries \
  --entry-type review_started \
  --include-entries
```

## 验证 journal {#verify-a-journal}

验证该 journal 的哈希链是否完整：

```shell
ti fs-journal verify-journal --journal-id "<journal-id>"
```

## 后续操作 {#what-s-next}

- [在 TiDB Cloud Filesystem Journal 中记录 Agent 工作流](/ai/ti/guides/ti-journal-agent-workflow-example.md)
- [TiDB Cloud Filesystem Journal CLI 命令参考](/ai/ti/reference/ti-filesystem-journal.md)