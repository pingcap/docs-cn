---
title: TiFlash 简介
---

# TiFlash 简介

TiFlash 是 TiDB HTAP 形态的关键组件，它是 TiKV 的列存扩展，在提供了良好的隔离性的同时，也兼顾了强一致性。列存副本通过 Raft Learner 协议异步复制，但是在读取的时候通过 Raft 校对索引配合 MVCC 的方式获得 Snapshot Isolation 的一致性隔离级别。这个架构很好地解决了 HTAP 场景的隔离性以及列存同步的问题。

## 整体架构

![TiFlash 架构](/media/tiflash/tiflash-architecture.png)

上图为 TiDB HTAP 形态架构，其中包含 TiFlash 节点。

TiFlash 提供列式存储，且拥有借助 ClickHouse 高效实现的协处理器层。除此以外，它与 TiKV 非常类似，依赖同样的 Multi-Raft 体系，以 Region 为单位进行数据复制和分散（详情见[《说存储》](https://pingcap.com/blog-cn/tidb-internal-1/)一文）。

TiFlash 以低消耗不阻塞 TiKV 写入的方式，实时复制 TiKV 集群中的数据，并同时提供与 TiKV 一样的一致性读取，且可以保证读取到最新的数据。TiFlash 中的 Region 副本与 TiKV 中完全对应，且会跟随 TiKV 中的 Leader 副本同时进行分裂与合并。

TiFlash 可以兼容 TiDB 与 TiSpark，用户可以选择使用不同的计算引擎。

TiFlash 推荐使用和 TiKV 不同的节点以做到 Workload 隔离，但在无业务隔离的前提下，也可以选择与 TiKV 同节点部署。

TiFlash 暂时无法直接接受数据写入，任何数据必须先写入 TiKV 再同步到 TiFlash。TiFlash 以 learner 角色接入 TiDB 集群，TiFlash 支持表粒度的数据同步，部署后默认情况下不会同步任何数据，需要按照[按表构建 TiFlash 副本](/tiflash/use-tiflash.md#按表构建-tiflash-副本)一节完成指定表的数据同步。

TiFlash 主要包含三个组件，除了主要的存储引擎组件，另外包含 tiflash proxy 和 pd buddy 组件，其中 tiflash proxy 主要用于处理 Multi-Raft 协议通信的相关工作，pd buddy 负责与 PD 协同工作，将 TiKV 数据按表同步到 TiFlash。

对于按表构建 TiFlash 副本的流程，TiDB 接收到相应的 DDL 命令后 pd buddy 组件会通过 TiDB 的 status 端口获取到需要同步的数据表信息，然后会将需要同步的数据信息发送到 PD，PD 根据该信息进行相关的数据调度。

## 核心特性

TiFlash 主要有异步复制、一致性、智能选择、计算加速等几个核心特性。

### 异步复制

TiFlash 中的副本以特殊角色 (Raft Learner) 进行异步的数据复制。这表示当 TiFlash 节点宕机或者网络高延迟等状况发生时，TiKV 的业务仍然能确保正常进行。

这套复制机制也继承了 TiKV 体系的自动负载均衡和高可用：并不用依赖附加的复制管道，而是直接以多对多方式接收 TiKV 的数据传输；且只要 TiKV 中数据不丢失，就可以随时恢复 TiFlash 的副本。

### 一致性

TiFlash 提供与 TiKV 一样的快照隔离支持，且保证读取数据最新（确保之前写入的数据能被读取）。这个一致性是通过对数据进行复制进度校验做到的。

每次收到读取请求，TiFlash 中的 Region 副本会向 Leader 副本发起进度校对（一个非常轻的 RPC 请求），只有当进度确保至少所包含读取请求时间戳所覆盖的数据之后才响应读取。

### 智能选择

TiDB 可以自动选择使用 TiFlash 列存或者 TiKV 行存，甚至在同一查询内混合使用提供最佳查询速度。这个选择机制与 TiDB 选取不同索引提供查询类似：根据统计信息判断读取代价并作出合理选择。

### 计算加速

TiFlash 对 TiDB 的计算加速分为两部分：列存本身的读取效率提升以及为 TiDB 分担计算。其中分担计算的原理和 TiKV 的协处理器一致：TiDB 会将可以由存储层分担的计算下推。能否下推取决于 TiFlash 是否可以支持相关下推。具体介绍请参阅[“TiFlash 支持的计算下推”](/tiflash/use-tiflash.md#tiflash-支持的计算下推)一节。

## 另请参阅

- 全新部署一个包含 TiFlash 节点的集群，请参考 [使用 TiUP 部署 TiDB 集群](/production-deployment-using-tiup.md)
- 已有集群新增一个 TiFlash 节点，请参考 [扩容 TiFlash 节点](/scale-tidb-using-tiup.md#扩容-tiflash-节点)
- 部署完成后，如何使用 TiFlash 节点，请参考 [使用 TiFlash](/tiflash/use-tiflash.md)
- TiFlash 常用运维操作，请参考 [TiFlash 运维](/tiflash/maintain-tiflash.md)
- TiFlash 性能调优，请参考 [TiFlash 性能调优](/tiflash/tune-tiflash-performance.md)
- TiFlash 配置参数介绍，请参考 [TiFlash 参数](/tiflash/tiflash-configuration.md)
- TiFlash 监控说明，请参考 [TiFlash 监控](/tiflash/monitor-tiflash.md)
- TiFlash 报警规则，请参考 [TiFlash 报警](/tiflash/tiflash-alert-rules.md)
- TiFlash 常见问题处理，请参考 [TiFlash 常见问题](/tiflash/troubleshoot-tiflash.md)
