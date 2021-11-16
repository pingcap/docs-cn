---
title: Data Check in the Sharding Scenario
summary: Learn the data check in the sharding scenario.
aliases: ['/docs/dev/sync-diff-inspector/shard-diff/','/docs/dev/reference/tools/sync-diff-inspector/shard-diff/']
---

# Data Check in the Sharding Scenario

sync-diff-inspector supports data check in the sharding scenario. Assume that you use the [TiDB Data Migration](https://docs.pingcap.com/tidb-data-migration/stable/overview) tool to replicate data from multiple MySQL instances into TiDB, you can use sync-diff-inspector to check upstream and downstream data.

For scenarios where the number of upstream sharded tables is small and the naming rules of sharded tables do not have a pattern as shown below, you can use `Datasource config` to configure `table-0`, set corresponding `rules` and configure the tables that have the mapping relationship between the upstream and downstream databases. This configuration method requires setting all sharded tables.

![shard-table-replica-1](/media/shard-table-replica-1.png)

Below is a complete example of the sync-diff-inspector configuration.

``` toml
# Diff Configuration.

######################### Global config #########################

# The number of goroutines created to check data. The number of connections between upstream and downstream databases are slightly greater than this value
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables
export-fix-sql = true

# Only compares the table structure instead of the data
check-struct-only = false

######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule1"]

[data-sources.mysql2]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

    route-rules = ["rule2"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""

########################### Routes ###########################
[routes.rule1]
schema-pattern = "test"        # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "table-[1-2]"  # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test"         # The name of the schema in the target database
target-table = "table-0"       # The name of the target table

[routes.rule2]
schema-pattern = "test"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "table-3"    # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test"       # The name of the schema in the target database
target-table = "table-0"     # The name of the target table

######################### Task config #########################
[task]
    output-dir = "./output"

    source-instances = ["mysql1", "mysql2"]

    target-instance = ["tidb0"]

    # The tables of downstream databases to be compared. Each table needs to contain the schema name and the table name, separated by '.'
    target-check-tables = ["test.table-0"]
```

You can use `table-rules` for configuration when there are a large number of upstream sharded tables and the naming rules of all sharded tables have a pattern, as shown below:

![shard-table-replica-2](/media/shard-table-replica-2.png)

Below is a complete example of the sync-diff-inspector configuration.

```toml
# Diff Configuration.
######################### Global config #########################

# The number of goroutines created to check data. The number of connections between upstream and downstream databases are slightly greater than this value.
check-thread-count = 4

# If enabled, SQL statements is exported to fix inconsistent tables.
export-fix-sql = true

# Only compares the table structure instead of the data.
check-struct-only = false

######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

[data-sources.mysql2]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""

########################### Routes ###########################
[routes.rule1]
schema-pattern = "test"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "table-*"    # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test"       # The name of the schema in the target database
target-table = "table-0"     # The name of the target table

######################### Task config #########################
[task]
    output-dir = "./output"
    source-instances = ["mysql1", "mysql2"]

    target-instance = ["tidb0"]

    # The tables of downstream databases to be compared. Each table needs to contain the schema name and the table name, separated by '.'
    target-check-tables = ["test.table-0"]
```

## Note

If `test.table-0` exists in the upstream database, the downstream database also compares this table.