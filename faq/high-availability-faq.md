---
title: High Availability FAQs
summary: Learn about the FAQs related to high availability of TiDB.
---

# High Availability FAQs

This document summarizes the FAQs related to high availability of TiDB.

## How is TiDB strongly consistent?

Data is redundantly replicated between TiKV nodes using the [Raft consensus algorithm](https://raft.github.io/) to ensure recoverability when a node failure occurs.

At the bottom layer, TiKV uses a model of replication log + State Machine to replicate data. For the write requests, the data is written to a Leader and the Leader then replicates the command to its Followers in the form of log. When the majority of nodes in the cluster receive this log, this log is committed and can be applied into the State Machine.

## What's the recommended solution for the deployment of three geo-distributed data centers?

The architecture of TiDB guarantees that it fully supports geo-distribution and multi-activeness. Your data and applications are always-on. All the outages are transparent to your applications and your data can recover automatically. The operation depends on the network latency and stability. It is recommended to keep the latency within 5ms. Currently, TiDB already has similar use cases. For details, see [Three Data Centers in Two Cities Deployment](/three-data-centers-in-two-cities-deployment.md).
