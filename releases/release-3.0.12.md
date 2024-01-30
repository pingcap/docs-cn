---
title: TiDB 3.0.12 Release Notes
aliases: ['/docs/dev/releases/release-3.0.12/','/docs/dev/releases/3.0.12/']
summary: TiDB 3.0.12 was released on March 16, 2020. It includes compatibility changes, new features, bug fixes, and improvements for TiDB, TiKV, PD, and TiDB Ansible. Some known issues are fixed in new versions, so it is recommended to use the latest 3.0.x version. New features include dynamic loading of replaced certificate files, flow limiting for DDL requests, and support for exiting the TiDB server when binlog write fails. Bug fixes address issues with locking, error message display, decimal point accuracy, and data index inconsistency. Additionally, improvements have been made to TiKV's flow control mechanism and PD's Region information processing.
---

# TiDB 3.0.12 Release Notes

Release date: March 16, 2020

TiDB version: 3.0.12

TiDB Ansible version: 3.0.12

> **Warning:**
>
> Some known issues are found in this version, and these issues are fixed in new versions. It is recommended that you use the latest 3.0.x version.

## Compatibility Changes

+ TiDB
    - Fix the issue of inaccurate timing of prewrite binlog in slow query log. The original timing field was called `Binlog_prewrite_time`. After this fix, the name is changed to `Wait_prewrite_binlog_time`. [#15276](https://github.com/pingcap/tidb/pull/15276)

## New Features

+ TiDB
    - Support dynamic loading of the replaced certificate file by using the `alter instance` statement [#15080](https://github.com/pingcap/tidb/pull/15080) [#15292](https://github.com/pingcap/tidb/pull/15292)
    - Add the `cluster-verify-cn` configuration item. After configuration, the status service can only be used when with the corresponding CN certificate. [#15164](https://github.com/pingcap/tidb/pull/15164)
    - Add a flow limiting feature for DDL requests in each TiDB server to reduce the error reporting frequency of DDL request conflicts [#15148](https://github.com/pingcap/tidb/pull/15148)
    - Support exiting of the TiDB server when binlog write fails [#15339](https://github.com/pingcap/tidb/pull/15339)

+ Tools
    - TiDB Binlog
        - Add the `kafka-client-id` configuration item in Drainer, which supports connecting to Kafka clients to configure the client ID [#929](https://github.com/pingcap/tidb-binlog/pull/929)

## Bug Fixes

+ TiDB
    - Make `GRANT`, `REVOKE` guarantee atomicity when modifying multiple users [#15092](https://github.com/pingcap/tidb/pull/15092)
    - Fix the issue that the locking of pessimistic lock on the partition table failed to lock the correct row [#15114](https://github.com/pingcap/tidb/pull/15114)
    - Make the error message display according to the value of `max-index-length` in the configuration when the index length exceeds the limit [#15130](https://github.com/pingcap/tidb/pull/15130)
    - Fix the incorrect decimal point issue of the `FROM_UNIXTIME` function [#15270](https://github.com/pingcap/tidb/pull/15270)
    - Fix the issue of conflict detection failure or data index inconsistency caused by deleting records written by oneself in a transaction [#15176](https://github.com/pingcap/tidb/pull/15176)

+ TiKV
    - Fix the issue of conflict detection failure or data index inconsistency caused by inserting an existing key into a transaction and then deleting it immediately when disabling the consistency check parameter [#7054](https://github.com/tikv/tikv/pull/7054)
    - Introduce a flow control mechanism in Raftstore to solve the problem that without flow control, it might lead to too slow tracking and cause the cluster to be stuck, and the transaction size might cause frequent reconnection of TiKV connections [#7072](https://github.com/tikv/tikv/pull/7072) [#6993](https://github.com/tikv/tikv/pull/6993)

+ PD
    - Fix the issue of incorrect Region information caused by data race when PD processes Region heartbeats [#2233](https://github.com/pingcap/pd/pull/2233)

+ TiDB Ansible
    - Support deploying multiple Grafana/Prometheus/Alertmanager in a cluster [#1198](https://github.com/pingcap/tidb-ansible/pull/1198)
