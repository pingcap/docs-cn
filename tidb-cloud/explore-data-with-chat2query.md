---
title: 使用 AI 辅助 SQL 编辑器探索数据
summary: 了解如何在 TiDB Cloud 控制台中使用 AI 辅助 SQL 编辑器，以最大化数据价值。
---

# 使用 AI 辅助 SQL 编辑器探索数据

你可以使用 [TiDB Cloud 控制台](https://tidbcloud.com/) 中内置的 AI 辅助 SQL 编辑器来最大化数据价值。

在 SQL 编辑器中，你可以手动编写 SQL 查询，也可以在 macOS 上按 <kbd>⌘</kbd> + <kbd>I</kbd>（或在 Windows 或 Linux 上按 <kbd>Control</kbd> + <kbd>I</kbd>）来指示 [Chat2Query (beta)](/tidb-cloud/tidb-cloud-glossary.md#chat2query) 自动生成 SQL 查询。这使你无需本地 SQL 客户端即可对数据库运行 SQL 查询。你可以直观地以表格或图表形式查看查询结果，并轻松查看查询日志。

## 使用场景

SQL 编辑器的推荐使用场景如下：

- 利用 Chat2Query 的 AI 功能即时生成、调试或重写复杂的 SQL 查询。
- 快速测试 TiDB 的 MySQL 兼容性。
- 使用自己的数据集轻松探索 TiDB 中的 SQL 功能。

## 限制

- AI 生成的 SQL 查询可能不是 100% 准确，你可能需要对其进行优化。
- SQL 编辑器仅支持 v6.5.0 或更高版本且托管在 AWS 上的 TiDB 集群。
- SQL 编辑器默认适用于 [TiDB Cloud Serverless](/tidb-cloud/select-cluster-tier.md#tidb-cloud-serverless) 集群。要在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上使用 SQL 编辑器和 Chat2Query，请联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)。

## 访问 SQL 编辑器

1. 转到项目的[**集群**](https://tidbcloud.com/project/clusters)页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击集群名称，然后在左侧导航栏中点击 **SQL 编辑器**。

    > **注意：**
    >
    > 在以下情况下，**SQL 编辑器**入口显示为灰色且不可点击：
    >
    > - 你的 TiDB Cloud Dedicated 集群版本早于 v6.5.0。要使用 SQL 编辑器，你需要联系 [TiDB Cloud 支持团队](/tidb-cloud/tidb-cloud-support.md)升级集群。
    > - 你的 TiDB Cloud Dedicated 集群刚刚创建，SQL 编辑器的运行环境仍在准备中。在这种情况下，等待几分钟后 Chat2Query 就会可用。
    > - 你的 TiDB Cloud Dedicated 集群已[暂停](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

## 启用或禁用 AI 生成 SQL 查询

PingCAP 将用户数据的隐私和安全视为首要任务。SQL 编辑器中的 Chat2Query AI 功能只需要访问数据库架构来生成 SQL 查询，而不需要访问你的数据本身。更多信息，请参见 [Chat2Query 隐私常见问题](https://www.pingcap.com/privacy-policy/privacy-chat2query)。

当你首次访问 Chat2Query 时，会出现一个对话框，询问是否允许 PingCAP 和 Amazon Bedrock 使用你的代码片段来研究和改进服务。

- 要启用 AI 生成 SQL 查询，选中复选框并点击**保存并开始使用**。
- 要禁用 AI 生成 SQL 查询，直接关闭此对话框。

首次访问后，你仍然可以按照以下方式更改 AI 设置：

- 要启用 AI，点击 Chat2Query 右上角的**启用 AI 功能进行数据探索**。
- 要禁用 AI，点击 [TiDB Cloud 控制台](https://tidbcloud.com/) 左下角的 <MDSvgIcon name="icon-top-account-settings" />，点击**账户设置**，点击 **AI 和隐私**标签，然后禁用 **AI 驱动的数据探索**选项。

## 编写和运行 SQL 查询

在 SQL 编辑器中，你可以使用自己的数据集编写和运行 SQL 查询。

1. 编写 SQL 查询。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果启用了 AI，只需按 **⌘ + I** 后输入你的指令并按 **Enter** 键，即可让 AI 自动生成 SQL 查询。

        对于 Chat2Query 生成的 SQL 查询，点击**接受**以接受查询并继续编辑。如果查询不符合你的要求，点击**放弃**以拒绝它。或者，点击**重新生成**以从 Chat2Query 请求新的查询。

    - 如果禁用了 AI，手动编写 SQL 查询。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果启用了 AI，只需按 **Ctrl + I** 后输入你的指令并按 **Enter** 键，即可让 AI 自动生成 SQL 查询。

        对于 Chat2Query 生成的 SQL 查询，点击**接受**以接受查询并继续编辑。如果查询不符合你的要求，点击**放弃**以拒绝它。或者，点击**重新生成**以从 Chat2Query 请求新的查询。

    - 如果禁用了 AI，手动编写 SQL 查询。

    </div>
    </SimpleTab>

2. 运行 SQL 查询。

    <SimpleTab>
    <div label="macOS">

    对于 macOS：

    - 如果编辑器中只有一个查询，要运行它，按 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**运行**。

    - 如果编辑器中有多个查询，要按顺序运行其中一个或多个查询，用光标选择目标查询的行，然后按 **⌘ + Enter** 或点击**运行**。

    - 要按顺序运行编辑器中的所有查询，按 **⇧ + ⌘ + Enter**，或用光标选择所有查询的行并点击**运行**。

    </div>

    <div label="Windows/Linux">

    对于 Windows 或 Linux：

    - 如果编辑器中只有一个查询，要运行它，按 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**运行**。

    - 如果编辑器中有多个查询，要按顺序运行其中一个或多个查询，用光标选择目标查询的行，然后按 **Ctrl + Enter** 或点击**运行**。

    - 要按顺序运行编辑器中的所有查询，按 **Shift + Ctrl + Enter**，或用光标选择所有查询的行并点击**运行**。

    </div>
    </SimpleTab>

运行查询后，你可以立即在页面底部看到查询日志和结果。

> **注意：**
>
> 返回结果的大小限制为 8 MiB。

## 使用 Chat2Query 重写 SQL 查询

在 SQL 编辑器中，你可以使用 Chat2Query 重写现有的 SQL 查询，以优化性能、修复错误或满足其他特定要求。

1. 用光标选择要重写的 SQL 查询行。

2. 使用操作系统对应的键盘快捷键调用 Chat2Query 进行重写：

    - macOS 上按 <kbd>⌘</kbd> + <kbd>I</kbd>
    - Windows 或 Linux 上按 <kbd>Control</kbd> + <kbd>I</kbd>

    提供指令后按 **Enter** 键让 AI 处理重写。

3. 调用 Chat2Query 后，你可以看到建议的重写内容和以下选项：

    - **接受**：点击此项以接受建议的重写并继续编辑。
    - **放弃**：如果建议的重写不符合你的期望，点击此项。
    - **重新生成**：点击此项以根据你的反馈或额外指令从 Chat2Query 请求另一个重写。

> **注意：**
> 
> Chat2Query 使用 AI 算法来提供优化和修正建议。建议在最终确定查询之前仔细审查这些建议。

## 管理 SQL 文件

在 SQL 编辑器中，你可以将 SQL 查询保存在不同的 SQL 文件中，并按以下方式管理 SQL 文件：

- 要添加 SQL 文件，点击 **SQL 文件**标签上的 **+**。
- 要重命名 SQL 文件，将光标移到文件名上，点击文件名旁边的 **...**，然后选择**重命名**。
- 要删除 SQL 文件，将光标移到文件名上，点击文件名旁边的 **...**，然后选择**删除**。注意，当 **SQL 文件**标签上只有一个 SQL 文件时，你无法删除它。

## 通过 API 访问 Chat2Query

除了通过 UI 访问 Chat2Query 外，你还可以通过 API 访问 Chat2Query。要实现这一点，你需要先创建一个 Chat2Query Data App。

在 Chat2Query 中，你可以按以下方式访问或创建 Chat2Query Data App：

1. 点击右上角的 **...**，然后点击**通过 API 访问 Chat2Query**。
2. 在显示的对话框中，执行以下操作之一：

    - 要创建新的 Chat2Query Data App，点击**新建 Chat2Query Data App**。
    - 要访问现有的 Chat2Query Data App，点击目标 Data App 的名称。

更多信息，请参见[开始使用 Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

## 从 SQL 文件生成端点

对于 TiDB 集群，TiDB Cloud 提供了 [Data Service (beta)](/tidb-cloud/data-service-overview.md) 功能，使你能够使用自定义 API 端点通过 HTTPS 请求访问 TiDB Cloud 数据。在 SQL 编辑器中，你可以通过以下步骤从 SQL 文件生成 Data Service (beta) 的端点：

1. 将光标移到文件名上，点击文件名旁边的 **...**，然后选择**生成端点**。
2. 在**生成端点**对话框中，选择要为其生成端点的 Data App 并输入端点名称。
3. 点击**生成**。端点生成后，将显示其详细信息页面。

更多信息，请参见[管理端点](/tidb-cloud/data-service-manage-endpoint.md)。

## 管理 SQL 编辑器设置

在 SQL 编辑器中，你可以更改以下设置：

- 查询结果中的最大行数
- 是否在**架构**标签上显示系统数据库架构

要更改设置，请执行以下步骤：

1. 在 **SQL 编辑器**右上角，点击 **...** 并选择**设置**。
2. 根据需要更改设置。
3. 点击**保存**。
