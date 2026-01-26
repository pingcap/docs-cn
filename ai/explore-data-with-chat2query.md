---
title: 使用 AI 辅助 SQL 编辑器探索你的数据
summary: 了解如何在 TiDB Cloud 控制台中使用 AI 辅助 SQL 编辑器，最大化你的数据价值。
---

# 使用 AI 辅助 SQL 编辑器探索你的数据 <!-- Draft translated by AI -->

你可以在 [TiDB Cloud 控制台](https://tidbcloud.com/)中使用内置的 AI 辅助 SQL 编辑器，最大化你的数据价值。

在 SQL 编辑器中，你可以手动编写 SQL 查询，或者只需在 macOS 上按下 <kbd>⌘</kbd> + <kbd>I</kbd>（或在 Windows 或 Linux 上按下 <kbd>Control</kbd> + <kbd>I</kbd>），即可指示 [Chat2Query (beta)](/ai/tidb-cloud-glossary.md#chat2query) 自动生成 SQL 查询。这样，你无需本地 SQL 客户端即可对数据库运行 SQL 查询。你可以直观地在表格或图表中查看查询结果，并轻松检查查询日志。

## 使用场景

SQL 编辑器推荐的使用场景如下：

- 利用 Chat2Query 的 AI 能力，快速生成、调试或重写复杂的 SQL 查询。
- 快速测试 TiDB 的 MySQL 兼容性。
- 使用你自己的数据集，轻松探索 TiDB 的 SQL 特性。

## 限制

- AI 生成的 SQL 查询可能并非 100% 准确，你可能需要对其进行优化。
- SQL 编辑器仅支持部署在 AWS 上、版本为 v6.5.0 及以上的 TiDB 集群。

## 前提条件

目前，只有部署在 AWS 上的 [TiDB Cloud Starter](/tidb-cloud/select-cluster-tier.md#starter) 集群在控制台上提供了 SQL 编辑器。如需使用该编辑器，你需要先[创建一个部署在 AWS 上的 TiDB Cloud Starter 集群](https://docs.pingcap.com/zh/tidbcloud/tidb-cloud-intro/)。

> **注意：**
>
> 如需在 [TiDB Cloud Dedicated](/tidb-cloud/select-cluster-tier.md#tidb-cloud-dedicated) 集群上使用 SQL 编辑器和 Chat2Query，请联系 [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md)。

## 访问 SQL 编辑器

1. 进入你的项目的 [**Clusters**](https://tidbcloud.com/project/clusters) 页面。

    > **提示：**
    >
    > 你可以使用左上角的下拉框在组织、项目和集群之间切换。

2. 点击你的集群名称，然后在左侧导航栏点击 **SQL Editor**。

    > **注意：**
    >
    > 在以下情况下，**SQL Editor** 入口会显示为灰色且不可点击。
    >
    > - 你的 TiDB Cloud Dedicated 集群版本低于 v6.5.0。如需使用 SQL 编辑器，你需要联系 [TiDB Cloud support](/tidb-cloud/tidb-cloud-support.md) 升级你的集群。
    > - 你的 TiDB Cloud Dedicated 集群刚刚创建，SQL 编辑器的运行环境仍在准备中。此时请等待几分钟，Chat2Query 即可使用。
    > - 你的 TiDB Cloud Dedicated 集群已被 [暂停](/tidb-cloud/pause-or-resume-tidb-cluster.md)。

## 启用或禁用 AI 生成 SQL 查询

PingCAP 将用户数据的隐私和安全放在首位。SQL 编辑器中 Chat2Query 的 AI 能力仅需访问数据库的 schema 信息来生成 SQL 查询，不会访问你的数据本身。更多信息请参见 [Chat2Query 隐私常见问题](https://www.pingcap.com/privacy-policy/privacy-chat2query)。

首次访问 Chat2Query 时，你会看到一个对话框，询问是否允许 PingCAP 和 Amazon Bedrock 使用你的代码片段进行服务研究和改进。

- 若要启用 AI 生成 SQL 查询，请勾选复选框并点击 **Save and Get Started**。
- 若要禁用 AI 生成 SQL 查询，直接关闭该对话框即可。

首次访问后，你仍然可以按如下方式更改 AI 设置：

- 若要启用 AI，在 Chat2Query 右上角点击 **Enable AI power for data exploration**。
- 若要禁用 AI，在 [TiDB Cloud 控制台](https://tidbcloud.com/) 左下角点击 <MDSvgIcon name="icon-top-account-settings" />，点击 **Account Settings**，切换到 **AI & Privacy** 标签页，然后关闭 **AI-powered Data Exploration** 选项。

## 编写并运行 SQL 查询

在 SQL 编辑器中，你可以使用你自己的数据集编写并运行 SQL 查询。

1. 编写 SQL 查询。

    <SimpleTab>
    <div label="macOS">

    针对 macOS：

    - 如果已启用 AI，只需按下 **⌘ + I**，输入你的指令并按 **Enter**，即可让 AI 自动生成 SQL 查询。

        对于 Chat2Query 生成的 SQL 查询，点击 **Accept** 接受该查询并继续编辑。如果查询不符合你的需求，点击 **Discard** 拒绝该查询。你也可以点击 **Regenerate** 让 Chat2Query 重新生成查询。

    - 如果未启用 AI，则需手动编写 SQL 查询。

    </div>

    <div label="Windows/Linux">

    针对 Windows 或 Linux：

    - 如果已启用 AI，只需按下 **Ctrl + I**，输入你的指令并按 **Enter**，即可让 AI 自动生成 SQL 查询。

        对于 Chat2Query 生成的 SQL 查询，点击 **Accept** 接受该查询并继续编辑。如果查询不符合你的需求，点击 **Discard** 拒绝该查询。你也可以点击 **Regenerate** 让 Chat2Query 重新生成查询。

    - 如果未启用 AI，则需手动编写 SQL 查询。

    </div>
    </SimpleTab>

2. 运行 SQL 查询。

    <SimpleTab>
    <div label="macOS">

    针对 macOS：

    - 如果编辑器中只有一个查询，按 **⌘ + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 即可运行。

    - 如果编辑器中有多个查询，选中目标查询的行，然后按 **⌘ + Enter** 或点击 **Run**，即可依次运行所选查询。

    - 若要依次运行编辑器中的所有查询，按 **⇧ + ⌘ + Enter**，或选中所有查询的行后点击 **Run**。

    </div>

    <div label="Windows/Linux">

    针对 Windows 或 Linux：

    - 如果编辑器中只有一个查询，按 **Ctrl + Enter** 或点击 <svg width="1rem" height="1rem" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M6.70001 20.7756C6.01949 20.3926 6.00029 19.5259 6.00034 19.0422L6.00034 12.1205L6 5.33028C6 4.75247 6.00052 3.92317 6.38613 3.44138C6.83044 2.88625 7.62614 2.98501 7.95335 3.05489C8.05144 3.07584 8.14194 3.12086 8.22438 3.17798L19.2865 10.8426C19.2955 10.8489 19.304 10.8549 19.3126 10.8617C19.4069 10.9362 20 11.4314 20 12.1205C20 12.7913 19.438 13.2784 19.3212 13.3725C19.307 13.3839 19.2983 13.3902 19.2831 13.4002C18.8096 13.7133 8.57995 20.4771 8.10002 20.7756C7.60871 21.0812 7.22013 21.0683 6.70001 20.7756Z" fill="currentColor"></path></svg>**Run** 即可运行。

    - 如果编辑器中有多个查询，选中目标查询的行，然后按 **Ctrl + Enter** 或点击 **Run**，即可依次运行所选查询。

    - 若要依次运行编辑器中的所有查询，按 **Shift + Ctrl + Enter**，或选中所有查询的行后点击 **Run**。

    </div>
    </SimpleTab>

运行查询后，你可以在页面底部立即看到查询日志和结果。

> **注意：**
>
> 返回结果有 8 MiB 的大小限制。

## 使用 Chat2Query 重写 SQL 查询

在 SQL 编辑器中，你可以使用 Chat2Query 重写已有的 SQL 查询，以优化性能、修复错误或满足其他特定需求。

1. 用光标选中你想要重写的 SQL 查询行。

2. 使用对应操作系统的快捷键调用 Chat2Query 进行重写：

    - macOS：<kbd>⌘</kbd> + <kbd>I</kbd>
    - Windows 或 Linux：<kbd>Control</kbd> + <kbd>I</kbd>

    输入你的指令后按 **Enter**，让 AI 进行重写。

3. 调用 Chat2Query 后，你会看到建议的重写内容，并有以下选项：

    - **Accept**：点击此按钮接受建议的重写并继续编辑。
    - **Discard**：如果建议的重写不符合你的预期，点击此按钮拒绝。
    - **Regenerate**：根据你的反馈或补充指令，点击此按钮让 Chat2Query 重新生成重写内容。

> **注意：**
> 
> Chat2Query 使用 AI 算法提供优化和修正建议。建议你在最终确定查询前，仔细审查这些建议。

## 管理 SQL 文件

在 SQL 编辑器中，你可以将 SQL 查询保存在不同的 SQL 文件中，并按如下方式管理 SQL 文件：

- 新增 SQL 文件：点击 **SQL Files** 标签页上的 **+**。
- 重命名 SQL 文件：将光标移到文件名上，点击文件名旁的 **...**，然后选择 **Rename**。
- 删除 SQL 文件：将光标移到文件名上，点击文件名旁的 **...**，然后选择 **Delete**。注意，当 **SQL Files** 标签页上只剩一个 SQL 文件时，无法删除该文件。

## 通过 API 访问 Chat2Query

除了通过 UI 访问 Chat2Query，你还可以通过 API 访问 Chat2Query。为此，你需要先创建一个 Chat2Query Data App。

在 Chat2Query 中，你可以按如下方式访问或创建 Chat2Query Data App：

1. 点击右上角的 **...**，然后点击 **Access Chat2Query via API**。
2. 在弹出的对话框中，执行以下操作之一：

    - 若要创建新的 Chat2Query Data App，点击 **New Chat2Query Data App**。
    - 若要访问已有的 Chat2Query Data App，点击目标 Data App 的名称。

更多信息请参见 [Get started with Chat2Query API](/tidb-cloud/use-chat2query-api.md)。

## 从 SQL 文件生成 endpoint

对于 TiDB 集群，TiDB Cloud 提供了 [Data Service (beta)](/tidb-cloud/data-service-overview.md) 功能，使你可以通过自定义 API endpoint 以 HTTPS 请求方式访问 TiDB Cloud 数据。在 SQL 编辑器中，你可以通过以下步骤从 SQL 文件生成 Data Service (beta) 的 endpoint：

1. 将光标移到文件名上，点击文件名旁的 **...**，然后选择 **Generate endpoint**。
2. 在 **Generate endpoint** 对话框中，选择你要为其生成 endpoint 的 Data App，并输入 endpoint 名称。
3. 点击 **Generate**。endpoint 生成后会显示其详情页面。

更多信息请参见 [Manage an endpoint](/tidb-cloud/data-service-manage-endpoint.md)。

## 管理 SQL 编辑器设置

在 SQL 编辑器中，你可以更改以下设置：

- 查询结果的最大行数
- 是否在 **Schemas** 标签页显示系统数据库 schema

更改设置的步骤如下：

1. 在 **SQL Editor** 右上角点击 **...** 并选择 **Settings**。
2. 根据需要更改设置。
3. 点击 **Save**。