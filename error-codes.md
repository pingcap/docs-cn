---
title: Error Codes and Troubleshooting
summary: Learn about the error codes and solutions in TiDB.
aliases: ['/docs/dev/error-codes/','/docs/dev/reference/error-codes/']
---

# Error Codes and Troubleshooting

This document describes the problems encountered during the use of TiDB and provides the solutions.

## Error codes

TiDB is compatible with the error codes in MySQL, and in most cases returns the same error code as MySQL. For a list of error codes for MySQL, see [MySQL 5.7 Error Message Reference](https://dev.mysql.com/doc/mysql-errors/5.7/en/). In addition, TiDB has the following unique error codes:

> **Note:**
>
> Some error codes stand for internal errors. Normally, TiDB handles the error rather than return it to the user, so some error codes are not listed here.
>
> If you encounter an error code that is not listed here, [get support](/support.md) from PingCAP or the community.

* Error Number: 8001

    The memory used by the request exceeds the threshold limit for the TiDB memory usage.

    Increase the memory limit for a single SQL statement by configuring the system variable [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query).

* Error Number: 8002

    To guarantee consistency, a transaction with the `SELECT FOR UPDATE` statement cannot be retried when it encounters a commit conflict. TiDB rolls back the transaction and returns this error.

    The application can safely retry the whole transaction.

* Error Number: 8003

    If the data in a row is not consistent with the index when executing the [`ADMIN CHECK TABLE`](/sql-statements/sql-statement-admin-check-table-index.md) command, TiDB returns this error. This error is commonly seen when you check the data corruption in the table.

    You can [get support](/support.md) from PingCAP or the community.

* Error Number: 8004

    A single transaction is too large.

    See [the error message `transaction too large`](/faq/migration-tidb-faq.md#the-error-message-transaction-too-large-is-displayed) for the cause and solution.

* Error Number: 8005

    The complete error message: `ERROR 8005 (HY000): Write Conflict, txnStartTS is stale`

    Transactions in TiDB encounter write conflicts. Check your application logic and retry the write operation.

* Error Number: 8018

    When you reload a plugin, if the plugin has not been loaded before, this error is returned.

    You can execute an initial load of the plugin.

* Error Number: 8019

    The version of the plugin that is being reloaded is different from the previous version. Therefore, the plugin cannot be reloaded, and this error is returned.

    You can reload the plugin by ensuring that the plugin version is the same as the previous one.

* Error Number: 8020

    When the table is locked, if you perform a write operation on the table, this error is returned.

    Unlock the table and retry the write operation.

* Error Number: 8021

    When the key to be read from TiKV does not exist, this error is returned. This error is used internally, and the external result is an empty read.

* Error Number: 8022

    The transaction commit fails and has been rolled back.

    The application can safely retry the whole transaction.

* Error Number: 8023

    If you set an empty value when writing the transaction cache, this error is returned. This error is used and dealt with internally, and is not returned to the application.

* Error Number: 8024

    Invalid transactions. If TiDB finds that no transaction ID (Start Timestamp) is obtained for the transaction that is being executed, which means this transaction is invalid, this error is returned.

    Usually this error does not occur. If you encounter this error, [get support](/support.md) from PingCAP or the community.

* Error Number: 8025

    The single Key-Value pair being written is too large. The largest single Key-Value pair supported in TiDB is 6 MB by default.

    If a pair exceeds this limit, you need to properly adjust the [`txn-entry-size-limit`](/tidb-configuration-file.md#txn-entry-size-limit-new-in-v50) configuration value to relax the limit.

* Error Number: 8026

    The interface function being used has not been implemented. This error is only used internally, and is not returned to the application.

* Error Number: 8027

    The table schema version is outdated. TiDB applies schema changes online. When the table schema version of the TiDB server is earlier than that of the entire system, this error is returned if you execute a SQL statement.

    When this error occurs, check the network between the TiDB server and the PD Leader.

* Error Number: 8028

    Since v6.3.0, TiDB introduces the [Metadata lock](/metadata-lock.md) feature. When the metadata lock is disabled and a transaction is executed, the transaction cannot recognize the table schema changes. Therefore, when the transaction is committed, TiDB checks the table schema related to the transaction. If the related table schema has been changed during the execution, the transaction commit fails with this error. At this time, the application can safely retry the whole transaction.

    When the metadata lock is enabled not in the Read Committed isolation level, if a lossy column type change occurs on a table (for example, changing from `INT` to `CHAR` is lossy, and changing from `TINYINT` to `INT` is not lossy because overwriting data is not required) from a transaction start to access the table for the first time, then the query fails while the transaction will not roll back automatically. You can continue to execute other statements and decide whether to roll back or commit the transaction.

* Error Number: 8029

    This error occurs when numeric conversion within the database encounters an error. This error is only used internally and is converted to a specific type of error for external applications.

* Error Number: 8030

    After an unsigned positive integer is converted to a signed integer, it exceeds the maximum value and displays as a negative integer. This error mostly occurs in the alert message.

* Error Number: 8031

    When being converted to an unsigned integer, a negative integer is converted to a positive integer. This error mostly occurs in the alert message.

* Error Number: 8032

    Invalid `year` format is used. `year` only accepts 1, 2 or 4 digits.

* Error Number: 8033

    Invalid `year` value is used. The valid range of `year` is (1901, 2155).

* Error Number: 8037

    Invalid `mode` format is used in the `week` function. `mode` must be 1 digit within [0, 7].

* Error Number: 8038

    The field fails to obtain the default value. This error is usually used internally, and is converted to a specific type of error for external applications.

* Error Number: 8040

    Unsupported operations are performed. For example, you perform a table locking operation on a view or a sequence.

* Error Number: 8047

    The value of the system variable is not supported. This error usually occurs in the alarm information when the user sets a variable value that is not supported in the database.

* Error Number: 8048

    An unsupported database isolation level is set.

    If you cannot modify the codes because you are using a third-party tool or framework, consider using [`tidb_skip_isolation_level_check`](/system-variables.md#tidb_skip_isolation_level_check) to bypass this check.

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_skip_isolation_level_check = 1;
    ```

* Error Number: 8050

    An unsupported privilege type is set.

    See [Privileges required for TiDB operations](/privilege-management.md#privileges-required-for-tidb-operations) for the solution.

* Error Number: 8051

    Unknown data type is encountered when TiDB parses the Exec argument list sent by the client.

    If you encounter this error, check the client. If the client is normal, [get support](/support.md) from PingCAP or the community.

* Error Number: 8052

    The serial number of the data packet from the client is incorrect.

    If you encounter this error, check the client. If the client is normal, [get support](/support.md) from PingCAP or the community.

* Error Number: 8055

    The current snapshot is too old. The data may have been garbage collected. You can increase the value of [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) to avoid this problem. TiDB automatically reserves data for long-running transactions. Usually this error does not occur.

    See [garbage collection overview](/garbage-collection-overview.md) and [garbage collection configuration](/garbage-collection-configuration.md).

* Error Number: 8059

    The auto-random ID is exhausted and cannot be allocated. There is no way to recover from such errors currently. It is recommended to use bigint when using the auto random feature to obtain the maximum number of assignment. And try to avoid manually assigning values to the auto random column.

    See [auto random](/auto-random.md) for reference.

* Error Number: 8060

    Invalid auto-incrementing offset. Check the values of `auto_increment_increment` and `auto_increment_offset`.

* Error Number: 8061

    Unsupported SQL Hint.

    See [Optimizer Hints](/optimizer-hints.md) to check and modify the SQL Hint.

* Error Number: 8062

    An invalid token is used in SQL Hint. It conflicts with reserved words in SQL Hint.

    See [Optimizer Hints](/optimizer-hints.md) to check and modify the SQL Hint.

* Error Number: 8063

    The limited memory usage set in SQL Hint exceeds the upper limit of the system. The setting in SQL Hint is ignored.

    See [Optimizer Hints](/optimizer-hints.md) to check and modify the SQL Hint.

* Error Number: 8064

    It fails to parse SQL Hint.

    See [Optimizer Hints](/optimizer-hints.md) to check and modify the SQL Hint.

* Error Number: 8065

    An invalid integer is used in SQL Hint.

    See [Optimizer Hints](/optimizer-hints.md) to check and modify the SQL Hint.

* Error Number: 8066

    The second parameter in the `JSON_OBJECTAGG` function is invalid.

* Error Number: 8101

    The format of plugin ID is incorrect.

    The correct format is `[name]-[version]`, and no `-` is allowed in `name` and `version`.

* Error Number: 8102

    Unable to read the plugin definition information.

    Check the configuration related to the plugin.

* Error Number: 8103

    The plugin name is incorrect.

    Check the configuration of the plugin.

* Error Number: 8104

    The plugin version does not match.

    Check the configuration of the plugin.

* Error Number: 8105

    The plugin is repeatedly loaded.

* Error Number: 8106

    The plugin defines a system variable whose name does not begin with the plugin name.

    Contact the developer of the plugin to modify, or [get support](/support.md) from PingCAP or the community.

* Error Number: 8107

    The loaded plugin does not specify a version, or the specified version is too low.

    Check the configuration of the plugin.

* Error Number: 8108

    Unsupported execution plan type. This error is an internal error.

    If you encounter this error, [get support](/support.md) from PingCAP or the community.

* Error Number: 8109

    The specified index cannot be found when the index is analyzed.

* Error Number: 8110

    The Cartesian product operation cannot be executed.

    Set `cross-join` in the configuration to `true`.

* Error Number: 8111

    When executing the `EXECUTE` statement, the corresponding `Prepare` statement cannot be found.

* Error Number: 8112

    The number of parameters in the `EXECUTE` statement is not consistent with the `Prepare` statement.

* Error Number: 8113

    The table schema related in the `EXECUTE` statement has changed after the `Prepare` statement is executed.

* Error Number: 8115

    It is not supported to prepare multiple lines of statements.

* Error Number: 8116

    It is not supported to prepare DDL statements.

* Error Number: 8120

    The `start tso` of transactions cannot be obtained.

    Check the state/monitor/log of the PD server and the network between the TiDB server and the PD server.

* Error Number: 8121

    Privilege check fails.

    Check the privilege configuration of the database.

* Error Number: 8122

    No corresponding table name is found, given the specified wild cards.

* Error Number: 8123

    An SQL query with aggregate functions returns non-aggregated columns, which violates the `only_full_group_by` mode.

    Modify the SQL statement or disable the `only_full_group_by` mode.

* Error Number: 8129

    TiDB does not yet support JSON objects with the key length >= 65536.

* Error Number: 8130

    The complete error message: `ERROR 8130 (HY000): client has multi-statement capability disabled`

    This error might occur after you upgrade from an earlier version of TiDB. To reduce the impact of SQL injection attacks, TiDB now prevents multiple queries from being executed in the same `COM_QUERY` call by default.

    The system variable [`tidb_multi_statement_mode`](/system-variables.md#tidb_multi_statement_mode-new-in-v4011) can be used to control this behavior.

* Error Number: 8138

    The transaction attempts to write an incorrect row value. For more information, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md#error-8138).

* Error Number: 8139

    The transaction attempts to write a row whose handle is inconsistent with that in the index. For more information, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md#error-8139).

* Error Number: 8140

   The transaction attempts to write a row whose data is inconsistent with the index data. For more information, see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md#error-8140).

* Error Number: 8141

    When a transaction is being committed, the existence assertion of a key fails. For more information,see [Troubleshoot Inconsistency Between Data and Indexes](/troubleshoot-data-inconsistency-errors.md#error-8141).

* Error Number: 8143

    During the execution of a non-transactional DML statement, if a batch fails, the statement is stopped. For more information, see [Non-transactional DML statements](/non-transactional-dml.md).

* Error Number: 8147

    When [`tidb_constraint_check_in_place_pessimistic`](/system-variables.md#tidb_constraint_check_in_place_pessimistic-new-in-v630) is set to `OFF`, to ensure the correctness of transactions, any errors in the SQL statement execution might cause TiDB to return this `8147` error and abort the current transaction. For specific causes of the error, refer to the error message. For more information, see [Constraints](/constraints.md#pessimistic-transactions).

* Error Number: 8200

    The DDL syntax is not yet supported.

    See [compatibility of MySQL DDL](/mysql-compatibility.md#ddl) for reference.

* Error Number: 8214

    The DDL operation is terminated by the `admin cancel` operation.

* Error Number: 8215

    [`ADMIN REPAIR TABLE`](/sql-statements/sql-statement-admin.md#admin-repair-statement) fails.

    If you encounter this error, [get support](/support.md) from PingCAP or the community.

* Error Number: 8216

    The usage of automatic random columns is incorrect.

    See [auto random](/auto-random.md) to modify.

* Error Number: 8223

    This error occurs when detecting that the data is not consistent with the index.

    If you encounter this error, [get support](/support.md) from PingCAP or the community.

* Error Number: 8224

    The DDL job cannot be found.

    Check whether the job id specified by the `restore` operation exists.

* Error Number: 8225

    The DDL operation is completed and cannot be canceled.

* Error Number: 8226

    The DDL operation is almost completed and cannot be canceled.

* Error Number: 8227

    Unsupported options are used when creating Sequence.

    See [Sequence documentation](/sql-statements/sql-statement-create-sequence.md#parameters) to find the list of the supported options.

* Error Number: 8228

    Unsupported types are specified when using `setval` on Sequence.

    See [Sequence documentation](/sql-statements/sql-statement-create-sequence.md#examples) to find the example of the function.

* Error Number: 8229

    The transaction exceeds the survival time.

    Commit or roll back the current transaction, and start a new transaction.

* Error Number: 8230

    TiDB currently does not support using Sequence as the default value on newly added columns, and reports this error if you use it.

* Error Number: 9001

    The complete error message: `ERROR 9001 (HY000): PD Server Timeout`

    The PD request timed out.

    Check the status, monitoring data and log of the PD server, and the network between the TiDB server and the PD server.

* Error Number: 9002

    The complete error message: `ERROR 9002 (HY000): TiKV Server Timeout`

    The TiKV request timed out.

    Check the status, monitoring data and log of the TiKV server, and the network between the TiDB server and the TiKV server.

* Error Number: 9003

    The complete error message: `ERROR 9003 (HY000): TiKV Server is Busy`

    The TiKV server is busy and this usually occurs when the workload is too high.

    Check the status, monitoring data, and log of the TiKV server.

* Error Number: 9004

    The complete error message: `ERROR 9004 (HY000): Resolve Lock Timeout`

    A lock resolving timeout. This error occurs when a large number of transactional conflicts exist in the database.

    Check the application code to see whether lock contention exists in the database.

* Error Number: 9005

    The complete error message: `ERROR 9005 (HY000): Region is unavailable`

    The accessed Region or a certain Raft Group is not available, with possible reasons such as insufficient replicas. This error usually occurs when the TiKV server is busy or the TiKV node is down.

    Check the status, monitoring data and log of the TiKV server.

* Error Number: 9006

    The complete error message: `ERROR 9006 (HY000): GC life time is shorter than transaction duration`

    The interval of `GC Life Time` is too short. The data that should have been read by long transactions might be deleted. You can adjust [`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) using the following command:

    ```sql
    SET GLOBAL tidb_gc_life_time = '30m';
    ```

    > **Note:**
    >
    > "30m" means only cleaning up the data generated 30 minutes ago, which might consume some extra storage space.

* Error Number: 9500

    A single transaction is too large.

    See [the error message `transaction too large`](/faq/migration-tidb-faq.md#the-error-message-transaction-too-large-is-displayed) for the solution.

* Error Number: 9007

    The error message starts with `ERROR 9007 (HY000): Write conflict`.

    If the error message contains `reason=LazyUniquenessCheck`, it means that the transaction is pessimistic, `@@tidb_constraint_check_in_place_pessimistic=OFF` is set, and a write conflict occurs on a unique index for the application. In this case, successful execution of the pessimistic transaction is not guaranteed. You can retry the transaction from the application, or set the variable to `ON` to avoid the error.

* Error Number: 9008

    Too many requests are sent to TiKV at the same time. The number exceeds limit.

    Increase `tidb_store_limit` or set it to `0` to remove the limit on the traffic of requests.

* Error Number: 9010

    TiKV cannot process this raft log.

    Check the state/monitor/log of the TiKV server.

* Error Number: 9012

    The TiFlash request timed out.

    Check the state/monitor/log of the TiFlash server and the network between the TiDB server and TiFlash server.

* Error Number: 9013

    The TiFlash server is busy and this usually occurs when the workload is too high.

    Check the state/monitor/log of the TiFlash server.

### MySQL native error messages

* Error Number: 2013 (HY000)

    The complete error message: `ERROR 2013 (HY000): Lost connection to MySQL server during query`

    You can handle this error as follows:

    - Check whether panic is in the log.
    - Check whether OOM exists in dmesg using `dmesg -T | grep -i oom`.
    - A long time of no access might also lead to this error. It is usually caused by TCP timeout. If TCP is not used for a long time, the operating system kills it.

* Error Number: 1105 (HY000)

    The complete error message: `ERROR 1105 (HY000): other error: unknown error Wire Error(InvalidEnumValue(4004))`

    This error usually occurs when the version of TiDB does not match with that of TiKV. To avoid version mismatch, upgrade all components when you upgrade the version.

* Error Number: 1148 (42000)

    The complete error message: `ERROR 1148 (42000): the used command is not allowed with this TiDB version`

    When you execute the `LOAD DATA LOCAL` statement but the MySQL client does not allow executing this statement (the value of the `local_infile` option is 0), this error occurs.

    The solution is to use the `--local-infile=1` option when you start the MySQL client. For example, run the command `mysql --local-infile=1 -u root -h 127.0.0.1 -P 4000`. The default value of `local-infile` varies in different versions of the MySQL client. Therefore, you need to configure it in specific MySQL clients.

* Error Number: 9001 (HY000)

    The complete error message: `ERROR 9001 (HY000): PD server timeout start timestamp may fall behind safe point`

    This error occurs when TiDB fails to access PD. A worker in the TiDB background continuously queries the safepoint from PD and reports this error if it fails to query within 100s. Generally, it is because the disk on PD is slow and busy or the network failed between TiDB and PD. For the details of common errors, see [Error Number and Fault Diagnosis](/error-codes.md).

* TiDB log error message: EOF error

    When the client or proxy disconnects from TiDB, TiDB does not immediately notice the disconnection. Instead, TiDB notices the disconnection only when it begins to return data to the connection. At this time, the log prints an EOF error.

## Troubleshooting

See the [troubleshooting](/troubleshoot-tidb-cluster.md) and [FAQ](/faq/tidb-faq.md) documents.
