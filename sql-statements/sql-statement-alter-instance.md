---
title: ALTER INSTANCE
summary: Learn the overview of the `ALTER INSTANCE` usage in TiDB.
aliases: ['/docs/dev/sql-statements/sql-statement-alter-instance/','/docs/dev/reference/sql/statements/alter-instance/']
---

# ALTER INSTANCE

The `ALTER INSTANCE` statement is used to make changes to a single TiDB instance. Currently, TiDB only supports the `RELOAD TLS` clause.

## RELOAD TLS

You can execute the `ALTER INSTANCE RELOAD TLS` statement to reload the certificate ([`ssl-cert`](/tidb-configuration-file.md#ssl-cert)), the key ([`ssl-key`](/tidb-configuration-file.md#ssl-key)), and the CA ([`ssl-ca`](/tidb-configuration-file.md#ssl-ca)) from the original configuration path.

The newly loaded certificate, key, and CA take effect on the connection that is established after the statement is successfully executed. The connection established before this statement execution is not affected.

When an error occurs during reloading, by default, this error message is returned and the previous key and certificate continue to be used. However, if you have added the optional `NO ROLLBACK ON ERROR`, when an error occurs during reloading, the error is not returned, and the subsequent requests are handled  with the TLS security connection disabled.

## Syntax diagram

**AlterInstanceStmt:**

![AlterInstanceStmt](/media/sqlgram/AlterInstanceStmt.png)

**InstanceOption:**

![InstanceOption](/media/sqlgram/InstanceOption.png)

## Example

{{< copyable "sql" >}}

```sql
ALTER INSTANCE RELOAD TLS;
```

## MySQL compatibility

The `ALTER INSTANCE RELOAD TLS` statement only supports reloading from the original configuration path. It does not support dynamically modifying the loading path or dynamically enabling the TLS encrypted connection feature when TiDB is started. This feature is disabled by default when you restart TiDB.

## See also

[Enable TLS Between TiDB Clients and Servers](/enable-tls-between-clients-and-servers.md).
