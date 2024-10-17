---
title: TiFlash MinTSO
summary: 介绍 TiFlash MinTSO 的调度原则
---

# TiFlash MinTSO

本文介绍了 MinTSO 的调度原则以及与 MinTSO 调度有关的参数。

为了避免 OOT，TiFlash 在调度前会获取 MPP Task 需要的线程数量，然后和当前存在的线程数量进行计算，最后决定是否调度该 Task。TiFlash 在运行时，会有多个 query 的 MPP Task 同时运行，这里潜藏资源死锁的风险，最后导致所有 query 的 Task 都无法继续被调度。为了解决死锁，我们引入了 MinTSO 机制。

MinTSO 有以下几个调度原则：
- 在某个 resource group 中，同时运行的 query 数量有限制，如果一条非 query id 最小的 query 被调度后会超过该限制，那么先将其放入等待队列。
- 在某个 resource group 中，总线程数量有限制(soft limit)，如果一条非 query id 最小的 query 被调度后会超过该限制，那么先将其放入等待队列。
- 在某个 resource group 中，如果某个非 query id 最小的 task 被调度后超过 hard limit 限制，那么它会被放入等待队列中。
- 在某个 resource group 中，query id 最小的 task 总是会被调度。
- 在某个 resource group 中，如果 query id 最小的 task 被调度后，全局线程数量超过了 hard limit，则该 query 直接报错，否则，调度成功。

参数：
- task_scheduler_thread_soft_limit：规定了某个 resource group 中最多可使用的线程数量，默认值为 5000
- task_scheduler_thread_hard_limit：规定了全局最多可使用的线程数量，默认值为 10000
- task_scheduler_active_set_soft_limit：规定了同时运行的 query 数量，默认值为两倍 vcpu 数量
