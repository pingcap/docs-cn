---
title: TiDB Cloud 快速上手
summary: 快速注册并试用 TiDB Cloud，创建你的 TiDB 集群。
category: quick start
---

# TiDB Cloud 快速上手

*预计完成时间：20 分钟*

本教程将指导你快速开始使用 TiDB Cloud。你也可以在 TiDB Cloud 控制台的[**快速开始**](https://tidbcloud.com/getting-started)页面按照分步教程进行操作。

此外，你还可以在 [TiDB Playground](https://play.tidbcloud.com/?utm_source=docs&utm_medium=tidb_cloud_quick_start) 上试用 TiDB 的功能。

## 第 1 步：创建 TiDB 集群

[TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 是开始使用 TiDB Cloud 的最佳方式。要创建 TiDB Cloud Serverless 集群，请按照以下步骤操作：

1. 如果你还没有 TiDB Cloud 账号，请点击[这里](https://tidbcloud.com/free-trial)注册。

    你可以使用电子邮件和密码注册，通过 TiDB Cloud 管理你的密码，或者选择使用 Google、GitHub 或 Microsoft 账号进行单点登录 (SSO)。

2. [登录](https://tidbcloud.com/)你的 TiDB Cloud 账号。

    默认显示[**集群**](https://tidbcloud.com/project/clusters)页面。

3. 对于新注册用户，TiDB Cloud 会自动为你创建一个名为 `Cluster0` 的默认 TiDB Cloud Serverless 集群。

    - 要立即使用此默认集群试用 TiDB Cloud 功能，请继续[第 2 步：试用 AI 辅助 SQL 编辑器](#第-2-步试用-ai-辅助-sql-编辑器)。
    - 要自行创建新的 TiDB Cloud Serverless 集群，请按照以下步骤操作：

        1. 点击**创建集群**。
        2. 在**创建集群**页面，默认选择 **Serverless**。选择集群的目标区域，根据需要更新默认集群名称，选择你的[集群方案](/tidb-cloud/select-cluster-tier.md#cluster-plans)，然后点击**创建**。你的 TiDB Cloud Serverless 集群将在大约 30 秒内创建完成。

## 第 2 步：试用 AI 辅助 SQL 编辑器

你可以使用 TiDB Cloud 控制台中内置的 AI 辅助 SQL 编辑器来最大化数据价值。这使你无需本地 SQL 客户端即可对数据库运行 SQL 查询。你可以直观地以表格或图表形式查看查询结果，并轻松查看查询日志。

1. 在[**集群**](https://tidbcloud.com/project/clusters)页面，点击集群名称进入其概览页面，然后在左侧导航栏中点击 **SQL 编辑器**。

2. 要试用 TiDB Cloud 的 AI 功能，请按照屏幕上的说明允许 PingCAP 和 AWS Bedrock 使用你的代码片段进行研究和服务改进，然后点击**保存并开始**。

3. 在 SQL 编辑器中，在 macOS 上按 <kbd>⌘</kbd> + <kbd>I</kbd>（或在 Windows 或 Linux 上按 <kbd>Control</kbd> + <kbd>I</kbd>）来指示 [Chat2Query (beta)](/tidb-cloud/tidb-cloud-glossary.md#chat2query) 自动生成 SQL 查询。

    例如，要创建一个包含两列（列 `id` 和列 `name`）的新表 `test.t`，你可以输入 `use test;` 来指定数据库，按 <kbd>⌘</kbd> + <kbd>I</kbd>，输入 `create a new table t with id and name` 作为指令，然后按 **Enter** 让 AI 相应地生成 SQL 语句。
    
    对于生成的语句，你可以点击**接受**来接受它，然后根据需要进一步编辑，或者点击**放弃**来拒绝它。

    > **注意：**
    >
    > AI 生成的 SQL 查询并非 100% 准确，可能仍需要进一步调整。

4. 运行 SQL 查询。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果编辑器中只有一个查询，按 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**运行**来执行它。

    - 如果编辑器中有多个查询，用光标选择目标查询的行，然后按 **⌘ + Enter** 或点击**运行**来按顺序执行它们。

    - 要按顺序运行编辑器中的所有查询，按 **⇧ + ⌘ + Enter**，或用光标选择所有查询的行并点击**运行**。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果编辑器中只有一个查询，按 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**运行**来执行它。

    - 如果编辑器中有多个查询，用光标选择目标查询的行，然后按 **Ctrl + Enter** 或点击**运行**来按顺序执行它们。

    - 要按顺序运行编辑器中的所有查询，按 **Shift + Ctrl + Enter**，或用光标选择所有查询的行并点击**运行**。

    </div>
    </SimpleTab>

运行查询后，你可以立即在页面底部看到查询日志和结果。

要让 AI 生成更多 SQL 语句，你可以按照以下示例输入更多指令：

```sql
use test;

-- create a new table t with id and name 
CREATE TABLE
  `t` (`id` INT, `name` VARCHAR(255));

-- add 3 rows 
INSERT INTO
  `t` (`id`, `name`)
VALUES
  (1, 'row1'),
  (2, 'row2'),
  (3, 'row3');

-- query all
SELECT
  `id`,
  `name`
FROM
  `t`;
```

## 第 3 步：试用交互式教程

TiDB Cloud 提供了带有精心设计的示例数据集的交互式教程，帮助你快速开始使用 TiDB Cloud。你可以尝试这些教程，学习如何使用 TiDB Cloud 进行高性能数据分析。

1. 点击控制台右下角的 **?** 图标，选择**交互式教程**。
2. 在教程列表中，选择一个教程卡片开始，例如 **Steam 游戏统计**。
3. 选择你想要用于教程的 TiDB Cloud Serverless 集群，然后点击**导入数据集**。导入过程可能需要大约一分钟。
4. 数据导入完成后，按照屏幕上的说明完成教程。

## 下一步

- 要了解如何使用不同方法连接到集群，请参阅[连接到 TiDB Cloud Serverless 集群](/tidb-cloud/connect-to-tidb-cluster-serverless.md)。
- 要了解更多关于如何使用 SQL 编辑器和 Chat2Query 探索数据的信息，请参阅[使用 AI 辅助 SQL 编辑器探索数据](/tidb-cloud/explore-data-with-chat2query.md)。
- 关于 TiDB SQL 的使用，请参阅[使用 TiDB 探索 SQL](/basic-sql-operations.md)。
- 对于需要跨可用区高可用性、水平扩展和 [HTAP](https://en.wikipedia.org/wiki/Hybrid_transactional/analytical_processing) 优势的生产环境使用，请参阅[创建 TiDB Cloud Dedicated 集群](/tidb-cloud/create-tidb-cluster.md)。
