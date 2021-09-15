---
title: TiDB 5.0.4 Release Notes
---

# TiDB 5.0.4 Release Notes

发版日期：2021 年 9 月 27 日

TiDB 版本：5.0.4

## 兼容性更改

## 功能增强

+ TiKV

    - 支持动态修改 CDC 配置 [#10685](https://github.com/tikv/tikv/pull/10685)

+ TiFlash

    - 支持 `HAVING()` 函数
    - 支持 `DATE()` 函数
    - 为 Grafana 面板增加每个实例的写入吞吐

## 提升改进

+ TiKV

    - 读写 Ready 操作分离处理以减少读操作时延。 [#10620](https://github.com/tikv/tikv/pull/10620)
    - 减少 resolved ts 消息大小以节省网络带宽。 [#10678](https://github.com/tikv/tikv/pull/10678)
    - 当 slogger 线程过载且队列已满时，删除日志而不是阻塞线程。 [#10864](https://github.com/tikv/tikv/pull/10864)
    - 慢日志只考虑处理请求所花费的时间。[#10864](https://github.com/tikv/tikv/pull/10864)
    - 使预写尽可能具有幂等性，以减少出现未确定错误的机会。 [#10587](https://github.com/tikv/tikv/pull/10587)
    - 避免在低写入流量下出现错误的“GC 无法工作”警报。 [#10662](https://github.com/tikv/tikv/pull/10662)
    - 从 BR 或 Lightning 本地后端恢复的数据库现在更小，备份时应与原始集群大小匹配。 [#10643](https://github.com/tikv/tikv/pull/10643)
    - 确保 Panic 信息刷新到日志 [#10487](https://github.com/tikv/tikv/pull/10487)

+ PD

    - 在 placement rule 开启时并且 Region 拥有 down/pending 副本时，PD 会保证留下健康副本[#4073](https://github.com/tikv/pd/pull/4073)
    - PD 会动态调整调度计算重试次数，避免消耗过量 CPU 资源[#4047](https://github.com/tikv/pd/pull/4047)
    - 提升了 PD 之间 region 同步的性能 [#3993](https://github.com/tikv/pd/pull/3993)
    - 出于安全考虑，PD persist-api 只会接收 json 文件 [#3969](https://github.com/tikv/pd/pull/3969)
    - 提升了热点调度计算时的性能 [#3910](https://github.com/tikv/pd/pull/3910)

## Bug 修复

+ TiKV

    - 修复快照 GC 过程中可能遗留快照文件的问题。 [#10872](https://github.com/tikv/tikv/pull/10872)
    - 修复 TiKV 在启用 Titan 并从 pre-5.0 版本升级时出现的 Panic 问题。 [#10843](https://github.com/tikv/tikv/pull/10843)
    - 修复高版本 TiKV 无法回滚到 5.0.x 的问题。 [#10843](https://github.com/tikv/tikv/pull/10843)
    - 修复了启用 Titan 并从 < 5.0 版本升级到 >= 5.0 版本时 TiKV 崩溃的问题（如果集群从 TiKV 3.x 升级并在升级之前启用了 Titan，则该集群可能会遇到问题）。 [#10778](https://github.com/tikv/tikv/pull/10778)
    - 修复遗留的悲观锁导致的解析失败问题。 [#10654](https://github.com/tikv/tikv/pull/10654)
    - 修复某些平台上时间间隔计算 Panic 问题。 [#10571](https://github.com/tikv/tikv/pull/10571)
    - 修复 load-base-split 中`batch_get_command` 的键值未编码问题。 [#10564](https://github.com/tikv/tikv/pull/10564)

+ PD

    - 修复了 PD 无法及时修复 down peer 副本的问题 [#4082](https://github.com/tikv/pd/pull/4082)
    - 修复了 PD 在热点调度时没有考虑驱逐 leader 的 Store 的情况 [#3975](https://github.com/tikv/pd/pull/3975)
    - 修复了 PD 在热点调度中的错误统计 [#3964](https://github.com/tikv/pd/pull/3964)
    - 修复了 PD placement rule 在相关配置更改后没有及时更新的问题 [#3914](https://github.com/tikv/pd/pull/3914)
    - 修复了 PD 在产生调度时计算出错误的 store limit 使用情况从而无法调度 [#3856](https://github.com/tikv/pd/pull/3856)
    - 修复了 PD 调度器在修改失败时没有及时报错的问题 [#3823](https://github.com/tikv/pd/pull/3823)

+ TiFlash

    - 修复执行扫表任务时潜在的进程崩溃问题
    - 修复执行 `MPP` 任务时潜在的内存泄漏问题
    - 修复处理 DAG 请求时出现 `duplicated region` 报错的问题
    - 修复执行 `COUNT` 或 `COUNT DISTINCT` 函数时出现非预期结果的问题
    - 修复执行 `MPP` 任务时潜在的进程崩溃问题
    - 修复 TiFlash 多盘部署时无法恢复数据的潜在问题
    - 修复析构 `SharedQueryBlockInputStream` 时出现进程崩溃的潜在问题
    - 修复析构 `MPPTask` 时出现进程崩溃的潜在问题
    - 修复 TiFlash 无法建立 MPP 连接时出现非预期结果的问题
    - 修复解决锁时潜在的进程崩溃问题
    - 修复写压力重时 metrics 中 store size 不准确的问题
    - 修复当查询过滤条件包含诸如 `CONSTANT` `<` | `<=` | `>` | `>=` `COLUMN` 时出现错误结果的问题
    - 修复 TiFlash 长时间运行后无法回收 delta 数据的潜在问题
    - 修复 metrics 显示错误数值的潜在问题
    - 修复多盘部署时数据不一致的潜在问题
