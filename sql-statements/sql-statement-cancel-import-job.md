---
title: CANCEL IMPORT
summary: An overview of the usage of CANCEL IMPORT in TiDB.
---

# CANCEL IMPORT

The `CANCEL IMPORT` statement is used to cancel a data import job created in TiDB.

<!-- Support note for TiDB Cloud:

This TiDB statement is not applicable to TiDB Cloud.

-->

## Required privileges

To cancel a data import job, you need to be the creator of the import job or have the `SUPER` privilege.

## Synopsis

```ebnf+diagram
CancelImportJobsStmt ::=
    'CANCEL' 'IMPORT' 'JOB' JobID
```

## Example

To cancel an import job with the ID as `1`, execute the following statement:

```sql
CANCEL IMPORT JOB 1;
```

The output is as follows:

```
Query OK, 0 rows affected (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
* [`SHOW IMPORT JOB`](/sql-statements/sql-statement-show-import-job.md)
