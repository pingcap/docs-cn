---
title: TiDB 3.0.8 Release Notes
aliases: ['/docs/dev/releases/release-3.0.8/','/docs/dev/releases/3.0.8/']
---

# TiDB 3.0.8 Release Notes

Release date: December 31, 2019

TiDB version: 3.0.8

TiDB Ansible version: 3.0.8

## TiDB

+ SQL Optimizer
    - Fix the wrong SQL binding plan caused by untimely cache updates [#13891](https://github.com/pingcap/tidb/pull/13891)
    - Fix the issue that the SQL binding might be invalid when an SQL statement contains a symbol list [#14004](https://github.com/pingcap/tidb/pull/14004)
    - Fix the issue that an SQL binding cannot be created or deleted because an SQL statement ends with `;` [#14113](https://github.com/pingcap/tidb/pull/14113)
    - Fix the issue that a wrong SQL query plan might be selected because the `PhysicalUnionScan` operator sets wrong statistics [#14133](https://github.com/pingcap/tidb/pull/14133)
    - Remove the `minAutoAnalyzeRatio` restriction to make `autoAnalyze` more timely [#14015](https://github.com/pingcap/tidb/pull/14015)
+ SQL Execution Engine
    - Fix issues that the `INSERT/REPLACE/UPDATE ... SET ... = DEFAULT` syntax might report an error and combining the usage of the `DEFAULT` expression with a virtual generated column might report an error [#13682](https://github.com/pingcap/tidb/pull/13682)
    - Fix the issue that the `INSERT` statement might report an error when converting a string to a float [#14011](https://github.com/pingcap/tidb/pull/14011)
    - Fix the issue that sometimes the aggregate operation is low effective because the concurrency value of the `HashAgg` executor is incorrectly initialized [#13811](https://github.com/pingcap/tidb/pull/13811)
    - Fix the issue that an error is reported in the execution of`group by item` when the clause is in the parentheses [#13658](https://github.com/pingcap/tidb/pull/13658)
    - Fix the issue that the execution of `OUTER JOIN` might report an error because TiDB incorrectly calculates `group by item` [#14014](https://github.com/pingcap/tidb/pull/14014)
    - Fix the issue that the error message is inaccurate when Range-exceeding data is written into Range partitioned tables [#14107](https://github.com/pingcap/tidb/pull/14107)
    - Revert [PR #10124](https://github.com/pingcap/tidb/pull/10124) and cancel the `PadCharToFullLength` effect to avoid unexpected query results in special cases, considering that MySQL 8 will discard `PadCharToFullLength` soon [#14157](https://github.com/pingcap/tidb/pull/14157)
    - Fix the goroutine leak issue when executing the `EXPLAIN ANALYZE` statement caused by unguaranteed `close()` calling in `ExplainExec` [#14226](https://github.com/pingcap/tidb/pull/14226)
+ DDL
    - Optimize the error message output of `change column`/`modify column` to make it easier to understand [#13796](https://github.com/pingcap/tidb/pull/13796)
    - Add the `SPLIT PARTITION TABLE` syntax to support splitting Regions for partitioned tables [#13929](https://github.com/pingcap/tidb/pull/13929)
    - Fix the issue that the index length exceeds 3072 bytes and no error is reported because the index length is incorrectly checked when an index is created [#13779](https://github.com/pingcap/tidb/pull/13779)
    - Fix the issue that the `GC life time is shorter than transaction duration` error message might be reported because it takes too much time to add an index in partitioned tables [#14132](https://github.com/pingcap/tidb/pull/14132)
    - Fix the panic when `SELECT * FROM information_schema.KEY_COLUMN_USAGE` is executed because the foreign key is not checked when `DROP COLUMN`/`MODIFY COLUMN`/`CHANGE COLUMN` is executed [#14105](https://github.com/pingcap/tidb/pull/14105)
+ Server
    - Statement Summary improvements:
        - Add a large number of SQL metric fields to facilitate analyzing SQL statements in more detail [#14151](https://github.com/pingcap/tidb/pull/14151), [#14168](https://github.com/pingcap/tidb/pull/14168)
        - Add the `stmt-summary.refresh-interval` parameter to control whether to move the stale data from the `events_statements_summary_by_digest` table to the `events_statements_summary_by_digest_history` table (the default interval: 30 minutes) [#14161](https://github.com/pingcap/tidb/pull/14161)
        - Add the `events_statements_summary_by_digest_history` table to save the stale data in `events_statements_summary_by_digest` [#14166](https://github.com/pingcap/tidb/pull/14166)
    - Fix the issue that the binlog is incorrectly output when RBAC-related internal SQL statements are executed [#13890](https://github.com/pingcap/tidb/pull/13890)
    - Add the `server-version` configuration item to control the feature of modifying the TiDB server version [#13906](https://github.com/pingcap/tidb/pull/13906)
    - Add the feature of using the HTTP interface to recover writing the TiDB binlog [#13892](https://github.com/pingcap/tidb/pull/13892)
    - Update the privilege required by `GRANT roles TO user` from `GrantPriv` to `ROLE_ADMIN` or `SUPER`, to keep consistency with the MySQL behavior [#13932](https://github.com/pingcap/tidb/pull/13932)
    - Modify the TiDB behavior from using the current database to reporting the `No database selected` error when the `GRANT` statement does not specify a database name, to keep compatibility with the MySQL behavior [#13784](https://github.com/pingcap/tidb/pull/13784)
    - Modify the execution privilege for the `REVOKE` statement from `SuperPriv` to `REVOKE` being executable only if the user has the privilege for the corresponding schema, to keep consistency with the MySQL behavior [#13306](https://github.com/pingcap/tidb/pull/13306)
    - Fix the issue that `GrantPriv` is mistakenly granted to the target user when the `GRANT ALL` syntax does not contain `WITH GRANT OPTION` [#13943](https://github.com/pingcap/tidb/pull/13943)
    - Fix the issue that the error message does not contain the cause for the `LOAD DATA` statement’s wrong behavior when `LoadDataInfo` fails to call `addRecord` [#13980](https://github.com/pingcap/tidb/pull/13980)
    - Fix the issue that wrong slow query information is output because multiple SQL statements in a query share the same `StartTime` [#13898](https://github.com/pingcap/tidb/pull/13898)
    - Fix the issue that the memory might leak when `batchClient` processes a large transaction [#14032](https://github.com/pingcap/tidb/pull/14032)
    - Fix the issue that `system_time_zone` is always displayed as `CST` and now TiDB’s `system_time_zone` is obtained from `systemTZ` in the `mysql.tidb` table [#14086](https://github.com/pingcap/tidb/pull/14086)
    - Fix the issue that the `GRANT ALL` syntax does not grant all privileges to the user [#14092](https://github.com/pingcap/tidb/pull/14092)
    - Fix the issue that the `Priv_create_user` privilege is invalid for `CREATE ROLE` and `DROP ROLE` [#14088](https://github.com/pingcap/tidb/pull/14088)
    - Modify the error code of `ErrInvalidFieldSize` from `1105(Unknow Error)` to `3013` [#13737](https://github.com/pingcap/tidb/pull/13737)
    - Add the `SHUTDOWN` command to stop a TiDB server and add the `ShutdownPriv` privilege [#14104](https://github.com/pingcap/tidb/pull/14104)
    - Fix the atomicity issue for the `DROP ROLE` statement to avoid some roles being deleted unexpectedly when TiDB fails to execute a statement [#14130](https://github.com/pingcap/tidb/pull/14130)
    - Fix the issue that the `tidb_enable_window_function` in the `SHOW VARIABLE` result incorrectly outputs `1` when a TiDB version is upgraded to 3.0, and replace the wrong result with `0` [#14131](https://github.com/pingcap/tidb/pull/14131)
    - Fix the issue that the goroutine might leak because `gcworker` continuously retries when the TiKV node is offline [#14106](https://github.com/pingcap/tidb/pull/14106)
    - Record the binlog `Prewrite` time in the slow query log to improve the usability for issue tracking [#14138](https://github.com/pingcap/tidb/pull/14138)
    - Make the `tidb_enable_table_partition` variable support `GLOBAL SCOPE` [#14091](https://github.com/pingcap/tidb/pull/14091)
    - Fix the issue that the user privilege might be missing or mistakenly added because the newly added privilege is not correctly granted to the corresponding user when a new privilege is added [#14178](https://github.com/pingcap/tidb/pull/14178)
    - Fix the issue that the `CheckStreamTimeoutLoop` goroutine might leak because `rpcClient` does not close when the TiKV server is disconnected [#14227](https://github.com/pingcap/tidb/pull/14227)
    - Support certificate-based authentication ([User document](/certificate-authentication.md)) [#13955](https://github.com/pingcap/tidb/pull/13955)
+ Transaction
    - Update the default value of the `tidb_txn_mode` variable from `""` to `"pessimistic"` when a new cluster is created [#14171](https://github.com/pingcap/tidb/pull/14171)
    - Fix the issue that the lock waiting time is too long for a pessimistic transaction because the lock waiting time for a single statement is not reset when a transaction is retried [#13990](https://github.com/pingcap/tidb/pull/13990)
    - Fix the issue that wrong data might be read because unmodified data is unlocked for the pessimistic transaction model [#14050](https://github.com/pingcap/tidb/pull/14050)
    - Fix repeated insert value restriction checks because transaction types are not distinguished when prewrite is performed in mocktikv [#14175](https://github.com/pingcap/tidb/pull/14175)
    - Fix the panic because transactions are not correctly handled when `session.TxnState` is `Invalid` [#13988](https://github.com/pingcap/tidb/pull/13988)
    - Fix the issue that the `ErrConfclit` structure in mocktikv does not contain `ConflictCommitTS` [#14080](https://github.com/pingcap/tidb/pull/14080)
    - Fix the issue that the transaction is blocked because TiDB does not correctly check lock timeout after resolving the lock [#14083](https://github.com/pingcap/tidb/pull/14083)
+ Monitor
    - Add the `pessimistic_lock_keys_duration` monitoring item in `LockKeys` [#14194](https://github.com/pingcap/tidb/pull/14194)

## TiKV

+ Coprocessor
    - Modify the level of the output log from `error` to `warn` when an error occurs in Coprocessor [#6051](https://github.com/tikv/tikv/pull/6051)
    - Modify the update behavior of statistics sampling data from directly updating the row to deleting before inserting, to keep consistency with the update behavior of tidb-server [#6069](https://github.com/tikv/tikv/pull/6096)
+ Raftstore
    - Fix the panic caused by repeatedly sending the `destroy` message to `peerfsm` and `peerfsm` being destroyed multiple times [#6297](https://github.com/tikv/tikv/pull/6297)
    - Update the default value of `split-region-on-table` from `true` to `false` to disable splitting Regions by table by default [#6253](https://github.com/tikv/tikv/pull/6253)
+ Engine
    - Fix the issue that empty data might be returned because RocksDB iterator errors are not correctly processed in extreme conditions [#6326](https://github.com/tikv/tikv/pull/6326)
+ Transaction
    - Fix the issue that TiKV fails to write data into keys and GC is blocked because the pessimistic locks are incorrectly cleaned up [#6354](https://github.com/tikv/tikv/pull/6354)
    - Optimize the pessimistic lock waiting mechanism to improve the performance in scenarios where the lock conflict is severe [#6296](https://github.com/tikv/tikv/pull/6296)
+ Update the default value of `tikv_alloc` from `tikv_alloc/default` to `jemalloc` [#6206](https://github.com/tikv/tikv/pull/6206)

## PD

- Client
    - Support using `context` to create a client and setting the timeout duration when creating a new client [#1994](https://github.com/pingcap/pd/pull/1994)
    - Support creating the `KeepAlive` connection [#2035](https://github.com/pingcap/pd/pull/2035)
- Optimize the performance for the `/api/v1/regions` API [#1986](https://github.com/pingcap/pd/pull/1986)
- Fix the issue that deleting stores in a `tombstone` state might cause a panic [#2038](https://github.com/pingcap/pd/pull/2038)
- Fix the issue that overlapped Regions are mistakenly deleted when loading the Region information from disks [#2011](https://github.com/pingcap/pd/issues/2011), [#2040](https://github.com/pingcap/pd/pull/2040)
- Upgrade etcd from v3.4.0 to v3.4.3 (note that after upgrading you can only degrade etcd using pd-recover) [#2058](https://github.com/pingcap/pd/pull/2058)

## Tools

+ TiDB Binlog
    - Fix the issue that the binlog is ignored because Pump does not receive the DDL committed binlog [#853](https://github.com/pingcap/tidb-binlog/pull/853)

## TiDB Ansible

- Revert the simplified configuration item [#1053](https://github.com/pingcap/tidb-ansible/pull/1053)
- Optimize the logic for checking the TiDB version when performing a rolling update [#1056](https://github.com/pingcap/tidb-ansible/pull/1056)
- Upgrade TiSpark to v2.1.8 [#1061](https://github.com/pingcap/tidb-ansible/pull/1061)
- Fix the issue that the PD role monitoring item is wrongly displayed on Grafana [#1065](https://github.com/pingcap/tidb-ansible/pull/1065)
- Optimize `Thread Voluntary Context Switches` and `Thread Nonvoluntary Context Switches` monitoring items on the TiKV Detail page on Grafana [#1071](https://github.com/pingcap/tidb-ansible/pull/1071)
