---
title: Filter DMLs Using SQL Expressions
aliases: ['/tidb/dev/feature-expression-filter/']
summary: In incremental data migration, you can filter binlog events using SQL expressions. DM supports filtering data during migration using binlog value filter since v2.0.5. You can configure SQL expressions based on the values in binlog events to determine whether to migrate a row change downstream. For detailed operation and implementation, refer to "Filter DML Events Using SQL Expressions".
---

# Filter DMLs Using SQL Expressions

## Overview

In the process of incremental data migration, you can filter certain types of binlog events using the [Filter Binlog Events](/filter-binlog-event.md) feature. For example, for archiving or auditing purposes, you can filter out `DELETE` events when migrating data to the downstream. However, Binlog Event Filter cannot judge with a greater granularity on whether to filter out a specific row of `DELETE` events.

To solve the above issue, DM supports filtering data during incremental migration using `binlog value filter` since v2.0.5. The binlog in the `ROW` format supported by DM has the values of all columns in binlog events. You can configure SQL expressions according to these values. If the SQL expressions evaluate a row change as `TRUE`, DM will not migrate the row change downstream.

For detailed operation and implementation, see [Filter DML Events Using SQL Expressions](/filter-dml-event.md).