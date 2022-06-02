---
title: TiFlash v6.1.0 升级帮助
summary: 了解升级 TiFlash 至 v6.1.0 时的注意事项。
---

# TiFlash v6.1.0 升级帮助

本文主要介绍 TiFlash 升级至 v6.1.0 时功能模块变化带来的影响，以及推荐的应对方法。

如需了解标准升级流程，请参考如下文档：

- [使用 TiUP 升级 TiDB](/upgrade-tidb-using-tiup.md)
- [使用 TiDB Operator 升级 TiDB](https://docs.pingcap.com/zh/tidb-in-kubernetes/stable/upgrade-a-tidb-cluster)

## 升级策略

 不推荐跨大版本升级。请先升级至 v5.4.x 或 v6.0.0，然后再升级至 v6.1.0。

### 升级 v4.x.x 至 v5.x.x

v4.x.x 已近品周期尾声，请尽早升级到主流版本。商业客户请联系售后和客服。

### 升级 v5.x.x 至 v6.0.0

v6.0.0 作为非 LTS 版本，不会推出后续的 bug 修复版，建议商业客户慎用。尽可能使用 v6.1.0 及之后的 LTS 版本。

### 升级 v5.x.x 至 v6.1.0

#### TiFlash Proxy

TiFlash 在 v6.1.0 对 Proxy 做了升级（与 TiKV v6.0.0 对齐）。该版本升级了 RocksDB 版本，在升级过程中会自动将数据格式转换为新版本。

正常升级时，不会有明显风险，但是，如果你有特殊需求，请注意，v6.1.0 降级到之前的任意版本时，会无法解析新版 RocksDB 配置，从而导致 TiFlash 重启失败。请做好升级验证工作，并尽可能准备应急方案。

##### 测试环境及特殊回退需求下的对策

强制缩容 TiFlash 节点，并重新同步数据。操作步骤详见[缩容 TiFlash 节点](/scale-tidb-using-tiup.md#缩容-tiflash-节点)。

#### 动态分区裁剪

如果你没有也不打算开启动态分区裁剪，可略过本部分。

- TiDB v6.1.0 全新安装：默认开启动态分区裁剪（Dynamic Pruning）。

- TiDB v6.0.0 及之前版本：默认关闭动态分区裁剪。旧版本升级遵循用户已有设定，不会自动开启（相对的也不会关闭）此功能。

    升级完成之后，如果要启用动态分区裁剪特性，需要手动更新分区表的全局统计信息。关于如何手动更新统计信息，参见[动态裁剪模式](/partitioned-table.md#动态裁剪模式)。

#### TiFlash PageStorage

v6.1.0 默认升级到 PageStorage V3 版本（对应配置项参数 format_version=4）。新版本大幅降低了峰值写 IO 流量，在高并发或者重型查询情况下，TiFlash 数据 GC 带来的 CPU 占用高问题得到缓解。

- 已有节点升级 v6.1.0 后，随着数据不断写入，旧版本的数据会逐步转换成新版本数据。
- 不能做到完全的转换，这会带来一定系统开销（通常不影响业务，但需要请用户提起注意）。你也可以使用[手动 compact 命令](/sql-statements/sql-statement-alter-table-compact.md)触发一个 compaction 动作。在 compaction 过程中，相关表的数据转成新版本格式。操作步骤如下：

    - 对每张有 TiFlash 副本（replica）的表执行如下命令：

     ```
     alter table <table_name> compact tiflash replica;
     ```

    - 重启 TiFlash 节点。

具体表运行的数据版本，可以在 Grafana 对应监控查看（Tiflash summary → storage pool → Storage Pool Run Mode）。

##### 测试环境及特殊回退需求下的对策

强制缩容 TiFlash 节点，并重新同步数据。操作步骤详见[缩容 TiFlash 节点](/scale-tidb-using-tiup.md#缩容-tiflash-节点)。

### 升级 v6.0.0 至 v6.1.0

#### 动态分区裁剪

如用户你关闭了分区表动态分区裁剪，可略过本部分。

TiDB v6.0.0 之后的全新安装会默认开启动态分区裁剪（Dynamic Pruning），旧版本升级遵循用户已有设定，不会自动开启（相对的也不会关闭）此功能。

如果你使用的是 TiDB 6.0.0，在升级过程中，不需要做任何特别操作，但是注意，升级过程中，分区表全局统计信息将会自动更新。

#### TiFlash PageStorage

参考升级 v5.x.x 至 v6.1.0 中 [TiFlash PageStorage](#tiflash-pagestorage) 的描述。

#### TiFlash Proxy

参考升级 v5.x.x 至 v6.1.0 中 [TiFlash Proxy](#tiflash-pagestorage) 的描述。
