---
title: TiDB 3.1 RC Release Notes
aliases: ['/docs/dev/releases/release-3.1.0-rc/','/docs/dev/releases/3.1.0-rc/']
---

# TiDB 3.1 RC Release Notes

Release date: April 2, 2020

TiDB version: 3.1.0-rc

TiDB Ansible version: 3.1.0-rc

> **Warning:**
>
> Some known issues are found in this version, and these issues are fixed in new versions. It is recommended that you use the latest 3.1.x version.

## New Features

+ TiDB

    - Use the binary search to re-implement partition pruning for better performance [#15678](https://github.com/pingcap/tidb/pull/15678)
    - Support using the `RECOVER` syntax to recover the truncated table [#15460](https://github.com/pingcap/tidb/pull/15460)
    - Add the `AUTO_RANDOM` ID cache for retrying statements and recovering tables [#15393](https://github.com/pingcap/tidb/pull/15393)
    - Support restoring the state of the `AUTO_RANDOM` ID allocator using the `recover table` statement [#15393](https://github.com/pingcap/tidb/pull/15393)
    - Support `YEAR`, `MONTH`, and `TO_DAY` functions as the partitioning keys of the Hash partitioned table [#15619](https://github.com/pingcap/tidb/pull/15619)
    - Add the table ID to the schema-change related tables only when keys need to be locked in the `SELECT... FOR UPDATE` statement [#15708](https://github.com/pingcap/tidb/pull/15708)
    - Add the feature of automatically reading data from different roles according to the load balancing policy and add the `leader-and-follower` system variable to enable this feature [#15721](https://github.com/pingcap/tidb/pull/15721)
    - Support dynamically updating the TLS certificate every time TiDB establishes a new connection to update expired client certificate without restarting the RPC client side [#15163](https://github.com/pingcap/tidb/pull/15163)
    - Upgrade PD Client to support loading the latest certificate every time TiDB establishes a new connection [#15425](https://github.com/pingcap/tidb/pull/15425)
    - Forcibly use the HTTPS protocol with the configured TLS certificates between a TiDB server and a PD server, or between two TiDB servers when `cluster-ssl-*` is configured [#15430](https://github.com/pingcap/tidb/pull/15430)
    - Add the MySQL-compatible `--require-secure-transport` startup option to force the client to enable TLS authentication during the configuration [#15442](https://github.com/pingcap/tidb/pull/15442)
    - Add the `cluster-verify-cn` configuration item. After configuration, the status service can only be used when with the corresponding CN certificate [#15137](https://github.com/pingcap/tidb/pull/15137)

+ TiKV

    - Support backing up data with the Raw KV API [#7051](https://github.com/tikv/tikv/pull/7051)
    - Support TLS authentication for the status server [#7142](https://github.com/tikv/tikv/pull/7142)
    - Support TLS authentication for the KV server [#7305](https://github.com/tikv/tikv/pull/7305)
    - Optimize the time to hold locks to improve the performance of backup [#7202](https://github.com/tikv/tikv/pull/7202)

+ PD

    - Support scheduling learner using `shuffle-region-scheduler` [#2235](https://github.com/pingcap/pd/pull/2235)
    - Add commands in pd-ctl to configure Placement Rules [#2306](https://github.com/pingcap/pd/pull/2306)

+ Tools

    - TiDB Binlog

        * Support TLS authentication between the components [#931](https://github.com/pingcap/tidb-binlog/pull/931) [#937](https://github.com/pingcap/tidb-binlog/pull/937) [#939](https://github.com/pingcap/tidb-binlog/pull/939)
        * Add the `kafka-client-id` configuration item in Drainer to configure Kafka's client ID [#929](https://github.com/pingcap/tidb-binlog/pull/929)

    - TiDB Lightning

        * Optimize the performance of TiDB Lightning [#281](https://github.com/pingcap/tidb-lightning/pull/281) [#275](https://github.com/pingcap/tidb-lightning/pull/275)
        * Support TLS authentication for TiDB Lightning [#270](https://github.com/pingcap/tidb-lightning/pull/270)

    - Backup & Restore (BR)

        * Optimize the log output [#189](https://github.com/pingcap/br/pull/189)

+ TiDB Ansible

    - Optimize the way the TiFlash data directories are created [#1242](https://github.com/pingcap/tidb-ansible/pull/1242)
    - Add the `Write Amplification` monitoring item in TiFlash [#1234](https://github.com/pingcap/tidb-ansible/pull/1234)
    - Optimize the error message of failed preflight checks when CPU epollexclusive is unavailable [#1243](https://github.com/pingcap/tidb-ansible/pull/1243)

## Bug Fixes

+ TiDB

    - Fix the information schema error caused by frequently updating the TiFlash replica [#14884](https://github.com/pingcap/tidb/pull/14884)
    - Fix the issue that `last_insert_id` is incorrectly generated when applying `AUTO_RANDOM` [#15149](https://github.com/pingcap/tidb/pull/15149)
    - Fix the issue that updating the status of TiFlash replica might cause the DDL operation to get stuck [#15161](https://github.com/pingcap/tidb/pull/15161)
    - Forbid `Aggregation` pushdown and `TopN` pushdown when there are predicates that can not be pushed down [#15141](https://github.com/pingcap/tidb/pull/15141)
    - Forbid the nested `view` creation [#15440](https://github.com/pingcap/tidb/pull/15440)
    - Fix the error occurred when executing `SELECT CURRENT_ROLE()` after `SET ROLE ALL` [#15570](https://github.com/pingcap/tidb/pull/15570)
    - Fix the failure to identify the `view` name when executing the `select view_name.col_name from view_name` statement [#15573](https://github.com/pingcap/tidb/pull/15573)
    - Fix the issue that an error might occur when pre-processing DDL statements during the write of binlog information [#15444](https://github.com/pingcap/tidb/pull/15444)
    - Fix the panic occurred when accessing both `view`s and partitioned tables [#15560](https://github.com/pingcap/tidb/pull/15560)
    - Fix the error occurred when executing the `VALUES` function with the `update duplicate key` statement that contains the `bit(n)` data type [#15487](https://github.com/pingcap/tidb/pull/15487)
    - Fix the issue that the specified maximum execution time fails to take effect in some scenarios [#15616](https://github.com/pingcap/tidb/pull/15616)
    - Fix the issue that whether the current `ReadEngine` contains TiKV server is not checked when generating the execution plan using `Index Scan` [#15773](https://github.com/pingcap/tidb/pull/15773)

+ TiKV

    - Fix the issue of conflict check failure or data index inconsistency caused by inserting an existing key into a transaction and then deleting it immediately when disabling the consistency check parameter [#7112](https://github.com/tikv/tikv/pull/7112)
    - Fix the calculation error when `TopN` compares unsigned integers [#7199](https://github.com/tikv/tikv/pull/7199)
    - Introduce a flow control mechanism in Raftstore to solve the problem that without flow control, it might cause slow log tracking and cause the cluster to be stuck; and the problem that the large transaction size might cause the frequent reconnection among TiKV servers [#7087](https://github.com/tikv/tikv/pull/7087) [#7078](https://github.com/tikv/tikv/pull/7078)
    - Fix the issue that pending read requests sent to replicas might be permanently blocked [#6543](https://github.com/tikv/tikv/pull/6543)
    - Fix the issue that replica read might be blocked by applying snapshots [#7249](https://github.com/tikv/tikv/pull/7249)
    - Fix the issue that transferring leader might cause TiKV to panic [#7240](https://github.com/tikv/tikv/pull/7240)
    - Fix the issue that all SST files are filled with zeroes when backing up data to S3 [#6967](https://github.com/tikv/tikv/pull/6967)
    - Fix the issue that the size of SST file is not recorded during backup, resulting in many empty Regions after restoration [#6983](https://github.com/tikv/tikv/pull/6983)
    - Support AWS IAM web identity for backup [#7297](https://github.com/tikv/tikv/pull/7297)

+ PD

    - Fix the issue of incorrect Region information caused by data race when PD processes Region heartbeats [#2234](https://github.com/pingcap/pd/pull/2234)
    - Fix the issue that `random-merge-scheduler` fails to follow location labels and Placement Rules [#2212](https://github.com/pingcap/pd/pull/2221)
    - Fix the issue that a placement rule is overwritten by another placement rule with the same `startKey` and `endKey` [#2222](https://github.com/pingcap/pd/pull/2222)
    - Fix the issue that the version number of API is inconsistent with that of PD server [#2192](https://github.com/pingcap/pd/pull/2192)

+ Tools

    - TiDB Lightning

        * Fix the bug that the `&` character is replaced by the `EOF` character in TiDB backend [#283](https://github.com/pingcap/tidb-lightning/pull/283)

    - Backup & Restore (BR)

        * Fix the issue that BR cannot restore the TiFlash cluster data [#194](https://github.com/pingcap/br/pull/194)
