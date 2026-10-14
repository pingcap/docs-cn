---
title: 从 tdc 迁移到 TiDB Cloud CLI
summary: 将受支持的本地状态和自动化从 tdc v0.1.x 迁移到 TiDB Cloud CLI。
---

# 从 tdc 迁移到 TiDB Cloud CLI

仅当你之前使用过 `tdc` v0.1.x 时，才需要执行此迁移。新安装的 TiDB Cloud CLI 不需要执行此迁移。

> **注意：**
>
> TiDB Cloud CLI (`ti`) 当前处于公测预览阶段。其功能和命令行接口可能会在不另行通知的情况下发生变化。

## 开始之前 {#before-you-begin}

- 停止写入程序，并卸载所有由 `tdc` 启动的文件系统和 Vault 挂载。如果旧挂载仍处于活动状态，迁移将停止，因为它无法转移正在运行的 FUSE 或 WebDAV 进程。

    对每个活动挂载，运行相应的命令。对于 FUSE 文件系统挂载，先运行 `drain-file-system` 以刷写待处理的写入，然后运行 `unmount-file-system` 以卸载挂载。对于 WebDAV 文件系统挂载，停止写入程序后仅运行 `unmount-file-system`。Vault 挂载只需要运行 `unmount-vault`。

    ```bash
    # FUSE file system mount
    tdc fs drain-file-system --mount-path <filesystem-mount-path>
    tdc fs unmount-file-system --mount-path <filesystem-mount-path>

    # WebDAV file system mount
    tdc fs unmount-file-system --mount-path <filesystem-mount-path>

    # Vault mount
    tdc fs-vault unmount-vault --mount-path <vault-mount-path>
    ```

- 在解决目录冲突之前，备份 `~/.tdc/` 以及任何现有的 `~/.ti/` 目录。

## 安装 ti 并迁移本地状态 {#install-ti-and-migrate-local-state}

旧的 `tdc update` 命令无法安装重命名后的 `ti` 可执行文件，并且 `ti` 不提供 `tdc` 命令别名。请按照[安装 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md#install-tidb-cloud-cli)中的说明直接安装 `ti`。

当 `~/.tdc/` 存在且 `~/.ti/` 不存在时，安装程序以及首次执行的非更新类 `ti` 命令会自动迁移受支持的本地状态。迁移会保留 `~/.tdc/` 作为回滚副本，并在 `~/.ti/` 下创建一个仅所有者可访问的标记文件，用于记录迁移已完成。

下表总结了哪些状态会被迁移：

| 已迁移 | 未迁移 |
| --- | --- |
| 配置（Profile）和 TiDB Cloud API 凭证 | 二进制文件 |
| 全局偏好设置和遥测安装标识 | 日志和缓存 |
| 数据库 SQL 凭证 | 本地叠加层 |
| 文件系统注册信息和凭证 | 挂载定位文件和配套运行时状态 |

安装完成后，验证新的可执行文件，并针对你使用的资源运行只读命令。例如：

```bash
ti --version

# For TiDB Cloud Starter
ti db list-db-clusters --db-cluster-type starter --output text

# For TiDB Cloud Filesystem
ti fs list-file-systems --output text
```

验证迁移完成后，当你不再需要回滚副本时，可以删除旧的 `tdc` 二进制文件和本地状态。

## 解决本地状态冲突 {#resolve-a-local-state-conflict}

如果 `~/.tdc/` 和 `~/.ti/` 是分别独立创建的，或者迁移标记缺失、无效，或指向不同的源目录，`ti` 会停止运行，而不会合并或覆盖任一目录。

请确定哪个目录才是预期的真实来源，并将另一个目录移动到备份位置。然后再次运行安装程序或 `ti` 命令。不要手动合并凭证目录或文件系统注册目录。

## 更新环境变量 {#update-environment-variables}

更新自动化脚本，改用以下环境变量名称：

| `tdc` v0.1.x 变量 | `ti` 变量 |
| --- | --- |
| `TDC_PROFILE` | `TI_PROFILE` |
| `TDC_REGION_CODE` | `TI_REGION_CODE` |
| `TDC_PUBLIC_KEY` | `TIDB_CLOUD_PUBLIC_KEY` |
| `TDC_PRIVATE_KEY` | `TIDB_CLOUD_PRIVATE_KEY` |
| `TDC_FS_TOKEN` | `TI_FS_TOKEN` |
| `TDC_FS_FILE_SYSTEM_ID` | `TI_FS_FILE_SYSTEM_ID` |
| `TDC_LOGGING` | `TI_LOGGING` |
| `TDC_TELEMETRY` | `TI_TELEMETRY` |
| `TDC_TELEMETRY_TAG` | `TI_TELEMETRY_TAG` |
| `TDC_TELEMETRY_EXTRA` | `TI_TELEMETRY_EXTRA` |
| `TDC_VAULT_TOKEN` | `TI_VAULT_TOKEN` |
| `TDC_INSTALL_DIR` | `TI_INSTALL_DIR` |

在 v0.2.x 过渡期间，只有在对应的新变量未设置时，`ti` 才会接受旧版 `TDC_*` 环境变量。如果两种形式都已设置且值不同，命令会在修改本地或远程状态之前失败。对旧版 `TDC_*` 变量的支持将在 v0.3.0 中移除。

## 后续步骤 {#what-s-next}

- [安装、配置和更新 TiDB Cloud CLI](/ai/ti/reference/ti-install-configure-update.md)
- [TiDB Cloud CLI 配置与凭证](/ai/ti/reference/ti-configuration-and-credentials.md)
- [管理 TiDB Cloud Starter 实例](/ai/ti/guides/manage-starter-instances.md)
- [管理 TiDB Cloud Filesystem](/ai/ti/guides/manage-filesystems-via-cli.md)
- [排查 TiDB Cloud CLI 故障](/ai/ti/reference/ti-troubleshooting.md)