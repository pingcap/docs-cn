---
title: Error Codes and Troubleshooting
summary: Learn about the error codes and solutions in TiDB.
category: reference
aliases: ['/docs/sql/error/']
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
| 8004 | A single transaction is too large. | See [the answer of the error message `transaction too large`](/v3.0/faq/tidb.md#the-error-message-transaction-too-large-is-displayed) for the cause and solution.  |
| 8005 | Transactions in TiDB encounter write conflicts. | See [the Troubleshoot section](/v3.0/faq/tidb.md#troubleshoot) for the cause and solution. |
| 9001 | The PD request timed out. | Check the state/monitor/log of the PD server and the network between the TiDB server and the PD server. |
| 9002 | The TiKV request timed out. | Check the state/monitor/log of the TiKV server and the network between the TiDB server and the TiKV server. |
| 9003 | The TiKV server is busy and this usually occurs when the workload is too high. | Check the state/monitor/log of the TiKV server. |
| 9004 | This error occurs when a large number of transactional conflicts exist in the database. | Check the code of application. |
| 9005 | A certain Raft Group is not available, such as the number of replicas is not enough. This error usually occurs when the TiKV server is busy or the TiKV node is down. | Check the state/monitor/log of the TiKV server. |
| 9006 | The interval of GC Life Time is too short and the data that should be read by the long transactions might be cleared. | Extend the interval of GC Life Time. |
| 9500 | A single transaction is too large. | See [the error message `transaction too large`](/v3.0/faq/tidb.md#the-error-message-transaction-too-large-is-displayed) for the solution. |
| 9007 | Transactions in TiKV encounter write conflicts. | See [the Troubleshoot section](/v3.0/faq/tidb.md#troubleshoot) for the cause and solution. |

## Troubleshooting

See the [troubleshooting](/v3.0/how-to/troubleshoot/cluster-setup.md) and [FAQ](/v3.0/faq/tidb.md) documents.
