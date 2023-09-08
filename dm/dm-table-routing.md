---
title: TiDB Data Migration Table Routing
summary: Learn the usage and precautions of table routing in DM.
---

# TiDB Data Migration Table Routing

When you migrate data using TiDB Data Migration (DM), you can configure the table routing to migrate a certain table of the upstream MySQL or MariaDB instance to the specified table in the downstream.

> **Note:**
>
> - Configuring multiple different routing rules for a single table is not supported.
> - The match rule of schema needs to be configured separately, which is used to migrate `CREATE/DROP SCHEMA xx`, as shown in `rule-2` of the [Configure table routing](#configure-table-routing) section.

## Configure table routing

```yaml
routes:
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
    # extract-table, extract-schema, and extract-source are optional and
    # are required only when you need to extract information about sharded
    # tables, sharded schemas, and source datatabase information.
    extract-table:
      table-regexp: "t_(.*)"
      target-column: "c_table"
    extract-schema:
      schema-regexp: "test_(.*)"
      target-column: "c_schema"
    extract-source:
      source-regexp: "(.*)"
      target-column: "c_source"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

Regular expressions and wildcards are supported to match database and table names. In simple scenarios, it is recommended that you use the wildcard for matching schemas and tables. However, note the following:

- Wildcards including `*`, `?`, and `[]` are supported. There can only be one `*` symbol in a wildcard match, and it must be at the end. For example, in `table-pattern: "t_*"`, `"t_*"` indicates all tables starting with `t_`. See [wildcard matching](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax) for details.

- `table-regexp`, `schema-regexp`, and `source-regexp` only support regular expressions and cannot start with the `~` symbol.

- `schema-pattern` and `table-pattern` support both wildcards and regular expressions. Regular expressions must begin with the `~` symbol.

## Parameter descriptions

- DM migrates the upstream MySQL or MariaDB instance tables that match the [`schema-pattern`/`table-pattern` rule provided by Table selector](/dm/table-selector.md) to the downstream `target-schema`/`target-table`.
- For sharded tables that match the `schema-pattern`/`table-pattern` rules, DM extracts the table name by using the `extract-table`.`table-regexp` regular expression, the schema name by using the `extract-schema`.`schema-regexp` regular expression, and source information by using the `extract-source`.`source-regexp` regular expression. Then DM writes the extracted information to the corresponding `target-column` in the merged table in the downstream.

## Usage examples

This section shows the usage examples in four different scenarios.

If you need to migrate and merge MySQL shards of small datasets to TiDB, refer to [this tutorial](/migrate-small-mysql-shards-to-tidb.md).

### Merge sharded schemas and tables

Assuming in the scenario of sharded schemas and tables, you want to migrate the `test_{1,2,3...}`.`t_{1,2,3...}` tables in two upstream MySQL instances to the `test`.`t` table in the downstream TiDB instance.

To migrate the upstream instances to the downstream `test`.`t`, you must create the following routing rules:

- `rule-1` is used to migrate DML or DDL statements of the table that matches `schema-pattern: "test_*"` and `table-pattern: "t_*"` to the downstream `test`.`t`.
- `rule-2` is used to migrate DDL statements of the schema that matches `schema-pattern: "test_*"`, such as `CREATE/DROP SCHEMA xx`.

> **Note:**
>
> - If the downstream `schema: test` already exists and is not to be deleted, you can omit `rule-2`.
> - If the downstream `schema: test` does not exist and only `rule-1` is configured, then it reports the `schema test doesn't exist` error during migration.

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

### Extract table, schema, and source information and write into the merged table

Assuming in the scenario of sharded schemas and tables, you want to migrate the `test_{1,2,3...}`.`t_{1,2,3...}` tables in two upstream MySQL instances to the `test`.`t` table in the downstream TiDB instance. At the same time, you want to extract the source information of the sharded tables and write it to the downstream merged table.

To migrate the upstream instances to the downstream `test`.`t`, you must create routing rules similar to the previous section [Merge sharded schemas and tables](#merge-sharded-schemas-and-tables). In addtion, you need to add the `extract-table`, `extract-schema`, and `extract-source` configurations:

- `extract-table`: For a sharded table matching `schema-pattern` and `table-pattern`, DM extracts the sharded table name by using `table-regexp` and writes the name suffix without the `t_` part to `target-column` of the merged table, that is, the `c_table` column.
- `extract-schema`: For a sharded schema matching `schema-pattern` and `table-pattern`, DM extracts the sharded schema name by using `schema-regexp` and writes the name suffix without the `test_` part to `target-column` of the merged table, that is, the `c_schema` column.
- `extract-source`: For a sharded table matching `schema-pattern` and `table-pattern`, DM writes the source instance information to the `target-column` of the merged table, that is, the `c_source` column.

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
    extract-table:
      table-regexp: "t_(.*)"
      target-column: "c_table"
    extract-schema:
      schema-regexp: "test_(.*)"
      target-column: "c_schema"
    extract-source:
      source-regexp: "(.*)"
      target-column: "c_source"
  rule-2:
    schema-pattern: "test_*"
    target-schema: "test"
```

To extract the source information of upstream sharded tables to the merged table in the downstream, you **must manually create a merged table in the downstream before starting the migration**. The merged table must contain the three `target-columns` (`c_table`, `c_schema`, and `c_source`) used for specifying the source information. In addition, these columns **must be the last columns and be [string types](/data-type-string.md)**.

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

Assume that the upstream has the following two data sources:

Data source `mysql-01`:

```sql
mysql> select * from test_11.t_1;
+---+
| a |
+---+
| 1 |
+---+
mysql> select * from test_11.t_2;
+---+
| a |
+---+
| 2 |
+---+
mysql> select * from test_12.t_1;
+---+
| a |
+---+
| 3 |
+---+
```

Data source `mysql-02`:

```sql
mysql> select * from test_13.t_3;
+---+
| a |
+---+
| 4 |
+---+
```

After migration using DM, data in the merged table will be as follows:

```sql
mysql> select * from test.t;
+---+---------+----------+----------+
| a | c_table | c_schema | c_source |
+---+---------+----------+----------+
| 1 | 1       | 11       | mysql-01 |
| 2 | 2       | 11       | mysql-01 |
| 3 | 1       | 12       | mysql-01 |
| 4 | 3       | 13       | mysql-02 |
+---+---------+----------+----------+
```

#### Incorrect examples of creating merged tables

> **Note:**
>
> If any of the following errors occur, source information of sharded tables and schemas might fail to be written to the merged table.

- `c-table` is not in the last three columns:

```sql
CREATE TABLE `test`.`t` (
    c_table varchar(10) DEFAULT NULL,
    a int(11) PRIMARY KEY,
    c_schema varchar(10) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL
);
```

- `c-source` is absent:

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema varchar(10) DEFAULT NULL,
);
```

- `c_schema` is not a string type:

```sql
CREATE TABLE `test`.`t` (
    a int(11) PRIMARY KEY,
    c_table varchar(10) DEFAULT NULL,
    c_schema int(11) DEFAULT NULL,
    c_source varchar(10) DEFAULT NULL,
);
```

### Merge sharded schemas

Assuming in the scenario of sharded schemas, you want to migrate the `test_{1,2,3...}`.`t_{1,2,3...}` tables in the two upstream MySQL instances to the `test`.`t_{1,2,3...}` tables in the downstream TiDB instance.

To migrate the upstream schemas to the downstream `test`.`t_[1,2,3]`, you only need to create one routing rule.

```yaml
  rule-1:
    schema-pattern: "test_*"
    target-schema: "test"
```

### Incorrect table routing

Assuming that the following two routing rules are configured and `test_1_bak`.`t_1_bak` matches both `rule-1` and `rule-2`, an error is reported because the table routing configuration violates the number limitation.

```yaml
  rule-1:
    schema-pattern: "test_*"
    table-pattern: "t_*"
    target-schema: "test"
    target-table: "t"
  rule-2:
    schema-pattern: "test_1_bak"
    table-pattern: "t_1_bak"
    target-schema: "test"
    target-table: "t_bak"
```
