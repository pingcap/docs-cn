---
title: 备份与恢复工具
summary: 了解备份与恢复的场景和工具选择。
---

# 备份与恢复工具

## 概述

备份与恢复中所使用的工具有 Dumpling、TiDB Lightning 和 BR。

- [Dumpling](/dumpling-overview.md) 是一个数据导出工具，该工具可以把存储在 TiDB/MySQL 中的数据导出为 SQL 或者 CSV 格式，可以用于完成逻辑上的全量备份或者导出。
- [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 是一个数据导入工具，该工具可以把 Dumpling 或 CSV 输出格式的数据快速导入到 TiDB 中，可以用于完成逻辑上的全量恢复或者导入。
- [BR](/br/backup-and-restore-overview.md) 是 TiDB 分布式备份恢复的命令行工具，用于对 TiDB 集群进行数据备份和恢复。相比 Dumpling 和 TiDB Lightning，BR 更适合大数据量的场景。如果需要对延迟不敏感的增量备份，请参阅 BR。

## 工具选择

**数据备份**

如果你对数据备份有以下要求，可考虑使用 BR 对 TiDB 进行数据备份：

- 备份的数据量较大，而且要求备份速度较快
- 直接备份数据的 SST 文件（键值对）
- 对延迟不敏感的增量备份

如果你对数据备份有以下要求，可考虑使用 Dumpling 对 TiDB 进行数据备份：

- 导出 SQL 或 CSV 格式的数据
- 对单条 SQL 语句的内存进行限制
- 导出 TiDB 的历史数据快照

**数据恢复**

如果你需要从由 BR 备份出的 SST 文件对 TiDB 进行数据恢复，则应使用 BR。

如果你需要从由 Dumpling 导出的或其他格式兼容的 SQL 或 CSV 文件对 TiDB 进行数据恢复，则应使用 TiDB Lightning。
