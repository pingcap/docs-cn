---
title: 排查 TiDB Cloud CLI
summary: 了解如何安全地诊断 TiDB Cloud CLI 中与 API 身份验证、Starter 配额、SQL 凭据以及命令中断相关的故障。
---

# 排查 TiDB Cloud CLI

使用本文档排查 CLI 身份验证、Starter、SQL 以及命令中断相关的故障。有关文件系统令牌、Region、配套进程和挂载的问题，请参见 [排查 TiDB Cloud Filesystem](/tidb-cloud-filesystem/filesystem-troubleshooting.md)。仅在需要时添加 `--debug`；在分享脱敏后的输出前，仍应先自行检查。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## API 身份验证失败 {#api-authentication-fails}

常见症状包括凭据缺失、Digest 身份验证失败或权限被拒绝。

检查以下两个环境变量是否同时已设置：

```bash
test -n "$TIDB_CLOUD_PUBLIC_KEY"
test -n "$TIDB_CLOUD_PRIVATE_KEY"
```

如果你打算使用已保存的凭据，请取消设置这两个变量，并验证配置（Profile）：

```bash
unset TIDB_CLOUD_PUBLIC_KEY TIDB_CLOUD_PRIVATE_KEY
ti db list-db-clusters --db-cluster-type starter --profile default
```

API key 可能能够成功完成身份验证，但仍然缺少某个命令声明所需的权限。请使用具备该操作所需访问权限的 key。`ti configure` 只会验证并存储本地值，不会联系 TiDB Cloud，因此凭据失败通常会在执行远程命令时首次出现。

## Starter 创建达到配额 {#starter-creation-reaches-quota}

配额和容量错误可能意味着组织已达到其免费 Starter 限额。在创建另一个 Starter 资源之前，请先列出现有的 Starter 资源：

```bash
ti db list-db-clusters --db-cluster-type starter --output text
```

切勿删除不相关的资源来让自动化流程通过。Starter 的支出限制可能要求先配置计费。

## SQL 凭据缺失 {#sql-credentials-are-missing}

为目标集群准备或修复用户：

```bash
ti db create-db-sql-users --db-cluster-id "<cluster-id>"
```

然后使用显式角色重试：

```bash
ti db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT 1"
```

删除 `~/.ti/db_users/<cluster-id>/credentials` 会移除本地密码。请运行 create/repair 命令，而不是自行编造凭据。

## 被中断的命令会留下资源 {#an-interrupted-command-leaves-resources}

列出资源，并仅识别由你的工作流创建的资源。删除前先使用 describe 进行确认：

```bash
ti db describe-db-cluster --db-cluster-id "<cluster-id>"
ti fs describe-file-system --file-system-id "<file-system-id>"
```

预览支持的清理操作：

```bash
ti db delete-db-cluster --db-cluster-id "<cluster-id>" --dry-run
ti fs delete-file-system \
  --file-system-id "<file-system-id>" \
  --dry-run
```

## 报告问题 {#report-a-problem}

请提供 TiDB Cloud CLI 版本、操作系统和架构、命令名称、稳定错误码以及已脱敏的日志。切勿包含 API keys、FS 或 vault tokens、DB 密码、包含私有数据的 SQL，或文件内容。请在 [github.com/tidbcloud/ti-cli/issues](https://github.com/tidbcloud/ti-cli/issues) 报告问题。