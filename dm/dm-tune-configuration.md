---
title: Optimize Configuration of DM
summary: Learn how to optimize the configuration of the data migration task to improve the performance of data migration.
---

# Optimize Configuration of DM

This document introduces how to optimize the configuration of the data migration task to improve the performance of data migration.

## Full data export

`mydumpers` is the configuration item related to full data export. This section describes how to configure performance-related options.

### `rows`

Setting the `rows` option enables concurrently exporting data from a single table using multi-thread. The value of `rows` is the maximum number of rows contained in each exported chunk. After this option is enabled, DM selects a column as the split benchmark when the data of a MySQL single table is concurrently exported. This column can be one of the following columns: the primary key column, the unique index column, and the normal index column (ordered from highest priority to lowest). Make sure this column is of integer type (for example, `INT`, `MEDIUMINT`, `BIGINT`).

The value of `rows` can be set to 10000. You can change this value according to the total number of rows in the table and the performance of the database. In addition, you need to set `threads` to control the number of concurrent threads. By default, the value of `threads` is 4. You can adjust this value as needed.

### `chunk-filesize`

During full backup, DM splits the data of each table into multiple chunks according to the value of the `chunk-filesize` option. Each chunk is saved in a file with a size of about `chunk-filesize`. In this way, data is split into multiple files and you can use the parallel processing of the DM Load unit to improve the import speed. The default value of this option is 64 (in MB). Normally, you do not need to set this option. If you set it, adjust the value of this option according to the size of the full data.

> **Note:**
>
> - You cannot update the value of `mydumpers` after the migration task is created. Be sure about the value of each option before creating the task. If you need to update the value, stop the task using dmctl, update the configuration file, and re-create the task.
> - `mydumpers`.`threads` can be replaced with the `mydumper-thread` configuration item for simplicity.
> - If `rows` is set, DM ignores the value of `chunk-filesize`.

## Full data import

`loaders` is the configuration item related to full data import. This section describes how to configure performance-related options.

### `pool-size`

The `pool-size` option determines the number of threads in the DM Load unit. The default value is 16. Normally, you do not need to set this option. If you set it, adjust the value of this option according to the size of the full data and the performance of the database.

> **Note:**
>
> - You cannot update the value of `loaders` after the migration task is created. Be sure about the value of each option before creating the task. If you need to update the value, stop the task using dmctl, update the configuration file, and re-create the task.
> - `loaders`.`pool-size` can be replaced with the `loader-thread` configuration item for simplicity.

## Incremental data replication

`syncers` is the configuration item related to incremental data replication. This section describes how to configure performance-related options.

### `worker-count`

`worker-count` determines the number of threads for concurrent replication of DMLs in the DM Sync unit. The default value is 16. To speed up data replication, increase the value of this option appropriately.

### `batch`

`batch` determines the number of DMLs included in each transaction when the data is replicated to the downstream database during the DM Sync unit. The default value is 100. Normally, you do not need to change the value of this option.

> **Note:**
>
> - You cannot update the value of `syncers` after the replication task is created. Be sure about the value of each option before creating the task. If you need to update the value, stop the task using dmctl, update the configuration file, and re-create the task.
> - `syncers`.`worker-count` can be replaced with the `syncer-thread` configuration item for simplicity.
> - You can change the values of `worker-count` and `batch` according to the actual scenario. For example, if there is a high network delay between DM and the downstream database, you can increase the value of `worker-count` and decrease the value of `batch` appropriately.
