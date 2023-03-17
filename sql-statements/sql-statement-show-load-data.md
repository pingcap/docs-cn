---
title: SHOW LOAD DATA
summary: TiDB 数据库中 SHOW LOAD DATA 的使用概况。
---

# SHOW LOAD DATA

`SHOW LOAD DATA` 语句用于显示系统中创建的 LOAD DATA JOB。该语句只能显示由当前用户创建的 job。

## 语法图

```ebnf+diagram
ShowLoadDataJobsStmt ::=
    'SHOW' 'LAOD' 'DATA' 'JOBS'

ShowLoadDataJobStmt ::=
    'SHOW' 'LAOD' 'DATA' 'JOB' JobID
```

`SHOW LOAD DATA` 语句显示的字段含义如下:

| 列名 | 说明            |
| -------- | ------------- |
|Job_ID |任务 ID|
|Create_Time |任务创建时间|
|Start_Time |任务启动时间|
|End_Time |任务结束时间|
|Data_Source |数据源信息|
|Target_Table |目标表|
|Import_Mode |导入模式，目前该字段只能取值 `logical`|
|Created_By |创建该任务的数据库用户名|
|Job_State |表示任务当前所处的步骤，对于 `logical` 模式的任务，只有 `loading` 这一个步骤|
|Job_Status |表示当前任务的状态。有以下几种状态：`running`，表示运行中；`canceled`，表示已经取消的任务；`failed`，表示任务失败并退出；`finished`，表示任务已完成。|
|Source_File_Size |源文件大小|
|Loaded_File_Size |已经读到并写入目标表的数据量大小|
|Result_Code |任务状态为 `finished` 时为 0，`failed` 时为对应的错误码|
|Result_Message |具体错误信息|

## 示例

{{< copyable "sql" >}}

```sql
SHOW LOAD DATA JOBS\G;
```

```
*************************** 1. row ***************************
          Job_ID: 1
     Create_Time: 2023-03-17 15:16:08.352125
      Start_Time: 2023-03-17 15:16:08.355728
        End_Time: 2023-03-17 15:16:08.363810
     Data_Source: s3://mybucket/small.csv
    Target_Table: `test`.`t`
     Import_Mode: logical
      Created_By: root@%
       Job_State: loading
      Job_Status: finished
Source_File_Size: 17B
Loaded_File_Size: 17B
     Result_Code: 0
  Result_Message: Records: 2  Deleted: 0  Skipped: 0  Warnings: 0
*************************** 2. row ***************************
          Job_ID: 30002
     Create_Time: 2023-03-17 15:24:35.839165
      Start_Time: 2023-03-17 15:24:35.841178
        End_Time: 2023-03-17 15:16:08.363810
     Data_Source: s3://mybucket/small.csv
    Target_Table: `test`.`t`
     Import_Mode: logical
      Created_By: root@%
       Job_State: loading
      Job_Status: running
Source_File_Size: NULL
Loaded_File_Size: NULL
     Result_Code: 0
  Result_Message:
2 rows in set (0.00 sec)
```

{{< copyable "sql" >}}

```sql
SHOW LOAD DATA JOB 1\G;
```

```
*************************** 1. row ***************************
          Job_ID: 1
     Create_Time: 2023-03-17 15:16:08.352125
      Start_Time: 2023-03-17 15:16:08.355728
        End_Time: 2023-03-17 15:16:08.363810
     Data_Source: s3://mybucket/small.csv
    Target_Table: `test`.`t`
     Import_Mode: logical
      Created_By: root@%
       Job_State: loading
      Job_Status: finished
Source_File_Size: 17B
Loaded_File_Size: 17B
     Result_Code: 0
  Result_Message: Records: 2  Deleted: 0  Skipped: 0  Warnings: 0
1 row in set (0.01 sec)
```

## MySQL 兼容性

该语句是 TiDB 对 MySQL 语法的扩展。

## 另请参阅

* [LOAD DATA](/sql-statements/sql-statement-load-data.md)
* [OPERATE LOAD DATA JOB](/sql-statements/sql-statement-operate-load-data-job.md)
