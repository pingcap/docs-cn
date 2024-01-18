---
title: ADMIN [SET|SHOW|UNSET] BDR ROLE
summary: An overview of the usage of ADMIN [SET|SHOW|UNSET] BDR ROLE for the TiDB database.
---

# ADMIN [SET|SHOW|UNSET] BDR ROLE

- Use `ADMIN SET BDR ROLE` to set the BDR role of the cluster. Currently, you can set the following BDR roles for a TiDB cluster: `PRIMARY` and `SECONDARY`. For more information about BDR roles, see [DDL Synchronization in TiCDC Bidirectional Replication](/ticdc/ticdc-bidirectional-replication.md#ddl-replication).
- Use `ADMIN SHOW BDR ROLE` to show the BDR role of the cluster.
- Use `ADMIN UNSET BDR ROLE` to unset the BDR role of the cluster.

> **Warning:**
>
> This feature is experimental. It is not recommended that you use it in the production environment. This feature might be changed or removed without prior notice. If you find a bug, you can report an [issue](https://github.com/pingcap/tidb/issues) on GitHub.

## Synopsis

```ebnf+diagram
AdminShowBDRRoleStmt ::=
    'ADMIN' 'SHOW' 'BDR' 'ROLE'

AdminSetBDRRoleStmt ::=
    'ADMIN' 'SET' 'BDR' 'ROLE' ('PRIMARY' | 'SECONDARY')

AdminUnsetBDRRoleStmt ::=
    'ADMIN' 'UNSET' 'BDR' 'ROLE'
```

## Examples

By default, a TiDB cluster has no BDR role. Run the following command to show the BDR role of the cluster.

```sql
ADMIN SHOW BDR ROLE;
```

```sql
+------------+
| BDR_ROLE   |
+------------+
|            |
+------------+
1 row in set (0.01 sec)
```

Run the following command to set the BDR role to `PRIMARY`.

```sql
ADMIN SET BDR ROLE PRIMARY;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
ADMIN SHOW BDR ROLE;
+----------+
| BDR_ROLE |
+----------+
| primary  |
+----------+
1 row in set (0.00 sec)
```

Run the following command to unset the BDR role of the cluster.

```sql
ADMIN UNSET BDR ROLE;
```

```sql
Query OK, 0 rows affected (0.01 sec)
```

```sql
ADMIN SHOW BDR ROLE;
+----------+
| BDR_ROLE |
+----------+
|          |
+----------+
1 row in set (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.
