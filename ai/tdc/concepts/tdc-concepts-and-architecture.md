---
title: tdc 概念与架构
summary: 了解 tdc profile、region、凭证、SQL 角色、文件系统资源、本地状态和内置的 Drive9 companion。
---

# tdc 概念与架构

本文介绍使用 tdc 管理 TiDB Cloud Starter 和 TiDB Cloud 文件系统所需的核心概念。

> **注意：**
>
> tdc 当前处于预览（Preview）阶段，其功能和命令行界面可能会发生变更，恕不另行通知。

## 命令模型

tdc 使用 service 名词和显式 operation 名称：

```text
tdc db create-db-cluster
tdc fs copy-file
tdc fs-git clone-git-workspace
```

命令树最多两级。完整且清晰的命令与参数名称，让日志和 Agent 生成的命令更容易理解。除 `tdc configure` 外，其他命令均不交互。

结构化命令默认返回 JSON。使用 `--output text` 获得面向终端的输出，使用 `--query` 进行 JMESPath 投影。

## Profile 与 region

Profile 是包含 TiDB Cloud 部署区域、默认 virtual project 和凭证的本地命名空间。默认 profile 名为 `default`，使用 `--profile` 选择其他 profile。

tdc 使用一个 canonical region code 表示 placement：

```text
aws-us-east-1
aws-ap-southeast-1
ali-ap-southeast-1
```

前缀表示云服务提供商。全局 `--region` 可为单次命令覆盖 `TDC_REGION_CODE` 和 profile 中的 region，但不会修改已保存的配置。

执行 `tdc configure` 时，tdc 会调用 organization API，并要求 API key 恰好能访问一个 `type = "tidbx_virtual"` 的 project。该 project ID 会成为创建 Starter 集群时的默认值。

## 凭证边界

tdc 为不同安全边界使用不同凭证：

| 凭证 | 用途 | 存储位置 |
| --- | --- | --- |
| TiDB Cloud API public/private key | Organization、Starter control plane、文件系统创建与删除 | `~/.tdc/credentials` |
| DB SQL 用户名/密码 | 访问一个 Starter 集群的 SQL | `~/.tdc/db_users/<cluster-id>/credentials` |
| 文件系统 owner token | 文件系统数据面、挂载、Git、Journal 和 owner Vault 操作 | `~/.tdc/fs_resources/` 下的每资源凭证或 `TDC_FS_TOKEN` |
| 委派 Vault token | 对指定 secret 字段的有限访问 | `TDC_VAULT_TOKEN` 或显式命令输入 |

TiDB Cloud API key 不会被复用为 SQL 密码或文件系统 token。

## SQL 角色

`tdc db create-db-sql-users` 为集群创建或修复三个稳定用户：

- `read_only`：不能修改数据的查询；
- `read_write`：常规应用与 Agent 工作；
- `admin`：DDL 和权限管理。

使用 `--read-only`、`--read-write` 或 `--admin` 显式选择角色。不提供角色 flag 时，默认使用 read-write。

## 一个 profile 管理多个文件系统

一个 profile 可以注册多个文件系统资源。每个资源拥有独立的配置和凭证文件。选择顺序如下：

1. `--file-system-name`；
2. `TDC_FS_FILE_SYSTEM_NAME`；
3. profile 的默认文件系统；
4. 只有一个已注册文件系统时，选择该资源。

如果存在多个资源但没有选择，tdc 会报错而不是猜测。使用 `tdc fs set-default-file-system` 设置默认资源。

## 无配置 sandbox 访问

全新的 Agent 沙箱不需要运行 `tdc configure`，也不需要 TiDB Cloud API key。只需提供：

```bash
export TDC_FS_TOKEN="<owner-token>"
export TDC_REGION_CODE="aws-us-east-1"
export TDC_FS_FILE_SYSTEM_NAME="workspace"
```

tdc 会在内存中将这些值解析为 profile 命名空间，不会写入 `[env]` profile，也不会持久化 token。

## 本地状态

tdc 管理的所有状态都位于 `~/.tdc/`：

| 路径 | 内容 |
| --- | --- |
| `config` | 非敏感 profile、默认 project 和日志设置 |
| `credentials` | TiDB Cloud API key |
| `fs_resources/` | 按 profile 和文件系统隔离的元数据与 owner 凭证 |
| `db_users/` | 集群级 SQL 凭证 |
| `mounts/` | 后台挂载的非敏感定位信息 |
| `logs/tdc.jsonl` | 已脱敏的本地 operation log |
| `bin/` | 已安装的 `tdc` 和 `tdc-drive9` |

Operation logging 是本地日志，不是 telemetry。设置 `TDC_LOGGING=off` 可为单个进程关闭。

## tdc 与 Drive9 companion

tdc 将 [Drive9](https://github.com/mem9-ai/drive9) 安装为内部名称 `tdc-drive9`。

tdc 负责：

- profile、凭证、region 和文件系统选择；
- TiDB Cloud control-plane 调用；
- JSON/text 输出、查询、错误和本地日志；
- 将 tdc 命令转换为 companion 调用。

Companion 负责：

- 文件系统读写、元数据、链接、搜索和 layer；
- FUSE/WebDAV 挂载进程、缓存、drain 和 unmount；
- pack/unpack、Git workspace、Journal 和 Vault 语义。

后台挂载会留下长期运行的 `tdc-drive9 mount --foreground` 进程。`tdc fs drain-file-system` 要求该进程刷出待处理的 FUSE 工作，`tdc fs unmount-file-system` 停止挂载。不要在仍有未刷出的写入或需要保留的本地 overlay 数据时终止机器。

## 后续步骤

- [安装、配置和更新 tdc](/ai/tdc/guides/tdc-install-configure-update.md)
- [tdc 配置与凭证](/ai/tdc/reference/tdc-configuration-and-credentials.md)
- [tdc 区域、安全与限制](/ai/tdc/reference/tdc-regions-security-and-limitations.md)
