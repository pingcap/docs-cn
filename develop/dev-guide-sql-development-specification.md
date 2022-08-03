---
title: SQL Development Specifications
summary: Learn about the SQL development specifications for TiDB.
---

# SQL Development Specifications

This document introduces some general development specifications for using SQL.

## Create and delete tables

- Basic principle: under the premise of following the table naming convention, it is recommended that the application internally packages the table creation and deletion statements and adds judgment logic to prevent abnormal interruption of business processes.
- Details: `create table if not exists table_name` or `drop table if exists table_name` statements are recommended to add `if` judgments to avoid abnormal interruptions caused by SQL commands running abnormally on the application side.

## `SELECT *` usage

- Basic principle: avoid using `SELECT *` for queries.
- Details: select the appropriate columns as required and avoid using `SELECT *` to read all fields because such operations consume network bandwidth. Consider adding the queried fields to the index to make effective use of the covering index.

## Use functions on fields

- Basic principle: You can use related functions on the queried fields. To avoid index failure, do not use any functions on the filtered fields in the `WHERE` clause, including data type conversion functions. You may consider using the expression index.
- Detailed description:

    NOT recommended:

    {{< copyable "sql" >}}

    ```sql
    SELECT gmt_create
    FROM ...
    WHERE DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s') = '20090101 00:00:00'
    ```

    Recommended:

    {{< copyable "sql" >}}

    ```sql
    SELECT DATE_FORMAT(gmt_create, '%Y%m%d %H:%i:%s')
    FROM ...
    WHERE gmt_create = str_to_date('20090101 00:00:00', '%Y%m%d %H:%i:%s')
    ```

## Other specifications

- Do not perform mathematical operations or functions on the index column in the `WHERE` condition.
- Replace `OR` with `IN` or `UNION`. The number of `IN` must be less than `300`.
- Avoid using the `%` prefix for fuzzy prefix queries.
- If the application uses **Multi Statements** to execute SQL, that is, multiple SQLs are joined with semicolons and sent to the client for execution at once, TiDB only returns the result of the first SQL execution.
- When you use expressions, check if the expressions support computing push-down to the storage layer (TiKV or TiFlash). If not, you should expect more memory consumption and even OOM at the TiDB layer. Computing that can be pushe down the storage layer is as follows:
    - [TiFlash supported push-down calculations](/tiflash/tiflash-supported-pushdown-calculations.md).
    - [TiKV - List of Expressions for Pushdown](/functions-and-operators/expressions-pushed-down.md).
    - [Predicate push down](/predicate-push-down.md).
