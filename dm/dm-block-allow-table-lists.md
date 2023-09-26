---
title: TiDB Data Migration Block and Allow Lists
summary: Learn how to use the DM block and allow lists feature.
---

# TiDB Data Migration Block and Allow Lists

When you migrate data using TiDB Data Migration (DM), you can configure the block and allow lists to filter or only migrate all operations of some databases or some tables.

## Configure the block and allow lists

In the task configuration file, add the following configuration:

```yaml
block-allow-list:             # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  rule-1:
    do-dbs: ["test*"]         # Starting with characters other than "~" indicates that it is a wildcard;
                              # v1.0.5 or later versions support the regular expression rules.
    do-tables:
    - db-name: "test[123]"    # Matches test1, test2, and test3.
      tbl-name: "t[1-5]"      # Matches t1, t2, t3, t4, and t5.
    - db-name: "test"
      tbl-name: "t"
  rule-2:
    do-dbs: ["~^test.*"]      # Starting with "~" indicates that it is a regular expression.
    ignore-dbs: ["mysql"]
    do-tables:
    - db-name: "~^test.*"
      tbl-name: "~^t.*"
    - db-name: "test"
      tbl-name: "t*"
    ignore-tables:
    - db-name: "test"
      tbl-name: "log"
```

In simple scenarios, it is recommended that you use the wildcard for matching schemas and tables. However, note the following version differences:

- Wildcards including `*`, `?`, and `[]` are supported. There can only be one `*` symbol in a wildcard match, and it must be at the end. For example, in `tbl-name: "t*"`, `"t*"` indicates all tables starting with `t`. See [wildcard matching](https://en.wikipedia.org/wiki/Glob_(programming)#Syntax) for details.

- A regular expression must begin with the `~` character.

## Parameter descriptions

- `do-dbs`: allow lists of the schemas to be migrated, similar to [`replicate-do-db`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-do-db) in MySQL.
- `ignore-dbs`: block lists of the schemas to be migrated, similar to [`replicate-ignore-db`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-ignore-db) in MySQL.
- `do-tables`: allow lists of the tables to be migrated, similar to [`replicate-do-table`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-do-table) in MySQL. Both `db-name` and `tbl-name` must be specified.
- `ignore-tables`: block lists of the tables to be migrated, similar to [`replicate-ignore-table`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-ignore-table) in MySQL. Both `db-name` and `tbl-name` must be specified.

If a value of the above parameters starts with the `~` character, the subsequent characters of this value are treated as a [regular expression](https://golang.org/pkg/regexp/syntax/#hdr-syntax). You can use this parameter to match schema or table names.

## Filtering process

- The filtering rules corresponding to `do-dbs` and `ignore-dbs` are similar to the [Evaluation of Database-Level Replication and Binary Logging Options](https://dev.mysql.com/doc/refman/8.0/en/replication-rules-db-options.html) in MySQL.
- The filtering rules corresponding to `do-tables` and `ignore-tables` are similar to the [Evaluation of Table-Level Replication Options](https://dev.mysql.com/doc/refman/8.0/en/replication-rules-table-options.html) in MySQL.

> **Note:**
>
> In DM and in MySQL, the block and allow lists filtering rules are different in the following ways:
>
> - In MySQL, [`replicate-wild-do-table`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-wild-do-table) and [`replicate-wild-ignore-table`](https://dev.mysql.com/doc/refman/8.0/en/replication-options-replica.html#option_mysqld_replicate-wild-ignore-table) support wildcard characters. In DM, some parameter values directly supports regular expressions that start with the `~` character.
> - DM currently only supports binlogs in the `ROW` format, and does not support those in the `STATEMENT` or `MIXED` format. Therefore, the filtering rules in DM correspond to those in the `ROW` format in MySQL.
> - MySQL determines a DDL statement only by the database name explicitly specified in the `USE` section of the statement. DM determines a statement first based on the database name section in the DDL statement. If the DDL statement does not contain such a section, DM determines the statement by the `USE` section. Suppose that the SQL statement to be determined is `USE test_db_2; CREATE TABLE test_db_1.test_table (c1 INT PRIMARY KEY)`; that `replicate-do-db=test_db_1` is configured in MySQL and `do-dbs: ["test_db_1"]` is configured in DM. Then this rule only applies to DM and not to MySQL.

The filtering process of a `test`.`t` table is as follows:

1. Filter at the **schema** level:

    - If `do-dbs` is not empty, check whether a matched schema exists in `do-dbs`.

        - If yes, continue to filter at the **table** level.
        - If not, filter `test`.`t`.

    - If `do-dbs` is empty and `ignore-dbs` is not empty, check whether a matched schema exits in `ignore-dbs`.

        - If yes, filter `test`.`t`.
        - If not, continue to filter at the **table** level.

    - If both `do-dbs` and `ignore-dbs` are empty, continue to filter at the **table** level.

2. Filter at the **table** level:

    1. If `do-tables` is not empty, check whether a matched table exists in `do-tables`.

        - If yes, migrate `test`.`t`.
        - If not, filter `test`.`t`.

    2. If `ignore-tables` is not empty, check whether a matched table exists in `ignore-tables`.

        - If yes, filter `test`.`t`.
        - If not, migrate `test`.`t`.

    3. If both `do-tables` and `ignore-tables` are empty, migrate `test`.`t`.

> **Note:**
>
> To check whether the schema `test` should be filtered, you only need to filter at the schema level.

## Usage examples

Assume that the upstream MySQL instances include the following tables:

```
`logs`.`messages_2016`
`logs`.`messages_2017`
`logs`.`messages_2018`
`forum`.`users`
`forum`.`messages`
`forum_backup_2016`.`messages`
`forum_backup_2017`.`messages`
`forum_backup_2018`.`messages`
```

The configuration is as follows:

```yaml
block-allow-list:  # Use black-white-list if the DM version is earlier than or equal to v2.0.0-beta.2.
  bw-rule:
    do-dbs: ["forum_backup_2018", "forum"]
    ignore-dbs: ["~^forum_backup_"]
    do-tables:
    - db-name: "logs"
      tbl-name: "~_2018$"
    - db-name: "~^forum.*"
​      tbl-name: "messages"
    ignore-tables:
    - db-name: "~.*"
​      tbl-name: "^messages.*"
```

After applying the `bw-rule` rule:

| Table | Whether to filter | Why filter |
|:----|:----|:--------------|
| `logs`.`messages_2016` | Yes | The schema `logs` fails to match any `do-dbs`. |
| `logs`.`messages_2017` | Yes | The schema `logs` fails to match any `do-dbs`. |
| `logs`.`messages_2018` | Yes | The schema `logs` fails to match any `do-dbs`. |
| `forum_backup_2016`.`messages` | Yes | The schema `forum_backup_2016` fails to match any `do-dbs`. |
| `forum_backup_2017`.`messages` | Yes | The schema `forum_backup_2017` fails to match any `do-dbs`. |
| `forum`.`users` | Yes | 1. The schema `forum` matches `do-dbs` and continues to filter at the table level.<br/> 2. The schema and table fail to match any of `do-tables` and `ignore-tables` and `do-tables` is not empty. |
| `forum`.`messages` | No | 1. The schema `forum` matches `do-dbs` and continues to filter at the table level.<br/> 2. The table `messages` is in the `db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`. |
| `forum_backup_2018`.`messages` | No | 1. The schema `forum_backup_2018` matches `do-dbs` and continues to filter at the table level.<br/> 2. The schema and table match the `db-name: "~^forum.*",tbl-name: "messages"` of `do-tables`. |
