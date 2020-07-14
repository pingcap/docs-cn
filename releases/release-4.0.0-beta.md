---
title: TiDB 4.0 Beta Release Notes
aliases: ['/docs/dev/releases/release-4.0.0-beta/','/docs/dev/releases/4.0.0-beta/']
---

# TiDB 4.0 Beta Release Notes

Release date: January 17, 2020

TiDB version: 4.0.0-beta

TiDB Ansible version: 4.0.0-beta

## TiDB

+ Print the log or cancel the SQL execution when the memory used during the execution of `INSERT`/`REPLACE`/`DELETE`/`UPDATE` exceeds the limit specified by the `MemQuotaQuery` configuration item. The actual behavior depends on the `OOMAction` configuration. [#14179](https://github.com/pingcap/tidb/pull/14179) [#14289](https://github.com/pingcap/tidb/pull/14289) [#14299](https://github.com/pingcap/tidb/pull/14299)
+ Increase the accuracy of calculating the cost of `Index Join` by considering the row counts of both driving tables and driven tables [#12085](https://github.com/pingcap/tidb/pull/12085)
+ Add 15 SQL hints to control the behavior of the optimizer and make the optimizer more stable
    - [#11253](https://github.com/pingcap/tidb/pull/11253) [#11364](https://github.com/pingcap/tidb/pull/11364) [#11673](https://github.com/pingcap/tidb/pull/11673) [#11740](https://github.com/pingcap/tidb/pull/11740) [#11746](https://github.com/pingcap/tidb/pull/11746)
    - [#11809](https://github.com/pingcap/tidb/pull/11809) [#11996](https://github.com/pingcap/tidb/pull/11996) [#12043](https://github.com/pingcap/tidb/pull/12043) [#12059](https://github.com/pingcap/tidb/pull/12059) [#12246](https://github.com/pingcap/tidb/pull/12246)
    - [#12382](https://github.com/pingcap/tidb/pull/12382)
+ Improve the performance when the columns involved in a query can be fully covered by indexes [#12022](https://github.com/pingcap/tidb/pull/12022)
+ Improve the performance of table query by supporting the Index Merge feature [#10121](https://github.com/pingcap/tidb/pull/10121) [#10512](https://github.com/pingcap/tidb/pull/10512) [#11245](https://github.com/pingcap/tidb/pull/11245) [#12225](https://github.com/pingcap/tidb/pull/12225) [#12248](https://github.com/pingcap/tidb/pull/12248) [#12305](https://github.com/pingcap/tidb/pull/12305) [#12843](https://github.com/pingcap/tidb/pull/12843)
+ Improve the performance of Range calculation and reduce the CPU overhead by caching index results and eliminating duplicate results [#12856](https://github.com/pingcap/tidb/pull/12856)
+ Decouple the level of slow logs from the level of ordinary logs [#12359](https://github.com/pingcap/tidb/pull/12359)
+ Add the `oom-use-tmp-storage` parameter (`true` by default) to control whether to use temporary files to cache intermediate results when the memory usage for the execution of a single SQL statement exceeds `mem-quota-query` and the SQL contains `Hash Join` [#11832](https://github.com/pingcap/tidb/pull/11832) [#11937](https://github.com/pingcap/tidb/pull/11937) [#12116](https://github.com/pingcap/tidb/pull/12116) [#12067](https://github.com/pingcap/tidb/pull/12067)
+ Support using `create index`/`alter table` to create expression index and using `drop index` to drop expression index [#14117](https://github.com/pingcap/tidb/pull/14117)
+ Increase the default value of the `query-log-max-len` parameter to `4096` to reduce the number of truncated SQL outputs. This parameter can be adjusted dynamically. [#12491](https://github.com/pingcap/tidb/pull/12491)
+ Support adding the `AutoRandom` keyword in the column attribute to control whether the system automatically assigns a random integer to the primary key, which avoids the hotspot problem caused by the `AUTO_INCREMENT` primary key [#13127](https://github.com/pingcap/tidb/pull/13127)
+ Support Table Locks [#11038](https://github.com/pingcap/tidb/pull/11038)
+ Support using the `LIKE` or `WHERE` clause in `ADMIN SHOW DDL JOBS` for conditional filtering [#12484](https://github.com/pingcap/tidb/pull/12484)
+ Add the `TIDB_ROW_ID_SHARDING_INFO` column in the `information_schema.tables` table to output the `RowID` scattering information (for example, the value of the `SHARD_ROW_ID_BITS` column in table `A` is `"SHARD_BITS={bit_number}"`) [#13418](https://github.com/pingcap/tidb/pull/13418)
+ Optimize the error code of SQL error messages to avoid the situation that the `ERROR 1105 (HY000)` code is used for multiple error messages (the `Unknown Error` type)
    - [#14002](https://github.com/pingcap/tidb/pull/14002) [#13874](https://github.com/pingcap/tidb/pull/13874) [#13733](https://github.com/pingcap/tidb/pull/13733) [#13654](https://github.com/pingcap/tidb/pull/13654) [#13646](https://github.com/pingcap/tidb/pull/13646)
    - [#13540](https://github.com/pingcap/tidb/pull/13540) [#13366](https://github.com/pingcap/tidb/pull/13366) [#13329](https://github.com/pingcap/tidb/pull/13329) [#13300](https://github.com/pingcap/tidb/pull/13300) [#13233](https://github.com/pingcap/tidb/pull/13233)
    - [#13033](https://github.com/pingcap/tidb/pull/13033) [#12866](https://github.com/pingcap/tidb/pull/12866) [#14054](https://github.com/pingcap/tidb/pull/14054)
+ Convert a narrow data range of the discrete type into `point set` and use CM-Sketch to improve the estimation accuracy when estimating the number of rows [#11524](https://github.com/pingcap/tidb/pull/11524)
+ Extract the `TopN` information from CM-Sketch for normal `Analyze` and separately maintain the frequently occurring values [#11409](https://github.com/pingcap/tidb/pull/11409)
+ Support dynamically adjusting the depth and width of CM-Sketch and the number of `TopN` information [#11278](https://github.com/pingcap/tidb/pull/11278)
+ Support automatically capturing and evolving SQL Binding [#13199](https://github.com/pingcap/tidb/pull/13199) [#12434](https://github.com/pingcap/tidb/pull/12434)
+ Optimize the encoding format of communication with TiKV by using `Chunk` to improve communication performance [#12023](https://github.com/pingcap/tidb/pull/12023) [#12536](https://github.com/pingcap/tidb/pull/12536) [#12613](https://github.com/pingcap/tidb/pull/12613) [#12621](https://github.com/pingcap/tidb/pull/12621) [#12899](https://github.com/pingcap/tidb/pull/12899) [#13060](https://github.com/pingcap/tidb/pull/13060) [#13349](https://github.com/pingcap/tidb/pull/13349)
+ Support the new row store format to improve the performance of the wide table [#12634](https://github.com/pingcap/tidb/pull/12634)
+ Optimize the `Recover Binlog` interface to ensure waiting all transactions to be committed before returning to the client [#13740](https://github.com/pingcap/tidb/pull/13740)
+ Support querying the binlog statuses enabled by TiDB servers in the cluster through the HTTP `info/all` interface [#13025](https://github.com/pingcap/tidb/pull/13025)
+ Support the MySQL-compatible `Read Committed` transaction isolation level when using the pessimistic transaction mode [#14087](https://github.com/pingcap/tidb/pull/14087)
+ Support large-sized transactions. The transaction size is limited by the size of the physical memory.
    - [#11999](https://github.com/pingcap/tidb/pull/11999) [#11986](https://github.com/pingcap/tidb/pull/11986) [#11974](https://github.com/pingcap/tidb/pull/11974) [#11817](https://github.com/pingcap/tidb/pull/11817) [#11807](https://github.com/pingcap/tidb/pull/11807)
    - [#12133](https://github.com/pingcap/tidb/pull/12133) [#12223](https://github.com/pingcap/tidb/pull/12223) [#12980](https://github.com/pingcap/tidb/pull/12980) [#13123](https://github.com/pingcap/tidb/pull/13123) [#13299](https://github.com/pingcap/tidb/pull/13299)
    - [#13432](https://github.com/pingcap/tidb/pull/13432) [#13599](https://github.com/pingcap/tidb/pull/13599)
+ Improve the stability of `Kill` [#10841](https://github.com/pingcap/tidb/pull/10841)
+ Support hexadecimal and binary expressions as separators in `LOAD DATA` [#11029](https://github.com/pingcap/tidb/pull/11029)
+ Improve the performance of `IndexLookupJoin` and reduce memory consumption during execution by splitting `IndexLookupJoin` into `IndexHashJoin` and `IndexMergeJoin` [#8861](https://github.com/pingcap/tidb/pull/8861) [#12139](https://github.com/pingcap/tidb/pull/12139) [#12349](https://github.com/pingcap/tidb/pull/12349) [#13238](https://github.com/pingcap/tidb/pull/13238) [#13451](https://github.com/pingcap/tidb/pull/13451) [#13714](https://github.com/pingcap/tidb/pull/13714)
+ Fix several issues relating to RBAC [#13896](https://github.com/pingcap/tidb/pull/13896) [#13820](https://github.com/pingcap/tidb/pull/13820) [#13940](https://github.com/pingcap/tidb/pull/13940) [#14090](https://github.com/pingcap/tidb/pull/14090) [#13940](https://github.com/pingcap/tidb/pull/13940) [#13014](https://github.com/pingcap/tidb/pull/13014)
+ Fix the issue that `VIEW` cannot be created because the `SELECT` statement contains `union` [#12595](https://github.com/pingcap/tidb/pull/12595)
+ Fix several issues relating to the `CAST` function
    - [#12858](https://github.com/pingcap/tidb/pull/12858) [#11968](https://github.com/pingcap/tidb/pull/11968) [#11640](https://github.com/pingcap/tidb/pull/11640) [#11483](https://github.com/pingcap/tidb/pull/11483) [#11493](https://github.com/pingcap/tidb/pull/11493)
    - [#11376](https://github.com/pingcap/tidb/pull/11376) [#11355](https://github.com/pingcap/tidb/pull/11355) [#11114](https://github.com/pingcap/tidb/pull/11114) [#14405](https://github.com/pingcap/tidb/pull/14405) [#14323](https://github.com/pingcap/tidb/pull/14323)
    - [#13837](https://github.com/pingcap/tidb/pull/13837) [#13401](https://github.com/pingcap/tidb/pull/13401) [#13334](https://github.com/pingcap/tidb/pull/13334) [#12652](https://github.com/pingcap/tidb/pull/12652) [#12864](https://github.com/pingcap/tidb/pull/12864)
    - [#12623](https://github.com/pingcap/tidb/pull/12623) [#11989](https://github.com/pingcap/tidb/pull/11989)
+ Output the detailed `backoff` information of TiKV RPC in the slow log to facilitate troubleshooting [#13770](https://github.com/pingcap/tidb/pull/13770)
+ Optimize and unify the format of the memory statistics in the expensive log [#12809](https://github.com/pingcap/tidb/pull/12809)
+ Optimize the explicit format of `EXPLAIN` and support outputting information about the operator’s usage of memory and disk [#13914](https://github.com/pingcap/tidb/pull/13914) [#13692](https://github.com/pingcap/tidb/pull/13692) [#13686](https://github.com/pingcap/tidb/pull/13686) [#11415](https://github.com/pingcap/tidb/pull/11415) [#13927](https://github.com/pingcap/tidb/pull/13927) [#13764](https://github.com/pingcap/tidb/pull/13764) [#13720](https://github.com/pingcap/tidb/pull/13720)
+ Optimize the check for duplicate values in `LOAD DATA` based on the transaction size and support setting the transaction size by configuring the `tidb_dml_batch_size` parameter [#11132](https://github.com/pingcap/tidb/pull/11132)
+ Optimize the performance of `LOAD DATA` by separating the data preparing routine and the commit routine and assigning the workload to different Workers [#11533](https://github.com/pingcap/tidb/pull/11533) [#11284](https://github.com/pingcap/tidb/pull/11284)

## TiKV

+ Upgrade the RocksDB version to 6.4.6
+ Fix the issue that the system cannot perform the compaction task normally when the disk space is used up by automatically creating a 2GB empty file when TiKV is started [#6321](https://github.com/tikv/tikv/pull/6321)
+ Support quick backup and restoration
    - [#6462](https://github.com/tikv/tikv/pull/6462) [#6395](https://github.com/tikv/tikv/pull/6395) [#6378](https://github.com/tikv/tikv/pull/6378) [#6374](https://github.com/tikv/tikv/pull/6374) [#6349](https://github.com/tikv/tikv/pull/6349)
    - [#6339](https://github.com/tikv/tikv/pull/6339) [#6308](https://github.com/tikv/tikv/pull/6308) [#6295](https://github.com/tikv/tikv/pull/6295) [#6286](https://github.com/tikv/tikv/pull/6286) [#6283](https://github.com/tikv/tikv/pull/6283)
    - [#6261](https://github.com/tikv/tikv/pull/6261) [#6222](https://github.com/tikv/tikv/pull/6222) [#6209](https://github.com/tikv/tikv/pull/6209) [#6204](https://github.com/tikv/tikv/pull/6204) [#6202](https://github.com/tikv/tikv/pull/6202)
    - [#6198](https://github.com/tikv/tikv/pull/6198) [#6186](https://github.com/tikv/tikv/pull/6186) [#6177](https://github.com/tikv/tikv/pull/6177) [#6146](https://github.com/tikv/tikv/pull/6146) [#6071](https://github.com/tikv/tikv/pull/6071)
    - [#6042](https://github.com/tikv/tikv/pull/6042) [#5877](https://github.com/tikv/tikv/pull/5877) [#5806](https://github.com/tikv/tikv/pull/5806) [#5803](https://github.com/tikv/tikv/pull/5803) [#5800](https://github.com/tikv/tikv/pull/5800)
    - [#5781](https://github.com/tikv/tikv/pull/5781) [#5772](https://github.com/tikv/tikv/pull/5772) [#5689](https://github.com/tikv/tikv/pull/5689) [#5683](https://github.com/tikv/tikv/pull/5683)
+ Support reading data from Follower replicas
    - [#5051](https://github.com/tikv/tikv/pull/5051) [#5118](https://github.com/tikv/tikv/pull/5118) [#5213](https://github.com/tikv/tikv/pull/5213) [#5316](https://github.com/tikv/tikv/pull/5316) [#5401](https://github.com/tikv/tikv/pull/5401)
    - [#5919](https://github.com/tikv/tikv/pull/5919) [#5887](https://github.com/tikv/tikv/pull/5887) [#6340](https://github.com/tikv/tikv/pull/6340) [#6348](https://github.com/tikv/tikv/pull/6348) [#6396](https://github.com/tikv/tikv/pull/6396)
+ Improve the performance of TiDB reading data through index [#5682](https://github.com/tikv/tikv/pull/5682)
+ Fix the issue that the `CAST` function behaves inconsistently in TiKV and in TiDB
    - [#6459](https://github.com/tikv/tikv/pull/6459) [#6461](https://github.com/tikv/tikv/pull/6461) [#6458](https://github.com/tikv/tikv/pull/6458) [#6447](https://github.com/tikv/tikv/pull/6447) [#6440](https://github.com/tikv/tikv/pull/6440)
    - [#6425](https://github.com/tikv/tikv/pull/6425) [#6424](https://github.com/tikv/tikv/pull/6424) [#6390](https://github.com/tikv/tikv/pull/6390) [#5842](https://github.com/tikv/tikv/pull/5842) [#5528](https://github.com/tikv/tikv/pull/5528)
    - [#5334](https://github.com/tikv/tikv/pull/5334) [#5199](https://github.com/tikv/tikv/pull/5199) [#5167](https://github.com/tikv/tikv/pull/5167) [#5146](https://github.com/tikv/tikv/pull/5146) [#5141](https://github.com/tikv/tikv/pull/5141)
    - [#4998](https://github.com/tikv/tikv/pull/4998) [#5029](https://github.com/tikv/tikv/pull/5029) [#5099](https://github.com/tikv/tikv/pull/5099) [#5006](https://github.com/tikv/tikv/pull/5006) [#5095](https://github.com/tikv/tikv/pull/5095)
    - [#5093](https://github.com/tikv/tikv/pull/5093) [#5090](https://github.com/tikv/tikv/pull/5090) [#4987](https://github.com/tikv/tikv/pull/4987) [#5066](https://github.com/tikv/tikv/pull/5066) [#5038](https://github.com/tikv/tikv/pull/5038)
    - [#4962](https://github.com/tikv/tikv/pull/4962) [#4890](https://github.com/tikv/tikv/pull/4890) [#4727](https://github.com/tikv/tikv/pull/4727) [#6060](https://github.com/tikv/tikv/pull/6060) [#5761](https://github.com/tikv/tikv/pull/5761)
    - [#5793](https://github.com/tikv/tikv/pull/5793) [#5468](https://github.com/tikv/tikv/pull/5468) [#5540](https://github.com/tikv/tikv/pull/5540) [#5548](https://github.com/tikv/tikv/pull/5548) [#5455](https://github.com/tikv/tikv/pull/5455)
    - [#5543](https://github.com/tikv/tikv/pull/5543) [#5433](https://github.com/tikv/tikv/pull/5433) [#5431](https://github.com/tikv/tikv/pull/5431) [#5423](https://github.com/tikv/tikv/pull/5423) [#5179](https://github.com/tikv/tikv/pull/5179)
    - [#5134](https://github.com/tikv/tikv/pull/5134) [#4685](https://github.com/tikv/tikv/pull/4685) [#4650](https://github.com/tikv/tikv/pull/4650) [#6463](https://github.com/tikv/tikv/pull/6463)

## PD

+ Support optimizing hotspot scheduling according to the load information of storage nodes
    - [#1870](https://github.com/pingcap/pd/pull/1870) [#1982](https://github.com/pingcap/pd/pull/1982) [#1998](https://github.com/pingcap/pd/pull/1998) [#1843](https://github.com/pingcap/pd/pull/1843) [#1750](https://github.com/pingcap/pd/pull/1750)
+ Add the Placement Rules feature that supports controlling the number of replicas of any data range, the storage location, the storage host type and roles  by combining different scheduling rules
    - [#2051](https://github.com/pingcap/pd/pull/2051) [#1999](https://github.com/pingcap/pd/pull/1999) [#2042](https://github.com/pingcap/pd/pull/2042) [#1917](https://github.com/pingcap/pd/pull/1917) [#1904](https://github.com/pingcap/pd/pull/1904)
    - [#1897](https://github.com/pingcap/pd/pull/1897) [#1894](https://github.com/pingcap/pd/pull/1894) [#1865](https://github.com/pingcap/pd/pull/1865) [#1855](https://github.com/pingcap/pd/pull/1855) [#1834](https://github.com/pingcap/pd/pull/1834)
+ Support using plugins (experimental) [#1799](https://github.com/pingcap/pd/pull/1799)
+ Add the feature that the schedulers support the customized configuration and key ranges (experimental) [#1735](https://github.com/pingcap/pd/pull/1735) [#1783](https://github.com/pingcap/pd/pull/1783) [#1791](https://github.com/pingcap/pd/pull/1791)
+ Support automatically adjusting the scheduling speed according the cluster load information (experimental, disabled by default) [#1875](https://github.com/pingcap/pd/pull/1875) [#1887](https://github.com/pingcap/pd/pull/1887) [#1902](https://github.com/pingcap/pd/pull/1902)

## Tools

+ TiDB Lightning
    - Add the parameter in the command-line tool to set the password of the downstream database [#253](https://github.com/pingcap/tidb-lightning/pull/253)

## TiDB Ansible

+ Add checksum check in the package in case that the downloaded package is incomplete [#1002](https://github.com/pingcap/tidb-ansible/pull/1002)
+ Support checking the systemd version which must be `systemd-219-52` or later [#1020](https://github.com/pingcap/tidb-ansible/pull/1020) [#1074](https://github.com/pingcap/tidb-ansible/pull/1074)
+ Fix the issue that the log directory is incorrectly created when TiDB Lightning is started [#1103](https://github.com/pingcap/tidb-ansible/pull/1103)
+ Fix the issue that the customized port of TiDB Lightning is invalid [#1107](https://github.com/pingcap/tidb-ansible/pull/1107)
+ Support deploying and maintaining TiFlash [#1119](https://github.com/pingcap/tidb-ansible/pull/1119)
