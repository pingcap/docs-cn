---
title: 执行日常 tdc Workflow
summary: 查看 project、管理 Starter 集群和文件系统、检查 tdc 更新并清理资源。
---

# 执行日常 tdc Workflow

本示例展示跨 TiDB Cloud Starter 和 TiDB Cloud 文件系统的典型 operator workflow。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

- 安装 tdc 并运行 `tdc configure`。
- 确保 organization 有一个 Starter 集群和一个文件系统的可用 quota。

## 第 1 步：查看 active account

```bash
tdc organization list-projects --output text
tdc db list-db-clusters --output text
tdc fs list-file-systems --output text
```

## 第 2 步：创建 Starter 集群

```bash
tdc db create-db-cluster \
  --db-cluster-name daily-demo \
  --db-cluster-type starter \
  --dry-run

tdc db create-db-cluster \
  --db-cluster-name daily-demo \
  --db-cluster-type starter
```

记录返回的 cluster ID，并等待集群 active：

```bash
tdc db describe-db-cluster \
  --db-cluster-id "<cluster-id>" \
  --output text
```

## 第 3 步：验证 SQL 访问

```bash
tdc db create-db-sql-users --db-cluster-id "<cluster-id>"
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT CURRENT_TIMESTAMP AS checked_at" \
  --output text
```

## 第 4 步：创建并使用文件系统

```bash
tdc fs create-file-system \
  --file-system-name daily-workspace \
  --set-default

printf 'daily workflow\n' | tdc fs copy-file \
  --from-stdin \
  --to-remote /notes/today.txt

tdc fs list-files --path /notes --output text
```

`/notes/today.txt` 验证所选默认资源可用。

## 第 5 步：检查更新

应用更新前 unmount active filesystem。Check 始终不修改文件：

```bash
tdc update --check
```

在合适时应用更新：

```bash
tdc update --dry-run
tdc update
```

## 清理

```bash
tdc fs delete-file-system \
  --file-system-name daily-workspace \
  --confirm-file-system-name daily-workspace

tdc db delete-db-cluster \
  --db-cluster-id "<cluster-id>"
```

删除本地 tdc 配置不能替代删除远端资源。

## 安全说明

- 不要 echo FS token 或格式化后的数据库连接字符串。
- 自动化使用唯一 prefix，只删除本次运行创建的资源。
- 使用 `--dry-run` 预览 destructive operation。

## 后续步骤

- [管理 TiDB Cloud Starter 数据库](/ai/tdc/guides/tdc-starter-database.md)
- [使用 tdc 管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
