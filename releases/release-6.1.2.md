---
title: TiDB 6.1.2 Release Notes
---

# TiDB 6.1.2 Release Notes

发版日期：2022 年 xx 月 xx 日

TiDB 版本：6.1.2

## 兼容性变更

## 提升改进

+ TiDB **TW: @TomShawn**

    <!--sql-infra **owner: @wjhuang2016**-->

    - 允许在一张表上同时设置数据放置规则和 TiFlash 副本 [#37171](https://github.com/pingcap/tidb/issues/37171)

    <!--execution **owner: @zanmato1984**-->

    <!--transaction **owner: @cfzjywxk**-->

    <!--planner **owner: @fixdb**-->

+ TiKV **owner: @ethercflow TW: @Oreoxmt**

    - (dup) 支持配置 `unreachable_backoff` 避免 Raftstore 发现某个 Peer 无法连接时广播过多消息 [#13054](https://github.com/tikv/tikv/issues/13054)
    - (dup) 支持将 RocksDB write stall 参数设置为比 flow control 流控阈值更小的值 [#13467](https://github.com/tikv/tikv/issues/13467)

+ PD **owner: @nolouch TW: @Oreoxmt**

+ TiFlash

<!--compute **owner: @zanmato1984**-->

<!--storage **owner: @flowbehappy**-->

+ Tools

    + TiDB Lightning **owner: @niubell TW: @shichun-0415**

        - 增加 checksum 阶段可重试错误 (retryable error)，提升鲁棒性 [#37690](https://github.com/pingcap/tidb/issues/37690)

    + TiDB Data Migration (DM) **owner: @niubell**

    + TiCDC **owner: @nongfushanquan**

    + Backup & Restore (BR) **owner: @3pointer**

    + Dumpling

## Bug 修复

+ TiDB **TW: @TomShawn**

    <!--sql-infra **owner: @wjhuang2016**-->

    - 修复数据库级别的权限清理不正确的问题 [#38363](https://github.com/pingcap/tidb/issues/38363)
    - (dup) 修复 `SHOW CREATE PLACEMENT POLICY` 输出结果不正确的问题 [#37526](https://github.com/pingcap/tidb/issues/37526)
    - (dup) 修复了当某台 PD 宕机时，由于没有重试其他 PD 节点，导致查询表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 时请求失败的问题 [#35708](https://github.com/pingcap/tidb/issues/35708)
    - (dup) 修复 `UNION` 运算符可能会非预期地返回空结果的问题 [#36903](https://github.com/pingcap/tidb/issues/36903)

    <!--execution **owner: @zanmato1984**-->

    - (dup) 修复在 TiFlash 中为分区表开启动态模式时结果出错的问题 [#37254](https://github.com/pingcap/tidb/issues/37254)

    <!--transaction **owner: @cfzjywxk**-->

    - 修复 Region 合并情况下 Region cache 没有及时被清理的问题 [#37141](https://github.com/pingcap/tidb/issues/37141)
    - 修复 KV 客户端发送不必要 ping 消息的问题 [#36861](https://github.com/pingcap/tidb/issues/36861)
    - (dup) 修复带 DML 算子的 `EXPLAIN ANALYZE` 语句可能在事务提交完成前返回结果的问题 [#37373](https://github.com/pingcap/tidb/issues/37373)

    <!--planner **owner: @fixdb**-->

    - 修复当 `ORDER BY` 子句里包含关联子查询时与 `GROUP CONCAT` 一起执行可能会导致出错的问题 [#18216](https://github.com/pingcap/tidb/issues/18216)
    - (dup) 修复 `UPDATE` 语句中带公共表表达式 (CTE) 的情况下会报 `Can't find column` 的问题 [#35758](https://github.com/pingcap/tidb/issues/35758)
    - (dup) 修复某些情况下，`EXECUTE` 语句可能抛出非预期异常的问题 [#37187](https://github.com/pingcap/tidb/issues/37187)

+ TiKV **owner: @ethercflow TW: @Oreoxmt**

    - 修复因引入跨 Region 批量 snapshot 导致 snapshot 数据不完整的问题 [#13553](https://github.com/tikv/tikv/issues/13553)
    - (dup) 修复开启流量控制且显式设置 `level0_slowdown_trigger` 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424)
    - (dup) 修复 Web 身份提供程序 (web identity provider) 报错并失效后，自动恢复为默认提供程序 (default provider) 时出现权限拒绝的问题 [#13122](https://github.com/tikv/tikv/issues/13122)
    - (dup) 修复当有一个 TiKV 实例出现网络隔离时，一段时间内服务不可用问题 [#12966](https://github.com/tikv/tikv/issues/12966)

+ PD **owner: @nolouch TW: @Oreoxmt**

    - 修复 Region tree 统计可能不准确的问题 [#5318](https://github.com/tikv/pd/issues/5318)
    - (dup) 修复 PD 可能没创建 TiFlash Learner 副本的问题 [#5401](https://github.com/tikv/pd/issues/5401)
    - (dup) 修复 PD 无法正确处理 dashboard 代理请求的问题 [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) 修复不健康的 Region 可能导致 PD panic 的问题 [#5491](https://github.com/tikv/pd/issues/5491)

+ TiFlash **TW: @Oreoxmt**

    <!--compute **owner: @zanmato1984**-->

    - 修复在大批量写入之后，I/O Limiter 可能错误地限制了读请求的 I/O 吞吐量，从而降低查询性能的问题 [#5801](https://github.com/pingcap/tiflash/issues/5801)
    - (dup) 修复取消查询时 window function 可能会导致 TiFlash 崩溃的问题 [#5814](https://github.com/pingcap/tiflash/issues/5814)

    <!--storage **owner: @flowbehappy**-->

    - (dup) 修复使用包含 `NULL` 值的列创建主键时导致崩溃的问题 [#5859](https://github.com/pingcap/tiflash/issues/5859)

+ Tools

    + TiDB Lightning **owner: @niubell TW: @shichun-0415**

        - 修复非法 metric 数值可能导致 TiDB Lightning panic 的问题 [#37338](https://github.com/pingcap/tidb/issues/37338)

    + TiDB Data Migration (DM) **owner: @niubell TW: @shichun-0415**

        - 修复某些情况下，进入 sync unit 的任务中断导致的上游表结构信息丢失问题 [#7159](https://github.com/pingcap/tiflow/issues/7159)
        - 通过在保存 checkpoint 时拆分 SQL 语句解决大事务问题 [#5010](https://github.com/pingcap/tiflow/issues/5010)
        - 解决 Pre-Check 阶段 `INFORMATION_SCHEMA` 表需要 `SELECT` 权限的问题 [#7317](https://github.com/pingcap/tiflow/issues/7317)
        - 修复开启 fast/full validator 时 DM-worker 可能触发死锁问题 [#7241](https://github.com/pingcap/tiflow/issues/7241)
        - (dup) 修复 DM 报错 `Specified key was too long` 的问题 [#5315](https://github.com/pingcap/tiflow/issues/5315)
        - (dup) 修复数据同步过程中，latin1 字符集数据可能损坏的问题 [#7028](https://github.com/pingcap/tiflow/issues/7028)

    + TiCDC **owner: @nongfushanquan TW: @hfxsd**

        - 修复 cdc server 在尚未启动成功前收到 HTTP 请求导致 panic 的问题 [#6838](https://github.com/pingcap/tiflow/issues/6838)
        - 修复升级时日志数量过多的问题 [#7235](https://github.com/pingcap/tiflow/issues/7235)
        - 修复 redo log 中错误清理非当前 changefeed 日志文件的问题 [#6413](https://github.com/pingcap/tiflow/issues/6413)
        - 修复在一个 etcd 事务中提交太多数据导致 TiCDC 服务不可用问题 [#7131](https://github.com/pingcap/tiflow/issues/7131)
        - 修复 redo log 中 不可重入 DDL 重复执行可能导致的数据不一致性问题 [#6927](https://github.com/pingcap/tiflow/issues/6927)
        - 采用批处理 resolved ts 的模式，提升 region worker 的性能 [#7078](https://github.com/pingcap/tiflow/issues/7078)

    + Backup & Restore (BR) **owner: @3pointer TW: @shichun-0415**

        - (dup) 修复在恢复时配置过高的 concurrency 会导致 Region 不均衡的问题 [#37549](https://github.com/pingcap/tidb/issues/37549)
        - (dup) 修复当外部存储的鉴权 Key 中存在某些特殊符号时，会导致备份恢复失败的问题 [#37469](https://github.com/pingcap/tidb/issues/37469)

    + Dumpling
