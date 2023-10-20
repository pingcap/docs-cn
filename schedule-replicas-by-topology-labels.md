---
title: Schedule Replicas by Topology Labels
summary: Learn how to schedule replicas by topology labels.
aliases: ['/docs/dev/location-awareness/','/docs/dev/how-to/deploy/geographic-redundancy/location-awareness/','/tidb/dev/location-awareness']
---

# Schedule Replicas by Topology Labels

> **Note:**
>
> TiDB v5.3.0 introduces [Placement Rules in SQL](/placement-rules-in-sql.md). This offers a more convenient way to configure the placement of tables and partitions. Placement Rules in SQL might replace placement configuration with PD in future releases.

To improve the high availability and disaster recovery capability of TiDB clusters, it is recommended that TiKV nodes are physically scattered as much as possible. For example, TiKV nodes can be distributed on different racks or even in different data centers. According to the topology information of TiKV, the PD scheduler automatically performs scheduling at the background to isolate each replica of a Region as much as possible, which maximizes the capability of disaster recovery.

To make this mechanism effective, you need to properly configure TiKV and PD so that the topology information of the cluster, especially the TiKV location information, is reported to PD during deployment. Before you begin, see [Deploy TiDB Using TiUP](/production-deployment-using-tiup.md) first.

## Configure `labels` based on the cluster topology

### Configure `labels` for TiKV and TiFlash

You can use the command-line flag or set the TiKV or TiFlash configuration file to bind some attributes in the form of key-value pairs. These attributes are called `labels`. After TiKV and TiFlash are started, they report their `labels` to PD so users can identify the location of TiKV and TiFlash nodes.

Assume that the topology has four layers: zone > data center (dc) > rack > host, and you can use these labels (zone, dc, rack, host) to set location of the TiKV and TiFlash. To set labels for TiKV and TiFlash, you can use one of the following methods:

+ Use the command-line flag to start a TiKV instance:

    ```shell
    tikv-server --labels zone=<zone>,dc=<dc>,rack=<rack>,host=<host>
    ```

+ Configure in the TiKV configuration file:

    ```toml
    [server]
    [server.labels]
    zone = "<zone>"
    dc = "<dc>"
    rack = "<rack>"
    host = "<host>"
    ```

To set labels for TiFlash, you can use the `tiflash-learner.toml` file, which is the configuration file of tiflash-proxy:

```toml
[server]
[server.labels]
zone = "<zone>"
dc = "<dc>"
rack = "<rack>"
host = "<host>"
```

### (Optional) Configure `labels` for TiDB

When [Follower read](/follower-read.md) is enabled, if you want TiDB to prefer to read data from the same region, you need to configure `labels` for TiDB nodes.

You can set `labels` for TiDB using the configuration file:

```toml
[labels]
zone = "<zone>"
dc = "<dc>"
rack = "<rack>"
host = "<host>"
```

> **Note:**
>
> Currently, TiDB depends on the `zone` label to match and select replicas that are in the same region. To use this feature, you need to include `zone` when [configuring `location-labels` for PD](#configure-location-labels-for-pd), and configure `zone` when configuring `labels` for TiDB, TiKV, and TiFlash. For more details, see [Configure `labels` for TiKV and TiFlash](#configure-labels-for-tikv-and-tiflash).

### Configure `location-labels` for PD

According to the description above, the label can be any key-value pair used to describe TiKV attributes. But PD cannot identify the location-related labels and the layer relationship of these labels. Therefore, you need to make the following configuration for PD to understand the TiKV node topology.

Defined as an array of strings, `location-labels` is the configuration for PD. Each item of this configuration corresponds to the key of TiKV `labels`. Besides, the sequence of each key represents the layer relationship of different labels (the isolation levels decrease from left to right).

You can customize the value of `location-labels`, such as `zone`, `rack`, or `host`, because the configuration does not have default values. Also, this configuration has **no** restriction in the number of label levels (not mandatory for 3 levels) as long as they match with TiKV server labels.

> **Note:**
>
> - To make configurations take effect, you must configure `location-labels` for PD and `labels` for TiKV at the same time. Otherwise, PD does not perform scheduling according to the topology.
> - If you use Placement Rules in SQL, you only need to configure `labels` for TiKV. Currently, Placement Rules in SQL is incompatible with the `location-labels` configuration of PD and ignores this configuration. It is not recommended to use `location-labels` and Placement Rules in SQL at the same time; otherwise, unexpected results might occur.

To configure `location-labels`, choose one of the following methods according to your cluster situation:

+ If the PD cluster is not initialized, configure `location-labels` in the PD configuration file:

    {{< copyable "" >}}

    ```toml
    [replication]
    location-labels = ["zone", "rack", "host"]
    ```

+ If the PD cluster is already initialized, use the pd-ctl tool to make online changes:

    {{< copyable "shell-regular" >}}

    ```bash
    pd-ctl config set location-labels zone,rack,host
    ```

### Configure `isolation-level` for PD

If `location-labels` has been configured, you can further enhance the topological isolation requirements on TiKV clusters by configuring `isolation-level` in the PD configuration file.

Assume that you have made a three-layer cluster topology by configuring `location-labels` according to the instructions above: zone -> rack -> host, you can configure the `isolation-level` to `zone` as follows:

{{< copyable "" >}}

```toml
[replication]
isolation-level = "zone"
```

If the PD cluster is already initialized, you need to use the pd-ctl tool to make online changes:

{{< copyable "shell-regular" >}}

```bash
pd-ctl config set isolation-level zone
```

The `location-level` configuration is an array of strings, which needs to correspond to a key of `location-labels`. This parameter limits the minimum and mandatory isolation level requirements on TiKV topology clusters.

> **Note:**
>
> `isolation-level` is empty by default, which means there is no mandatory restriction on the isolation level. To set it, you need to configure `location-labels` for PD and ensure that the value of `isolation-level` is one of `location-labels` names.

### Configure a cluster using TiUP (recommended)

When using TiUP to deploy a cluster, you can configure the TiKV location in the [initialization configuration file](/production-deployment-using-tiup.md#step-3-initialize-cluster-topology-file). TiUP will generate the corresponding configuration files for TiKV, PD, and TiFlash during deployment.

In the following example, a two-layer topology of `zone/host` is defined. The TiKV nodes and TiFlash nodes of the cluster are distributed among three zones, z1, z2, and z3. 

- In each zone, there are two hosts that have TiKV instances deployed. In z1, each host has two TiKV instances deployed. In z2 and z3, each host has a separate TiKV instance deployed. 
- In each zone, there are two hosts that have TiFlash instances deployed, and each host has a separate TiFlash instance deployed. 

In the following example, `tikv-host-machine-n` represents the IP address of the `n`th TiKV node, and `tiflash-host-machine-n` represents the IP address of the `n`th TiFlash node.

```
server_configs:
  pd:
    replication.location-labels: ["zone", "host"]

tikv_servers:
# z1
  # machine-1 on z1
  - host: tikv-host-machine-1
    port：20160
    config:
      server.labels:
        zone: z1
        host: tikv-host-machine-1
  - host: tikv-host-machine-1
    port：20161
    config:
      server.labels:
        zone: z1
        host: tikv-host-machine-1
  # machine-2 on z1
  - host: tikv-host-machine-2
    port：20160
    config:
      server.labels:
        zone: z1
        host: tikv-host-machine-2
  - host: tikv-host-machine-2
    port：20161
    config:
      server.labels:
        zone: z1
        host: tikv-host-machine-2
# z2
  - host: tikv-host-machine-3
    config:
      server.labels:
        zone: z2
        host: tikv-host-machine-3
  - host: tikv-host-machine-4
    config:
      server.labels:
        zone: z2
        host: tikv-host-machine-4
# z3
  - host: tikv-host-machine-5
    config:
      server.labels:
        zone: z3
        host: tikv-host-machine-5
  - host: tikv-host-machine-6
    config:
      server.labels:
        zone: z3
        host: tikv-host-machine-6

tiflash_servers:
# z1
  - host: tiflash-host-machine-1
    learner_config:
      server.labels:
        zone: z1
        host: tiflash-host-machine-1
  - host: tiflash-host-machine-2
    learner_config:
      server.labels:
        zone: z1
        host: tiflash-host-machine-2
# z2
  - host: tiflash-host-machine-3
    learner_config:
      server.labels:
        zone: z2
        host: tiflash-host-machine-3
  - host: tiflash-host-machine-4
    learner_config:
      server.labels:
        zone: z2
        host: tiflash-host-machine-4
# z3
  - host: tiflash-host-machine-5
    learner_config:
      server.labels:
        zone: z3
        host: tiflash-host-machine-5
  - host: tiflash-host-machine-6
    learner_config:
      server.labels:
        zone: z3
        host: tiflash-host-machine-6
```

For details, see [Geo-distributed Deployment topology](/geo-distributed-deployment-topology.md).

> **Note:**
>
> If you have not configured `replication.location-labels` in the configuration file, when you deploy a cluster using this topology file, an error might occur. It is recommended that you confirm `replication.location-labels` is configured in the configuration file before deploying a cluster.

## PD schedules based on topology label

PD schedules replicas according to the label layer to make sure that different replicas of the same data are scattered as much as possible.

Take the topology in the previous section as an example.

Assume that the number of cluster replicas is 3 (`max-replicas=3`). Because there are 3 zones in total, PD ensures that the 3 replicas of each Region are respectively placed in z1, z2, and z3. In this way, the TiDB cluster is still available when one zone fails.

Then, assume that the number of cluster replicas is 5 (`max-replicas=5`). Because there are only 3 zones in total, PD cannot guarantee the isolation of each replica at the zone level. In this situation, the PD scheduler will ensure replica isolation at the host level. In other words, multiple replicas of a Region might be distributed in the same zone but not on the same host.

In the case of the 5-replica configuration, if z3 fails or is isolated as a whole, and cannot be recovered after a period of time (controlled by `max-store-down-time`), PD will make up the 5 replicas through scheduling. At this time, only 4 hosts are available. This means that host-level isolation cannot be guaranteed and that multiple replicas might be scheduled to the same host. But if the `isolation-level` value is set to `zone` instead of being left empty, this specifies the minimum physical isolation requirements for Region replicas. That is to say, PD will ensure that replicas of the same Region are scattered among different zones. PD will not perform corresponding scheduling even if following this isolation restriction does not meet the requirement of `max-replicas` for multiple replicas.

If the `isolation-level` setting is set to `zone`, this specifies the minimum isolation requirement for Region replicas at the physical level. In this case, PD will always guarantee that replicas of the same Region are distributed across different zones. Even if following this isolation restriction would not meet the multi-replica requirements of `max-replicas`, PD will not schedule accordingly. Taking a TiKV cluster distributed across three data zones (z1, z2, and z3) as an example, if each Region requires three replicas, PD distributes the three replicas of the same Region to these three data zones respectively. If a power outage occurs in z1 and cannot be recovered after a period of time (30 minutes by default, controlled by [`max-store-down-time`](/pd-configuration-file.md#max-store-down-time)), PD determines that the Region replicas in z1 are no longer available. However, because `isolation-level` is set to `zone`, PD needs to strictly guarantee that different replicas of the same Region will not be scheduled to the same data zone. Because both z2 and z3 already have replicas, PD will not perform any scheduling under the minimum isolation level restriction of `isolation-level`, even if there are only two replicas at this moment.

Similarly, when `isolation-level` is set to `rack`, the minimum isolation level applies to different racks in the same data center. With this configuration, the isolation at the zone layer is guaranteed first if possible. When the isolation at the zone level cannot be guaranteed, PD tries to avoid scheduling different replicas to the same rack in the same zone. The scheduling works similarly when `isolation-level` is set to `host` where PD first guarantees the isolation level of rack, and then the level of host.

In summary, PD maximizes the disaster recovery of the cluster according to the current topology. Therefore, if you want to achieve a certain level of disaster recovery, deploy more machines on different sites according to the topology than the number of `max-replicas`. TiDB also provides mandatory configuration items such as `isolation-level` for you to more flexibly control the topological isolation level of data according to different scenarios.
