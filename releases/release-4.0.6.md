---
title: TiDB 4.0.6 Release Notes
---

# TiDB 4.0.6 Release Notes

发版日期：2020 年 9 月 15 日

TiDB 版本：4.0.6

## 兼容性变化

+ TiDB

    - 

## 新功能

+ TiDB

    - 


+ TiDB Dashboard

  - 添加 Query 编辑和执行页面 (实验性功能) [#713](https://github.com/pingcap-incubator/tidb-dashboard/pull/713)
  - 添加 Store 地理拓扑显示页面 [#719](https://github.com/pingcap-incubator/tidb-dashboard/pull/719)
  - 添加集群配置调整页面 (实验性功能) [#733](https://github.com/pingcap-incubator/tidb-dashboard/pull/733)
  - 支持共享当前 session [#741](https://github.com/pingcap-incubator/tidb-dashboard/pull/741)
  - 支持显示 SQL 语句分析中执行计划的数量 [#746](https://github.com/pingcap-incubator/tidb-dashboard/pull/746)

## 优化提升

+ TiDB

    - 

+ PD
    - 添加更多关于 store 和 region 心跳的 metrics [#2891](https://github.com/tikv/pd/pull/2891)
    - 升级 Dashboard 到 v2020.09.08.1 [#2928](https://github.com/pingcap/pd/pull/2928)
    - 回滚空间不足的阈值策略 [#2875](https://github.com/pingcap/pd/pull/2875)
    - 支持标准错误码 [#2918](https://github.com/tikv/pd/pull/2918) [#2911](https://github.com/tikv/pd/pull/2911) [#2913](https://github.com/tikv/pd/pull/2913) [#2915](https://github.com/tikv/pd/pull/2915) [#2912](https://github.com/tikv/pd/pull/2912) [#2907](https://github.com/tikv/pd/pull/2907) [#2906](https://github.com/tikv/pd/pull/2906) [#2903](https://github.com/tikv/pd/pull/2903) [#2806](https://github.com/tikv/pd/pull/2806) [#2900](https://github.com/tikv/pd/pull/2900) [#2902](https://github.com/tikv/pd/pull/2902)

    - 

+ TiKV

    - 优化 DropTable/TruncateTable 时导致的性能下降 [#8627](https://github.com/tikv/tikv/pull/8627)
    - 标准错误码支持生成 meta 文件 [#8619](https://github.com/tikv/tikv/pull/8619)
    - scan detail 中增加 tombstone 个数的 metrics [#8618](https://github.com/tikv/tikv/pull/8618)
    - 添加 rocksdb perf context metrics 面版 [#8467](https://github.com/tikv/tikv/pull/8467)

+ TiFlash

    - 

+ Tools

    + TiCDC

        - 

    + Backup & Restore (BR)

        - 

    + Dumpling

        - 

    + TiDB Lightning

        - 

## Bug 修复

+ TiDB

    - 

+ PD
    - 添加 `initial-cluster-token` 配置避免启动时 cluster 之间的通信 [#2922](https://github.com/pingcap/pd/pull/2922)
    - 修正自动模式下 store limit 的单位 [#2826](https://github.com/pingcap/pd/pull/2826)
    - 添加对于 scheduler 持久化时引发的错误的处理 [#2818](https://github.com/tikv/pd/pull/2818)
    - 修复 scheduler 的 http 接口的返回结果可能为空的问题 [#2871](https://github.com/tikv/pd/pull/2871) [#2874](https://github.com/tikv/pd/pull/2874)

+ TiKV

    - 修复开启 collation 时对于非 index 列统计信息估算错误的问题 [#8620](https://github.com/tikv/tikv/pull/8620)
    - 修复当迁移 region 时 green GC 可能错过 lock 的问题 [#8460](https://github.com/tikv/tikv/pull/8460)
    - 修复 CDC 不合理的 resloved TS 超时等待 [#8573](https://github.com/tikv/tikv/pull/8573)
    - 修复 TiKV 在极端繁忙下 conf change 可能 panic 的问题 [#8497](https://github.com/tikv/tikv/pull/8497)
    - 修复 PD client 和其他线程发起 PD sync requests 可能导致死锁的问题 [#8612](https://github.com/tikv/tikv/pull/8612)

+ TiFlash

    - 

+ Tools

    + Backup & Restore (BR)

        - 

    + Dumpling

        - 

    + TiCDC

        - 

    + TiDB Lightning

        - 
