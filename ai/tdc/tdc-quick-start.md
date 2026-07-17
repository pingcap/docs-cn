---
title: 快速上手 TiDB Cloud CLI（tdc）
summary: 安装和配置 tdc，并完成第一个 TiDB Cloud Starter 数据库或文件系统操作。
---

# 快速上手 TiDB Cloud CLI（tdc）

本快速上手将帮助你安装 tdc、配置一个 profile，并通过 TiDB Cloud Starter 或 TiDB Cloud 文件系统获得第一个成功结果。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 前置条件

开始前，请从 [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) 页面获取 API public key 和 private key。该 key 必须能够访问一个 `tidbx_virtual` project。

## 第 1 步：安装 tdc

在 macOS 或 Linux 上：

```bash
curl -fsSL https://github.com/tidbcloud/tdc/releases/latest/download/install.sh | sh -s -- --yes
export PATH="$HOME/.tdc/bin:$PATH"
tdc --version
```

将 `export PATH="$HOME/.tdc/bin:$PATH"` 加入 shell profile，使新终端也能找到 tdc。

在 Windows PowerShell 上：

```powershell
$script = "$env:TEMP\install-tdc.ps1"
iwr https://github.com/tidbcloud/tdc/releases/latest/download/install.ps1 -OutFile $script
powershell -ExecutionPolicy Bypass -File $script -Yes
$env:Path = "$HOME\.tdc\bin;$env:Path"
tdc --version
```

## 第 2 步：配置 tdc

运行交互式配置：

```bash
tdc configure
```

输入 API public key、private key，以及 `aws-us-east-1` 之类的 canonical region code。tdc 会验证 key、发现 `tidbx_virtual` project，并将其保存为默认 project。

验证配置：

```bash
tdc organization list-projects --output text
```

## 第 3 步：选择第一个 workflow

选择完成文件系统或 Starter 数据库 workflow。

### 选项 A：写入并读取文件

创建文件系统，并在不显示完整结果的情况下获取 owner token：

```bash
export TDC_FS_TOKEN="$(tdc fs create-file-system \
  --file-system-name quickstart-fs \
  --query fs_token \
  --output text)"
```

通过 data plane 写入并读取文件：

```bash
printf 'hello from tdc\n' | tdc fs copy-file \
  --file-system-name quickstart-fs \
  --from-stdin \
  --to-remote /hello.txt

tdc fs read-file \
  --file-system-name quickstart-fs \
  --path /hello.txt
```

预期输出：

```text
hello from tdc
```

清理：

```bash
tdc fs delete-file-system \
  --file-system-name quickstart-fs \
  --confirm-file-system-name quickstart-fs
unset TDC_FS_TOKEN
```

### 选项 B：查询 Starter 数据库

列出集群并选择一个 active cluster ID：

```bash
tdc db list-db-clusters --output text
export TDC_DB_CLUSTER_ID="<active-cluster-id>"
```

如果该集群还没有 tdc 管理的 SQL 用户，则创建这些用户：

```bash
tdc db create-db-sql-users --db-cluster-id "$TDC_DB_CLUSTER_ID"
```

运行只读验证查询：

```bash
tdc db execute-sql-statement \
  --db-cluster-id "$TDC_DB_CLUSTER_ID" \
  --read-only \
  --sql "SELECT 1 AS ready" \
  --output text
```

该命令通过 HTTPS SQL API 执行一条 statement，并返回包含 `ready = 1` 的结果。

## 后续步骤

- [管理 TiDB Cloud Starter 数据库](/ai/tdc/guides/tdc-starter-database.md)
- [管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
