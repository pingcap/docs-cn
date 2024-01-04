---
title: SHOW IMPORT
summary: An overview of the usage of SHOW IMPORT in TiDB.
---

# SHOW IMPORT

The `SHOW IMPORT` statement is used to show the IMPORT jobs created in TiDB. This statement can only show jobs created by the current user.

> **Note:**
>
> This feature is not available on [TiDB Serverless](https://docs.pingcap.com/tidbcloud/select-cluster-tier#tidb-serverless) clusters.

## Required privileges

- `SHOW IMPORT JOBS`: if a user has the `SUPER` privilege, this statement shows all import jobs in TiDB. Otherwise, this statement only shows jobs created by the current user.
- `SHOW IMPORT JOB <job-id>`: only the creator of an import job or users with the `SUPER` privilege can use this statement to view a specific job.

## Synopsis

```ebnf+diagram
ShowImportJobsStmt ::=
    'SHOW' 'IMPORT' 'JOBS'

ShowImportJobStmt ::=
    'SHOW' 'IMPORT' 'JOB' JobID
```

The output fields of the `SHOW IMPORT` statement are described as follows:

| Column           | Description             |
|------------------|-------------------------|
| Job_ID           | The ID of the task                  |
| Data_Source      | Information about the data source                  |
| Target_Table     | The name of the target table                     |
| Phase            | The current phase of the job, including `importing`, `validating`, and `add-index` |
| Status           | The current status of the job, including `pending` (means created but not started yet), `running`, `canceled`, `failed`, and `finished` |
| Source_File_Size | The size of the source file  |
| Imported_Rows | The number of data rows that have been read and written to the target table  |
| Result_Message   | If the import fails, this field returns the error message. Otherwise, it is empty.|
| Create_Time      | The time when the task is created                 |
| Start_Time       | The time when the task is started                     |
| End_Time         | The time when the task is ended            |
| Created_By       | The name of the database user who creates the task         |

## Example

```sql
SHOW IMPORT JOBS;
```

```
+--------+-------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
| Job_ID | Data_Source       | Target_Table | Table_ID | Phase | Status   | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time                 | End_Time                   | Created_By |
+--------+-------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
|      1 | /path/to/file.csv | `test`.`foo` |      116 |       | finished | 11GB             |        950000 |                | 2023-06-26 11:23:59.281257 | 2023-06-26 11:23:59.484932 | 2023-06-26 13:04:30.622952 | root@%     |
|      2 | /path/to/file.csv | `test`.`bar` |      130 |       | finished | 1.194TB          |      49995000 |                | 2023-06-26 15:42:45.079237 | 2023-06-26 15:42:45.388108 | 2023-06-26 17:29:43.023568 | root@%     |
+--------+-------------------+--------------+----------+-------+----------+------------------+---------------+----------------+----------------------------+----------------------------+----------------------------+------------+
1 row in set (0.01 sec)
```

```sql
SHOW IMPORT JOB 60001;
```

```
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
| Job_ID | Data_Source        | Target_Table | Table_ID | Phase | Status  | Source_File_Size | Imported_Rows | Result_Message | Create_Time                | Start_Time | End_Time | Created_By |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
|  60001 | /path/to/small.csv | `test`.`t`   |      361 |       | pending | 16B              |          NULL |                | 2023-06-08 15:59:37.047703 | NULL       | NULL     | root@%     |
+--------+--------------------+--------------+----------+-------+---------+------------------+---------------+----------------+----------------------------+------------+----------+------------+
1 row in set (0.01 sec)
```

## MySQL compatibility

This statement is a TiDB extension to MySQL syntax.

## See also

* [`IMPORT INTO`](/sql-statements/sql-statement-import-into.md)
* [`CANCEL IMPORT JOB`](/sql-statements/sql-statement-cancel-import-job.md)
