---
title: TiDB Cloud CLI (`ti`) 概述
summary: 了解何时使用 TiDB Cloud CLI (`ti`) 来管理 TiDB Cloud Starter 实例和 TiDB Cloud Filesystems。
---

# TiDB Cloud CLI (`ti`) 概述

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) 是一个用于管理 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) 实例和 [TiDB Cloud Filesystems](#tidb-cloud-filesystem) 的 CLI。它同时适用于交互式使用和自动化场景，并且默认提供结构化的 JSON 输出。

> **注意：**
>
> - TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不事先通知的情况下发生变化。
> - TiDB Cloud 当前提供两个作用域不同的 CLI：[`ti`](https://github.com/tidbcloud/ti-cli) 和 [`ticloud`](https://github.com/tidbcloud/tidbcloud-cli)。要了解何时使用 `ti` 或 `ticloud`，请参见[ `ti` 与 `ticloud` 的区别](#differences-between-ti-and-ticloud)和[何时使用 TiDB Cloud CLI (`ti`)](#when-to-use-tidb-cloud-cli-ti)。

## TiDB Cloud Filesystem {#tidb-cloud-filesystem}

TiDB Cloud Filesystem 是一个面向 AI agent 和自动化工作负载设计的无服务器分布式文件系统。它提供持久、可共享的文件命名空间，并且独立于访问它的本地机器、沙箱或 CI runner 持续可用，因此非常适合持久化存储、共享工作区以及 AI agent 工作流。

## 何时使用 TiDB Cloud CLI (`ti`) {#when-to-use-tidb-cloud-cli-ti}

当你希望通过终端、脚本、CI 作业或 AI agent 环境来管理 TiDB Cloud 时，请使用 TiDB Cloud CLI (`ti`)。

| 典型使用场景 | 你可以执行的操作 |
| --- | --- |
| 自动化 TiDB Cloud Starter 生命周期操作 | 创建和管理 TiDB Cloud Starter 实例与分支，等待其就绪，以 JSON 形式检查结果，执行 SQL 语句，并按 ID 删除资源。 |
| 按任务分离 SQL 权限 | 为每个任务使用由 CLI 管理的只读、读写或管理员身份，而无需在每条命令中处理数据库密码。 |
| 在不同环境之间持久化并共享文件 | 让文件在本地机器、CI 作业、沙箱及其他临时环境之间保持可用，并通过直接文件命令或受支持的 FUSE 和 WebDAV 挂载访问同一个远程命名空间。 |
| 在临时环境中使用 Filesystems | 在受信任的机器上预配一个 Filesystem，然后将其 Filesystem 访问令牌和 region code 提供给沙箱，而无需复制 CLI 配置（Profile）或提供 TiDB Cloud API key。 |
| 更早启动大型 Git 工作区 | 在后台继续为干净的 Git 数据补全内容的同时，先暴露仓库文件树。 |
| 记录并委派 agent 工作 | 将仅追加的、基于哈希链的工作流事件存储在日志（Journal）中，并对选定的 Vault 字段授予临时且有作用域限制的访问权限。 |

对于可视化、引导式工作流，请使用 [TiDB Cloud console](https://tidbcloud.com/)。对于 TiDB Cloud Essential 或 `ti` 不支持的操作，请使用 [`ticloud`](#differences-between-ti-and-ticloud)。

## TiDB Cloud CLI 管理的内容 {#what-tidb-cloud-cli-manages}

TiDB Cloud CLI 涵盖以下功能领域：

- **TiDB Cloud Starter**
    - 实例和分支生命周期操作
    - SQL 用户和连接信息
    - SQL 语句执行
- **TiDB Cloud Filesystem**
    - Filesystem 生命周期和文件操作
    - FUSE 和 WebDAV 挂载
    - 层、packs 和 Git 工作区
    - Journals 和 vaults
- **CLI 配置**
    - Profiles、regions 和本地凭证
    - CLI 更新
    - 输出格式化和 JMESPath 查询

大多数资源命令遵循两级命令模型：

```text
ti <command-group> <operation>
```

例如，`ti db list-db-clusters --db-cluster-type starter`、`ti fs copy-file` 和 `ti fs-journal verify-journal`。

你还可以使用顶层命令 `ti configure` 和 `ti update` 来配置和维护 CLI。

## `ti` 与 `ticloud` 的区别 {#differences-between-ti-and-ticloud}

TiDB Cloud 当前提供两个作用域不同的 CLI：`ti` 和 [`ticloud`](https://docs.pingcap.com/tidbcloud/cli-reference)。

`ti` 专为 TiDB Cloud Starter 的自动化以及 TiDB Cloud Filesystems 管理而设计，而 `ticloud` 继续支持 TiDB Cloud Essential 以及 `ti` 中尚不可用的其他 TiDB Cloud 操作。

| CLI | 最适合 | 关键特性 |
| --- | --- | --- |
| `ti` | 受支持的 TiDB Cloud Starter 自动化工作流和 TiDB Cloud Filesystems | 为自动化而设计；默认输出 JSON；命令支持非交互式工作流，同时 `ti configure` 也可以进行交互式提示 |
| `ticloud` | TiDB Cloud Essential、现有的 TiDB Cloud Starter 工作流，以及 `ti` 中不可用的操作（例如数据导入、数据导出和审计日志操作） | 支持 `ti` 中不可用的其他 TiDB Cloud 操作，并同时支持交互式和非交互式模式 |

`ti` 并不替代 `ticloud`。请根据你需要的资源和操作选择 CLI：

- 对于新的 TiDB Cloud Starter 自动化工作流，如果 `ti` 支持你需要的操作，请使用 `ti`。
- 对于管理 TiDB Cloud Filesystems，请使用 `ti`。
- 如果你已有用于 TiDB Cloud Starter 或 TiDB Cloud Essential 的 `ticloud` 工作流，可以继续使用它们。
- 对于 TiDB Cloud Essential 或 `ti` 中不可用的操作（例如数据导入、数据导出和审计日志操作），请使用 [`ticloud`](https://docs.pingcap.com/tidbcloud/cli-reference)。

## 后续步骤 {#next-steps}

如果你是第一次使用 TiDB Cloud CLI，请先阅读[快速开始](/ai/ti/ti-quick-start.md)，安装 `ti`、配置 profile，并完成一个基础的 TiDB Cloud Starter 或 Filesystem 工作流。

然后根据你的目标继续阅读：

- [管理 TiDB Cloud Starter 实例](/ai/ti/guides/manage-starter-instances.md)
- [管理 TiDB Cloud Filesystems](/ai/ti/guides/manage-filesystem-resources.md)
- **按照端到端工作流操作**：从[运行日常 TiDB Cloud CLI 工作流](/ai/ti/guides/ti-daily-workflow-example.md)或[在 Agent Sandbox 中使用 TiDB Cloud Filesystem](/ai/ti/guides/ti-agent-sandbox-example.md)开始
- **查找特定命令**：查看 [TiDB Cloud CLI 命令参考](/ai/ti/reference/ti-cli-reference.md)
- **查看 TiDB Cloud CLI 的新功能**：查看 [TiDB Cloud CLI (`ti`) Release Notes](https://github.com/tidbcloud/ti-cli/releases)
- **报告问题**：在 [TiDB Cloud CLI GitHub repository](https://github.com/tidbcloud/ti-cli/issues) 中创建 issue。