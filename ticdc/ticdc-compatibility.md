---
title: TiCDC 兼容性
summary: 了解 TiCDC 兼容性相关限制和问题处理。
---

# TiCDC 兼容性

本文介绍了与 TiCDC 有关的一系列兼容性问题及其处理方案。

<!--
## 组件兼容性矩阵

TODO

## 特性兼容性矩阵

TODO
-->

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

### 向量数据类型兼容性说明

从 v8.4.0 开始，TiCDC 支持同步包含[向量数据类型](/vector-search-data-types.md)的表到下游（实验特性）。

当下游为 Kafka 或者存储服务（如：Amazon S3、GCS、Azure Blob Storage 和 NFS）时，TiCDC 会将向量数据类型转为字符串类型进行写入。

当下游为不支持向量类型的 MySQL 兼容数据库时，涉及向量类型的 DDL 事件无法成功写入。在这种情况下，请在 `sink-url` 中添加配置参数 `has-vector-type=true`，然后 TiCDC 会将向量数据类型转为 `LONGTEXT` 类型进行写入。