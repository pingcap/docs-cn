---
title: TiDB Cloud CLI 快速上手指南
summary: 安装并配置 TiDB Cloud CLI，然后创建并使用文件系统，或管理并查询 TiDB Cloud Starter 数据库。
---

# TiDB Cloud CLI 快速上手指南

[TiDB Cloud CLI (`ti`)](https://github.com/tidbcloud/ti-cli) 是一个命令行工具，用于管理 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) 实例和 [TiDB Cloud Filesystem 中的文件系统](/ai/ti/ti-overview.md#tidb-cloud-filesystem)。它同时支持交互式使用和自动化场景，并以 JSON 作为命令的默认输出格式。

本文档将指导你安装并配置 TiDB Cloud CLI (`ti`)，然后完成一个使用 TiDB Cloud Starter 或 TiDB Cloud Filesystem 的基础工作流。有关 CLI 的概览、功能和支持的工作流，请参见[TiDB Cloud 命令行接口概览](/ai/ti/ti-overview.md)。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于 public preview 阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 前提条件 {#prerequisites}

开始之前，请先在 [TiDB Cloud console](https://tidbcloud.com/) 的 [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) 页面获取 TiDB Cloud API 公钥和私钥。这些密钥必须具有你所在组织的 `Organization Owner` 访问权限。

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

    - CLI 操作的默认 Region，使用 region code 指定（例如 `aws-us-west-2`）。有关 TiDB Cloud CLI 支持的 Region 列表，请参见[支持的 Region](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions)。
    - 你的 TiDB Cloud API 公钥和私钥。

3. 运行一个只读命令，验证 CLI 是否可以使用已保存的凭证访问 TiDB Cloud：

    ```bash
    ti fs list-file-systems
    ```

    输出示例：

    ```bash
    {
      "region_code": "aws-us-west-2",
      "file_systems": []
    }
    ```

## 第 3 步：选择工作流 {#step-3-choose-a-workflow}

根据你的需要，继续执行以下任一工作流：

- [选项 A：TiDB Cloud Filesystem](/ai/ti/ti-quick-start.md#option-a-tidb-cloud-filesystem)
- [选项 B：TiDB Cloud Starter](/ai/ti/ti-quick-start.md#option-b-tidb-cloud-starter)

### 选项 A：TiDB Cloud Filesystem {#option-a-tidb-cloud-filesystem}

TiDB Cloud Filesystem 是一种持久化、可共享的云文件系统，可用于本地机器、CI 作业、沙箱以及其他临时环境。

以下示例展示了如何在一个环境中创建文件系统，并从同一环境或另一个环境访问它。例如，你可以从 AI agent 沙箱（一个任务完成后可能会被丢弃的临时环境）访问它。

1. 在你的本地机器或另一个已配置 TiDB Cloud API 凭证的环境中，创建一个文件系统并获取其所有者令牌：

    ```bash
    export TI_FS_TOKEN="$(ti fs create-file-system --display-name agent-workspace --wait --query fs_token --output text --region aws-us-west-2)"
    ```

    > **Tip:**
    >
    > 为了简化操作，本快速上手使用创建文件系统时返回的所有者令牌。若要遵循最小权限原则，你可以生成范围受限令牌，以将访问限制为特定路径和操作。更多信息，请参见 [Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md)。

2. 在你要使用该文件系统的环境中，将上一步的所有者令牌设置为 `TI_FS_TOKEN`，然后按如下方式将文件系统挂载到本地路径。该环境可以是你创建文件系统时使用的同一台机器、另一台机器，或 AI agent 沙箱。

    ```bash
    export TI_FS_TOKEN="<owner-token>" # Skip this line if you are continuing in the same terminal as step 1, where TI_FS_TOKEN is already set.
    mkdir ~/mnt-test
    ti fs mount-file-system --mount-path ~/mnt-test --region aws-us-west-2
    echo 'Hello from TiDB Cloud Filesystem' >> ~/mnt-test/hello.txt
    ls -l ~/mnt-test/hello.txt
    ```

    挂载后，你可以使用标准的本地文件操作来处理这些文件。

3. 在该环境中使用完挂载的文件系统后，将其卸载：

    ```bash
    ti fs unmount-file-system --mount-path ~/mnt-test --region aws-us-west-2
    ```

    卸载会移除本地挂载，但文件仍保留在 TiDB Cloud Filesystem 中，并且可以从同一环境或另一个环境再次访问。

### 选项 B：TiDB Cloud Starter {#option-b-tidb-cloud-starter}

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

3. 生成连接字符串：

    ```bash
    export DATABASE_URL="$(ti db format-db-connection-string \
      --db-cluster-id "$TI_DB_CLUSTER_ID" \
      --read-write --query connection_string \
      --output text)"
    ```

## 后续步骤 {#what-s-next}

- 阅读[TiDB Cloud 命令行接口概览](/ai/ti/ti-overview.md)，了解 `ti` 管理哪些资源以及何时使用它。
- 按照任务指南管理 [TiDB Cloud Starter](https://docs.pingcap.com/tidbcloud/select-cluster-tier/?plan=starter#starter) 或 [TiDB Cloud Filesystem](/tidb-cloud-filesystem/manage-filesystem-resources.md)。
- 查阅 [TiDB Cloud CLI 命令参考](/ai/ti/reference/ti-cli-reference.md)，了解命令组、全局选项和 CLI 的共享行为。
- 了解 [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)，以设置多个配置（Profile）或非交互式身份验证。