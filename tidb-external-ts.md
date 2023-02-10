---
title: Read Historical Data Using the `tidb_external_ts` Variable
summary: Learn how to read historical data using the `tidb_external_ts` variable.
---

# Read Historical Data Using the `tidb_external_ts` Variable

To support reading the historical data, TiDB v6.4.0 introduces a system variable [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640). This document describes how to read historical data through this system variable, including detailed usage examples.

## Scenarios

Read historical data from a specified point in time is very useful for data replication tools such as TiCDC. After the data replication tool completes the data replication before a certain point in time, you can set the `tidb_external_ts` system variable of the downstream TiDB to read the data before that point in time. This prevents the data inconsistency caused by data replication.

## Feature description

The system variable [`tidb_external_ts`](/system-variables.md#tidb_external_ts-new-in-v640) specifies the timestamp of the historical data to be read when `tidb_enable_external_ts_read` is enabled.

The system variable [`tidb_enable_external_ts_read`](/system-variables.md#tidb_enable_external_ts_read-new-in-v640) controls whether to read historical data in the current session or globally. The default value is `OFF`, which means the feature of reading historical data is disabled, and the `tidb_external_ts` value is ignored. When `tidb_enable_external_ts_read` is set to `ON` globally, all queries read historical data before the time specified by `tidb_external_ts`. If `tidb_enable_external_ts_read` is set to `ON` only for a certain session, only queries in that session read historical data.

When the `tidb_enable_external_ts_read` is enabled, TiDB becomes read-only. All write queries will fail with an error like `ERROR 1836 (HY000): Running in read-only mode`.

## Usage examples

This section describes how to use the `tidb_external_ts` variable to read historical data with examples.

1. Create a table and insert some rows into the table:

    ```sql
    CREATE TABLE t (c INT);
    ```

    ```
    Query OK, 0 rows affected (0.01 sec)
    ```

    ```sql
    INSERT INTO t VALUES (1), (2), (3);
    ```

    ```
    Query OK, 3 rows affected (0.00 sec)
    ```

2. View the data in the table:

    ```sql
    SELECT * FROM t;
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

3. Set `tidb_external_ts` to `@@tidb_current_ts`:

    ```sql
    START TRANSACTION;
    SET GLOBAL tidb_external_ts=@@tidb_current_ts;
    COMMIT;
    ```

4. Insert a new row and confirm that it is inserted:

    ```sql
    INSERT INTO t VALUES (4);
    ```

    ```
    Query OK, 1 row affected (0.001 sec)
    ```

    ```sql
    SELECT * FROM t;
    ```

    ```
    +------+
    | id   |
    +------+
    |    1 |
    |    2 |
    |    3 |
    |    4 |
    +------+
    4 rows in set (0.00 sec)
    ```

5. Set `tidb_enable_external_ts_read` to `ON` and then view data in the table:

    ```sql
    SET tidb_enable_external_ts_read=ON;
    SELECT * FROM t;
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

    Because `tidb_external_ts` is set to the timestamp before the new row is inserted, the newly inserted row is not returned after the `tidb_enable_external_ts_read` is enabled.
