---
title: TiDB Cloud CLI (`ti`) 命令参考
summary: 参考 TiDB Cloud CLI 命令组、语法、全局选项、输出、dry-run 行为、帮助形式和错误。
---

# TiDB Cloud CLI (`ti`) 命令参考

本页介绍 [TiDB Cloud CLI (`ti`)](/ai/ti/ti-overview.md) 命令共享的命令结构和行为。要查看单个命令的语法和选项，请选择其命令组或使用文档导航。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 语法 {#syntax}

```text
ti <command> [options] [global options]
ti <command-group> <command> [options] [global options]
```

例如：

```bash
ti configure --profile staging
ti db list-db-clusters --db-cluster-type starter
```

`ti` 可执行文件仅接受长选项。像 `-p` 这样的单字母选项会被拒绝。

在生成的用法说明中，必需选项应写在可选选项之前，并使用方括号括起可选选项：

```text
ti db describe-db-cluster
  --db-cluster-id <string>
  [--output <string>]
  [--view <string>]
```

值类型使用尖括号括起。在命令帮助中，每个必需选项的名称和类型后面都会跟随 `(required)`：

```text
--db-cluster-name <string> (required)   Starter DB cluster display name
--wait                                  Wait until the created cluster is active
```

## 命令和命令组 {#commands-and-command-groups}

使用下表查找顶层命令或命令组的参考文档。每个命令页面都包含其语法、选项和示例。

| 命令或命令组 | 用途 | 参考 |
| --- | --- | --- |
| `configure` | 配置本地配置（Profile）、API key 和默认 Region。 | [`ti configure`](/ai/ti/reference/ti-configure.md) |
| `update` | 检查并安装 TiDB Cloud CLI 更新。 | [`ti update`](/ai/ti/reference/ti-update.md) |
| `db` | 管理 TiDB Cloud Starter 实例、分支、SQL 用户、连接和 SQL 语句。 | [`ti db` 命令](/ai/ti/reference/ti-starter-database.md) |
| `fs` | 管理文件系统资源、AI provider、token、数据、层和挂载。 | [`ti fs` 命令](/ai/ti/reference/ti-filesystem.md) |
| `fs-git` | 管理已挂载文件系统上的 Git workspace。 | [`ti fs-git` 命令](/ai/ti/reference/ti-filesystem-git.md) |
| `fs-journal` | 管理可验证的文件系统日志（Journal）。 | [`ti fs-journal` 命令](/ai/ti/reference/ti-filesystem-journal.md) |
| `fs-vault` | 管理文件系统 Vault Secret 和委托访问。 | [`ti fs-vault` 命令](/ai/ti/reference/ti-filesystem-vault.md) |

要在终端中列出可用命令，请运行 `ti help` 或 `ti <command-group> help`。

## 全局选项 {#global-options}

- `--debug`：启用已脱敏的调试输出。
- `--output <string>`：将输出格式设置为 `json` 或 `text`。\[default: json]
- `--profile <string>`：选择本地配置（Profile）。\[default: default]
- `--query <string>`：在渲染输出之前应用 JMESPath 表达式。
- `--region <string>`：为当前命令覆盖配置中的默认 Region 代码，例如 `aws-us-east-1`。

命令页面会单独记录 `--help`、`--version` 以及所有命令特定选项。

## 输出 {#output}

返回结构化数据的命令默认使用 JSON：

```bash
ti db list-db-clusters --db-cluster-type starter
```

使用文本输出可获得更适合人工阅读的表示形式：

```bash
ti db list-db-clusters --db-cluster-type starter --output text
```

像 `ti fs read-file` 和 `ti fs copy-file --to-stdout` 这样的原始字节导向命令会直接写出文件内容。

## JMESPath 查询 {#jmespath-queries}

`--query` 会在命令成功执行之后、输出渲染之前运行：

```bash
ti db list-db-clusters \
  --db-cluster-type starter \
  --query 'clusters[].{id:id,name:display_name,state:state}'
```

无效的表达式会导致失败，不会用部分输出替代命令结果。

## 试运行 (Dry-run) {#dry-run}

支持 `--dry-run` 的变更型控制平面命令会验证本地选项、配置、凭证、Region 和请求结构，然后在不执行远程变异的情况下报告一个计划。

```bash
ti db delete-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --dry-run
```

只读命令会拒绝 `--dry-run`。该选项不是全局模拟选项，仅在命令帮助中显示时才可用。

## 帮助和版本形式 {#help-and-version-forms}

运行 `ti` 而不带命令时，会返回退出码 `2`，并将紧凑的命令树概要打印到 stderr：

```text
ti [ERROR]: the following arguments are required: command

The TiDB Cloud Command Line Interface is a unified tool to manage your TiDB Cloud Filesystem (FS) and Starter services.

usage: ti <command> [<subcommand>] [parameters]
To see help information, you can run:

  ti help
  ti <command> help
  ti <command> <subcommand> help
```

使用显式帮助形式来显示命令和选项：

```bash
ti help
ti db help
ti db create-db-cluster help
ti --help
ti --version
```

`help` 是一个用于浏览命令层级的命令。`--help` 在每个命令上都可用；这两种形式是有意并存的。`--version` 选项在每个命令级别也都可用，并报告同一个 `ti` 可执行文件的版本。

## 错误和退出行为 {#errors-and-exit-behavior}

人类可读的错误信息以一个空行开头，并使用稳定的前缀：

```text
ti [ERROR]: <message>
```

错误会写入 stderr，成功的命令输出会写入 stdout。用法和配置失败会在远程变异发生之前返回非零退出码。运行时和远程 API 失败也会返回非零退出码。交互式配置被中断时会返回退出码 `130`。

`--debug` 可以显示已脱敏的请求和解析上下文。它不得显示 API key、文件系统 token、DB 密码、SQL 文本、文件内容或连接字符串。

## 相关文档 {#related-documentation}

有关配置、安全性、兼容性和故障排查的详细信息，请参阅以下文档：

| 文档 | 用途 |
| --- | --- |
| [安装、配置和更新 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md) | 安装发布版本、配置 Profile、更新并卸载 `ti` |
| [TiDB Cloud CLI 配置和凭证](/ai/ti/reference/ti-configuration-and-credentials.md) | 了解配置（Profile）、优先级规则、凭证和本地状态 |
| [TiDB Cloud CLI Regions、安全性和限制](/ai/ti/reference/ti-regions-security-and-limitations.md) | 查看支持的 Region、凭证边界、平台支持和限制 |
| [从 `tdc` 迁移到 TiDB Cloud CLI](/ai/ti/reference/ti-migrate-from-tdc.md) | 从 `tdc` v0.1.x 迁移本地状态和环境变量 |
| [排查 TiDB Cloud CLI 问题](/ai/ti/reference/ti-troubleshooting.md) | 诊断配置、身份验证、路由和命令失败问题 |

## 发布说明 {#release-notes}

有关 TiDB Cloud CLI (`ti`) 的最新变更，请参阅 [TiDB Cloud CLI (`ti`) Release Notes](https://github.com/tidbcloud/ti-cli/releases)。