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

开始前，请从 [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) 页面获取 API public key 和 private key。

## 第 1 步：安装 tdc

在 macOS 或 Linux 上运行安装程序：

```bash
curl -fsSL https://github.com/tidbcloud/tdc/releases/latest/download/install.sh | sh -s -- --yes
```

安装完成后，将 tdc 加入当前 shell 并验证安装：

```bash
export PATH="$HOME/.tdc/bin:$PATH"
tdc --version
```

将 `export PATH="$HOME/.tdc/bin:$PATH"` 加入 shell profile，使新终端也能找到 tdc。

在 Windows PowerShell 上运行安装程序：

```powershell
$script = "$env:TEMP\install-tdc.ps1"
iwr https://github.com/tidbcloud/tdc/releases/latest/download/install.ps1 -OutFile $script
powershell -ExecutionPolicy Bypass -File $script -Yes
```

安装完成后，将 tdc 加入当前 PowerShell session 并验证安装：

```powershell
$env:Path = "$HOME\.tdc\bin;$env:Path"
tdc --version
```

将 `$HOME\.tdc\bin` 加入用户 `PATH`，使新 PowerShell session 也能找到 tdc。

## 第 2 步：配置 tdc

运行交互式配置：

```bash
tdc configure
```

输入 API public key、private key，以及 `aws-us-east-1` 之类的 canonical region code。

验证配置：

```bash
tdc organization list-projects --output text
```

## 第 3 步：选择第一个 workflow

选择完成文件系统或 Starter 数据库 workflow。

### 选项 A：写入并读取文件

创建文件系统并将其设为默认文件系统：

```bash
tdc fs create-file-system \
  --file-system-name quickstart-fs \
  --set-default \
  --wait \
  --output text
```

tdc 会在本地保存文件系统凭证。接下来可以直接写入并读取文件：

```bash
printf 'hello from tdc\n' | tdc fs copy-file \
  --from-stdin \
  --to-remote /hello.txt

tdc fs read-file --path /hello.txt
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
```

### 选项 B：查询 Starter 数据库

创建 Starter 集群并保存其 ID：

```bash
export TDC_DB_CLUSTER_ID="$(tdc db create-db-cluster \
  --db-cluster-name quickstart-db \
  --db-cluster-type starter \
  --wait \
  --query id \
  --output text)"
```

创建 SQL 用户并运行只读验证查询：

```bash
tdc db create-db-sql-users \
  --db-cluster-id "$TDC_DB_CLUSTER_ID"

tdc db execute-sql-statement \
  --db-cluster-id "$TDC_DB_CLUSTER_ID" \
  --read-only \
  --sql "SELECT 1 AS ready" \
  --output text
```

该命令通过 HTTPS SQL API 执行一条 statement，并返回包含 `ready = 1` 的结果。

清理资源：

```bash
tdc db delete-db-cluster \
  --db-cluster-id "$TDC_DB_CLUSTER_ID" \
  --wait
unset TDC_DB_CLUSTER_ID
```

## 后续步骤

- [管理 TiDB Cloud Starter 数据库](/ai/tdc/guides/tdc-starter-database.md)
- [管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
