---
title: tdc 故障排查
summary: 排查 tdc 认证、project、文件系统选择、companion、配额、SQL 用户、挂载和中断清理问题。
---

# tdc 故障排查

使用本文排查当前常见的 tdc 故障。只在需要时添加 `--debug`；调试输出已经脱敏，但共享前仍需检查。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## API 认证失败

常见症状包括凭证缺失、Digest 认证失败或权限不足。

检查两个环境值是否同时设置：

```bash
test -n "$TDC_PUBLIC_KEY"
test -n "$TDC_PRIVATE_KEY"
```

如果要使用已保存的凭证，请清除这两个变量并验证 profile：

```bash
unset TDC_PUBLIC_KEY TDC_PRIVATE_KEY
tdc organization list-projects --profile default
```

API key 即使认证成功，也可能缺少命令所需的权限。请使用对相应 organization 或 project 具备访问权限的 key。

## Configure 找不到 virtual project

`tdc configure` 要求恰好一个可访问 project 的 `type` 为 `tidbx_virtual`。

```bash
tdc organization list-projects \
  --query 'projects[].{id:id,name:name,type:type}'
```

如果没有 virtual project，请检查 API key 对 organization 和 project 的访问权限。如果出现多个，请通过 [tdc issue tracker](https://github.com/tidbcloud/tdc/issues)报告无法确定默认项目的问题。

## 文件系统 token 缺失

干净 sandbox 需要提供三个值：

```bash
export TDC_FS_TOKEN="<owner-token>"
export TDC_REGION_CODE="aws-us-east-1"
export TDC_FS_FILE_SYSTEM_NAME="workspace"
tdc fs check-file-system
```

FS token 不是 TiDB Cloud API private key。

## 文件系统选择存在歧义

列出已注册资源并显式选择：

```bash
tdc fs list-file-systems --output text
tdc fs list-files --file-system-name workspace --path /
```

或者设置默认值：

```bash
tdc fs set-default-file-system --file-system-name workspace
```

tdc 不会在多个资源中猜测。

## 文件系统 region 不受支持

已配置的 TiDB Cloud region 可能没有 `tidb_cloud_native` 文件系统 endpoint。请与[当前文件系统 region](/ai/tdc/reference/tdc-regions-security-and-limitations.md#文件系统-region)比较。使用有效的 profile 或命令级 `--region` 修改部署区域，不要配置原始 server URL。

## Companion 缺失或不兼容

Release installer 会将 `tdc-drive9` 放在 `tdc` 旁。tdc 报告 companion 缺失时，请重新运行当前 installer：

```bash
curl -fsSL https://github.com/tidbcloud/tdc/releases/latest/download/install.sh | sh -s -- --yes
```

验证 `PATH` 解析到预期 tdc：

```bash
command -v tdc
tdc --version
```

不要复制任意 standalone Drive9 二进制。

## Starter 或文件系统创建达到 quota

Quota 和 capacity error 可能表示 organization 达到 free Starter limit。创建前列出已有资源：

```bash
tdc db list-db-clusters --output text
tdc fs list-file-systems --output text
```

不要为了让自动化通过而删除无关资源。Starter spending limit 可能要求配置 billing。

## SQL 凭证缺失

为准确 cluster 准备或修复用户：

```bash
tdc db create-db-sql-users --db-cluster-id "<cluster-id>"
```

然后以显式角色重试：

```bash
tdc db execute-sql-statement \
  --db-cluster-id "<cluster-id>" \
  --read-only \
  --sql "SELECT 1"
```

删除 `~/.tdc/db_users/<cluster-id>/credentials` 会删除本地密码。请运行创建或修复命令，不要自行构造凭证。

## Mount 未能 ready

查看 timeout error 输出的 log path，并确认：

- Mount path 存在且可写；
- 没有其他挂载覆盖该路径；
- FS token 和 region 有效；
- 已安装 FUSE prerequisite 或 WebDAV helper；
- 远端 region 可达。

macOS 默认使用 WebDAV。安装 macFUSE 后请求 FUSE：

```bash
tdc fs mount-file-system \
  --mount-path /path/to/workspace \
  --driver fuse
```

Linux 需要 FUSE3，并且当前用户需要访问 `/dev/fuse`。Windows WebDAV 需要 WebClient 服务和 `X:` 之类的盘符。

## 进程崩溃后 mount stale

如果 companion 未正常卸载就被终止，FUSE 访问可能返回 `EIO` 或 `Transport endpoint is not connected`。请先停止仍在打开文件的进程，然后尝试：

```bash
tdc fs unmount-file-system \
  --mount-path /path/to/workspace \
  --force
```

没有 locator 时，如果清理应成功，使用 `--ignore-absent`。突然清理无法保证恢复已删除本地磁盘上的 pending write。

## Unmount 报告 busy

关闭编辑器、工作目录位于挂载点内的 shell，以及其他持有已打开文件的进程。对于 FUSE，请在 drain 后重试：

```bash
tdc fs drain-file-system --mount-path /path/to/workspace --timeout 30s
tdc fs unmount-file-system --mount-path /path/to/workspace
```

不要对 WebDAV 使用 drain。

## 中断命令留下资源

列出资源，并且只处理本次工作流创建的对象。删除前先查看详情：

```bash
tdc db describe-db-cluster --db-cluster-id "<cluster-id>"
tdc fs describe-file-system --file-system-name "<filesystem-name>"
```

预览受支持的清理：

```bash
tdc db delete-db-cluster --db-cluster-id "<cluster-id>" --dry-run
tdc fs delete-file-system \
  --file-system-name "<filesystem-name>" \
  --confirm-file-system-name "<filesystem-name>" \
  --dry-run
```

## 报告问题

请提供 tdc 版本、操作系统与架构、命令名称、稳定错误码和已脱敏日志。不要提供 API key、FS/Vault token、DB 密码、包含私有数据的 SQL 或文件内容。请在 [github.com/tidbcloud/tdc/issues](https://github.com/tidbcloud/tdc/issues) 报告问题。
