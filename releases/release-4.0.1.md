---
title: TiDB 4.0.1 Release Notes
aliases: ['/docs/dev/releases/release-4.0.1/']
---

# TiDB 4.0.1 Release Notes

Release date: June 12, 2020

TiDB version: 4.0.1

## New Features

+ TiKV

    - Add the `--advertise-status-addr` start flag to specify the status address to advertise [#8046](https://github.com/tikv/tikv/pull/8046)

+ PD

    - Support the internal proxy for the built-in TiDB Dashboard [#2511](https://github.com/pingcap/pd/pull/2511)
    - Support setting a custom timeout for PD client [#2509](https://github.com/pingcap/pd/pull/2509)

+ TiFlash

    - Support the TiDB new collation framework
    - Support pushing down the `If`/`BitAnd/BitOr`/`BitXor/BitNot`/`Json_length` functions to TiFlash
    - Support the Resolve Lock logic for large transactions in TiFlash

+ Tools

    - Backup & Restore (BR)

        - Add a version check when starting BR to avoid the issue that BR and the TiDB cluster are incompatible [#311](https://github.com/pingcap/br/pull/311)

## Bug Fixes

+ TiKV

    - Fix the issue that the `use-unified-pool` configuration in the startup log is incorrectly printed [#7946](https://github.com/tikv/tikv/pull/7946)
    - Fix the issue that the tikv-ctl does not support relative path [#7963](https://github.com/tikv/tikv/pull/7963)
    - Fix the bug that the monitoring metric of Point Selects is inaccurate [#8033](https://github.com/tikv/tikv/pull/8033)
    - Fix the issue that a peer might not be destroyed after the network isolation disappears [#8006](https://github.com/tikv/tikv/pull/8006)
    - Fix the issue that a request for read index might get outdated commit index [#8043](https://github.com/tikv/tikv/pull/8043)
    - Improve the reliability of backup and restore with S3 and GCS storages [#7917](https://github.com/tikv/tikv/pull/7917)

+ PD

    - Prevent misconfiguration of Placement Rules in some situations [#2516](https://github.com/pingcap/pd/pull/2516)
    - Fix the issue that deleting the Placement Rule might cause panic [#2515](https://github.com/pingcap/pd/pull/2515)
    - Fix a bug that the store information cannot be obtained when the store's used size is zero [#2474](https://github.com/pingcap/pd/pull/2474)

+ TiFlash

    - Fix the issue that default value of the `bit` type column in TiFlash is incorrectly parsed
    - Fix the miscalculation of `1970-01-01 00:00:00 UTC` in some timezones in TiFlash
