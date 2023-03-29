---
title: TiDB 4.0.1 Release Notes
---

# TiDB 4.0.1 Release Notes

发版日期：2020 年 6 月 12 日

TiDB 版本：4.0.1

## 新功能

+ TiKV

    - 添加 `--advertise-status-addr` 启动参数 [#8046](https://github.com/tikv/tikv/pull/8046)

+ PD

    - 为内嵌的 TiDB Dashboard 添加内部代理的支持 [#2511](https://github.com/pingcap/pd/pull/2511)
    - 添加对 PD 客户端自定义超时的设置 [#2509](https://github.com/pingcap/pd/pull/2509)

+ TiFlash

    - 支持 TiDB `new collation framework` 排序规则框架
    - 支持函数 `If`/`BitAnd/BitOr`/`BitXor/BitNot`/`Json_length` 下推到 TiFlash
    - 支持 TiFlash 中对于大事务的 Resolve Lock 逻辑

+ Tools

    - Backup & Restore (BR)

        * 增加启动时集群版本检查，避免 BR 和 TiDB 集群不兼容的问题 [#311](https://github.com/pingcap/br/pull/311)

## Bug 修复

+ TiKV

    - 修复日志中 `use-unified-pool` 配置打印不正确的问题 [#7946](https://github.com/tikv/tikv/pull/7946)
    - 修复 tikv-ctl 不支持相对路径的问题 [#7963](https://github.com/tikv/tikv/pull/7963)
    - 修复点查监控指标不准确的问题 [#8033](https://github.com/tikv/tikv/pull/8033)
    - 修复过时副本在网络隔离消除后不能销毁的问题 [#8006](https://github.com/tikv/tikv/pull/8006)
    - 修复 `read index` 可能过时的问题 [#8043](https://github.com/tikv/tikv/pull/8043)
    - 改善备份恢复文件操作的可靠性 [#7917](https://github.com/tikv/tikv/pull/7917)

+ PD

    - 防止某些场景下对 Placement Rules 的错误配置 [#2516](https://github.com/pingcap/pd/pull/2516)
    - 修复删除 Placement Rules 可能引发 panic 的问题 [#2515](https://github.com/pingcap/pd/pull/2515)
    - 修复当 Store 的已用空间为零时无法获取 Store 信息的 bug [#2474](https://github.com/pingcap/pd/pull/2474)

+ TiFlash

    - 修复 TiFlash 中 Bit 类型列的 Default Value 解析不正确的问题
    - 修复 TiFlash 对于 `1970-01-01 00:00:00 UTC` 在部分时区下计算错误的问题
