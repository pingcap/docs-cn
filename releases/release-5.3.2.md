---
title: TiDB 5.3.2 Release Notes
---

# TiDB 5.3.2 Release Notes

发版日期：2022 年 6 月 x 日

TiDB 版本：5.3.2

## 兼容性更改

+ TiDB

    - 修复当 auto ID 超出范围时，`REPLACE` 语句错误地修改了其它行的问题 [#29483](https://github.com/pingcap/tidb/issues/29483)

## 功能增强

## 提升改进

+ TiKV

    - 健康检查可以检测到无法正常工作的 Raftstore，使得 TiKV client 可以及时更新 Region Cache [#12398](https://github.com/tikv/tikv/issues/12398)
    - 通过将 leader 转让给 CDC observer 减少延迟抖动 [#12111](https://github.com/tikv/tikv/issues/12111)
    - 降低写入延迟，从 Raftstore 线程池中分离出 IO 线程池（默认不开启）。具体调优操作，请参考 [TiKV 线程池性能调优](https://docs.pingcap.com/zh/tidb/dev/tune-tikv-thread-performance) [#10540](https://github.com/tikv/tikv/issues/10540)
    - 在 Raft 日志垃圾回收模块中添加了更多监控指标，从而定位该模块中出现的性能问题 [#11374](https://github.com/tikv/tikv/issues/11374)

## Bug 修复

+ TiDB

    - 修复乐观事务下数据索引可能不一致的问题 [#30410](https://github.com/pingcap/tidb/issues/30410)
    - 修复当 SQL 语句中存在 JSON 类型列与 `CHAR` 类型列连接时，SQL 出错的问题 [#29401](https://github.com/pingcap/tidb/issues/29401)
    - 如果发生网络连接问题，TiDB 并不总是能正确释放断开的会话所持有的资源。该修复可以确保回滚打开的事务以及释放其他相关资源。[#34722](https://github.com/pingcap/tidb/issues/34722)
    - 修复由于多余数据导致 binlog 出错的问题 [#33608](https://github.com/pingcap/tidb/issues/33608)
    - 修复在 RC 隔离情况下 Plan Cache 启用时可能导致查询结果错误的问题 [#34447](https://github.com/pingcap/tidb/issues/34447)
    - 修复了在 MySQL binary 协议下，当 schema 变更后，执行 prepared statement 会导致会话崩溃的问题 [#33509](https://github.com/pingcap/tidb/issues/33509)
    - 修复对于新加入的分区，表属性 (table attributes) 无法被检索到，以及分区更新后，表的 range 信息不会被更新的问题 [#33929](https://github.com/pingcap/tidb/issues/33929)
    - 修复了查询 `INFORMATION_SCHEMA.CLUSTER_SLOW_QUERY` 表导致 TiDB 服务器 OOM 的问题，在 Grafana dashboard 中查看慢查询记录的时候可能会触发该问题 [#33893](https://github.com/pingcap/tidb/issues/33893)
    - 修复集群的 PD 节点被替换后一些 DDL 语句会卡住一段时间的问题 [#33908](https://github.com/pingcap/tidb/issues/33908)
    - 修复了集群从 4.0 版本升级后，为用户授予 `all` 权限时报错的问题 [#33588](https://github.com/pingcap/tidb/issues/33588)
    - 修复使用 left join 同时删除多张表数据时可能出现错误结果的问题 [#31321](https://github.com/pingcap/tidb/issues/31321)
    - 修复 TiDB 可能向 TiFlash 发送重复任务的问题 [#32814](https://github.com/pingcap/tidb/issues/32814)
    - 修复 TiDB 的后台 HTTP 服务可能没有正确关闭导致集群状态异常的问题 [#30571](https://github.com/pingcap/tidb/issues/30571)

+ TiKV

    - 修复了 PD Client 频繁重连的问题 [#12345](https://github.com/tikv/tikv/issues/12345)
    - 修复了 datetime 类型的数据包含小数部分和 'Z' 后缀导致检查报错的问题 [#12739](https://github.com/tikv/tikv/issues/12739)
    - 修复了对空字符串进行类型转换导致 TiKV panic 的问题 [#12673](https://github.com/tikv/tikv/issues/12673)
    - 修复了在悲观事务中使用 async-commit 导致重复的提交记录的问题 [#12615](https://github.com/tikv/tikv/issues/12615)
    - 修复了在使用 Follower Read 时，可能会报 invalid store ID 0 错误的问题 [#12478](https://github.com/tikv/tikv/issues/12478)
    - 修复了销毁 peer 和批量分裂 Region 之间的竞争导致的 TiKV panic [#12368](https://github.com/tikv/tikv/issues/12368)
    - 修复了在网络状况不好时，已成功提交的乐观事务可能返回 `Write Conflict` 的问题 [#34066](https://github.com/pingcap/tidb/issues/34066)
    - 修复待 merge 的 Region 无效会导致 TiKV panic 且非预期地销毁 peer 的问题 [#12232](https://github.com/tikv/tikv/issues/12232)
    - 修复旧信息造成 TiKV panic 的问题 [#12023](https://github.com/tikv/tikv/issues/12023)
    - 修复因内存统计指标溢出而造成的间歇性丢包和内存不足 (OOM) 的问题 [#12160](https://github.com/tikv/tikv/issues/12160)
    - 修复在 Ubuntu 18.04 下进行性能分析会造成 TiKV panic 的问题 [#9765](https://github.com/tikv/tikv/issues/9765)
    - 修复 tikv-ctl 对 `bad-ssts` 结果字符串进行错误匹配的问题 [#12329](https://github.com/tikv/tikv/issues/12329)
    - 修复 replica read 可能违反线性一致性的问题 [#12109](https://github.com/tikv/tikv/issues/12109)
    - 修复合并 Region 时因 target peer 被一个未进行初始化就被销毁的 peer 所替换，从而引起 TiKV panic 的问题 [#12048](https://github.com/tikv/tikv/issues/12048)
    - 修复 TiKV 运行 2 年以上可能 panic 的问题 [#11940](https://github.com/tikv/tikv/issues/11940)

+ TiFlash

    - 修复配置文件的一些问题 [#4093](https://github.com/pingcap/tiflash/issues/4093), [#4091](https://github.com/pingcap/tiflash/issues/4091)
    - 修复在设置副本数为 0 之后不能完全清理文件的问题 [#4414](https://github.com/pingcap/tiflash/issues/4414)
    - 修复在添加一些 `NOT NULL` 的列时报错的问题 [#4596](https://github.com/pingcap/tiflash/issues/4596)
    - 修复在重启过程中出现 `commit state jump backward` 错误的问题 [#2576](https://github.com/pingcap/tiflash/issues/2576)
    - 修复在大量 insert 后，TiFlash 副本可能会出现数据不一致的问题 [#4956](https://github.com/pingcap/tiflash/issues/4956)
    - 修复 MPP query 在出错时可能导致 task hang 住的问题 [#4229](https://github.com/pingcap/tiflash/issues/4229)
    - 修复 TiFlash 使用远程读时可能会误报集群 TiFlash 版本不一致的问题 [#3713](https://github.com/pingcap/tiflash/issues/3713)
    - 修复 MPP query 会随机碰到 grpc keepalive timeout 导致 query 失败的问题 [#4662](https://github.com/pingcap/tiflash/issues/4662)
    - 修复 MPP exchange receiver 如果出现大量重试可能会导致 query hang 住的问题 [#3473](https://github.com/pingcap/tiflash/pull/3473)
    - 修复 cast datetime as decimal 的结果出错的问题 [#4151](https://github.com/pingcap/tiflash/issues/4151)
    - 修复 cast float32 as decimal 是可能会出现结果不对的问题 [#3998](https://github.com/pingcap/tiflash/issues/3998)
    - 修复 `json_length` 对空字符串可能会报 `index out of bounds` 错误的问题 [#2705](https://github.com/pingcap/tiflash/issues/2705)
    - 修复极端情况下 decimal 比较可能会结果不对的问题 [#4942](https://github.com/pingcap/tiflash/pull/4942)
    - 修复 MPP query 在 join build 阶段出错可能导致 query hang 住的问题 [#4195](https://github.com/pingcap/tiflash/issues/4195)
    - 修复 sql 过滤条件为 `where string_col` 时，结果可能不对的问题 [#3447](https://github.com/pingcap/tiflash/issues/3447)
    - 修复 corner case 下面 cast string as double 结果和 TiDB 不一致的问题 [#3475](https://github.com/pingcap/tiflash/issues/3475)
    - 修复 cast string to datetime 时，microsecond 结果可能不对的问题 [#3556](https://github.com/pingcap/tiflash/issues/3556)

