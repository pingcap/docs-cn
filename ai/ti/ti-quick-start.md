---
title: TiDB Cloud CLI 快速上手指南
summary: 安装并配置 TiDB Cloud CLI，然后创建并使用 TiDB Cloud Filesystem，或查询 TiDB Cloud Starter 数据库。
---

# TiDB Cloud CLI 快速上手指南

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) 是一个命令行工具，用于管理 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) 实例和 [TiDB Cloud Filesystem](/ai/ti/ti-overview.md#tidb-cloud-filesystem)。它同时支持交互式使用和自动化场景，并以 JSON 作为命令的默认输出格式。

本文档将指导你安装并配置 TiDB Cloud CLI (`ti`)，然后完成一个使用 TiDB Cloud Starter 或 TiDB Cloud Filesystem 的基础工作流。有关 CLI 的概览、功能和支持的工作流，请参见[TiDB Cloud 命令行接口概览](/ai/ti/ti-overview.md)。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于 public preview 阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 前提条件 {#prerequisites}

开始之前，请先在 [TiDB Cloud console](https://tidbcloud.com/) 的 [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) 页面获取 TiDB Cloud API 公钥和私钥。

## 第 1 步：安装 TiDB Cloud CLI {#step-1-install-tidb-cloud-cli}

根据你的操作系统，按照以下步骤安装 TiDB Cloud CLI。

<SimpleTab>

<div label="macOS 或 Linux">

1. 在 macOS 或 Linux 上，运行以下命令安装 TiDB Cloud CLI：

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. 将 `ti` 添加到当前 shell，并验证安装结果：

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"
    ti --version
    ```

3. 将 `export PATH="$HOME/.ti/bin:$PATH"` 添加到你的 shell profile 中，以便在新终端中也能使用 `ti`。

    例如，如果你使用 `zsh`，请运行以下命令：

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

</div>

<div label="Windows PowerShell">

1. 在 Windows PowerShell 中，运行以下命令安装 TiDB Cloud CLI：

    ```powershell
    $script = "$env:TEMP\install-ti.ps1"
    iwr https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
    powershell -ExecutionPolicy Bypass -File $script -Yes
    ```

2. 将 `ti` 添加到当前 PowerShell 会话，并验证安装结果：

    ```powershell
    $env:Path = "$HOME\.ti\bin;$env:Path"
    ti --version
    ```

3. 将 `$HOME\.ti\bin` 添加到你的用户 `PATH` 中，以便在新的 PowerShell 会话中也能使用 `ti`：

    ```powershell
    $tiBin = "$HOME\.ti\bin"
    [Environment]::SetEnvironmentVariable("Path", "$tiBin;$([Environment]::GetEnvironmentVariable('Path', 'User'))", "User")
    ```

</div>
</SimpleTab>

## 第 2 步：配置 TiDB Cloud CLI {#step-2-configure-tidb-cloud-cli}

1. 运行交互式配置：

    ```bash
    ti configure
    ```

2. 提供以下信息：

    - CLI 操作的默认 Region，使用 region code 指定（例如 `aws-us-east-1`）。有关 TiDB Cloud CLI 支持的 Region 列表，请参见[支持的 Region](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions)。
    - 你的 TiDB Cloud API 公钥和私钥。

3. 运行一个只读命令，验证 CLI 是否可以使用已保存的凭证访问 TiDB Cloud：

    ```bash
    ti db list-db-clusters --db-cluster-type starter --output text
    ```

    输出示例：

    ```bash
    {
      "profile": "default",
      "region_code": "aws-us-east-1",
      "credentials_stored": true
    }
    ```

## 第 3 步：选择工作流 {#step-3-choose-a-workflow}

完成以下任一工作流。

- [选项 A：创建并使用 Filesystem](/ai/ti/ti-quick-start.md#option-a-create-and-use-a-filesystem)
- [选项 B：创建 TiDB Cloud Starter 实例并查询数据库](/ai/ti/ti-quick-start.md#option-b-create-a-tidb-cloud-starter-instance-and-query-the-database)

### 选项 A：创建并使用 Filesystem {#option-a-create-and-use-a-filesystem}

TiDB Cloud Filesystem 是一种持久化、可共享的云文件系统，可用于本地机器、CI 作业、沙箱以及其他临时环境。

1. 创建一个 Filesystem，等待其就绪，并保存服务器分配的 ID：

    ```bash
    export TI_FS_FILE_SYSTEM_ID="$(ti fs create-file-system \
      --wait \
      --query file_system_id \
      --output text)"
    ```

    `ti` 会在本地存储 Filesystem 凭证，因此后续文件操作无需再次提供该凭证。

2. 向 Filesystem 写入一个文件，然后读取该文件：

    ```bash
    printf 'hello from ti\n' | ti fs copy-file \
      --from-stdin \
      --to-remote /hello.txt

    ti fs read-file \
      --path /hello.txt
    ```

    预期输出：

    ```text
    hello from ti
    ```

3. 删除 Filesystem：

    ```bash
    ti fs delete-file-system \
      --file-system-id "$TI_FS_FILE_SYSTEM_ID"
    unset TI_FS_FILE_SYSTEM_ID
    ```

### 选项 B：创建 TiDB Cloud Starter 实例并查询数据库 {#option-b-create-a-tidb-cloud-starter-instance-and-query-the-database}

1. 创建一个 TiDB Cloud Starter 实例并保存其 ID：

    ```bash
    export TI_DB_CLUSTER_ID="$(ti db create-db-cluster \
      --db-cluster-type starter \
      --db-cluster-name quickstart-db \
      --wait \
      --query id \
      --output text)"
    ```

2. 创建 SQL 用户，并运行一个只读查询以验证连接：

    ```bash
    ti db create-db-sql-users \
      --db-cluster-id "$TI_DB_CLUSTER_ID"

    ti db execute-sql-statement \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --read-only \
      --sql "SELECT 1 AS ready" \
      --output text
    ```

    `ti db execute-sql-statement` 命令通过 HTTPS SQL API 执行该查询。输出中包含 `ready = 1`。

3. 删除 TiDB Cloud Starter 实例：

    ```bash
    ti db delete-db-cluster \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --wait
    unset TI_DB_CLUSTER_ID
    ```

## 后续步骤 {#what-s-next}

- 阅读[TiDB Cloud 命令行接口概览](/ai/ti/ti-overview.md)，了解 `ti` 管理哪些资源以及何时使用它。
- 按照任务指南管理 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) 或 [Filesystem 资源](/ai/ti/guides/manage-filesystem-resources.md)。
- 查阅 [TiDB Cloud CLI 命令参考](/ai/ti/reference/ti-cli-reference.md)，了解命令组、全局选项和 CLI 的共享行为。
- 了解 [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)，以设置多个配置（Profile）或非交互式身份验证。