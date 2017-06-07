---
title: Deploying Recommendations
category: deployment
---

## Deploying Recommendations

To learn the TiDB architecture, see [TiDB Architecture](../README.md#TiDB-Architecture).

The following table lists the recommended hardware for each component.

| Component | # of CPU Cores | Memory | Disk Type | Disk | # of Instances |
| ---- | ------- | -------- | ------- | ------- | --------- |
| TiDB | 8+ | 16G+ |  |  | 2+ |
| PD   | 8+ | 16G+ |  | 200G+ | 3+ |
| TiKV | 8+ | 16G+ | SSD | 200G~500G | 3+ |


**Deployment tips:**

* Deploy only one TiKV instance on one disk.

* Don’t deploy the PD instance and TiKV instance on the same disk

* The TiDB instance can be deployed to the same disk with either PD or TiKV.

* The size of the disk for TiKV does not exceed 500G. This is to avoid a long data recovering time in case of disk failure.

* Use SSD for TiKV.
