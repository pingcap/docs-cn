---
title: 使用 TiDB Cloud 进行概念验证（PoC）
summary: 了解如何使用 TiDB Cloud 进行概念验证（PoC）。
---

# 使用 TiDB Cloud 进行概念验证（PoC）

TiDB Cloud 是一个数据库即服务（DBaaS）产品，它以完全托管的云数据库形式提供 TiDB 的所有优秀特性。它让您能够专注于应用程序开发，而不必关心数据库的复杂性。TiDB Cloud 目前可在 Amazon Web Services (AWS)、Google Cloud 和 Microsoft Azure 上使用。

启动概念验证（PoC）是确定 TiDB Cloud 是否最适合您业务需求的最佳方式。它还能帮助您在短时间内熟悉 TiDB Cloud 的主要功能。通过运行性能测试，您可以了解您的工作负载是否能在 TiDB Cloud 上高效运行。您还可以评估数据迁移和配置调整所需的工作量。

本文档描述了典型的 PoC 流程，旨在帮助您快速完成 TiDB Cloud PoC。这是经过 TiDB 专家和大量客户验证的最佳实践。

如果您有兴趣进行 PoC，欢迎在开始之前联系 <a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>。支持团队可以帮助您制定测试计划，并指导您顺利完成 PoC 流程。

另外，您也可以[创建 TiDB Cloud Serverless 集群](/tidb-cloud/tidb-cloud-quickstart.md#step-1-create-a-tidb-cluster)来快速评估和熟悉 TiDB Cloud。请注意，TiDB Cloud Serverless 有一些[特殊条款和条件](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless-special-terms-and-conditions)。

## PoC 流程概述

PoC 的目的是测试 TiDB Cloud 是否满足您的业务需求。典型的 PoC 通常持续 14 天，在此期间您需要专注于完成 PoC。

典型的 TiDB Cloud PoC 包含以下步骤：

1. 定义成功标准并制定测试计划
2. 识别工作负载特征
3. 注册并创建用于 PoC 的 TiDB Cloud Dedicated 集群
4. 调整数据库模式和 SQL
5. 导入数据
6. 运行工作负载并评估结果
7. 探索更多功能
8. 清理环境并完成 PoC

## 步骤 1. 定义成功标准并制定测试计划

在通过 PoC 评估 TiDB Cloud 时，建议根据您的业务需求确定关注点和相应的技术评估标准，然后明确您对 PoC 的期望和目标。清晰且可衡量的技术标准和详细的测试计划可以帮助您专注于关键方面，覆盖业务层面的需求，并最终通过 PoC 流程获得答案。

使用以下问题帮助确定您的 PoC 目标：

- 您的工作负载场景是什么？
- 您的业务数据集大小或工作负载是多少？增长率如何？
- 性能要求是什么，包括业务关键的吞吐量或延迟要求？
- 可用性和稳定性要求是什么，包括可接受的最小计划内或计划外停机时间？
- 运营效率的必要指标是什么？如何衡量它们？
- 您的工作负载的安全性和合规性要求是什么？

有关成功标准和如何制定测试计划的更多信息，请随时联系 <a href="mailto:tidbcloud-support@pingcap.com">PingCAP</a>。

## 步骤 2. 识别工作负载特征

TiDB Cloud 适用于需要高可用性和强一致性且数据量大的各种使用场景。[TiDB 简介](https://docs.pingcap.com/tidb/stable/overview)列出了主要特性和场景。您可以检查它们是否适用于您的业务场景：

- 水平扩展或收缩
- 金融级高可用
- 实时 HTAP
- 兼容 MySQL 协议和 MySQL 生态系统

您可能还对使用 [TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview) 感兴趣，这是一个可以加速分析处理的列式存储引擎。在 PoC 期间，您可以随时使用 TiFlash 功能。

## 步骤 3. 注册并创建用于 PoC 的 TiDB Cloud Dedicated 集群

要创建用于 PoC 的 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群，请执行以下步骤：

1. 通过以下方式之一填写 PoC 申请表：

    - 在 PingCAP 网站上，访问 [Apply for PoC](https://pingcap.com/apply-for-poc/) 页面填写申请表。
    - 在 [TiDB Cloud 控制台](https://tidbcloud.com/)中，点击右下角的 **?**，点击 **Contact Sales**，然后选择 **Apply for PoC** 填写申请表。

    提交表单后，TiDB Cloud 支持团队将审核您的申请，与您联系，并在申请获批后将积分转入您的账户。您还可以联系 PingCAP 支持工程师协助您的 PoC 流程，以确保 PoC 顺利进行。

2. 参考[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)为 PoC 创建 TiDB Cloud Dedicated 集群。

在创建集群之前，建议进行容量规划。您可以从估算的 TiDB、TiKV 或 TiFlash 节点数量开始，之后根据性能需求进行扩展。您可以在以下文档中找到更多详细信息，或咨询我们的支持团队。

- 有关估算实践的更多信息，请参见[规划 TiDB 集群规模](/tidb-cloud/size-your-cluster.md)。
- 有关 TiDB Cloud Dedicated 集群的配置，请参见[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。分别为 TiDB、TiKV 和 TiFlash（可选）配置集群大小。
- 有关如何有效规划和优化 PoC 积分消耗，请参见本文档中的 [FAQ](#faq)。
- 有关扩展的更多信息，请参见[扩展 TiDB 集群](/tidb-cloud/scale-tidb-cluster.md)。

创建专用 PoC 集群后，您就可以加载数据并执行一系列测试了。有关如何连接 TiDB 集群，请参见[连接到 TiDB Cloud Dedicated 集群](/tidb-cloud/connect-to-tidb-cluster.md)。

对于新创建的集群，请注意以下配置：

- 默认时区（仪表板上的 **Create Time** 列）是 UTC。您可以按照[设置本地时区](/tidb-cloud/manage-user-access.md#set-the-time-zone-for-your-organization)将其更改为您的本地时区。
- 新集群的默认备份设置是每日全量数据库备份。您可以指定首选备份时间或手动备份数据。有关默认备份时间和更多详细信息，请参见[备份和恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

## 步骤 4. 调整数据库模式和 SQL

接下来，您可以将数据库模式加载到 TiDB 集群中，包括表和索引。

由于 PoC 积分有限，为了最大化积分价值，建议您创建 [TiDB Cloud Serverless 集群](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless)进行兼容性测试和 TiDB Cloud 的初步分析。

TiDB Cloud 与 MySQL 8.0 高度兼容。如果您的数据与 MySQL 兼容或可以调整为与 MySQL 兼容，您可以直接将数据导入 TiDB。

有关兼容性的更多信息，请参见以下文档：

- [TiDB 与 MySQL 的兼容性](https://docs.pingcap.com/tidb/stable/mysql-compatibility)。
- [TiDB 与 MySQL 的不同特性](https://docs.pingcap.com/tidb/stable/mysql-compatibility#features-that-are-different-from-mysql)。
- [TiDB 的关键字和保留字](https://docs.pingcap.com/tidb/stable/keywords)。
- [TiDB 限制](https://docs.pingcap.com/tidb/stable/tidb-limitations)。

以下是一些最佳实践：

- 检查模式设置中是否存在效率低下的问题。
- 删除不必要的索引。
- 规划有效的分区策略。
- 避免由右手索引增长导致的[热点问题](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)，例如时间戳上的索引。
- 通过使用 [SHARD_ROW_ID_BITS](https://docs.pingcap.com/tidb/stable/shard-row-id-bits) 和 [AUTO_RANDOM](https://docs.pingcap.com/tidb/stable/auto-random) 避免[热点问题](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#identify-hotspot-issues)。

对于 SQL 语句，根据您的数据源与 TiDB 的兼容性级别，您可能需要进行调整。

如果您有任何问题，请联系 [PingCAP](/tidb-cloud/tidb-cloud-support.md) 进行咨询。

## 步骤 5. 导入数据

您可以导入小型数据集来快速测试可行性，或导入大型数据集来测试 TiDB 数据迁移工具的吞吐量。虽然 TiDB 提供示例数据，但强烈建议使用来自您业务的真实工作负载进行测试。

您可以将各种格式的数据导入 TiDB Cloud：

- [使用数据迁移将 MySQL 兼容数据库迁移到 TiDB Cloud](/tidb-cloud/migrate-from-mysql-using-data-migration.md)
- [将本地文件导入 TiDB Cloud](/tidb-cloud/tidb-cloud-import-local-files.md)
- [导入 SQL 文件格式的示例数据](/tidb-cloud/import-sample-data.md)
- [从云存储导入 CSV 文件](/tidb-cloud/import-csv-files.md)
- [导入 Apache Parquet 文件](/tidb-cloud/import-parquet-files.md)

> **注意：**
>
> **导入**页面上的数据导入不会产生额外的计费费用。

## 步骤 6. 运行工作负载并评估结果

现在您已经创建了环境、调整了模式并导入了数据。是时候测试您的工作负载了。

在测试工作负载之前，考虑执行手动备份，这样在需要时可以将数据库恢复到原始状态。有关更多信息，请参见[备份和恢复 TiDB 集群数据](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)。

启动工作负载后，您可以使用以下方法观察系统：

- 在集群概览页面上可以找到集群的常用指标，包括总 QPS、延迟、连接数、TiFlash 请求 QPS、TiFlash 请求持续时间、TiFlash 存储大小、TiKV 存储大小、TiDB CPU、TiKV CPU、TiKV IO 读取和 TiKV IO 写入。请参见[监控 TiDB 集群](/tidb-cloud/monitor-tidb-cluster.md)。
- 导航到集群的[**诊断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)页面，然后查看 **SQL Statement** 标签页，您可以在此观察 SQL 执行情况，无需查询系统表即可轻松定位性能问题。请参见[语句分析](/tidb-cloud/tune-performance.md#statement-analysis)。
- 导航到集群的[**诊断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)页面，然后查看 **Key Visualizer** 标签页，您可以在此查看 TiDB 数据访问模式和数据热点。请参见[Key Visualizer](/tidb-cloud/tune-performance.md#key-visualizer)。
- 您还可以将这些指标集成到您自己的 Datadog 和 Prometheus 中。请参见[第三方监控集成](/tidb-cloud/third-party-monitoring-integrations.md)。

现在是评估测试结果的时候了。

为了获得更准确的评估，在测试之前确定指标基线，并适当记录每次运行的测试结果。通过分析结果，您可以决定 TiDB Cloud 是否适合您的应用。同时，这些结果表明了系统的运行状态，您可以根据指标调整系统。例如：

- 评估系统性能是否满足您的要求。检查总 QPS 和延迟。如果系统性能不令人满意，您可以通过以下方式调优性能：

    - 监控和优化网络延迟。
    - 调查和调优 SQL 性能。
    - 监控和[解决热点问题](https://docs.pingcap.com/tidb/dev/troubleshoot-hot-spot-issues#troubleshoot-hotspot-issues)。

- 评估存储大小和 CPU 使用率，相应地扩展或收缩 TiDB 集群。有关扩展的详细信息，请参见 [FAQ](#faq) 部分。

以下是性能调优的提示：

- 提高写入性能

    - 通过扩展 TiDB 集群增加写入吞吐量（请参见[扩展 TiDB 集群](/tidb-cloud/scale-tidb-cluster.md)）。
    - 通过使用[乐观事务模型](https://docs.pingcap.com/tidb/stable/optimistic-transaction#tidb-optimistic-transaction-model)减少锁冲突。

- 提高查询性能

    - 在[**诊断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)页面的 [**SQL Statement**](/tidb-cloud/tune-performance.md#statement-analysis) 标签页上检查 SQL 执行计划。
    - 在[**诊断**](/tidb-cloud/tune-performance.md#view-the-diagnosis-page)页面的 [**Key Visualizer**](/tidb-cloud/tune-performance.md#key-visualizer) 标签页上检查热点问题。
    - 在[**指标**](/tidb-cloud/built-in-monitoring.md#view-the-metrics-page)页面上监控 TiDB 集群是否容量不足。
    - 使用 TiFlash 功能优化分析处理。请参见[使用 HTAP 集群](/tiflash/tiflash-overview.md)。

## 步骤 7. 探索更多功能

现在工作负载测试已完成，您可以探索更多功能，例如升级和备份。

- 升级

    TiDB Cloud 定期升级 TiDB 集群，您也可以提交支持工单请求升级集群。请参见[升级 TiDB 集群](/tidb-cloud/upgrade-tidb-cluster.md)。

- 备份

    为避免供应商锁定，您可以使用每日全量备份将数据迁移到新集群，并使用 [Dumpling](https://docs.pingcap.com/tidb/stable/dumpling-overview) 导出数据。有关更多信息，请参见[备份和恢复 TiDB Cloud Dedicated 数据](/tidb-cloud/backup-and-restore.md#turn-on-auto-backup)和[备份和恢复 TiDB Cloud Serverless 数据](/tidb-cloud/backup-and-restore-serverless.md)。

## 步骤 8. 清理环境并完成 PoC

在使用真实工作负载测试 TiDB Cloud 并获得测试结果后，您已完成了 PoC 的完整周期。这些结果帮助您确定 TiDB Cloud 是否满足您的期望。同时，您也积累了使用 TiDB Cloud 的最佳实践。

如果您想在更大规模上尝试 TiDB Cloud，进行新一轮的部署和测试，例如使用 TiDB Cloud 提供的其他节点存储大小进行部署，可以通过创建 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群来获得 TiDB Cloud 的完整访问权限。

如果您的积分即将用完，想继续进行 PoC，请联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)进行咨询。

您可以随时结束 PoC 并删除测试环境。有关更多信息，请参见[删除 TiDB 集群](/tidb-cloud/delete-tidb-cluster.md)。

我们非常感谢您通过填写 [TiDB Cloud 反馈表](https://www.surveymonkey.com/r/L3VVW8R)向我们的支持团队提供任何反馈，例如 PoC 流程、功能请求以及我们如何改进产品。

## FAQ

### 1. 备份和恢复我的数据需要多长时间？

TiDB Cloud 提供两种类型的数据库备份：自动备份和手动备份。这两种方法都会备份完整的数据库。

备份和恢复数据所需的时间可能会有所不同，这取决于表的数量、镜像副本的数量以及 CPU 密集程度。单个 TiKV 节点的备份和恢复速率约为 50 MB/s。

数据库备份和恢复操作通常是 CPU 密集型的，始终需要额外的 CPU 资源。它们可能会对 QPS 和事务延迟产生影响（10% 到 50%），具体取决于环境的 CPU 密集程度。

### 2. 什么时候需要扩展和收缩？

以下是关于扩展的一些考虑因素：

- 在高峰时段或数据导入期间，如果您观察到仪表板上的容量指标已达到上限（请参见[监控 TiDB 集群](/tidb-cloud/monitor-tidb-cluster.md)），您可能需要扩展集群。
- 如果您观察到资源使用率持续较低，例如，CPU 使用率仅为 10%-20%，您可以收缩集群以节省资源。

您可以在控制台上自行扩展集群。如果您需要收缩集群，需要联系 [TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)寻求帮助。有关扩展的更多信息，请参见[扩展 TiDB 集群](/tidb-cloud/scale-tidb-cluster.md)。您可以与支持团队保持联系，跟踪具体进度。由于数据重新平衡可能会影响性能，您必须等待扩展操作完成后再开始测试。

### 3. 如何最有效地使用我的 PoC 积分？

一旦您的 PoC 申请获得批准，您将在账户中收到积分。通常，这些积分足够进行为期 14 天的 PoC。积分按节点类型和节点数量按小时计费。有关更多信息，请参见 [TiDB Cloud 计费](/tidb-cloud/tidb-cloud-billing.md#credits)。

要查看 PoC 剩余积分，请转到目标项目的[**集群**](https://tidbcloud.com/project/clusters)页面，如下图所示。

![TiDB Cloud PoC 积分](/media/tidb-cloud/poc-points.png)

或者，您也可以使用 TiDB Cloud 控制台左上角的组合框切换到目标组织，点击左侧导航栏中的**计费**，然后点击**积分**标签页查看积分信息。

要节省积分，请删除您不使用的集群。目前，您无法停止集群。在删除集群之前，您需要确保备份是最新的，这样当您想要恢复 PoC 时可以恢复集群。

如果在 PoC 流程完成后您仍有未使用的积分，只要这些积分未过期，您可以继续使用它们支付 TiDB 集群费用。

### 4. 我可以花超过 2 周的时间完成 PoC 吗？

如果您想延长 PoC 试用期或积分即将用完，请[联系 PingCAP](https://www.pingcap.com/contact-us/) 寻求帮助。

### 5. 我遇到了技术问题。如何获取 PoC 帮助？

您随时可以[联系 TiDB Cloud 支持](/tidb-cloud/tidb-cloud-support.md)寻求帮助。
