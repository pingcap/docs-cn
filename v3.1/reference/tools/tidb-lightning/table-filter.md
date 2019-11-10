---
title: TiDB Lightning Table Filter
summary: Use black and white lists to filter out tables, ignoring them during import.
category: reference
---

# TiDB Lightning Table Filter

TiDB Lightning supports setting up black and white lists to ignore certain databases and tables. This can be used to skip cache tables, or manually partition the data source on a shared storage to allow multiple Lightning instances work together without interfering each other.

The filtering rule is similar to MySQL `replication-rules-db`/`replication-rules-table`.

## Filtering databases

```toml
[black-white-list]
do-dbs = ["pattern1", "pattern2", "pattern3"]
ignore-dbs = ["pattern4", "pattern5"]
```

* If the `do-dbs` array in the `[black-white-list]` section is not empty,
    * If the name of a database matches *any* pattern in the `do-dbs` array, the database is included.
    * Otherwise, the database is skipped.
* Otherwise, if the name matches *any* pattern in the `ignore-dbs` array, the database is skipped.
* If a database’s name matches *both* the `do-dbs` and `ignore-dbs` arrays, the database is included.

The pattern can either be a simple name, or a regular expression in [Go dialect](https://golang.org/pkg/regexp/syntax/#hdr-syntax) if it starts with a `~` character.

## Filtering tables

```toml
[[black-white-list.do-tables]]
db-name = "db-pattern-1"
tbl-name = "table-pattern-1"

[[black-white-list.do-tables]]
db-name = "db-pattern-2"
tbl-name = "table-pattern-2"

[[black-white-list.do-tables]]
db-name = "db-pattern-3"
tbl-name = "table-pattern-3"

[[black-white-list.ignore-tables]]
db-name = "db-pattern-4"
tbl-name = "table-pattern-4"

[[black-white-list.ignore-tables]]
db-name = "db-pattern-5"
tbl-name = "table-pattern-5"
```

* If the `do-tables` array is not empty,
    * If the qualified name of a table matched *any* pair of patterns in the `do-tables` array, the table is included.
    * Otherwise, the table is skipped
* Otherwise, if the qualified name matched *any* pair of patterns in the `ignore-tables` array, the table is skipped.
* If a table’s qualified name matched *both* the `do-tables` and `ignore-tables` arrays, the table is included.

Note that the database filtering rules are applied before Lightning considers the table filtering rules. This means if a database is ignored by `ignore-dbs`, all tables inside this database are not considered even if they matches any `do-tables` array.

## Example

To illustrate how these rules work, suppose the data source contains the following tables:

```
`logs`.`messages_2016`
`logs`.`messages_2017`
`logs`.`messages_2018`
`forum`.`users`
`forum`.`messages`
`forum_backup_2016`.`messages`
`forum_backup_2017`.`messages`
`forum_backup_2018`.`messages`
`admin`.`secrets`
```

Using this configuration:

```toml
[black-white-list]
do-dbs = [
    "forum_backup_2018",            # rule A
    "~^(logs|forum)$",              # rule B
]
ignore-dbs = [
    "~^forum_backup_",              # rule C
]

[[black-white-list.do-tables]]      # rule D
db-name = "logs"
tbl-name = "~_2018$"

[[black-white-list.ignore-tables]]  # rule E
db-name = "~.*"
tbl-name = "~^messages.*"

[[black-white-list.do-tables]]      # rule F
db-name = "~^forum.*"
tbl-name = "messages"
```

First apply the database rules:

| Database                  | Outcome                                    |
|---------------------------|--------------------------------------------|
| `` `logs` ``              | Included by rule B                         |
| `` `forum` ``             | Included by rule B                         |
| `` `forum_backup_2016` `` | Skipped by rule C                          |
| `` `forum_backup_2017` `` | Skipped by rule C                          |
| `` `forum_backup_2018` `` | Included by rule A (rule C will not apply) |
| `` `admin` ``             | Skipped since `do-dbs` is not empty and this does not match any pattern |

Then apply the table rules:

| Table                                | Outcome                                    |
|--------------------------------------|--------------------------------------------|
| `` `logs`.`messages_2016` ``         | Skipped by rule E                          |
| `` `logs`.`messages_2017` ``         | Skipped by rule E                          |
| `` `logs`.`messages_2018` ``         | Included by rule D (rule E will not apply) |
| `` `forum`.`users` ``                | Skipped, since `do-tables` is not empty and this does not match any pattern |
| `` `forum`.`messages` ``             | Included by rule F (rule E will not apply) |
| `` `forum_backup_2016`.`messages` `` | Skipped, since database is already skipped |
| `` `forum_backup_2017`.`messages` `` | Skipped, since database is already skipped |
| `` `forum_backup_2018`.`messages` `` | Included by rule F (rule E will not apply) |
| `` `admin`.`secrets` ``              | Skipped, since database is already skipped |
