---
title: tdc 配置与凭证
summary: 参考 tdc profile、环境变量和参数优先级、本地状态路径、文件系统 registry、SQL 凭证、挂载定位信息和操作日志。
---

# tdc 配置与凭证

tdc 将所有产品管理的本地状态保存在 `~/.tdc/`，并分离非敏感配置与凭证。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 主文件

```toml
# ~/.tdc/config
[default]
region_code = "aws-us-east-1"
project_id = "..."
fs_default_file_system_name = "workspace"

[logging]
enabled = true
max_file_mb = 10
max_files = 5
```

```toml
# ~/.tdc/credentials
[default]
tdc_public_key = "..."
tdc_private_key = "..."
```

平台支持 POSIX mode 时，凭证文件仅允许所有者访问。

## Profile 选择

Profile 命名空间的选择顺序如下：

1. 显式 `--profile`；
2. `TDC_PROFILE`；
3. `default`。

显式空 profile 无效。环境凭证不会创建 `[env]` profile，也不会修改所选命名空间。

## TiDB Cloud API 凭证

凭证选择顺序如下：

1. 设置了任意一项时，使用 `TDC_PUBLIC_KEY` 和 `TDC_PRIVATE_KEY`；
2. 使用 `~/.tdc/credentials` 中所选 profile section。

两个环境值必须同时存在。tdc 不会混用一半环境变量和一半文件值。

部署区域的选择顺序如下：

1. 显式全局 `--region`；
2. `TDC_REGION_CODE`；
3. profile `region_code`。

命令参数、环境输入、已保存配置和命令默认值会按字段分别解析。因此，除 API key pair 这类必须成对提供的字段外，不同字段可以来自不同层级。

## 默认 Starter project

创建 Starter 集群时，project 的选择顺序如下：

1. 显式非空 `--project-id`；
2. `tdc configure` 发现的 profile `project_id`；
3. 否则在发送创建请求前失败。

其他 DB 命令通过集群或分支 ID 定位资源，不使用 `project_id`。文件系统命令不使用 DB 默认 project。

## 文件系统资源 registry

一个 profile 可以注册多个文件系统。主配置仅保存可选的默认名称，各资源状态彼此隔离：

```text
~/.tdc/fs_resources/<profile-key>/<resource-key>/config
~/.tdc/fs_resources/<profile-key>/<resource-key>/credentials
```

资源配置包含文件系统名称、tenant ID、云服务提供商、region code 和创建时间。凭证文件只包含 owner `api_key`，且只允许所有者访问。

资源选择顺序如下：

1. 显式 `--file-system-name`；
2. `TDC_FS_FILE_SYSTEM_NAME`；
3. profile `fs_default_file_system_name`；
4. 唯一已注册资源；
5. 否则以资源缺失或选择不明确的错误失败。

远端 `fs`、`fs-git`、`fs-journal` 和 owner `fs-vault` 操作的 FS owner 凭证选择顺序如下：

1. 显式 `--fs-token`；
2. `TDC_FS_TOKEN`；
3. 所选资源的凭证。

优先使用 `TDC_FS_TOKEN`，因为命令行参数可能保留在 shell history 或进程列表中。

## 无配置访问文件系统

全新的沙箱可以使用：

```bash
export TDC_FS_TOKEN="<owner-token>"
export TDC_REGION_CODE="aws-us-east-1"
export TDC_FS_FILE_SYSTEM_NAME="workspace"
```

这些值只构成内存中的命名空间，tdc 不会写入 `~/.tdc/`。创建和删除文件系统仍需要 TiDB Cloud API 凭证；删除还需要本地资源注册信息。

## DB SQL 凭证

生成的 SQL 凭证以集群为作用域：

```text
~/.tdc/db_users/<cluster-id>/credentials
```

```toml
[read_only]
username = "..."
password = "..."

[read_write]
username = "..."
password = "..."

[admin]
username = "..."
password = "..."
```

`tdc db create-db-sql-users` 创建或修复这些稳定用户。它们不存储在主凭证文件中。

## Companion 状态与挂载定位信息

每个已注册文件系统都有隔离的 companion home：

```text
~/.tdc/drive9-home/<profile-key>/<resource-key>/
```

不要为 tdc 工作流编辑该状态或独立的 `~/.drive9` 配置。

后台 FS 或 Vault 挂载成功后会写入非敏感的定位文件：

```text
~/.tdc/mounts/<mount-hash>.locator.json
```

定位文件包含足以确定部署区域和 companion home 的信息，使同一个 `HOME` 中的 drain 和 unmount 无需再次提供 token。定位文件不包含 FS token，并会在 unmount 成功后删除。

## 操作日志

tdc 将已脱敏的本地 JSON Lines 事件写入：

```text
~/.tdc/logs/tdc.jsonl
```

这是本地审计和调试数据，不是 telemetry。它可以包含命令名、参数名、profile、region、耗时、退出状态、稳定错误码、HTTP method/status、操作与 request ID；不包含参数值、SQL、文件路径或内容、payload、连接字符串或凭证。

为单个进程关闭：

```bash
TDC_LOGGING=off tdc db list-db-clusters
```

或者配置：

```toml
[logging]
enabled = false
```

环境值 `off`、`false`、`0`、`no` 用于关闭，`on`、`true`、`1`、`yes` 用于开启。环境变量优先于配置文件。

## 敏感值

以下值均应视为密钥：

- TiDB Cloud API private key 和 public-key pair；
- FS owner token；
- DB SQL 用户名、密码和连接字符串；
- 委派的 Vault token 和 secret 值。

不要将其写入版本控制、工单、日志、命令示例或不受保护的 shell history。

## 相关文档

- [tdc 区域、安全与限制](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
- [tdc 故障排查](/ai/tdc/reference/tdc-troubleshooting.md)
