---
title: Troubleshoot Inconsistency Between Data and Indexes
summary: Learn how to deal with errors reported by the consistency check between data and indexes.
---

# Troubleshoot Inconsistency Between Data and Indexes

TiDB checks consistency between data and indexes when it executes transactions or the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement. If the check finds that a record key-value and the corresponding index key-value are inconsistent, that is, a key-value pair storing row data and the corresponding key-value pair storing its index are inconsistent (for example, more indexes or missing indexes), TiDB reports a data inconsistency error and prints the related errors in error logs.

<CustomContent platform="tidb">

This document describes the meanings of data inconsistency errors and provides some methods to bypass the consistency check. If a data consistency error occurs, you can [get support](/support.md) from PingCAP or the community.

</CustomContent>

<CustomContent platform="tidb-cloud">

This document describes the meanings of data inconsistency errors and provides some methods to bypass the consistency check. If a data consistency error occurs, you can [contact TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md).

</CustomContent>

## Error explanation

When inconsistency between data and indexes occurs, you can check TiDB error messages to know which item is inconsistent between row data and index data, or check the related error logs for further investigation.

### Errors reported during transaction execution

This section lists the data inconsistency errors reported when TiDB executes transactions and explains the meanings of these errors with examples.

#### Error 8133

`ERROR 8133 (HY000): data inconsistency in table: t, index: k2, index-count:1 != record-count:0`

This error indicates that for the `k2` index in table `t`, the number of indexes in the table is 1 and the number of row records is 0. The number is inconsistent.

#### Error 8138

`ERROR 8138 (HY000): writing inconsistent data in table: t, expected-values:{KindString green} != record-values:{KindString GREEN}`

This error indicates that the transaction was attempting to write an incorrect row value. For the data to be written, the encoded row data does not match the original data before encoding.

#### Error 8139

`ERROR 8139 (HY000): writing inconsistent data in table: t, index: i1, index-handle:4 != record-handle:3, index: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x69, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x1, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x1, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x0, 0x0, 0x0, 0xfc, 0x3, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x4}, flags:0x0, value:[]uint8{0x30}, indexID:1}, record: tables.mutation{key:kv.Key{0x74, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x49, 0x5f, 0x72, 0x80, 0x0, 0x0, 0x0, 0x0, 0x0, 0x0, 0x3}, flags:0xd, value:[]uint8{0x80, 0x0, 0x2, 0x0, 0x0, 0x0, 0x1, 0x2, 0x5, 0x0, 0xa, 0x0, 0x68, 0x65, 0x6c, 0x6c, 0x6f, 0x68, 0x65, 0x6c, 0x6c, 0x6f}, indexID:0}`

This error indicates that the handle (that is, the key of the row data) of the data to be written is inconsistent. For index `i1` in table `t`, the row to be written by the transaction has a handle of 4 in the index key-value pair and a handle of 3 in the row record key-value pair. The data of this row will not be written.

#### Error 8140

`ERROR 8140 (HY000): writing inconsistent data in table: t, index: i2, col: c1, indexed-value:{KindString hellp} != record-value:{KindString hello}`

This error indicates that the data in a row to be written by the transaction does not match the data in the index. For index `i2` in table `t`, a row to be written by the transaction has data `hellp` in the index key-value pair and data `hello` in the record key-value pair. The data of this row will not be written.

#### Error 8141

`ERROR 8141 (HY000): assertion failed: key: 7480000000000000405f72013300000000000000f8, assertion: NotExist, start_ts: 430590532931813377, existing start ts: 430590532931551233, existing commit ts: 430590532931551234`

This error indicates that the assertion failed when a transaction was being committed. Assuming that data and indexes are consistent, TiDB asserted that the key `7480000000000000405f720133000000000000000000f8` did not exist. When the transaction was being committed, TiDB found the key did exist, written by the transaction with the `start ts` `430590532931551233`. TiDB will print the Multi-Version Concurrency Control (MVCC) history of this key to logs.

### Errors reported in admin check

This section lists the data inconsistency errors that might occur in TiDB when you execute the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement, and explains the meanings of these errors with examples.

#### Error 8003

`ERROR 8003 (HY000): table count 3 != index(idx) count 2`

This error indicates that the table on which the [`ADMIN CHECK`](/sql-statements/sql-statement-admin-check-table-index.md) statement is executed has 3 row key-value pairs but only 2 index key-value pairs.

#### Error 8134

`ERROR 8134 (HY000): data inconsistency in table: t, index: c2, col: c2, handle: "2", index-values:"KindInt64 13" != record-values:"KindInt64 12", compare err:<nil>`

This error indicates that for index `c2` in table `t`, the value of column `c2` has the following inconsistency:

- In the index key-value pair of the row whose handle is `2`, the value of column `c2` is `13`.
- In the row record key-value pair, the value of column `c2` is `12`.

#### Error 8223

`ERROR 8223 (HY000): data inconsistency in table: t2, index: i1, handle: {hello, hello}, index-values:"" != record-values:"handle: {hello, hello}, values: [KindString hello KindString hello]"`

This error indicates that `index-values` are null and `record-values` are not null, meaning that there is no corresponding index for the row.

## Solutions

<CustomContent platform="tidb">

If you encounter a data inconsistency error, [get support](/support.md) from PingCAP for troubleshooting immediately instead of dealing with the error by yourself. If your application needs to skip such errors urgently, you can use the following methods to bypass the check.

</CustomContent>

<CustomContent platform="tidb-cloud">

If you encounter a data inconsistency error, [contact TiDB Cloud Support](/tidb-cloud/tidb-cloud-support.md) for troubleshooting immediately instead of dealing with the error by yourself. If your application needs to skip such errors urgently, you can use the following methods to bypass the check.

</CustomContent>

### Rewrite SQL

If the data inconsistency error occurs in a particular SQL statement only, you can bypass this error by rewriting the SQL statement to another equivalent form using different execution operators.

### Disable error checks

For the following errors reported in transaction execution, you can bypass the corresponding checks:

- To bypass the checks of errors 8138, 8139, and 8140, configure `set @@tidb_enable_mutation_checker=0`.
- To bypass the checks of error 8141, configure `set @@tidb_txn_assertion_level=OFF`.

> **Note:**
>
> Disabling `tidb_enable_mutation_checker` and `tidb_txn_assertion_level` will bypass the corresponding checks of all SQL statements.

For other errors reported in transaction execution and all errors reported during the execution of the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement, you cannot bypass the corresponding check, because the data is already inconsistent.