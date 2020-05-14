---
title: TiDB 2.1.12 Release Notes
category: Releases
---

# TiDB 2.1.12 Release Notes

Release date: June 13, 2019

TiDB version: 2.1.12

TiDB Ansible version: 2.1.12

## TiDB

- Fix the issue caused by unmatched data types when using the index query feedback [#10755](https://github.com/pingcap/tidb/pull/10755)
- Fix the issue that the blob column is changed to the text column caused by charset altering in some cases [#10745](https://github.com/pingcap/tidb/pull/10745)
- Fix the issue that the `GRANT` operation in the transaction mistakenly reports "Duplicate Entry" in some cases [#10739](https://github.com/pingcap/tidb/pull/10739)
- Improve the compatibility with MySQL of the following features
    - The `DAYNAME` function [#10732](https://github.com/pingcap/tidb/pull/10732)
    - The `MONTHNAME` function [#10733](https://github.com/pingcap/tidb/pull/10733)
    - Support the 0 value for the `EXTRACT` function when processing `MONTH` [#10702](https://github.com/pingcap/tidb/pull/10702)
    - The `DECIMAL` type can be converted to `TIMESTAMP` or `DATETIME` [#10734](https://github.com/pingcap/tidb/pull/10734)
- Change the column charset while changing the table charset [#10714](https://github.com/pingcap/tidb/pull/10714)
- Fix the overflow issue when converting a decimal to a float in some cases [#10730](https://github.com/pingcap/tidb/pull/10730)
- Fix the issue that some extremely large messages report the "grpc: received message larger than max" error caused by inconsistent maximum sizes of messages sent/received by gRPC of TiDB and TiKV [#10710](https://github.com/pingcap/tidb/pull/10710)
- Fix the panic issue caused by `ORDER BY` not filtering NULL in some cases [#10488](https://github.com/pingcap/tidb/pull/10488)
- Fix the issue that values returned by the `UUID` function might be duplicate when multiple nodes exist [#10711](https://github.com/pingcap/tidb/pull/10711)
- Change the value returned by `CAST(-num as datetime)` from `error` to NULL [#10703](https://github.com/pingcap/tidb/pull/10703)
- Fix the issue that an unsigned histogram meets signed ranges in some cases [#10695](https://github.com/pingcap/tidb/pull/10695)
- Fix the issue that an error is reported mistakenly for reading data when the statistics feedback meets the bigint unsigned primary key [#10307](https://github.com/pingcap/tidb/pull/10307)
- Fix the issue that the result of `Show Create Table` for partitioned tables is not correctly displayed in some cases [#10690](https://github.com/pingcap/tidb/pull/10690)
- Fix the issue that the calculation result of the `GROUP_CONCAT` aggregate function is not correct for some correlated subqueries [#10670](https://github.com/pingcap/tidb/pull/10670)
- Fix the issue that the result is wrongly displayed when the memory table of slow queries parses the slow query log in some cases [#10776](https://github.com/pingcap/tidb/pull/10776)

## PD

- Fix the issue that etcd leader election is blocked in extreme conditions
[#1576](https://github.com/pingcap/pd/pull/1576)

## TiKV

- Fix the issue that Regions are not available during the leader transfer process in extreme conditions [#4799](https://github.com/tikv/tikv/pull/4734)
- Fix the issue that TiKV loses data when the power of the machine fails abnormally, caused by delayed data flush to the disk when receiving snapshots [#4850](https://github.com/tikv/tikv/pull/4850)
