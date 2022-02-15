---
title: TiDB 5.1.4 Release Note
---

# TiDB 5.1.4 Release Note

发版日期：2022 年 2 月 22 日

TiDB 版本：5.1.4

## 兼容性更改

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools

## 功能增强

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools

## 改进提升

+ TiDB

+ TiKV

+ PD

+ TiFlash

+ Tools
 + TiCDC
    
        - 为 changefeed 重启操作添加指数退避机制 [#3329](https://github.com/pingcap/tiflow/issues/3329)
        - 优化多表场景下的 checkpoint 同步延迟 [#3900](https://github.com/pingcap/tiflow/issues/3900) 
        - 增加观察 incremental scan 剩余时间的指标 [#2985](https://github.com/pingcap/tiflow/issues/2985) 
        - 降低 TiKV 遇到 OOM 错误时， TiCDC 打印 "EventFeed retry rate limited" 日志的频率 [#4006](https://github.com/pingcap/tiflow/issues/4006)
## Bug 修复

+ TiDB

+ TiKV
+ TiKV
    - 修复了 GC worker 繁忙后无法执行范围删除的问题 [#11903](https://github.com/tikv/tikv/issues/11903)
    - 避免删除 peer 造成潜在的高延迟 [#10210](https://github.com/tikv/tikv/issues/10210)
    - 修复了 region 没有数据时 `any_value` 函数结果错误 [#11735](https://github.com/tikv/tikv/issues/11735)
    - 修复了删除未初始化的副本可能会造成旧副本被重新创建的问题 [#10533](https://github.com/tikv/tikv/issues/10533)
    - 修复了在新选举但未能通知隔离了的 peer 后 prepare merge 造成元数据损坏的问题 [#11526](https://github.com/tikv/tikv/issues/11526)
    - 修复了协程执行太快时偶尔出现的死锁问题 [#11549](https://github.com/tikv/tikv/issues/11549)
    - 避免抓取火焰图时潜在的死锁和内存泄漏 [#11108](https://github.com/tikv/tikv/issues/11108)
    - 修复了悲观事务中重试 prewrite 有可能破坏数据一致性的问题 [#11187](https://github.com/tikv/tikv/issues/11187)
    - 修复了 resource-metering.enabled 配置不生效的问题 [#11235](https://github.com/tikv/tikv/issues/11235)
    - 修复了 resolved_ts 模块中的协程泄漏.  [#10965](https://github.com/tikv/tikv/issues/10965)
    - 避免低写入流量时误报 GC can not work 警告 [#9910](https://github.com/tikv/tikv/issues/9910)
+ PD

+ TiFlash

+ Tools

    + TiCDC

        - 修复 MySQL sink 在禁用 `batch-replace-enable` 参数时生成重复 `replace SQL` 语句的错误 [#4501](https://github.com/pingcap/tiflow/issues/4501)
        - 修复 `kv client cached regions` 指标可能为负数的问题 [#4300](https://github.com/pingcap/tiflow/issues/4300)
        - 修复当 `min.insync.replicas` 小于 `replication-factor` 时, TiCDC 无法发送消息的问题 [#3994](https://github.com/pingcap/tiflow/issues/3994)
        - 修复从 etcd 中删除 changefeed 信息时可能发生的 panic 问题 [#3128](https://github.com/pingcap/tiflow/issues/3128)
        - 修复 checkpointTs 非预计向前推进的问题 [#3545](https://github.com/pingcap/tiflow/issues/3545)
        - 修复 Table 调度时可能卡住 changefeed 的问题 [#4055](https://github.com/pingcap/tiflow/issues/4055)    
        - 修复 TiCDC 同步带特殊注释 DDL 时出现的语法错误问题 [#3755](https://github.com/pingcap/tiflow/issues/3755)
        - 修复 EtcdWorker 可能阻塞 owner 和 processor 的错误[#3750](https://github.com/pingcap/tiflow/issues/3750)    
        - 修复集群升级后处于 `stopped` 状态的 changefeed 自动恢复的问题 [#3473](https://github.com/pingcap/tiflow/issues/3473)    
        - 修复 TiCDC 与 TiDB amend 机制在数据类型上的兼容性问题 [#3793](https://github.com/pingcap/tiflow/issues/3793)     
        - 修复 TiCDC 默认值填充异常导致的数据不一致问题 [#3918](https://github.com/pingcap/tiflow/issues/3918) [#3929](https://github.com/pingcap/tiflow/issues/3929)
        - 修复当 PD leader 故障后转移到其他节点时 owner 卡住的问题 [#3615](https://github.com/pingcap/tiflow/issues/3615)    
        - 修复在 TiKV 部分节点故障后 TiCDC `kv client` 恢复时间过长的问题 [#3191](https://github.com/pingcap/tiflow/issues/3191) 

    + Backup & Restore (BR)

        + 修复 restoring 后可能出现的 region 不平衡的问题 [#30425](https://github.com/pingcap/tidb/issues/30425) [#31034](https://github.com/pingcap/tidb/issues/31034)
    
    + TiDB Lightning

      + 修复 s3 存储路径不存在时 Lightning 不报错的问题 [#28031](https://github.com/pingcap/tidb/issues/28031) [#30709](https://github.com/pingcap/tidb/issues/30709)
