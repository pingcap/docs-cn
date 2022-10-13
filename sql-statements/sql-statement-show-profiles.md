---
title: SHOW PROFILES
summary: An overview of the usage of SHOW PROFILES for the TiDB database.
aliases: ['/docs/dev/sql-statements/sql-statement-show-profiles/']
---

# SHOW PROFILES

The `SHOW PROFILES` statement currently only returns an empty result.

## Synopsis

**ShowStmt:**

![ShowStmt](/media/sqlgram/ShowStmt.png)

## Examples

{{< copyable "sql" >}}

```sql
SHOW PROFILES;
```

```
Empty set (0.00 sec)
```

## MySQL compatibility

This statement is included only for compatibility with MySQL. Executing `SHOW PROFILES` always returns an empty result.