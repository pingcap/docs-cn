---
title: TiDB Lightning Prechecks
summary: This document describes the checks that TiDB Lightning performs before performing a data migration task. These precheckes ensure that TiDB Lightning can perform the task smoothly.
---

# TiDB Lightning Prechecks

Starting from TiDB 5.3.0, TiDB Lightning provides the ability to check the configuration before running a migration task. It is enabled by default. This feature automatically performs some routine checks for disk space and execution configuration. The main purpose is to ensure that the whole subsequent import process goes smoothly.

The following table describes each check item and detailed explanation.

|  Check Items | Description |
|  ----  | ----  |
| Cluster version and status| Check whether the cluster can be connected in the configuration, and whether the TiKV/PD/TiFlash version supports the Local import mode when the backend mode is Local. |
| Disk space | Check whether there is enough space on the local disk and on the TiKV cluster for importing data. TiDB Lightning samples the data sources and estimates the percentage of the index size from the sample result. Because indexes are included in the estimation, there may be cases where the size of the source data is less than the available space on the local disk, but still the check fails. When the backend is Local, it also checks whether the local storage is sufficient because external sorting needs to be done locally. | 
| Region distribution status | Check whether the regions in the TiKV cluster are distributed evenly and whether there are too many empty regions. If the number of empty regions exceeds max(1000, number of tables * 3), i.e. greater than the bigger one of "1000" or "3 times the number of tables ", then the import cannot be executed. |
| Exceedingly Large CSV files in the data file | When there are CSV files larger than 10 GiB in the backup file and auto-slicing is not enabled (StrictFormat=false), it will impact the import performance. The purpose of this check is to remind you to ensure the data is in the right format and to enable auto-slicing. |
| Recovery from breakpoints | This check ensures that no changes are made to the source file or schema in the database during the breakpoint recovery process that would result in importing the wrong data. |
| Import into an existing table | When importing into an already created table, it checks, as much as possible, whether the source file matches the existing table. Check if the number of columns matches. If the source file has column names, check if the column names match. When there are default columns in the source file, it checks if the default columns have Default Value, and if they have, the check passes. ｜