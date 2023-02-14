---
title: TiDB Control User Guide
summary: Use TiDB Control to obtain TiDB status information for debugging.
aliases: ['/docs/dev/tidb-control/','/docs/dev/reference/tools/tidb-control/']
---

# TiDB Control User Guide

TiDB Control is a command-line tool of TiDB, usually used to obtain the status information of TiDB for debugging. This document introduces the features of TiDB Control and how to use these features.

## Get TiDB Control

You can get TiDB Control by installing it using TiUP or by compiling it from source code.

> **Note:**
>
> It is recommended that the version of the Control tool you use is consistent with the version of the cluster.

### Install TiDB Control using TiUP

After installing TiUP, you can use `tiup ctl:v<CLUSTER_VERSION> tidb` command to get and execute TiDB Control.

### Compile from source code

- Compilation environment requirement: [Go](https://golang.org/) Version 1.19 or later
- Compilation procedures: Go to the root directory of the [TiDB Control project](https://github.com/pingcap/tidb-ctl), use the `make` command to compile, and generate `tidb-ctl`.
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

Currently, TiDB Control has the following subcommands:

- `tidb-ctl base64decode`: used for `BASE64` decoding
- `tidb-ctl decoder`: used for `KEY` decoding
- `tidb-ctl etcd`: used for operating etcd
- `tidb-ctl log`: used to format the log file to expand the single-line stack information
- `tidb-ctl mvcc`: used to get the MVCC information
- `tidb-ctl region`: used to get the Region information
- `tidb-ctl schema`: used to get the schema information
- `tidb-ctl table`: used to get the table information

### Get help

Use `tidb-ctl -h/--help` to get usage information.

TiDB Control consists of multiple layers of commands. You can use `-h/--help` after each command/subcommand to get its respective usage information.

The following example shows how to obtain the schema information:

Use `tidb-ctl schema -h` to get usage details. The `schema` command itself has two subcommands: `in` and `tid`.

- `in` is used to obtain the table schema of all tables in the database through the database name.
- `tid` is used to obtain the table schema by using the unique `table_id` in the whole database.

### Global options

`tidb-ctl` has the following connection-related global options:

- `--host`: TiDB Service address (default 127.0.0.1)
- `--port`: TiDB status port (default 10080)
- `--pdhost`: PD Service address (default 127.0.0.1)
- `--pdport`: PD Service port (default 2379)
- `--ca`: The CA file path used for the TLS connection
- `--ssl-key`: The key file path used for the TLS connection
- `--ssl-cert`: The certificate file path used for the TLS connection

`--pdhost` and `--pdport` are mainly used in the `etcd` subcommand. For example, `tidb-ctl etcd ddlinfo`. If you do not specify the address and the port, the following default value is used:

- The default service address of TiDB and PD: `127.0.0.1`. The service address must be an IP address.
- The default service port of TiDB: `10080`.
- The default service port of PD: `2379`.

### The `schema` command

#### The `in` subcommand

`in` is used to obtain the table schema of all tables in the database through the database name.

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

#### The `tid` subcommand

`tid` is used to obtain the table schema by using the unique `table_id` in the whole database. You can use the `in` subcommand to get all table IDs of certain schema and use the `tid` subcommand to get the detailed table information.

For example, the table ID of `mysql.stat_meta` is `21`. You can use `tidb-ctl schema tid -i 21` to obtain the detail of `mysql.stat_meta`.

```json
{
 "id": 21,
 "name": {
  "O": "stats_meta",
  "L": "stats_meta"
 },
 "charset": "utf8mb4",
 "collate": "utf8mb4_bin",
  ...
}
```

Like the `in` subcommand, if you do not want to use the default TiDB service address and status port, use the `--host` and `--port` options to specify the host and port.

#### The `base64decode` command

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

3. Decode ```handle id (uint64) using `base64decode` ```.

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

### The `decoder` command

- The following example shows how to decode the row key, similar to decoding the index key.

    ```shell
    $ ./tidb-ctl decoder "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    format: table_row
    table_id: -9223372036854775780      table_id: -9223372036854775780
    row_id: -9223372036854775558        row_id: -9223372036854775558
    ```

- The following example shows how to decode `value`.

    ```shell
    $ ./tidb-ctl decoder AhZoZWxsbyB3b3JsZAiAEA==
    format: index_value
    type: bigint, value: 1024       index_value[0]: {type: bytes, value: hello world}
    index_value[1]: {type: bigint, value: 1024}
    ```

### The `etcd` command

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

### The `log` command

The stack information for the TiDB error log is in one line format. You could use `tidb-ctl log` to change its format to multiple lines.

### The `keyrange` command

The `keyrange` subcommand is used to query the global or table-related key range information, which is output in the hexadecimal form.

* Execute the `tidb-ctl keyrange` command to check the global key range information:

    {{< copyable "shell-regular" >}}

    ```shell
    tidb-ctl keyrange
    ```

    ```
    global ranges:
      meta: (6d, 6e)
      table: (74, 75)
    ```

* Add the `--encode` option to display encoded keys (in the same format as in TiKV and PD):

    {{< copyable "shell-regular" >}}

    ```shell
    tidb-ctl keyrange --encode
    ```

    ```
    global ranges:
      meta: (6d00000000000000f8, 6e00000000000000f8)
      table: (7400000000000000f8, 7500000000000000f8)
    ```

* Execute the `tidb-ctl keyrange --database={db} --table={tbl}` command to check the global and table-related key range information:

    {{< copyable "shell-regular" >}}

    ```shell
    tidb-ctl keyrange --database test --table ttt
    ```

    ```
    global ranges:
      meta: (6d, 6e)
      table: (74, 75)
    table ttt ranges: (NOTE: key range might be changed after DDL)
      table: (74800000000000002f, 748000000000000030)
      table indexes: (74800000000000002f5f69, 74800000000000002f5f72)
        index c2: (74800000000000002f5f698000000000000001, 74800000000000002f5f698000000000000002)
        index c3: (74800000000000002f5f698000000000000002, 74800000000000002f5f698000000000000003)
        index c4: (74800000000000002f5f698000000000000003, 74800000000000002f5f698000000000000004)
      table rows: (74800000000000002f5f72, 748000000000000030)
    ```
