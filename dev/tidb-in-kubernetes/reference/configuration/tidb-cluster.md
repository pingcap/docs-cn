---
title: TiDB Cluster Configurations in Kubernetes
summary: Learn the configurations of a TiDB cluster in Kubernetes.
category: reference
---

# TiDB Cluster Configurations in Kubernetes

This document introduces the following items of a TiDB cluster in Kubernetes:

+ The configuration parameters
+ The configuration of resources
+ The configuration of disaster recovery

## Configuration parameters

TiDB Operator uses `Helm` to deploy and manage TiDB clusters. The configuration file obtained through Helm provides the basic configuration by default with which you could quickly start a TiDB cluster. However, if you want special configurations or are deploying in a production environment, you need to manually configure the corresponding parameters according to the table below.

> **Note:**
>
> In the following table, `values.yaml` refers to the TiDB cluster's configuration file to be modified.

| Parameter | Description | Default Value |
| :----- | :---- | :----- |
| `rbac.create` | Whether to enable the RBAC mode of Kubernetes | `true` |
| `clusterName` |The TiDB cluster name. This variable is unset by default. In this case, `tidb-cluster` directly replaces it with `ReleaseName` when the cluster is being installed. | `nil` |
| `extraLabels` | Adds extra labels to the `TidbCluster` object (CRD). See [labels](https://kubernetes.io/docs/concepts/overview/working-with-objects/labels/) | `{}` |
| `schedulerName` | The scheduler used by the TiDB cluster | `tidb-scheduler` |
| `timezone` | The default timezone used by the TiDB cluster | `UTC` |
| `pvReclaimPolicy` | The reclaim policy for PV (Persistent Volume) used by the TiDB cluster | `Retain` |
| `services[0].name` | The name of the service that the TiDB cluster exposes | `nil` |
| `services[0].type` | The type of the service that the TiDB cluster exposes (selected from `ClusterIP`, `NodePort` and `LoadBalancer`) | `nil` |
| `discovery.image` | The image of PD's service discovery component in the TiDB cluster. This component is used to provide service discovery for each PD instance to coordinate the starting sequence when the PD cluster is started for the first time. | `pingcap/tidb-operator:v1.0.0` |
| `discovery.imagePullPolicy` | The pulling policy for the image of PD's service discovery component | `IfNotPresent` |
| `discovery.resources.limits.cpu` | The CPU resource limit of PD's service discovery component | `250m` |
| `discovery.resources.limits.memory` | The memory resource limit of PD's service discovery component | `150Mi` |
| `discovery.resources.requests.cpu` | The CPU resource request of PD's service discovery component | `80m` |
| `discovery.resources.requests.memory` | The memory resource request of PD's service discovery component | `50Mi` |
| `enableConfigMapRollout` | Whether to enable the automatic rolling update of the TiDB cluster. If enabled, the TiDB cluster automatically updates the corresponding components when the `ConfigMap` of this cluster changes. This configuration is only supported in `tidb-operator` v1.0 and later versions. | `false` |
| `pd.config` | The configuration of PD. Check [the `config.toml` file](https://github.com/pingcap/pd/blob/master/conf/config.toml) for the default PD configuration file (by choosing the tag of the corresponding PD version). You can see [PD Configuration Flags](/dev/reference/configuration/pd-server/configuration.md) for the detailed description of the configuration parameters (by choosing the corresponding document version). Here you must **modify the configuration based on the format of the configuration file**. | If the version of TiDB Operator is v1.0.0 or earlier, the default value is <br>`nil`<br>If the version of TiDB Operator is later than v1.0.0, the default value is <br>`[log]`<br>`level = "info"`<br>`[replication]`<br>`location-labels = ["region", "zone", "rack", "host"]`.<br>Sample configuration:<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`[log]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`level = "info"`<br>&nbsp;&nbsp;&nbsp;&nbsp;`[replication]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`location-labels = ["region", "zone", "rack", "host"]` |
| `pd.replicas` | The number of Pods in PD | `3` |
| `pd.image` | The PD image | `pingcap/pd:v3.0.0-rc.1` |
| `pd.imagePullPolicy` | The pulling policy for the PD image | `IfNotPresent` |
| `pd.logLevel` | The log level of PD<br>If the version of TiDB Operator is later than v1.0.0, configure the parameter via `pd.config`: <br>`[log]`<br>`level = "info"` | `info` |
| `pd.storageClassName` | The `storageClass` used by PD. `storageClassName` refers to a type of storage provided by the Kubernetes cluster, which might map to a level of service quality, a backup policy, or to any policy determined by the cluster administrator. Detailed reference: [storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes) | `local-storage` |
| `pd.maxStoreDownTime` | This parameter indicates how soon a store node is marked as `down` after it is disconnected. When the state changes to `down`, the store node starts migrating data to other store nodes.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `pd.config`:<br>`[schedule]`<br>`max-store-down-time = "30m"`  | `30m` |
| `pd.maxReplicas` | The number of data replicas in the TiDB cluster<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `pd.config`:<br>`[replication]`<br>`max-replicas = 3` | `3` |
| `pd.resources.limits.cpu` | The CPU resource limit per PD Pod | `nil` |
| `pd.resources.limits.memory` | The memory resource limit per PD Pod | `nil` |
| `pd.resources.limits.storage` | The storage limit per PD Pod | `nil` |
| `pd.resources.requests.cpu` | The CPU resource requests of each PD Pod | `nil` |
| `pd.resources.requests.memory` | The memory resource requests of each PD Pod | `nil` |
| `pd.resources.requests.storage` | The storage requests of each PD Pod | `1Gi` |
| `pd.affinity` | Defines PD's scheduling rules and preferences. Detailed reference: [affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-affinity) | `{}` |
| `pd.nodeSelector` | Ensures that PD Pods are only scheduled to the node with the specific key-value pair as the label. Detailed reference: [nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `pd.tolerations` | Applies to PD Pods, allowing the Pods to be scheduled to the nodes with specified taints. Detailed reference: [taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `pd.annotations` | Adds a specific `annotations` for PD Pods. | `{}` |
| `tikv.config` | The configuration of TiKV. Check [the `config-template.toml` file](https://github.com/tikv/tikv/blob/master/etc/config-template.toml) for the default TiKV configuration file (by choosing the tag of the corresponding TiKV version). You can see [TiKV Configuration Flags](/dev/reference/configuration/tikv-server/configuration.md) for the detailed description of the configuration parameters (by choosing the corresponding document version). Here you must **modify the configuration based on the format of the configuration file**.<br/><br/>You need to explicitly configure the following two configuration items:<br/><br/>`[storage.block-cache]`<br/>&nbsp;&nbsp;`shared = true`<br/>&nbsp;&nbsp;`capacity = "1GB"`<br/>It is recommended to set `capacity` to 50% of the value of `tikv.resources.limits.memory`.<br/><br/>`[readpool.coprocessor]`<br/>&nbsp;&nbsp;`high-concurrency = 8`<br/>&nbsp;&nbsp;`normal-concurrency = 8`<br/>&nbsp;&nbsp;`low-concurrency = 8`<br/>It is recommended to set to 80% of the value of `tikv.resources.limits.cpu`. | If the version of TiDB Operator is v1.0.0-beta.3 or earlier, the default value is<br>`nil`<br>If the version of TiDB Operator is later than v1.0.0-beta.3, the default value is<br>`log-level = "info"`<br>Sample configuration:<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`log-level = "info"` |
| `tikv.replicas` | The number of Pods in TiKV | `3` |
| `tikv.image` | The TiKV image | `pingcap/tikv:v3.0.0-rc.1` |
| `tikv.imagePullPolicy` | The pulling policy for the TiKV image | `IfNotPresent` |
| `tikv.logLevel` | The level of TiKV logs<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tikv.config`:<br>`log-level = "info"` | `info` |
| `tikv.storageClassName` | The `storageClass` used by TiKV. `storageClassName` refers to a type of storage provided by the Kubernetes cluster, which might map to a level of service quality, a backup policy, or to any policy determined by the cluster administrator. Detailed reference: [storage-classes](https://kubernetes.io/docs/concepts/storage/storage-classes) | `local-storage` |
| `tikv.syncLog` | `SyncLog` means whether to enable the raft log replication. Enabling this feature ensures that data will not be lost when power is off.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tikv.config`:<br>`[raftstore]`<br>`sync-log = true`  | `true` |
| `tikv.grpcConcurrency` | Configures the thread pool size of the gRPC server.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tikv.config`:<br>`[server]`<br>`grpc-concurrency = 4` | `4` |
| `tikv.resources.limits.cpu` | The CPU resource limit per TiKV Pod | `nil` |
| `tikv.resources.limits.memory` | The memory resource limit per TiKV Pod | `nil` |
| `tikv.resources.limits.storage` | The storage limit per TiKV Pod | `nil` |
| `tikv.resources.requests.cpu` | The CPU resource requests of each TiKV Pod | `nil` |
| `tikv.resources.requests.memory` | The memory resource requests of each TiKV Pod | `nil` |
| `tikv.resources.requests.storage` | The storage requests of each TiKV Pod | `10Gi` |
| `tikv.affinity` | Defines TiKV's scheduling rules and preferences. Detailed reference:[affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-affinity) | `{}` |
| `tikv.nodeSelector` | Ensures that TiKV Pods are only scheduled to the node with the specific key-value pair as the label. Detailed reference: [nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `tikv.tolerations` | Applies to TiKV Pods, allowing TiKV Pods to be scheduled to the nodes with specified taints. Detailed reference: [taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `tikv.annotations` | Adds a specific `annotations` for TiKV Pods. | `{}` |
| `tikv.defaultcfBlockCacheSize` | Specifies the size of block cache which is used to cache uncompressed blocks. Larger block cache settings speed up reads. It is recommended to set the parameter to 30%-50% of the value of `tikv.resources.limits.memory`.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tikv.config`:<br>`[rocksdb.defaultcf]`<br>`block-cache-size = "1GB"`<br>From TiKV v3.0.0 on, you do not need to configure `[rocksdb.defaultcf].block-cache-size` and `[rocksdb.writecf].block-cache-size`. Instead, configure `[storage.block-cache].capacity`. | `1GB` |
| `tikv.writecfBlockCacheSize` | Specifies the size of writecf block cache. It is recommended to set the parameter to 10%-30% of the value of `tikv.resources.limits.memory`.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tikv.config`:<br>`[rocksdb.writecf]`<br>`block-cache-size = "256MB"`<br>From TiKV v3.0.0 on, you do not need to configure `[rocksdb.defaultcf].block-cache-size` and `[rocksdb.writecf].block-cache-size`. Instead, configure `[storage.block-cache].capacity`. | `256MB` |
| `tikv.readpoolStorageConcurrency` | The size of thread pool for high priority, normal priority or low priority operations in the TiKV storage<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tikv.config`:<br>`[readpool.storage]`<br>`high-concurrency = 4`<br>`normal-concurrency = 4`<br>`low-concurrency = 4` | `4` |
| `tikv.readpoolCoprocessorConcurrency` | If `tikv.resources.limits.cpu` is greater than `8`, set the value of `tikv.readpoolCoprocessorConcurrency` to `tikv.resources.limits.cpu` * 0.8<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tikv.config`:<br>`[readpool.coprocessor]`<br>`high-concurrency = 8`<br>`normal-concurrency = 8`<br>`low-concurrency = 8` | `8` |
| `tikv.storageSchedulerWorkerPoolSize` | The worker pool size of the TiKV scheduler. This size must be increased in the case of rewriting but be smaller than the total CPU cores.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tikv.config`:<br>`[storage]`<br>`scheduler-worker-pool-size = 4` | `4` |
| `tidb.config` | The configuration of TiDB. Check [the `config.toml.example` file](https://github.com/pingcap/tidb/blob/master/config/config.toml.example) for the default TiDB configuration file (by choosing the tag of the corresponding TiDB version). You can see [TiDB Configuration File Description](https://pingcap.com/docs/v3.0/reference/configuration/tidb-server/configuration-file/) for the detailed description of the configuration parameters (by choosing the corresponding document version). Here you must **modify the configuration based on the format of the configuration file**.<br/><br/>You need to explicitly configure the following configuration items:<br/><br/>`[performance]`<br/>&nbsp;&nbsp;`max-procs = 0`<br/>It is recommended to set `max-procs` to the value of corresponding cores of `tidb.resources.limits.cpu` | If the version of TiDB Operator is v1.0.0-beta.3 or earlier, the default value is<br>`nil`<br>If the version of TiDB Operator is later than v1.0.0-beta.3, the default value is<br>`[log]`<br>`level = "info"`<br>Sample configuration:<br>&nbsp;&nbsp;`config:` \|<br>&nbsp;&nbsp;&nbsp;&nbsp;`[log]`<br>&nbsp;&nbsp;&nbsp;&nbsp;`level = "info"` |
| `tidb.replicas` | The number of Pods in TiDB | `2` |
| `tidb.image` | The TiDB image | `pingcap/tidb:v3.0.0-rc.1` |
| `tidb.imagePullPolicy` | The pulling policy for the TiDB image | `IfNotPresent` |
| `tidb.logLevel` | The level of TiDB logs<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`[log]`<br>`level = "info"`  | `info` |
| `tidb.resources.limits.cpu` | The CPU resource limit per TiDB Pod | `nil` |
| `tidb.resources.limits.memory` | The memory resource limit per TiDB Pod | `nil` |
| `tidb.resources.requests.cpu` | The CPU resource requests of each TiDB Pod | `nil` |
| `tidb.resources.requests.memory` | The memory resource requests of each TiDB Pod | `nil` |
| `tidb.passwordSecretName`| The name of the `Secret` that stores the TiDB username and password. The `Secret` can create a secret with this command: `kubectl create secret generic tidb secret--from literal=root=<root password>--namespace=<namespace>`. If the parameter is unset, TiDB root password is empty. | `nil` |
| `tidb.initSql`| The initialization script that will be executed after a TiDB cluster is successfully started. | `nil` |
| `tidb.affinity` | Defines TiDB's scheduling rules and preferences. Detailed reference: [affinity-and-anti-affinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-affinity) | `{}` |
| `tidb.nodeSelector` | Ensures that TiDB Pods are only scheduled to the node with the specific key-value pair as the label. Detailed reference: [nodeselector](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#nodeselector) | `{}` |
| `tidb.tolerations` | Applies to TiDB Pods, allowing TiDB Pods to be scheduled to nodes with specified taints. Detailed reference: [taint-and-toleration](https://kubernetes.io/docs/concepts/configuration/taint-and-toleration) | `{}` |
| `tidb.annotations` | Adds a specific `annotations` for TiDB Pods. | `{}` |
| `tidb.maxFailoverCount` | The maximum number of failovers for TiDB. Assuming the number is `3`, that is, up to 3 failovers TiDB instances are supported at the same time. | `3` |
| `tidb.service.type` | The type of service that the TiDB cluster exposes | `Nodeport` |
| `tidb.service.externalTrafficPolicy` | Whether this Service routes external traffic to a node-local or cluster-wide endpoint. There are two options available: `Cluster`(by default) and `Local`. `Cluster` obscures the client source IP and some traffic needs to hop twice among nodes for the intended node, but with a good overall load distribution. `Local` preserves the client source IP and avoids a second hop for the LoadBalancer and `Nodeport` type services, but risks potentially imbalanced traffic distribution. Detailed reference: [External LoadBalancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/#preserving-the-client-source-ip) | `nil` |
| `tidb.service.loadBalancerIP` | Specifies the IP of LoadBalancer. Some cloud providers allow you to specify `loadBalancerIP`. In these cases, the LoadBalancer will be created using the user-specified `loadBalancerIP`. If the `loadBalancerIP` field is not specified, the LoadBalancer will be set using the temporary IP address. If `loadBalancerIP` is specified but the cloud provider does not support this feature, the `loadbalancerIP` field you set will be ignored.| `nil` |
| `tidb.service.mysqlNodePort` | The MySQL `NodePort` that TiDB Service exposes |  |
| `tidb.service.exposeStatus` | The port that indicates the expose status of TiDB Service | `true` |
| `tidb.service.statusNodePort` | The `NodePort` exposed through specifying the status of TiDB Service |  |
| `tidb.separateSlowLog` | Whether to run in the sidecar mode the `SlowLog` of TiDB exported by the independent container | If the version of TiDB Operator is v1.0.0 or earlier, the default value is `false`.<br>If the version of TiDB Operator is later than v1.0.0, the default value is `true`.  |
| `tidb.slowLogTailer.image` | The image of TiDB's `slowLogTailer`. `slowLogTailer` is a container of the sidecar type, used to export the `SlowLog` of TiDB. This configuration only takes effect when `tidb.separateSlowLog`=`true`. | `busybox:1.26.2` |
| `tidb.slowLogTailer.resources.limits.cpu` | The CPU resource limit per TiDB Pod's `slowLogTailer` | `100m` |
| `tidb.slowLogTailer.resources.limits.memory` | The memory resource limit per TiDB Pod's `slowLogTailer` | `50Mi` |
| `tidb.slowLogTailer.resources.requests.cpu` | The requests of each TiDB Pod's `slowLogTailer` for CPU resources | `20m` |
| `tidb.slowLogTailer.resources.requests.memory` | The requests of each TiDB Pod's `slowLogTailer` for memory resources | `5Mi` |
| `tidb.plugin.enable` | Whether to enable the TiDB plugin | `false` |
| `tidb.plugin.directory` | Specifies the directory where the TiDB plugin is located. | `/plugins` |
| `tidb.plugin.list` | Specifies a list of plugins loaded on TiDB. The naming rules of Plugin ID: `plugin name-version`. For example: `'conn_limit-1'`. | `[]` |
| `tidb.preparedPlanCacheEnabled` | Whether to enable TiDB's prepared plan cache<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`[prepared-plan-cache]`<br>`enabled = false` | `false` |
| `tidb.preparedPlanCacheCapacity` | The cache capacity of TiDB's prepared plan<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`[prepared-plan-cache]`<br>`capacity = 100`  | `100` |
| `tidb.txnLocalLatchesEnabled` | Whether to enable the memory lock for transactions. It is recommended to enable the lock when there are many local transaction conflicts.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`[txn-local-latches]`<br>`enabled = false` | `false` |
| `tidb.txnLocalLatchesCapacity` |  The capacity of the transaction memory lock. The number of slots corresponding to Hash is automatically adjusted upward to an exponential multiple of `2`. Each slot occupies 32 Bytes of memory. When the range of writing data is relatively wide (such as importing data), setting this parameter too small a value results in lower performance.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`[txn-local-latches]`<br>`capacity = 10240000` | `10240000` |
| `tidb.tokenLimit` | The restrictions on TiDB to execute concurrent sessions<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`token-limit = 1000` | `1000` |
| `tidb.memQuotaQuery` | The memory quota for TiDB queries, which is 32GB by default.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`mem-quota-query = 34359738368` | `34359738368` |
| `tidb.txnEntryCountLimit` | The limit on the number of entries in a transaction. If TiKV is used as the storage, the entry represents a key-value pair. **Warning:** Do not set this value too large. Otherwise, it might have a big impact on the TiKV cluster. Set this parameter carefully.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`[performance]`<br>`txn-entry-count-limit = 300000` | `300000` |
| `tidb.txnTotalSizeLimit` | The limit on byte size for each entry in a transaction. If TiKV is used as the storage, the entry represents a key-value pair. **Warning:** Do not set this value too large. Otherwise, it might have a big impact on the TiKV cluster. Set this parameter carefully.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`[performance]`<br>`txn-total-size-limit = 104857600` | `104857600` |
| `tidb.enableBatchDml` | Enables batch submission for DML.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`enable-batch-dml = false` | `false` |
| `tidb.checkMb4ValueInUtf8` | Controls whether to check the `mb4` characters when the character set is `utf8`.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`check-mb4-value-in-utf8 = true` | `true` |
| `tidb.treatOldVersionUtf8AsUtf8mb4` | This parameter is used for upgrading compatibility. When it is set to `true`, `utf8` character set in the old table/column is treated as `utf8mb4`.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`treat-old-version-utf8-as-utf8mb4 = true` | `true` |
| `tidb.lease` | The lease time of TiDB Schema lease. It is highly risky to change this parameter. Therefore, it is not recommended to do so unless you know exactly what might be happening.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`lease = "45s"`  | `45s` |
| `tidb.maxProcs` | The maximum available CPU cores. `0` represents the number of CPU on the machine or Pod.<br>If the version of TiDB Operator is later than v1.0.0, configure this parameter via `tidb.config`:<br>`[performance]`<br>`max-procs = 0` | `0` |

## Resource configuration

Before deploying a TiDB cluster, it is necessary to configure the resources for each component of the cluster depending on your needs. PD, TiKV and TiDB are the core service components of a TiDB cluster. In a production environment, their resource configurations must be specified according to component needs. Detailed reference: [Hardware Recommendations](/dev/how-to/deploy/hardware-recommendations.md).

To ensure the proper scheduling and stable operation of the components of the TiDB cluster in Kubernetes, it is recommended to set Guaranteed-level QoS by letting `limits` equal to `requests` when configuring resources. Detailed reference: [Configure Quality of Service for Pods](https://kubernetes.io/docs/tasks/configure-pod-container/quality-service-pod/).

If you are using a NUMA-based CPU, you need to enable `Static`'s CPU management policy on the node for better performance. In order to allow the TiDB cluster component to monopolize the corresponding CPU resources, the CPU quota must be an integer greater than or equal to `1` besides setting Guaranteed-level QoS as mentioned above. Detailed reference: [Control CPU Management Policies on the Node](https://kubernetes.io/docs/tasks/administer-cluster/cpu-management-policies).

## Disaster recovery configuration

TiDB is a distributed database and its disaster recovery must ensure that when any physical topology node fails, not only the service is unaffected, but also the data is complete and available. The two configurations of disaster recovery are described separately as follows.

### Disaster recovery of TiDB service

The disaster recovery of TiDB service is essentially based on Kubernetes' scheduling capabilities. To optimize scheduling, TiDB Operator provides a custom scheduler that guarantees the disaster recovery of TiDB service at the host level through the specified scheduling algorithm. Currently, the TiDB cluster uses this scheduler as the default scheduler, which is configured through the item `schedulerName` in the above table.

Disaster recovery at other levels (such as rack, zone, region) are guaranteed by Affinity's `PodAntiAffinity`. `PodAntiAffinity` can avoid the situation where different instances of the same component are deployed on the same physical topology node. In this way, disaster recovery is achieved. Detailed user guide for Affinity: [Affinity & AntiAffinity](https://kubernetes.io/docs/concepts/configuration/assign-Pod-node/#affinity-and-anti-affinity).

The following is an example of a typical disaster recovery setup:

{{< copyable "" >}}

```shell
affinity:
 podAntiAffinity:
   preferredDuringSchedulingIgnoredDuringExecution:
   # this term works when the nodes have the label named region
   - weight: 10
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "region"
       namespaces:
       - <helm namespace>
   # this term works when the nodes have the label named zone
   - weight: 20
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "zone"
       namespaces:
       - <helm namespace>
   # this term works when the nodes have the label named rack
   - weight: 40
     podAffinityTerm:
       labelSelector:
         matchLabels:
           app.kubernetes.io/instance: <release name>
           app.kubernetes.io/component: "pd"
       topologyKey: "rack"
       namespaces:
       - <helm namespace>
   # this term works when the nodes have the label named kubernetes.io/hostname
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

### Disaster recovery of data

Before configuring the data disaster recovery, read [Information Configuration of the Cluster Typology](/dev/how-to/deploy/geographic-redundancy/location-awareness.md) which describes how the disaster recovery of the TiDB cluster is implemented.

To add the data disaster recovery feature in Kubernetes:

1. Set the label collection of topological location for PD

    > **Note:**
    >
    > Except for `kubernetes.io/hostname`, PD currently does not support labels with `/` in the name.

    Replace the `location-labels` information in the `pd.config` with the label collection that describes the topological location on the nodes in the Kubernetes cluster.

2. Set the topological information of the Node where the TiKV node is located.

    TiDB Operator automatically obtains the topological information of the Node for TiKV and calls the PD interface to set this information as the information of TiKV's store labels. Based on this topological information, the TiDB cluster schedules the replicas of the data.

    If the Node of the current Kubernetes cluster does not have a label indicating the topological location, or if the existing label name of topology contains `/`, you can manually add a label to the Node by running the following command:

    {{< copyable "shell-regular" >}}

    ```shell
    kubectl label node <nodeName> region=<regionName> zone=<zoneName> rack=<rackName> kubernetes.io/hostname=<hostName>
    ```

    In the command above, `region`, `zone`, `rack`, and `kubernetes.io/hostname` are just examples. The name and number of the label to be added can be arbitrarily defined, as long as it conforms to the specification and is consistent with the labels set by `location-labels` in `pd.config`.
