---
title: Reading Data from History Versions
category: advanced
---

# Reading Data From History Versions

This document describes how TiDB reads data from the history versions, how TiDB manages the data versions, as well as an example to show how to use the feature.

## Feature Description

TiDB implements a feature to read history data using the standard SQL interface directly without special clients or drivers. By using this feature, 
- Even when data is updated or removed, its history versions can be read using the SQL interface.
- Even if the table structure changes after the data is updated, TiDB can use the old structure to read the history data.

## How TiDB Reads Data From History Versions

The `tidb_snapshot` system variable is introduced to support reading history data. About the `tidb_snapshot` variable:

- The variable is valid in the `Session` scope.
- Its value can be modified using the `Set` statement. 
- The data type for the variable is text. 
- The variable is to record time in the following format: “2016-10-08 16:45:26.999”. Generally, the time can be set to seconds like in “2016-10-08 16:45:26”. 
- When the variable is set, TiDB creates a Snapshot using its value as the timestamp, just for the data structure and there is no any overhead. After that, all the `Select` operations will read data from this Snapshot.

> **Note:** Because the timestamp in TiDB transactions is allocated by Placement Driver (PD), the version of the stored data is also marked based on the timestamp allocated by PD. When a Snapshot is created, the version number is based on the value of the `tidb_snapshot` variable. If there is a large difference between the local time of the TiDB server and the PD server, use the time of the PD server.

After reading data from history versions, you can read data from the latest version by ending the current Session or using the `Set` statement to set the value of the `tidb_snapshot` variable to "" (empty string). 

## How TiDB Manages the Data Versions

TiDB implements Multi-Version Concurrency Control (MVCC) to manage data versions. The history versions of data are kept because each update / removal creates a new version of the data object instead of updating / removing the data object in-place. But not all the versions are kept. If the versions are older than a specific time, they will be removed completely to reduce the storage occupancy and the performance overhead caused by too many history versions.

In TiDB, Garbage Collection (GC) runs periodically to remove the obsolete data versions. GC is triggered in the following way: There is a `gc_worker` goroutine running in the background of each TiDB server. In a cluster with multiple TiDB servers, one of the `gc_worker` goroutines will be automatically selected to be the leader. The leader is responsible for maintaining the GC state and sends GC commands to each TiKV region leader.

The running record of GC is recorded in the system table of `mysql.tidb` as follows and can be monitored and configured using the SQL statements：

```
mysql> select variable_name, variable_value from mysql.tidb;
+-----------------------+----------------------------+
| variable_name         | variable_value             |
+-----------------------+----------------------------+
| bootstrapped          | True                       |
| tikv_gc_leader_uuid   | 55daa0dfc9c0006            |
| tikv_gc_leader_desc   | host:pingcap-pc5 pid:10549 |
| tikv_gc_leader_lease  | 20160927-13:18:28 +0800 CST|
| tikv_gc_run_interval  | 10m0s                      |
| tikv_gc_life_time     | 10m0s                      |
| tikv_gc_last_run_time | 20160927-13:13:28 +0800 CST|
| tikv_gc_safe_point    | 20160927-13:03:28 +0800 CST|
+-----------------------+----------------------------+
7 rows in set (0.00 sec)
```

Pay special attention to the following two rows:

- `tikv_gc_life_time`: This row is to configure the retention time of the history version and its default value is 10m. You can use SQL statements to configure it. For example, if you want all the data within one day to be readable, set this row to 24h by using the `update mysql.tidb set variable_value='24h' where variable_name='tikv_gc_life_time'` statement. The format is: "24h", "2h30m", "2.5h". The unit of time can be: "h", "m", "s".

> **Note:** If your data is updated very frequently, the following issues might occur if the value of the `tikv_gc_life_time` is set to be too large like in days or months:
> 
>  - The more versions of the data, the more disk storage is occupied.
>  - A large amount of the history versions might slow down the query, especially the range queries like `select count(*) from t`.
>  - If the value of the `tikv_gc_life_time` variable is suddenly changed to be smaller while the database is running, it might lead to the removal of large amounts of history data and cause huge I/O burden.
>  - `tikv_gc_safe_point`: This row records the current safePoint. You can safely create the Snapshot to read the history data using the timestamp that is later than the safePoint. The safePoint automatically updates every time GC runs.

## Example

1. At the initial stage, create a table and insert several rows of data:

  ```sql
  mysql> create table t (c int);
  Query OK, 0 rows affected (0.01 sec)
  
  mysql> insert into t values (1), (2), (3);
  Query OK, 3 rows affected (0.00 sec)
  ```

2. View the data in the table:
  
  ```sql
  mysql> select * from t;
  +------+
  | c    |
  +------+
  |    1 |
  |    2 |
  |    3 |
  +------+
  3 rows in set (0.00 sec)
  ```

3. View the timestamp of the table:
  
  ```sql
  mysql> select now();
  +---------------------+
  | now()               |
  +---------------------+
  | 2016-10-08 16:45:26 |
  +---------------------+
  1 row in set (0.00 sec)
  ```

4. Update the data in one row:

  ```sql
  mysql> update t set c=22 where c=2;
  Query OK, 1 row affected (0.00 sec)
  ```

5. Make sure the data is updated:

  ```sql
  mysql> select * from t;
  +------+
  | c    |
  +------+
  |    1 |
  |   22 |
  |    3 |
  +------+
  3 rows in set (0.00 sec)
  ```

6. Set the `tidb_snapshot` variable whose scope is Session. The variable is set so that the latest version before the value can be read. 

  > **Note:** In this example, the value is set to be the time before the update operation.
  
  ```sql
  mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
  Query OK, 0 rows affected (0.00 sec)
  ```
  **Result:** The read from the following statement is the data before the update operation, which is the history data.

  ```sql
  mysql> select * from t;
  +------+
  | c    |
  +------+
  |    1 |
  |    2 |
  |    3 |
  +------+
  3 rows in set (0.00 sec)
  ```

7. Set the  `tidb_snapshot` variable to be "" (empty string) and you can read the data from the latest version:
  
  ```sql
  mysql> set @@tidb_snapshot="";
  Query OK, 0 rows affected (0.00 sec)
  ```
  ```sql
  mysql> select * from t;
  +------+
  | c    |
  +------+
  |    1 |
  |   22 |
  |    3 |
  +------+
  3 rows in set (0.00 sec)
  ```