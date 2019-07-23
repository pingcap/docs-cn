---
title: Kubernetes 上的 TiDB 集群配置
category: reference
---

# Kubernetes 上的 TiDB 集群配置

本文介绍 Kubernetes 上 TiDB 集群的配置参数、资源配置，以及容灾配置。

## 配置参数

TiDB Operator 使用 Helm 部署和管理 TiDB 集群。通过 Helm 获取的配置文件默认提供了基本的配置，通过这个基本配置，可以快速启动一个 TiDB 集群。但是如果用户需要特殊配置或是用于生产环境，则需要根据以下配置参数列表手动配置对应的配置项。

> **注意：**
>
> 下文用 `values.yaml` 指代要修改的 TiDB 集群配置文件。

| 参数名 | 说明 | 默认值 |
| :----- | :---- | :----- |
| `rbac.create` | 是否启用 Kubernetes 的 RBAC | `true` |
| `clusterName` | TiDB 集群名，默认不设置该变量，`tidb-cluster` 会直接用执行安装时的 `RealeaseName` 代替 | `nil` |
| `extraLabels` | TiDB 集群附加的自定义标签 参考：[labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) | `{}` |
| `schedulerName` | TiDB 集群使用的调度器 | `tidb-scheduler` |
| `timezone` | TiDB 集群默认时区 | `UTC` |
| `pvReclaimPolicy` | TiDB 集群使用的 PV (Persistent Volume)的 reclaim policy | `Retain` |
| `services[0].name` | TiDB 集群对外暴露服务的名字 | `nil` |
| `services[0].type` | TiDB 集群对外暴露服务的类型，(从 `ClusterIP`、`NodePort`、`LoadBalancer` 中选择) | `nil` |
| `discovery.image` | TiDB 集群 PD 服务发现组件的镜像，该组件用于在 PD 集群第一次启动时，为各个 PD 实例提供服务发现功能以协调启动顺序 | `pingcap/tidb-operator:v1.0.0-beta.3` |
| `discovery.imagePullPolicy` | PD 服务发现组件镜像的拉取策略 | `IfNotPresent` |
| `discovery.resoureces.limits.cpu` | PD 服务发现组件的 CPU 资源限额 | `250m` |
| `discovery.resoureces.limits.memory` | PD 服务发现组件的内存资源限额 | `150Mi` |
| `discovery.resoureces.requests.cpu` | PD 服务发现组件的 CPU 资源请求 | `80m` |
| `discovery.resoureces.requests.memory` | PD 服务发现组件的内存资源请求 | `50Mi` |
| `enableConfigMapRollout` | 是否开启 TiDB 集群自动滚动更新。如果启用，则 TiDB 集群的 ConfigMap 变更时，TiDB 集群自动更新对应组件。该配置只在 tidb-operator v1.0 及以上版本才支持 | `false` |
| `pd.config` | 配置文件格式的 PD 的配置，请参考[链接](https://github.com/pingcap/pd/blob/master/conf/config.toml)查看默认 PD 配置文件（选择对应 PD 版本的 tag），可以参考[文档](https://pingcap.com/docs-cn/v3.0/reference/configuration/pd-server/configuration-file/)查看配置参数的具体介绍（请选择对应的文档版本），这里只需要**按照配置文件中的格式修改配置** | TiDB Operator 版本 <= v1.0.0-beta.3，默认值为：<br>`nil`<br>TiDB Operator 版本 > v1.0.0-beta.3，默认值为：<br>`[log]`<br>`level = "info"`<br>`[replication]`<br>`location-labels = ["region", "zone", "rack", "host"]`<br>配置示例：<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`[log]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`level = "info"`<br>&nbsp;&nbsp;&nbsp;&nbsp;`[replication]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`location-labels = ["region", "zone", "rack", "host"]` |
| `pd.replicas` | PD 的 Pod 数 | `3` |
| `pd.image` | PD 镜像 | `pingcap/pd:v3.0.0-rc.1` |
| `pd.imagePullPolicy` | PD 镜像的拉取策略 | `IfNotPresent` |
| `pd.logLevel` | PD 日志级别<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `pd.config` 配置：<br>`[log]`<br>`level = "info"` | `info` |
| `pd.storageClassName` | PD 使用的 storageClass，storageClassName 指代一种由 Kubernetes 集群提供的存储类型，不同的类可能映射到服务质量级别、备份策略或集群管理员确定的任意策略。详细参考：[storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes) | `local-storage` |
| `pd.maxStoreDownTime` | `pd.maxStoreDownTime` 指一个 store 节点断开连接多长时间后状态会被标记为 `down`，当状态变为 `down` 后，store 节点开始迁移数据到其它 store 节点<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `pd.config` 配置：<br>`[schedule]`<br>`max-store-down-time = "30m"` | `30m` |
| `pd.maxReplicas` | `pd.maxReplicas` 是 TiDB 集群的数据的副本数<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `pd.config` 配置：<br>`[replication]`<br>`max-replicas = 3` | `3` |
| `pd.resources.limits.cpu` | 每个 PD Pod 的 CPU 资源限额 | `nil` |
| `pd.resources.limits.memory` | 每个 PD Pod 的内存资源限额 | `nil` |
| `pd.resources.limits.storage` | 每个 PD Pod 的存储容量限额 | `nil` |
| `pd.resources.requests.cpu` | 每个 PD Pod 的 CPU 资源请求 | `nil` |
| `pd.resources.requests.memory` | 每个 PD Pod 的内存资源请求 | `nil` |
| `pd.resources.requests.storage` | 每个 PD Pod 的存储容量请求 | `1Gi` |
| `pd.affinity` | `pd.affinity` 定义 PD 的调度规则和偏好，详细请参考：[affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity) | `{}` |
| `pd.nodeSelector` | `pd.nodeSelector` 确保 PD Pods 只调度到以该键值对作为标签的节点，详情参考：[nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `pd.tolerations` | `pd.tolerations` 应用于 PD Pods，允许 PD Pods 调度到含有指定 taints 的节点上，详情参考：[taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `pd.annotations` | 为 PD Pods 添加特定的 `annotations` | `{}` |
| `tikv.config` | 配置文件格式的 TiKV 的配置，请参考[链接](https://github.com/tikv/tikv/blob/master/etc/config-template.toml)查看默认 TiKV 配置文件（选择对应 TiKV 版本的 tag），可以参考[文档](https://pingcap.com/docs-cn/v3.0/reference/configuration/tikv-server/configuration-file/)查看配置参数的具体介绍（请选择对应的文档版本），这里只需要**按照配置文件中的格式修改配置** | TiDB Operator 版本 <= v1.0.0-beta.3，默认值为：<br>`nil`<br>TiDB Operator 版本 > v1.0.0-beta.3，默认值为：<br>`log-level = "info"`<br>配置示例：<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`log-level = "info"` |
| `tikv.replicas` | TiKV 的 Pod 数 | `3` |
| `tikv.image` | TiKV 的镜像 | `pingcap/tikv:v3.0.0-rc.1` |
| `tikv.imagePullPolicy` | TiKV 镜像的拉取策略 | `IfNotPresent` |
| `tikv.logLevel` | TiKV 的日志级别<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tikv.config` 配置：<br>`log-level = "info"` | `info` |
| `tikv.storageClassName` | TiKV 使用的 storageClass，storageClassName 指代一种由 Kubernetes 集群提供的存储类型，不同的类可能映射到服务质量级别、备份策略或集群管理员确定的任意策略。详细参考：[storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes) | `local-storage` |
| `tikv.syncLog` | syncLog 指是否启用 raft 日志同步功能，启用该功能能保证在断电时数据不丢失<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tikv.config` 配置：<br>`[raftstore]`<br>`sync-log = true` | `true` |
| `tikv.grpcConcurrency` | 配置 gRPC server 线程池大小<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tikv.config` 配置：<br>`[server]`<br>`grpc-concurrency = 4` | `4` |
| `tikv.resources.limits.cpu` | 每个 TiKV Pod 的 CPU 资源限额 | `nil` |
| `tikv.resources.limits.memory` | 每个 TiKV Pod 的内存资源限额 | `nil` |
| `tikv.resources.limits.storage` | 每个 TiKV Pod 的存储容量限额 | `nil` |
| `tikv.resources.requests.cpu` | 每个 TiKV Pod 的 CPU 资源请求 | `nil` |
| `tikv.resources.requests.memory` | 每个 TiKV Pod 的内存资源请求 | `nil` |
| `tikv.resources.requests.storage` | 每个 TiKV Pod 的存储容量请求 | `10Gi` |
| `tikv.affinity` | `tikv.affinity` 定义 TiKV 的调度规则和偏好，详细请参考：[affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity) | `{}` |
| `tikv.nodeSelector` | `tikv.nodeSelector`确保 TiKV Pods 只调度到以该键值对作为标签的节点，详情参考：[nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `tikv.tolerations` | `tikv.tolerations` 应用于 TiKV Pods，允许 TiKV Pods 调度到含有指定 taints 的节点上，详情参考：[taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `tikv.annotations` | 为 TiKV Pods 添加特定的 `annotations` | `{}` |
| `tikv.defaultcfBlockCacheSize` | 指定 block 缓存大小，block 缓存用于缓存未压缩的 block，较大的 block 缓存设置可以加快读取速度。一般推荐设置为 `tikv.resources.limits.memory` 的 30%-50%<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tikv.config` 配置：<br>`[rocksdb.defaultcf]`<br>`block-cache-size = "1GB"`<br>从 TiKV v3.0.0 开始，不再需要配置 `[rocksdb.defaultcf].block-cache-size` 和 `[rocksdb.writecf].block-cache-size`，改为配置 `[storage.block-cache].capacity` | `1GB` |
| `tikv.writecfBlockCacheSize` | 指定 writecf 的 block 缓存大小，一般推荐设置为 `tikv.resources.limits.memory` 的 10%-30%<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tikv.config` 配置：<br>`[rocksdb.writecf]`<br>`block-cache-size = "256MB"`<br>从 TiKV v3.0.0 开始，不再需要配置 `[rocksdb.defaultcf].block-cache-size` 和 `[rocksdb.writecf].block-cache-size`，改为配置 `[storage.block-cache].capacity` | `256MB` |
| `tikv.readpoolStorageConcurrency` | TiKV 存储的高优先级/普通优先级/低优先级操作的线程池大小<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tikv.config` 配置：<br>`[readpool.storage]`<br>`high-concurrency = 4`<br>`normal-concurrency = 4`<br>`low-concurrency = 4` | `4` |
| `tikv.readpoolCoprocessorConcurrency` | 一般如果 `tikv.resources.limits.cpu` > 8，则 `tikv.readpoolCoprocessorConcurrency` 设置为`tikv.resources.limits.cpu` * 0.8<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tikv.config` 配置：<br>`[readpool.coprocessor]`<br>`high-concurrency = 8`<br>`normal-concurrency = 8`<br>`low-concurrency = 8` | `8` |
| `tikv.storageSchedulerWorkerPoolSize` | TiKV 调度程序的工作池大小，应在重写情况下增加，同时应小于总 CPU 核心<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tikv.config` 配置：<br>`[storage]`<br>`scheduler-worker-pool-size = 4` | `4` |
| `tidb.config` | 配置文件格式的 TiDB 的配置，请参考[链接](https://github.com/pingcap/tidb/blob/master/config/config.toml.example)查看默认 TiDB 配置文件（选择对应 TiDB 版本的 tag），可以参考[文档](https://pingcap.com/docs-cn/v3.0/reference/configuration/tidb-server/configuration-file/)查看配置参数的具体介绍（请选择对应的文档版本），这里只需要**按照配置文件中的格式修改配置** | TiDB Operator 版本 <= v1.0.0-beta.3，默认值为：<br>`nil`<br>TiDB Operator 版本 > v1.0.0-beta.3，默认值为：<br>`[log]`<br>`level = "info"`<br>配置示例：<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`[log]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`level = "info"` |
| `tidb.replicas` | TiDB 的 Pod 数 | `2` |
| `tidb.image` | TiDB 的镜像 | `pingcap/tidb:v3.0.0-rc.1` |
| `tidb.imagePullPolicy` | TiDB 镜像的拉取策略 | `IfNotPresent` |
| `tidb.logLevel` | TiDB 的日志级别<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`[log]`<br>`level = "info"` | `info` |
| `tidb.resources.limits.cpu` | 每个 TiDB Pod 的 CPU 资源限额 | `nil` |
| `tidb.resources.limits.memory` | 每个 TiDB Pod 的内存资源限额 | `nil` |
| `tidb.resources.requests.cpu` | 每个 TiDB Pod 的 CPU 资源请求 | `nil` |
| `tidb.resources.requests.memory` | 每个 TiDB Pod 的内存资源请求 | `nil` |
| `tidb.passwordSecretName`| 存放 TiDB 用户名及密码的 Secret 的名字，该 Secret 可以使用以下命令创建机密：`kubectl create secret generic tidb secret--from literal=root=<root password>--namespace=<namespace>`，如果没有设置，则 TiDB 根密码为空 | `nil` |
| `tidb.initSql`| 在 TiDB 集群启动成功后，会执行的初始化脚本 | `nil` |
| `tidb.affinity` | `tidb.affinity` 定义 TiDB 的调度规则和偏好，详细请参考：[affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity) | `{}` |
| `tidb.nodeSelector` | `tidb.nodeSelector`确保 TiDB Pods 只调度到以该键值对作为标签的节点，详情参考：[nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `tidb.tolerations` | `tidb.tolerations` 应用于 TiDB Pods，允许 TiDB Pods 调度到含有指定 taints 的节点上，详情参考：[taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `tidb.annotations` | 为 TiDB Pods 添加特定的 `annotations` | `{}` |
| `tidb.maxFailoverCount` | TiDB 最大的故障转移数量，假设为 3 即最多支持同时 3 个 TiDB 实例故障转移 | `3` |
| `tidb.service.type` | TiDB 服务对外暴露类型 | `NodePort` |
| `tidb.service.externalTrafficPolicy` | 表示此服务是否希望将外部流量路由到节点本地或集群范围的端点。有两个可用选项：`Cluster`（默认）和 `Local`。`Cluster` 隐藏了客户端源 IP，可能导致流量需要二次跳转到另一个节点，但具有良好的整体负载分布。`Local` 保留客户端源 IP 并避免 LoadBalancer 和 NodePort 类型服务流量的第二次跳转，但存在潜在的不均衡流量传播风险。详细参考：[外部负载均衡器](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip) | `nil` |
| `tidb.service.loadBalancerIP` | 指定 tidb 负载均衡 IP，某些云提供程序允许您指定loadBalancerIP。在这些情况下，将使用用户指定的loadBalancerIP创建负载平衡器。如果未指定loadBalancerIP字段，则将使用临时IP地址设置loadBalancer。如果指定loadBalancerIP但云提供程序不支持该功能，则将忽略您设置的loadbalancerIP字段 | `nil` |
| `tidb.service.mysqlNodePort` | TiDB 服务暴露的 mysql NodePort 端口 |  |
| `tidb.service.exposeStatus` | TiDB 服务是否暴露状态端口 | `true` |
| `tidb.service.statusNodePort` | 指定 TiDB 服务的状态端口暴露的 `NodePort` |  |
| `tidb.separateSlowLog` | 是否以 sidecar 方式运行独立容器输出 TiDB 的 SlowLog | 如果 TiDB Operator 版本 <= v1.0.0-beta.3，默认值为 `false`<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，默认值为 `true` |
| `tidb.slowLogTailer.image` | TiDB 的 slowLogTailer 的镜像，slowLogTailer 是一个 sidecar 类型的容器，用于输出 TiDB 的 SlowLog，该配置仅在 `tidb.separateSlowLog`=`true` 时生效 | `busybox:1.26.2` |
| `tidb.slowLogTailer.resources.limits.cpu` | 每个 TiDB Pod 的 slowLogTailer 的 CPU 资源限额 | `100m` |
| `tidb.slowLogTailer.resources.limits.memory` | 每个 TiDB Pod 的 slowLogTailer 的内存资源限额 | `50Mi` |
| `tidb.slowLogTailer.resources.requests.cpu` | 每个 TiDB Pod 的 slowLogTailer 的 CPU 资源请求 | `20m` |
| `tidb.slowLogTailer.resources.requests.memory` | 每个 TiDB Pod 的 slowLogTailer 的内存资源请求 | `5Mi` |
| `tidb.plugin.enable` | 是否启用 TiDB 插件功能 | `false` |
| `tidb.plugin.directory` | 指定 TiDB 插件所在的目录 | `/plugins` |
| `tidb.plugin.list` | 指定 TiDB 加载的插件列表，plugin ID 命名规则：插件名-版本，例如：'conn_limit-1' | `[]` |
| `tidb.preparedPlanCacheEnabled` | 是否启用 TiDB 的 prepared plan 缓存<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`[prepared-plan-cache]`<br>`enabled = false` | `false` |
| `tidb.preparedPlanCacheCapacity` | TiDB 的 prepared plan 缓存数量<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`[prepared-plan-cache]`<br>`capacity = 100` | `100` |
| `tidb.txnLocalLatchesEnabled` | 是否启用事务内存锁，当本地事务冲突比较多时建议开启<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`[txn-local-latches]`<br>`enabled = false` | `false` |
| `tidb.txnLocalLatchesCapacity` |  事务内存锁的容量，Hash 对应的 slot 数，会自动向上调整为 2 的指数倍。每个 slot 占 32 Bytes 内存。当写入数据的范围比较广时（如导数据），设置过小会导致变慢，性能下降。<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`[txn-local-latches]`<br>`capacity = 10240000` | `10240000` |
| `tidb.tokenLimit` | TiDB 并发执行会话的限制<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`token-limit = 1000` | `1000` |
| `tidb.memQuotaQuery` | TiDB 查询的内存限额，默认 32GB<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`mem-quota-query = 34359738368` | `34359738368` |
| `tidb.txnEntryCountLimit` | 一个事务中条目的数目限制。如果使用 TiKV 作为存储，则条目表示键/值对。**警告**：不要将该值设置得太大，否则会对 TiKV 集群造成很大影响。请仔细调整此配置<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`[performance]`<br>`txn-entry-count-limit = 300000` | `300000` |
| `tidb.txnTotalSizeLimit` | 一个事务中各条目的字节大小限制。如果使用 TiKV 作为存储，则条目表示键/值对。**警告**：不要将该值设置得太大，否则会对 TiKV 集群造成很大影响。请仔细调整此配置<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`[performance]`<br>`txn-total-size-limit = 104857600` | `104857600` |
| `tidb.enableBatchDml` | `tidb.enableBatchDml` 为 DML 启用批提交<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`enable-batch-dml = false` | `false` |
| `tidb.checkMb4ValueInUtf8` | 用于控制当字符集为 utf8 时是否检查 mb4 字符<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`check-mb4-value-in-utf8 = true` | `true` |
| `tidb.treatOldVersionUtf8AsUtf8mb4` | 用于升级兼容性。设置为 `true` 将把旧版本的表/列的 `utf8` 字符集视为 `utf8mb4` 字符集<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`treat-old-version-utf8-as-utf8mb4 = true` | `true` |
| `tidb.lease` | `tidb.lease`是 TiDB Schema lease 的期限，对其更改是非常危险的，除非你明确知道可能产生的结果，否则不建议更改。<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`lease = "45s"` | `45s` |
| `tidb.maxProcs` | 最大可使用的 CPU 核数，0 代表机器/Pod 上的 CPU 数量<br>如果 TiDB Operator 版本 > v1.0.0-beta.3，请通过 `tidb.config` 配置：<br>`[performance]`<br>`max-procs = 0` | `0` |

## 资源配置说明

部署前需要根据实际情况和需求，为 TiDB 集群各个组件配置资源，上面列表中所述每个组件的资源配置包括 requests 和 limits，分别指资源的最低要求和最大限额，资源的 limits 要大于等于 requests，建议 limits 等于 requests，这样可以保证服务获得 Guaranteed 级别的 QoS。

其中 PD/TiKV/TiDB 是 TiDB 集群的核心服务组件，在生产环境下它们的资源配置需要按组件要求指定，具体参考：[资源配置推荐](/how-to/deploy/hardware-recommendations.md)。如果是测试环境，可以无需配置资源直接使用 `values.yaml` 中默认的配置。

## 容灾配置说明

TiDB 是分布式数据库，它的容灾需要做到在任一个物理拓扑节点发生故障时，不仅服务不受影响，还要保证数据也是完整和可用。下面分别具体说明这两种容灾的配置。

### TiDB 服务的容灾

TiDB 服务容灾本质上基于 Kubernetes 的调度功能来实现的，为了优化调度，TiDB Operator 提供了自定义的调度器，该调度器通过指定的调度算法能在 host 层面，保证 TiDB 服务的容灾，而且目前 TiDB Cluster 使用该调度器作为默认调度器，设置项是上述列表中的 `schedulerName` 配置项。

其它层面的容灾（例如 rack，zone，region）是通过 Affinity 的 `PodAntiAffinity` 来保证，通过 `PodAntiAffinity` 能尽量避免同一组件的不同实例部署到同一个物理拓扑节点上，从而达到容灾的目的，Affinity 的使用参考：[Affinity & AntiAffinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-baffinity) 。

下面是一个典型的容灾设置例子：

{{< copyable "shell-regular" >}}

```shell
affinity:
 podAntiAffinity:
   preferredDuringSchedulingIgnoredDuringExecution:
   # this term work when the nodes have the label named region
   - weight: 10
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "region"
       namespaces:
       - <helm namespace>
   # this term work when the nodes have the label named zone
   - weight: 20
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "zone"
       namespaces:
       - <helm namespace>
   # this term work when the nodes have the label named rack
   - weight: 40
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "rack"
       namespaces:
       - <helm namespace>
   # this term work when the nodes have the label named kubernetes.io/hostname
   - weight: 80
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "kubernetes.io/hostname"
       namespaces:
       - <helm namespace>
```

### 数据的容灾

在开始数据容灾配置前，首先请阅读[集群拓扑信息配置](/how-to/deploy/geographic-redundancy/location-awareness.md)。该文档描述了 TiDB 集群数据容灾的实现原理。

在 Kubernetes 上集成该功能，需要如下操作：

* 为 PD 设置拓扑位置 Label 集合

    > **注意：**
    >
    > 除 `kubernetes.io/hostname` 外，目前 PD 暂不支持名字中带 `/` 的 Label。

    用 Kubernetes 集群 Node 节点上描述拓扑位置的 Label 集合替换 `pd.config` 配置项中里的 `location-labels` 信息。

* 为 TiKV 节点设置所在的 Node 节点的拓扑信息

    TiDB Operator 会自动为 TiKV 获取其所在 Node 节点的拓扑信息，并调用 PD 接口将这些信息设置为 TiKV 的 store labels 信息，这样 TiDB 集群就能基于这些信息来调度数据副本。

    如果当前 Kubernetes 集群的 Node 节点没有表示拓扑位置的 Label，或者已有的拓扑 Label 名字中带有 `/`，可以通过下面的命令手动给 Node 增加标签：

    {{< copyable "shell-regular" >}}

    ```shell
    $ kubectl label node <nodeName> region=<regionName> zone=<zoneName> rack=<rackName> kubernetes.io/hostname=<hostName>
    ```

    其中 `region`、`zone`、`rack`、`kubernetes.io/hostname` 只是举例，要添加的 Label 名字和数量可以任意定义，只要符合规范且和 `pd.config` 里的 `location-labels` 设置的 Labels 保持一致即可
