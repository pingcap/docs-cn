---
title: TiDB Cloud CLI 区域、安全性与限制
summary: 参考支持的区域、认证边界、安全最佳实践以及当前 TiDB Cloud CLI 限制。
---

# TiDB Cloud CLI 区域、安全性与限制

本文档介绍 TiDB Cloud CLI 当前的区域、认证、平台和预览边界。有关文件系统区域和限制，请参见 [TiDB Cloud Filesystem 区域和限制](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md)。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公开预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 支持的区域 {#supported-regions}

使用 TiDB Cloud CLI 时，你需要为 CLI 操作配置一个默认区域。

下表列出了 TiDB Cloud CLI 支持的区域，并说明了每个区域中可用的 TiDB Cloud CLI 服务。

| 提供商 | 位置 | 规范区域代码 | TiDB Cloud Starter | TiDB Cloud Filesystem |
| --- | --- | --- | --- | --- |
| AWS | 弗吉尼亚北部 | `aws-us-east-1` | 支持 | 支持 |
| AWS | 俄勒冈 | `aws-us-west-2` | 支持 | 支持 |
| AWS | 新加坡 | `aws-ap-southeast-1` | 支持 | 支持 |
| AWS | 法兰克福 | `aws-eu-central-1` | 支持 | 不支持 |
| AWS | 东京 | `aws-ap-northeast-1` | 支持 | 不支持 |
| Alibaba Cloud | 新加坡 | `alicloud-ap-southeast-1` | 支持 | 支持 |

如果你配置的区域支持 TiDB Cloud Starter 但不支持 TiDB Cloud Filesystem，则你仍然可以在该区域管理 Starter 实例。文件系统命令会因 `unsupported endpoint` 错误而失败。

支持的文件系统区域内置于每个 `ti` 发布版本中。若要在你的已安装版本发布之后新增的区域中使用文件系统，请升级 `ti`。你不能通过指定服务 URL 来启用不受支持的区域。

## 凭证要求 {#credential-requirements}

| 操作 | 所需凭证 |
| --- | --- |
| `ti configure`、所有 `ti db` 控制平面操作 | TiDB Cloud API 公钥/私钥 |
| `ti fs create-file-system` | TiDB Cloud API key |
| `ti fs delete-file-system` | TiDB Cloud API key 和文件系统 ID |
| 描述或修改文件系统的媒体内容提取和向量嵌入配置 | TiDB Cloud API key 和显式文件系统 ID |
| 生成、列出、启用、禁用或删除文件系统访问令牌 | TiDB Cloud API key 和显式文件系统 ID |
| 刷新文件系统访问令牌 | 仅当前 FS bearer token |
| 远程文件、层、pack、挂载、Git、日志（Journal）和 owner vault 操作 | FS owner token 或已注册资源凭证 |
| 委派 vault 的读、列出、运行或挂载 | 与作用域匹配的 Vault 委派令牌 |
| 成功执行后台挂载后的刷写和卸载 | 同一 `HOME` 中的非 Secret 挂载定位文件 |

TiDB Cloud API 调用使用 Digest 认证。SQL HTTPS 执行使用通过 TLS 传输的、生成的 SQL 用户名/密码 Basic 认证。这些凭证不能互换使用。

## 安全最佳实践 {#security-best-practices}

- 创建 TiDB Cloud API key 时，仅授予工作流所需的访问权限。不要在无人值守的自动化流程中复用个人管理员 key。
- 从 CI Secret 存储或运行时 Secret 管理器中注入自动化凭证。不要将凭证放入源代码管理、容器镜像、shell 脚本或可能出现在进程列表和 shell 历史中的命令行参数中。
- 不要将完整的 `~/.ti/` 目录复制到 agent 沙箱中。对于现有文件系统，仅传递 `TI_FS_TOKEN` 和 `TI_REGION_CODE`；仅在作为可选断言时使用 `TI_FS_FILE_SYSTEM_ID`。
- 对于不受信任或探索性的 agent 执行 SQL 检查时，请使用 `--read-only`。仅在执行 DDL 或权限管理时使用 `--admin`，仅在确实需要修改数据时使用 `--read-write`。
- 在执行破坏性的控制平面操作前，先使用 `--dry-run`。确保 `~/.ti/credentials`、资源凭证和 DB SQL 凭证仅对所有者可读。
- 在共享诊断信息前，请先检查本地操作日志。日志不包含 SQL 文本、路径、payload 和凭证值，但命令名称、（命令行）标记/参数名称、配置（Profile）和区域元信息、状态码以及操作时序信息仍可能是敏感信息。

有关文件系统访问令牌、挂载、Vault 和 AI provider 安全性，请参见 [Authorization](/tidb-cloud-filesystem/filesystem-authorization.md)、[Manage File System Tokens](/tidb-cloud-filesystem/manage-filesystem-tokens.md) 和 [Configure AI Providers for a File System](/tidb-cloud-filesystem/configure-filesystem-ai-providers.md)。

## 产品限制 {#product-limitations}

- TiDB Cloud CLI 处于预览阶段，命令契约可能会发生变化。
- 数据库管理面向 TiDB Cloud Starter 实例，而不是其他 TiDB Cloud 数据库计划。
- SQL 执行每次调用只接受一条语句。
- 读写是默认 SQL 角色；在对安全敏感的自动化场景中，请使用显式角色参数。
- 遥测管理命令是有意未实现的。请通过 `~/.ti/.preferences` 或 `TI_TELEMETRY` 控制遥测；未实现 serverless-function 部署、Homebrew 和 Scoop 分发。

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem 区域和限制](/tidb-cloud-filesystem/filesystem-regions-and-limitations.md)
- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)
- [排查 TiDB Cloud CLI 故障](/ai/ti/reference/ti-troubleshooting.md)