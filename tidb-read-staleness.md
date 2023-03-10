---
title: Read Historical Data Using the `tidb_read_staleness` System Variable
summary: Learn how to read historical data using the `tidb_read_staleness` system variable.
---

# Read Historical Data Using the `tidb_read_staleness` System Variable

To support reading the historical data, in v5.4, TiDB introduces a new system variable `tidb_read_staleness`. This document describes how to read historical data through this system variable, including detailed operating procedures.

## Feature description

The `tidb_read_staleness` system variable is used to set the time range of historical data that TiDB can read in the current session. The data type of this variable is int type, and the scope of it is `SESSION`. After setting the value, TiDB selects a timestamp as new as possible from the range allowed by this variable, and all subsequent read operations are performed against this timestamp. For example, if the value of this variable is set to `-5`, on the condition that TiKV has the corresponding historical version's data, TiDB selects a timestamp as new as possible within a 5-second time range.

After enabling `tidb_read_staleness`, you still can perform the following operations:

- Insert, modify, delete data or perform DML operations in the current session. These statements are not affected by `tidb_read_staleness`.
- Start an interactive transaction in the current session. Queries within this transaction still read the latest data.

After reading the historical data, you can read the latest data in the following two ways:

- Start a new session.
- Set the value of the `tidb_read_staleness` variable to `""` using the `SET` statement.

> **Note:**
>
> To reduce the latency and improve the timeliness of the Stale Read data, you can modify the TiKV `advance-ts-interval` configuration item. See [Reduce Stale Read latency](/stale-read.md#reduce-stale-read-latency) for details.

## Usage examples

This section describes how to use `tidb_read_staleness` with examples.

1. Create a table, and insert a few rows of data into the table:

    {{< copyable "sql" >}}

    ```sql
    create table t (c int);
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    insert into t values (1), (2), (3);
    ```

    ```
    Query OK, 3 rows affected (0.00 sec)
    ```

2. Check out the data in the table:

    {{< copyable "sql" >}}

    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

3. Update the data in a row:

    {{< copyable "sql" >}}

    ```sql
    update t set c=22 where c=2;
    ```

    ```
    Query OK, 1 row affected (0.00 sec)
    ```

4. Confirm that the data has been updated:

    {{< copyable "sql" >}}

    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

5. Set the `tidb_read_staleness` system variable.

    The scope of this variable is `SESSION`. After setting its value, TiDB reads the latest version data before the time set by the value.

    The following setting indicates that TiDB selects a timestamp as new as possible within the time range from 5 seconds ago to now and uses it as the timestamp for reading historical data:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_read_staleness="-5";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    > **Note:**
    >
    >  - Use `@@` instead of `@` before `tidb_read_staleness`. `@@` means system variables, and `@` means user variables.
    >  - You need to set the historical time range (the value of `tidb_read_staleness`) according to the total time that you spent in step 3 and step 4. Otherwise, the latest data will be displayed in the query results, not the historical data. Therefore, you need to adjust this time range according to the time you spent on operations. For example, in this example, since the set time range is 5 seconds, you need to complete step 3 and step 4 within 5 seconds.

    The data read here is the data before the update, that is, the historical data:

    {{< copyable "sql" >}}

    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |    2 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```

6. After un-setting this variable as follows, TiDB can read the latest data:

    {{< copyable "sql" >}}

    ```sql
    set @@tidb_read_staleness="";
    ```

    ```
    Query OK, 0 rows affected (0.00 sec)
    ```

    {{< copyable "sql" >}}

    ```sql
    select * from t;
    ```

    ```
    +------+
    | c    |
    +------+
    |    1 |
    |   22 |
    |    3 |
    +------+
    3 rows in set (0.00 sec)
    ```