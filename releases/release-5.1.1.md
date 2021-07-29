---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 Release Notes

## 兼容性更改

## 功能增强

+ TiFlash

    - 支持 DAG 请求中的 `HAVING()` 函数

## 改进提升

+ TiKV

    - 提升 prewrite 请求的幂等性以减少不确定性错误的概率 [#10586](https://github.com/tikv/tikv/pull/10586)
    - 预防处理多个过期命令时出现栈溢出的风险 [#10502](https://github.com/tikv/tikv/pull/10502)
    - 不使用 Stale Read 请求的 `start_ts` 更新 `max_ts` 以避免过多不必要的 commit 请求重试 [#10451](https://github.com/tikv/tikv/pull/10451)
    - 分离处理读写的 ready 状态以减少读延迟 [#10592](https://github.com/tikv/tikv/pull/10592)
    - 降低 I/O 限流器开启后对数据导入速度的影响 [#10390](https://github.com/tikv/tikv/pull/10390)
    - 提升 Raft gRPC 连接的负载均衡 [#10495](https://github.com/tikv/tikv/pull/10495)

+ Tools

    + TiCDC

        - 移除 `file sorter` 文件排序器 [#2327](https://github.com/pingcap/ticdc/pull/2327)
        - 优化连接 PD 时缺少证书情况下的报错提示 [#2186](https://github.com/pingcap/ticdc/pull/2186)

    + TiDB Lightning

        - 为恢复 schema 添加重试机制 [#1294](https://github.com/pingcap/br/pull/1294)

    + Dumpling

        - 上游是 TiDB v3.x 集群时，使用 _tidb_rowid 来切分表以减少 TiDB 的内存使用 [#308](https://github.com/pingcap/dumpling/pull/308)
        - 减少访问数据库元信息的频率以提升性能和稳定性 [#315](https://github.com/pingcap/dumpling/pull/315)

## Bug 修复

+ TiKV

    - 修复某些平台上计时操作触发 panic 的问题 [#10569](https://github.com/tikv/tikv/pull/10569)
    - 修复 load-base-split 误用 `batch_get_command` 中未编码的键 [#10565](https://github.com/tikv/tikv/pull/10565)
    - 修复 `resolved-ts.advance-ts-interval` 在线配置无法立即起效的问题 [#10494](https://github.com/tikv/tikv/pull/10494)
    - 修复在超过 4 副本的罕见场景下 follower 元信息损坏的问题 [#10486](https://github.com/tikv/tikv/pull/10486)
    - 修复加密启用时两次构建快照触发 panic 的问题 [#10464](https://github.com/tikv/tikv/pull/10464)
    - 修正 `tikv_raftstore_hibernated_peer_state` 监控指标项 [#10432](https://github.com/tikv/tikv/pull/10432)
    - 修复 `json_unquote` 使用错误参数类型的问题 [#10428](https://github.com/tikv/tikv/pull/10428)
    - 修复悲观事务中索引键被重复 commit 的问题 [#10586](https://github.com/tikv/tikv/pull/10586)
    - 修复 `ReadIndex` 请求在 leader 迁移后返回过期数据的问题 [#10474](https://github.com/tikv/tikv/pull/10474)

+ TiFlash

    - 修复处理扫表任务时出现进程崩溃的潜在问题
    - 修复处理 DAG 请求时出现  `duplicated region` 报错的问题
    - 修复读负载高的情况下进程崩溃的问题
    - 修复执行 `DateFormat` 函数时出现进程崩溃的潜在问题
    - 修复处理 MPP 任务时出现内存泄漏的潜在问题
    - 修复执行 `COUNT` 或 `COUNT DISTINCT` 函数时出现非预期结果的问题
    - 修复多盘部署时出现数据无法恢复的潜在问题
    - 修复 TiDB Dashboard 无法正确显示 TiFlash 磁盘信息的问题
    - 修复析构 `SharedQueryBlockInputStream` 时出现进程崩溃的潜在问题
    - 修复析构 `MPPTask` 时出现进程崩溃的潜在问题
    - 修复通过快照同步数据后可能出现的数据不一致的问题

+ Tools

    + TiCDC

        - 修复对 new collation 的支持 [#2306](https://github.com/pingcap/ticdc/pull/2306)
        - 修复了一个运行中 panic 的问题 [#2300](https://github.com/pingcap/ticdc/pull/2300)
        - 修复了 DDL 执行中 owner 崩溃可能导致的 DDL 遗漏问题 [#2290](https://github.com/pingcap/ticdc/pull/2290)
        - 修复了试图过早在 TiDB 中 resolve lock [#2266](https://github.com/pingcap/ticdc/pull/2266)
        - 修复了表迁移后节点崩溃可能导致的数据丢失问题 [#2033](https://github.com/pingcap/ticdc/pull/2033)
        - 修复了 `changefeed update` 对 --sort-dir and --start-ts 的处理逻辑 [#1921](https://github.com/pingcap/ticdc/pull/1921)

    + Backup & Restore (BR)

        - 修复了对将要恢复的数据大小的错误计算 [#1285](https://github.com/pingcap/br/pull/1285)
        - 修复了从 cdclog 恢复时会遗漏 DDL 的问题 [#1094](https://github.com/pingcap/br/pull/1094)

    + TiDB Lightning

        - 修复了处理 Parquet 格式 `demical` 类型的问题 [#1272](https://github.com/pingcap/br/pull/1272)
        - 修复了计算 key 区间时的整形溢出问题 [#1294](https://github.com/pingcap/br/pull/1294)
