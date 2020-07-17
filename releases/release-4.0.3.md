---
title: TiDB 4.0.3 Release Notes
category: Releases
---

# TiDB 4.0.3 Release Notes

发版日期：2020 年 7 月 22 日

TiDB 版本：4.0.3

## 新功能

+ TiDB

    - 当 IndexHashJoin 遇到执行错误时，返回错误而不是空结果集 [#18586](https://github.com/pingcap/tidb/pull/18586)
    - 修复 GRPC transportReader 导致的反复异常 [#18562](https://github.com/pingcap/tidb/pull/18562)
    - 修复因为 green GCFix 不会扫描已下线 store 上的锁而可能导致数据不完整的问题 [#18550](https://github.com/pingcap/tidb/pull/18550)
    - 非只读语句不会使用 TiFlash 引擎 [#18534](https://github.com/pingcap/tidb/pull/18534)
    - 当查询连接异常时返回真实的错误信息 [#18500](https://github.com/pingcap/tidb/pull/18500)
    - DDL：修复非 repair mode 的 TiDB 节点不会重新读取修复的表元信息的错误 [#18323](https://github.com/pingcap/tidb/pull/18323)
    - 修复因为锁指向的 primary key 被其事务改删而导致的读写不一致的问题 [#18291](https://github.com/pingcap/tidb/pull/18291)
    - 修复数据落盘为正确生效导致的内存溢出 [#18288](https://github.com/pingcap/tidb/pull/18288)
    - 修复 REPLACE INTO 语句作用在包含生成列的表时会错误报错的问题 [#17907](https://github.com/pingcap/tidb/pull/17907)

+ TiKV



+ PD

+ Dashboard

   - 显示详细的 TiDB Dashboard 版本信息 [#679](https://github.com/pingcap-incubator/tidb-dashboard/pull/679)
   - 显示不受支持的浏览器或过时的浏览器的兼容性通知[#654](https://github.com/pingcap-incubator/tidb-dashboard/pull/654)
   - 支持在 SQL 语句分析页面搜索 [#658](https://github.com/pingcap-incubator/tidb-dashboard/pull/658)


+ TiFlash



+ Tools

    - Backup & Restore (BR)



    - Dumpling



+ TiCDC


## 改进提升

+ TiDB



+ TiKV

  - 添加了新的配置项 `backup.num-threads` 用语控制 backup 线程池的大小 [#8199](https://github.com/tikv/tikv/pull/8199)
  - 收取 snapshot 时不再发送 store heartbeat [#8136](https://github.com/tikv/tikv/pull/8136)
  - 支持动态调整 shared block cache 的大小 [#8232](https://github.com/tikv/tikv/pull/8232)

+ PD

  - 支持 json 格式日志 [#2565](https://github.com/pingcap/pd/pull/2565)

+ Dashboard

  - 优化keyviz中冷表的bucket合并 [#674](https://github.com/pingcap-incubator/tidb-dashboard/pull/674)
  - 重命名配置项disable-telemetry以使遥测更一致 [#684](https://github.com/pingcap-incubator/tidb-dashboard/pull/684)
  - 切换页面时显示进度条 [#661](https://github.com/pingcap-incubator/tidb-dashboard/pull/661)
  - 保证慢日志查询和日志查询行为的一致性，即使在空格存在的情况 [#682](https://github.com/pingcap-incubator/tidb-dashboard/pull/682)



+ TiFlash



+ Tools

     

## Bug 修复

+ TiDB



+ TiKV

  - 修复 merge 期间可能读到过期数据的问题 [#8113](https://github.com/tikv/tikv/pull/8113)
  - 修复聚合函数 min/max 下推到 TiKV 时，collation 不能正确工作的问题 [#8108](https://github.com/tikv/tikv/pull/8108)

+ PD

  - 修复如果服务器崩溃，创建 TSO 流可能会阻塞一段时间的问题 [#2648](https://github.com/pingcap/pd/pull/2648)
  - 修复`getSchedulers`可能导致数据争用的问题 [#2638](https://github.com/pingcap/pd/pull/2638)
  - 修复删除 `scheduler`时导致死锁的问题 [#2637](https://github.com/pingcap/pd/pull/2637)
  - 修复`balance-leader-scheduler`没有考虑`placement rule`的问题  [#2636](https://github.com/pingcap/pd/pull/2636)
  - 修复有时无法正确设置`safepoint `的问题，这可能会使 BR 和 dumpling 失败  [#2635](https://github.com/pingcap/pd/pull/2635)
  - 修复`hot region scheduler`中目标 store 选择错误的问题 [#2627](https://github.com/pingcap/pd/pull/2627)
  - 修复 PD Leader 切换时 TSO 请求可能花费太长时间的问题 [#2622](https://github.com/pingcap/pd/pull/2622)
  - 修复 PD Leader 切换后过期`scheduler`的问题 [#2608](https://github.com/pingcap/pd/pull/2608)
  - 修复了启用`placement rule`时，有时 region 的副本可能无法调整到最佳位置的问题 [#2605](https://github.com/pingcap/pd/pull/2605)
  - 修复了存储的部署路径不会随着部署目录移动而更新的问题 [#2600](https://github.com/pingcap/pd/pull/2600)
  - 修复了`store limit` 可能为零的问题 [#2588](https://github.com/pingcap/pd/pull/2588)

+ Dashboard

  - 修复 TiDB 扩容时的 TiDB 连接错误 [#689](https://github.com/pingcap-incubator/tidb-dashboard/pull/689)
  - 修复 TiFlash 实例未显示在日志搜索页面的问题 [#680](https://github.com/pingcap-incubator/tidb-dashboard/pull/680) 
  - 修复概况页面刷新之后 metris 会重置的问题 [#663](https://github.com/pingcap-incubator/tidb-dashboard/pull/663) 
  - 修复某些TLS方案中的连接问题 [#660](https://github.com/pingcap-incubator/tidb-dashboard/pull/660) 
  - 修复在某些情况下无法正确显示语言的下拉列表 [#677](https://github.com/pingcap-incubator/tidb-dashboard/pull/677)




+ TiFlash



+ Tools
