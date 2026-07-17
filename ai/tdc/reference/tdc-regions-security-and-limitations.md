---
title: tdc 区域、安全与限制
summary: 参考 tdc 支持的 region、认证边界、平台依赖、Preview 限制和文件系统 companion 行为。
---

# tdc 区域、安全与限制

本文说明当前部署区域、认证、平台和 Preview 边界。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## TiDB Cloud region

tdc 接受一个 canonical region code：

| Canonical code | Provider | Location |
| --- | --- | --- |
| `aws-us-east-1` | AWS | N. Virginia |
| `aws-us-west-2` | AWS | Oregon |
| `aws-eu-central-1` | AWS | Frankfurt |
| `aws-ap-northeast-1` | AWS | Tokyo |
| `aws-ap-southeast-1` | AWS | Singapore |
| `ali-ap-southeast-1` | Alibaba Cloud | Singapore |

Alibaba Cloud 当前在 tdc 中只支持 Singapore。用户不能配置原始 service URL。

## 文件系统 region

文件系统 endpoint 的可用性由托管的 Drive9 region manifest 解析。本文发布时，TiDB Cloud native Filesystem mode 支持：

- `aws-us-east-1`；
- `aws-ap-southeast-1`。

托管的 manifest 是权威来源，在 Preview 阶段可能变化。位于其他 TiDB Cloud region 的 profile 仍可以管理 Starter 数据库，但在 manifest 支持该部署区域之前，文件系统命令会返回 endpoint 不受支持的错误。

## 凭证要求

| 操作 | 所需凭证 |
| --- | --- |
| `tdc configure`、`tdc organization`、所有 `tdc db` control-plane 操作 | TiDB Cloud API public/private key |
| `tdc fs create-file-system` | TiDB Cloud API key |
| `tdc fs delete-file-system` | TiDB Cloud API key、本地资源注册信息和 owner 资源凭证 |
| 远端文件、layer、pack、挂载、Git、Journal 和 owner Vault 操作 | FS owner token 或已注册的资源凭证 |
| 委派的 Vault 读取、列出、运行或挂载操作 | Scope 合适的委派 Vault token |
| 后台挂载成功后的 drain 和 unmount | 同一 `HOME` 中的非敏感挂载定位信息 |

TiDB Cloud API 调用使用 Digest 认证。SQL HTTPS 执行使用生成的 SQL 用户名和密码，并通过 TLS 上的 Basic 认证传递。这些凭证不能互换。

## 安全建议

- 密钥优先使用环境变量或受保护的凭证文件。
- SQL 使用显式 read-only、read-write 或 admin 角色。
- Agent 仅需访问密钥时，应提供委派的 Vault grant，而不是 FS owner token。
- 执行破坏性 control-plane 操作前使用 `--dry-run`。
- 确保 `~/.tdc/credentials`、资源凭证和 DB SQL 凭证仅所有者可读。
- 即使 tdc 会对已知密钥类型进行脱敏，共享诊断信息前仍应检查本地操作日志。

## 挂载平台限制

| 平台 | 默认 | 限制 |
| --- | --- | --- |
| macOS | WebDAV | 安装 macFUSE 并显式使用 `--driver fuse`，获得 FUSE cache、drain 和更完整的 POSIX 行为 |
| Linux | FUSE | 需要 FUSE3 和 `/dev/fuse`；显式 WebDAV 需要 `davfs2` |
| Windows | WebDAV | 需要 WebClient 服务和盘符形式的挂载路径；不支持 FUSE 和 Vault 挂载 |

FUSE 和 WebDAV 由内置 [Drive9](https://github.com/mem9-ai/drive9) companion 实现。tdc 不会回退到另一套原生挂载实现。

## 持久性限制

- companion 支持时，默认 FUSE 行为会使用本地缓冲和异步远端操作。
- `drain-file-system` 仅支持 FUSE。
- 突然终止挂载进程或删除机器，可能丢失尚未提交的内存或 write-back 状态。
- 默认 `coding-agent` 挂载 profile 会在本地保存依赖树、生成输出、缓存和 Git 内部状态。除非执行 pack 或以其他方式保留，否则这些本地数据会随磁盘删除而消失。
- 运行中的挂载会继续使用挂载时加载的 companion 版本。更新 tdc 后需要卸载并重新挂载。
- 已提交到远端的文件系统数据不受客户端或沙箱删除影响；删除机器不会删除远端资源。

## 产品限制

- tdc 处于 Preview，命令契约可能变化。
- 数据库管理面向 TiDB Cloud Starter，不覆盖所有 TiDB Cloud 集群规格。
- 每次 SQL 执行只接受一条 statement。
- 默认 SQL 角色为 read-write；安全敏感的自动化应显式指定角色参数。
- Journal 仅支持追加，当前公开命令面没有删除 Journal 的命令。
- 文件系统资源的 list 和 describe 针对本地 registry，不是 organization 级的发现 API。
- Telemetry 命令、Serverless Function 部署、Homebrew 和 Scoop 分发尚未实现。
- 所有公开的文件系统运行时行为都依赖已安装的 `tdc-drive9` companion。

## 相关文档

- [使用 tdc 管理 TiDB Cloud 文件系统](/ai/tdc/guides/tdc-filesystem.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [tdc 故障排查](/ai/tdc/reference/tdc-troubleshooting.md)
