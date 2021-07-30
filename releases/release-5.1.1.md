---
title: TiDB 5.1.1 Release Notes
---

# TiDB 5.1.1 Release Notes

发版日期：2021 年 7 月 30 日

TiDB 版本：5.1.1

## 兼容性更改

+ TiDB

    - 对于从 v4.0 升级至 v5.1 的集群，`tidb_multi_statement_mode` 的默认值从为 `OFF`。建议使用客户端库的多语句功能，参考 [`tidb_multi_statement_mode` 文档](/system-variables.md#tidb_multi_statement_mode-从-v4011-版本开始引入) [#25751](https://github.com/pingcap/tidb/pull/25751)
    - 将系统变量 `tidb_stmt_summary_max_stmt_count` 的默认值从 `200` 修改为 `3000` [#25874](https://github.com/pingcap/tidb/pull/25874)
    - 访问 `table_storage_stats` 表现在需要 `SUPER` 权限 [#26352](https://github.com/pingcap/tidb/pull/26352)
    - 访问 `information_schema.user_privileges` 表现在需要 `mysql.user` 上的 `SELECT` 权限来显示其他人的权限 [#26311](https://github.com/pingcap/tidb/pull/26311)
    - 访问 `information_schema.cluster_hardware` 现在需要 `CONFIG` 权限 [#26297](https://github.com/pingcap/tidb/pull/26297)
    - 访问 `information_schema.cluster_info` 表现在需要 `PROCESS` 权限 [#26297](https://github.com/pingcap/tidb/pull/26297)
    - 访问 `information_schema.cluster_load` 表现在需要 `PROCESS` 权限 [#26297](https://github.com/pingcap/tidb/pull/26297)
    - 访问 `information_schema.cluster_systeminfo` 表现在需要 `PROCESS` 权限 [#26297](https://github.com/pingcap/tidb/pull/26297)
    - 访问 `information_schema.cluster_log` 表现在需要 `PROCESS` 权限 [#26297](https://github.com/pingcap/tidb/pull/26297)
    - 访问 `information_schema.cluster_config` 表现在需要 `CONFIG` 权限 [#26150](https://github.com/pingcap/tidb/pull/26150)

## 功能增强

+ TiDB Dashboard

    - 新增 OIDC SSO 支持。通过设置兼容 OIDC 标准的 SSO 服务（例如 Okta、Auth0 等），用户可以在不输入 SQL 密码的情况下登录 TiDB Dashboard [#3883](https://github.com/tikv/pd/pull/3883)

+ TiFlash

    - 支持 DAG 请求中的 `HAVING()` 函数

## 改进提升

+ TiDB

    - Stale Read 成为正式功能 (GA)
    - 避免对 `paramMarker` 的分配以加快数据插入速度 [#26076](https://github.com/pingcap/tidb/pull/26076)
    - 支持稳定结果模式，使查询结果更稳定 [#25995](https://github.com/pingcap/tidb/pull/25995)
    - 支持将函数 `json_unquote()` 下推到 TiKV [#26265](https://github.com/pingcap/tidb/pull/26265)
    - 支持 MPP 查询的重试 [#26480](https://github.com/pingcap/tidb/pull/26480)
    - 对于 `point get` 或 `batch point get` 算子，在唯一索引写入过程中，将悲观锁 `LOCK` 记录转化为 `PUT` 记录 [#26225](https://github.com/pingcap/tidb/pull/26225)
    - 禁止使用 Stale 查询来进行创建视图 [#26225](https://github.com/pingcap/tidb/pull/26225)
    - 在 MPP 模式下彻底下推 `COUNT(DISTINCT)` 聚合函数 [#26194](https://github.com/pingcap/tidb/pull/26194)
    - 在发起 MPP 查询之前检查 TiFlash 的可用性 [#26192](https://github.com/pingcap/tidb/pull/26192)
    - 不允许将读时间戳设置为将来的时间 [#25763](https://github.com/pingcap/tidb/pull/25763)
    - 当聚合函数在 `EXPLAIN` 语句中不能被下推时打印警告日志 [#25737](https://github.com/pingcap/tidb/pull/25737)
    - 增加 `statements_summary_evicted` 表来记录集群的驱逐数量信息 [#25587](https://github.com/pingcap/tidb/pull/25587)
    - 提升内置函数 `str_to_date` 在格式指定器中 `%b/%M/%r/%T` 的 MySQL 兼容性 [#25768](https://github.com/pingcap/tidb/pull/25768)

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

    - 修复了 `tidb_enable_amend_pessimistic_txn=on` 下更改列类型可能出现数据丢失的问题 [#26203](https://github.com/pingcap/tidb/issues/26203)
    - 修复了 `last_day` 函数的行为在 SQL 模式下不兼容的问题 [#26001](https://github.com/pingcap/tidb/pull/26001)
    - 修复 `LIMIT` 位于窗口函数之上时可能出现的 panic 问题 [#25344](https://github.com/pingcap/tidb/issues/25344)
    - 修复了提交悲观事务可能会导致写冲突的问题 [#25964](https://github.com/pingcap/tidb/issues/25964)
    - 修复关联子查询中 Index Join 的结果不正确问题 [#25799](https://github.com/pingcap/tidb/issues/25799)
    - 修复了成功提交的悲观事务可能会报提交失败的问题 [#10468](https://github.com/tikv/tikv/issues/10468)
    - 修复在 `SET` 类型列上 Merge Join 结果不正确的问题 [#25669](https://github.com/pingcap/tidb/issues/25669)
    - 修复了在悲观事务中索引键值可能会被重复提交的问题 [#26359](https://github.com/pingcap/tidb/issues/26359)
    - 修复了优化器在定位分区时存在整数溢出的风险 [#26227](https://github.com/pingcap/tidb/issues/26227)
    - 修复了将 `DATE` 类型转换成时间戳时可能会写入无效值的问题 [#26292](https://github.com/pingcap/tidb/issues/26292)
    - 修复了 Coprocessor Cache 监控项未在 Grafana 中显示的问题 [#26338](https://github.com/pingcap/tidb/issues/26338)
    - 修复了遥测引起的干扰日志 [#25760](https://github.com/pingcap/tidb/issues/25760) [#25785](https://github.com/pingcap/tidb/issues/25785)
    - 修复了索引前缀的查询范围问题 [#26029](https://github.com/pingcap/tidb/issues/26029)
    - 修复了并发 truncate 同一个 partition 会导致 DDL 执行卡住的问题 [#26229](https://github.com/pingcap/tidb/issues/26229)
    - 修复了 `EMUN` 元素重复的问题 [#25955](https://github.com/pingcap/tidb/issues/25955)
    - 修复了 CTE 迭代器没有正确关闭的问题 [#26112](https://github.com/pingcap/tidb/issues/26112)
    - 修复 `LOAD DATA` 语句可能不正常导入非 utf8 数据的问题 [#25979](https://github.com/pingcap/tidb/issues/25979)
    - 修复在无符号整数列上使用窗口函数可能导致崩溃的问题 [#25956](https://github.com/pingcap/tidb/issues/25956)
    - 修复了清除 Async Commit 锁时可能会导致 TiDB panic 的问题 [#25778](https://github.com/pingcap/tidb/issues/25778)
    - 修复了 Stale Read 不完全兼容 `PREPARE` 语句的问题 [#25800](https://github.com/pingcap/tidb/pull/25800)
    - 修复 ODBC 类常数（例如 `{d '2020-01-01'}`）不能被用作表达式的问题 [#25531](https://github.com/pingcap/tidb/issues/25531)
    - 修复了单独运行 TiDB 时出现的一个错误 [#25555](https://github.com/pingcap/tidb/pull/25555)

+ TiKV

    - 修复特定平台上的 duration 计算可能崩溃的问题 [#10569](https://github.com/tikv/tikv/pull/10569)
    - 修复 Load Base Split 误用 `batch_get_command` 中未编码键的问题 [#10542](https://github.com/tikv/tikv/issues/10542)
    - 修复在线变更 `resolved-ts.advance-ts-interval` 配置无法立即生效的问题 [#10426](https://github.com/tikv/tikv/issues/10426)
    - 修复在超过 4 副本的罕见场景下 Follower 元信息损坏的问题 [#10225](https://github.com/tikv/tikv/issues/10225)
    - 修复开启加密后再次生成同样的 snapshot 会出现 panic 的问题 [#9786](https://github.com/tikv/tikv/issues/9786) [#10407](https://github.com/tikv/tikv/issues/10407)
    - 修正 `tikv_raftstore_hibernated_peer_state` 监控指标项 [#10330](https://github.com/tikv/tikv/issues/10330)
    - 修复 coprocessor 中 `json_unquote()` 函数错误的参数类型 [#10176](https://github.com/tikv/tikv/issues/10176)
    - 修复悲观事务中索引键被重复 commit 的问题 [#10468](https://github.com/tikv/tikv/issues/10468#issuecomment-869491061)
    - 修复 `ReadIndex` 请求在 leader 迁移后返回过期数据的问题 [#9351](https://github.com/tikv/tikv/issues/9351)

+ PD

    - 修复多个调度器产生调度冲突时无法生产预期调度的问题 [#3807](https://github.com/tikv/pd/issues/3807) [#3778](https://github.com/tikv/pd/issues/3778)
    - 修复当调度器被删除后，可能会再度运行的问题 [#2572](https://github.com/tikv/pd/issues/2572)

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
        - 修复了试图过早在 TiDB 中解锁的问题 [#2188](https://github.com/pingcap/ticdc/issues/2188)
        - 修复了表迁移后节点崩溃可能导致数据丢失的问题 [#2033](https://github.com/pingcap/ticdc/pull/2033)
        - 修复了 `changefeed update` 对 `--sort-dir` and `--start-ts` 的处理逻辑 [#1921](https://github.com/pingcap/ticdc/pull/1921)

    + Backup & Restore (BR)

        - 修复了错误计算待恢复数据的大小的问题 [#1270](https://github.com/pingcap/br/issues/1270)
        - 修复了从 cdclog 恢复数据时会遗漏 DDL event 的问题 [#870](https://github.com/pingcap/br/issues/870)

    + TiDB Lightning

        - 修复 TiDB Lightning 解析 Parquet 文件中 `DECIMAL` 类型数据失败的问题 [#1275](https://github.com/pingcap/br/pull/1275)
        - 修复了计算 key 区间时出现整数型溢出的问题 [#1291](https://github.com/pingcap/br/issues/1291) [#1290](https://github.com/pingcap/br/issues/1290)
