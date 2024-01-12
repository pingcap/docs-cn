---
title: TiProxy Deployment Topology
summary: Learn the deployment topology of TiProxy based on the minimal TiDB topology.
---

# TiProxy Deployment Topology

This document describes the deployment topology of [TiProxy](/tiproxy/tiproxy-overview.md) based on the minimal TiDB topology.

TiProxy is a L7 proxy server for TiDB, which can balance connections and migrate sessions when possible.

## Topology information

| Instance | Count | Physical machine configuration | IP | Configuration |
| :-- | :-- | :-- | :-- | :-- |
| TiDB | 3 | 16 VCore 32GB * 3 | 10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | Default port <br/> Global directory configuration |
| PD | 3 | 4 VCore 8GB * 3 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | Default port <br/> Global directory configuration |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 3 | 10.0.1.7 <br/> 10.0.1.8 <br/> 10.0.1.9 | Default port <br/> Global directory configuration |
| TiProxy | 3 | 4 VCore 8 GB * 1  | 10.0.1.11 | Default port <br/> Global directory configuration |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.13 | Default port <br/> Global directory configuration |

### Topology templates

For more information about the template for TiProxy, see [The simple template for the TiProxy topology](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiproxy.yaml).

For detailed descriptions of the configuration items in the preceding TiDB cluster topology file, see [Topology Configuration File for Deploying TiDB Using TiUP](/tiup/tiup-cluster-topology-reference.md).

### Key parameters

- The instance level `"-host"` configuration in `tiproxy_servers` only supports IP, not domain name.
- For detailed TiProxy parameter description, see [TiProxy Configuration](/tiproxy/tiproxy-configuration.md).

> **Note:**
>
> - You do not need to manually create the `tidb` user in the configuration file. The TiUP cluster component automatically creates the `tidb` user on the target machines. You can customize the user, or keep the user consistent with the control machine.
> - If you configure the deployment directory as a relative path, the cluster will be deployed in the home directory of the user.
