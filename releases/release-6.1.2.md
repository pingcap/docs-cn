---
title: TiDB 6.1.2 Release Notes
summary: TiDB 6.1.2 发布，包括 TiDB、TiKV、Tools 和 Bug 修复。提升改进包括允许在一张表上同时设置数据放置规则和 TiFlash 副本。Bug 修复包括修复数据库级别的权限清理不正确的问题。
---

# TiDB 6.1.2 Release Notes

发版日期：2022 年 10 月 24 日

TiDB 版本：6.1.2

试用链接：[快速体验](https://docs.pingcap.com/zh/tidb/v6.1/quick-start-with-tidb) | [生产部署](https://docs.pingcap.com/zh/tidb/v6.1/production-deployment-using-tiup)

## 提升改进

+ TiDB

    - 允许在一张表上同时设置数据放置规则和 TiFlash 副本 [#37171](https://github.com/pingcap/tidb/issues/37171) @[lcwangchao](https://github.com/lcwangchao)

+ TiKV

    - 支持配置 `unreachable_backoff` 避免 Raftstore 发现某个 Peer 无法连接时广播过多消息 [#13054](https://github.com/tikv/tikv/issues/13054) @[5kbpers](https://github.com/5kbpers)
    - 支持将 RocksDB write stall 参数设置为比 flow control 流控阈值更小的值 [#13467](https://github.com/tikv/tikv/issues/13467) @[tabokie](https://github.com/tabokie)

+ Tools

    + TiDB Lightning

        - 增加 checksum 阶段可重试错误 (retryable error)，提升鲁棒性 [#37690](https://github.com/pingcap/tidb/issues/37690) @[D3Hunter](https://github.com/D3Hunter)

    + TiCDC

        - 采用批处理 resolved ts 的模式，提升 region worker 的性能 [#7078](https://github.com/pingcap/tiflow/issues/7078) @[sdojjy](https://github.com/sdojjy)

## Bug 修复

+ TiDB

    - 修复数据库级别的权限清理不正确的问题 [#38363](https://github.com/pingcap/tidb/issues/38363) @[dveeden](https://github.com/dveeden)
    - 修复 `SHOW CREATE PLACEMENT POLICY` 输出结果不正确的问题 [#37526](https://github.com/pingcap/tidb/issues/37526) @[xhebox](https://github.com/xhebox)
    - 修复了当某台 PD 宕机时，由于没有重试其他 PD 节点，导致查询表 `INFORMATION_SCHEMA.TIKV_REGION_STATUS` 时请求失败的问题 [#35708](https://github.com/pingcap/tidb/issues/35708) @[tangenta](https://github.com/tangenta)
    - 修复 `UNION` 运算符可能会非预期地返回空结果的问题 [#36903](https://github.com/pingcap/tidb/issues/36903) @[tiancaiamao](https://github.com/tiancaiamao)
    - 修复在 TiFlash 中为分区表开启动态模式时结果出错的问题 [#37254](https://github.com/pingcap/tidb/issues/37254) @[wshwsh12](https://github.com/wshwsh12)
    - 修复 Region 合并情况下 Region cache 没有及时被清理的问题 [#37141](https://github.com/pingcap/tidb/issues/37141) @[sticnarf](https://github.com/sticnarf)
    - 修复 KV 客户端发送不必要 ping 消息的问题 [#36861](https://github.com/pingcap/tidb/issues/36861) @[jackysp](https://github.com/jackysp)
    - 修复带 DML 算子的 `EXPLAIN ANALYZE` 语句可能在事务提交完成前返回结果的问题 [#37373](https://github.com/pingcap/tidb/issues/37373) @[cfzjywxk](https://github.com/cfzjywxk)
    - 修复当 `ORDER BY` 子句里包含关联子查询时与 `GROUP CONCAT` 一起执行可能会导致出错的问题 [#18216](https://github.com/pingcap/tidb/issues/18216) @[winoros](https://github.com/winoros)
    - 修复 `UPDATE` 语句中带公共表表达式 (CTE) 的情况下会报 `Can't find column` 的问题 [#35758](https://github.com/pingcap/tidb/issues/35758) @[AilinKid](https://github.com/AilinKid)
    - 修复某些情况下，`EXECUTE` 语句可能抛出非预期异常的问题 [#37187](https://github.com/pingcap/tidb/issues/37187) @[Reminiscent](https://github.com/Reminiscent)

+ TiKV

    - 修复因引入跨 Region 批量 snapshot 导致 snapshot 数据不完整的问题 [#13553](https://github.com/tikv/tikv/issues/13553) @[SpadeA-Tang](https://github.com/SpadeA-Tang)
    - 修复开启流量控制且显式设置 `level0_slowdown_trigger` 时出现 QPS 下降的问题 [#11424](https://github.com/tikv/tikv/issues/11424) @[Connor1996](https://github.com/Connor1996)
    - 修复 Web 身份提供程序 (web identity provider) 报错并失效后，自动恢复为默认提供程序 (default provider) 时出现权限拒绝的问题 [#13122](https://github.com/tikv/tikv/issues/13122) @[3pointer](https://github.com/3pointer)
    - 修复当有一个 TiKV 实例出现网络隔离时，一段时间内服务不可用问题 [#12966](https://github.com/tikv/tikv/issues/12966) @[cosven](https://github.com/cosven)

+ PD

    - 修复 Region tree 统计可能不准确的问题 [#5318](https://github.com/tikv/pd/issues/5318) @[rleungx](https://github.com/rleungx)
    - 修复 PD 可能没创建 TiFlash Learner 副本的问题 [#5401](https://github.com/tikv/pd/issues/5401) @[HunDunDM](https://github.com/HunDunDM)
    - 修复 PD 无法正确处理 dashboard 代理请求的问题 [#5321](https://github.com/tikv/pd/issues/5321) @[HunDunDM](https://github.com/HunDunDM)
    - 修复不健康的 Region 可能导致 PD panic 的问题 [#5491](https://github.com/tikv/pd/issues/5491) @[nolouch](https://github.com/nolouch)

+ TiFlash

    - 修复在大批量写入之后，I/O Limiter 可能错误地限制了读请求的 I/O 吞吐量，从而降低查询性能的问题 [#5801](https://github.com/pingcap/tiflash/issues/5801) @[JinheLin](https://github.com/JinheLin)
    - 修复取消查询时 window function 可能会导致 TiFlash 崩溃的问题 [#5814](https://github.com/pingcap/tiflash/issues/5814) @[SeaRise](https://github.com/SeaRise)
    - 修复使用包含 `NULL` 值的列创建主键时导致崩溃的问题 [#5859](https://github.com/pingcap/tiflash/issues/5859) @[JaySon-Huang](https://github.com/JaySon-Huang)

+ Tools

    + TiDB Lightning

        - 修复非法 metric 数值可能导致 TiDB Lightning panic 的问题 [#37338](https://github.com/pingcap/tidb/issues/37338) @[D3Hunter](https://github.com/D3Hunter)

    + TiDB Data Migration (DM)

        - 修复某些情况下，进入 sync unit 的任务中断导致的上游表结构信息丢失问题 [#7159](https://github.com/pingcap/tiflow/issues/7159) @[lance6716](https://github.com/lance6716)
        - 通过在保存 checkpoint 时拆分 SQL 语句解决大事务问题 [#5010](https://github.com/pingcap/tiflow/issues/5010) @[lance6716](https://github.com/lance6716)
        - 解决 Pre-Check 阶段 `INFORMATION_SCHEMA` 表需要 `SELECT` 权限的问题 [#7317](https://github.com/pingcap/tiflow/issues/7317) @[lance6716](https://github.com/lance6716)
        - 修复开启 fast/full validator 时 DM-worker 可能触发死锁问题 [#7241](https://github.com/pingcap/tiflow/issues/7241) @[buchuitoudegou](https://github.com/buchuitoudegou)
        - 修复 DM 报错 `Specified key was too long` 的问题 [#5315](https://github.com/pingcap/tiflow/issues/5315) @[lance6716](https://github.com/lance6716)
        - 修复数据同步过程中，latin1 字符集数据可能损坏的问题 [#7028](https://github.com/pingcap/tiflow/issues/7028) @[lance6716](https://github.com/lance6716)

    + TiCDC

        - 修复 cdc server 在尚未启动成功前收到 HTTP 请求导致 panic 的问题 [#6838](https://github.com/pingcap/tiflow/issues/6838) @[asddongmen](https://github.com/asddongmen)
        - 修复升级时日志数量过多的问题 [#7235](https://github.com/pingcap/tiflow/issues/7235) @[hi-rustin](https://github.com/Rustin170506)
        - 修复 redo log 中错误清理非当前 changefeed 日志文件的问题 [#6413](https://github.com/pingcap/tiflow/issues/6413) @[hi-rustin](https://github.com/Rustin170506)
        - 修复在一个 etcd 事务中提交太多数据导致 TiCDC 服务不可用问题 [#7131](https://github.com/pingcap/tiflow/issues/7131) @[hi-rustin](https://github.com/Rustin170506)
        - 修复 redo log 中不可重入 DDL 重复执行可能导致的数据不一致性问题 [#6927](https://github.com/pingcap/tiflow/issues/6927) @[hicqu](https://github.com/hicqu)

    + Backup & Restore (BR)

        - 修复在恢复时配置过高的 concurrency 会导致 Region 不均衡的问题 [#37549](https://github.com/pingcap/tidb/issues/37549) @[3pointer](https://github.com/3pointer)
        - 修复当外部存储的鉴权 Key 中存在某些特殊符号时，会导致备份恢复失败的问题 [#37469](https://github.com/pingcap/tidb/issues/37469) @[MoCuishle28](https://github.com/MoCuishle28)
