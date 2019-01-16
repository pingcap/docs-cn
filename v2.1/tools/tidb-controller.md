---
title: TiDB Controller User Guide
summary: Use TiDB Controller to obtain TiDB status information for debugging.
category: tools
---

# TiDB Controller User Guide

TiDB Controller is a command line tool of TiDB, usually used to obtain the status information of TiDB for debugging.

## Compile from source code

- Compilation environment requirement: [Go](https://golang.org/) Version 1.7 or later
- Compilation procedures: Go to the root directory of the [TiDB Controller project](https://github.com/pingcap/tidb-ctl), use the `make` command to compile, and generate `tidb-ctl`.
- Compilation documentation: you can find the help files in the `doc` directory; if the help files are lost or you want to update them, use the `make doc` command to generate the help files.

## Usage introduction

The usage of `tidb-ctl` consists of command (including subcommand), option, and flag.

- command: characters without `-` or `--`
- option: characters with `-` or `--`
- flag: characters exactly following the command or option, passing value to the command or option

Usage example: `tidb-ctl schema in mysql -n db`

- `schema`: the command
- `in`: the subcommand of schema
- `mysql`: the flag of `in`
- `-n`: the option
- `db`: the flag of `-n`

### Get help

Use `tidb-ctl -h/--help` to get the help information. `tidb-ctl` consists of multiple layers of commands. You can use `-h/--help` to get the help information of `tidb-ctl` and all other subcommands.

### Connect

```
tidb-ctl -H/--host {TiDB service address} -P/--port {TiDB service port}
```

If you do not add an address or a port, the default value is used. The default address is `127.0.0.1` (service address must be the IP address); the default port is `10080`. Connection options are top-level options and apply to all of the following commands.

Currently, TiDB Controller can obtain four categories of information using the following four commands:

- `tidb-ctl mvcc`: MVCC information
- `tidb-ctl region`: Region information
- `tidb-ctl schema`: Schema information
- `tidb-ctl table`: Table information

### Examples

The following example shows how to obtain the schema information:

Use `tidb-ctl schema -h` to get the help information of the subcommands. `schema` has two subcommands: `in` and `tid`.

- `in` is used to obtain the table schema of all tables in the database through the database name.
- `tid` is used to obtain the table schema through the unique `table_id` in the whole database.

#### The `in` command

You can also use `tidb-ctl schema in -h/--help` to get the help information of the `in` subcommand.

##### Basic usage

```
tidb-ctl schema in {database name}
```

For example, `tidb-ctl schema in mysql` returns the following result:

```json
[
    {
        "id": 13,
        "name": {
            "O": "columns_priv",
            "L": "columns_priv"
        },
              ...
        "update_timestamp": 399494726837600268,
        "ShardRowIDBits": 0,
        "Partition": null
    }
]
```

The result is long and displayed in JSON. The above result is a truncated one.

- If you want to specify the table name, use `tidb-ctl schema in {database} -n {table name}` to filter.

    For example, `tidb-ctl schema in mysql -n db` returns the table schema of the `db` table in the `mysql` database:

    ```json
    {
        "id": 9,
        "name": {
            "O": "db",
            "L": "db"
        },
        ...
        "Partition": null
    }
    ```

    The above result is a truncated one, too.

- If you want to specify the server address, use the `-H -P` option.

    For example, `tidb-ctl -H 127.0.0.1 -P 10080 schema in mysql -n db`.