---
title: Read Historical Data
summary: Learn about how TiDB reads data from history versions.
category: how-to
aliases: ['/docs/op-guide/history-read/']
---

# Read Historical Data

This document describes how TiDB reads data from the history versions, how TiDB manages the data versions, as well as an example to show how to use the feature.

## Feature description

TiDB implements a feature to read history data using the standard SQL interface directly without special clients or drivers. By using this feature:

- Even when data is updated or removed, its history versions can be read using the SQL interface.
- Even if the table structure changes after the data is updated, TiDB can use the old structure to read the history data.

## How TiDB reads data from history versions

The `tidb_snapshot` system variable is introduced to support reading history data. About the `tidb_snapshot` variable:

- The variable is valid in the `Session` scope.
- Its value can be modified using the `Set` statement.
- The data type for the variable is text.
- The variable accepts TSO (Timestamp Oracle) and datetime. TSO is a globally unique time service, which is obtained from PD. The acceptable datetime format is "2016-10-08 16:45:26.999". Generally, the datetime can be set using second precision, for example "2016-10-08 16:45:26".
- When the variable is set, TiDB creates a Snapshot using its value as the timestamp, just for the data structure and there is no any overhead. After that, all the `Select` operations will read data from this Snapshot.

> **Note:**
>
> Because the timestamp in TiDB transactions is allocated by Placement Driver (PD), the version of the stored data is also marked based on the timestamp allocated by PD. When a Snapshot is created, the version number is based on the value of the `tidb_snapshot` variable. If there is a large difference between the local time of the TiDB server and the PD server, use the time of the PD server.

After reading data from history versions, you can read data from the latest version by ending the current Session or using the `Set` statement to set the value of the `tidb_snapshot` variable to "" (empty string).

## How TiDB manages the data versions

TiDB implements Multi-Version Concurrency Control (MVCC) to manage data versions. The history versions of data are kept because each update/removal creates a new version of the data object instead of updating/removing the data object in-place. But not all the versions are kept. If the versions are older than a specific time, they will be removed completely to reduce the storage occupancy and the performance overhead caused by too many history versions.

In TiDB, Garbage Collection (GC) runs periodically to remove the obsolete data versions. For GC details, see [TiDB Garbage Collection (GC)](/reference/garbage-collection.md)

Pay special attention to the following two variables:

- `tikv_gc_life_time`: It is used to configure the retention time of the history version. You can modify it manually.
- `tikv_gc_safe_point`: It records the current `safePoint`. You can safely create the snapshot to read the history data using the timestamp that is later than `safePoint`. `safePoint` automatically updates every time GC runs.

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

    > **Note:**
    >
    > In this example, the value is set to be the time before the update operation.

    ```sql
    mysql> set @@tidb_snapshot="2016-10-08 16:45:26";
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **Note:**
    >
    > You should use `@@` instead of `@` before `tidb_snapshot` because `@@` is used to denote the system variable while `@` is used to denote the user variable.

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

    > **Note:**
    >
    > You should use `@@` instead of `@` before `tidb_snapshot` because `@@` is used to denote the system variable while `@` is used to denote the user variable.
