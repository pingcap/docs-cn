---
title: Deploying Recommendations
category: deployment
---

## Deployment Recommendations

Before your start, see [TiDB Architecture](../README.md#TiDB-Architecture).

The following table lists the recommended hardware for each component.

| Component | Hardware Resources | # of CPU Cores | Memory | Disk Type | Disk  Size|
| ---- |-------| ------- | -------- | ------- | ------- | 
| TiDB | CPU, Memory | 8+ | 32G+ |  |  | 
| TiKV | CPU, Memory, Disk I/O |8+ | 32G+ | SSD | 200G~500G | 
| PD   | CPU, Memory, Disk I/O |8+ | 16G+ |  | 200G+ |

**Note:** The size of the disk for TiKV does not exceed 500G to avoid long data recovering time in case of disk failure.

## The Overall Deployment Plan

| Component |# and of Instances for Production | # of Instances for Test |
| ----- | ------- | ------- |
| TiDB | 2+, highly available, and add more instances based on the concurrency and throughputs| 1+|
| PD | 3+，highly available | 1+ |
| TiKV | 3+，highly available，and add more instances based on the computing resources and storage capacity |3+|

**Note:** 

- The TiDB instance can be deployed on its own, or share the same node with PD.

- For PD and TiKV, deploy a single instance on one disk to avoid I/O competition which impacts the performance.

- Deploy the TiDB instances and the TiKV instances separately to avoid competing CPU resources which impacts the performance. 


### Example: Deployment for the Production Environment (at least 6 nodes)

|Node1|Node2|Node3|Node4|Node5|Node6|
|----|----|----|----|----|----|
|TiKV1|TiKV2|TiKV3|PD1|PD2|PD3|
|-|-|-|TiDB1|TiDB2|-|

TiDB1 and TiDB2 provide the SQL interface to access data through the load balancing component.


### Example: Deployment for the Test Environment (at least 4 nodes)

|Node1|Node2|Node3|Node4|
|----|----|----|----|
|TiKV1|TiKV2|TiKV3|PD1|
|-|-|-|TiDB1|



