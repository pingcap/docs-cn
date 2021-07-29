---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 Release Notes

## 兼容性更改

+ TiDB

    - 对于从 4.0 上升上来的集群来说，该 tidb_multi_statement_mode 的当前值是 OFF。推荐您替代使用客户端上的 multi-statement 的功能，可以参考文档的更多细节。[#25751](https://github.com/pingcap/tidb/pull/25751)
    - 访问表 table_storage_stats 现在需要 SUPER 权限。[#26352](https://github.com/pingcap/tidb/pull/26352)
    - 访问表 information_schema.user_privileges 现在需要 mysql.user 上的 SELECT 权限来显示其他人的权限。[#26311](https://github.com/pingcap/tidb/pull/26311)
    - 访问表 information_schema.cluster_hardware 现在需要 CONFIG 权限。
    - 访问表 information_schema.cluster_info 现在需要 PROCESS 权限。
    - 访问表 information_schema.cluster_load 现在需要 PROCESS 权限。
    - 访问表 information_schema.cluster_systeminfo 现在需要 PROCESS 权限。
    - 访问表 information_schema.cluster_log 现在需要 PROCESS 权限。[#26297](https://github.com/pingcap/tidb/pull/26297)
    - 访问表 information_schema.cluster_config 现在需要 CONFIG 权限。[#26150](https://github.com/pingcap/tidb/pull/26150)
    - 提升了 str_to_date 对 MySQL 的兼容性。[#25768](https://github.com/pingcap/tidb/pull/25768)

## 功能增强

+ TiDB Dashboard

    - 新增 OIDC SSO 支持。通过设置兼容 OIDC 标准的 SSO 服务（例如 Okta、Auth0 等），用户可以在不输入 SQL 密码的情况下登录 TiDB Dashboard

+ TiFlash

    - 支持 DAG 请求中的 `HAVING()` 函数

## 改进提升

+ TiDB

    - Stale Read 功能的 GA
    - 在插入数据时候，避免了对 paramMarker 的分配。[#26076](https://github.com/pingcap/tidb/pull/26076)
    - 优化器：支持了稳定结果顺序模式。[#25995](https://github.com/pingcap/tidb/pull/25995)
    - 开启了内置函数 json_unquote 下推到 TiKV。[#26265](https://github.com/pingcap/tidb/pull/26265)
    - 支持了 mpp 查询的重试。[#26480](https://github.com/pingcap/tidb/pull/26480)
    - 使用 point/batch point get 将索引键的 lock 记录更改为 put 记录来读取更新。[#26225](https://github.com/pingcap/tidb/pull/26225)
    - 禁止使用 stale 查询来进行创建视图。[#26225](https://github.com/pingcap/tidb/pull/26225)
    - 在 MPP 模式下彻底下推 count-distinct agg。[#26194](https://github.com/pingcap/tidb/pull/26194)
    - MPP：在发起 mpp 查询之前检查 tiflash 的可用性。[#26192](https://github.com/pingcap/tidb/pull/26192)
    - 扩大 tidb_stmt_summary_max_stmt_count 的值从 200 到 30000。[#25874](https://github.com/pingcap/tidb/pull/25874)
    - 不支持设置读时间戳为将来的时间。[#25763](https://github.com/pingcap/tidb/pull/25763)
    - 当 agg 函数在 explain 语句中不能下推时打印警告日志。[#25737](https://github.com/pingcap/tidb/pull/25737)
    - 增加 evicted count 的集群信息。[#25587](https://github.com/pingcap/tidb/pull/25587)

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

+ TiDB

    - 修复了 amend 事务在 modify column（需要 reorg）下且开关 tidb_enable_amend_pessimistic_txn=on 下的正确性。[#26273](https://github.com/pingcap/tidb/pull/26273)
    - 修复了 last_day 函数行为在 SQLmode 行为下的不兼容问题。[#26001](https://github.com/pingcap/tidb/pull/26001)
    - 确保 limit 输出不会多于他孩子节点的列数。[#25980](https://github.com/pingcap/tidb/pull/25980)
    - 修复了提交悲观事务可能会导致写冲突的问题。[#25973](https://github.com/pingcap/tidb/pull/25973)
    - 修复了优化器当构建 IndexJoin 时可以正确处理自查询中的其他条件。[#25819](https://github.com/pingcap/tidb/pull/25819)
    - 修复了成功提交的悲观事务可能会报提交失败的问题。[#25803](https://github.com/pingcap/tidb/pull/25803)
    - 修复了 merge join 中 set 类型的不正确结果。[#25695](https://github.com/pingcap/tidb/pull/25695)
    - 修复了在悲观事务中索引键值可能会被重复提交的问题。[#26482](https://github.com/pingcap/tidb/pull/26482)
    - 修复了优化器在定位分区时可能会有整数溢出的风险。[#26471](https://github.com/pingcap/tidb/pull/26471)
    - 修复了将 date 类型 cast 成 timestamp 时可能会写入无效值的问题。[#26395](https://github.com/pingcap/tidb/pull/26395)
    - 修复了 copt-cache metrics 会在 grafana 显示 hits/miss/evict 数量的问题。[#26344](https://github.com/pingcap/tidb/pull/26344)
    - 修复了 telemetry 引起的吵杂日志。[#26284](https://github.com/pingcap/tidb/pull/26284)
    - 修复了索引前缀的查询范围问题。[#26262](https://github.com/pingcap/tidb/pull/26262)
    - 修复了并发 truncate 共一个 partition 会导致 DDL 卡住的问题。[#26239](https://github.com/pingcap/tidb/pull/26239)
    - 修复了重复 enum 元素的问题。[#26202](https://github.com/pingcap/tidb/pull/26202)
    - 修复了 CTE 迭代器没有正确关闭的问题。[#26148](https://github.com/pingcap/tidb/pull/26148)
    - 修复了 load data 可能成功导入非 utf8 字符的数据。[#26144](https://github.com/pingcap/tidb/pull/26144)
    - 修复了窗口函数中 unsigned int 的错误。[#26027](https://github.com/pingcap/tidb/pull/26027)
    - 修复了 async-commit 清锁时可能会导致 TiDB panic 的问题。[#25862](https://github.com/pingcap/tidb/pull/25862)
    - 使 Stale Read 完全支持 prepare 语句。[#25800](https://github.com/pingcap/tidb/pull/25800)
    - 修复了 ODCB 风格的文本 (如 {d '2020-01-01'}...) 不能被作为表达式的问题。[#25578](https://github.com/pingcap/tidb/pull/25578)
    - 修复了单独运行 tidb 时候一些不必要的错误。[#25555](https://github.com/pingcap/tidb/pull/25555)

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
