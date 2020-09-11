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

+ TiKV

    - 标准错误码支持生成 meta 文件 [#8619](https://github.com/tikv/tikv/pull/8619)
    - scan detail 中增加 tombstone 个数的 metrics [#8618](https://github.com/tikv/tikv/pull/8618)
    - 添加 rocksdb perf context metrics 面版 [#8467](https://github.com/tikv/tikv/pull/8467)


## 优化提升

+ TiDB

    - 

+ PD

    - 

+ TiKV

    - 

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

    - 

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
