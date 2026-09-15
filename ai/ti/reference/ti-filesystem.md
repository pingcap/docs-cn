---
title: TiDB Cloud Filesystem CLI 命令参考
summary: 参考所有用于 Filesystem 资源、文件、层、打包和挂载的 `ti fs` 命令。
---

# TiDB Cloud Filesystem CLI 命令参考

使用 `ti fs` 可以预配 TiDB Cloud Filesystem 资源，并通过命令或本地挂载访问其中的数据。

在命令语法中，方括号（`[]`）表示可选项。圆括号用于对必选项进行分组，竖线（`|`）用于分隔可选分支。例如，`(--ttl <duration> | --no-expiration)` 表示你必须且只能指定这两个选项中的一个。

## 资源和令牌命令 {#resource-and-token-commands}

| 命令 | 描述 |
| --- | --- |
| [`create-file-system`](/ai/ti/reference/ti-fs-create-file-system.md) | 创建一个 Filesystem 及其初始所有者令牌。 |
| [`list-file-systems`](/ai/ti/reference/ti-fs-list-file-systems.md) | 列出当前生效 Region 中的 Filesystem。 |
| [`describe-file-system`](/ai/ti/reference/ti-fs-describe-file-system.md) | 按 ID 描述一个 Filesystem。 |
| [`check-file-system`](/ai/ti/reference/ti-fs-check-file-system.md) | 检查 Filesystem 选择、路由、凭证以及数据平面访问。 |
| [`delete-file-system`](/ai/ti/reference/ti-fs-delete-file-system.md) | 永久删除一个 Filesystem。 |
| [`import-file-system-token`](/ai/ti/reference/ti-fs-import-file-system-token.md) | 在本地导入并选中一个现有的 Filesystem 访问令牌。 |
| [`generate-file-system-token`](/ai/ti/reference/ti-fs-generate-file-system-token.md) | 生成一个额外的所有者令牌。 |
| [`generate-file-system-scoped-token`](/ai/ti/reference/ti-fs-generate-file-system-scoped-token.md) | 生成一个受路径、操作和有效期限制的令牌。 |
| [`list-file-system-tokens`](/ai/ti/reference/ti-fs-list-file-system-tokens.md) | 列出不含 Secret 的令牌元信息。 |
| [`enable-file-system-token`](/ai/ti/reference/ti-fs-enable-file-system-token.md) | 重新启用已禁用的令牌。 |
| [`disable-file-system-token`](/ai/ti/reference/ti-fs-disable-file-system-token.md) | 临时禁用一个令牌。 |
| [`delete-file-system-token`](/ai/ti/reference/ti-fs-delete-file-system-token.md) | 永久（权限）回收一个令牌。 |
| [`refresh-file-system-token`](/ai/ti/reference/ti-fs-refresh-file-system-token.md) | 轮转一个令牌，并一次性返回其替代令牌。 |

### 令牌管理授权 {#token-management-authorization}

当所有者令牌被授予令牌管理权限后，它可以列出令牌、创建范围受限令牌，并（权限）回收所有者令牌或范围受限令牌。它只能启用或禁用范围受限令牌。TiDB Cloud API 凭证则可以启用、禁用或（权限）回收这两类令牌中的任意一种。

## AI 提供方配置命令 {#ai-provider-configuration-commands}

这些命令用于配置可选的提供方，以便从媒体文件中提取内容并生成向量嵌入。普通的 Filesystem 资源和文件操作不需要 AI 提供方配置。

| 命令 | 描述 |
| --- | --- |
| [`describe-file-system-extract-configuration`](/ai/ti/reference/ti-fs-describe-file-system-extract-configuration.md) | 描述媒体内容提取提供方配置。 |
| [`update-file-system-extract-configuration`](/ai/ti/reference/ti-fs-update-file-system-extract-configuration.md) | 修改用于提取媒体内容的提供方。 |
| [`describe-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-describe-file-system-embedding-configuration.md) | 描述向量嵌入提供方配置。 |
| [`update-file-system-embedding-configuration`](/ai/ti/reference/ti-fs-update-file-system-embedding-configuration.md) | 修改用于生成向量嵌入的提供方。 |

## 数据和命名空间命令 {#data-and-namespace-commands}

| 命令 | 描述 |
| --- | --- |
| [`copy-file`](/ai/ti/reference/ti-fs-copy-file.md) | 在本地存储与 Filesystem 之间，或在 Filesystem 内部复制文件。 |
| [`read-file`](/ai/ti/reference/ti-fs-read-file.md) | 读取远程文件或字节范围。 |
| [`list-files`](/ai/ti/reference/ti-fs-list-files.md) | 列出远程路径下的条目。 |
| [`describe-file`](/ai/ti/reference/ti-fs-describe-file.md) | 描述远程文件或目录。 |
| [`move-file`](/ai/ti/reference/ti-fs-move-file.md) | 移动或重命名远程路径。 |
| [`delete-file`](/ai/ti/reference/ti-fs-delete-file.md) | 删除远程文件或目录。 |
| [`create-directory`](/ai/ti/reference/ti-fs-create-directory.md) | 创建远程目录。 |
| [`chmod-file`](/ai/ti/reference/ti-fs-chmod-file.md) | 修改 POSIX 风格的模式元信息。 |
| [`create-symlink`](/ai/ti/reference/ti-fs-create-symlink.md) | 创建符号链接。 |
| [`create-hardlink`](/ai/ti/reference/ti-fs-create-hardlink.md) | 创建硬链接。 |
| [`search-file-content`](/ai/ti/reference/ti-fs-search-file-content.md) | 搜索提取出的文件内容和描述。 |
| [`find-files`](/ai/ti/reference/ti-fs-find-files.md) | 按名称、标签、日期、大小或类型查找文件。 |

## 层和可移植性命令 {#layer-and-portability-commands}

| 命令 | 描述 |
| --- | --- |
| [`create-layer`](/ai/ti/reference/ti-fs-create-layer.md) | 创建一个隔离的可写层。 |
| [`list-layers`](/ai/ti/reference/ti-fs-list-layers.md) | 列出 Filesystem 中的层。 |
| [`fork-layer`](/ai/ti/reference/ti-fs-fork-layer.md) | 从父 tip 或检查点派生一个子层。 |
| [`list-layer-chain`](/ai/ti/reference/ti-fs-list-layer-chain.md) | 列出某个层被固定的祖先链。 |
| [`describe-layer`](/ai/ti/reference/ti-fs-describe-layer.md) | 按 ID 描述一个层。 |
| [`diff-layer`](/ai/ti/reference/ti-fs-diff-layer.md) | 列出记录在某个层中的变更。 |
| [`create-layer-checkpoint`](/ai/ti/reference/ti-fs-create-layer-checkpoint.md) | 在层中创建一个持久检查点。 |
| [`delete-layer`](/ai/ti/reference/ti-fs-delete-layer.md) | 在逻辑上放弃一个层。 |
| [`rollback-layer`](/ai/ti/reference/ti-fs-rollback-layer.md) | 在不提交其变更的情况下回滚一个层。 |
| [`commit-layer`](/ai/ti/reference/ti-fs-commit-layer.md) | 将某个层的变更应用到基础 Filesystem。 |
| [`pack-file-system`](/ai/ti/reference/ti-fs-pack-file-system.md) | 将选定的本地叠加层状态归档到 Filesystem。 |
| [`unpack-file-system`](/ai/ti/reference/ti-fs-unpack-file-system.md) | 从归档中恢复本地叠加层状态。 |

### 层引用 {#layer-references}

层引用可以是层 ID、唯一的层名称，或形如 `tag:<key>=<value>` 的标签引用，例如 `tag:run=123`。由于名称和标签引用都可能存在歧义，因此在自动化场景中建议使用层 ID。

### 挂载预设和本地叠加层 {#mount-profiles-and-local-overlays}

本地叠加层用于存储挂载预设保留在本地机器上、而不是写入远程命名空间的文件。挂载预设定义了哪些路径使用该叠加层：

| 挂载预设 | 行为 |
| --- | --- |
| `coding-agent` | 将版本控制元信息、依赖关系目录、缓存、构建输出以及常见临时路径保存在本地叠加层中。它不会自动选择打包路径。 |
| `portable` | 使用与 `coding-agent` 相同的本地路径规则，并默认对完整叠加层执行打包或解包，因此你可以在不同机器或沙箱会话之间移动它。 |
| `none` | 禁用本地叠加层路径路由以及自动打包或解包行为。 |

## 挂载命令 {#mount-commands}

| 命令 | 描述 |
| --- | --- |
| [`mount-file-system`](/ai/ti/reference/ti-fs-mount-file-system.md) | 将 Filesystem 挂载到本地路径。 |
| [`drain-file-system`](/ai/ti/reference/ti-fs-drain-file-system.md) | 从在线 FUSE 挂载中刷写待处理的写入。 |
| [`unmount-file-system`](/ai/ti/reference/ti-fs-unmount-file-system.md) | 刷写并卸载一个 Filesystem。 |

## 命令别名 {#command-aliases}

以下 `ti fs` 命令提供 Unix 风格的别名。例如，`ti fs cp` 等价于 `ti fs copy-file`。表中未列出的命令（包括 `pack-file-system` 和 `unpack-file-system`）没有别名。

| 别名 | 规范命令 |
| --- | --- |
| `cp` | `copy-file` |
| `cat` | `read-file` |
| `ls` | `list-files` |
| `stat` | `describe-file` |
| `mv` | `move-file` |
| `rm` | `delete-file` |
| `mkdir` | `create-directory` |
| `chmod` | `chmod-file` |
| `symlink` | `create-symlink` |
| `hardlink` | `create-hardlink` |
| `grep` | `search-file-content` |
| `find` | `find-files` |
| `mount` | `mount-file-system` |
| `drain` | `drain-file-system` |
| `umount` | `unmount-file-system` |

别名与规范命令使用相同的选项、认证、输出、查询和错误处理行为。

## 另请参阅 {#see-also}

- [管理 TiDB Cloud Filesystem 资源](/ai/ti/guides/manage-filesystem-resources.md)
- [配置 TiDB Cloud Filesystem AI 提供方](/ai/ti/guides/configure-filesystem-ai-providers.md)
- [管理 TiDB Cloud Filesystem 令牌](/ai/ti/guides/manage-filesystem-tokens.md)
- [使用 TiDB Cloud Filesystem 数据](/ai/ti/guides/work-with-filesystem-data.md)
- [管理 Filesystem 层和检查点](/ai/ti/guides/manage-filesystem-layers.md)
- [挂载 TiDB Cloud Filesystem](/ai/ti/guides/mount-filesystem.md)
- [在 TiDB Cloud Filesystem 上管理 Git 工作区](/ai/ti/guides/manage-git-workspaces.md)
- [使用 TiDB Cloud Filesystem Journals](/ai/ti/guides/use-filesystem-journals.md)
- [管理 TiDB Cloud Filesystem Vault Secrets](/ai/ti/guides/manage-filesystem-vault-secrets.md)