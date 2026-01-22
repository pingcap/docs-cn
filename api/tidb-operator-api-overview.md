---
title: TiDB Operator API Overview
summary: Learn the API of TiDB Operator services.
---

# TiDB Operator API Overview

[TiDB Operator](https://docs.pingcap.com/tidb-in-kubernetes/stable/) is an automatic operation system for TiDB clusters on Kubernetes. It provides full life-cycle management for TiDB including deployment, upgrades, scaling, backup, failover, and configuration changes. With TiDB Operator, TiDB can run seamlessly in the Kubernetes clusters deployed on a public or private cloud.

To manage TiDB clusters on Kubernetes, you can use the following TiDB Operator APIs:

- [Backup](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md#backup>)
- [BackupSchedule](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md#backupschedule>)
- [DMCluster](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md#dmcluster>)
- [Restore](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md#restore>)
- [TidbCluster](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md#tidbcluster>)
- [TidbInitializer](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md#tidbinitializer>)
- [TidbMonitor](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md#tidbmonitor>)

For more information, see [TiDB Operator API Document](<https://github.com/pingcap/tidb-operator/blob/{{{ .tidb-operator-version }}}/docs/api-references/docs.md>).
