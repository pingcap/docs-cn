---
title: TiCDC 兼容性
summary: 了解 TiCDC 兼容性相关限制和问题处理。
---

## 兼容性问题处理

本文介绍了兼容性相关的问题。

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
| v4.0.12，v4.0.13，v5.0.0 及 v5.0.1 | 作为 changefeed 配置项或 `cdc server` 配置项 | 在默认情况下 changefeed 的 `sort-dir` 配置不会生效，而 `cdc server` 的 `sort-dir` 配置默认为 `/tmp/cdc_sort`。建议生产环境下仅配置 `cdc server` 的相关配置。<br /><br />如果你使用 TiUP 部署 TiCDC，建议升级到最新的 TiUP 版本并在 TiCDC server 配置中设置 `sorter.sort-dir` 一项。<br /><br />在 v4.0.13、v5.0.0 和 v5.0.1 中 unified sorter 是默认开启的，如果要将集群升级至这些版本，请确保 TiCDC server 配置中的 `sorter.sort-dir` 已经被正确配置。| 需要通过 `cdc server` 命令行参数（或 TiUP）配置 `sort-dir` |
|  v4.0.14 及之后的 v4.0 版本，v5.0.3 及之后的 v5.0 版本，更新的版本  | `sort-dir` 被弃用，建议配置 `data-dir` |  `data-dir` 可以通过最新版本的 TiUP 进行配置。这些版本中 unified sorter 是默认开启的，升级时请确保 `data-dir` 已经被正确配置，否则将默认使用 `/tmp/cdc_data`。<br /><br />如果该目录所在设备空间不足，有可能出现硬盘空间不足的问题。之前配置的 changefeed 的 `sort-dir` 配置将会失效。| 需要通过 `cdc server` 命令行参数（或 TiUP）配置 `data-dir` |

### 全局临时表兼容性说明

TiCDC 从 v5.3.0 开始支持[全局临时表](/temporary-tables.md#全局临时表)。

你需要使用 TiCDC v5.3.0 及以上版本同步全局临时表到下游。低于该版本，会导致表定义错误。

如果 TiCDC 的上游集群包含全局临时表，下游集群也必须是 TiDB 5.3.0 及以上版本，否则同步报错。

