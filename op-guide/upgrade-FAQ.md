---
title: 升级后常见问题与解答(upgrade FAQ)
category: deployment
---

# 升级后常见问题与解答(upgrade FAQ)

本文列出了一些升级后的可能会遇到的问题。

## 执行 DDL 时遇到的字符集（charset）问题

TiDB 在 v2.1.0 以及之前（包括 v2.0 所有版本）默认字符集是 UTF8，从 v2.1.1 开始，默认字符集变更为 UTF8MB4。如果在 v2.1.0 之前建表时显式指定了 table 的 charset 为 UTF8，那后升级到 v2.1.1 之后，执行 DDL 变更可能会失败。

记住下面 2 个要点：

1. 在 v2.1.3 之前，不支持修改 column 的 charset。所以需要做 DDL 时需要新 column 的 charset 和 旧 column 的保持一致。

2. v2.1.3 之前，`show create table` 不会显示 column 的 charset，即使 column 的 charset 和 table 的 charset 不一样。可以通过 http  api 拿 table 的元信息查看 column 的 charset，下面会有示例。

### 问题1: unsupported modify column charset utf8mb4 not match origin utf8

升级前：v2.1.0 以及之前

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

升级后： v2.1.1,  v2.1.2（v2.1.3 以及之后不会出现下面的问题）

```SQL
tidb > alter table t change column a a varchar(20);
ERROR 1105 (HY000): unsupported modify column charset utf8mb4 not match origin utf8
```

解决方案：显式指定 column charset，保持和原来的 charset 一致即可。

```SQL
alter table t change column a a varchar(22) character set utf8;
```

根据要点 1 , 此处如果不指定 column 的charset，会用默认的 UTF8MB4 ，所以需要指定 column charset 保持和原来一致。

根据要点 2，用 http api 获取 table 元信息，然后根据 column 名字和 Charset 关键字搜索即可找到 column 的 charset。

```shell
▶ curl "http://$IP:10080/schema/test/t" | python -m json.tool  # 这里用了 python 的格式化 json的工具，也可以不加，此处只是为了方便注释。
{
    "ShardRowIDBits": 0,
    "auto_inc_id": 0,
    "charset": "utf8",   # 这是 table 的 charset
    "collate": "",
    "cols": [			 # 从这里开始列举 column 的相关信息
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

### 问题2 : unsupported modify charset from utf8mb4 to utf8

升级前：v2.1.1, v2.1.2

```SQL
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

上面 `show create table` 只 show 出了 table 的 charset，但其实 column 的 charset 是 UTF8MB4，这可以用 http api 获取 schema 来确认。 这是一个 bug，即此处建表时 column 的 charset 应该要和 table 保持一致为 UTF8，这个问题在  v2.1.3 后已经修复。

升级后：v2.1.3 以及之后

```SQL
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

因为 v2.1.3 之后支持修改 column 和  table 的 charset 了，所以这里推荐修改 table 的 charset 为 UTF8MB4。

```SQL
alter table t convert to character set utf8mb4;
```

也可以像问题 1 一样指定 column 的 charset，保持和 column 原来的 charset  UTF8MB4 一致即可。

```SQL
alter table t change column a a varchar(20) character set utf8mb4;
```

