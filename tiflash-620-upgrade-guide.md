---
title: TiFlash v6.2 升级帮助
summary: 了解升级 TiFlash 至 v6.2 时的注意事项。
---

# TiFlash v6.2 升级帮助

本文介绍从 TiFlash 低版本升级至 v6.2 时功能模块的变化，以及推荐的应对方法。

如需了解标准升级流程，请参考如下文档：

- [使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md)
- [使用 TiDB Operator 升级 TiDB](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

> **注意：**
>
> - v6.2.0 新增了一项名为 [FastScan](/tiflash/use-fastscan.md) 的实验功能。该实验功能在牺牲强一致性保证的前提下可以大幅提升扫表性能。相关实验功能的形态和使用方式有可能在后续版本中发生变化。
>
> - 不推荐跨主干版本升级包含 TiFlash 的 TiDB 集群，如从 v4.x 升级至 v6.x，请先升级至 v5.x，然后再升级至 v6.x。
>
> - v6.x. 已接近产品周期尾声，请尽早升级到 v7.x 及以上版本。具体的版本周期请参考 [TiDB 版本周期支持策略](https://pingkai.cn/tidb-release-support-policy)。
>
> - v6.0 作为非 LTS 版本，不会推出后续的 bug 修复版，请尽量使用 v6.1 及之后的 LTS 版本。
>
> - 若想将 TiFlash 从 v5.3.0 之前的版本升级到 v5.3.0 及之后的版本，必须进行 TiFlash 的停机升级。参考如下步骤，可以在确保其他组件正常运行的情况下升级 TiFlash：
>
>     - 关闭 TiFlash 实例：`tiup cluster stop <cluster-name> -R tiflash`
>     - 使用 `--offline` 参数在不重启（只更新文件）的情况下升级集群：`tiup cluster upgrade <cluster-name> <version> --offline`，例如 `tiup cluster upgrade <cluster-name> v5.3.0 --offline`
>     - reload 整个集群：`tiup cluster reload <cluster-name>`。此时，TiFlash 也会正常启动，无需额外操作。

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
