---
title: TiDB 4.0.0 Beta.2 Release Notes
aliases: ['/docs/dev/releases/release-4.0.0-beta.2/','/docs/dev/releases/4.0.0-beta.2/']
---

# TiDB 4.0.0 Beta.2 Release Notes

Release date: March 18, 2020

TiDB version: 4.0.0-beta.2

TiDB Ansible version: 4.0.0-beta.2

## Compatibility Changes

+ Tools
    - TiDB Binlog
        - Fix the issue that the system returns an error and exits when `disable-dispatch` and `disable-causality` are configured in Drainer [#915](https://github.com/pingcap/tidb-binlog/pull/915)

## New Features

+ TiKV
    - Support persisting the dynamically updated configuration into the hardware disk [#6684](https://github.com/tikv/tikv/pull/6684)

+ PD
    - Support persisting the dynamically updated configuration into the hardware disk [#2153](https://github.com/pingcap/pd/pull/2153)

+ Tools
    - TiDB Binlog
        - Support the bidirectional data replication between TiDB clusters [#879](https://github.com/pingcap/tidb-binlog/pull/879) [#903](https://github.com/pingcap/tidb-binlog/pull/903)
    - TiDB Lightning
        - Support the TLS configuration [#40](https://github.com/tikv/importer/pull/40) [#270](https://github.com/pingcap/tidb-lightning/pull/270)
    - TiCDC
        - Initial release of the change data capture (CDC), providing the following features:
            - Support capturing changed data from TiKV
            - Support replicating the changed data from TiKV to MySQL compatible databases, and guarantee the eventual data consistency
            - Support replicating the changed data to Kafka, and guarantee either the eventual data consistency or the row-level orderliness
            - Provide process-level high availability
    - Backup & Restore (BR)
        - Enable experimental features such as incremental backup and backing up files to Amazon S3 [#175](https://github.com/pingcap/br/pull/175)

+ TiDB Ansible
    - Support injecting the node information to etcd [#1196](https://github.com/pingcap/tidb-ansible/pull/1196)
    - Support deploying TiDB services on the ARM platform [#1204](https://github.com/pingcap/tidb-ansible/pull/1204)

## Bug Fixes

+ TiKV
    - Fix the panic issue that might occur when meeting empty short values during the backup [#6718](https://github.com/tikv/tikv/pull/6718)
    - Fix the issue that Hibernate Regions might not be correctly awakened in some cases [#6772](https://github.com/tikv/tikv/pull/6672) [#6648](https://github.com/tikv/tikv/pull/6648) [#6376](https://github.com/tikv/tikv/pull/6736)

+ PD
    - Fix the panic issue that the rule checker fails to allocate stores to Regions [#2160](https://github.com/pingcap/pd/pull/2160)
    - Fix the issue that after the dynamic configuration is enabled, the configuration might have replication delay when the Leader is being switched [#2154](https://github.com/pingcap/pd/pull/2154)

+ Tools
    - Backup & Restore (BR)
        - Fix the issue that BR might fail to restore data of a large size because PD cannot process large-sized data [#167](https://github.com/pingcap/br/pull/167)
        - Fix the BR failure occurred because the BR version is not compatible with the TiDB version [#186](https://github.com/pingcap/br/pull/186)
        - Fix the BR failure occurred because the BR version is not compatible with TiFlash [#194](https://github.com/pingcap/br/pull/194)
