# TiFlash 6.1 升级帮助

## 标准升级流程和操作
使用 TiUP 升级的用户请参[照用户手册](https://docs.pingcap.com/tidb/v6.0/upgrade-tidb-using-tiup)，以及[常见问题帮助](https://docs.pingcap.com/tidb/v6.0/upgrade-faq#upgrade-and-after-upgrade-faqs)。TiDB Cloud 用户请关注 Cloud 平台相关说明。
**友情提示**：生产环境用户升级请务必做好相关测试验证工作。

## 版本升降级兼容性说明和对应方法
本文列出升级前后具体功能模块的变化和带来的影响以及相关注意事项。

### 常见升级策略
不推荐跨大版本升级。请先升级至 5.4.x 或 6.0 之后再升级 6.1. 

### v4.x to v5.x 
v4 用户已经接近产品周期尾声，请及时尽早升级到主流版本。商业客户请联系售后和客服。

### v5.x to v6.0
6.0 作为非 LST 的产品发展里程碑，不会推出后续的 bug 修复版，建议商业客户慎用。尽可能使用 6.1 及之后的 LTS 版本。

### v5.x to v6.1

#### <a name="proxy"></a>TiFlash Proxy
TiFlash 在 6.1 版本将 Proxy 做了升级（与 TiKV 6.0 版本对齐）。该版本升级了 rocksdb 的版本，在升级过程中会自动将数据格式转换为新版本。
正常升级风险不大，但有特殊需要的用户请注意：6.1 降级到之前的任意低版本时，会无法解析新版的 rocksdb 配置，导致 TiFlash 重启失败。请事先做好升级验证工作并尽可能做好应急方案（确保 TiKV 数据可用，并预估重新同步数据可能造成的影响）。

##### 测试环境及特殊回退需求下的对策
确保相应表中 TiKV 副本的数据可用，强制缩容 TiFlash 节点，并重新同步数据。操作步骤详见[用户手册](https://docs.pingcap.com/tidb/stable/scale-tidb-using-tiup#scale-in-a-tiflash-cluster)。

#### Partition Table Dynamic Pruning 动态分区裁剪
如用户没有也不打算开启动态分区裁剪，可略过此段。
TiDB 6.1 全新安装会默认开启“动态分区裁剪”（Dynamic Pruning）， 6.0之前的版本则默认关闭。旧版本升级过程遵循用户已由设定，不会自动开启（相对的也不会关闭）此功能。升级完成之后如果打开此功能则需要由用户手动更新分区表的全局统计信息。请务必参考以下详细说明：[动态分区裁剪](https://github.com/pingcap/docs-cn/blob/3a24eb9e532b7281cbf16386ef4dccd0b4c95eaa/statistics.md#%E5%8A%A8%E6%80%81%E8%A3%81%E5%89%AA%E6%A8%A1%E5%BC%8F%E4%B8%8B%E7%9A%84%E5%88%86%E5%8C%BA%E8%A1%A8%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF)

#### TiFlash PageStorage
v6.1 默认升级到 PageStorage V3 版本（对应配置项参数 format_version=4）。新版本大幅降低了峰值写 IO 流量，在高并发或者重型查询情况下，TiFlash 数据 GC 带来的 CPU 占用高问题得到缓解。

1. 已有节点升级 v6.1 后，随着数据不断写入，旧版本的数据会逐步转换成新版本数据。
2. 通常不能做到完全的转换，这会带来一定系统开销（通常不影响业务）。用户也可以使用[手动 compact 命令](/sql-statements/sql-statement-alter-table-compact.md)触发一个 compaction 动作。在文件 Compaction 过程中，相关表的数据转成新版本格式。操作步骤如下。
  * 对每张有 TiFlash replica 的表执行 
     ```alter table <table_name> compact tiflash replica;```
  * 重启 TiFlash 节点
3. 具体实例跑的版本，可以在 grafana 对应监控查看（Tiflash summary → storage pool → global run mode 和 storage pool run mode）。
  * Global run mode 对应了全局的运行模式。
  * Storage pool run mode 对应了单表的运行模式。

##### 测试环境及特殊回退需求下的对策
确保相应表中 TiKV 副本的数据可用，删除 TiFlash 副本，之后重新生成 TiFlash 副本并同步数据。删除副本操作步骤详见[用户手册](https://docs.pingcap.com/zh/tidb/stable/use-tiflash)。

### v6.0 to v6.1

#### Partition Table Dynamic Pruning 动态分区裁剪

如用户关闭了分区表动态分区裁剪，可略过此段。
TiDB 6.0之后的全新安装会默认开启“动态分区裁剪”（Dynamic Pruning），旧版本升级过程遵循用户已由有设定，不会自动开启（相对的也不会关闭）此功能。6.0 版本用户在升级过程中不需要做任何特别操作，但本文提示用户，升级过程中将会发生自动的分区表全局统计信息的更新动作。

#### TiFlash PageStorage
同 `v5.x to v6.1`，请参照前文。

#### TiFlash Proxy
参见 v5.x to v6.1 [升级说明](#proxy)

