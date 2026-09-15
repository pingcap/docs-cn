---
title: TiDB Cloud CLI 配置与凭证
summary: 参考 TiDB Cloud CLI 配置（Profile）、优先级规则、本地状态路径、Filesystem 凭证、SQL 凭证、挂载定位文件和操作日志。
---

# TiDB Cloud CLI 配置与凭证

`ti` 将所有由产品管理的本地状态都存储在 `~/.ti/` 下，并将非敏感配置与凭证分开存放。

> **Note:**
>
> TiDB Cloud CLI (`ti`) 目前处于公测阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 主要文件 {#main-files}

```toml
# ~/.ti/config
[default]
region_code = "aws-us-east-1"
```

```toml
# ~/.ti/credentials
[default]
tidb_cloud_public_key = "..."
tidb_cloud_private_key = "..."
```

在平台支持 POSIX 权限模式时，凭证文件会使用仅所有者可访问的权限。

全局偏好设置与配置（Profile）和凭证分开存储：

```toml
# ~/.ti/.preferences
schema_version = 1

[logging]
enabled = true
max_file_mb = 10
max_files = 5

[telemetry]
enabled = false
```

这个以点开头的偏好设置文件是可选的，在普通目录列表中默认隐藏，并且会应用于每个配置（Profile）。全新安装和执行 `ti configure` 时都不会创建该文件。读取用户自行创建的文件时，不会重写其权限、注释或格式。

## 配置（Profile）选择 {#profile-selection}

配置命名空间按以下顺序选择：

1. 显式指定的 `--profile`；
2. `TI_PROFILE`；
3. `default`。

显式指定空配置是无效的。

## TiDB Cloud API 凭证 {#tidb-cloud-api-credentials}

凭证选择顺序如下：

1. `TIDB_CLOUD_PUBLIC_KEY` 和 `TIDB_CLOUD_PRIVATE_KEY`，当其中任意一个被设置时；
2. `~/.ti/credentials` 中所选 section 的内容。

这两个环境变量必须同时提供。`ti` 绝不会将一个来自环境变量的值与一个来自文件的值混合使用。

部署位置选择顺序如下：

1. 显式指定的全局 `--region`；
2. `TI_REGION_CODE`；
3. 配置中的 `region_code`。

命令行参数、环境变量输入、已保存配置和命令默认值都是按字段分别解析的。因此，当值不构成像 API 密钥对这样的原子组合时，不同字段的值可能来自不同层级。

## Starter 项目放置 {#starter-project-placement}

TiDB Cloud CLI 不接受也不存储项目选择器。创建 TiDB Cloud Starter 实例时不会指定项目放置，而是由 TiDB Cloud 在服务端选择其默认项目。TiDB Cloud 返回的项目字段和标签仍会作为资源元信息可见，但不会在后续请求中复用。

## Filesystem 凭证与远端资源清单 {#filesystem-credentials-and-remote-inventory}

一个配置可以访问多个 Filesystem。按 region 划分作用域的远端资源清单是资源是否存在及其状态的权威来源。本地状态仅存储凭证及其路由提示：

```text
~/.ti/fs_credentials/<profile-key>/<file-system-id-key>/credentials
```

该凭证包含服务端分配的文件系统 ID、规范 region code、所选 `api_key`，以及可选的权威令牌元信息，并使用仅所有者可访问的权限。`ti fs list-file-systems` 会读取远端资源，并仅关联非敏感的 `has_local_token` 提示。

一个远端 Filesystem 可以有多个令牌，但每个配置对每个 Filesystem 最多只存储一个已选令牌。本地存储表示的是操作层面的选择，而不是远端令牌清单的副本。通过预配或较早导入方式创建的凭证可能不包含 `token_id`、`scope_kind`、`token_name`、`expires_at` 或 `scopes`；它们对数据面使用仍然有效，并且 `ti` 不会根据令牌列表中的行去推导缺失的元信息。

`ti fs generate-file-system-token` 不会更改已选凭证，除非设置了 `--store-locally`。`--replace` 只会更改本地选择，不会使之前的远端令牌失效。若刷新来源于本地凭证，则会以原子方式替换该凭证。若刷新来源于命令行参数或 `TI_FS_TOKEN`，则会返回替换后的明文，而不会写入本地状态。

`ti fs generate-file-system-scoped-token` 仅接受所有者令牌，并且可以将其权威路径作用域存储到本地。令牌 JWT 本身包含 Filesystem ID，但不包含令牌类型、令牌 ID 或作用域。因此，显式提供的令牌或环境变量中的令牌会直接传递给服务进行授予权限，而不是在本地进行分类。`TI_FS_TOKEN` 可以包含所有者令牌或范围受限令牌；可执行的操作取决于其服务端能力。

FS 所有者令牌可授予 Filesystem 数据访问，以及令牌清单或生命周期操作的权限。它们不能授予 TiDB Cloud Filesystem 资源的创建、列出、描述或删除权限，也不能生成另一个所有者令牌。这些操作需要 TiDB Cloud API 凭证。`ti fs delete-file-system` 还额外要求显式指定 `--file-system-id`；绝不会使用嵌入在 `TI_FS_TOKEN` 中的 ID 来选择要删除的 Filesystem。

资源选择顺序如下：

1. 显式指定的 `--file-system-id`；
2. `TI_FS_FILE_SYSTEM_ID`；
3. 从显式提供的 FS 令牌中推导 ID；
4. 否则以 `fs.missing_file_system_id` 失败。

`ti` 绝不会根据已保存的默认值或本地凭证数量来推导 Filesystem。对于单次命令，请使用 `--file-system-id`；对于 shell、沙箱或自动化环境，请使用 `TI_FS_FILE_SYSTEM_ID`。

用于远端 `fs`、`fs-git`、`fs-journal` 和所有者 `fs-vault` 操作的 FS 所有者凭证选择顺序如下：

1. 显式指定的 `--fs-token`；
2. `TI_FS_TOKEN`；
3. 所选资源凭证。

相比命令行参数，更推荐使用 `TI_FS_TOKEN`，因为命令行参数可能会保留在 shell 历史记录或进程列表中。

## 无配置 Filesystem 输入 {#config-free-filesystem-inputs}

一个干净的沙箱环境只需要：

```bash
export TI_FS_TOKEN="<owner-token>"
export TI_REGION_CODE="aws-us-east-1"
```

这些值仅构成内存中的命名空间。`ti` 会从令牌中推导 ID，并且不会将这两个值写入 `~/.ti/`。`TI_FS_FILE_SYSTEM_ID` 是可选的；如果提供，则必须与令牌匹配。远端 Filesystem 资源清单、描述、预配和删除需要 TiDB Cloud API 凭证。FS 令牌既不是删除 Filesystem 所必需的，也不能作为删除 Filesystem 的授权方式被接受。

## DB SQL 凭证 {#db-sql-credentials}

生成的 SQL 凭证以集群为作用域：

```text
~/.ti/db_users/<cluster-id>/credentials
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

`ti db create-db-sql-users` 会创建或修复这些稳定用户。它们不会存储在主凭证文件中。

这三种访问模式映射到 TiDB Cloud 内置数据库角色：

| `ti` 访问模式 | TiDB Cloud 内置角色 | 预期用途 |
| --- | --- | --- |
| `read_only` | `role_readonly` | 查询并验证数据而不修改数据 |
| `read_write` | `role_readwrite` | 查询并修改应用数据 |
| `admin` | `role_admin` | 执行 schema 变更并管理权限 |

有关完整的 TiDB Cloud 角色模型，请参见 [管理数据库用户和角色](https://docs.pingcap.com/tidbcloud/configure-sql-users)。

## 配套运行时状态与挂载定位文件 {#companion-state-and-mount-locators}

安装程序包含 `ti-drive9`，这是执行 `ti fs`、`ti fs-git`、`ti fs-journal` 和 `ti fs-vault` 操作的配套运行时。你无需直接调用它。每个已注册的 Filesystem 都有独立隔离的配套运行时主目录：

```text
~/.ti/drive9-home/<profile-key>/<resource-key>/
```

对于 `ti` 工作流，请不要修改这些状态，也不要修改独立的 `~/.drive9` 配置。

成功的后台 FS 或 vault 挂载会写入一个非敏感的定位文件：

```text
~/.ti/mounts/<mount-hash>.locator.json
```

该定位文件记录了在同一个 `HOME` 下执行刷写和卸载所需的部署位置及配套运行时主目录信息。它不包含 FS 令牌。成功卸载后会将其删除。

## 操作日志 {#operation-logs}

`ti` 会将经过脱敏处理的本地 JSON Lines 事件写入：

```text
~/.ti/logs/ti.jsonl
```

该日志是本地审计/调试数据，不属于遥测数据。它可能包含命令名称、参数名称、配置（Profile）和 region、持续时间、退出码和稳定错误码、HTTP 方法/状态、操作以及请求 ID。它不包含参数值、SQL、文件路径和内容、payload、连接字符串以及凭证。

为单个进程禁用它：

```bash
TI_LOGGING=off ti db list-db-clusters --db-cluster-type starter
```

或者创建或修改 `~/.ti/.preferences`：

```toml
schema_version = 1

[logging]
enabled = false
```

环境变量取值 `off`、`false`、`0` 和 `no` 会禁用日志记录；`on`、`true`、`1` 和 `yes` 会启用日志记录。环境变量的优先级高于设置。无效设置会在不导致所请求命令失败的情况下禁用操作日志。

对于现有安装，如果此前将 `[logging]` 存储在 `~/.ti/config` 中，系统会自动将这些值迁移到 `~/.ti/.preferences`。迁移会保留 profiles 和凭证。`ti update` 不会读写 `~/.ti/` 下的设置、profiles、凭证、操作日志或其他状态。

## 匿名遥测 {#anonymous-telemetry}

发布版本会为符合条件的命令向 TiDB Cloud CLI 遥测服务发送一条尽力而为的完成事件。该事件包含规范化命令以及显式提供的参数名称、稳定退出码和错误码、持续时间、region、CLI 版本、OS、架构、安装来源，以及一个随机的匿名安装 ID。它不包含参数值、凭证、令牌、SQL 文本、文件路径或内容、命令输出、API payload、配置名称或云资源 ID。

开发版本和已识别的 CI 环境默认禁用。帮助、版本、无命令用法以及所有 `ti update` 模式始终被排除在外。要持久禁用遥测，请添加以下全局偏好设置：

```toml
[telemetry]
enabled = false
```

为单个进程禁用它而不修改文件：

```bash
TI_TELEMETRY=off ti db list-db-clusters --db-cluster-type starter
```

TiDB Cloud CLI 会在首次产生符合条件的事件时按需创建 `~/.ti/.telemetry-installation-id`，并在支持 POSIX 权限时将其限制为当前用户可访问。删除此文件可重置该匿名身份。遥测传输可能会有丢失，且绝不会改变命令输出、错误或退出状态。

集成可以附加显式的进程作用域元信息，而无需修改 profile 或命令。`TI_TELEMETRY_TAG` 接受一个最长 128 字节的 UTF-8 字符串。`TI_TELEMETRY_EXTRA` 接受一个压缩后不超过 2 KiB 的完整 JSON 值。无效、被禁止、嵌套过深或过大的元信息会被忽略，且不会影响命令。请勿在这两个值中包含凭证、令牌、SQL、路径、个人数据、profile 名称或云资源 ID：

```bash
TI_TELEMETRY_TAG="e2b-preview" \
TI_TELEMETRY_EXTRA='{"campaign":"launch","runtime":"e2b"}' \
ti fs list-files --file-system-id <file-system-id> --path /
```

## 敏感值 {#sensitive-values}

请将以下内容视为 Secret：

- TiDB Cloud API 私钥和公钥对；
- FS 所有者令牌；
- DB SQL 用户名、密码和连接字符串；
- Vault 委派令牌和 Secret 值。

不要将它们放入源代码管理、工单、日志、命令示例或未受保护的 shell 历史记录中。

## 相关文档 {#related-documentation}

- [TiDB Cloud CLI Regions、安全性与限制](/ai/ti/reference/ti-regions-security-and-limitations.md)
- [TiDB Cloud CLI 故障排查](/ai/ti/reference/ti-troubleshooting.md)