---
title: GBK 字符集
---

# GBK 字符集

本文档介绍 TiDB 对 GBK 字符集的支持情况。

目前 TiDB 支持 GBK 字符集和排序规则情况：
```sql
SHOW CHARACTER SET WHERE CHARSET = 'gbk';;
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| gbk     | Chinese Internal Code Specification | gbk_bin           |      2 |
+---------+-------------------------------------+-------------------+--------+
1 row in set (0.00 sec)


SHOW COLLATION WHERE CHARSET = 'gbk';
+----------------+---------+------+---------+----------+---------+
| Collation      | Charset | Id   | Default | Compiled | Sortlen |
+----------------+---------+------+---------+----------+---------+
| gbk_bin        | gbk     |   87 |         | Yes      |       1 |
+----------------+---------+------+---------+----------+---------+
2 rows in set (0.00 sec)
```
TiDB GBK 字符集默认排序规则与 MySQL 不一致，MySQL 的是 `gbk_chinese_ci`. 另外，目前 TiDB 支持的 `gbk_bin` 与 MySQL 使用的也不一致。TiDB 这边排序规则是在将 GBK 转换成 UTF8MB4 然后做二进制排序。
如果需要兼容 MySQL 的排序规则，需要使用[新的排序规则框架](/character-set-and-collation.md#新框架下的排序规则支持)。

利用以下的语句可以查看字符集对应的排序规则（以下是[新的排序规则框架](/character-set-and-collation.md#新框架下的排序规则支持)）下的结果：

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gbk';;
+---------+-------------------------------------+-------------------+--------+
| Charset | Description                         | Default collation | Maxlen |
+---------+-------------------------------------+-------------------+--------+
| gbk     | Chinese Internal Code Specification | gbk_chinese_ci    |      2 |
+---------+-------------------------------------+-------------------+--------+
1 row in set (0.00 sec)

SHOW COLLATION WHERE CHARSET = 'gbk';
+----------------+---------+------+---------+----------+---------+
| Collation      | Charset | Id   | Default | Compiled | Sortlen |
+----------------+---------+------+---------+----------+---------+
| gbk_bin        | gbk     |   87 |         | Yes      |       1 |
| gbk_chinese_ci | gbk     |   28 | Yes     | Yes      |       1 |
+----------------+---------+------+---------+----------+---------+
2 rows in set (0.00 sec)
```

## MySQL 兼容性

### 非法字符兼容性

* 在设置成 `character_set_client = gbk`、`character_set_connection = utf8mb4` 和 `character_set_table = gbk` 的情况下，TiDB 处理非法字符的情况与 MySQL 兼容。
* 当设置 `names` 为 `gbk` 后 TiDB 处理非法字符的情况与 MySQL 有一些不一样。具体行为如下（其中 `insert` 语句所在表的建表语句：`create table gbk_table(a varchar(32) character set gbk);`）：

|   DB    |    SQL_Mode          |   (Compatible)                       |   (Imcompatible)                     |
|---------|----------------------|--------------------------------------|--------------------------------------|
|         |                      |   character_set_client = gbk <br>    |   character_set_client = gbk         |
|    /    |          /           |   character_set_connection = utf8mb4 |   character_set_connection = gbk     |
|         |                      |   character_set_table = gbk          |   character_set_client = gbk         |
|         |                      |   (Compatible)                       |   (Imcompatible)                     |
|---------|----------------------|--------------------------------------|--------------------------------------|
| MySQL   | STRICT_ALL_TABLES or | select hex('一a') (0xe4b88061)       | select hex('一a') (0xe4b88061)        |
|         | STRICT_TRANS_TABLES  | e6b6933f                             | e4b88061                             |
|         |                      |                                      |                                      |
|         |                      | insert into gbk_table values('一a'); | insert into gbk_table values('一a');  |
|         |                      | select hex(a) from gbk_table;        | Incorrect Error                      |
|         |                      | e4b83f                               |                                      |
|---------|----------------------|--------------------------------------|--------------------------------------|
| TiDB    | STRICT_ALL_TABLES or | select hex('一a') (0xe4b88061)       | select hex('一a') (0xe4b88061)        |
|         | STRICT_TRANS_TABLES  | e6b6933f                             | Incorrect Error                      |
|         |                      |                                      |                                      |
|         |                      | insert into gbk_table values('一a'); | insert into gbk_table values('一a');  |
|         |                      | select hex(a) from gbk_table;        | Incorrect Error                      |
|         |                      | e4b83f                               |                                      |
|---------|----------------------|--------------------------------------|--------------------------------------|
| MySQL   | not include          | select hex('一a') (0xe4b88061)       | select hex('一a') (0xe4b88061)        |
|         | STRICT_ALL_TABLES or | e6b6933f                             | e4b88061                             |
|         | STRICT_TRANS_TABLES  |                                      |                                      |
|         |                      | insert into gbk_table values('一a'); | insert into gbk_table values('一a');  |
|         |                      | select hex(a) from gbk_table;        | select hex(a) from gbk_table;        |
|         |                      | e4b83f                               | e4b8                                 |
|---------|----------------------|--------------------------------------|--------------------------------------|
| TiDB    | not include          | select hex('一a') (0xe4b88061)       | select hex('一a') (0xe4b88061)        |
|         | STRICT_ALL_TABLES or | e6b6933f                             | e4b83f                               |
|         | STRICT_TRANS_TABLES  |                                      |                                      |
|         |                      | insert into gbk_table values('一a'); | insert into gbk_table values('一a');  |
|         |                      | select hex(a) from gbk_table;        | select hex(a) from gbk_table;        |
|         |                      | e4b83f                               | e4b83f                               |



### 其它

* 目前不支持通过 `alter table` 语句变更字符集类型。

* 不支持使用 `_gbk`， 比如：

  ```sql
  create table t(a char(10) charset binary);
  Query OK, 0 rows affected (0.00 sec)
  insert into t values (_gbk'啊');
  ERROR 1115 (42000): Unsupported character introducer: 'gbk'
  ```

