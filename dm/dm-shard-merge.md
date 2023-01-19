---
title: TiDB Data Migration Shard Merge
summary: Learn the shard merge feature of DM.
---

# TiDB Data Migration Shard Merge

TiDB Data Migration (DM) supports merging the DML and DDL data in the upstream MySQL/MariaDB sharded tables and migrating the merged data to the downstream TiDB tables.

If you need to migrate and merge MySQL shards of small datasets to TiDB, refer to [this tutorial](/migrate-small-mysql-shards-to-tidb.md).

## Restrictions

Currently, the shard merge feature is supported only in limited scenarios. For details, refer to [Sharding DDL usage Restrictions in the pessimistic mode](/dm/feature-shard-merge-pessimistic.md#restrictions) and [Sharding DDL usage Restrictions in the optimistic mode](/dm/feature-shard-merge-optimistic.md#restrictions).

## Configure parameters

In the task configuration file, set `shard-mode` to `pessimistic`:

```yaml
shard-mode: "pessimistic"
# The shard merge mode. Optional modes are ""/"pessimistic"/"optimistic". The "" mode is used by default
# which means sharding DDL merge is disabled. If the task is a shard merge task, set it to the "pessimistic"
# mode. After getting a deep understanding of the principles and restrictions of the "optimistic" mode, you
# can set it to the "optimistic" mode.
```

## Handle sharding DDL locks manually

In some abnormal scenarios, you need to [handle sharding DDL Locks manually](/dm/manually-handling-sharding-ddl-locks.md).
