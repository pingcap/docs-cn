---
title: Data Check in the DM Replication Scenario
summary: Learn about how to set a specific `task-name` configuration from `DM-master` to perform a data check.
---

# Data Check in the DM Replication Scenario

When using replication tools such as [TiDB Data Migration](https://docs.pingcap.com/tidb-data-migration/stable/overview), you need to check the data consistency before and after the replication process. You can set a specific `task-name` configuration from `DM-master` to perform a data check.

The following is a simple configuration example. To learn the complete configuration, refer to [Sync-diff-inspector User Guide](/sync-diff-inspector/sync-diff-inspector-overview.md).

```toml
# Diff Configuration.

######################### Global config #########################

# The number of goroutines created to check data. The number of connections between upstream and downstream databases are slightly greater than this value.
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables.
export-fix-sql = true

# Only compares the table structure instead of the data.
check-struct-only = false

# The IP address of dm-master and the format is "http://127.0.0.1:8261".
dm-addr = "http://127.0.0.1:8261"

# Specifies the `task-name` of DM.
dm-task = "test"

######################### Task config #########################
[task]
    output-dir = "./output"

    # The tables of downstream databases to be compared. Each table needs to contain the schema name and the table name, separated by '.'
    target-check-tables = ["hb_test.*"]
```

This example is configured in dm-task = "test", which checks all the tables of hb_test schema under the "test" task. It automatically gets the regular matching of the schemas between upstream and downstream databases to verify the data consistency after DM replication.