---
title: 安装、配置和更新 tdc
summary: 安装 tdc release 二进制、以交互或自动化方式配置 profile、安全更新并卸载 CLI。
---

# 安装、配置和更新 tdc

本文介绍受支持的 release installer、profile 配置、帮助与版本行为、更新和卸载。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 安装 tdc

### macOS 和 Linux

```bash
curl -fsSL https://github.com/tidbcloud/tdc/releases/latest/download/install.sh | sh -s -- --yes
export PATH="$HOME/.tdc/bin:$PATH"
tdc --version
```

Installer 会将 `tdc` 和 `tdc-drive9` companion 放入 `~/.tdc/bin`。请将 PATH 设置加入 shell profile。安装过程不需要 `sudo`，也不会写入凭证。

### Windows

```powershell
$script = "$env:TEMP\install-tdc.ps1"
iwr https://github.com/tidbcloud/tdc/releases/latest/download/install.ps1 -OutFile $script
powershell -ExecutionPolicy Bypass -File $script -Yes
$env:Path = "$HOME\.tdc\bin;$env:Path"
tdc --version
```

将 `$HOME\.tdc\bin` 加入用户 `PATH`，使新 PowerShell session 也能找到 tdc。

## 配置 profile

交互式配置是唯一会提示输入的 tdc workflow：

```bash
tdc configure
```

tdc 会请求 TiDB Cloud API public key、private key 和 canonical region code。它通过列出 project 验证 key，并将唯一的 `tidbx_virtual` project 记录为 profile 的默认 project。

配置命名 profile：

```bash
tdc configure --profile staging
```

在 CI 或其他非交互环境中，优先使用环境变量：

```bash
TDC_PUBLIC_KEY="<public-key>" \
TDC_PRIVATE_KEY="<private-key>" \
TDC_REGION_CODE="aws-us-east-1" \
tdc configure --profile ci --non-interactive
```

也可以使用 `--tdc-public-key`、`--tdc-private-key` 和 `--region-code`，但 secret flag 可能保留在 shell history 或进程列表中。

配置优先级为命令参数、环境变量、已保存 profile。全局 `--region` 只覆盖当前命令的 region：

```bash
tdc db list-db-clusters --profile staging --region aws-us-west-2
```

## 获取帮助与版本信息

所有命令层级都支持 `help`、`--help` 和 `--version`：

```bash
tdc help
tdc fs help
tdc db create-db-cluster help
tdc --version
tdc fs --version
```

生成的 usage 会先显示必需参数，再显示带方括号的可选参数。tdc 仅支持长参数。

## 更新 tdc

只检查而不修改文件：

```bash
tdc update --check
```

在自动化中，有更新时返回失败：

```bash
tdc update --check --fail-if-update-available
```

预览并执行更新：

```bash
tdc update --dry-run
tdc update
```

安装指定 tdc release：

```bash
tdc update --target-version v0.1.2
```

更新命令会替换用户安装目录中的两个二进制。活跃的文件系统挂载会继续运行已经加载的 companion 进程。为避免旧挂载运行时与新 CLI 命令混用，请在更新前停止写入、drain FUSE 挂载并 unmount：

```bash
tdc fs drain-file-system --mount-path /path/to/workspace
tdc fs unmount-file-system --mount-path /path/to/workspace
tdc update
```

WebDAV 应关闭写入进程并 unmount；drain 仅支持 FUSE。tdc 不会修改受保护位置或 package manager 管理的安装。较早安装在 `/usr/local/bin` 的版本需要重新运行 installer，一次性迁移到 `~/.tdc/bin`。

## 卸载 tdc

仅删除二进制：

```bash
rm -f "$HOME/.tdc/bin/tdc" "$HOME/.tdc/bin/tdc-drive9"
```

在 Windows 上：

```powershell
Remove-Item "$HOME\.tdc\bin\tdc.exe", "$HOME\.tdc\bin\tdc-drive9.exe"
```

删除二进制会保留 profile、凭证、文件系统注册、DB SQL 凭证、日志和挂载定位文件。只有在确定要删除全部本地 tdc 状态时，才删除 `~/.tdc/`：

```bash
rm -rf "$HOME/.tdc"
```

删除本地状态不会删除远端 Starter 集群或文件系统资源。

## 后续步骤

- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [管理 TiDB Cloud Starter 数据库](/ai/tdc/guides/tdc-starter-database.md)
- [管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
