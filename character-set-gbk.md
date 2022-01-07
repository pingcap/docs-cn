---
title: GBK
summary: 本文介绍 TiDB 对 GBK 字符集的支持情况。
---

# GBK

本文档介绍 TiDB 对 GBK 字符集的支持和兼容性情况。

从 TiDB v5.4.0 起，TiDB 支持 GBK 字符集。
```sql
SHOW CHARACTER SET WHERE CHARSET = 'gbk';
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
1 rows in set (0.00 sec)
```
TiDB GBK 字符集默认排序规则与 MySQL 不一致，TiDB GBK 字符集的默认排序规则为 `gbk_bin`，MySQL 的字符集默认排序规则是 `gbk_chinese_ci`。 另外，目前 TiDB 支持的 `gbk_bin` 与 MySQL 支持的 `gbk_bin` 也不一致，TiDB 是将 GBK 转换成 UTF8MB4 然后做二进制排序。

如果要兼容 MySQL 的 GBK 字符集排序规则，你需要在初次初始化集群时通过设置 TiDB 配置项[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 为 `true`来开启[新的排序规则框架](/character-set-and-collation.md#新框架下的排序规则支持)。

开启新的排序规则框架后，你可以通过以下 SQL 语句查看 GBK 字符集对应的排序规则：

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gbk';
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

* 在 `character_set_client` 和 `character_set_connection` 不同时为 `gbk` 的情况下，TiDB 处理非法字符的方式与 MySQL 一致。
* 在 `character_set_client` 和 `character_set_connection` 同时为 `gbk` 的情况下， TiDB 处理非法字符的方式与 MySQL 有所区别。例如，以 `set names gbk` 为前提，具体行为如下（其中 `insert` 语句所在表的建表语句：`create table gbk_table(a varchar(32) character set gbk);`）：

| DB    |    sql_mode:<br><br>  STRICT_ALL_TABLES or<br>  STRICT_TRANS_TABLES                                               | sql_mode 不包括： <br><br>  STRICT_ALL_TABLES or<br>  STRICT_TRANS_TABLES                                                                     |
|-------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| MySQL | `select hex('一a');` (0xe4b88061)<br> e4b88061<br><br>`insert into gbk_table values('一a');`<br> Incorrect Error       | `select hex('一a');` (0xe4b88061)<br> e4b88061<br><br>`insert into gbk_table values('一a');`<br>`select hex(a) from gbk_table;`<br> e4b8 |
| TiDB  | `select hex('一a');` (0xe4b88061)<br> Incorrect Error<br><br>`insert into gbk_table values('一a');`<br> Incorrect Error | `select hex('一a');` (0xe4b88061)<br> e4b83f<br><br>`insert into gbk_table values('一a');`<br>`select hex(a) from gbk_table;`<br> e4b83f  |

### 其它

* 目前 TiDB 不支持通过 `ALTER TABLE` 语句将其它字符集类型改成 `gbk`，或者从 `gbk` 转成其它字符集类型。

* TiDB 不支持使用 `_gbk`， 比如：

  ```sql
  CREATE TABLE t(a CHAR(10) CHARSET BINARY);
  Query OK, 0 rows affected (0.00 sec)
  INSERT INTO t VALUES (_gbk'啊');
  ERROR 1115 (42000): Unsupported character introducer: 'gbk'
  ```

* 对于 `ENUM` 类型中的二进制字符，TiDB 目前都会将其作为 `utf8mb4` 字符集处理。

## 其他组件兼容性

* 目前不支持 GBK 字符集的组件包括：TiCDC 和 TiFlash。