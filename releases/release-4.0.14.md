---
title: TiDB 4.0.14 Release Notes
---

# TiDB 4.0.14 Release Notes

发版日期：2021 年 7 月 22 日

TiDB 版本：4.0.14

## 兼容性更改

+ TiKV

    - 修改 merge-check-tick-interval 的默认值为 2 来加快 merge 速度 [#9676](https://github.com/tikv/tikv/pull/9676)

## 功能增强

+ TiKV

    - 添加待 pending pd heartbeat 统计以定位 pd 线程变慢的问题 [#10008](https://github.com/tikv/tikv/pull/10008)
    - 支持 vritual-host 风格的地址来让 BR 兼容类 S3 储存 [#10242](https://github.com/tikv/tikv/pull/10242)

## 改进提升

+ TiKV

    - 关闭 TiKV 时，优先关闭 status server 来确保客户端可以正确检测关闭状态 [#10504](https://github.com/tikv/tikv/pull/10504)
    - 响应过期副本的消息来确保其被及时清除 [#10400](https://github.com/tikv/tikv/pull/10400)
    - 限制 CDC 的内存使用避免 OOM [#10147](https://github.com/tikv/tikv/pull/10147)
    - 当 region 大小太大时，使用均匀分裂来加快分裂速度 [#10275](https://github.com/tikv/tikv/pull/10275)

## Bug 修复

+ TiKV

    - 性能统计时容忍时间倒退避免 panic [#10572](https://github.com/tikv/tikv/pull/10572)
    - 修复 double 转 double 时对符号的错误处理 [#10532](https://github.com/tikv/tikv/pull/10532)
    - 修复 panic 退出有时报错信息会丢失的问题 [#10488](https://github.com/tikv/tikv/pull/10488)
    - 修复开启加密情况下重新生成同样 snapshot 会 panic 的问题 [#10462](https://github.com/tikv/tikv/pull/10462)
    - 修复 json_unquote 中错误的参数类型 [#10425](https://github.com/tikv/tikv/pull/10425)
    - 滚动重启时跳过清除回调以避免在高冲突下破坏事务一致 [#10395](https://github.com/tikv/tikv/pull/10395)
    - 修复 backup 线程泄漏 [#10360](https://github.com/tikv/tikv/pull/10360)
    - 修复 split 和创建新 region 冲突时可能会损坏 metadata 的问题 [#9584](https://github.com/tikv/tikv/pull/9584)
    - 修复特定情况下 region 心跳会导致 TiKV 不进行 split 的问题 [#10274](https://github.com/tikv/tikv/pull/10274)
    - 修复 CM Sketch 格式不一致导致的统计信息错误问题 [#10433](https://github.com/tikv/tikv/pull/10433)
    - 修复 apply wait duration 的错误统计 [#9966](https://github.com/tikv/tikv/pull/9966)
    - 修复使用 titan 时 delete_files_in_range 以后可能会产生 "Missing Blob" 报错的问题 [#10232](https://github.com/tikv/tikv/pull/10232)

+ TiFlash

    - 修复编译 DAG 请求时出现进程崩溃的潜在问题
    - 修复读负载高的情况下进程崩溃的问题
    - 修复因 split 失败而不断重启的问题
    - 修复无法删除 Delta 历史数据的潜在问题
    - 修复并发复制共享 Delta 索引导致结果错误的问题
    - 修复当存在数据缺失的情况下 TiFlash 无法启动的问题
    - 修复旧的 dm 文件无法被自动清理的问题
    - 修复 SUBSTRING 函数包含特殊参数时引起进程崩溃的潜在问题
    - 修复 INT 类型转换为 TIME 类型时产生错误结果的问题
