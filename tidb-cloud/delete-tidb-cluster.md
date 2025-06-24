---
title: 删除 TiDB 集群
summary: 了解如何删除 TiDB 集群。
---

# 删除 TiDB 集群

本文介绍如何在 TiDB Cloud 上删除 TiDB 集群。

你可以随时通过执行以下步骤删除集群：

1. 导航到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。
2. 在要删除的目标集群所在行，点击 **...**。

    > **提示：**
    >
    > 或者，你也可以点击目标集群的名称进入其概览页面，然后点击右上角的 **...**。

3. 在下拉菜单中点击**删除**。
4. 在集群删除窗口中，确认删除：

    - 如果你至少有一个手动或自动备份，你可以看到备份数量和备份的收费政策。点击**继续**并输入 `<组织名称>/<项目名称>/<集群名称>`。
    - 如果你没有任何备份，只需输入 `<组织名称>/<项目名称>/<集群名称>`。

    如果你想在将来某个时候恢复集群，请确保你有集群的备份。否则，你将无法再恢复它。有关如何备份 TiDB Cloud Dedicated 集群的更多信息，请参见[备份和恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md)。

    > **注意：**
    >
    > [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)不支持删除后恢复数据。如果你想删除 TiDB Cloud Serverless 集群并在将来恢复其数据，请参见[从 TiDB Cloud Serverless 导出数据](/tidb-cloud/serverless-export.md)以导出数据作为备份。

5. 点击**我明白，删除它**。

    一旦已备份的 TiDB Cloud Dedicated 集群被删除，该集群的现有备份文件将被移至回收站。

    - 自动备份将在保留期结束后过期并自动删除。如果你不修改，默认保留期为 7 天。
    - 手动备份将保留在回收站中，直到手动删除。

    > **注意：**
    >
    > 请注意，备份将继续产生费用，直到被删除。

    如果你想从回收站恢复 TiDB Cloud Dedicated 集群，请参见[恢复已删除的集群](/tidb-cloud/backup-and-restore.md#restore-a-deleted-cluster)。
