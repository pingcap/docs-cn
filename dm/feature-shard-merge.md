---
title: Merge and Migrate Data from Sharded Tables
summary: Learn how DM merges and migrates data from sharded tables.
aliases: ['/docs/tidb-data-migration/dev/feature-shard-merge/']
---

# Merge and Migrate Data from Sharded Tables

This document introduces the sharding support feature provided by Data Migration (DM). This feature allows you to merge and migrate the data of tables with the same or different table schemas in the upstream MySQL or MariaDB instances into one same table in the downstream TiDB. It supports not only migrating the upstream DML statements, but also coordinating to migrate the table schema change using DDL statements in multiple upstream sharded tables.

## Overview

DM supports merging and migrating the data of multiple upstream sharded tables into one table in TiDB. During the migration, the DDL of each sharded table, and the DML before and after the DDL need to be coordinated. For the usage scenarios, DM supports two different modes: pessimistic mode and optimistic mode.

> **Note:**
>
> - To merge and migrate data from sharded tables, you must set `shard-mode` in the task configuration file.
> - DM uses the pessimistic mode by default for the merge of the sharding support feature. (If there is no special description in the document, use the pessimistic mode by default.)
> - It is not recommended to use this mode if you do not understand the principles and restrictions of the optimistic mode. Otherwise, it may cause serious consequences such as migration interruption and even data inconsistency.

### The pessimistic mode

When an upstream sharded table executes a DDL statement, the migration of this sharded table will be suspended. After all other sharded tables execute the same DDL, the DDL will be executed in the downstream and the data migration task will restart. The advantage of this mode is that it can ensure that the data migrated to the downstream will not go wrong. For details, refer to [shard merge in pessimistic mode](/dm/feature-shard-merge-pessimistic.md).
 
### The optimistic mode

DM will automatically modify the DDL executed on a sharded table into a statement compatible with other sharded tables, and then migrate to the downstream. This will not block the DML migration of any sharded tables. The advantage of this mode is that it will not block data migration when processing DDL. However, improper use will cause migration interruption or even data inconsistency. For details, refer to [shard merge in optimistic mode](/dm/feature-shard-merge-optimistic.md).

### Contrast

| Pessimistic mode   | Optimistic mode   |
| :----------- | :----------- |
| Sharded tables that executes DDL suspend DML migration | Sharded tables that executes DDL continue DML migration |
| The DDL execution order and statements of each sharded table must be the same | Each sharded table only needs to keep the table schema compatible with each other  |
| The DDL is migrated to the downstream after the entire shard group is consistent | The DDL of each sharded table immediately affects the downstream |
| Wrong DDL operations can be intercepted after the detection | Wrong DDL operations will be migrated to the downstream, which may cause inconsistency between the upstream and downstream data before the detection  |