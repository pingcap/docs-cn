---
title: GB18030
summary: 本文介绍 TiDB 对 GB18030 字符集的支持情况。
---

# GB18030

TiDB 从 v8.4.0 开始支持 GB18030 字符集。本文档介绍 TiDB 对 GB18030 字符集的支持和兼容情况。

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gb18030';
+---------+---------------------------------+--------------------+--------+
| Charset | Description                     | Default collation  | Maxlen |
+---------+---------------------------------+--------------------+--------+
| gb18030 | China National Standard GB18030 | gb18030_chinese_ci |      4 |
+---------+---------------------------------+--------------------+--------+
1 row in set (0.01 sec)

SHOW COLLATION WHERE CHARSET = 'gb18030';
+-------------+---------+-----+---------+----------+---------+---------------+
| Collation   | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+-------------+---------+-----+---------+----------+---------+---------------+
| gb18030_bin | gb18030 | 249 | Yes     | Yes      |       1 | PAD SPACE     |
+-------------+---------+-----+---------+----------+---------+---------------+
1 row in set (0.00 sec)
```

## 与 MySQL 的兼容性

本节介绍 TiDB 中 GB18030 字符集与 MySQL 的兼容情况。

### 排序规则兼容性

MySQL 的字符集默认排序规则是 `gb18030_chinese_ci`。与 MySQL 不同，TiDB GB18030 字符集的默认排序规则为 `gb18030_bin`。另外，TiDB 支持的 `gb18030_bin` 与 MySQL 支持的 `gb18030_bin` 排序规则也不一致，TiDB 是将 GB18030 转换成 UTF8MB4 然后做二进制排序。

如果要使 TiDB 兼容 MySQL 的 GB18030 字符集排序规则，你需要在初次初始化 TiDB 集群时设置 TiDB 配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 为 `true` 来开启[新的排序规则框架](/character-set-and-collation.md#新框架下的排序规则支持)。

开启新的排序规则框架后，如果查看 GB18030 字符集对应的排序规则，你可以看到 TiDB GB18030 默认排序规则已经切换为 `gb18030_chinese_ci`。

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gb18030';
+---------+---------------------------------+--------------------+--------+
| Charset | Description                     | Default collation  | Maxlen |
+---------+---------------------------------+--------------------+--------+
| gb18030 | China National Standard GB18030 | gb18030_chinese_ci |      4 |
+---------+---------------------------------+--------------------+--------+
1 row in set (0.01 sec)

SHOW COLLATION WHERE CHARSET = 'gb18030';
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| gb18030_bin        | gb18030 | 249 |         | Yes      |       1 | PAD SPACE     |
| gb18030_chinese_ci | gb18030 | 248 | Yes     | Yes      |       1 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
2 rows in set (0.00 sec)
```

### 非法字符兼容性

* 在系统变量 [`character_set_client`](/system-variables.md#character_set_client) 和 [`character_set_connection`](/system-variables.md#character_set_connection) 没有同时设置为 `gb18030` 的情况下，TiDB 处理非法字符的方式与 MySQL 一致。
* 在 `character_set_client` 和 `character_set_connection` 同时为 `gb18030` 的情况下，TiDB 处理非法字符的方式与 MySQL 有如下区别：

    - MySQL 处理非法 GB18030 字符集时，对读和写操作的处理方式不同。
    - TiDB 处理非法 GB18030 字符集时，对读和写操作的处理方式相同。TiDB 在严格模式下读写非法 GB18030 字符都会报错，在非严格模式下，读写非法 GB18030 字符都会用 `?` 替换。
