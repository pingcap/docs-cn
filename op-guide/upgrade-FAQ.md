---
title: 升级后常见 FAQ
category: deployment
---

# 升级后常见 FAQ

本文列出了一些升级后的可能会遇到的问题。

1. 字符集（charset）问题1: unsupported modify column charset utf8mb4 not match origin utf8

    TiDB 在 v2.1.0 以及之前（包括v2.0 所有版本）默认字符集是 utf8，从 v2.1.1 开始，默认字符集变更为 utf8mb4。如果在 v2.1.0 之前建表时显式指定了 table 的 charset 为 utf8，那后升级到 v2.1.1 之后，执行 DDL 变更可能会失败。示例如下：

    v2.1.0 and before v2.1.0

    ```SQL
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

    after v2.1.0, before v2.1.3

    ```SQL
    tidb > use test
    You are now connected to database "test" as user "root"
    Time: 0.000s
    tidb > alter table t change column a a varchar(20);
    (1105, u'unsupported modify column charset utf8mb4 not match origin utf8')
    ```

    解决方案：显式指定 column charset，保持和原来的 charset 一致即可。

    ```sql
    alter table t change column a a varchar(22) character set utf8;
    ```

    v2.1.3 之前不支持修改column 的charset , 所以需要指定column charset 保持和原来一致。v2.1.3 之前，`show create table` 不会显示 column 的 charset，即使 column 的 charset 和 table 的 charset 不一样。只能通过 http  api 拿table 的元信息查看 column 的 schema。然后根据 column 名字和 Charset 关键字搜索即可找到

    ```shell
    ▶ curl "http://$IP:10080/schema/test/t"
    {
        "ShardRowIDBits": 0,
        "auto_inc_id": 0,
        "charset": "utf8",
        "collate": "",
        "cols": [
            {
                ...
                "id": 1,
                "name": {
                    "L": "a",
                    "O": "a"
                },
                "offset": 0,
                "origin_default": null,
                "state": 5,
                "type": {
                    "Charset": "utf8",
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

2. 字符集（charset）问题2 : unsupported modify charset from utf8mb4 to utf8

   v2.1.1

   ```sql
   tidb > create table t(a varchar(10)) charset=utf8;
   Query OK, 0 rows affected
   Time: 0.109s
   ```

   v2.1.3

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
   (1105, u'unsupported modify charset from utf8mb4 to utf8')
   ```

   因为v2.1.3 之后支持修改column 和  table 的 charset 了，所以这里推荐修改table 的charset 为 utf8mb4。

   ```
   alter table t convert to character set utf8mb4;
   ```

   也可以像问题1一样指定 charset。

   ```sql
   alter table t change column a a varchar(20) character set utf8mb4;
   ```

   
