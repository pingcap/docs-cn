---
title: TiDB Scheduler
summary: Learn what is TiDB Scheduler and how it works.
category: reference
---

# TiDB Scheduler

TiDB Scheduler is a TiDB implementation of [Kubernetes scheduler extender](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/scheduler_extender.md). TiDB Scheduler is used to add new scheduling rules to Kubernetes. This document introduces these new scheduling rules and how TiDB Scheduler works.

## TiDB cluster scheduling requirements

A TiDB cluster includes three key components: PD, TiKV, and TiDB. Each consists of multiple nodes: PD is a Raft cluster, and TiKV is a multi-group Raft cluster. PD and TiKV components are stateful. Therefore, the default scheduling rules of the Kubernetes (K8s) scheduler can no longer meet the TiDB cluster scheduling requirements. To extend the K8s scheduling rules, TiDB Scheduler implements the following customized scheduling rules:

### PD component

Scheduling rule 1: Make sure that the number of PD instances scheduled on each node is less than `Replicas / 2`. For example:

| PD cluster size (Replicas) | Maximum number of PD instances scheduled on each node |
| ------------- | ------------- |
| 1  | 1  |
| 2  | 1  |
| 3  | 1  |
| 4  | 1  |
| 5  | 2  |
| ...  |   |

### TiKV component

Scheduling rule 2: If the number of K8s nodes is less than three (In this case, TiKV is not highly available), arbitrary scheduling is supported; otherwise, the number of TiKV instances that can be scheduled on each node must be `ceil(Replicas / 3)`. For example:

| TiKV cluster size (Replicas) | Maximum number of TiKV instances scheduled on each node | Best scheduling distribution |
| ------------- | ------------- | ------------- |
| 3  | 1  | 1,1,1  |
| 4  | 2  | 1,1,2  |
| 5  | 2  | 1,2,2  |
| 6  | 2  | 2,2,2  |
| 7  | 3  | 2,2,3  |
| 8  | 3  | 2,3,3  |
| ...  |   |   |

### TiDB component

Scheduling rule 3: When you perform a rolling upgrade to a TiDB instance, the instance tends to be scheduled back to its original node.

This ensures stable scheduling and is helpful for the scenario of manually mounting Node IP and NodePort to the LB backend. It can reduce the impact on the cluster during the rolling upgrade because you do not need to rearrange the LB when the Node IP is changed after the upgrade.

## How TiDB Scheduler works

![TiDB Scheduler Overview](/media/tidb-scheduler-overview.png)

TiDB Scheduler adds customized scheduling rules by implementing K8s [Scheduler extender](https://github.com/kubernetes/community/blob/master/contributors/design-proposals/scheduling/scheduler_extender.md).

The TiDB Scheduler component is deployed as one or more Pods, though only one Pod is working at the same time. Each Pod has two Containers inside: one Container is a native `kube-scheduler`, and the other is a `tidb-scheduler` implemented as a K8s scheduler extender.

The `.spec.schedulerName` attribute of all Pods created by the TiDB Operator is set to `tidb-scheduler`. This means that the TiDB Scheduler is used for the scheduling.

If you are using a testing cluster and do not require high availability, you can change `.spec.schedulerName` into `default-scheduler` to use the built-in K8s scheduler.

The scheduling process of a Pod is as follows:

- First, `kube-scheduler` pulls all Pods whose `.spec.schedulerName` is `tidb-scheduler`. And Each Pod is filtered using the default K8s scheduling rules.
- Then, `kube-scheduler` sends a request to the `tidb-scheduler` service. Then `tidb-scheduler` filters the sent nodes through the customized scheduling rules (as mentioned above), and returns schedulable nodes to `kube-scheduler`.
- Finally, `kube-scheduler` determines the nodes to be scheduled.

If a Pod cannot be scheduled, see the [troubleshooting document](/tidb-in-kubernetes/troubleshoot.md#the-Pod-is-in-the-Pending-state) to diagnose and solve the issue.
