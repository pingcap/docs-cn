---
title: TiDB Cloud Filesystem Journal CLI 命令参考
summary: 参考所有 `ti fs-journal` 命令，用于创建、追加、读取、搜索和验证日志（Journal）。
---

# TiDB Cloud Filesystem Journal CLI 命令参考

`ti fs-journal` 为代理和工作流事件提供一个仅追加、可验证的账本。

## 命令 {#commands}

| 命令 | 描述 |
|---|---|
| [`create-journal`](/ai/ti/reference/ti-fs-journal-create-journal.md) | 创建日志（Journal）。 |
| [`append-journal-entries`](/ai/ti/reference/ti-fs-journal-append-journal-entries.md) | 向日志（Journal）追加事件。 |
| [`read-journal-entries`](/ai/ti/reference/ti-fs-journal-read-journal-entries.md) | 按顺序读取日志（Journal）条目。 |
| [`search-journal-entries`](/ai/ti/reference/ti-fs-journal-search-journal-entries.md) | 搜索日志（Journal）和条目。 |
| [`verify-journal`](/ai/ti/reference/ti-fs-journal-verify-journal.md) | 验证日志（Journal）的哈希链。 |

## 另请参阅 {#see-also}

- [使用 TiDB Cloud Filesystem Journals](/tidb-cloud-filesystem/use-filesystem-journals.md)
- [在文件系统日志（Journal）中记录 Agent 工作流](/ai/ti/guides/ti-journal-agent-workflow-example.md)