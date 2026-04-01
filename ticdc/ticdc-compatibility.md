---
title: TiCDC 兼容性
summary: 了解 TiCDC 兼容性相关限制和问题处理。
---

# TiCDC 兼容性

本文介绍了与 TiCDC 有关的一系列兼容性问题及其处理方案。

## TiCDC 与 TiDB Lightning 的兼容性

[TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md) 支持[逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode.md)和[物理导入模式](/tidb-lightning/tidb-lightning-physical-import-mode.md)两种数据导入模式。本章节介绍这两种模式与 TiCDC 的兼容性，以及同时使用 TiDB Lightning 和 TiCDC 时的操作步骤。

在逻辑导入模式下，TiDB Lightning 通过执行 SQL 语句导入数据。此模式与 TiCDC 兼容。你可以按照以下步骤同时使用 TiDB Lightning 逻辑导入模式和 TiCDC 进行数据同步：

1. 创建 changefeed，详情参考[创建同步任务](/ticdc/ticdc-manage-changefeed.md#创建同步任务)。
2. 启动 TiDB Lightning 并使用逻辑模式模式导入数据，详情参考[使用逻辑导入模式](/tidb-lightning/tidb-lightning-logical-import-mode-usage.md)。

在物理导入模式下，TiDB Lightning 通过向 TiKV 插入 SST 文件的方式导入数据。TiCDC 与此模式不兼容，不支持同步通过物理模式导入的数据。如果你需要同时使用 TiDB Lightning 物理导入模式和 TiCDC，可以根据 TiCDC 下游系统的类型选择以下解决方案：

- 下游系统是 TiDB 集群：
    1. 使用 TiDB Lightning 分别向上下游 TiDB 集群导入数据，以确保两个集群的数据一致性。
    2. 创建 changefeed，用于同步后续通过 SQL 写入的增量数据。详情参考[创建同步任务](/ticdc/ticdc-manage-changefeed.md#创建同步任务)。

- 下游系统不是 TiDB 集群：
    1. 使用下游系统提供的离线导入工具，将 TiDB Lightning 的输入文件导入到下游系统。
    2. 创建 changefeed，用于同步后续通过 SQL 写入的增量数据。详情参考[创建同步任务](/ticdc/ticdc-manage-changefeed.md#创建同步任务)。

## TiCDC 与 TiFlash 的兼容性

目前，使用 TiCDC 同步表到下游 TiDB 集群时，不支持为表创建 TiFlash 副本，即 TiCDC 不支持同步 TiFlash 相关的 DDL，例如:

* `ALTER TABLE table_name SET TIFLASH REPLICA count;`
* `ALTER DATABASE db_name SET TIFLASH REPLICA count;`

## 历史版本滚动升级兼容性说明

> **注意：**
>
> - 本节适用于基于旧架构实现的 TiCDC 历史版本（`v6.5.0` 到 `v8.5.5`）。
> - 本节中的“最高目标版本”表示：从 TiCDC 自身版本兼容性检查看，在滚动升级的混合版本窗口内，不会被旧版本 TiCDC 直接拒绝的最高版本。
> - 本节结论不等同于对任意跨 minor 升级路径的完整支持矩阵。执行正式升级前，请同时查阅目标版本的 Release Notes 与升级文档。

TiCDC 依赖 TiDB、TiKV 和 PD 提供的上游变更数据及相关接口。随着 TiDB 集群持续演进，这些数据格式和接口可能发生变化。因此，旧架构 TiCDC 不对与更高版本 TiDB/TiKV/PD 的跨版本混部提供正式的向上兼容性保证。在滚动升级过程中，只要旧的 TiCDC 实例仍然存活，它就会继续校验新版本 PD、TiKV 和 peer TiCDC 的版本。虽然相关 API 在设计上会尽量保持兼容，但旧架构 TiCDC 对混合版本部署场景缺少充分的兼容性验证，因此 `pkg/version/check.go` 中的版本兼容性检查会直接影响滚动升级窗口是否可行。

该兼容性检查的关键分界点如下：

- `v7.1.5`：将 `maxPDVersion`、`maxTiKVVersion` 和 `MaxTiCDCVersion` 的上限从 `< 8.0.0` 提升到 `< 9.0.0`。
- `v7.5.2`：同样将上述上限从 `< 8.0.0` 提升到 `< 9.0.0`。
- `v7.6.0`：仍然保持 `< 8.0.0` 上限，**不会**继承 `v7.5.2` 及之后版本的 `< 9.0.0` 上限。
- `v8.0.0`：首次将上述上限提升到 `< 10.0.0`。
- `v8.2.0` 及之后版本：在保持 `< 10.0.0` 上限的同时，将 `minPDVersion` 和 `MinTiKVVersion` 提升到 `7.1.0-alpha`。

下表总结了旧架构 TiCDC 从 `v6.5` 到 `v8.5` 的滚动升级兼容性结论：

| 源版本范围 | 从 TiCDC 自身兼容性检查看最高可滚动到 | 是否建议直接与 `8.x` 滚动混跑 | 说明 |
| :-- | :-- | :-- | :-- |
| `v6.5.x`、`v6.6.0`、`v7.0.0`、`v7.2.0`、`v7.3.0`、`v7.4.0`、`v7.6.0` | `7.6.x` | 不建议 | 这些版本仍要求 `PD/TiKV < 8.0.0` 且 `TiCDC < 8.0.0-alpha`。 |
| `v7.1.0 ~ v7.1.4` | `7.6.x` | 不建议 | 在滚动升级窗口中，旧实例仍会拒绝 `8.x` 的 PD、TiKV 或 peer TiCDC。 |
| `v7.5.0 ~ v7.5.1` | `7.6.x` | 不建议 | 在滚动升级窗口中，旧实例仍会拒绝 `8.x` 的 PD、TiKV 或 peer TiCDC。 |
| `v7.1.5 ~ v7.1.6` | `8.5.x` | 可以 | 从版本兼容性检查看，已经可以进入 `8.x` 版本的混合版本窗口。 |
| `v7.5.2 ~ v7.5.4` | `8.5.x` | 可以，但建议先升级到 `v7.5.5+` | 版本兼容性检查已放开，但与 `CheckStoreVersion` 失败后的重试和恢复处理相关的修复直到 `v7.5.5` 才补齐。 |
| `v7.5.5 ~ v7.5.7` | `8.5.x` | 可以 | 版本兼容性检查已放开，且已包含 `CheckStoreVersion` 失败后的恢复逻辑修复。 |
| `v8.0.0 ~ v8.1.x` | `8.5.x` | 可以 | 这些版本已将上限提升到 `< 10.0.0`。 |
| `v8.2.0 ~ v8.5.x` | `8.5.x` | 可以 | 除 `< 10.0.0` 上限外，还要求滚动窗口中的 PD/TiKV 版本不低于 `7.1.0-alpha`。 |

对于不建议直接与 `8.x` 滚动混跑的源版本，建议采用以下方式之一降低风险：

1. 先升级到已抬高版本上限的桥接版本，例如 `v7.1.5+` 或 `v7.5.2+`。
2. 如果无法先桥接到上述版本，避免旧 TiCDC 实例与 `8.x` 长时间共存，优先采用更接近停机切换或完整重启 TiCDC 的方式完成升级。

### 升级建议

对于旧架构 TiCDC，不建议在 TiDB 滚动升级期间持续运行 changefeed。升级到 `v8.5` 时，建议按以下顺序执行：

1. 暂停所有 changefeed。
2. 将 TiCDC 升级到 `v8.5`。
3. 将 TiDB 集群升级到 `v8.5`。
4. 待升级完成后恢复 changefeed。

如果目标 TiDB 版本高于 `v8.1.x`，必须先升级 TiCDC，再升级 TiDB 集群。

### 与滚动升级相关的运行时注意事项

- 从 `v7.5.5` 开始，TiCDC 修复了 `CheckStoreVersion` 失败后的重试与恢复处理问题。如果源版本为 `v7.5.2 ~ v7.5.4`，虽然版本兼容性检查允许进入 `8.x` 的混合版本窗口，但升级过程中仍建议重点关注 `resolved-ts`、`checkpoint` 和相关错误日志。
- 从 `v8.5.3` 开始，TiCDC 修复了因 store ID 与 store version 检查异常导致 `resolved-ts lag` 持续升高的问题。如果源版本为 `v8.5.0 ~ v8.5.2`，建议在升级前评估是否需要先升级到 `v8.5.3+`。
- 如果升级后日志中出现 `version is incompatible: TiKV ... is not supported, only support version less than 8.0.0` 一类报错，通常说明滚动升级窗口中仍存在未退出的旧版本 TiCDC 实例。此时需要优先确认所有 TiCDC 实例是否均已升级到目标版本。

## 命令行参数和配置文件兼容性

* TiCDC v4.0.0 中移除了 `ignore-txn-commit-ts`，添加了 `ignore-txn-start-ts`，使用 start_ts 过滤事务。
* TiCDC v4.0.2 中移除了 `db-dbs`/`db-tables`/`ignore-dbs`/`ignore-tables`，添加了 `rules`，使用新版的数据库和数据表过滤规则，详细语法参考[表库过滤](/table-filter.md)。
* 自 TiCDC v6.2.0 开始，`cdc cli` 将通过 TiCDC 的 Open API 直接与 TiCDC server 进行交互，而不再需要访问 PD。`cdc cli` 子命令中的 `--pd` 参数被废除，增加了 `--server` 参数，用于指定 TiCDC Server 地址。请使用 `--server` 参数替代 `--pd` 参数。
* 从 v6.4.0 开始，TiCDC 使用 Syncpoint 功能需要同步任务拥有下游集群的 `SYSTEM_VARIABLES_ADMIN` 或者 `SUPER` 权限。

## 兼容性问题处理

本节介绍了兼容性相关的问题。

### 使用 TiCDC v5.0.0-rc 版本的 `cdc cli` 工具操作 v4.0.x 集群导致不兼容问题

使用 TiCDC v5.0.0-rc 版本的 `cdc cli` 工具操作 v4.0.x 版本的 TiCDC 集群时，可能会遇到如下异常情况：

- 若 TiCDC 集群版本为 v4.0.8 或以下，使用 v5.0.0-rc 版本的 `cdc cli` 创建同步任务 changefeed 时，可能导致 TiCDC 集群陷入异常状态，导致同步卡住。
- 若 TiCDC 集群版本为 v4.0.9 或以上，使用 v5.0.0-rc 版本的 `cdc cli` 创建同步任务 changefeed，会导致 Old Value 和 Unified Sorter 特性被非预期地默认开启。

处理方案：

使用和 TiCDC 集群版本对应的 `cdc` 可执行文件进行如下操作：

1. 删除使用 v5.0.0-rc 版本创建的 changefeed，例如：`tiup cdc:v4.0.9 cli changefeed remove -c xxxx --pd=xxxxx --force`。
2. 如果 TiCDC 同步已经卡住，重启 TiCDC 集群，例如：`tiup cluster restart <cluster_name> -R cdc`。
3. 重新创建 changefeed，例如：`tiup cdc:v4.0.9 cli changefeed create --sink-uri=xxxx --pd=xxx`。

> **注意：**
>
> 上述问题仅在 `cdc cli` 的版本是 v5.0.0-rc 时存在。未来其他 v5.0.x 版本的 `cdc cli` 可以兼容 v4.0.x 版本的集群。

### `sort-dir` 及 `data-dir` 配置项的兼容性说明

`sort-dir` 配置项用于给 TiCDC 内部的排序器指定临时文件目录，其作用在各版本有过如下兼容性更改：

|  版本  |  `sort-engine` 的使用  |  说明   |  使用建议  |
|  :---  |    :---               |  :--    | :-- |
| v4.0.11 及之前的 v4.0 版本，v5.0.0-rc | 作为 changefeed 配置项，给 `file` sorter 和 `unified` Sorter 指定临时文件目录 | 在这些版本中，`file` sorter 和 `unified` sorter **均不是**正式功能 (GA)，不推荐在生产环境中使用。<br/><br/>如果有多个 changefeed 被配置使用了 `unified` 作为 `sort-engine`，那么实际使用的临时文件目录可能是任何一个 changefeed 的 `sort-dir` 配置，且每个 TiCDC 节点上使用的目录可能不一致。 | 不推荐在生产环境中使用 Unified Sorter |
| v4.0.12，v4.0.13，v5.0.0 及 v5.0.1 | 作为 changefeed 配置项或 `cdc server` 配置项 | 在默认情况下 changefeed 的 `sort-dir` 配置不会生效，而 `cdc server` 的 `sort-dir` 配置默认为 `/tmp/cdc_sort`。建议生产环境下仅配置 `cdc server` 的相关配置。<br/><br/>如果你使用 TiUP 部署 TiCDC，建议升级到最新的 TiUP 版本并在 TiCDC server 配置中设置 `sorter.sort-dir` 一项。<br/><br />在 v4.0.13、v5.0.0 和 v5.0.1 中 unified sorter 是默认开启的，如果要将集群升级至这些版本，请确保 TiCDC server 配置中的 `sorter.sort-dir` 已经被正确配置。| 需要通过 `cdc server` 命令行参数（或 TiUP）配置 `sort-dir` |
|  v4.0.14 及之后的 v4.0 版本，v5.0.3 及之后的 v5.0 版本，更新的版本  | `sort-dir` 被弃用，建议配置 `data-dir` |  `data-dir` 可以通过最新版本的 TiUP 进行配置。这些版本中 unified sorter 是默认开启的，升级时请确保 `data-dir` 已经被正确配置，否则将默认使用 `/tmp/cdc_data`。<br/><br/>如果该目录所在设备空间不足，有可能出现硬盘空间不足的问题。之前配置的 changefeed 的 `sort-dir` 配置将会失效。| 需要通过 `cdc server` 命令行参数（或 TiUP）配置 `data-dir` |
| v6.0.0 及之后版本 | `data-dir` 被用来存放 TiCDC 生成的临时文件  | 在该版本之后，TiCDC 默认采用 `db sorter` 作为内部的排序引擎，它使用 `data-dir` 作为磁盘目录。 | 需要通过 `cdc server` 命令行参数（或 TiUP）配置 `data-dir` |

### 全局临时表兼容性说明

TiCDC 从 v5.3.0 开始支持[全局临时表](/temporary-tables.md#全局临时表)。

你需要使用 TiCDC v5.3.0 及以上版本同步全局临时表到下游。低于该版本，会导致表定义错误。

如果 TiCDC 的上游集群包含全局临时表，下游集群也必须是 TiDB 5.3.0 及以上版本，否则同步报错。

### 向量数据类型兼容性说明 {#compatibility-with-vector-data-types}

从 v8.4.0 开始，TiCDC 支持同步包含[向量数据类型](/ai/reference/vector-search-data-types.md)的表到下游（实验特性）。

当下游为 Kafka 或者存储服务（如：Amazon S3、GCS、Azure Blob Storage 和 NFS）时，TiCDC 会将向量数据类型转为字符串类型进行写入。

当下游为不支持向量类型的 MySQL 兼容数据库时，涉及向量类型的 DDL 事件无法成功写入。在这种情况下，请在 `sink-url` 中添加配置参数 `has-vector-type=true`，然后 TiCDC 会将向量数据类型转为 `LONGTEXT` 类型进行写入。