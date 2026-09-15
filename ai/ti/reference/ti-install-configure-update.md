---
title: 安装、配置和更新 TiDB Cloud CLI
summary: 安装 TiDB Cloud CLI 发布版本，配置配置（Profile），检查版本，应用更新，以及卸载 CLI。
---

# 安装、配置和更新 TiDB Cloud CLI

使用本指南安装和配置 TiDB Cloud CLI (`ti`)，检查并应用更新，并在需要时卸载 CLI。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 前提条件 {#prerequisites}

要配置 TiDB Cloud CLI，请先在 TiDB Cloud 控制台的 [TiDB Cloud API Keys](https://tidbcloud.com/org-settings/api-keys) 页面获取 TiDB Cloud API 公钥和私钥。

> **Note:**
>
> 如果你之前使用过 TiDB Cloud CLI `tdc` v0.1.x，请先卸载由 `tdc` 启动的所有 Filesystem 或 Vault 挂载，并在安装 `ti` 之前阅读[从 tdc 迁移到 TiDB Cloud CLI](/ai/ti/reference/ti-migrate-from-tdc.md)。

## 安装 TiDB Cloud CLI {#install-tidb-cloud-cli}

请根据你的操作系统，按照以下步骤安装 TiDB Cloud CLI。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. 在 macOS 或 Linux 上，运行以下命令安装 TiDB Cloud CLI：

    ```bash
    curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
    ```

2. 将 `ti` 添加到当前 shell 中并验证：

    ```bash
    export PATH="$HOME/.ti/bin:$PATH"
    ti --version
    ```

3. 为了让 `ti` 在新的终端会话中仍然可用，请将其添加到你的 shell 配置中。例如，如果你使用 `zsh`，请运行以下命令：

    ```bash
    echo 'export PATH="$HOME/.ti/bin:$PATH"' >> ~/.zshrc
    source ~/.zshrc
    ```

    如果你使用 Bash，请将相同的 `export` 命令添加到终端使用的启动文件中，Linux 上通常是 `~/.bashrc`，macOS 上通常是 `~/.bash_profile`。

</div>

<div label="Windows PowerShell" value="windows-powershell">

1. 在 Windows PowerShell 中，运行以下命令安装 TiDB Cloud CLI：

    ```powershell
    $script = "$env:TEMP\install-ti.ps1"
    iwr https://github.com/tidbcloud/ti-cli/releases/latest/download/install.ps1 -OutFile $script
    powershell -ExecutionPolicy Bypass -File $script -Yes
    ```

2. 将 `ti` 添加到当前 PowerShell 会话中并验证：

    ```powershell
    $env:Path = "$HOME\.ti\bin;$env:Path"
    ti --version
    ```

3. 将 `$HOME\.ti\bin` 添加到你的用户 `PATH` 中，以便 `ti` 在新的 PowerShell 会话中仍然可用：

    ```powershell
    $tiBin = "$HOME\.ti\bin"
    [Environment]::SetEnvironmentVariable("Path", "$tiBin;$([Environment]::GetEnvironmentVariable('Path', 'User'))", "User")
    ```

</div>
</SimpleTab>

安装程序会写入你的主目录，不需要提升权限。

安装程序还会显示一条关于匿名使用遥测以及如何选择退出的提示。安装过程不要求你必须对遥测做出选择。详情请参见[匿名遥测](/ai/ti/reference/ti-configuration-and-credentials.md#anonymous-telemetry)。

## 配置一个配置（Profile） {#configure-a-profile}

配置（Profile）是由 TiDB Cloud API 公钥、私钥和 Region 代码组成的一组命名配置。

本节介绍如何为 TiDB Cloud CLI 配置一个配置（Profile）。

### 交互式配置 {#configure-interactively}

默认情况下，`ti configure` 会提示你输入配置一个配置（Profile）所需的信息：

```bash
ti configure
```

`ti configure` 会提示你输入 TiDB Cloud API 公钥、私钥以及默认 Region 代码。除非你为单个命令覆盖该设置，否则 CLI 会对命令使用此 Region。可用 Region 请参见[支持的 Region](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions)。

该命令会在本地验证输入格式，并在不向 TiDB Cloud 发起请求的情况下保存配置（Profile）。当你运行访问 TiDB Cloud 的命令时，系统才会验证你的凭证。要更改默认配置（Profile），请再次运行 `ti configure`。要更改命名配置（Profile），请包含其名称，例如 `ti configure --profile staging`。

### 配置命名配置（Profile） {#configure-a-named-profile}

传递 `--profile` 以配置命名配置（Profile）：

```bash
ti configure --profile staging
```

### 为自动化进行配置 {#configure-for-automation}

对于 CI 或其他非交互式环境，建议优先使用环境变量：

```bash
TIDB_CLOUD_PUBLIC_KEY="<public-key>" \
TIDB_CLOUD_PRIVATE_KEY="<private-key>" \
TI_REGION_CODE="aws-us-east-1" \
ti configure --profile ci --non-interactive
```

你也可以提供 `--tidb-cloud-public-key`、`--tidb-cloud-private-key` 和 `--region-code`，但这些包含 Secret 的命令行参数可能会保留在 shell 历史记录或进程列表中。

## 选择配置（Profile）并覆盖其 Region {#select-a-profile-and-override-its-region}

要使用命名配置（Profile）并为单个命令覆盖其默认 Region，请使用全局 `--profile` 和 `--region` 选项：

```bash
ti --profile staging --region aws-us-west-2 db list-db-clusters --db-cluster-type starter
```

有关配置（Profile）、凭证和 Region 优先级规则的详细信息，请参见[TiDB Cloud CLI 配置和凭证](/ai/ti/reference/ti-configuration-and-credentials.md)。

## 获取帮助并检查版本 {#get-help-and-check-the-version}

使用 `help` 或 `--help` 查看命令，使用 `--version` 检查已安装的版本：

```bash
ti help
ti fs help
ti --version
```

有关命令组和 CLI 约定，请参见[TiDB Cloud CLI 命令参考](/ai/ti/reference/ti-cli-reference.md)。

## 更新 TiDB Cloud CLI {#update-tidb-cloud-cli}

在不更改文件的情况下进行检查：

```bash
ti update --check
```

在自动化场景中，如果有较新版本可用，则返回退出码 `1`：

```bash
ti update --check --fail-if-update-available
```

预览更新：

```bash
ti update --dry-run
```

> **Note:**
>
> 如果你有活动中的 Filesystem 或 Vault 挂载，请在更新前停止写入端并卸载挂载，以便 `ti` 和 Filesystem 运行时一起更新。例如：
>
> ```bash
> ti fs unmount-file-system --mount-path <mount-path>
> ```
>
> 对于 Vault 挂载，请使用 `ti fs-vault unmount-vault --mount-path <mount-path>`。详情请参见[挂载 TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)和[管理 Filesystem Vault Secrets](/ai/ti/guides/manage-filesystem-vault-secrets.md)。

应用最新更新：

```bash
ti update
```

安装特定发布版本：

```bash
ti update --target-version <version>
```

`update` 命令会替换用户拥有安装中的 `ti` 和 `ti-drive9`。它不会修改位于受保护位置或由包管理器管理的位置中的安装。要将旧的 `/usr/local/bin` 安装迁移到 `~/.ti/bin`，请运行一次安装程序。

## 从 tdc v0.1.x 迁移 {#migrate-from-tdc-v01-x}

如果你从未使用过 `tdc` v0.1.x，请跳过本节。

如果你之前使用过 `tdc` v0.1.x，`ti` 可以将 `~/.tdc/` 中受支持的本地配置（Profile）、凭证、偏好设置和 Filesystem 状态迁移到 `~/.ti/`。在安装 `ti` 之前，请先卸载由 `tdc` 启动的所有 Filesystem 或 Vault 挂载。

有关完整迁移流程（包括会迁移和不会迁移的状态、目录冲突解决方式以及旧版环境变量兼容性），请参见[从 tdc 迁移到 TiDB Cloud CLI](/ai/ti/reference/ti-migrate-from-tdc.md)。

## 卸载 TiDB Cloud CLI {#uninstall-tidb-cloud-cli}

在卸载之前，请先停止写入器，并卸载所有处于活动状态的 Filesystem 或 Vault 挂载。

例如，运行与挂载类型对应的命令：

```bash
# Filesystem mount
ti fs unmount-file-system --mount-path <filesystem-mount-path>

# Vault mount
ti fs-vault unmount-vault --mount-path <vault-mount-path>
```

详情请参阅[挂载 TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)和[管理 Filesystem Vault Secrets](/ai/ti/guides/manage-filesystem-vault-secrets.md)。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

1. 删除二进制文件：

    ```bash
    rm -f "$HOME/.ti/bin/ti" "$HOME/.ti/bin/ti-drive9"
    ```

2. 从安装期间添加到 shell 配置文件中的条目里，移除 `~/.ti/bin`。

</div>

<div label="Windows PowerShell" value="windows-powershell">

1. 删除二进制文件：

    ```powershell
    Remove-Item "$HOME\.ti\bin\ti.exe", "$HOME\.ti\bin\ti-drive9.exe"
    ```

2. 从用户 `PATH` 中移除 `$HOME\.ti\bin`：

    ```powershell
    $tiBin = "$HOME\.ti\bin"
    $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
    $newPath = (($userPath -split ";") | Where-Object { $_ -and $_ -ne $tiBin }) -join ";"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    ```

</div>
</SimpleTab>

### 删除本地状态 {#remove-local-state}

删除二进制文件后，会保留配置（Profile）、凭证、Filesystem 注册信息、DB SQL 凭证、日志以及挂载定位文件。

> **注意：**
>
> 仅当你打算永久删除所有本地 TiDB Cloud CLI 状态时，才删除 `~/.ti/`。删除本地状态不会删除远程 TiDB Cloud Starter 实例或 Filesystem 资源。

<SimpleTab groupId="operating-systems">

<div label="macOS or Linux" value="macos-or-linux">

在 macOS 或 Linux 上：

```bash
rm -rf "$HOME/.ti"
```

</div>

<div label="Windows PowerShell" value="windows-powershell">

在 Windows PowerShell 上：

```powershell
Remove-Item "$HOME\.ti" -Recurse -Force
```

</div>
</SimpleTab>

## 另请参阅 {#see-also}

- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)
- [TiDB Cloud Starter CLI 命令参考](/ai/ti/reference/ti-starter-database.md)
- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)