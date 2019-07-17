---
title: TiDB Controller User Guide
summary: Use TiDB Controller to obtain TiDB status information for debugging.
category: reference
---

# TiDB Controller User Guide

TiDB Controller is a command line tool of TiDB, usually used to obtain the status information of TiDB for debugging.

## Compile from source code

- Compilation environment requirement: [Go](https://golang.org/) Version 1.7 or later
- Compilation procedures: Go to the root directory of the [TiDB Controller project](https://github.com/pingcap/tidb-ctl), use the `make` command to compile, and generate `tidb-ctl`.
- Compilation documentation: you can find the help files in the `doc` directory; if the help files are lost or you want to update them, use the `make doc` command to generate the help files.

## Usage introduction

This section describes how to use commands, subcommands, options, and flags in `tidb-ctl`.

- command: characters without `-` or `--`
- subcommand: characters without `-` or `--` that follow a command
- option: characters with `-` or `--`
- flag: characters exactly following a command/subcommand or option, passing value to the command/subcommand or option

Usage example: `tidb-ctl schema in mysql -n db`

- `schema`: the command
- `in`: the subcommand of `schema`
- `mysql`: the flag of `in`
- `-n`: the option
- `db`: the flag of `-n`

### Get help

Use `tidb-ctl -h/--help` to get usage information.

TiDB Controller consists of multiple layers of commands. You can use `-h/--help` after each command/subcommand to get its respective usage information.

### Connect

`tidb-ctl` has 4 connection related options:

- `--host`: TiDB Service address (default 127.0.0.1)
- `--port`: TiDB Service port (default 10080)
- `--pdhost`: PD Service address (default 127.0.0.1)
- `--pdport`: PD Service port (default 2379)

`--pdhost` and `--pdport` are mainly used in the `etcd` subcommand. For example, `tidb-ctl etcd ddlinfo`. If you do not specify the address and the port, the following default value is used:

- The default service address of TiDB and PD: `127.0.0.1`. The service address must be an IP address.
- The default service port of TiDB: `10080`.
- The default service port of PD: `2379`.

**Connection options are global options that apply to all the following commands:**

- `tidb-ctl base64decode`: BASE64 decode
- `tidb-ctl decoder`: for KEY decode
- `tidb-ctl etcd`: for operating etcd
- `tidb-ctl log`: format the log file to expand the single-line stack information
- `tidb-ctl mvcc`: MVCC information
- `tidb-ctl region`: Region information
- `tidb-ctl schema`: Schema information
- `tidb-ctl table`: Table information

For details about how to use the above `tidb-ctl` commands, use `tidb-ctl SUBCOMMAND --help` to get the help information.

### Usage examples

The following example shows how to obtain the schema information:

Use `tidb-ctl schema -h` to get usage details. The `schema` command itself has two subcommands: `in` and `tid`.

- `in` is used to obtain the table schema of all tables in the database through the database name.
- `tid` is used to obtain the table schema by using the unique `table_id` in the whole database.

#### The `in` command

You can use `tidb-ctl schema in -h/--help` to get the help information of the `in` subcommand.

##### Basic usage

```bash
tidb-ctl schema in <database name>
```

For example, running `tidb-ctl schema in mysql` returns the following result:

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

The result is displayed in the JSON format. (The above output is truncated.)

- If you want to specify the table name, use `tidb-ctl schema in <database> -n <table name>` to filter.

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

    (The above output is also truncated.)
    
    If you do not want to use the default TiDB service address and port, use the `--host` and `--port` options to configure. For example, `tidb-ctl --host 172.16.55.88 --port 8898 schema in mysql -n db`.

#### The `base64decode` subcommand

`base64decode` is used to decode `base64` data.

```shell
tidb-ctl base64decode [base64_data]
tidb-ctl base64decode [db_name.table_name] [base64_data]
tidb-ctl base64decode [table_id] [base64_data]
```

1. Execute the following SQL statement to prepare the environment:

    ```sql
    use test;
    create table t (a int, b varchar(20),c datetime default current_timestamp , d timestamp default current_timestamp, unique index(a));
    insert into t (a,b,c) values(1,"哈哈 hello",NULL);
    alter table t add column e varchar(20);
    ```

2. Obtian MVCC data using the HTTP API interface:

    ```shell
    $ curl "http://$IP:10080/mvcc/index/test/t/a/1?a=1"
    {
     "info": {
      "writes": [
       {
        "start_ts": 407306449994645510,
        "commit_ts": 407306449994645513,
        "short_value": "AAAAAAAAAAE="    # The unique index a stores the handle id of the corresponding row.
       }
      ]
     }
    }%

    $ curl "http://$IP:10080/mvcc/key/test/t/1"
    {
     "info": {
      "writes": [
       {
        "start_ts": 407306588892692486,
        "commit_ts": 407306588892692489,
        "short_value": "CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk="  # Row data that handle id is 1.
       }
      ]
     }
    }% 
    ```

3. Decode `handle id (uint64) using `base64decode`.

    ```shell
    $ tidb-ctl base64decode AAAAAAAAAAE=
    hex: 0000000000000001
    uint64: 1
    ```

4. Decode row data using `base64decode`.

    ```shell
    $ ./tidb-ctl base64decode test.t CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk=
    a:      1
    b:      哈哈 hello
    c is NULL
    d:      2019-03-28 05:35:30
    e not found in data

    # if the table id of test.t is 60, you can also use below command to do the same thing.
    $ ./tidb-ctl base64decode 60 CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk=
    a:      1
    b:      哈哈 hello
    c is NULL
    d:      2019-03-28 05:35:30
    e not found in data
    ```

#### The `decoder` subcommand

- The following example shows how to decode the row key, similar to decoding the index key.

    ```shell
    $ ./tidb-ctl decoder -f table_row -k "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    table_id: -9223372036854775780
    row_id: -9223372036854775558
    ```

- The following example shows how to decode `value`.

    ```shell
    $ ./tidb-ctl decoder -f value -k AhZoZWxsbyB3b3JsZAiAEA==
    type: bytes, value: hello world
    type: bigint, value: 1024
    ```

#### The `etcd` subcommand

- `tidb-ctl etcd ddlinfo` is used to obtain DDL information.
- `tidb-ctl etcd putkey KEY VALUE` is used to add KEY VALUE to etcd (All the KEYs are added to the `/tidb/ddl/all_schema_versions/` directory).

    ```shell
    tidb-ctl etcd putkey "foo" "bar"
    ```

    In fact, a key-value pair is added to the etcd whose KEY is `/tidb/ddl/all_schema_versions/foo` and VALUE is `bar`.

- `tidb-ctl etcd delkey` deletes the KEY in etcd. Only those KEYs with the `/tidb/ddl/fg/owner/` or `/tidb/ddl/all_schema_versions/` prefix can be deleted.

    ```shell
    tidb-ctl etcd delkey "/tidb/ddl/fg/owner/foo"
    tidb-ctl etcd delkey "/tidb/ddl/all_schema_versions/bar"
    ```

#### The `log` subcommand

The stack information for the TiDB error log is in one line format. You could use `tidb-ctl log` to change its format to multiple lines.
