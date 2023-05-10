---
title: GBK
summary: 本文介绍 TiDB 对 GBK 字符集的支持情况。
---

# GBK

TiDB 从 v5.4.0 开始支持 GBK 字符集。本文档介绍 TiDB 对 GBK 字符集的支持和兼容情况。

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

## 与 MySQL 的兼容性

本节介绍 TiDB 中 GBK 字符集与 MySQL 的兼容情况。

### 排序规则兼容性

MySQL 的字符集默认排序规则是 `gbk_chinese_ci`。与 MySQL 不同，TiDB GBK 字符集的默认排序规则为 `gbk_bin`。另外，TiDB 支持的 `gbk_bin` 与 MySQL 支持的 `gbk_bin` 排序规则也不一致，TiDB 是将 GBK 转换成 UTF8MB4 然后做二进制排序。

如果要使 TiDB 兼容 MySQL 的 GBK 字符集排序规则，你需要在初次初始化 TiDB 集群时设置 TiDB 配置项[`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 为 `true` 来开启[新的排序规则框架](/character-set-and-collation.md#新框架下的排序规则支持)。

开启新的排序规则框架后，如果查看 GBK 字符集对应的排序规则，你可以看到 TiDB GBK 默认排序规则已经切换为 `gbk_chinese_ci`。

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

### 非法字符兼容性

* 在系统变量 [`character_set_client`](/system-variables.md#character_set_client) 和 [`character_set_connection`](/system-variables.md#character_set_connection) 不同时设置为 `gbk` 的情况下，TiDB 处理非法字符的方式与 MySQL 一致。
* 在 `character_set_client` 和 `character_set_connection` 同时为 `gbk` 的情况下，TiDB 处理非法字符的方式与 MySQL 有所区别。

    - MySQL 处理非法 GBK 字符集时，对读和写操作的处理方式不同。
    - TiDB 处理非法 GBK 字符集时，对读和写操作的处理方式相同。TiDB 在严格模式下读写非法 GBK 字符都会报错，在非严格模式下，读写非法 GBK 字符都会用 `?` 替换。

例如，当 `SET NAMES gbk` 时，如果分别在 MySQL 和 TiDB 上通过 `CREATE TABLE gbk_table(a VARCHAR(32) CHARACTER SET gbk)` 语句建表，然后按照下表中的 SQL 语句进行操作，就能看到具体的区别。

| 数据库    |    如果设置的 SQL 模式包含 `STRICT_ALL_TABLES` 或 `STRICT_TRANS_TABLES`                                               | 如果设置的 SQL 模式不包含 `STRICT_ALL_TABLES` 和  `STRICT_TRANS_TABLES`                                                                     |
|-------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| MySQL | `SELECT HEX('一a');` <br /> `e4b88061`<br /><br />`INSERT INTO gbk_table values('一a');`<br /> `Incorrect Error`       | `SELECT HEX('一a');` <br /> `e4b88061`<br /><br />`INSERT INTO gbk_table VALUES('一a');`<br />`SELECT HEX(a) FROM gbk_table;`<br /> `e4b8` |
| TiDB  | `SELECT HEX('一a');` <br /> `Incorrect Error`<br /><br />`INSERT INTO gbk_table VALUES('一a');`<br /> `Incorrect Error` | `SELECT HEX('一a');` <br /> `e4b83f`<br /><br />`INSERT INTO gbk_table VALUES('一a');`<br />`SELECT HEX(a) FROM gbk_table;`<br /> `e4b83f`  |

说明：该表中 `SELECT HEX('一a');` 在 `utf8mb4` 字节集下的结果为 `e4b88061`。

### 其它

* 目前 TiDB 不支持通过 `ALTER TABLE` 语句将其它字符集类型改成 `gbk` 或者从 `gbk` 转成其它字符集类型。

* TiDB 不支持使用 `_gbk`，比如：

  ```sql
  CREATE TABLE t(a CHAR(10) CHARSET BINARY);
  Query OK, 0 rows affected (0.00 sec)
  INSERT INTO t VALUES (_gbk'啊');
  ERROR 1115 (42000): Unsupported character introducer: 'gbk'
  ```

* 对于 `ENUM` 和 `SET` 类型中的二进制字符，TiDB 目前都会将其作为 `utf8mb4` 字符集处理。

## 组件兼容性

* TiFlash 目前不支持 GBK 字符集。

* TiDB Data Migration (DM) 在 v5.4.0 之前不支持将 `charset=GBK` 的表迁移到 TiDB。

* TiDB Lightning 在 v5.4.0 之前不支持导入 `charset=GBK` 的表。

* TiCDC 在 v6.1.0 之前不支持同步 `charset=GBK` 的表。另外，任何版本的 TiCDC 都不支持同步 `charset=GBK` 的表到 6.1.0 之前的 TiDB 集群。

* TiDB Backup & Restore（BR）在 v5.4.0 之前不支持恢复 `charset=GBK` 的表。另外，任何版本的 BR 都不支持恢复 `charset=GBK` 的表到 5.4.0 之前的 TiDB 集群。