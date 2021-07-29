---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 Release Notes

## 兼容性更改

## 功能增强

+ TiDB Dashboard

    - 新增 OIDC SSO 支持。通过设置兼容 OIDC 标准的 SSO 服务（例如 Okta、Auth0 等），用户可以在不输入 SQL 密码的情况下登录 TiDB Dashboard

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
        - 优化连接 PD 时缺少证书情况下的报错提示 [#1973](https://github.com/pingcap/ticdc/issues/1973)

    + TiDB Lightning

        - 为恢复 schema 添加重试机制 [#1294](https://github.com/pingcap/br/pull/1294)

    + Dumpling

        - 上游是 TiDB v3.x 集群时，使用 `_tidb_rowid` 来切分表以减少 TiDB 的内存使用 [#295](https://github.com/pingcap/dumpling/issues/295)
        - 减少访问数据库元信息的频率以提升性能和稳定性 [#315](https://github.com/pingcap/dumpling/pull/315)

## Bug 修复

+ TiKV

    - 修复特定平台上的 duration 计算可能崩溃的问题 [#10569](https://github.com/tikv/tikv/pull/10569)
    - 修复 Load Base Split 误用 `batch_get_command` 中未编码键的问题 [#10565](https://github.com/tikv/tikv/pull/10565)
    - 修复在线变更 `resolved-ts.advance-ts-interval` 配置无法立即生效的问题 [#10494](https://github.com/tikv/tikv/pull/10494)
    - 修复在超过 4 副本的罕见场景下 Follower 元信息损坏的问题 [#10486](https://github.com/tikv/tikv/pull/10486)
    - 修复开启加密后再次生成同样的 snapshot 会出现 panic 的问题 [#9786](https://github.com/tikv/tikv/issues/9786) [#10407](https://github.com/tikv/tikv/issues/10407)
    - 修正 `tikv_raftstore_hibernated_peer_state` 监控指标项 [#10432](https://github.com/tikv/tikv/pull/10432)
    - 修复 coprocessor 中 `json_unquote()` 函数错误的参数类型 [#10176](https://github.com/tikv/tikv/issues/10176)
    - 修复悲观事务中索引键被重复 commit 的问题 [#10586](https://github.com/tikv/tikv/pull/10586)
    - 修复 `ReadIndex` 请求在 leader 迁移后返回过期数据的问题 [#10474](https://github.com/tikv/tikv/pull/10474)

+ PD

    - 修复多个调度器产生调度冲突时无法生产预期调度的问题 [#3857](https://github.com/tikv/pd/pull/3857)
    - 修复当调度器被删除后，可能会再度运行的问题 [#3824](https://github.com/tikv/pd/pull/3824)

+ TiFlash

    - 修复执行扫表任务时出现进程崩溃的潜在问题
    - 修复处理 DAG 请求时出现 `duplicated region` 报错的问题
    - 修复读负载高的情况下进程崩溃的问题
    - 修复执行 `DateFormat` 函数时出现进程崩溃的潜在问题
    - 修复执行 MPP 任务时出现内存泄漏的潜在问题
    - 修复执行 `COUNT` 或 `COUNT DISTINCT` 函数时出现非预期结果的问题
    - 修复多盘部署时出现数据无法恢复的潜在问题
    - 修复 TiDB Dashboard 无法正确显示 TiFlash 磁盘信息的问题
    - 修复析构 `SharedQueryBlockInputStream` 时出现进程崩溃的潜在问题
    - 修复析构 `MPPTask` 时出现进程崩溃的潜在问题
    - 修复通过快照同步数据后可能出现的数据不一致的问题

+ Tools

    + TiCDC

        - 修复对 New Collation 的支持 [#2301](https://github.com/pingcap/ticdc/issues/2301)
        - 修复了运行时因非同步访问共享 map 可能导致 panic 的问题 [#2300](https://github.com/pingcap/ticdc/pull/2300)
        - 修复了 DDL 语句执行时 owner 崩溃可能导致的 DDL event 遗漏的问题 [#2290](https://github.com/pingcap/ticdc/pull/2290)
        - 修复了试图过早在 TiDB 中解锁的问题 [#2266](https://github.com/pingcap/ticdc/pull/2266)
        - 修复了表迁移后节点崩溃可能导致数据丢失的问题 [#2033](https://github.com/pingcap/ticdc/pull/2033)
        - 修复了 `changefeed update` 对 `--sort-dir` and `--start-ts` 的处理逻辑 [#1921](https://github.com/pingcap/ticdc/pull/1921)

    + Backup & Restore (BR)

        - 修复了错误计算待恢复数据的大小的问题 [#1285](https://github.com/pingcap/br/pull/1285)
        - 修复了从 cdclog 恢复数据时会遗漏 DDL event 的问题 [#1094](https://github.com/pingcap/br/pull/1094)

    + TiDB Lightning

        - 修复 TiDB Lightning 解析 Parquet 文件中 `DECIMAL` 类型数据失败的问题 [#1275](https://github.com/pingcap/br/pull/1275)
        - 修复了计算 key 区间时出现整数型溢出的问题 [#1291](https://github.com/pingcap/br/issues/1291) [#1290](https://github.com/pingcap/br/issues/1290)
