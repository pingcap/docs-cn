---
title: TiDB Cloud CLI（tdc）概览
summary: 了解预览版 tdc 命令行如何为用户、脚本和 AI Agent 管理 TiDB Cloud Starter 数据库与 TiDB Cloud 文件系统。
---

# TiDB Cloud CLI（tdc）概览

tdc 是用于管理 TiDB Cloud Starter 数据库和 TiDB Cloud 文件系统的命令行工具。它提供确定性的 JSON 输出、显式权限、可脚本化配置，以及同时面向用户与 AI Agent 的命令设计。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## tdc 能做什么

你可以使用 tdc：

- 创建、查看、更新和删除 TiDB Cloud Starter 集群；
- 创建和管理 Starter 分支；
- 创建只读、读写和管理员 SQL 用户，格式化连接字符串并执行 SQL；
- 在一个 profile 中创建和选择多个 TiDB Cloud 文件系统资源；
- 直接访问文件系统数据，或者通过 FUSE、WebDAV 挂载；
- 使用文件系统 layer、pack、Git workspace、仅追加 journal 和委派密钥；
- 在脚本和 Agent 工作流中使用 JSON 输出与 JMESPath 查询。

tdc 使用两级命令模型：

```text
tdc <service> <operation>
```

例如 `tdc db list-db-clusters`、`tdc fs copy-file` 和 `tdc fs-journal verify-journal`。顶层的 `tdc configure` 和 `tdc update` 分别用于配置和维护 CLI。

## tdc 与 Drive9

tdc 会安装名为 `tdc-drive9` 的内置 [Drive9](https://github.com/mem9-ai/drive9) companion。tdc 负责 profile 选择、TiDB Cloud 凭证、region 与文件系统选择、输出格式和错误处理；companion 负责文件系统数据面语义、FUSE/WebDAV 挂载、layer、pack/unpack、Git workspace 加速、Journal 和 Vault。

在常规 tdc 工作流中，你不需要单独安装、配置或调用 Drive9。

## 开始使用 tdc

- [快速上手](/ai/tdc/tdc-quick-start.md)
- [概念与架构](/ai/tdc/concepts/tdc-concepts-and-architecture.md)

### 使用指南

- [安装、配置和更新 tdc](/ai/tdc/guides/tdc-install-configure-update.md)
- [管理 TiDB Cloud Organization](/ai/tdc/guides/tdc-organization.md)
- [管理 TiDB Cloud Starter 数据库](/ai/tdc/guides/tdc-starter-database.md)
- [管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
- [在 TiDB Cloud 文件系统中使用 Git Workspace](/ai/tdc/guides/tdc-filesystem-git.md)
- [使用文件系统 Journal](/ai/tdc/guides/tdc-filesystem-journal.md)
- [使用文件系统 Vault](/ai/tdc/guides/tdc-filesystem-vault.md)

### 场景示例

- [在 Agent Sandbox 中使用文件系统](/ai/tdc/examples/tdc-agent-sandbox-example.md)
- [执行日常 tdc 工作流](/ai/tdc/examples/tdc-daily-workflow-example.md)
- [使用显式角色查询 SQL](/ai/tdc/examples/tdc-query-sql-with-roles-example.md)
- [在不同机器间共享文件系统](/ai/tdc/examples/tdc-share-filesystem-across-machines-example.md)
- [为 Agent 准备 Git Workspace](/ai/tdc/examples/tdc-git-workspace-for-agents-example.md)
- [使用 Journal 记录 Agent 工作流](/ai/tdc/examples/tdc-journal-agent-workflow-example.md)
- [向 Agent 委派 Vault 密钥](/ai/tdc/examples/tdc-vault-agent-secrets-example.md)

### 参考

- [tdc CLI 参考](/ai/tdc/reference/tdc-cli-reference.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [tdc 区域、安全与限制](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
- [tdc 故障排查](/ai/tdc/reference/tdc-troubleshooting.md)

如需报告问题或提出改进建议，请在 [tdc GitHub 仓库](https://github.com/tidbcloud/tdc/issues)创建 issue。
