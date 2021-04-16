---
title: TiFlash Deployment Topology
summary: Learn the deployment topology of TiFlash based on the minimal TiDB topology.
aliases: ['/docs/dev/tiflash-deployment-topology/']
---

# TiFlash Deployment Topology

This document describes the deployment topology of [TiFlash](/tiflash/tiflash-overview.md) based on the minimal TiDB topology.

TiFlash is a columnar storage engine, and gradually becomes the standard cluster topology. It is suitable for real-time HTAP applications.

## Topology information

| Instance | Count | Physical machine configuration | IP | Configuration |
| :-- | :-- | :-- | :-- | :-- |
| TiDB | 3 | 16 VCore 32GB * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | Default port <br/> Global directory configuration |
| PD | 3 | 4 VCore 8GB * 1 | 10.0.1.4 <br/> 10.0.1.5 <br/> 10.0.1.6 | Default port <br/> Global directory configuration |
| TiKV | 3 | 16 VCore 32GB 2TB (nvme ssd) * 1 | 10.0.1.1 <br/> 10.0.1.2 <br/> 10.0.1.3 | Default port <br/> Global directory configuration |
| TiFlash | 1 | 32 VCore 64 GB 2TB (nvme ssd) * 1  | 10.0.1.10 | Default port <br/> Global directory configuration |
| Monitoring & Grafana | 1 | 4 VCore 8GB * 1 500GB (ssd) | 10.0.1.10 | Default port <br/> Global directory configuration |

### Topology templates

- [The simple template for the TiFlash topology](https://github.com/pingcap/docs/blob/master/config-templates/simple-tiflash.yaml)
- [The complex template for the TiFlash topology](https://github.com/pingcap/docs/blob/master/config-templates/complex-tiflash.yaml)

For detailed descriptions of the configuration items in the above TiDB cluster topology file, see [Topology Configuration File for Deploying TiDB Using TiUP](/tiup/tiup-cluster-topology-reference.md).

### Key parameters

- To enable the [Placement Rules](/configure-placement-rules.md) feature of PD, set the value of `replication.enable-placement-rules` in the configuration template to `true`.
- The instance level `"-host"` configuration in `tiflash_servers` only supports IP, not domain name.
- For detailed TiFlash parameter description, see [TiFlash Configuration](/tiflash/tiflash-configuration.md).

> **Note:**
>
> - You do not need to manually create the `tidb` user in the configuration file. The TiUP cluster component automatically creates the `tidb` user on the target machines. You can customize the user, or keep the user consistent with the control machine.
> - If you configure the deployment directory as a relative path, the cluster will be deployed in the home directory of the user.
