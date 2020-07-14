---
title: SHOW PLUGINS
summary: An overview of the usage of SHOW PLUGINS for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-plugins/']
---

# SHOW PLUGINS

`SHOW PLUGINS` shows all plugins installed in TiDB, including each plugin's status and version information.

## Synopsis

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

**ShowTargetFilterable:**

![ShowTargetFilterable](/media/sqlgram/ShowTargetFilterable.png)

## Examples

{{< copyable "sql" >}}

```sql
SHOW PLUGINS;
```

```
+-------+--------------+-------+-----------------------------+---------+---------+
| Name  | Status       | Type  | Library                     | License | Version |
+-------+--------------+-------+-----------------------------+---------+---------+
| audit | Ready-enable | Audit | /tmp/tidb/plugin/audit-1.so |         | 1       |
+-------+--------------+-------+-----------------------------+---------+---------+
1 row in set (0.000 sec)
```

{{< copyable "sql" >}}

```sql
SHOW PLUGINS LIKE 'a%';
```

```
+-------+--------------+-------+-----------------------------+---------+---------+
| Name  | Status       | Type  | Library                     | License | Version |
+-------+--------------+-------+-----------------------------+---------+---------+
| audit | Ready-enable | Audit | /tmp/tidb/plugin/audit-1.so |         | 1       |
+-------+--------------+-------+-----------------------------+---------+---------+
1 row in set (0.000 sec)
```

## MySQL compatibility

This statement is understood to be fully compatible with MySQL. Any compatibility differences should be [reported via an issue](/report-issue.md) on GitHub.
