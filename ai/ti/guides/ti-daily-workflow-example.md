---
title: 运行日常 TiDB Cloud CLI 工作流
summary: 检查资源、管理 TiDB Cloud Starter 实例和文件系统、检查 TiDB Cloud CLI 更新并清理资源。
---

# 运行日常 TiDB Cloud CLI 工作流

本示例展示了一个跨 TiDB Cloud Starter 和 TiDB Cloud Filesystem 的典型运维工作流。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 前提条件 {#prerequisites}

- 安装 `ti` 并运行 `ti configure`。
- 确保你的组织具有一个 TiDB Cloud Starter 实例和一个文件系统的容量。

## 步骤 1：检查当前资源 {#step-1-inspect-current-resources}

```bash
ti db list-db-clusters --db-cluster-type starter --output text
ti fs list-file-systems --output text
```

## 步骤 2：创建一个 TiDB Cloud Starter 实例 {#step-2-create-a-tidb-cloud-starter-instance}

```bash
ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name daily-demo \
  --dry-run

export DB_CLUSTER_ID="$(ti db create-db-cluster \
  --db-cluster-type starter \
  --db-cluster-name daily-demo \
  --wait \
  --query id \
  --output text)"
```

该命令会将返回的集群 ID 保存到 `DB_CLUSTER_ID` 中。由于设置了 `--wait`，创建命令会在集群变为活动状态后才返回。你也可以稍后再次查看它：

```bash
ti db describe-db-cluster \
  --db-cluster-id "$DB_CLUSTER_ID" \
  --output text
```

## 步骤 3：验证 SQL 访问 {#step-3-verify-sql-access}

```bash
ti db create-db-sql-users --db-cluster-id "$DB_CLUSTER_ID"
ti db execute-sql-statement \
  --db-cluster-id "$DB_CLUSTER_ID" \
  --read-only \
  --sql "SELECT CURRENT_TIMESTAMP AS checked_at" \
  --output text
```

## 步骤 4：创建并使用文件系统 {#step-4-create-and-use-a-filesystem}

```bash
export TI_FS_FILE_SYSTEM_ID="$(ti fs create-file-system \
  --wait \
  --query file_system_id \
  --output text)"

printf 'daily workflow\n' | ti fs copy-file \
  --from-stdin \
  --to-remote /notes/today.txt

ti fs list-files \
  --path /notes \
  --output text
```

`/notes/today.txt` 中的文件可用于验证显式选择的资源是否可用。

## 步骤 5：检查更新 {#step-5-check-for-updates}

在不更改已安装版本的情况下，检查是否有可用的新版本：

```bash
ti update --check
```

预览更新：

```bash
ti update --dry-run
```

如果另一个工作流存在活动中的文件系统或 Vault 挂载，请在应用更新前先停止写入端并卸载它，以便 `ti` 和文件系统运行时一起更新。有关说明，请参见[更新 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md#update-tidb-cloud-cli)。

在适当的时候应用更新：

```bash
ti update
```

## 清理 {#cleanup}

```bash
ti fs delete-file-system \
  --file-system-id "$TI_FS_FILE_SYSTEM_ID"

ti db delete-db-cluster \
  --db-cluster-id "$DB_CLUSTER_ID"
```

> **Note:**
>
> 删除本地 TiDB Cloud CLI 配置不会删除远程资源。

## 安全说明 {#security-notes}

- 不要回显文件系统 token 或格式化后的数据库连接字符串。
- 使用唯一的自动化前缀，并且只删除该次运行创建的资源。
- 使用 `--dry-run` 预览破坏性操作。

## 后续内容 {#what-s-next}

- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)