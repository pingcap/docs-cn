---
title: TiDB 2.1.13 Release Notes
category: Releases
---

# TiDB 2.1.13 Release Notes

Release date: June 21, 2019

TiDB version: 2.1.13

TiDB Ansible version: 2.1.13

## TiDB

- Add a feature to use `SHARD_ROW_ID_BITS` to scatter row IDs when the column contains an `AUTO_INCREMENT` attribute to relieve the hotspot issue [#10788](https://github.com/pingcap/tidb/pull/10788)
- Optimize the lifetime of invalid DDL metadata to speed up recovering the normal execution of DDL operations after upgrading the TiDB cluster [#10789](https://github.com/pingcap/tidb/pull/10789)
- Fix the OOM issue in high concurrent scenarios caused by the failure to quickly release Coprocessor resources, resulted from the `execdetails.ExecDetails` pointer [#10833](https://github.com/pingcap/tidb/pull/10833)
- Add the `update-stats` configuration item to control whether to update statistics [#10772](https://github.com/pingcap/tidb/pull/10772)
- Add the following TiDB-specific syntax to support Region presplit to solve the hotspot issue:
- Add the `PRE_SPLIT_REGIONS` table option [#10863](https://github.com/pingcap/tidb/pull/10863)
- Add the `SPLIT TABLE table_name INDEX index_name` syntax [#10865](https://github.com/pingcap/tidb/pull/10865)
- Add the `SPLIT TABLE [table_name] BETWEEN (min_value...) AND (max_value...) REGIONS [region_num]` syntax [#10882](https://github.com/pingcap/tidb/pull/10882)
- Fix the panic issue caused by the `KILL` syntax in some cases [#10879](https://github.com/pingcap/tidb/pull/10879)
- Improve the compatibility with MySQL for `ADD_DATE` in some cases [#10718](https://github.com/pingcap/tidb/pull/10718)
- Fix the wrong estimation for the selectivity rate of the inner table selection in index join [#10856](https://github.com/pingcap/tidb/pull/10856)

## TiKV

- Fix the issue that incomplete snapshots are generated in the system caused by the iterator not checking the status [#4940](https://github.com/tikv/tikv/pull/4940)
- Add a feature to check the validity for the `block-size` configuration [#4930](https://github.com/tikv/tikv/pull/4930)

## Tools

- TiDB Binlog
    - Fix the wrong offset issue caused by Pump not checking the returned value when it fails to write data [#640](https://github.com/pingcap/tidb-binlog/pull/640)
    - Add the `advertise-addr` configuration in Drainer to support the bridge mode in the container environment [#634](https://github.com/pingcap/tidb-binlog/pull/634)
