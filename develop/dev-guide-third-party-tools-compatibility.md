---
title: Known Incompatibility Issues with Third-Party Tools
summary: Describes TiDB compatibility issues with third-party tools found during testing.
---

# Known Incompatibility Issues with Third-Party Tools

> **Note:**
>
> The [Unsupported features](/mysql-compatibility.md#unsupported-features) section lists the unsupported features in TiDB, including:
>
> - Stored procedures and functions
> - Triggers
> - Events
> - User-defined functions
> - `FOREIGN KEY` constraints
> - `SPATIAL` functions, data types and indexes
> - `XA` syntax
>
> The preceding unsupported features are expected behavior and are not listed in this document. For more details, see [MySQL Compatibility](/mysql-compatibility.md).

## General incompatibility

### `SELECT CONNECTION_ID()` returns a 64-bit integer in TiDB

**Description**

The `SELECT CONNECTION_ID()` function returns a 64-bit integer in TiDB, such as `2199023260887`, while it returns a 32-bit integer in MySQL, such as `391650`.

**Way to avoid**

In a TiDB application, to avoid data overflow, you should use a 64-bit integer or string type to store the result of `SELECT CONNECTION_ID()`. For example, you can use `Long` or `String` in Java and use `string` in JavaScript or TypeScript.

### TiDB does not maintain `Com_*` counters

**Description**

MySQL maintains a series of [server status variables starting with `Com_`](https://dev.mysql.com/doc/refman/8.0/en/server-status-variables.html#statvar_Com_xxx) to keep track of the total number of operations you have performed on the database. For example, `Com_select` records the total number of `SELECT` statements initiated by MySQL since it was last started (even if the statements were not queried successfully). TiDB does not maintain these variables. You can use the statement [`SHOW GLOBAL STATUS LIKE 'Com_%'`](/sql-statements/sql-statement-show-status.md) to see the difference between TiDB and MySQL.

**Way to avoid**

Do not use these variables. One common scenario is monitoring. TiDB is well observable and does not require querying from server status variables. For custom monitoring tools, refer to [TiDB Monitoring Framework Overview](/tidb-monitoring-framework.md).

### TiDB distinguishes between `TIMESTAMP` and `DATETIME` in error messages

**Description**

TiDB error messages distinguish between `TIMESTAMP` and `DATETIME`, while MySQL does not, and returns them all as `DATETIME`. That is, MySQL incorrectly converts `TIMESTAMP` type error messages to `DATETIME` type.

**Way to avoid**

Do not use the error messages for string matching. Instead, use [Error Codes](/error-codes.md) for troubleshooting.

### TiDB does not support the `CHECK TABLE` statement

**Description**

The `CHECK TABLE` statement is not supported in TiDB.

**Way to avoid**

To check the consistency of data and corresponding indexes, you can use the [`ADMIN CHECK [TABLE|INDEX]`](/sql-statements/sql-statement-admin-check-table-index.md) statement in TiDB.

## Compatibility with MySQL JDBC

The test version is MySQL Connector/J 8.0.29.

### The default collation is inconsistent

**Description**

The collations of MySQL Connector/J are stored on the client side and distinguished by the server version.

The following table lists known client-side and server-side collation inconsistencies in character sets:

| Character | Client-side default collation | Server-side default collation |
| --------- | -------------------- | ------------- |
| `ascii`   | `ascii_general_ci`   | `ascii_bin`   |
| `latin1`  | `latin1_swedish_ci`  | `latin1_bin`  |
| `utf8mb4` | `utf8mb4_0900_ai_ci` | `utf8mb4_bin` |

**Way to avoid**

Set the collation manually, and do not rely on the client-side default collation. The client-side default collation is stored by the MySQL Connector/J configuration file.

### The `NO_BACKSLASH_ESCAPES` parameter does not take effect

**Description**

In TiDB, you cannot use the `NO_BACKSLASH_ESCAPES` parameter without escaping the `\` character. For more details, track this [issue](https://github.com/pingcap/tidb/issues/35302).

**Way to avoid**

Do not use `NO_BACKSLASH_ESCAPES` with `\` in TiDB, but use `\\` in SQL statements.

### The `INDEX_USED` related parameters are not supported

**Description**

TiDB does not set the `SERVER_QUERY_NO_GOOD_INDEX_USED` and `SERVER_QUERY_NO_INDEX_USED` parameters in the protocol. This will cause the following parameters to be returned inconsistently with the actual situation:

- `com.mysql.cj.protocol.ServerSession.noIndexUsed()`
- `com.mysql.cj.protocol.ServerSession.noGoodIndexUsed()`

**Way to avoid**

Do not use the `noIndexUsed()` and `noGoodIndexUsed()` functions in TiDB.

### The `enablePacketDebug` parameter is not supported

**Description**

TiDB does not support the [enablePacketDebug](https://dev.mysql.com/doc/connector-j/8.0/en/connector-j-connp-props-debugging-profiling.html) parameter. It is a MySQL Connector/J parameter used for debugging that will keep the buffer of the data packet. This might cause the connection to close unexpectedly. **DO NOT** turn it on.

**Way to avoid**

Do not set the `enablePacketDebug` parameter in TiDB.

### The UpdatableResultSet is not supported

**Description**

TiDB does not support `UpdatableResultSet`. **DO NOT** specify the `ResultSet.CONCUR_UPDATABLE` parameter and **DO NOT** update data inside the `ResultSet`.

**Way to avoid**

To ensure data consistency by transaction, you can use `UPDATE` statements to update data.

## MySQL JDBC bugs

### `useLocalTransactionState` and `rewriteBatchedStatements` are true at the same time will cause the transaction to fail to commit or roll back

**Description**

When the `useLocalTransactionState` and `rewriteBatchedStatements` parameters are set to `true` at the same time, the transaction might fail to commit. You can reproduce with [this code](https://github.com/Icemap/tidb-java-gitpod/tree/reproduction-local-transaction-state-txn-error).

**Way to avoid**

> **Note:**
>
> This bug has been reported to MySQL JDBC. To keep track of the process, you can follow this [Bug Report](https://bugs.mysql.com/bug.php?id=108643).

**DO NOT** turn on `useLocalTransactionState` as this might prevent transactions from being committed or rolled back.

### Connector is incompatible with the server version earlier than 5.7.5

**Description**

The database connection might hang under certain conditions when using MySQL Connector/J 8.0.29 with a MySQL server < 5.7.5 or a database using the MySQL server < 5.7.5 protocol (such as TiDB earlier than v6.3.0). For more details, see the [Bug Report](https://bugs.mysql.com/bug.php?id=106252).

**Way to avoid**

This is a known issue. As of October 12, 2022, MySQL Connector/J has not fixed the issue.

TiDB fixes it in the following ways:

- Client side: This bug has been fixed in **pingcap/mysql-connector-j** and you can use the [pingcap/mysql-connector-j](https://github.com/pingcap/mysql-connector-j) instead of the official MySQL Connector/J.
- Server side: This compatibility issue has been fixed since TiDB v6.3.0 and you can upgrade the server to v6.3.0 or later versions.
