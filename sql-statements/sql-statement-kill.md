---
title: KILL
summary: An overview of the usage of KILL for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-kill/','/docs/dev/reference/sql/statements/kill/']
---

# KILL

The `KILL` statement is used to terminate a connection in any TiDB instance in the current TiDB cluster.

## Synopsis

```ebnf+diagram
KillStmt ::= 'KILL' 'TIDB'? ( 'CONNECTION' | 'QUERY' )? CONNECTION_ID
```

## Examples

The following example shows how to get all active queries in the current cluster and terminate any one of them.

{{< copyable "sql" >}}

```sql
SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST;
```

```
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| ID                  | USER | INSTANCE        | INFO                                                                        |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
| 8306449708033769879 | root | 127.0.0.1:10082 | select sleep(30), 'foo'                                                     |
| 5857102839209263511 | root | 127.0.0.1:10080 | select sleep(50)                                                            |
| 5857102839209263513 | root | 127.0.0.1:10080 | SELECT ID, USER, INSTANCE, INFO FROM INFORMATION_SCHEMA.CLUSTER_PROCESSLIST |
+---------------------+------+-----------------+-----------------------------------------------------------------------------+
```

{{< copyable "sql" >}}

```sql
KILL 5857102839209263511;
```

```
Query OK, 0 rows affected (0.00 sec)
```

## MySQL compatibility

- The `KILL` statement of MySQL can only terminate a connection in the currently connected MySQL instance, while the `KILL` statement of TiDB can terminate a connection in any TiDB instance in the entire cluster.
- In v7.2.0 and earlier versions, using the MySQL command line <kbd>Control+C</kbd> to terminate a query or connection in TiDB is not supported.

## Behavior change descriptions

<CustomContent platform="tidb">

Starting from v7.3.0, TiDB supports generating 32-bit connection IDs, which is enabled by default and controlled by the [`enable-32bits-connection-id`](/tidb-configuration-file.md#enable-32bits-connection-id-new-in-v730) configuration item. When both the Global Kill feature and 32-bit connection ID are enabled, TiDB generates a 32-bit connection ID and you can terminate queries or connections in the MySQL command-line using <kbd>Control+C</kbd>.

> **Warning:**
>
> When the number of TiDB instances in the cluster exceeds 2048 or the concurrent connection count of a single TiDB instance exceeds 1048576, the 32-bit connection ID space becomes insufficient and is automatically upgraded to 64-bit connection IDs. During the upgrade process, existing business and established connections are unaffected. However, subsequent new connections cannot be terminated using <kbd>Control+C</kbd> in the MySQL command-line.

Starting from v6.1.0, TiDB supports the Global Kill feature, which is enabled by default and controlled by the [`enable-global-kill`](/tidb-configuration-file.md#enable-global-kill-new-in-v610) configuration.

</CustomContent>

<CustomContent platform="tidb-cloud">

Starting from v7.3.0, TiDB supports generating 32-bit connection IDs, which is enabled by default. When both the Global Kill feature and 32-bit connection ID are enabled, You can terminate queries or connections in the MySQL command-line using <kbd>Control+C</kbd>.

Starting from v6.1.0, TiDB supports the Global Kill feature, which is enabled by default.

</CustomContent>

When the Global Kill feature is enabled, both `KILL` and `KILL TIDB` statements can terminate queries or connections across instances so you do not need to worry about erroneously terminating queries or connections. When you use a client to connect to any TiDB instance and execute the `KILL` or `KILL TIDB` statement, the statement will be forwarded to the target TiDB instance. If there is a proxy between the client and the TiDB cluster, the `KILL` and `KILL TIDB` statements will also be forwarded to the target TiDB instance for execution.

If the Global Kill feature is not enabled or you are using a TiDB version earlier than v6.1.0, note the following:

- By default, `KILL` is not compatible with MySQL. This helps prevent against a case of a connection being terminated by a wrong TiDB server, because it is common to place multiple TiDB servers behind a load balancer. To terminate other connections on the currently connected TiDB instance, you need to add the `TIDB` suffix explicitly by executing the `KILL TIDB` statement.

<CustomContent platform="tidb">

- It is **STRONGLY NOT RECOMMENDED** to set [`compatible-kill-query = true`](/tidb-configuration-file.md#compatible-kill-query) in your configuration file UNLESS you are certain that clients will be always connected to the same TiDB instance. This is because pressing <kbd>Control+C</kbd> in the default MySQL client opens a new connection in which `KILL` is executed. If there is a proxy between the client and the TiDB cluster, the new connection might be routed to a different TiDB instance, which possibly kills a different session by mistake.

</CustomContent>

- The `KILL TIDB` statement is a TiDB extension. The feature of this statement is similar to the MySQL `KILL [CONNECTION|QUERY]` command and the MySQL command line <kbd>Control+C</kbd>. It is safe to use `KILL TIDB` on the same TiDB instance.

## See also

* [SHOW \[FULL\] PROCESSLIST](/sql-statements/sql-statement-show-processlist.md)
* [CLUSTER_PROCESSLIST](/information-schema/information-schema-processlist.md#cluster_processlist)
