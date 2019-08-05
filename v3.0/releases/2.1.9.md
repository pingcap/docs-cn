---
title: TiDB 2.1.9 Release Notes
category: Releases
aliases: ['/docs/releases/2.1.9/']
---

# TiDB 2.1.9 Release Notes

Release date: May 6, 2019

TiDB version: 2.1.9

TiDB-Ansible version: 2.1.9

## TiDB

- Fix compatibility of the `MAKETIME` function when unsigned type overflows [#10089](https://github.com/pingcap/tidb/pull/10089)
- Fix the stack overflow caused by constant folding in some cases [#10189](https://github.com/pingcap/tidb/pull/10189)
- Fix the privilege check issue for `Update` when an alias exists in some cases [#10157](https://github.com/pingcap/tidb/pull/10157), [#10326](https://github.com/pingcap/tidb/pull/10326)
- Track and control memory usage in DistSQL [#10197](https://github.com/pingcap/tidb/pull/10197)
- Support specifying collation as `utf8mb4_0900_ai_ci` [#10201](https://github.com/pingcap/tidb/pull/10201)
- Fix the wrong result issue of the `MAX` function when the primary key is of the Unsigned type [#10209](https://github.com/pingcap/tidb/pull/10209)
- Fix the issue that NULL values can be inserted into NOT NULL columns in the non-strict SQL mode [#10254](https://github.com/pingcap/tidb/pull/10254)
- Fix the wrong result issue of the `COUNT` function when multiple columns exist in `DISTINCT` [#10270](https://github.com/pingcap/tidb/pull/10270)
- Fix the panic issue occurred when `LOAD DATA` parses irregular CSV files [#10269](https://github.com/pingcap/tidb/pull/10269)
- Ignore the overflow error when the outer and inner join key types are inconsistent in `Index Lookup Join` [#10244](https://github.com/pingcap/tidb/pull/10244)
- Fix the issue that a statement is wrongly judged as point-get in some cases [#10299](https://github.com/pingcap/tidb/pull/10299)
- Fix the wrong result issue when the time type does not convert the time zone in some cases [#10345](https://github.com/pingcap/tidb/pull/10345)
- Fix the issue that TiDB character set cases are inconsistent in some cases [#10354](https://github.com/pingcap/tidb/pull/10354)
- Support controlling the number of rows returned by operator [#9166](https://github.com/pingcap/tidb/issues/9166)
    - Selection & Projection [#10110](https://github.com/pingcap/tidb/pull/10110)
    - `StreamAgg` & `HashAgg` [#10133](https://github.com/pingcap/tidb/pull/10133)
    - `TableReader` & `IndexReader` & `IndexLookup` [#10169](https://github.com/pingcap/tidb/pull/10169)
- Improve the slow query log
    - Add `SQL Digest` to distinguish similar SQL [#10093](https://github.com/pingcap/tidb/pull/10093)
    - Add version information of statistics used by slow query statements [#10220](https://github.com/pingcap/tidb/pull/10220)
    - Show memory consumption of a statement in slow query log [#10246](https://github.com/pingcap/tidb/pull/10246)
    - Adjust the output format of Coprocessor related information so it can be parsed by pt-query-digest [#10300](https://github.com/pingcap/tidb/pull/10300)
    - Fix the `#` character issue in slow query statements [#10275](https://github.com/pingcap/tidb/pull/10275)
    - Add some information columns to the memory table of slow query statements  [#10317](https://github.com/pingcap/tidb/pull/10317)
    - Add the transaction commit time to slow query log [#10310](https://github.com/pingcap/tidb/pull/10310)
    - Fix the issue some time formats cannot be parsed by pt-query-digest [#10323](https://github.com/pingcap/tidb/pull/10323)

## PD

- Support the GetOperator service [#1514](https://github.com/pingcap/pd/pull/1514)

## TiKV

- Fix potential quorum changes when transferring leader [#4604](https://github.com/tikv/tikv/pull/4604)

## Tools

- TiDB Binlog
    - Fix the issue that data replication is interrupted because data in the unsigned int type of primary key column are minus numbers [#574](https://github.com/pingcap/tidb-binlog/pull/574)
    - Remove the compression option when the downstream is `pb` and change the downstream name from `pb` to `file` [#597](https://github.com/pingcap/tidb-binlog/pull/575)
    - Fix the bug that Reparo introduced in 2.1.7 generates wrong `UPDATE` statements [#576](https://github.com/pingcap/tidb-binlog/pull/576)
- TiDB Lightning
    - Fix the bug that the bit type of column data is incorrectly parsed by the parser [#164](https://github.com/pingcap/tidb-lightning/pull/164)
    - Fill the lacking column data in dump files using row id or the default column value [#174](https://github.com/pingcap/tidb-lightning/pull/174)
    - Fix the Importer bug that some SST files fail to be imported but it still returns successful import result [#4566](https://github.com/tikv/tikv/pull/4566)
    - Support setting a speed limit in Importer when uploading SST files to TiKV [#4607](https://github.com/tikv/tikv/pull/4607)
    - Change Importer RocksDB SST compression method to `lz4` to reduce CPU consumption [#4624](https://github.com/tikv/tikv/pull/4624)
- sync-diff-inspector
    - Support checkpoint [#227](https://github.com/pingcap/tidb-tools/pull/227)

## TiDB-Ansible

- Update links in tidb-ansible documentation according to docs refactoring [#740](https://github.com/pingcap/tidb-ansible/pull/740), [#741](https://github.com/pingcap/tidb-ansible/pull/741)
- Remove the `enable_slow_query_log` parameter in the `inventory.ini` file and output the slow query log to a separate log file by default [#742](https://github.com/pingcap/tidb-ansible/pull/742)
