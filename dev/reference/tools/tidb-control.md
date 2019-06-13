---
title: TiDB Controller 使用说明
category: reference
aliases: ['/docs-cn/tools/tidb-controller/']
---

# TiDB Controller 使用说明

TiDB Controller 是 TiDB 的命令行工具，用于获取 TiDB 状态信息，多用于调试。

## 源码编译

* 编译环境要求：[Go](https://golang.org/) Version 1.7 以上

* 编译步骤：在 [TiDB Controller 项目](https://github.com/pingcap/tidb-ctl)根目录，使用 `make` 命令进行编译，生成 tidb-ctl。

* 编译文档：帮助文档在 doc 文件夹下，如丢失或需要更新，可通过 `make doc` 命令生成帮助文档。

## 使用介绍

`tidb-ctl` 的使用由命令（包括子命令）、选项和参数组成。

* 命令：即不带 `-` 或者 `--` 的字符
* 选项：即带有 `-` 或者 `--` 的字符
* 参数：即命令或选项字符后紧跟的传递给命令和选项的字符

如：`tidb-ctl schema in mysql -n db`

* schema: 命令
* in: schema 的子命令
* mysql: in 的参数
* -n: 选项
* db: -n 的参数

### 获取帮助

`tidb-ctl -h/--help` 用于获取帮助信息。tidb-ctl 由多层命令组成，tidb-ctl 及其所有子命令都可以通过 `-h/--help` 来获取使用帮助。

### 连接

`tidb-ctl` 与连接相关的参数有 4 个，分别为：

* `--host`：TiDB 服务地址
* `--port`：TiDB 服务端口
* `--pdhost`：PD 服务地址
* `--pdport`：PD 服务端口

其中 `--pdhost` 和 `--pdport` 主要是用于 `etcd` 子命令，例如：`tidb-ctl etcd ddlinfo`。如不添加地址和端口将使用默认值，TiDB/PD 服务默认的地址是 127.0.0.1 （服务地址只能使用 IP 地址），TiDB 服务端口默认的端口是 10080，PD 服务端口默认的端口是 2379 **连接选项是全局选项，适用于以下所有命令。**

目前，TiDB Controller 包含以下子命令，各个子命令的具体用法可以使用 `tidb-ctl SUBCOMMAND --help` 获取使用帮助：

* `tidb-ctl base64decode`：BASE64 解码
* `tidb-ctl decoder`：用于 KEY 解码
* `tidb-ctl etcd`：用于操作 etcd
* `tidb-ctl log`：格式化日志文件，将单行的堆栈信息展开
* `tidb-ctl mvcc`：MVCC 信息
* `tidb-ctl region`：Region 信息
* `tidb-ctl schema`：Schema 信息
* `tidb-ctl table`：Table 信息

### 使用举例

以获取 Schema 信息为例：

通过 `tidb-ctl schema -h` 可以获取这个子命令的使用帮助。`schema` 有两个子命令，`in` 和 `tid`。`in` 用来通过数据库名获取数据库中所有表的表结构，`tid` 用来通过全数据库唯一的 `table_id` 获取表的表结构。

#### in 命令

同样可以通过 `tidb-ctl schema in -h/--help` 来获取子命令 `in` 的使用帮助。

##### 基本用法

```
tidb-ctl schema in {数据库名}
```

如：`tidb-ctl schema in mysql` 将得到以下结果：

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

结果将以 json 形式展示，内容较长，这里做了截断。

* 如希望指定表名，可以使用 `tidb-ctl schema in {数据库名} -n {表名}` 进行过滤。

    如：`tidb-ctl schema in mysql -n db` 将得到 mysql 库中 db 表的表结构，结果如下：

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

    这里同样做了截断。

    如使用的 TiDB 地址不为默认地址和端口，可以使用命令行参数 `--host`，`--port` 选项，如：`tidb-ctl --host 172.16.55.88 --port 8898 schema in mysql -n db`。

#### base64decode 子命令

`base64decode`  用来解码 base64 数据。

```shell
tidb-ctl base64decode [base64_data]
tidb-ctl base64decode [db_name.table_name] [base64_data]
tidb-ctl base64decode [table_id] [base64_data]
```

* 准备环境，执行以下 SQL

    ```sql
    use test;
    create table t (a int, b varchar(20),c datetime default current_timestamp , d timestamp default current_timestamp, unique index(a));
    insert into t (a,b,c) values(1,"哈哈 hello",NULL);
    alter table t add column e varchar(20);
    ```

* 用 http api 接口获取 mvcc 数据

    ```shell
    ▶ curl "http://$IP:10080/mvcc/index/test/t/a/1?a=1"
    {
     "info": {
      "writes": [
       {
        "start_ts": 407306449994645510,
        "commit_ts": 407306449994645513,
        "short_value": "AAAAAAAAAAE="    # unique index a 存的值是对应行的 handle id.
       }
      ]
     }
    }%

    ▶ curl "http://$IP:10080/mvcc/key/test/t/1"
    {
     "info": {
      "writes": [
       {
        "start_ts": 407306588892692486,
        "commit_ts": 407306588892692489,
        "short_value": "CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk="  # handle id 为 1 的行数据。 
       }
      ]
     }
    }% 
    ```

* 用 `base64decode` 解码 handle id (uint64)。

  ```shell
  ▶ tidb-ctl base64decode AAAAAAAAAAE=
  hex: 0000000000000001
  uint64: 1
  ```

* 用 `base64decode` 解码行数据。

    ```shell
    ▶ ./tidb-ctl base64decode test.t CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk=
    a:      1
    b:      哈哈 hello
    c is NULL
    d:      2019-03-28 05:35:30
    e not found in data

    # if the table id of test.t is 60, you can also use below command to do the same thing.
    ▶ ./tidb-ctl base64decode 60 CAIIAggEAhjlk4jlk4ggaGVsbG8IBgAICAmAgIDwjYuu0Rk=
    a:      1
    b:      哈哈 hello
    c is NULL
    d:      2019-03-28 05:35:30
    e not found in data
    ```

#### decoder 子命令

* 以下示例解码 row key，index key 类似。

    ```shell
    ▶ ./tidb-ctl decoder -f table_row -k "t\x00\x00\x00\x00\x00\x00\x00\x1c_r\x00\x00\x00\x00\x00\x00\x00\xfa"
    table_id: -9223372036854775780
    row_id: -9223372036854775558
    ```

* 以下示例解码 value

    ```shell
    ▶ ./tidb-ctl decoder -f value -k AhZoZWxsbyB3b3JsZAiAEA==
    type: bytes, value: hello world
    type: bigint, value: 1024
    ```

#### etcd 子命令

* `tidb-ctl etcd ddlinfo` 获取 DDL 信息。
* `tidb-ctl etcd putkey KEY VALUE` 添加 KEY VALUE 到 etcd （所有的 KEY 会添加到 `/tidb/ddl/all_schema_versions/` 之下）。

    ```shell
    tidb-ctl etcd putkey "foo" "bar"
    ```

    实际是添加 KEY 为 `/tidb/ddl/all_schema_versions/foo`，VALUE 为 `bar` 的键值对到 etcd 中。

* `tidb-ctl etcd delkey` 删除 etcd 中的 KEY，只有前缀以 `/tidb/ddl/fg/owner/` 和 `/tidb/ddl/all_schema_versions/` 开头才允许被删除。

    ```shell
    tidb-ctl etcd delkey "/tidb/ddl/fg/owner/foo"
    tidb-ctl etcd delkey "/tidb/ddl/all_schema_versions/bar"
    ```

#### log 子命令

TiDB 错误日志的堆栈信息是一行的格式，可以使用 `tidb-ctl log` 将堆栈信息格式化成多行形式。
