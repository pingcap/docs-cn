---
title: TiDB Cloud CLI 区域、安全性与限制
summary: 参考支持的区域、认证边界、平台依赖、预览限制以及 Filesystem 伴随组件行为。
---

# TiDB Cloud CLI 区域、安全性与限制

本文档介绍当前的部署位置、认证、平台和预览边界。

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

如果你配置的区域支持 TiDB Cloud Starter 但不支持 TiDB Cloud Filesystem，则你仍然可以在该区域管理 Starter 实例。Filesystem 命令会因 `unsupported endpoint` 错误而失败。

支持的 Filesystem 区域内置于每个 `ti` 发布版本中。若要在你的已安装版本发布之后新增的区域中使用 Filesystem，请升级 `ti`。你不能通过指定服务 URL 来启用不受支持的区域。

## 凭证要求 {#credential-requirements}

| 操作 | 所需凭证 |
| --- | --- |
| `ti configure`、所有 `ti db` 控制平面操作 | TiDB Cloud API 公钥/私钥 |
| `ti fs create-file-system` | TiDB Cloud API key |
| `ti fs delete-file-system` | TiDB Cloud API key 和 文件系统 ID |
| 描述或修改 Filesystem 的媒体内容提取和向量嵌入配置 | TiDB Cloud API key 和显式 文件系统 ID |
| 生成、列出、启用、禁用或删除 Filesystem 访问令牌 | TiDB Cloud API key 和显式 文件系统 ID |
| 刷新 Filesystem 访问令牌 | 仅当前 FS bearer token |
| 远程文件、层、pack、挂载、Git、日志（Journal）和 owner vault 操作 | FS owner token 或已注册资源凭证 |
| 委派 vault 的读、列出、运行或挂载 | 与作用域匹配的 Vault 委派令牌 |
| 成功执行后台挂载后的刷写和卸载 | 同一 `HOME` 中的非 Secret 挂载定位文件 |

TiDB Cloud API 调用使用 Digest 认证。SQL HTTPS 执行使用通过 TLS 传输的、生成的 SQL 用户名/密码 Basic 认证。这些凭证不能互换使用。

## 安全最佳实践 {#security-best-practices}

- 创建 TiDB Cloud API key 时，仅授予工作流所需的访问权限。不要在无人值守的自动化流程中复用个人管理员 key。
- 从 CI Secret 存储或运行时 Secret 管理器中注入自动化凭证。不要将凭证放入源代码管理、容器镜像、shell 脚本或可能出现在进程列表和 shell 历史中的命令行参数中。
- 不要将完整的 `~/.ti/` 目录复制到 agent 沙箱中。对于现有 Filesystem，仅传递 `TI_FS_TOKEN` 和 `TI_REGION_CODE`；仅在作为可选断言时使用 `TI_FS_FILE_SYSTEM_ID`。
- 将 FS owner token 视为对该 Filesystem 的完全访问权限。当 agent 只需要部分 Secret 时，请创建一个字段作用域尽可能窄、TTL 尽可能短的 vault grant，并改为传递 Vault 委派令牌。
- 为每台机器、每个 CI 工作流或每类沙箱使用单独的 Filesystem 访问令牌，这样就可以在不中断其他环境的情况下禁用或回收某一个环境。令牌名称只是运维标签，不是唯一标识符；仅通过 `token_id` 修改令牌。
- 立即保存生成或刷新的令牌明文，因为它只会返回一次。通过 `TI_FS_TOKEN` 刷新的令牌不会被写回外部 Secret 管理器。刷新操作不是幂等的，因此在网络故障状态不明确时不要重试。
- 对于共享令牌轮换，先生成并分发替代令牌，验证访问正常后，再禁用并删除旧令牌。状态变更后，认证缓存大约需要 10 秒收敛。
- 仅通过 `TI_FS_AI_PROVIDER_API_KEY` 传递 AI provider key。TiDB Cloud CLI 不会在本地持久化该值，Filesystem 服务返回该值时也只会以掩码形式显示。在有效配置尚未通过 describe 确认之前，不要在失败状态不明确后重试 AI 配置修改。
- 启用媒体内容提取后，Filesystem 中的媒体数据会与已配置的媒体内容提取 provider 共享。启用应用管理的向量嵌入后，文本或提取出的描述会与已配置的嵌入 provider 共享。在启用任一功能前，请先审查该 provider 的数据保留和安全条款。
- 对于不受信任或探索性的 agent 执行 SQL 检查时，请使用 `--read-only`。仅在执行 DDL 或权限管理时使用 `--admin`，仅在确实需要修改数据时使用 `--read-write`。
- 在执行破坏性的控制平面操作前，先使用 `--dry-run`。确保 `~/.ti/credentials`、资源凭证和 DB SQL 凭证仅对所有者可读。
- 仅向专用且受信任的容器授予对 `/dev/fuse`、`SYS_ADMIN` 和非受限 AppArmor profile 的 Docker 访问权限。这些设置会降低容器隔离性。
- 在共享诊断信息前，请先检查本地操作日志。日志不包含 SQL 文本、路径、payload 和凭证值，但命令名称、（命令行）标记/参数名称、配置（Profile）和区域元信息、状态码以及操作时序信息仍可能是敏感信息。

## 挂载平台限制 {#mount-platform-limitations}

| 平台 | Filesystem 挂载 | Vault 挂载 | 要求与替代方案 |
| --- | --- | --- | --- |
| macOS | 默认使用 WebDAV；显式指定 `--driver fuse` 时使用 FUSE | FUSE | 内置的 WebDAV helper 支持 Filesystem 挂载。对于 FUSE 或 Vault 挂载，请安装 macFUSE 并批准其系统扩展。 |
| Linux | FUSE | FUSE | 安装 FUSE3 并提供对 `/dev/fuse` 的访问。WebDAV 挂载不受支持。 |
| Windows | 不支持 | 不支持 | 请改用 `ti fs` 数据平面命令和非挂载类 Vault 命令。 |

FUSE 和 WebDAV 由随附的 [Drive9](https://github.com/mem9-ai/drive9) 伴随组件实现。TiDB Cloud CLI 不会回退到单独的原生挂载实现。

Ubuntu 26.04 还会使用 AppArmor 对 `fusermount3` 进行限制。请使用位于 `$HOME` 或 `/mnt` 下的挂载路径；即使 `ti` 以 root 身份运行，`/workspace` 也需要显式的本地 AppArmor 规则。

## 持久性限制 {#durability-limitations}

- 默认的 FUSE 行为会在伴随组件允许的情况下使用本地缓冲和异步远程处理。
- 成功执行 `unmount-file-system` 会优雅地刷写并完成 FUSE 工作；无需先单独执行一次刷写。
- `drain-file-system` 是仅适用于 FUSE 的在线持久性屏障，执行后挂载仍保持活动状态。
- 强制终止挂载进程或删除机器可能会导致尚未提交的内存/回写状态丢失。
- 默认的 coding-agent 挂载预设会将依赖关系树、生成输出、缓存和 Git 内部数据存储在本地。除非这些仅本地数据已被打包或以其他方式保留，否则其所在磁盘消失时，这些数据也会消失。
- 正在运行的挂载会持续使用挂载时加载的伴随组件版本。更新 TiDB Cloud CLI 后，请卸载并重新挂载。
- 已远程提交的 Filesystem 数据在客户端或沙箱被删除后仍会保留；删除机器不会删除远程资源。

## 产品限制 {#product-limitations}

- TiDB Cloud CLI 处于预览阶段，命令契约可能会发生变化。
- 数据库管理面向 TiDB Cloud Starter，而不是所有 TiDB Cloud 集群层级。
- SQL 执行每次调用只接受一条语句。
- 读写是默认 SQL 角色；在对安全敏感的自动化场景中，请使用显式角色参数。
- 日志（Journal）为仅追加，当前公开的命令接口中没有删除 journal 的命令。
- Filesystem 的 list 和 describe 命令会使用 TiDB Cloud 凭证查询区域作用域内的远程资源清单，不会跨区域聚合。
- 本地凭证存储会为每个配置（Profile）和 Filesystem 保留一个已选中的令牌，不会镜像所有远程令牌。较早创建/导入且没有已知 token ID 的凭证仍可使用，但无法与远程令牌元信息关联。
- Filesystem 的媒体内容提取和向量嵌入 provider 配置是可选的。保持未配置状态不会阻止资源管理、文件访问、搜索、层、Git、日志（Journal）、Vault 或挂载工作流。
- embedding 以及镜像、音频和视频媒体内容提取支持 OpenAI provider 接口。Alibaba Cloud Model Studio Qwen ASR 仅支持音频媒体内容提取。其他厂商仅在严格符合 OpenAI-compatible 契约时才具备条件兼容性；不支持原生 Anthropic、Gemini、Vertex AI、Bedrock 和 Azure OpenAI 接口。
- 应用管理的向量嵌入要求 provider model 精确返回 1024 维。报告 `source=database_auto` 的 Filesystem 使用数据库管理的向量嵌入，并会拒绝应用管理配置。
- 遥测管理命令是有意未实现的。请通过 `~/.ti/.preferences` 或 `TI_TELEMETRY` 控制遥测；未实现 serverless-function 部署、Homebrew 和 Scoop 分发。
- TiDB Cloud CLI 的所有公开 Filesystem 运行时行为都依赖其已安装的 `ti-drive9` 伴随组件，包括直接文件操作、层、挂载、Git 工作区、journals 和 Vault 操作。

## 相关文档 {#related-documentation}

- [TiDB Cloud Filesystem CLI 命令参考](/ai/ti/reference/ti-filesystem.md)
- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)
- [排查 TiDB Cloud CLI 故障](/ai/ti/reference/ti-troubleshooting.md)