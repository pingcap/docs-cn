---
title: 使用 AWS DMS 从 Amazon RDS for Oracle 迁移到 TiDB Cloud
summary: 了解如何使用 AWS Database Migration Service (AWS DMS) 将数据从 Amazon RDS for Oracle 迁移到 TiDB Cloud Serverless。
---

# 使用 AWS DMS 从 Amazon RDS for Oracle 迁移到 TiDB Cloud

本文档提供了一个分步示例，说明如何使用 AWS Database Migration Service (AWS DMS) 将数据从 Amazon RDS for Oracle 迁移到 [TiDB Cloud Serverless](https://tidbcloud.com/clusters/create-cluster)。

如果你想了解更多关于 TiDB Cloud 和 AWS DMS 的信息，请参阅以下内容：

- [TiDB Cloud](https://docs.pingcap.com/tidbcloud/)
- [TiDB 开发者指南](https://docs.pingcap.com/tidbcloud/dev-guide-overview)
- [AWS DMS 文档](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.html)

## 为什么使用 AWS DMS？

AWS DMS 是一项云服务，可用于迁移关系型数据库、数据仓库、NoSQL 数据库和其他类型的数据存储。

如果你想从异构数据库（如 PostgreSQL、Oracle 和 SQL Server）迁移数据到 TiDB Cloud，建议使用 AWS DMS。

## 部署架构

总体上，需要执行以下步骤：

1. 设置源 Amazon RDS for Oracle。
2. 设置目标 [TiDB Cloud Serverless](https://tidbcloud.com/project/clusters/create-cluster)。
3. 使用 AWS DMS 设置数据迁移（全量加载）。

下图展示了高级架构。

![架构](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-0.png)

## 前提条件

开始之前，请阅读以下前提条件：

- [AWS DMS 前提条件](/tidb-cloud/migrate-from-mysql-using-aws-dms.md#prerequisites)
- [AWS Cloud 账户](https://aws.amazon.com)
- [TiDB Cloud 账户](https://tidbcloud.com)
- [DBeaver](https://dbeaver.io/)

接下来，你将学习如何使用 AWS DMS 将数据从 Amazon RDS for Oracle 迁移到 TiDB Cloud。

## 步骤 1. 创建 VPC

登录 [AWS 控制台](https://console.aws.amazon.com/vpc/home#vpcs:) 并创建一个 AWS VPC。你稍后需要在此 VPC 中创建 Oracle RDS 和 DMS 实例。

有关如何创建 VPC 的说明，请参阅[创建 VPC](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html#Create-VPC)。

![创建 VPC](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-1.png)

## 步骤 2. 创建 Oracle 数据库实例

在刚刚创建的 VPC 中创建一个 Oracle 数据库实例，记住密码并授予公共访问权限。你必须启用公共访问才能使用 AWS Schema Conversion Tool。请注意，不建议在生产环境中授予公共访问权限。

有关如何创建 Oracle 数据库实例的说明，请参阅[创建 Oracle 数据库实例并连接到 Oracle 数据库实例上的数据库](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_GettingStarted.CreatingConnecting.Oracle.html)。

![创建 Oracle RDS](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-2.png)

## 步骤 3. 在 Oracle 中准备表数据

使用以下脚本在 github_events 表中创建并填充 10000 行数据。你可以使用 github 事件数据集，并从 [GH Archive](https://gharchive.org/) 下载。它包含 10000 行数据。在 Oracle 中执行以下 SQL 脚本。

- [table_schema_oracle.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_table_schema.sql)
- [oracle_data.sql](https://github.com/pingcap-inc/tidb-integration-script/blob/main/aws-dms/oracle_data.sql)

执行完 SQL 脚本后，检查 Oracle 中的数据。以下示例使用 [DBeaver](https://dbeaver.io/) 查询数据：

![Oracle RDS 数据](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-3.png)

## 步骤 4. 创建 TiDB Cloud Serverless 集群

1. 登录 [TiDB Cloud 控制台](https://tidbcloud.com/project/clusters)。

2. [创建 TiDB Cloud Serverless 集群](/tidb-cloud/tidb-cloud-quickstart.md)。

3. 在[**集群**](https://tidbcloud.com/project/clusters)页面，点击目标集群名称进入其概览页面。

4. 在右上角，点击**连接**。

5. 点击**生成密码**生成密码并复制生成的密码。

## 步骤 5. 创建 AWS DMS 复制实例

1. 在 AWS DMS 控制台中转到[复制实例](https://console.aws.amazon.com/dms/v2/home#replicationInstances)页面，并切换到相应的区域。

2. 在 VPC 中创建一个 `dms.t3.large` 的 AWS DMS 复制实例。

    ![创建 AWS DMS 实例](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-8.png)

> **注意：**
>
> 有关创建与 TiDB Cloud Serverless 配合使用的 AWS DMS 复制实例的详细步骤，请参阅[将 AWS DMS 连接到 TiDB Cloud 集群](/tidb-cloud/tidb-cloud-connect-aws-dms.md)。

## 步骤 6. 创建 DMS 端点

1. 在 [AWS DMS 控制台](https://console.aws.amazon.com/dms/v2/home)中，点击左侧窗格中的 `Endpoints` 菜单项。

2. 创建 Oracle 源端点和 TiDB 目标端点。

    以下截图显示了源端点的配置。

    ![创建 AWS DMS 源端点](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-9.png)

    以下截图显示了目标端点的配置。

    ![创建 AWS DMS 目标端点](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-10.png)

> **注意：**
>
> 有关创建 TiDB Cloud Serverless DMS 端点的详细步骤，请参阅[将 AWS DMS 连接到 TiDB Cloud 集群](/tidb-cloud/tidb-cloud-connect-aws-dms.md)。

## 步骤 7. 迁移架构

在本示例中，由于架构定义简单，AWS DMS 会自动处理架构。

如果你决定使用 AWS Schema Conversion Tool 迁移架构，请参阅[安装 AWS SCT](https://docs.aws.amazon.com/SchemaConversionTool/latest/userguide/CHAP_Installing.html#CHAP_Installing.Procedure)。

更多信息，请参阅[使用 AWS SCT 将源架构迁移到目标数据库](https://docs.aws.amazon.com/dms/latest/userguide/CHAP_GettingStarted.SCT.html)。

## 步骤 8. 创建数据库迁移任务

1. 在 AWS DMS 控制台中，转到[数据迁移任务](https://console.aws.amazon.com/dms/v2/home#tasks)页面。切换到你的区域。然后点击窗口右上角的**创建任务**。

    ![创建任务](/media/tidb-cloud/aws-dms-to-tidb-cloud-create-task.png)

2. 创建数据库迁移任务并指定**选择规则**：

    ![创建 AWS DMS 迁移任务](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-11.png)

    ![AWS DMS 迁移任务选择规则](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-12.png)

3. 创建任务，启动它，然后等待任务完成。

4. 点击**表统计信息**检查表。架构名称是 `ADMIN`。

    ![检查 AWS DMS 迁移任务](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-13.png)

## 步骤 9. 检查下游 TiDB 集群中的数据

连接到 [TiDB Cloud Serverless 集群](https://tidbcloud.com/clusters/create-cluster)并检查 `admin.github_event` 表数据。如下截图所示，DMS 成功迁移了表 `github_events` 和 10000 行数据。

![检查 TiDB 中的数据](/media/tidb-cloud/aws-dms-from-oracle-to-tidb-14.png)

## 总结

使用 AWS DMS，你可以按照本文档中的示例成功地从任何上游 AWS RDS 数据库迁移数据。

如果在迁移过程中遇到任何问题或失败，你可以在 [CloudWatch](https://console.aws.amazon.com/cloudwatch/home) 中检查日志信息来排查问题。

![故障排除](/media/tidb-cloud/aws-dms-to-tidb-cloud-troubleshooting.png)

## 另请参阅

- [使用 AWS DMS 从 MySQL 兼容数据库迁移](/tidb-cloud/migrate-from-mysql-using-aws-dms.md)
- [将 AWS DMS 连接到 TiDB Cloud 集群](/tidb-cloud/tidb-cloud-connect-aws-dms.md)
