---
title: TiFlash 升级帮助
summary: 了解升级 TiFlash 时的注意事项。
aliases: ['/zh/tidb/dev/tiflash-620-upgrade-guide']
---

# TiFlash 升级帮助

本文介绍 TiFlash 升级时功能模块的变化，以及推荐的应对方法。

如需了解标准升级流程，请参考如下文档：

- [使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md)
- [使用 TiDB Operator 升级 TiDB](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **注意：**
>
> - v6.2.0 新增了一项名为 [FastScan](/tiflash/use-fastscan.md) 的实验功能，该功能在 v7.0.0 GA。FastScan 在牺牲强一致性保证的前提下可以大幅提升扫表性能。
>
> - 不推荐跨主干版本升级包含 TiFlash 的 TiDB 集群，如从 v4.x 升级至 v6.x，请先升级至 v5.x，然后再升级至 v6.x。
>
> - v4.x. 已接近产品周期尾声，请尽早升级到 v5.x 及以上版本。具体的版本周期请参考 [TiDB 版本周期支持策略](https://pingcap.com/zh/tidb-release-support-policy)。
>
> - v6.0 作为非 LTS 版本，不会推出后续的 bug 修复版，请尽量使用 v6.1 及之后的 LTS 版本。

## 使用 TiUP 升级

如需将 TiFlash 从 v5.3.0 之前的版本升级到 v5.3.0 及之后的版本，必须进行 TiFlash 的停机升级。使用 TiUP 进行升级时：

- 如果 TiUP Cluster 版本大于或等于 v1.12.0，则无法进行 TiFlash 的停机升级。如果目标版本要求的 TiUP Cluster 版本大于或等于 v1.12.0，则建议先使用 `tiup cluster:v1.11.3 <subcommand>` 将 TiFlash 升级到某个中间版本，然后进行 TiDB 集群的在线升级，之后升级 TiUP 版本，最后对 TiDB 集群进行不停机升级至目标版本。
- 如果 TiUP Cluster 版本小于 v1.12.0，则执行以下步骤进行升级 TiFlash。

参考如下步骤，可以在确保其他组件正常运行的情况下，使用 TiUP 升级 TiFlash：

1. 关闭 TiFlash 实例：

    ```shell
    tiup cluster stop <cluster-name> -R tiflash
    ```

2. 使用 `--offline` 参数在不重启（只更新文件）的情况下升级集群：

    ```shell 
    tiup cluster upgrade <cluster-name> <version> --offline
    ```
    
    例如： 
    
    ```shell     
    tiup cluster upgrade <cluster-name> v5.3.0 --offline
    ```

3. 重新加载整个集群。此时，TiFlash 也会正常启动，无需额外操作。

    ```shell 
    tiup cluster reload <cluster-name>
    ```

## 从 v5.x 或 v6.0 升级至 v6.1

从 v5.x 或 v6.0 升级至 v6.1 时，需要注意 TiFlash Proxy 和动态分区裁剪功能的变化。

### TiFlash Proxy

TiFlash 在 v6.1.0 对 Proxy 做了升级（与 TiKV v6.0.0 对齐）。新的 Proxy 版本升级了 RocksDB 版本，在升级过程中会自动将数据格式转换为新版本。

正常升级时，不会有明显风险。如果特殊场景（如测试验证）需要降级，请注意，v6.1 降级到之前的任意版本时，会无法解析新版 RocksDB 配置，从而导致 TiFlash 重启失败。请做好升级验证工作，并尽可能准备应急方案。

**测试环境及特殊回退需求下的对策**

强制缩容 TiFlash 节点，并重新同步数据。操作步骤详见[缩容 TiFlash 节点](/scale-tidb-using-tiup.md#缩容-tiflash-节点)。

### 动态分区裁剪

如果你没有也不打算开启动[态分区裁剪](/partitioned-table.md#动态裁剪模式)，可略过本部分。

- TiDB v6.1 全新安装：默认开启动态分区裁剪 (Dynamic Pruning)。

- TiDB v6.0 及之前版本：默认关闭动态分区裁剪。旧版本升级遵循已有设定，不会自动开启（相对的也不会关闭）此功能。

    升级完成之后，如果要启用动态分区裁剪特性，请确保 `tidb_partition_prune_mode` 的值为 `dynamic`，并手动更新分区表的全局统计信息。关于如何手动更新统计信息，参见[动态裁剪模式](/partitioned-table.md#动态裁剪模式)。

## 从 v5.x 或 v6.0 升级至 v6.2

TiFlash 在 v6.2.0 将数据格式升级到 V3 版本，因此，从 v5.x 或 v6.0 升级至 v6.2 时，除了需要注意 [TiFlash Proxy](#tiflash-proxy) 和[动态分区裁剪](#动态分区裁剪)的变化，还应注意 PageStorage 变更数据版本带来的影响，具体如下：

- 已有节点升级 v6.2 后，随着数据不断写入，旧版本的数据会逐步转换成新版本数据。
- 新旧版本的数据格式不能做到完全的转换，这会带来一定系统开销（通常不影响业务，但需要注意）。因此升级完成后，建议使用 [`COMPACT` 命令](/sql-statements/sql-statement-alter-table-compact.md)触发数据整理 (Compaction) 将相关表的数据转成新版本格式。操作步骤如下：

    1. 对每张有 TiFlash 副本（replica）的表执行如下命令：

        ```sql
        ALTER TABLE <table_name> COMPACT tiflash replica;
        ```

    2. 重启 TiFlash 节点。

你可以在 Grafana 监控查看是否还有表使用旧的数据版本：**TiFlash-Summary** > **Storage Pool** > **Storage Pool Run Mode**

- Only V2：使用 PageStorage V2 的表数量（包括分区数）
- Only V3：使用 PageStorage V3 的表数量（包括分区数）
- Mix Mode：从 V2 迁移到 V3 的表数量（包括分区数）

**测试环境及特殊回退需求下的对策**

强制缩容 TiFlash 节点，并重新同步数据。操作步骤详见[缩容 TiFlash 节点](/scale-tidb-using-tiup.md#缩容-tiflash-节点)。

## 从 v6.1 升级至 v6.2

从 v6.1 升级至 v6.2 时，需要注意 PageStorage 变更数据版本带来的影响。具体请参考[从 v5.x 或 v6.0 升级至 v6.2](#从-v5x-或-v60-升级至-v62) 中关于 PageStorage 的描述。

## 从 v6.x 或 v7.x 升级至 v7.3，并且设置了 `storage.format_version = 5`

从 v7.3 开始，TiFlash 支持新的 DTFile 版本 V3（实验特性），可以将多个小文件合并成一个大文件，减少文件数量。DTFile 在 v7.3 的默认版本是 V2，如需使用 V3，可通过 [TiFlash 配置参数](/tiflash/tiflash-configuration.md) `storage.format_version = 5` 来设置。设置后，TiFlash 仍可以读 V2 版本的 DTFile，并且在后续的数据整理 (Compaction) 中会将这些 V2 版本的 DMFile 逐步重新写为 V3 版本的 DTFile。

在 TiFlash 升级到 v7.3 并且使用了 V3 版本的 DTFile 后，如需回退到之前的 TiFlash 版本，可以通过 DTTool 离线将 DTFile 重新写回 V2 版本，详见 [DTTool 迁移工具](/tiflash/tiflash-command-line-flags.md#dttool-migrate)。

## 从 v6.x 或 v7.x 升级至 v7.4 或以上版本

从 v7.4 开始，为了减少数据整理时产生的读、写放大，PageStorage V3 数据整理时逻辑进行了优化，导致底层部分存储文件名发生改动。因此，升级 TiFlash 到 v7.4 或以上版本后，不支持原地降级到之前的版本。

## 从 v7.x 升级至 v8.4 或以上版本

从 v8.4 开始，为了支持[向量搜索功能](/vector-search-index.md)，TiFlash 底层存储格式发生改动。因此，升级 TiFlash 到 v8.4 或以上版本后，不支持原地降级到之前的版本。

**测试环境及特殊回退需求下的对策**

如果在测试环境下或者其他有特殊回退需求的场景下，可以强制缩容 TiFlash 节点，并重新同步数据。操作步骤详见[缩容 TiFlash 节点](/scale-tidb-using-tiup.md#缩容-tiflash-节点)。
