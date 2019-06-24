---
title: Cluster Topology Configuration
summary: Learn to configure cluster topology to maximize the capacity for disaster recovery.
category: how-to
aliases: ['/docs/op-guide/location-awareness/']
---

# Cluster Topology Configuration

## Overview

PD schedules according to the topology of the TiKV cluster to maximize the TiKV's capability for disaster recovery.

Before you begin, see [Deploy TiDB Using Ansible (Recommended)](/how-to/deploy/orchestrated/ansible.md) and [Deploy TiDB Using Docker](/how-to/deploy/orchestrated/docker.md).

## TiKV reports the topological information

TiKV reports the topological information to PD according to the startup parameter or configuration of TiKV.

Assuming that the topology has three structures: zone > rack > host, use lables to specify the following information:

Startup parameter:

```
tikv-server --labels zone=<zone>,rack=<rack>,host=<host>
```

Configuration:

``` toml
[server]
labels = "zone=<zone>,rack=<rack>,host=<host>"
```

## PD understands the TiKV topology

PD gets the topology of TiKV cluster through the PD configuration.

``` toml
[replication]
max-replicas = 3
location-labels = ["zone", "rack", "host"]
```

`location-labels` needs to correspond to the TiKV `labels` name so that PD can understand that the `labels` represents the TiKV topology.

## PD schedules based on the TiKV topology

PD makes optimal scheduling according to the topological information. You just need to care about what kind of topology can achieve the desired effect.

If you use 3 replicas and hope that the TiDB cluster is always highly available even when a data zone goes down, you need at least 4 data zones.

Assume that you have 4 data zones, each zone has 2 racks, and each rack has 2 hosts. You can start 2 TiKV instances on each host:

```
# zone=z1
tikv-server --labels zone=z1,rack=r1,host=h1
tikv-server --labels zone=z1,rack=r1,host=h2
tikv-server --labels zone=z1,rack=r2,host=h1
tikv-server --labels zone=z1,rack=r2,host=h2

# zone=z2
tikv-server --labels zone=z2,rack=r1,host=h1
tikv-server --labels zone=z2,rack=r1,host=h2
tikv-server --labels zone=z2,rack=r2,host=h1
tikv-server --labels zone=z2,rack=r2,host=h2

# zone=z3
tikv-server --labels zone=z3,rack=r1,host=h1
tikv-server --labels zone=z3,rack=r1,host=h2
tikv-server --labels zone=z3,rack=r2,host=h1
tikv-server --labels zone=z3,rack=r2,host=h2

# zone=z4
tikv-server --labels zone=z4,rack=r1,host=h1
tikv-server --labels zone=z4,rack=r1,host=h2
tikv-server --labels zone=z4,rack=r2,host=h1
tikv-server --labels zone=z4,rack=r2,host=h2
```

In other words, 16 TiKV instances are distributed across 4 data zones, 8 racks and 16 machines.

In this case, PD will schedule different replicas of each datum to different data zones.

- If one of the data zones goes down, the high availability of the TiDB cluster is not affected.
- If the data zone cannot recover within a period of time, PD will remove the replica from this data zone.

To sum up, PD maximizes the disaster recovery of the cluster according to the current topology. Therefore, if you want to reach a certain level of disaster recovery, deploy many machines in different sites according to the topology. The number of machines must be more than the number of `max-replicas`.
