---
title: TiDB 6.1.2 Release Notes
---

# TiDB 6.1.2 Release Notes

发版日期：2022 年 xx 月 xx 日

TiDB 版本：6.1.2

## 兼容性变更

## 提升改进

+ TiDB

    <!--sql-infra **owner: @wjhuang2016**-->

    - (dup) 解决基于 SQL 的数据放置规则功能和构建 TiFlash 副本功能的冲突 [#37171](https://github.com/pingcap/tidb/issues/37171)

    <!--execution **owner: @zanmato1984**-->

    - (dup) 修复在 TiFlash 中为分区表开启动态模式时结果出错的问题 [#37254](https://github.com/pingcap/tidb/issues/37254)

    <!--transaction **owner: @cfzjywxk**-->

    - Reduce the risk of data race of SelectLock under parallel executors [#37141](https://github.com/pingcap/tidb/issues/37141)

    <!--planner **owner: @fixdb**-->

+ TiKV **owner: @ethercflow**

    - (dup) 支持配置 `unreachable_backoff` 避免 Raftstore 发现某个 Peer 无法连接时广播过多消息 [#13054](https://github.com/tikv/tikv/issues/13054)
    - (dup) 支持将 RocksDB write stall 参数设置为比 flow control 流控阈值更小的值 [#13467](https://github.com/tikv/tikv/issues/13467)

+ PD **owner: @nolouch**

+ TiFlash

<!--compute **owner: @zanmato1984**-->

<!--storage **owner: @flowbehappy**-->

+ Tools

    + TiDB Lightning **owner: @niubell**

    + TiDB Data Migration (DM) **owner: @niubell**

    + TiCDC **owner: @nongfushanquan**

    + Backup & Restore (BR) **owner: @3pointer**

    + Dumpling

## Bug 修复

+ TiDB

    <!--sql-infra **owner: @wjhuang2016**-->

    - (dup) 修复 `SHOW CREATE PLACEMENT POLICY` 输出结果不正确的问题 [#37526](https://github.com/pingcap/tidb/issues/37526)
    - (dup) 修复了当某台 PD 宕机时，由于没有重试其他 PD 节点，导致查询表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 时请求失败的问题 [#35708](https://github.com/pingcap/tidb/issues/35708)
    - (dup) 修复 `UNION` 运算符可能会非预期地返回空结果的问题 [#36903](https://github.com/pingcap/tidb/issues/36903)

    <!--execution **owner: @zanmato1984**-->

    - Database level privileges are cleaned up correctly [#38363](https://github.com/pingcap/tidb/issues/38363)

    <!--transaction **owner: @cfzjywxk**-->

    - (dup) 修复带 DML 算子的 `EXPLAIN ANALYZE` 语句可能在事务提交完成前返回结果的问题 [#37373](https://github.com/pingcap/tidb/issues/37373)

    <!--planner **owner: @fixdb**-->

    - Fix the issue that GROUP CONCAT with ORDER BY might fail when the ORDER BY clause contains a correlated subquery [#18216](https://github.com/pingcap/tidb/issues/18216)
    - (dup) 修复 `UPDATE` 语句中带公共表表达式 (CTE) 的情况下会报 `Can't find column` 的问题 [#35758](https://github.com/pingcap/tidb/issues/35758)
    - (dup) 修复某些情况下，`EXECUTE` 语句可能抛出非预期异常的问题 [#37187](https://github.com/pingcap/tidb/issues/37187)

+ TiKV **owner: @ethercflow**

    - (dup) 修复开启流量控制且显式设置 `level0_slowdown_trigger` 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424)
    - (dup) 修复 Web 身份提供程序 (web identity provider) 报错并失效后，自动恢复为默认提供程序 (default provider) 时出现权限拒绝的问题 [#13122](https://github.com/tikv/tikv/issues/13122)
    - (dup) 修复当有一个 TiKV 实例出现网络隔离时，一段时间内服务不可用问题 [#12966](https://github.com/tikv/tikv/issues/12966)

+ PD **owner: @nolouch**

    - Fix the issue that the statistics of the region tree may be not accurate [#5318](https://github.com/tikv/pd/issues/5318)
    - (dup) 修复 PD 可能没创建 TiFlash Learner 副本的问题 [#5401](https://github.com/tikv/pd/issues/5401)
    - (dup) 修复 PD 无法正确处理 dashboard 代理请求的问题 [#5321](https://github.com/tikv/pd/issues/5321)
    - (dup) 修复不健康的 Region 可能导致 PD panic 的问题 [#5491](https://github.com/tikv/pd/issues/5491)

+ TiFlash

    <!--compute **owner: @zanmato1984**-->

    - (dup) 修复取消查询时 window function 可能会导致 TiFlash 崩溃的问题 [#5814](https://github.com/pingcap/tiflash/issues/5814)

    <!--storage **owner: @flowbehappy**-->

    - (dup) 修复使用包含 `NULL` 值的列创建主键时导致崩溃的问题 [#5859](https://github.com/pingcap/tiflash/issues/5859)

+ Tools

    + TiDB Lightning **owner: @niubell**

    + TiDB Data Migration (DM) **owner: @niubell**

        - DM will try to persist upstream table structure from dump files when firstly switch to sync unit [#5010](https://github.com/pingcap/tiflow/issues/5010)
        - DM will try to persist upstream table structure from dump files when firstly switch to sync unit [#7159](https://github.com/pingcap/tiflow/issues/7159)
        - DM precheck no longer reports lacking privileges of INFORMATION_SCHEMA [#7317](https://github.com/pingcap/tiflow/issues/7317)
        - (dup) 修复 DM 报错 `Specified key was too long` 的问题 [#5315](https://github.com/pingcap/tiflow/issues/5315)
        - (dup) 修复数据同步过程中，latin1 字符集数据可能损坏的问题 [#7028](https://github.com/pingcap/tiflow/issues/7028)

    + TiCDC **owner: @nongfushanquan**

        - Fix a bug that may cause cdc server panic if it received a http request before cdc server fully started [#6838](https://github.com/pingcap/tiflow/issues/6838)
        - Change log level from info to debug for some logs to avoid too many logs [#7235](https://github.com/pingcap/tiflow/issues/7235)
        - Fix a bug that may cause changefeed's redo log files be deleted wrongly [#6413](https://github.com/pingcap/tiflow/issues/6413)
        - Fix a bug that may cause cdc unavaliable by commit too many operation in a etcd transaction [#7131](https://github.com/pingcap/tiflow/issues/7131)
        - Fix a bug which can lead inconsistency Change if non-reentrant DDLs can be executed twice [#6927](https://github.com/pingcap/tiflow/issues/6927)
        - Enhance the region worker's performance by handling the resolved ts in the batch mode [#7078](https://github.com/pingcap/tiflow/issues/7078)

    + Backup & Restore (BR) **owner: @3pointer**

        - (dup) 修复在恢复时配置过高的 concurrency 会导致 Region 不均衡的问题 [#37549](https://github.com/pingcap/tidb/issues/37549)
        - (dup) 修复当外部存储的鉴权 Key 中存在某些特殊符号时，会导致备份恢复失败的问题 [#37469](https://github.com/pingcap/tidb/issues/37469)

    + Dumpling
