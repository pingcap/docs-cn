---
title: 升级后常见问题
category: FAQ
aliases: ['/docs-cn/op-guide/upgrade-faq/','/docs-cn/faq/upgrade/']
---

# 升级后常见问题

本文列出了一些升级后可能会遇到的问题与解决办法。

## 执行 DDL 操作时遇到的字符集 (charset) 问题

TiDB 在 v2.1.0 以及之前版本（包括 v2.0 所有版本）中，默认字符集是 UTF8。从 v2.1.1 开始，默认字符集变更为 UTF8MB4。如果在 v2.1.0 及之前版本中，建表时显式指定了 table 的 charset 为 UTF8，那么升级到 v2.1.1 之后，执行 DDL 操作可能会失败。

要避免该问题，需注意以下两个要点：

1. 在 v2.1.3 之前，TiDB 不支持修改 column 的 charset。所以，执行 DDL 操作时，新 column 的 charset 需要和旧 column 的 charset 保持一致。

2. 在 v2.1.3 之前，即使 column 的 charset 和 table 的 charset 不一样，`show create table` 也不会显示 column 的 charset，但可以通过 HTTP API 获取 table 的元信息来查看 column 的 charset，下文提供了示例。

### 问题 1：`unsupported modify column charset utf8mb4 not match origin utf8`

- 升级前：v2.1.0 及之前版本

    ```sql
    tidb > create table t(a varchar(10)) charset=utf8;
    Query OK, 0 rows affected
    Time: 0.106s
    tidb > show create table t
    +-------+-------------------------------------------------------+
    | Table | Create Table                                          |
    +-------+-------------------------------------------------------+
    | t     | CREATE TABLE `t` (                                    |
    |       |   `a` varchar(10) DEFAULT NULL                        |
    |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
    +-------+-------------------------------------------------------+
    1 row in set
    Time: 0.006s
    ```

- 升级后：v2.1.1、v2.1.2 会出现下面的问题，v2.1.3 以及之后版本不会出现下面的问题。

    ```sql
    tidb > alter table t change column a a varchar(20);
    ERROR 1105 (HY000): unsupported modify column charset utf8mb4 not match origin utf8
    ```

解决方案：显式指定 column charset，保持和原来的 charset 一致即可。

```sql
alter table t change column a a varchar(22) character set utf8;
```

- 根据要点 1，此处如果不指定 column 的 charset，会用默认的 UTF8MB4，所以需要指定 column charset 保持和原来一致。

- 根据要点 2，用 HTTP API 获取 table 元信息，然后根据 column 名字和 Charset 关键字搜索即可找到 column 的 charset。

    ```sh
    ▶ curl "http://$IP:10080/schema/test/t" | python -m json.tool  # 这里用了 python 的格式化 json的工具，也可以不加，此处只是为了方便注释。
    {
        "ShardRowIDBits": 0,
        "auto_inc_id": 0,
        "charset": "utf8",   # table 的 charset
        "collate": "",
        "cols": [            # 从这里开始列举 column 的相关信息
            {
                ...
                "id": 1,
                "name": {
                    "L": "a",
                    "O": "a"   # column 的名字
                },
                "offset": 0,
                "origin_default": null,
                "state": 5,
                "type": {
                    "Charset": "utf8",   # column a 的 charset
                    "Collate": "utf8_bin",
                    "Decimal": 0,
                    "Elems": null,
                    "Flag": 0,
                    "Flen": 10,
                    "Tp": 15
                }
            }
        ],
        ...
    }
    ```

### 问题 2：`unsupported modify charset from utf8mb4 to utf8`

- 升级前：v2.1.1，v2.1.2

    ```sql
    tidb > create table t(a varchar(10)) charset=utf8;
    Query OK, 0 rows affected
    Time: 0.109s
    tidb > show create table t
    +-------+-------------------------------------------------------+
    | Table | Create Table                                          |
    +-------+-------------------------------------------------------+
    | t     | CREATE TABLE `t` (                                    |
    |       |   `a` varchar(10) DEFAULT NULL                        |
    |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin |
    +-------+-------------------------------------------------------+
    ```

    上面 `show create table` 只显示出了 table 的 charset，但其实 column 的 charset 是 UTF8MB4，这可以通过 HTTP API 获取 schema 来确认。这是一个 bug，即此处建表时 column 的 charset 应该要和 table 保持一致为 UTF8，该问题在 v2.1.3 中已经修复。

- 升级后：v2.1.3 及之后版本

    ```sql
    tidb > show create table t
    +-------+--------------------------------------------------------------------+
    | Table | Create Table                                                       |
    +-------+--------------------------------------------------------------------+
    | t     | CREATE TABLE `t` (                                                 |
    |       |   `a` varchar(10) CHARSET utf8mb4 COLLATE utf8mb4_bin DEFAULT NULL |
    |       | ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin              |
    +-------+--------------------------------------------------------------------+
    1 row in set
    Time: 0.007s
    tidb > alter table t change column a a varchar(20);
    ERROR 1105 (HY000): unsupported modify charset from utf8mb4 to utf8
    ```

解决方案：

- 因为在 v2.1.3 之后，TiDB 支持修改 column 和 table 的 charset，所以这里推荐修改 table 的 charset 为 UTF8MB4。

    ```sql
    alter table t convert to character set utf8mb4;
    ```

- 也可以像问题 1 一样指定 column 的 charset，保持和 column 原来的 charset (UTF8MB4) 一致即可。

    ```sql
    alter table t change column a a varchar(20) character set utf8mb4;
    ```

### 问题 3：`ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a`

TiDB 在 v2.1.1 及之前版本中，如果 charset 是 UTF8，没有对 4-byte 的插入数据进行 UTF8 Unicode encoding 检查。在v2.1.2 及之后版本中，添加了该检查。

- 升级前：v2.1.1 及之前版本

    ```sql
    tidb> create table t(a varchar(100) charset utf8);
    Query OK, 0 rows affected
    tidb> insert t values (unhex('f09f8c80'));
    Query OK, 1 row affected
    ```

- 升级后：v2.1.2 及之后版本

    ```sql
    tidb> insert t values (unhex('f09f8c80'));
    ERROR 1366 (HY000): incorrect utf8 value f09f8c80(🌀) for column a
    ```

解决方案：

- v2.1.2 版本：该版本不支持修改 column charset，所以只能跳过 UTF8 的检查。

    ```sql
    tidb > set @@session.tidb_skip_utf8_check=1;
    Query OK, 0 rows affected
    tidb > insert t values (unhex('f09f8c80'));
    Query OK, 1 row affected
    ```

- v2.1.3 及之后版本：建议修改 column 的 charset 为 UTF8MB4。或者也可以设置 `tidb_skip_utf8_check` 变量跳过 UTF8 的检查。如果跳过 UTF8 的检查，在需要将数据从 TiDB 同步回 MySQL 的时候，可能会失败，因为 MySQL 会执行该检查。

    ```sql
    tidb > alter table t change column a a varchar(100) character set utf8mb4;
    Query OK, 0 rows affected
    tidb > insert t values (unhex('f09f8c80'));
    Query OK, 1 row affected
    ```

    关于 `tidb_skip_utf8_check` 变量，具体来说是指跳过 UTF8 和 UTF8MB4 类型对数据的合法性检查。如果跳过这个检查，在需要将数据从 TiDB 同步回 MySQL 的时候，可能会失败，因为 MySQL 执行该检查。如果只想跳过 UTF8 类型的检查，可以设置 `tidb_check_mb4_value_in_utf8` 变量。

    `tidb_check_mb4_value_in_utf8` 在 v2.1.3 版本加入 `config.toml` 文件，可以修改配置文件里面的 `check-mb4-value-in-utf8` 后重启集群生效。

    `tidb_check_mb4_value_in_utf8` 在 v2.1.5 版本开始可以用 HTTP API 来设置，也可以用 session 变量来设置。

    * HTTP API（HTTP API 只在单台服务器上生效）

        ```sh
        # Enabled.
        curl -X POST -d "check_mb4_value_in_utf8=1" http://{TiDBIP}:10080/settings

        # Disabled.
        curl -X POST -d "check_mb4_value_in_utf8=0" http://{TiDBIP}:10080/settings
        ```

    * Session 变量

        ```sql
        # Enabled.
        set @@session.tidb_check_mb4_value_in_utf8 = 1;

        # Disabled.
        set @@session.tidb_check_mb4_value_in_utf8 = 0;
        ```
