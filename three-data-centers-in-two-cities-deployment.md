---
title: Three Data Centers in Two Cities Deployment
summary: Learn the deployment solution to three data centers in two cities.
aliases: ['/docs/dev/three-data-centers-in-two-cities-deployment/']
---

# Three Data Centers in Two Cities Deployment

This document introduces the architecture and configuration of the three data centers (DC) in two cities deployment.

## Overview

The architecture of three DCs in two cities is a highly available and disaster tolerant deployment solution that provides a production data center, a disaster recovery center in the same city, and a disaster recovery center in another city. In this mode, the three DCs in two cities are interconnected. If one DC fails or suffers from a disaster, other DCs can still operate well and take over the the key applications or all applications. Compared with the the multi-DC in one city deployment, this solution has the advantage of cross-city high availability and can survive city-level natural disasters.

The distributed database TiDB natively supports the three-DC-in-two-city architecture by using the Raft algorithm, and guarantees the consistency and high availability of data within a database cluster. Because the network latency across DCs in the same city is relatively low, the application traffic can be dispatched to two DCs in the same city, and the traffic load can be shared by these two DCs by controlling the distribution of TiKV Region leaders and PD leaders.

## Deployment architecture

This section takes the example of Seattle and San Francisco to explain the deployment mode of three DCs in two cities for the distributed database of TiDB.

In this example, two DCs (IDC1 and IDC2) are located in Seattle and another DC (IDC3) is located in San Francisco. The network latency between IDC1 and IDC2 is lower than 3 milliseconds. The network latency between IDC3 and IDC1/IDC2 in Seattle is about 20 milliseconds (ISP dedicated network is used).

The architecture of the cluster deployment is as follows:

- The TiDB cluster is deployed to three DCs in two cities: IDC1 in Seattle, IDC2 in Seattle, and IDC3 in San Francisco.
- The cluster has five replicas, two in IDC1, two in IDC2, and one in IDC3. For the TiKV component, each rack has a label, which means that each rack has a replica.
- The Raft protocol is adopted to ensure consistency and high availability of data, which is transparent to users.

![3-DC-in-2-city architecture](/media/three-data-centers-in-two-cities-deployment-01.png)

This architecture is highly available. The distribution of Region leaders is restricted to the two DCs (IDC1 and IDC2) that are in the same city (Seattle). Compared with the three-DC solution in which the distribution of Region leaders is not restricted, this architecture has the following advantages and disadvantages:

- **Advantages**

    - Region leaders are in DCs of the same city with low latency, so the write is faster.
    - The two DCs can provide services at the same time, so the resources usage rate is higher.
    - If one DC fails, services are still available and data safety is ensured.

- **Disadvantages**

    - Because the data consistency is achieved by the Raft algorithm, when two DCs in the same city fail at the same time, only one surviving replica remains in the disaster recovery DC in another city (San Francisco). This cannot meet the requirement of the Raft algorithm that most replicas survive. As a result, the cluster can be temporarily unavailable. Maintenance staff needs to recover the cluster from the one surviving replica and a small amount of hot data that has not been replicated will be lost. But this case is a rare occurrence.
    - Because the ISP dedicated network is used, the network infrastructure of this architecture has a high cost.
    - Five replicas are configured in three DCs in two cities, data redundancy increases, which brings a higher storage cost.

### Deployment details

The configuration of the three DCs in two cities (Seattle and San Francisco) deployment plan is illustrated as follows:

![3-DC-2-city](/media/three-data-centers-in-two-cities-deployment-02.png)

- From the illustration above, you can see that Seattle has two DCs: IDC1 and IDC2. IDC1 has three sets of racks: RAC1, RAC2, and RAC3. IDC2 has two racks: RAC4 and RAC5. The IDC3 DC in San Francisco has the RAC6 rack.
- From the RAC1 rack illustrated above, TiDB and PD services are deployed on the same server. Each of the two TiKV servers are deployed with two TiKV instances (tikv-server). This is similar to RAC2, RAC4, RAC5, and RAC6.
- The TiDB server, the control machine, and the monitoring server are on RAC3. The TiDB server is deployed for regular maintenance and backup. Prometheus, Grafana, and the restore tools are deployed on the control machine and monitoring machine.
- Another backup server can be added to deploy Drainer. Drainer saves binlog data to a specified location by outputting files, to achieve incremental backup.

## Configuration

### Example

See the following `tiup topology.yaml` yaml file for example:

```yaml
# # Global variables are applied to all deployments and used as the default value of
# # the deployments if a specific deployment value is missing.
global
  user: "tidb"
  ssh_port: 22
  deploy_dir: "/data/tidb_cluster/tidb-deploy"
  data_dir: "/data/tidb_cluster/tidb-data"

server_configs:
  tikv:
    server.grpc-compression-type: gzip
  pd:
    replication.location-labels:  ["dc","zone","rack","host"]

pd_servers:
  - host: 10.63.10.10
    name: "pd-10"
  - host: 10.63.10.11
    name: "pd-11"
  - host: 10.63.10.12
    name: "pd-12"
  - host: 10.63.10.13
    name: "pd-13"
  - host: 10.63.10.14
    name: "pd-14"

tidb_servers:
  - host: 10.63.10.10
  - host: 10.63.10.11
  - host: 10.63.10.12
  - host: 10.63.10.13
  - host: 10.63.10.14

tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { dc: "1", zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { dc: "1", zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { dc: "2", zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { dc: "2", zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { dc: "3", zone: "5", rack: "5", host: "34" }
      raftstore.raft-min-election-timeout-ticks: 1000
      raftstore.raft-max-election-timeout-ticks: 1200

monitoring_servers:
  - host: 10.63.10.60

grafana_servers:
  - host: 10.63.10.60

alertmanager_servers:
  - host: 10.63.10.60
```

### Labels design

In the deployment of three DCs in two cities, the label design requires taking availability and disaster recovery into account. It is recommended that you define the four levels (`dc`, `zone`, `rack`, `host`) based on the physical structure of the deployment.

![Label logical definition](/media/three-data-centers-in-two-cities-deployment-03.png)

In the PD configuration, add level information of TiKV labels:

```yaml
server_configs:
  pd:
    replication.location-labels:  ["dc","zone","rack","host"]
```

The configuration of `tikv_servers` is based on the label information of the real physical deployment location of TiKV, which makes it easier for PD to perform global management and scheduling.

```yaml
tikv_servers:
  - host: 10.63.10.30
    config:
      server.labels: { dc: "1", zone: "1", rack: "1", host: "30" }
  - host: 10.63.10.31
    config:
      server.labels: { dc: "1", zone: "2", rack: "2", host: "31" }
  - host: 10.63.10.32
    config:
      server.labels: { dc: "2", zone: "3", rack: "3", host: "32" }
  - host: 10.63.10.33
    config:
      server.labels: { dc: "2", zone: "4", rack: "4", host: "33" }
  - host: 10.63.10.34
    config:
      server.labels: { dc: "3", zone: "5", rack: "5", host: "34" }
```

### Optimize parameter configuration

In the deployment of three DCs in two cities, to optimize performance, you need to not only configure regular parameters, but also adjust component parameters.

- Enable gRPC message compression in TiKV. Because data of the cluster is transmitted in the network, you can enable the gRPC message compression to lower the network traffic.

    ```yaml
    server.grpc-compression-type: gzip
    ```

- Optimize the network configuration of the TiKV node in another city (San Francisco). Modify the following TiKV parameters for IDC3 (alone) in San Francisco and try to prevent the replica in this TiKV node from participating in the Raft election.

    ```yaml
    raftstore.raft-min-election-timeout-ticks: 1000
    raftstore.raft-max-election-timeout-ticks: 1200
    ```

- Configure scheduling. After the cluster is enabled, use the `tiup ctl:v<CLUSTER_VERSION> pd` tool to modify the scheduling policy. Modify the number of TiKV Raft replicas. Configure this number as planned. In this example, the number of replicas is five.

    ```yaml
    config set max-replicas 5
    ```

- Forbid scheduling the Raft leader to IDC3. Scheduling the Raft leader to in another city (IDC3) causes unnecessary network overhead between IDC1/IDC2 in Seattle and IDC3 in San Francisco. The network bandwidth and latency also affect performance of the TiDB cluster.

    ```yaml
    config set label-property reject-leader dc 3
    ```

   > **Note:**
   >
   > Since TiDB 5.2, the `label-property` configuration is not supported by default. To set the replica policy, use the [placement rules](/configure-placement-rules.md).

- Configure the priority of PD. To avoid the situation where the PD leader is in another city (IDC3), you can increase the priority of local PD (in Seattle) and decrease the priority of PD in another city (San Francisco). The larger the number, the higher the priority.

    ```yaml
    member leader_priority PD-10 5
    member leader_priority PD-11 5
    member leader_priority PD-12 5
    member leader_priority PD-13 5
    member leader_priority PD-14 1
    ```
