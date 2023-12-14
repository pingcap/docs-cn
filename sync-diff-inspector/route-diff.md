---
title: Data Check for Tables with Different Schema or Table Names
summary: Learn the data check for different database names or table names.
aliases: ['/docs/dev/sync-diff-inspector/route-diff/','/docs/dev/reference/tools/sync-diff-inspector/route-diff/']
---

# Data Check for Tables with Different Schema or Table Names

When using replication tools such as [TiDB Data Migration](/dm/dm-overview.md), you can set `route-rules` to replicate data to a specified table in the downstream. sync-diff-inspector enables you to verify tables with different schema names or table names by setting `rules`.

The following is a simple configuration example. To learn the complete configuration, refer to [sync-diff-inspector User Guide](/sync-diff-inspector/sync-diff-inspector-overview.md).

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

## The initialization of table routers and some examples

### The initialization of table routers

- If a `target-schema/target-table` table named `schema.table` exists in the rules, the behavior of sync-diff-inspector is as follows:

    - If there is a rule that matches `schema.table` to `schema.table`, sync-diff-inspector does nothing.
    - If there is no rule that matches `schema.table` to `schema.table`, sync-diff-inspector will add a new rule `schema.table -> _no__exists__db_._no__exists__table_` to the table router. After that, sync-diff-inspector will treat the table `schema.table` as the table `_no__exists__db_._no__exists__table_`.

- If `target-schema` exists only in the rules as follows:

    ```toml
    [routes.rule1]
    schema-pattern = "schema_2"  # the schema to match. Support wildcard characters * and ?
    target-schema = "schema"     # the target schema
    ```

    - If there is no schema `schema` in the upstream, sync-diff-inspector does nothing.
    - If there is a schema `schema` in the upstream, and a rule matches the schema, sync-diff-inspector does nothing.
    - If there is a schema `schema` in the upstream, but no rule matches the schema, sync-diff-inspector will add a new rule `schema -> _no__exists__db_` to the table router. After that, sync-diff-inspector will treat the table `schema` as the table `_no__exists__db_`.

- If `target-schema.target-table` does not exist in the rules, sync-diff-inspector will add a rule to match `target-schema.target-table` to `target-schema.target-table` to make it case-insensitive, because the table router is case-insensitive.

### Examples

Suppose there are seven tables in the upstream cluster:

- `inspector_mysql_0.tb_emp1`
- `Inspector_mysql_0.tb_emp1`
- `inspector_mysql_0.Tb_emp1`
- `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.Tb_emp1`
- `Inspector_mysql_1.Tb_emp1`

In the configuration example, the upstream cluster has a rule `Source.rule1`, and the target table is `inspector_mysql_1.tb_emp1`.

#### Example 1

If the configuration is as follows:

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_0"
table-pattern = "tb_emp1"
target-schema = "inspector_mysql_1"
target-table = "tb_emp1"
```

The routing results will be as follows:

- `inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.tb_emp1` is routed to `_no__exists__db_._no__exists__table_`
- `Inspector_mysql_1.tb_emp1` is routed to `_no__exists__db_._no__exists__table_`
- `inspector_mysql_1.Tb_emp1` is routed to `_no__exists__db_._no__exists__table_`
- `Inspector_mysql_1.Tb_emp1` is routed to `_no__exists__db_._no__exists__table_`

#### Example 2

If the configuration is as follows:

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_0"
target-schema = "inspector_mysql_1"
```

The routing results will be as follows:

- `inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_1.Tb_emp1`
- `inspector_mysql_1.tb_emp1` is routed to `_no__exists__db_._no__exists__table_`
- `Inspector_mysql_1.tb_emp1` is routed to `_no__exists__db_._no__exists__table_`
- `inspector_mysql_1.Tb_emp1` is routed to `_no__exists__db_._no__exists__table_`
- `Inspector_mysql_1.Tb_emp1` is routed to `_no__exists__db_._no__exists__table_`

#### Example 3

If the configuration is as follows:

```toml
[Source.rule1]
schema-pattern = "other_schema"
target-schema = "other_schema"
```

The routing results will be as follows:

- `inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_0.tb_emp1`
- `Inspector_mysql_0.tb_emp1` is routed to `Inspector_mysql_0.tb_emp1`
- `inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_0.Tb_emp1`
- `inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`

#### Example 4

If the configuration is as follows:

```toml
[Source.rule1]
schema-pattern = "inspector_mysql_?"
table-pattern = "tb_emp1"
target-schema = "inspector_mysql_1"
target-table = "tb_emp1"
```

The routing results will be as follows:

- `inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`

#### Example 5

If you do not set any rules, the routing results will be as follows:

- `inspector_mysql_0.tb_emp1` is routed to `inspector_mysql_0.tb_emp1`
- `Inspector_mysql_0.tb_emp1` is routed to `Inspector_mysql_0.tb_emp1`
- `inspector_mysql_0.Tb_emp1` is routed to `inspector_mysql_0.Tb_emp1`
- `inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
- `Inspector_mysql_1.Tb_emp1` is routed to `inspector_mysql_1.tb_emp1`
