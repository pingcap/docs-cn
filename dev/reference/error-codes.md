---
title: Error Codes and Troubleshooting
summary: Learn about the error codes and solutions in TiDB.
category: reference
---

# Error Codes and Troubleshooting

This document describes the problems encountered during the use of TiDB and provides the solutions.

## Error codes

TiDB is compatible with the error codes in MySQL, and in most cases returns the same error code as MySQL. In addition, TiDB has the following unique error codes:

| Error code | Description | Solution |
| ---- | ------- | --------- |
| 8001 | The memory used by the request exceeds the threshold limit for the TiDB memory usage. | Increase the value of the system variable with the `tidb_mem_quota` prefix. |
| 8002 | To guarantee consistency, a transaction with the `SELECT FOR UPDATE` statement cannot be retried when it encounters a commit conflict. TiDB rolls back the transaction and returns this error. | Retry the failed transaction. |
| 8003 | If the data in a row is not consistent with the index when executing the `ADMIN CHECK TABLE` command, TiDB returns this error. |
| 8004 | A single transaction is too large. | See [the error message `transaction too large`](/dev/faq/tidb.md#the-error-message-transaction-too-large-is-displayed) for the cause and solution.  |
| 8005 | Transactions in TiDB encounter write conflicts. | See [the Troubleshoot section](/dev/faq/tidb.md#troubleshoot) for the cause and solution. |
| 8018 | The plugin cannot be reloaded because it has not been loaded before. |
| 8019 | The version of the plugin that is being reloaded is different from the previous version. Therefore, the plugin cannot be reloaded. |
| 8020 | The table is locked. |
| 8021 | The key does not exist. |
| 8022 | The transaction commit fails. You can retry the process. |
| 8023 | An empty value is not allowed. |
| 8024 | Invalid transactions. |
| 8025 | The single Key-Value pair being written is too large. |
| 8026 | The interface has not been implemented. |
| 8027 | The table schema version is outdated. |
| 8028 | The table schema has changed. |
| 8029 | Incorrect value. |
| 8030 | After an unsigned positive integer is converted to a signed integer, it exceeds the maximum value and displays as a negative integer.|
| 8031 | When being converted to an unsigned integer, a negative integer is converted to a positive integer. |
| 8032 | Invalid `year` format. |
| 8033 | Invalid `year` value. |
| 8034 | Incorrect `datetime` value. |
| 8036 | Invalid `time` format. |
| 8037 | Invalid `week` format. |
| 8038 | The field fails to obtain the default value. |
| 8039 | Index offset is out of range. |
| 8042 | The state of table schema does not exist. |
| 8043 | The state of column information does not exist. |
| 8044 | The state of index does not exist. |
| 8045 | Invalid table data. |
| 8046 | The state of column information is invisible. |
| 8047 | The value of the system variable is not supported. This error usually occurs in the alarm information when the user sets a variable value that is not supported in the database. |
| 8048 | An unsupported database isolation level is set. |
| 8049 | It fails to load the privilege related table. |
| 8050 | An unsupported privilege type is set. |
| 8051 | Unknown field type. |
| 8052 | The serial number of the data packet from the client is incorrect. |
| 8053 | An invalid auto-incrementing column value is obtained. |
| 8055 | The current snapshot is too old. The data may have been garbage collected. |
| 8056 | Invalid table ID. |
| 8057 | Invalid field type. |
| 8058 | You apply an automatic variable type that does not exist. |
| 8059 | It fails to obtain an auto-random ID. |
| 8060 | Invalid auto-incrementing offset. |
| 8061 | Unsupported SQL Hint. |
| 8062 | An invalid token is used in SQL Hint. It conflicts with reserved words in SQL Hint. |
| 8063 | The limited memory usage set in SQL Hint exceeds the upper limit of the system. The setting in SQL Hint is ignored. |
| 8064 | It fails to parse SQL Hint. |
| 8065 | An invalid integer is used in SQL Hint. |
| 8066 | The second parameter in the `JSON_OBJECTAGG` function is invalid. |
| 8101 | The format of plugin ID is incorrect. | The correct format is `[name]-[version]`, and no `-` is allowed in `name` and `version`. |
| 8102 | Unable to read the plugin definition information. |
| 8103 | The plugin name is incorrect. |
| 8104 | The plugin version does not match. |
| 8105 | The plugin is repeatedly loaded. |
| 8106 | The plugin defines a system variable whose name does not begin with the plugin name. |
| 8107 | The loaded plugin does not specify a version, or the specified version is too low. |
| 8108 | Unsupported execution plan type. |
| 8109 | The specified index cannot be found when the index is analyzed. |
| 8110 | The Cartesian product operation cannot be executed. | Set `cross-join` in the configuration to `true`. |
| 8111 | When executing the `EXECUTE` statement, the corresponding `Prepare` statement cannot be found. |
| 8112 | The number of parameters in the `EXECUTE` statement is not consistent with the `Prepare` statement. |
| 8113 | The table schema related in the `EXECUTE` statement has changed after the `Prepare` statement is executed. |
| 8114 | Unknown execution plan type. |
| 8115 | It is not supported to prepare multiple lines of statements. |
| 8116 | It is not supported to prepare DDL statements. |
| 8118 | Executor build fails. |
| 8120 | The `start tso` of transactions cannot be obtained. |
| 8121 | Privilege check fails. |
| 8122 | No corresponding table name is found, given the specified wild cards. |
| 8123 | An SQL query with aggregate functions returns non-aggregated columns, which violates the `only_full_group_by` mode. |
| 8200 | The DDL syntax is not yet supported. |
| 8201 | TiDB is currently not the DDL owner. |
| 8202 | The index cannot be decoded. |
| 8203 | Invalid DDL worker. |
| 8204 | Invalid DDL job. |
| 8205 | Invalid DDL job mark. |
| 8206 | The DDL operation in `re-organize` phase timed out. |
| 8207 | Invalid storage nodes. |
| 8210 | Invalid DDL state. |
| 8211 | Panic occurs during the DDL operation in `re-organize` phase. |
| 8212 | Invalid split range of Region. |
| 8213 | Invalid DDL job version. |
| 8214 | The DDL operation is terminated. |
| 8215 | `ADMIN REPAIR TABLE` fails. |
| 8216 | Invalid automatic random columns. |
| 8221 | Incorrect Key encoding. |
| 8222 | Incorrect index Key encoding. |
| 8223 | This error occurs when detecting that the data is not consistent with the index. |
| 8224 | The DDL job cannot be found. |
| 8225 | The DDL operation is completed and cannot be canceled. |
| 8226 | The DDL operation is almost completed and cannot be canceled. |
| 8227 | Unsupported options are used when creating Sequence. |
| 9001 | The PD request timed out. | Check the state/monitor/log of the PD server and the network between the TiDB server and the PD server. |
| 9002 | The TiKV request timed out. | Check the state/monitor/log of the TiKV server and the network between the TiDB server and the TiKV server. |
| 9003 | The TiKV server is busy and this usually occurs when the workload is too high. | Check the state/monitor/log of the TiKV server. |
| 9004 | This error occurs when a large number of transactional conflicts exist in the database. | Check the code of application. |
| 9005 | A certain Raft Group is not available, such as the number of replicas is not enough. This error usually occurs when the TiKV server is busy or the TiKV node is down. | Check the state/monitor/log of the TiKV server. |
| 9006 | The interval of GC Life Time is too short and the data that should be read by the long transactions might be cleared. | Extend the interval of GC Life Time. |
| 9500 | A single transaction is too large. | See [the error message `transaction too large`](/dev/faq/tidb.md#the-error-message-transaction-too-large-is-displayed) for the solution. |
| 9007 | Transactions in TiKV encounter write conflicts. | See [the Troubleshoot section](/dev/faq/tidb.md#troubleshoot) for the cause and solution. |
| 9008 | Too many requests are sent to TiKV at the same time. The number exceeds limit. |

## Troubleshooting

See the [troubleshooting](/dev/how-to/troubleshoot/cluster-setup.md) and [FAQ](/dev/faq/tidb.md) documents.
