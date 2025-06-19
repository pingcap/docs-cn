---
title: 备份和恢复
summary: 了解 TiDB Cloud 的备份和恢复概念。
---

# 备份和恢复

TiDB Cloud 备份和恢复功能旨在通过使您能够备份和恢复集群数据来保护您的数据并确保业务连续性。

## 自动备份

对于 TiDB Cloud Serverless 和 TiDB Cloud Dedicated 集群，默认情况下会自动进行快照备份，并根据您的备份保留策略进行存储。

更多信息，请参见以下内容：

- [TiDB Cloud Serverless 集群的自动备份](/tidb-cloud/backup-and-restore-serverless.md#automatic-backups)
- [TiDB Cloud Dedicated 集群的自动备份](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)

## 手动备份

手动备份是 TiDB Cloud Dedicated 的一项功能，使您能够根据需要将数据备份到已知状态，然后随时恢复到该状态。

更多信息，请参见[执行手动备份](/tidb-cloud/backup-and-restore.md#perform-a-manual-backup)。

## 双区域备份

双区域备份是 TiDB Cloud Dedicated 的一项功能，使您能够将备份从集群所在区域复制到另一个不同的区域。启用后，所有备份都会自动复制到指定区域。这提供了跨区域数据保护和灾难恢复能力。估计约 99% 的数据可以在一小时内复制到次要区域。

更多信息，请参见[开启双区域备份](/tidb-cloud/backup-and-restore.md#turn-on-dual-region-backup)。

## 时间点恢复

时间点恢复是一项功能，使您能够将任意时间点的数据恢复到新集群。您可以使用它来：

- 降低灾难恢复中的 RPO。
- 通过恢复到错误事件发生之前的时间点来解决数据写入错误的情况。
- 审计业务的历史数据。

如果您想执行时间点恢复，请注意以下事项：

- 对于 TiDB Cloud Serverless 集群，时间点恢复仅适用于可扩展集群，不适用于免费集群。更多信息，请参见[恢复模式](/tidb-cloud/backup-and-restore-serverless.md#restore-mode)。
- 对于 TiDB Cloud Dedicated 集群，您需要提前[启用 PITR](/tidb-cloud/backup-and-restore.md#turn-on-point-in-time-restore)。
