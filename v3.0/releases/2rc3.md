---
title: TiDB 2.0 RC3 Release Notes
category: Releases
aliases: ['/docs-cn/releases/2rc3/']
---

# TiDB 2.0 RC3 Release Notes

2018 年 3 月 23 日，TiDB 发布 2.0 RC3 版。该版本在 2.0 RC2 版的基础上，对 MySQL 兼容性、系统稳定性和优化器做了很多改进。

## TiDB

- 修复部分场景下 `MAX/MIN` 结果不正确的问题
- 修复部分场景下 `Sort Merge Join` 结果未按照 Join Key 有序的问题
- 修复边界条件下 `uint` 和 `int` 比较的错误
- 完善浮点数类型的长度和精度检查，提升 MySQL 兼容性
- 完善时间类型解析报错日志，添加更多错误信息
- 完善内存控制，新增对 `IndexLookupExecutor` 的内存统计
- 优化 `ADD INDEX` 的执行速度，部分场景下速度大幅度提升
- `GROUP BY` 子句为空时使用 Stream Aggregation 算子，提升速度
- 支持通过 `STRAIGHT_JOIN` 来关闭优化器的 `Join Reorder` 优化
- `ADMIN SHOW DDL JOBS` 输出更详细的 DDL 任务状态信息
- 支持 `ADMIN SHOW DDL JOB QUERIES` 查询当前正在运行的 DDL 任务的原始语句
- 支持 `ADMIN RECOVER INDEX` 命令，用于灾难恢复情况下修复索引数据
- `ADD INDEX` 操作变更为低优先级，降低对线上业务影响
- 支持参数为 JSON 类型的 `SUM/AVG` 等聚合函数
- 支持配置文件修改 `lower_case_table_names` 系统变量，用于支持 OGG 数据同步工具
- 提升对 Navicat 管理工具的兼容性
- 支持在 CRUD 操作中使用隐式的行 ID

## PD

- 支持 Region Merge，合并数据删除后产生的空 Region 或小 Region
- 添加副本时忽略有大量 pending peer 的节点，提升恢复副本及下线的速度
- 优化有大量空 Region 时产生的频繁调度问题
- 优化不同 label 中资源不均衡的场景中 leader balance 调度的速度
- 添加更多异常 Region 的统计

## TiKV

- 支持 Region Merge
- Raft snapshot 流程完成之后立刻通知 PD，加速调度
- 增加 Raw DeleteRange API
- 增加 GetMetric API
- 减缓 RocksDB sync 文件造成的 I/O 波动
- 优化了对 delete 掉数据的空间回收机制
- 完善数据恢复工具 `tikv-ctl`
- 解决了由于 snapshot 导致下线节点慢的问题
- Coprocessor 支持 streaming
- 支持 Readpool，`raw_get/get/batch_get` 性能提升 30%
- 支持配置 Coprocessor 请求超时时间
- Coprocessor 支持 streaming aggregation
- 上报 Region heartbeat 时携带时间信息
- 限制 snapshot 文件的空间使用，防止占用过多磁盘空间
- 对长时间不能选出 leader 的 Region 进行记录上报
- 加速启动阶段的垃圾清理工作
- 根据 compaction 事件及时更新对应 Region 的 size 信息
- 对 `scan lock` 的大小进行限制，防止请求超时
- 使用 `DeleteRange` 加速 Region 删除
- 支持在线修改 RocksDB 的参数