---
title: Geo-distributed Deployment topology
summary: Learn the geo-distributed deployment topology of TiDB.
aliases: ['/docs/dev/geo-distributed-deployment-topology/']
---

# Geo-Distributed Deployment Topology

This document takes the typical architecture of three data centers (DC) in two cities as an example, and introduces the geo-distributed deployment architecture and the key configuration. The cities used in this example are Shanghai (referred to as `sha`) and Beijing (referred to as `bja` and `bjb`).

## Topology information

| Instance | Count | Physical machine configuration | BJ IP | SH IP | Configuration |
| :-- | :-- | :-- | :-- | :-- | :-- |
| TiDB | 5 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 <br/> 10.0.1.4 | 10.0.1.5 | Default port <br/> Global directory configuration |
| PD | 5 | 4 VCore 8GB * 1 | 10.0.1.6 <br/> 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | 10.0.1.10 | Default port <br/> Global directory configuration |
| TiKV | 5 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.11 <br/> 10.0.1.12 <br/> 10.0.1.13 <br/> 10.0.1.14 | 10.0.1.15 | Default port <br/> Global directory configuration |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.16 | | Default port <br/> Global directory configuration |

### Topology templates

- [The geo-distributed topology template](https://github.com/pingcap/docs/blob/master/config-templates/geo-redundancy-deployment.yaml)

For detailed descriptions of the configuration items in the above TiDB cluster topology file, see [Topology Configuration File for Deploying TiDB Using TiUP](/tiup/tiup-cluster-topology-reference.md).

### Key parameters

This section describes the key parameter configuration of the TiDB geo-distributed deployment.

#### TiKV parameters

- The gRPC compression format (`none` by default):

    To increase the transmission speed of gRPC packages between geo-distributed target nodes, set this parameter to `gzip`.

    ```yaml
    server.grpc-compression-type: gzip
    ```

- The label configuration:

    Since TiKV is deployed across different data centers, if the physical machines go down, the Raft Group might lose three of the default five replicas, which causes the cluster unavailability. To address this issue, you can configure the labels to enable the smart scheduling of PD, which ensures that the Raft Group does not allow three replicas to be located in TiKV instances on the same machine in the same cabinet of the same data center.

- The TiKV configuration:

    The same host-level label information is configured for the same physical machine.

    ```yaml
    config:
      server.labels:
        zone: bj
        dc: bja
        rack: rack1
        host: host2
    ```

- To prevent remote TiKV nodes from launching unnecessary Raft elections, it is required to increase the minimum and maximum number of ticks that the remote TiKV nodes need to launch an election. The two parameters are set to `0` by default.

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 1000
    raftstore.raft-max-election-timeout-ticks: 1020
    ```

#### PD parameters

- The PD metadata information records the topology of the TiKV cluster. PD schedules the Raft Group replicas on the following four dimensions:

    ```yaml
    replication.location-labels: ["zone","dc","rack","host"]
    ```

- To ensure high availability of the cluster, adjust the number of Raft Group replicas to be `5`:

    ```yaml
    replication.max-replicas: 5
    ```

- Forbid the remote TiKV Raft replica being elected as Leader:

    ```yaml
    label-property:
          reject-leader:
            - key: "dc"
              value: "sha"
    ```

> **Note:**
>
> - You do not need to manually create the `tidb` user in the configuration file. The TiUP cluster component automatically creates the `tidb` user on the target machines. You can customize the user, or keep the user consistent with the control machine.
> - If you configure the deployment directory as a relative path, the cluster will be deployed in the home directory of the user.

[Schedule Replicas by Topology Labels](/schedule-replicas-by-topology-labels.md) further explains the use of labels and the number of Raft Group replicas.
