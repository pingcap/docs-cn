---
title: Data Check for Tables with Different Schema or Table Names
summary: Learn the data check for different database names or table names.
category: tools
---

# Data Check for Tables with Different Schema or Table Names

When using replication tools such as TiDB Data Migration, you can set `route-rules` to replicate data to a specified table in the downstream. sync-diff-inspector enables you to verify tables with different schema names or table names.

Below is a simple example.

```toml
######################### Tables config #########################

# Configure the tables of the target database that need to be checked
[[check-tables]]
    # The name of the schema in the target database
    schema = "test_2"

    # The table that needs to be checked
    tables = ["t_2"]

# Configuration example of comparing two tables with different schema names and table names
[[table-config]]
    # The name of the schema in the target database
    schema = "test_2"

    # The name of the target table
    table = "t_2"

    # Configuration of the source data
    [[table-config.source-tables]]
        # The instance ID of the source schema
        instance-id = "source-1"
        # The name of the source schema
        schema = "test_1"
        # The name of the source table
        table  = "t_1"
```

This configuration can be used to check `test_2.t_2` in the downstream and `test_1.t_1` in the `source-1` instance.

To check a large number of tables with different schema names or table names, you can simplify the configuration by setting the mapping relationship by using `table-rule`. You can configure the mapping relationship of either schema or table, or of both. For example, all the tables in the upstream `test_1` database are replicated to the downstream `test_2` database, which can be checked through the following configuration:

```toml
######################### Tables config #########################

# Configures the tables of the target database that need to be checked
[[check-tables]]
    # The name of the schema in the target database
    schema = "test_2"

    # Check all the tables
    tables = ["~^"]

[[table-rules]]
    # schema-pattern and table-pattern support the wildcards "*" and "?"
    schema-pattern = "test_1"
    #table-pattern = ""
    target-schema = "test_2"
    #target-table = ""
```
