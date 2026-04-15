---
title: PD 重要监控指标详解
aliases: ['/docs-cn/dev/grafana-pd-dashboard/','/docs-cn/dev/reference/key-monitoring-metrics/pd-dashboard/']
summary: PD 重要监控指标详解：使用 TiUP 部署 TiDB 集群时，一键部署监控系统 (Prometheus & Grafana)，监控架构参见 [TiDB 监控框架概述]。Grafana Dashboard 分为 PD、TiDB、TiKV、Node_exporter、Overview、Performance_overview 等。通过观察 PD 面板上的 Metrics，可以了解 PD 当前的状态。监控包括 PD role、Storage capacity、Current storage size、Current storage usage、Normal stores、Number of Regions、Abnormal stores、Region health、Current peer count 等。Cluster、Operator、Statistics - Balance、Statistics - hot write、Statistics - hot read、Scheduler、gRPC、etcd、TiDB、Heartbeat、Region storage 等指标也很重要。
---

# PD 重要监控指标详解

使用 TiUP 部署 TiDB 集群时，一键部署监控系统 (Prometheus & Grafana)，监控架构参见 [TiDB 监控框架概述](/tidb-monitoring-framework.md)。

目前 Grafana Dashboard 整体分为 PD、TiDB、TiKV、Node\_exporter、Overview、Performance\_overview 等。

对于日常运维，我们通过观察 PD 面板上的 Metrics，可以了解 PD 当前的状态。

以下为 PD Dashboard 监控说明：

- PD role：当前 PD 的角色
- Storage capacity：TiDB 集群总可用数据库空间大小
- Current storage size：TiDB 集群目前已用数据库空间大小
- Current storage usage：TiDB 集群存储空间的使用率
- Current storage used：TiDB 集群存储空间已使用大小
- Normal stores：处于正常状态的节点数目
- Number of Regions：当前集群的 Region 总量
- Abnormal stores：处于异常状态的节点数目，正常情况应当为 0
- Region health：集群所有 Region 的状态。通常情况下，pending 或 down 的 peer 应该少于 100，miss 的 peer 不能一直大于 0，empty Region 过多需及时打开 Region Merge
- Current peer count：当前集群 peer 的总量
- Leader/Primary：当前 PD Leader 或 Primary 角色状态
- Offline store progress：离线 Store 的进度
- Online store progress：上线 Store 的进度
- Left time：调度或迁移剩余时间
- Current scaling speed：当前扩缩容速率
- Placement Rules Status：Placement Rules 状态
![PD Dashboard - Header](/media/pd-dashboard-header-v4.png)

## Cluster

- PD scheduler config：PD 调度配置列表
- Cluster ID：集群的 cluster id，唯一标识
- Current TSO：当前分配 TSO 的物理时间戳部分
- Current ID allocation：当前可分配 ID 的最大值
- Region label isolation level：不同 label 所在的 level 的 Region 数量
- Label distribution：集群中 TiKV 节点的 label 分布情况
- Store Limit：Store 的调度限流状态
- CPU Usage：PD 进程 CPU 使用
- Memory Usage：PD 进程内存使用
- Uptime：PD 进程运行时间
- Goroutine Count：PD 进程 Goroutine 数量
- Current TSO Physcial：当前 TSO 的物理时间戳部分
- Current TSO Datetime：当前 TSO 的时间展示
- Max TSO gap：当前最大 TSO gap
- Scheduling Allowance Status：调度许可状态

![PD Dashboard - Cluster metrics](/media/pd-dashboard-cluster-v4.png)

## Operator

- Schedule operator create：新创建的不同 operator 的数量，单位 opm 代表一分钟内创建的个数 
- Schedule operator check：已检查的 operator 的次数，主要检查是否当前步骤已经执行完成，如果是，则执行下一个步骤
- Schedule operator finish：已完成调度的 operator 的数量
- Schedule operator timeout：已超时的 operator 的数量
- Schedule operator replaced or canceled：已取消或者被替换的 operator 的数量
- Schedule operators count by state：不同状态的 operator 的数量
- Operator finish duration：已完成的 operator 所花费的最长时间
- Operator step duration：已完成的 operator 的步骤所花费的最长时间
- Operator step finish duration：operator 步骤完成耗时
- Schedulers reach limit：调度器触达限流次数
- 99% operator region size：operator 处理 Region 的 99% 大小

![PD Dashboard - Operator metrics](/media/pd-dashboard-operator-v4.png)

## Statistics - Balance

- Store capacity：每个 TiKV 实例的总的空间大小
- Store available：每个 TiKV 实例的可用空间大小
- Store used：每个 TiKV 实例的已使用空间大小
- Size amplification：每个 TiKV 实例的空间放大比率
- Store available ratio：每个 TiKV 实例的可用空间比率
- Store leader score：每个 TiKV 实例的 leader 分数
- Store Region score：每个 TiKV 实例的 Region 分数
- Store leader size：每个 TiKV 实例上所有 leader 的大小
- Store Region size：每个 TiKV 实例上所有 Region 的大小
- Store leader count：每个 TiKV 实例上所有 leader 的数量
- Store Region count：每个 TiKV 实例上所有 Region 的数量

![PD Dashboard - Balance metrics](/media/pd-dashboard-balance-v4.png)

## Statistics - hot write

- Hot Region's leader distribution：每个 TiKV 实例上成为写入热点的 leader 的数量
- Total written bytes on hot leader Regions：每个 TiKV 实例上所有成为写入热点的 leader 的总的写入流量大小
- Total written keys on hot leader Regions：每个 TiKV 实例上所有成为写入热点的 leader 的写入 keys 数量
- Hot write Region's peer distribution：每个 TiKV 实例上成为写入热点的 peer 的数量
- Total written bytes on hot peer Regions：每个 TiKV 实例上所有成为写入热点的 peer 的写入流量大小
- Store Write rate bytes：每个 TiKV 实例总的写入的流量
- Store Write rate keys：每个 TiKV 实例总的写入 keys
- Store write query：每个 TiKV 实例写请求数量
- Hot cache write entry numbers：每个 TiKV 实例进入热点统计模块的 peer 的数量
- Selector write events：热点调度中选择器的事件发生次数
- Direction of hotspot transfer leader：热点调度中 leader 迁移方向，正数代表调入，负数代表调出
- Direction of hotspot move peer：热点调度中 peer 的调度方向，正数代表调入，负数代表调出

![PD Dashboard - Hot write metrics](/media/pd-dashboard-hotwrite-v4.png)

## Statistics - hot read

- Hot Region's peer distribution：每个 TiKV 实例上成为读取热点的 peer 的数量
- Total read bytes on hot peer Regions：每个 TiKV 实例上所有成为读取热点的 peer 的总的读取流量大小
- Store read rate bytes：每个 TiKV 实例总的读取的流量
- Store read rate keys：每个 TiKV 实例总的读取 keys
- Store read query：每个 TiKV 实例读请求数量
- Hot cache read entry numbers：每个 TiKV 实例进入热点统计模块的 peer 的数量
- Selector read events：热点调度中选择器的事件发生次数
- Direction of hotspot transfer leader：热点调度中 leader 迁移方向，正数代表调入，负数代表调出
- Direction of hotspot move peer：热点调度中 peer 的调度方向，正数代表调入，负数代表调出

![PD Dashboard - Hot read metrics](/media/pd-dashboard-hotread-v4.png)

## Scheduler

- Scheduler is running：所有正在运行的 scheduler
- Balance leader movement：leader 移动的详细情况
- Balance Region movement：Region 移动的详细情况
- Balance leader event：balance leader 的事件数量
- Balance Region event：balance Region 的事件数量
- Balance leader scheduler：balance-leader scheduler 的状态
- Balance Region scheduler：balance-region scheduler 的状态
- Balance Hot Region scheduler：balance-hot-region scheduler 的状态
- Patrol Region time：巡检 Region 的耗时
- Replica checker：replica checker 的状态
- Rule checker：rule checker 的状态
- Region merge checker：merge checker 的状态
- Filter target：尝试选择 Store 作为调度 target 时没有通过 Filter 的计数
- Filter source：尝试选择 Store 作为调度 source 时没有通过 Filter 的计数
- Balance Direction：Store 被选作调度 target 或 source 的次数
- Slow Store Scheduler：慢节点调度器状态

![PD Dashboard - Scheduler metrics](/media/pd-dashboard-scheduler-v4.png)

## gRPC

- gRPC Completed commands rate：gRPC 命令的完成速率
- gRPC 99% Completed commands duration：99% 命令的最长消耗时间
- gRPC commands concurrency number：gRPC 并发请求数
- gRPC Received commands rate：gRPC 接收命令速率
- gRPC Error rate：gRPC 错误速率
- Success Region Request(1% sample)：成功的 Region 请求（1% 采样）
- Failed Region Request：失败的 Region 请求

![PD Dashboard - gRPC metrics](/media/pd-dashboard-grpc-v2.png)

## HTTP

- HTTP Completed commands rate：HTTP 命令完成速率
- HTTP 99% Completed commands duration：HTTP 命令 99% 耗时
- HTTP commands concurrency number：HTTP 并发请求数

## etcd

- MVCC DB total size：etcd MVCC 数据库总大小
- Handle transactions count：etcd 的事务个数
- Handle transactions rate：etcd 的事务处理速率
- 99% Handle transactions duration：99% 的情况下，处理 etcd 事务所需花费的时间
- 99% WAL fsync duration：99% 的情况下，持久化 WAL 所需花费的时间，这个值通常应该小于 1s
- 99% Peer round trip time seconds：99% 的情况下，etcd 的网络延时，这个值通常应该小于 1s
- etcd disk WAL fsync rate：etcd 持久化 WAL 的速率
- 99% backend commit duration：etcd backend commit 的 99% 耗时
- etcd disk backend commit rate：etcd backend commit 的速率
- 99% Endpoint health check latency：etcd Endpoint 健康检查 99% 耗时
- Endpoint health state：etcd Endpoint 健康状态
- Raft term：当前 Raft 的 term
- Raft committed index：最后一次 commit 的 Raft index
- Raft applied index：最后一次 apply 的 Raft index

![PD Dashboard - etcd metrics](/media/pd-dashboard-etcd-v2.png)

## TiDB

- PD Server TSO handle time and Client recv time：从 PD 开始处理 TSO 请求到 client 端接收到 TSO 的总耗时
- Handle requests count：TiDB 的请求数量
- Handle requests duration：每个请求所花费的时间，99% 的情况下，应该小于 100ms
- PD server TSO handle duration：PD 端处理 TSO 请求耗时
- PD client TSO handle duration：客户端处理 TSO 请求耗时
- Handle TSO requests count：TSO 请求数量
- TSO request batch size：TSO 批量请求大小
- PD server QueryRegion handle duration：PD 端处理 QueryRegion 请求耗时
- PD client QueryRegion handle duration：客户端处理 QueryRegion 请求耗时
- Handle QueryRegion requests count：QueryRegion 请求数量
- QueryRegion request batch size：QueryRegion 批量请求大小

![PD Dashboard - TiDB metrics](/media/pd-dashboard-tidb-v4.png)

## Heartbeat

- Heartbeat region event QPS：心跳处理 region 的 QPS，包括更新缓存和持久化
- Region heartbeat handle latency overview：心跳处理延迟概览
- TiKV side heartbeat statistics：TiKV 侧心跳统计
- 99% Region heartbeat handle latency by store：按 store 统计的 99% 心跳处理延迟
- Region heartbeat report：TiKV 向 PD 发送的心跳个数
- Region heartbeat report error：TiKV 向 PD 发送的异常的心跳个数
- Region heartbeat report active：TiKV 向 PD 发送的正常的心跳个数
- Region schedule push：PD 向 TiKV 发送的调度命令的个数
- 99% Region heartbeat latency：99% 的情况下，心跳的延迟
- Heartbeat Performance Duration BreakDown (Accumulation)：心跳处理各阶段耗时累积
- Concurrent Runner Pending Task：并发 runner 待处理任务数
- Concurrent Runner Pending Duration：并发 runner 任务等待耗时
- Concurrent Runner Failed Task：并发 runner 失败任务数
- 99% store heartbeat handle duration：store 心跳处理 99% 耗时
- Heartbeat stream report：心跳流上报统计
- Heartbeat stream report error：心跳流上报错误统计
- 99% Bucket Report Interval：Bucket report 99% 上报间隔
- Bucket Report State：Bucket report 状态

![PD Dashboard - Heartbeat metrics](/media/pd-dashboard-heartbeat-v4.png)

## Region storage

- Syncer Index：Leader 记录 Region 变更历史的最大 index
- history last index：Follower 成功同步的 Region 变更历史的 index

![PD Dashboard - Region storage](/media/pd-dashboard-region-storage.png)

## Scatter and Splitter

- scatter operator event：scatter operator 事件统计
- scatter store selection：scatter 选择 store 统计

## DR Autosync

- State：DR Autosync 当前状态
- State of all instances：所有实例的 DR Autosync 状态
- Tick：DR Autosync tick 计数
- State ID：DR Autosync 状态 ID
- Recovered region：已恢复的 Region 数量
- Recover progress：恢复进度

## GO Runtime

- Memory Usage：PD 进程内存使用
- Estimated Live Objects：估算存活对象数量
- CPU Usage：PD 进程 CPU 使用
- GC STW Duration (last 256 GC cycles)：最近 256 次 GC 的 STW 时长
- Goroutine Count：Goroutine 数量
- Allocator Throughput：内存分配吞吐量
- Estimated portion of CPU time：估算 CPU 时间占比
- GC STW Latency(>= go1.22.0)：Go 1.22+ 的 GC STW 延迟
- Goroutine scheduler latency：Goroutine 调度延迟
- Golang GC：Golang GC 相关统计
- Sync mutex wait：互斥锁等待时间
- GOGC & GOMEMLIMIT：`GOGC` 与 `GOMEMLIMIT` 配置及其影响
- Heap alloc：堆内存分配量
- Heap free：堆内存空闲量
