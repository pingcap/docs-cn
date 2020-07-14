---
title: TiDB 3.1 Beta.2 Release Notes
aliases: ['/docs/dev/releases/release-3.1.0-beta.2/','/docs/dev/releases/3.1.0-beta.2/']
---

# TiDB 3.1 Beta.2 Release Notes

Release date: March 9, 2020

TiDB version: 3.1.0-beta.2

TiDB Ansible version: 3.1.0-beta.2

> **Warning:**
>
> Some known issues are found in this version, and these issues are fixed in new versions. It is recommended that you use the latest 3.1.x version.

## Compatibility Changes

+ Tools
    - TiDB Lightning
        - Use the default configurations specified in the [TiDB Lightning Configuration](/tidb-lightning/tidb-lightning-configuration.md) for certain items not configured in the configuration file [#255](https://github.com/pingcap/tidb-lightning/pull/255)
        - Add the `--tidb-password` CLI parameter to set the TiDB password [#253](https://github.com/pingcap/tidb-lightning/pull/253)

## New Features

+ TiDB
    - Support adding the `AutoRandom` keyword in the column attribute to enable TiDB to automatically assign random integers to the primary key, which avoids the write hot spot caused by the `AUTO_INCREMENT` primary key [#14555](https://github.com/pingcap/tidb/pull/14555)
    - Support creating or deleting column store replicas through DDL statements [#14537](https://github.com/pingcap/tidb/pull/14537)
    - Add the feature that the optimizer can independently select different storage engines [#14537](https://github.com/pingcap/tidb/pull/14537)
    - Add the feature that the SQL hint supports different storage engines [#14537](https://github.com/pingcap/tidb/pull/14537)
    - Support reading data from followers by using the `tidb_replica_read` system variable [#13464](https://github.com/pingcap/tidb/pull/13464)
+ TiKV
    - Raftstore
        - Add the `peer_address` parameter to connect other nodes to the TiKV server [#6491](https://github.com/tikv/tikv/pull/6491)
        - Add the `read_index` and `read_index_resp` monitoring metrics to monitor the number of `ReadIndex` requests [#6610](https://github.com/tikv/tikv/pull/6610)
+ PD Client
    - Support reporting statistics of local threads to PD [#6605](https://github.com/tikv/tikv/pull/6605)
+ Backup
    - Replace the `RocksIOLimiter` flow control library with Rust’s `async-speed-limit` flow control library to eliminate extra memory copies when backing up a file [#6462](https://github.com/tikv/tikv/pull/6462)
+ PD
    - Tolerate backslash in the location label name [#2084](https://github.com/pingcap/pd/pull/2084)
+ TiFlash
    - Initial release
+ TiDB Ansible
    - Support deploying multiple Grafana/Prometheus/Alertmanager in one cluster [#1143](https://github.com/pingcap/tidb-ansible/pull/1143)
    - Support deploying the TiFlash component [#1148](https://github.com/pingcap/tidb-ansible/pull/1148)
    - Add monitoring metrics related to the TiFlash component [#1152](https://github.com/pingcap/tidb-ansible/pull/1152)

## Bug Fixes

+ TiKV
    - Raftstore
        - Fix the issue that the read requests cannot be processed because data is not properly read from Hibernate Regions [#6450](https://github.com/tikv/tikv/pull/6450)
        - Fix the panic issue caused by the `ReadIndex` requests during the leader transfer process [#6613](https://github.com/tikv/tikv/pull/6613)
        - Fix the issue that Hibernate Regions are not correctly awakened in some special conditions [#6730](https://github.com/tikv/tikv/pull/6730) [#6737](https://github.com/tikv/tikv/pull/6737) [#6972](https://github.com/tikv/tikv/pull/6972)
    - Backup
        - Fix the inconsistent data index during the restoration caused by the backup of the extra data [#6659](https://github.com/tikv/tikv/pull/6659)
        - Fix the panic caused by incorrectly processing the deleted values during the backup [#6726](https://github.com/tikv/tikv/pull/6726)
+ PD
    - Fix the panic occurred because the rule checker fails to assign stores to Regions [#2161](https://github.com/pingcap/pd/pull/2161)
+ Tools
    - TiDB Lightning
        - Fix the bug that the web interface does not work outside the Server mode [#259](https://github.com/pingcap/tidb-lightning/pull/259)
    - BR (Backup and Restore)
        - Fix the issue that BR cannot exit in time due to an unrecoverable error it encounters when restoring data [#152](https://github.com/pingcap/br/pull/152)
+ TiDB Ansible
    - Fix the issue that the rolling update command fails because the PD Leader cannot be obtained in some scenarios [#1122](https://github.com/pingcap/tidb-ansible/pull/1122)
