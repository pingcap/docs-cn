---
title: CANCEL LOAD DATA and DROP LOAD DATA
summary: An overview of the usage of CANCEL LOAD DATA and DROP LOAD DATA for the TiDB database.
---

# CANCEL LOAD DATA and DROP LOAD DATA

The `CANCEL LOAD DATA` statement cancels a LOAD DATA job created in the system.

The `DROP LOAD DATA` statement deletes a LOAD DATA job created in the system.

> **Warning:**
>
> For the current version, this feature is still experimental. It is not recommended to use it in a production environment.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is only available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

## Synopsis

```ebnf+diagram
CancelLoadDataJobsStmt ::=
    'CANCEL' 'LAOD' 'DATA' 'JOB' JobID

DropLoadDataJobsStmt ::=
    'DROP' 'LAOD' 'DATA' 'JOB' JobID
```

## Examples

```sql
CANCEL LOAD DATA JOB 1;
```

```
Query OK, 0 rows affected (0.01 sec)
```

```sql
DROP LOAD DATA JOB 1;
```

```
Query OK, 1 row affected (0.01 sec)
```

## MySQL compatibility

This statement is an extension of TiDB to MySQL syntax.

## See also

* [LOAD DATA](/sql-statements/sql-statement-load-data.md)
* [SHOW LOAD DATA](/sql-statements/sql-statement-show-load-data.md)
