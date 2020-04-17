---
title: Error Codes and Troubleshooting
summary: Learn about the error codes and solutions in TiDB.
category: reference
---

# Error Codes and Troubleshooting

This document describes the problems encountered during the use of TiDB and provides the solutions.

## Error codes

TiDB is compatible with the error codes in MySQL, and in most cases returns the same error code as MySQL. For a list of error codes for MySQL, see [Server Error Message Reference](https://dev.mysql.com/doc/refman/5.7/en/server-error-reference.html).
In addition, TiDB has the following unique error codes:

* Error Number: 8001

    The memory used by the request exceeds the threshold limit for the TiDB memory usage.

    Increase the value of the system variable with the `tidb_mem_quota` prefix.

* Error Number: 8002

    To guarantee consistency, a transaction with the `SELECT FOR UPDATE` statement cannot be retried when it encounters a commit conflict. TiDB rolls back the transaction and returns this error.

    Retry the failed transaction.

* Error Number: 8003

    If the data in a row is not consistent with the index when executing the `ADMIN CHECK TABLE` command, TiDB returns this error.

* Error Number: 8004

    A single transaction is too large.

    See [the error message `transaction too large`](/faq/tidb.md#the-error-message-transaction-too-large-is-displayed) for the cause and solution.

* Error Number: 8005

    Transactions in TiDB encounter write conflicts.

    See [the Troubleshoot section](/faq/tidb.md#troubleshoot) for the cause and solution.

* Error Number: 8018

    The plugin cannot be reloaded because it has not been loaded before.

* Error Number: 8019

    The version of the plugin that is being reloaded is different from the previous version. Therefore, the plugin cannot be reloaded.

* Error Number: 8020

    The table is locked.

* Error Number: 8021

    The key does not exist.

* Error Number: 8022

    The transaction commit fails. You can retry the process.

* Error Number: 8023

    An empty value is not allowed.

* Error Number: 8024

    Invalid transactions.

* Error Number: 8025

    The single Key-Value pair being written is too large.

* Error Number: 8026

    The interface has not been implemented.

* Error Number: 8027

    The table schema version is outdated.

* Error Number: 8028

    The table schema has changed.

* Error Number: 8029

    Incorrect value.

* Error Number: 8030

    After an unsigned positive integer is converted to a signed integer, it exceeds the maximum value and displays as a negative integer.

* Error Number: 8031

    When being converted to an unsigned integer, a negative integer is converted to a positive integer.

* Error Number: 8032

    Invalid `year` format.

* Error Number: 8033

    Invalid `year` value.

* Error Number: 8034

    Incorrect `datetime` value.

* Error Number: 8036

    Invalid `time` format.

* Error Number: 8037

    Invalid `week` format.

* Error Number: 8038

    The field fails to obtain the default value.

* Error Number: 8039

    Index offset is out of range.

* Error Number: 8042

    The state of table schema does not exist.

* Error Number: 8043

    The state of column information does not exist.

* Error Number: 8044

    The state of index does not exist.

* Error Number: 8045

    Invalid table data.

* Error Number: 8046

    The state of column information is invisible.

* Error Number: 8047

    The value of the system variable is not supported. This error usually occurs in the alarm information when the user sets a variable value that is not supported in the database.

* Error Number: 8048

    An unsupported database isolation level is set.

* Error Number: 8049

    It fails to load the privilege related table.

* Error Number: 8050

    An unsupported privilege type is set.

* Error Number: 8051

    Unknown field type.

* Error Number: 8052

    The serial number of the data packet from the client is incorrect.

* Error Number: 8053

    An invalid auto-incrementing column value is obtained.

* Error Number: 8055

    The current snapshot is too old. The data may have been garbage collected.

* Error Number: 8056

    Invalid table ID.

* Error Number: 8057

    Invalid field type.

* Error Number: 8058

    You apply an automatic variable type that does not exist.

* Error Number: 8059

    It fails to obtain an auto-random ID.

* Error Number: 8060

    Invalid auto-incrementing offset.

* Error Number: 8061

    Unsupported SQL Hint.

* Error Number: 8062

    An invalid token is used in SQL Hint. It conflicts with reserved words in SQL Hint.

* Error Number: 8063

    The limited memory usage set in SQL Hint exceeds the upper limit of the system. The setting in SQL Hint is ignored.

* Error Number: 8064

    It fails to parse SQL Hint.

* Error Number: 8065

    An invalid integer is used in SQL Hint.

* Error Number: 8066

    The second parameter in the `JSON_OBJECTAGG` function is invalid.

* Error Number: 8101

    The format of plugin ID is incorrect.

    The correct format is `[name]-[version]`, and no `-` is allowed in `name` and `version`.

* Error Number: 8102

    Unable to read the plugin definition information.

* Error Number: 8103

    The plugin name is incorrect.

* Error Number: 8104

    The plugin version does not match.

* Error Number: 8105

    The plugin is repeatedly loaded.

* Error Number: 8106

    The plugin defines a system variable whose name does not begin with the plugin name.

* Error Number: 8107

    The loaded plugin does not specify a version, or the specified version is too low.

* Error Number: 8108

    Unsupported execution plan type.

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

* Error Number: 8114

    Unknown execution plan type.

* Error Number: 8115

    It is not supported to prepare multiple lines of statements.

* Error Number: 8116

    It is not supported to prepare DDL statements.

* Error Number: 8118

    Executor build fails.

* Error Number: 8120

    The `start tso` of transactions cannot be obtained.

* Error Number: 8121

    Privilege check fails.

* Error Number: 8122

    No corresponding table name is found, given the specified wild cards.

* Error Number: 8123

    An SQL query with aggregate functions returns non-aggregated columns, which violates the `only_full_group_by` mode.

* Error Number: 8200

    The DDL syntax is not yet supported.

* Error Number: 8201

    TiDB is currently not the DDL owner.

* Error Number: 8202

    The index cannot be decoded.

* Error Number: 8203

    Invalid DDL worker.

* Error Number: 8204

    Invalid DDL job.

* Error Number: 8205

    Invalid DDL job mark.

* Error Number: 8206

    The DDL operation in `re-organize` phase timed out.

* Error Number: 8207

    Invalid storage nodes.

* Error Number: 8210

    Invalid DDL state.

* Error Number: 8211

    Panic occurs during the DDL operation in `re-organize` phase.

* Error Number: 8212

    Invalid split range of Region.

* Error Number: 8213

    Invalid DDL job version.

* Error Number: 8214

    The DDL operation is terminated.

* Error Number: 8215

    `ADMIN REPAIR TABLE` fails.

* Error Number: 8216

    Invalid automatic random columns.

* Error Number: 8221

    Incorrect Key encoding.

* Error Number: 8222

    Incorrect index Key encoding.

* Error Number: 8223

    This error occurs when detecting that the data is not consistent with the index.

* Error Number: 8224

    The DDL job cannot be found.

* Error Number: 8225

    The DDL operation is completed and cannot be canceled.

* Error Number: 8226

    The DDL operation is almost completed and cannot be canceled.

* Error Number: 8227

    Unsupported options are used when creating Sequence.

* Error Number: 8229

    The transaction exceeds the survival time.

    Commit or roll back the current transaction, and start a new transaction.

* Error Number: 9001

    The PD request timed out.

    Check the state/monitor/log of the PD server and the network between the TiDB server and the PD server.

* Error Number: 9002

    The TiKV request timed out.

    Check the state/monitor/log of the TiKV server and the network between the TiDB server and the TiKV server.

* Error Number: 9003

    The TiKV server is busy and this usually occurs when the workload is too high.

    Check the state/monitor/log of the TiKV server.

* Error Number: 9004

    This error occurs when a large number of transactional conflicts exist in the database.

    Check the code of application.

* Error Number: 9005

    A certain Raft Group is not available, such as the number of replicas is not enough. This error usually occurs when the TiKV server is busy or the TiKV node is down.

    Check the state/monitor/log of the TiKV server.

* Error Number: 9006

    The interval of GC Life Time is too short and the data that should be read by the long transactions might be cleared.

    Extend the interval of GC Life Time.

* Error Number: 9500

    A single transaction is too large.

    See [the error message `transaction too large`](/faq/tidb.md#the-error-message-transaction-too-large-is-displayed) for the solution.

* Error Number: 9007

    Transactions in TiKV encounter write conflicts.

    See [the Troubleshoot section](/faq/tidb.md#troubleshoot) for the cause and solution.

* Error Number: 9008

    Too many requests are sent to TiKV at the same time. The number exceeds limit.

## Troubleshooting

See the [troubleshooting](/how-to/troubleshoot/cluster-setup.md) and [FAQ](/faq/tidb.md) documents.
