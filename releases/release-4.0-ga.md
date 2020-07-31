---
title: TiDB 4.0 GA Release Notes
---

# TiDB 4.0 GA Release Notes

发版日期：2020 年 5 月 28 日

TiDB 版本：4.0.0

## 兼容性变化

* TiDB
    + 优化事务过大时系统的报错信息，方便排查问题 [#17219](https://github.com/pingcap/tidb/pull/17219)

* TiCDC
    + 优化 Changefeed 配置文件的结构，提升易用性 [#588](https://github.com/pingcap/ticdc/pull/588)
    + 新增 `ignore-txn-start-ts` 配置项，过滤事务时条件由原来的 `commit_ts` 改为 `start_ts` [#589](https://github.com/pingcap/ticdc/pull/589)

## 重点修复的 Bug

* TiKV
    + 修复 BR 备份时出现 `DefaultNotFound` 错误的问题 [#7937](https://github.com/tikv/tikv/pull/7937)
    + 修复 `ReadIndex` 因响应的数据包乱序而导致系统 panic 的问题 [#7930](https://github.com/tikv/tikv/pull/7930)
    + 修复 TiKV 重启后由于 snapshot 文件被错误删除导致系统 panic 的问题 [#7927](https://github.com/tikv/tikv/pull/7927)

* TiFlash
    + 修复因 Raft Admin Command 处理逻辑不正确，系统 panic 导致数据可能会丢失的问题

## 新功能

* TiDB
    + 新增 `committer-concurrency` 配置项，用于控制 retry commit 阶段的 goroutine 数量 [#16849](https://github.com/pingcap/tidb/pull/16849)
    + 支持 `show table partition regions` 语法 [#17294](https://github.com/pingcap/tidb/pull/17294)
    + 新增 `tmp-storage-quota` 配置项，用于限制 tidb-server 使用的临时磁盘空间 [#15700](https://github.com/pingcap/tidb/pull/15700)
    + 创建和更改表时新增检查分区表是否使用唯一前缀索引的功能 [#17213](https://github.com/pingcap/tidb/pull/17213)
    + 支持 `insert/replace into tbl_name partition`(`partition_name_list`) 语句 [#17313](https://github.com/pingcap/tidb/pull/17313)
    + Distinct 函数支持检查 collations 的值 [#17240](https://github.com/pingcap/tidb/pull/17240)
    + 哈希分区裁剪时支持 `is null` 过滤条件 [#17310](https://github.com/pingcap/tidb/pull/17310)
    + 分区表中支持 `admin check index`、`admin cleanup index` 和 `admin recover index` [#17392](https://github.com/pingcap/tidb/pull/17392) [#17405](https://github.com/pingcap/tidb/pull/17405) [#17317](https://github.com/pingcap/tidb/pull/17317)
    + 支持 `in` 表达式的范围分区裁剪 [#17320](https://github.com/pingcap/tidb/pull/17320)

* TiFlash
    + Learner 读取数据时通过 Lock CF 的 `min commit ts` 值过滤出符合条件的 TSO 对应的数据
    + 若 Timestamp 类型的值小于 `1970-01-01 00:00:00`，系统显式报错以避免计算结果出错
    + Search log 的正则表达式支持使用 flag 参数

* TiKV
    + 支持 `ascii_bin` 和 `latin1_bin` 编码的排序规则 [#7919](https://github.com/tikv/tikv/pull/7919)

* PD
    + 支持为内置的 TiDB Dashboard 指定反向代理资源前缀 [#2457](https://github.com/pingcap/pd/pull/2457)
    + PD client Region 相关接口支持返回 `pending peer` 和 `down peer` 的信息 [#2443](https://github.com/pingcap/pd/pull/2443)
    + 添加 `Direction of hotspot move leader`、`Direction of hotspot move peer` 和 `Hot cache read entry number` 等监控 [#2448](https://github.com/pingcap/pd/pull/2448)

* Tools
    + Backup & Restore (BR)
        - 支持备份与恢复 `Sequence` 和 `View` [#242](https://github.com/pingcap/br/pull/242)
    + TiCDC
        - 创建 `Changefeed` 时新增检查 Sink URI 的合法性 [#561](https://github.com/pingcap/ticdc/pull/561)
        - 系统启动时检查 PD 和 TiKV 版本是否符合系统要求 [#570](https://github.com/pingcap/ticdc/pull/570)
        - 支持同一个调度任务生成周期内可调度多张表 [#572](https://github.com/pingcap/ticdc/pull/572)
        - HTTP API 中增加节点角色的信息 [#591](https://github.com/pingcap/ticdc/pull/591)

## Bug 修复

* TiDB
    + 修复收发消息有不符合预期的超时，禁止合并发向 TiFlash 的消息 [#17307](https://github.com/pingcap/tidb/pull/17307)
    + 修复分区裁剪时未正确区分有符号/无符号整数的错误，并提高了性能 [#17230](https://github.com/pingcap/tidb/pull/17230)
    + 修复 3.1.1 升级到 4.0 时由于 `mysql.user` 表不兼容导致升级失败的问题 [#17300](https://github.com/pingcap/tidb/pull/17300)
    + 修复 `update` 语句分区选择不正确的问题 [#17305](https://github.com/pingcap/tidb/pull/17305)
    + 修复从 TiKV 收到未知错误消息时系统 panic 的问题 [#17380](https://github.com/pingcap/tidb/pull/17380)
    + 修复创建按 key 分区的分区表由于处理逻辑不正确导致系统 panic 的问题 [#17242](https://github.com/pingcap/tidb/pull/17242)
    + 修复某些情况下优化器处理逻辑不正确导致错误地选择 `Index Merge Join` 的问题 [#17365](https://github.com/pingcap/tidb/pull/17365)
    + 修复 Grafana 中 `SELECT` 语句的 `duration` 的监控指标不准确的问题 [#16561](https://github.com/pingcap/tidb/pull/16561)
    + 修复当系统发生错误时，GC 线程卡住的问题 [#16915](https://github.com/pingcap/tidb/pull/16915)
    + 修复当列的类型是 `Boolean` 时，由于 `UNIQUE` 约束比较的逻辑不正确导致输出结果不正确的问题 [#17306](https://github.com/pingcap/tidb/pull/17306)
    + 修复 `tidb_opt_agg_push_down` 开启且聚合函数下推分区表信息时，由于逻辑处理不正确导致系统 panic 的问题 [#17328](https://github.com/pingcap/tidb/pull/17328)
    + 修复某些情况下会访问已经发生故障的 TiKV 的问题 [#17342](https://github.com/pingcap/tidb/pull/17342)
    + 修复 `tidb.toml` 中的配置项 `isolation-read` 不生效时的问题 [#17322](https://github.com/pingcap/tidb/pull/17322)
    + 修复通过 `hint` 强制执行流式聚合时由于逻辑处理不正确导致输出的结果顺序不正确的问题 [#17347](https://github.com/pingcap/tidb/pull/17347)
    + 修复不同 `SQL_MODE` 时 `insert` 处理 `DIV` 的行为 [#17314](https://github.com/pingcap/tidb/pull/17314)

* TiFlash
    + 修复 Search log 功能正则表达式匹配的行为与其他组件不一致的问题
    + 默认关闭 Raft Compact Log Command 延迟处理的优化，避免节点大量写入数据时重启时间过长的问题
    + 修复部分场景因 TiDB 执行 `DROP DATABASE` 处理逻辑不正确导致系统启动不成功的问题
    + 修复采集 `Server_info` 中 CPU 信息方式与其他组件不一样的问题
    + 修复开启 `batch coprocessor` 功能时，执行 `Query` 报错 `Too Many Pings` 的问题
    + 修复 Dashboard 因未上报 `deploy path` 信息导致相关信息显示不正确的问题

* TiKV
    + 修复 BR 备份时出现 `DefaultNotFound` 错误的问题 [#7937](https://github.com/tikv/tikv/pull/7937)
    + 修复 `ReadIndex` 因响应的数据包乱序时导致系统 panic 问题 [#7930](https://github.com/tikv/tikv/pull/7930)
    + 修复读请求回调函数没有被调用，导致返回非预期错误的问题 [#7921](https://github.com/tikv/tikv/pull/7921)
    + 修复 TiKV 重启后由于 snapshot 文件被错误删除导致系统 panic 问题 [#7927](https://github.com/tikv/tikv/pull/7927)
    + 修复存储加密中因处理逻辑不正确导致 master key 无法轮转的问题 [#7898](https://github.com/tikv/tikv/pull/7898)
    + 修复开启存储加密后 snapshot 的 lock cf 文件在接收后未被加密的问题 [#7922](https://github.com/tikv/tikv/pull/7922)

* PD
    + 修复使用 pd-ctl 删除 `evict-leader-scheduler` 或者 `grant-leader-scheduler` 时报 404 错误的问题 [#2446](https://github.com/pingcap/pd/pull/2446)
    + 修复当存在 TiFlash 副本的时候，可能会导致 `presplit` 功能无法正常使用的问题 [#2447](https://github.com/pingcap/pd/pull/2447)

* Tools
    * BR
        + 修复从云存储恢复数据时因网络原因导致恢复失败的问题 [#298](https://github.com/pingcap/br/pull/298)
    * TiCDC
        + 修复若干因数据争用 (data race) 导致系统 panic 的问题 [#565](https://github.com/pingcap/ticdc/pull/565) [#566](https://github.com/pingcap/ticdc/pull/566)
        + 修复若干因处理逻辑不正确导致资源泄露或系统阻塞的问题 [#574](https://github.com/pingcap/ticdc/pull/574) [#586](https://github.com/pingcap/ticdc/pull/586)
        + 修复 CLI 因连接不上 PD 导致命令行阻塞的问题 [#579](https://github.com/pingcap/ticdc/pull/579)
