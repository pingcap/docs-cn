---
title: 排查 TiDB Cloud CLI
summary: 诊断 TiDB Cloud CLI 中与身份验证、项目、Filesystem 选择、配套运行时、配额、SQL 用户、挂载以及清理中断相关的常见故障。
---

# 排查 TiDB Cloud CLI

使用本文档排查当前 TiDB Cloud CLI 的常见故障。仅在需要时添加 `--debug`；调试输出虽然会做脱敏处理，但在分享前仍应先自行检查。

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

## Filesystem 访问令牌缺失 {#filesystem-token-is-missing}

对于一个干净的沙箱环境，请提供令牌和 Region。`ti` 会从令牌中推导文件系统 ID：

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="<filesystem-region-code>"
ti fs check-file-system
```

FS token 不是 TiDB Cloud API 私钥。提供令牌时，`TI_FS_FILE_SYSTEM_ID` 是可选的；只有当你希望 `ti` 验证单独分发的 ID 是否与该令牌匹配时，才需要设置它。

如果令牌已知但未存储在当前机器上，请先导入它，然后选择推导出的 ID：

```bash
# Store a known token without requiring TiDB Cloud API keys.
chmod 600 ./fs-token
ti fs import-file-system-token --from-file ./fs-token --region <filesystem-region-code>
ti fs list-files --file-system-id <file-system-id> --path /
```

如果所有已知令牌都已丢失或被（权限）回收，请使用 TiDB Cloud API key 生成另一个所有者令牌：

```bash
ti fs generate-file-system-token \
  --file-system-id "<file-system-id>" \
  --token-name recovery \
  --ttl 24h
```

新的明文令牌只会在响应中显示一次。请安全保存，或者添加 `--store-locally` 以便在当前机器上选中它。

## Filesystem 访问令牌被拒绝 {#filesystem-token-is-rejected}

数据平面的 HTTP 401 无法区分令牌是被禁用、已过期、在另一台机器上被刷新，还是已被（权限）回收。请使用 TiDB Cloud API key 检查远端元信息：

```bash
ti fs list-file-system-tokens \
  --file-system-id "<file-system-id>" \
  --include-expired \
  --output text
```

令牌名称不是唯一的。对于启用、禁用或删除操作，请使用此输出中的不可变 `token_id`。对于较早创建或导入、且不带令牌生命周期元信息的旧凭据，它们可能仍然有效，但 `ti` 无法安全识别其对应的列表行，因此绝不会猜测匹配项。

执行 enable、disable、delete 或 refresh 后，请等待大约 10 秒，让身份验证缓存完成收敛。如果 refresh 报告 `fs.token_refresh_ambiguous`，即使响应丢失，服务器也可能已经轮转了令牌。此时结果未知：如果 refresh 未提交，旧令牌可能仍然可用；如果已提交，旧令牌则可能已经失效。由于响应丢失，已提交 refresh 所生成的替换令牌无法恢复。不要使用旧令牌重试 refresh。应改为使用 TiDB Cloud 凭据生成一个独立的所有者令牌。

如果令牌变异操作报告 `fs.token_mount_active`，请使用错误信息中给出的精确挂载路径：

```bash
ti fs drain-file-system --mount-path /path/to/workspace
ti fs unmount-file-system --mount-path /path/to/workspace
```

然后重试该令牌操作。另一台机器上的挂载在本地不可见；请单独与那台机器协调轮转操作。

## Filesystem 选择缺失 {#filesystem-selection-is-missing}

使用 TiDB Cloud API key 列出已配置 Region 中的远端资源，并显式选择一个：

```bash
ti fs list-file-systems --output text
ti fs list-files --file-system-id <file-system-id> --path /
```

或者，为当前 shell 中后续命令选择该 Filesystem：

```bash
export TI_FS_FILE_SYSTEM_ID="<file-system-id>"
```

TiDB Cloud CLI 有意不根据本地凭据数量推导 Filesystem，即使只存在一个凭据也是如此。请提供其 ID，或提供一个可从中推导出内嵌 ID 的 FS token。

## Filesystem Region 不受支持 {#filesystem-region-is-unsupported}

已配置的 TiDB Cloud Region 可能不在当前已安装 TiDB Cloud CLI 版本内置的 Filesystem 端点列表中。请将其与[当前支持的 Filesystem Region](/ai/ti/reference/ti-regions-security-and-limitations.md#supported-regions)进行比较。请通过有效的配置（Profile）或命令级 `--region` 更改放置位置；不要配置原始服务器 URL。

## 配套运行时缺失或不兼容 {#companion-is-missing-or-incompatible}

发布安装程序会将 `ti-drive9`（Filesystem 命令的配套运行时）放在 `ti` 的旁边。你不需要直接调用 `ti-drive9`。当 TiDB Cloud CLI 报告缺少配套组件时，请重新运行当前安装程序：

```bash
curl -fsSL https://github.com/tidbcloud/ti-cli/releases/latest/download/install.sh | sh -s -- --yes
```

验证 `PATH` 解析到的是预期的 `ti`：

```bash
command -v ti
ti --version
```

不要随意复制一个独立的 Drive9 二进制文件到该位置。

## Starter 或 Filesystem 创建达到配额上限 {#starter-or-filesystem-creation-reaches-quota}

配额和容量错误可能意味着该组织已达到免费的 Starter 上限。在创建新资源之前，请先列出现有资源：

```bash
ti db list-db-clusters --db-cluster-type starter --output text
ti fs list-file-systems --output text
```

不要为了让自动化流程通过而删除无关资源。Starter 的支出上限可能要求先配置计费。

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

## 挂载未就绪 {#mount-does-not-become-ready}

后台挂载成功时，只会打印 TiDB Cloud CLI 的结果，而不会显示 Drive9 启动消息。如果启动失败或超时，请检查错误中给出的配套运行时日志路径。请确认：

- 挂载路径存在且可写；
- 没有现有挂载覆盖该路径；
- FS token 和 Region 有效；
- 已安装 FUSE 前置依赖或 WebDAV helper；
- 远端 Region 可达。

macOS 默认使用 WebDAV。安装 macFUSE 后，如需请求使用 FUSE，请执行：

```bash
ti fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux 需要 FUSE3 以及对 `/dev/fuse` 的访问权限。Windows 不支持 Filesystem 和 Vault 挂载；请改用 `ti fs` 数据平面命令或非挂载类 Vault 命令。

## Ubuntu 26.04 拒绝在 `/workspace` 下进行 FUSE 挂载 {#ubuntu-2604-rejects-a-fuse-mount-under-workspace}

Ubuntu 26.04 会对 `fusermount3` 应用 AppArmor 配置（Profile）。其默认的挂载路径允许列表不包含 `/workspace`，因此 root 用户和非 root 用户都可能收到以下错误：

```text
/usr/bin/fusermount3: mount failed: Permission denied
```

确认是否为该限制导致：

```bash
sudo journalctl -k --since "10 minutes ago" |
  grep 'profile="fusermount3"'
```

如果日志条目中包含 `operation="mount"`、`name="/workspace/"` 和 `info="failed mntpnt match"`，则说明这是该限制导致的。请改为挂载到 `$HOME` 或 `/mnt` 下：

```bash
mkdir -p "$HOME/workspace"
ti fs mount-file-system --mount-path "$HOME/workspace"
```

修改 `/workspace` 的 owner 或 mode 并不能绕过 AppArmor。如果无法更改路径，请按照[挂载 TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md#ubuntu-2604-mount-paths)中的说明，在 `/etc/apparmor.d/local/fusermount3` 中显式添加 `/workspace` 的挂载和卸载规则。

## 进程崩溃后挂载变为失效状态 {#mount-becomes-stale-after-a-process-crash}

如果 companion 在未优雅卸载的情况下被终止，FUSE 访问可能返回 `EIO` 或 `Transport endpoint is not connected`。请先停止所有打开了文件的进程，然后尝试：

```bash
ti fs unmount-file-system \
  --mount-path /path/to/workspace \
  --force
```

如果希望在没有残留 locator 时清理操作也能成功，请使用 `--ignore-absent`。对于被删除的本地磁盘，突发式清理无法保证恢复尚未完成的待写入数据。

## 卸载时报告 busy {#unmount-reports-busy}

关闭编辑器、工作目录位于该挂载点内的 shell，以及其他仍持有打开文件句柄的进程，然后重试：

```bash
ti fs unmount-file-system --mount-path /path/to/workspace
```

卸载会自动执行优雅的 FUSE 刷写。单独运行 `drain-file-system` 不会关闭文件描述符，也不能解决 busy 挂载；仅当你需要在保持挂载在线的同时刷写待处理工作时，才应使用它。WebDAV 不支持 Drain。

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