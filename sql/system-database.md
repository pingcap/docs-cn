---
title: The TiDB System Database
summary: Learn tables contained in the TiDB System Database.
category: user guide
---

# The TiDB System Database

The TiDB System Database is similar to MySQL, which contains tables that store information required by the server when it runs.

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
