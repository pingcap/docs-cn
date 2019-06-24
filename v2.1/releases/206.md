---
title: TiDB 2.0.6 Release Notes
category: Releases
---

# TiDB 2.0.6 Release Notes

On August 6, 2018, TiDB 2.0.6 is released. Compared with TiDB 2.0.5, this release has great improvement in system compatibility and stability.

## TiDB

- Improvements
    - Make "set system variable" log shorter to save disk space [#7031](https://github.com/pingcap/tidb/pull/7031)
    - Record slow operations during the execution of `ADD INDEX` in the log, to make troubleshooting easier [#7083](https://github.com/pingcap/tidb/pull/7083)
    - Reduce transaction conflicts when updating statistics [#7138](https://github.com/pingcap/tidb/pull/7138)
    - Improve the accuracy of row count estimation when the values pending to be estimated exceeds the statistics range [#7185](https://github.com/pingcap/tidb/pull/7185)
    - Choose the table with a smaller estimated row count as the outer table for `Index Join` to improve its execution efficiency [#7277](https://github.com/pingcap/tidb/pull/7277)
    - Add the recover mechanism for panics occurred during the execution of `ANALYZE TABLE`, to avoid that the tidb-server is unavailable caused by abnormal behavior in the process of collecting statistics [#7228](https://github.com/pingcap/tidb/pull/7228)
    - Return `NULL` and the corresponding warning when the results of `RPAD`/`LPAD` exceed the value of the `max_allowed_packet` system variable, compatible with MySQL [#7244](https://github.com/pingcap/tidb/pull/7244)
    - Set the upper limit of placeholders count in the `PREPARE` statement to 65535, compatible with MySQL [#7250](https://github.com/pingcap/tidb/pull/7250)
- Bug Fixes
    - Fix the issue that the `DROP USER` statement is incompatible with MySQL behavior in some cases [#7014](https://github.com/pingcap/tidb/pull/7014)
    - Fix the issue that statements like `INSERT`/`LOAD DATA` meet OOM aftering opening `tidb_batch_insert` [#7092](https://github.com/pingcap/tidb/pull/7092)
    - Fix the issue that the statistics fail to automatically update when the data of a table keeps updating [#7093](https://github.com/pingcap/tidb/pull/7093)
    - Fix the issue that the firewall breaks inactive gPRC connections [#7099](https://github.com/pingcap/tidb/pull/7099)
    - Fix the issue that prefix index returns a wrong result in some scenarios [#7126](https://github.com/pingcap/tidb/pull/7126)
    - Fix the panic issue caused by outdated statistics in some scenarios [#7155](https://github.com/pingcap/tidb/pull/7155)
    - Fix the issue that one piece of index data is missed after the `ADD INDEX` operation in some scenarios [#7156](https://github.com/pingcap/tidb/pull/7156)
    - Fix the wrong result issue when querying `NULL` values using the unique index in some scenarios [#7172](https://github.com/pingcap/tidb/pull/7172)
    - Fix the messy code issue of the `DECIMAL` multiplication result in some scenarios [#7212](https://github.com/pingcap/tidb/pull/7212)
    - Fix the wrong result issue of `DECIMAL` modulo operation in some scenarios [#7245](https://github.com/pingcap/tidb/pull/7245)
    - Fix the issue that the `UPDATE`/`DELETE` statement in a transaction returns a wrong result under some special sequence of statements [#7219](https://github.com/pingcap/tidb/pull/7219)
    - Fix the panic issue of the `UNION ALL`/`UPDATE` statement during the process of building the execution plan in some scenarios [#7225](https://github.com/pingcap/tidb/pull/7225)
    - Fix the issue that the range of prefix index is calculated incorrectly in some scenarios [#7231](https://github.com/pingcap/tidb/pull/7231)
    - Fix the issue that the `LOAD DATA` statement fails to write the binlog in some scenarios [#7242](https://github.com/pingcap/tidb/pull/7242)
    - Fix the wrong result issue of `SHOW CREATE TABLE` during the execution process of `ADD INDEX` in some scenarios [#7243](https://github.com/pingcap/tidb/pull/7243)
    - Fix the issue that panic occurs when `Index Join` does not initialize timestamps in some scenarios [#7246](https://github.com/pingcap/tidb/pull/7246)
    - Fix the false alarm issue when `ADMIN CHECK TABLE` mistakenly uses the timezone in the session [#7258](https://github.com/pingcap/tidb/pull/7258)
    - Fix the issue that `ADMIN CLEANUP INDEX` does not clean up the index in some scenarios [#7265](https://github.com/pingcap/tidb/pull/7265)
    - Disable the Read Committed isolation level [#7282](https://github.com/pingcap/tidb/pull/7282)

## TiKV

- Improvements
    - Enlarge scheduler's default slots to reduce false conflicts
    - Reduce continuous records of rollback transactions, to improve the Read performance when conflicts are extremely severe
    - Limit the size and number of RocksDB log files, to reduce unnecessary disk usage in long-running condition
- Bug Fixes
    - Fix the crash issue when converting the data type from string to decimal
