---
title: Minimal Deployment Topology
summary: Learn the minimal deployment topology of TiDB clusters.
aliases: ['/docs/dev/minimal-deployment-topology/']
---

# Minimal Deployment Topology

This document describes the minimal deployment topology of TiDB clusters.

## Topology information

| Instance | Count | Physical machine configuration | IP | Configuration |
| :-- | :-- | :-- | :-- | :-- |
| TiDB | 2 | 16 VCore 32 GiB <br/> 100 GiB for storage | 10.0.1.1 <br/> 10.0.1.2 | Default port <br/> Global directory configuration |
| PD | 3 | 4 VCore 8 GiB <br/> 100 GiB for storage |10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | Default port <br/> Global directory configuration |
| TiKV | 3 | 16 VCore 32 GiB <br/> 2 TiB (NVMe SSD) for storage | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | Default port <br/> Global directory configuration |
| Monitoring & Grafana | 1 | 4 VCore 8 GiB <br/> 500 GiB (SSD) for storage | 10.0.1.10 | Default port <br/> Global directory configuration |

### Topology templates

- [The simple template for the minimal topology](https://github.com/pingcap/docs/blob/master/config-templates/simple-mini.yaml)
- [The complex template for the minimal topology](https://github.com/pingcap/docs/blob/master/config-templates/complex-mini.yaml)

For detailed descriptions of the configuration items in the above TiDB cluster topology file, see [Topology Configuration File for Deploying TiDB Using TiUP](/tiup/tiup-cluster-topology-reference.md).

> **Note:**
>
> - You do not need to manually create the `tidb` user in the configuration file. The TiUP cluster component automatically creates the `tidb` user on the target machines. You can customize the user, or keep the user consistent with the control machine.
> - If you configure the deployment directory as a relative path, the cluster will be deployed in the home directory of the user.
