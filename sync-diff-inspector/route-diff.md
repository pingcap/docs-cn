---
title: Data Check for Tables with Different Schema or Table Names
summary: Learn the data check for different database names or table names.
aliases: ['/docs/dev/sync-diff-inspector/route-diff/','/docs/dev/reference/tools/sync-diff-inspector/route-diff/']
---

# Data Check for Tables with Different Schema or Table Names

When using replication tools such as [TiDB Data Migration](https://docs.pingcap.com/tidb-data-migration/stable/overview), you can set `route-rules` to replicate data to a specified table in the downstream. sync-diff-inspector enables you to verify tables with different schema names or table names by setting `rules`.

The following is a simple configuration example. To learn the complete configuration, refer to [Sync-diff-inspector User Guide](/sync-diff-inspector/sync-diff-inspector-overview.md).

```toml
######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    route-rules = ["rule1"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
########################### Routes ###########################
[routes.rule1]
schema-pattern = "test_1"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "t_1"          # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test_2"       # The name of the schema in the target database
target-table = "t_2"           # The name of the target table
```

This configuration can be used to check `test_2.t_2` in the downstream and `test_1.t_1` in the `mysql1` instance.

To check a large number of tables with different schema names or table names, you can simplify the configuration by setting the mapping relationship by using `rules`. You can configure the mapping relationship of either schema or table, or of both. For example, all the tables in the upstream `test_1` database are replicated to the downstream `test_2` database, which can be checked through the following configuration:

```toml
######################### Datasource config #########################
[data-sources.mysql1]
    host = "127.0.0.1"
    port = 3306
    user = "root"
    password = ""
    route-rules = ["rule1"]

[data-sources.tidb0]
    host = "127.0.0.1"
    port = 4000
    user = "root"
    password = ""
########################### Routes ###########################
[routes.rule1]
schema-pattern = "test_1"      # Matches the schema name of the data source. Supports the wildcards "*" and "?"
table-pattern = "*"            # Matches the table name of the data source. Supports the wildcards "*" and "?"
target-schema = "test_2"       # The name of the schema in the target database
target-table = "t_2"           # The name of the target table
```

## Note

If `test_2`.`t_2` exists in the upstream database, the downstream database also compares this table.