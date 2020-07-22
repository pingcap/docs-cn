---
title: mysql Schema
summary: Learn about the TiDB system tables.
aliases: ['/docs/dev/system-tables/system-table-overview/','/docs/dev/reference/system-databases/mysql/','/tidb/dev/system-table-overview/']
---

# `mysql` Schema

The `mysql` schema contains TiDB system tables. The design is similar to the `mysql` schema in MySQL, where tables such as `mysql.user` can be edited directly. It also contains a number of tables which are extensions to MySQL.

## Grant system tables

These system tables contain grant information about user accounts and their privileges:

- `user`: user accounts, global privileges, and other non-privilege columns
- `db`: database-level privileges
- `tables_priv`: table-level privileges
- `columns_priv`: column-level privileges

## Server-side help system tables

Currently, the `help_topic` is NULL.

## Statistics system tables

- `stats_buckets`: the buckets of statistics
- `stats_histograms`: the histograms of statistics
- `stats_meta`: the meta information of tables, such as the total number of rows and updated rows

## GC worker system tables

- `gc_delete_range`: to record the data to be deleted

## Miscellaneous system tables

- `GLOBAL_VARIABLES`: global system variable table
- `tidb`: to record the version information when TiDB executes `bootstrap`
