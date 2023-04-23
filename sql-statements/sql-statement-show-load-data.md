---
title: SHOW LOAD DATA
summary: An overview of the usage of SHOW LOAD DATA for the TiDB database.
---

# SHOW LOAD DATA

The `SHOW LOAD DATA` statement displays LOAD DATA jobs created in the system. This statement can only display jobs created by the current user.

<CustomContent platform="tidb-cloud">

> **Note:**
>
> This feature is only available on [Serverless Tier clusters](/tidb-cloud/select-cluster-tier.md#serverless-tier-beta).

</CustomContent>

## Synopsis

```ebnf+diagram
ShowLoadDataJobsStmt ::=
    'SHOW' 'LOAD' 'DATA' 'JOBS'

ShowLoadDataJobStmt ::=
    'SHOW' 'LOAD' 'DATA' 'JOB' JobID
```

The meanings of the fields displayed by the `SHOW LOAD DATA` statement are as follows:

| Column Name      | Description                                                |
|------------------|------------------------------------------------------------|
| Job_ID           | The job ID                                                 |
| Create_Time      | The creation time of the task                              |
| Start_Time       | The start time of the task                                 |
| End_Time         | The end time of the task                                   |
| Data_Source      | The information of the data source                         |
| Target_Table     | The target table                                           |
| Import_Mode      | The import mode. Currently it can only be `logical`.       |
| Created_By       | The database username that created the task                |
| Job_State        | Indicates the current state of the task. For the `logical` mode task, it can only be `loading`. |
| Job_Status       | Indicates the status of the current task. The following statuses are available: <ul><li>`pending` indicates that the task has been created but not yet started running; </li><li>`running` indicates that it is running; </li><li>`canceled` indicates that the task has been canceled; </li><li>`failed` indicates that the task has failed and exited; </li><li>`finished` indicates that the task is completed. </li></ul>|
| Source_File_Size | Size of the source file                                     |
| Imported_Rows    | The number of rows that has been read and written to the target table        |
| Result_Code      | When the task status is `finished`, it is `0`. When the task status is `failed`, it is the corresponding error code.  |
| Result_Message   | If the import succeeds, a summary message is returned. If the import fails, an error message is returned. |

## Examples

```sql
SHOW LOAD DATA JOBS;
```

```
+--------+----------------------------+----------------------------+---------------------+---------------------------+--------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
| Job_ID | Create_Time                | Start_Time                 | End_Time            | Data_Source               | Target_Table       | Import_Mode | Created_By | Job_State | Job_Status | Source_File_Size | Imported_Rows | Result_Code | Result_Message |
+--------+----------------------------+----------------------------+---------------------+---------------------------+-------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
|      1 | 2023-03-16 22:29:12.990576 | 2023-03-16 22:29:12.991951 | 0000-00-00 00:00:00 | s3://bucket-name/test.csv | `my_db`.`my_table` | logical     | root@%     | loading   | running    | 52.43MB          | 323339          |             |                |
+--------+----------------------------+----------------------------+---------------------+---------------------------+--------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
1 row in set (0.01 sec)
```

```sql
SHOW LOAD DATA JOB 1;
```

```
+--------+----------------------------+----------------------------+---------------------+---------------------------+--------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
| Job_ID | Create_Time                | Start_Time                 | End_Time            | Data_Source               | Target_Table       | Import_Mode | Created_By | Job_State | Job_Status | Source_File_Size | Imported_Rows | Result_Code | Result_Message |
+--------+----------------------------+----------------------------+---------------------+---------------------------+-------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
|      1 | 2023-03-16 22:29:12.990576 | 2023-03-16 22:29:12.991951 | 0000-00-00 00:00:00 | s3://bucket-name/test.csv | `my_db`.`my_table` | logical     | root@%     | loading   | running    | 52.43MB          | 323339          |             |                |
+--------+----------------------------+----------------------------+---------------------+---------------------------+--------------------+-------------+------------+-----------+------------+------------------+------------------+-------------+----------------+
1 row in set (0.01 sec)
```

## MySQL compatibility

This statement is an extension of TiDB to MySQL syntax.

## See also

* [`LOAD DATA`](/sql-statements/sql-statement-load-data.md)
* [`CANCEL LOAD DATA` and `DROP LOAD DATA`](/sql-statements/sql-statement-operate-load-data-job.md)
