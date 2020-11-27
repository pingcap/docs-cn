---
title: 读写延迟增加
summary: 介绍读写延时增加、抖动时的排查思路，可能的原因和解决方法。
aliases: ['/docs-cn/dev/troubleshoot-cpu-issues/']
---

# 读写延迟增加

本文档介绍读写延迟增加、抖动时的排查思路，可能的原因和解决方法。

## 常见原因

### TiDB 执行计划不对导致延迟增高

查询语句的执行计划不稳定，偶尔执行计划选择错误的索引，导致查询延迟增加。

**现象：**

* 如果慢日志中输出了执行计划，可以直接查看执行计划。用 `select tidb_decode_plan('xxx...')` 语句可以解析出具体的执行计划。
* 监控中的 key 扫描异常升高；慢日志中 SQL 执行时间 `Scan Keys` 数目较大。
* SQL 执行时间相比于其他数据库（例如 MySQL）有较大差距。可以对比其他数据库执行计划，例如 `Join Order` 是否不同。

**可能的原因：**

* 统计信息不准确

**解决方案：**

* 更新统计信息
    * 手动 `analyze table`，配合 crontab 定期 `analyze`，维持统计信息准确度。
    * 自动 `auto analyze`，调低 `analyze ratio` 阈值，提高收集频次，并设置运行时间窗口。示例如下：
        * `set global tidb_auto_analyze_ratio=0.2;`
        * `set global tidb_auto_analyze_start_time='00:00 +0800';`
        * `set global tidb_auto_analyze_end_time='06:00 +0800';`
* 绑定执行计划
    * 修改业务 SQL，使用 `use index` 固定使用列上的索引。
    * 3.0 版本下，业务可以不用修改 SQL，使用 `create global binding` 创建 `force index` 的绑定 SQL。
    * 4.0 版本支持 SQL Plan Management，可以避免因执行计划不稳定导致的性能下降。

### PD 异常

**现象：**

监控中 PD TSO 的 **wait duration** 异常升高。**wait duration** 代表从开始等待 PD 返回，到等待结束的时间。

**可能的原因：**

* 磁盘问题。PD 所在的节点 I/O 被占满，排查是否有其他 I/O 高的组件与 PD 混合部署以及磁盘的健康情况，可通过监控 Grafana -> **disk performance** -> **latency** 和 **load** 等指标进行验证，必要时可以使用 fio 工具对盘进行检测，见案例 [case-292](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case292.md)。

* PD 之间的网络问题。PD 日志中有 `"lost the TCP streaming connection"`，排查 PD 之间网络是否有问题，可通过监控 Grafana -> **PD** -> **etcd** 的 **round trip** 来验证，见案例 [case-177](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case177.md)。

* 系统负载高，日志中能看到 `"server is likely overloaded"`，见案例 [case-214](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case214.md)。

* 选举不出 leader。PD 日志中有 `"lease is not expired"`，见 issues [https://github.com/etcd-io/etcd/issues/10355](https://github.com/etcd-io/etcd/issues/10355)。v3.0.x 版本和 v2.1.19 版本已解决该问题，见案例 [case-875](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case875.md)。

* 选举慢。Region 加载时间长，从 PD 日志中 `grep "regions cost"`（例如日志中可能是 `load 460927 regions cost 11.77099s`）, 如果出现秒级，则说明较慢，v3.0 版本可开启 Region Storage（设置 `use-region-storage` 为 `true`），该特性能极大缩短加载 Region 的时间，见案例 [case-429](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case429.md)。

* TiDB 与 PD 之间的网络问题，应排查网络相关情况。通过监控 Grafana -> **blackbox_exporter** -> **ping latency** 确定 TiDB 到 PD leader 的网络是否正常。

* PD 报 `FATAL` 错误，日志中有 `"range failed to find revision pair"`。v3.0.8 中已经解决问题，见 PR [https://github.com/pingcap/pd/pull/2040](https://github.com/pingcap/pd/pull/2040)。详情请参考案例 [case-947](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case947.md)。

* 使用 `/api/v1/regions` 接口时 Region 数量过多可能会导致 PD OOM。已于 v3.0.8 版本修复，见 [https://github.com/pingcap/pd/pull/1986](https://github.com/pingcap/pd/pull/1986)。

* 滚动升级的时候 PD OOM，gRPC 消息大小没限制，监控可看到 TCP InSegs 较大，已于 v3.0.6 版本修复，见 [https://github.com/pingcap/pd/pull/1952](https://github.com/pingcap/pd/pull/1952)。

* PD panic。请[提交 bug](https://github.com/tikv/pd/issues/new?labels=kind/bug&template=bug-report.md)。

* 其他原因，通过 `curl http://127.0.0.1:2379/debug/pprof/goroutine?debug=2` 抓取 goroutine，并[提交 bug](https://github.com/pingcap/pd/issues/new?labels=kind%2Fbug&template=bug-report.md)。

### TiKV 异常

**现象：**

监控中 **KV Cmd Duration** 异常升高。KV Cmd Duration 是 TiDB 发送请求给 TiKV 到收到回复的延迟。

**可能的原因：**

* 查看 gRPC duration。gRPC duration 是请求在 TiKV 端的总耗时。通过对比 TiKV 的 gRPC duration 以及 TiDB 中的 KV duration 可以发现潜在的网络问题。比如 gRPC duration 很短但是 TiDB 的 KV duration 显示很长，说明 TiDB 和 TiKV 之间网络延迟可能很高，或者 TiDB 和 TiKV 之间的网卡带宽被占满。

* TiKV 重启了导致重新选举
    * TiKV panic 之后又被 `systemd` 重新拉起正常运行，可以通过查看 TiKV 的日志来确认是否有 `panic`，这种情况属于非预期，需要报 bug。
    * 被第三者 `stop`/`kill`，被 `systemd` 重新拉起。查看 `dmesg` 和 `TiKV log` 确认原因。
    * TiKV 发生 OOM 导致重启了。
    * 动态调整 `THP` 导致 hung 住，见案例 [case-500](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case500.md)。

* 查看监控：Grafana -> **TiKV-details** -> **errors** 面板 `server is busy` 看到 TiKV RocksDB 出现 write stall 导致发生重新选举。

* TiKV 发生网络隔离导致重新选举。

* `block-cache` 配置太大导致 OOM，在监控 Grafana -> **TiKV-details** 选中对应的 instance 之后查看 RocksDB 的 `block cache size` 监控来确认是否是该问题。同时请检查 `[storage.block-cache] capacity = # "1GB"` 参数是否设置合理，默认情况下 TiKV 的 `block-cache` 设置为机器总内存的 `45%`。在容器化部署时需要显式指定该参数，因为 TiKV 获取的是物理机的内存，可能会超出单个 container 的内存限制。

* Coprocessor 收到大量大查询，返回的数据量太大，gRPC 发送速度跟不上 Coprocessor 向客户端输出数据的速度导致 OOM。可以通过检查监控：Grafana -> **TiKV-details** -> **coprocessor overview** 的 `response size` 是否超过 `network outbound` 流量来确认是否属于这种情况。

### TiKV 单线程瓶颈

TiKV 中存在一些单线程线程，可能会成为瓶颈。

* 单个 TiKV Region 过多导致单个 gRPC 线程成为瓶颈（查看 Grafana -> TiKV-details -> `Thread CPU/gRPC CPU Per Thread` 监控），v3.x 以上版本可以开启 Hibernate Region 特性来解决，见案例 [case-612](https://github.com/pingcap/tidb-map/blob/master/maps/diagnose-case-study/case612.md)。
* v3.0 之前版本 Raftstore 单线程或者 Apply 单线程到达瓶颈（Grafana -> TiKV-details -> `Thread CPU/raft store CPU 和 Async apply CPU` 超过 `80%`），可以选择扩容 TiKV（v2.x 版本）实例或者升级到多线程模型的 v3.x 版本。

### CPU Load 升高

**现象：**

CPU 资源使用到达瓶颈

**可能的原因：**

* 热点问题。
* 整体负载高，排查 TiDB 的 slow query 和 expensive query。对运行的 query 进行优化，如果缺索引就加索引，如果可以批量执行就批量执行。另一个方案是对集群进行扩容。

## 其它原因

### 集群维护

通常大多数的线上集群有 3 或 5 个 PD 节点，如果维护的主机上有 PD 组件，需要具体考虑节点是 leader 还是 follower，关闭 follower 对集群运行没有任何影响，关闭 leader 需要先切换，并在切换时有 3 秒左右的性能抖动。

### 少数派副本离线

TiDB 集群默认配置为 3 副本，每一个 Region 都会在集群中保存 3 份，它们之间通过 Raft 协议来选举 Leader 并同步数据。Raft 协议可以保证在数量小于副本数（注意：不是节点数）一半的节点挂掉或者隔离的情况下，仍然能够提供服务，并且不丢失任何数据。对于 3 副本集群，挂掉一个节点可能会导致性能抖动，可用性和正确性理论上不会受影响。

### 新增索引

由于创建索引在扫表回填索引的时候会消耗大量资源，甚至与一些频繁更新的字段会发生冲突导致正常业务受到影响。大表创建索引的过程往往会持续很长时间，所以要尽可能地平衡执行时间和集群性能之间的关系，比如选择非高频更新时间段。

**参数调整：**

目前主要使用 `tidb_ddl_reorg_worker_cnt` 和 `tidb_ddl_reorg_batch_size` 这两个参数来动态调整索引创建速度，通常来说它们的值越小对系统影响越小，但是执行时间越长。

一般情况下，先将值保持为默认的 `4` 和 `256` ，观察集群资源使用情况和响应速度，再逐渐调大 `tidb_ddl_reorg_worker_cnt` 参数来增加并发，观察监控如果系统没有发生明显的抖动，再逐渐调大 `tidb_ddl_reorg_batch_size` 参数，但如果索引涉及的列更新很频繁的话就会造成大量冲突造成失败重试。

另外还可以通过调整参数 `tidb_ddl_reorg_priority` 为 `PRIORITY_HIGH` 来让创建索引的任务保持高优先级来提升速度，但在通用 OLTP 系统上，一般建议保持默认。

### GC 压力大

TiDB 的事务的实现采用了 MVCC（多版本并发控制）机制，当新写入的数据覆盖旧的数据时，旧的数据不会被替换掉，而是与新写入的数据同时保留，并以时间戳来区分版本。GC 的任务便是清理不再需要的旧数据。

* Resolve Locks 阶段在 TiKV 一侧会产生大量的 scan_lock 请求，可以在 gRPC 相关的 metrics 中观察到。`scan_lock` 请求会对全部的 Region 调用。
* Delete Ranges 阶段会往 TiKV 发送少量的 `unsafe_destroy_range` 请求，也可能没有。可以在 gRPC 相关的 metrics 中和 GC 分类下的 GC tasks 中观察到。
* Do GC 阶段，默认每台 TiKV 会自动扫描本机上的 leader Region 并对每一个 leader 进行 GC，这一活动可以在 GC 分类下的 GC tasks 中观察到。
