---
title: GBK
summary: 本文档提供了 TiDB 对 GBK 字符集支持的详细信息。
---

# GBK

从 v5.4.0 版本开始，TiDB 支持 GBK 字符集。本文档提供了 TiDB 对 GBK 字符集的支持和兼容性信息。

从 v6.0.0 版本开始，TiDB 默认启用[新的排序规则框架](/character-set-and-collation.md#new-framework-for-collations)。TiDB GBK 字符集的默认排序规则是 `gbk_chinese_ci`，这与 MySQL 保持一致。

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

本节提供 MySQL 和 TiDB 之间的兼容性信息。

### 排序规则

<CustomContent platform="tidb">

MySQL 中 GBK 字符集的默认排序规则是 `gbk_chinese_ci`。TiDB 中 GBK 字符集的默认排序规则取决于 TiDB 配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 的值：

- 默认情况下，TiDB 配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 设置为 `true`，这意味着启用了[新的排序规则框架](/character-set-and-collation.md#new-framework-for-collations)，GBK 字符集的默认排序规则是 `gbk_chinese_ci`。
- 当 TiDB 配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 设置为 `false` 时，[新的排序规则框架](/character-set-and-collation.md#new-framework-for-collations)被禁用，GBK 字符集的默认排序规则是 `gbk_bin`。

</CustomContent>

<CustomContent platform="tidb-cloud">

默认情况下，TiDB Cloud 启用[新的排序规则框架](/character-set-and-collation.md#new-framework-for-collations)，GBK 字符集的默认排序规则是 `gbk_chinese_ci`。

</CustomContent>

此外，由于 TiDB 将 GBK 转换为 `utf8mb4` 后再使用二进制排序规则，因此 TiDB 中的 `gbk_bin` 排序规则与 MySQL 中的 `gbk_bin` 排序规则不同。

### 非法字符兼容性

* 如果系统变量 [`character_set_client`](/system-variables.md#character_set_client) 和 [`character_set_connection`](/system-variables.md#character_set_connection) 没有同时设置为 `gbk`，TiDB 处理非法字符的方式与 MySQL 相同。
* 如果 `character_set_client` 和 `character_set_connection` 都设置为 `gbk`，TiDB 处理非法字符的方式与 MySQL 不同。

    - MySQL 对读写操作中的非法 GBK 字符集处理方式不同。
    - TiDB 对读写操作中的非法 GBK 字符集处理方式相同。在 SQL 严格模式下，TiDB 在读写非法 GBK 字符时都会报错。在非严格模式下，TiDB 在读写非法 GBK 字符时都会将非法 GBK 字符替换为 `?`。

例如，在执行 `SET NAMES gbk` 后，如果您分别在 MySQL 和 TiDB 中使用 `CREATE TABLE gbk_table(a VARCHAR(32) CHARACTER SET gbk)` 语句创建表，然后执行下表中的 SQL 语句，您可以看到详细的差异。

| 数据库    | 如果配置的 SQL 模式包含 `STRICT_ALL_TABLES` 或 `STRICT_TRANS_TABLES` 中的任一个                                               | 如果配置的 SQL 模式既不包含 `STRICT_ALL_TABLES` 也不包含 `STRICT_TRANS_TABLES`                                                                     |
|-------|-------------------------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------|
| MySQL | `SELECT HEX('一a');` <br /> `e4b88061`<br /><br />`INSERT INTO gbk_table values('一a');`<br /> `Incorrect Error`       | `SELECT HEX('一a');` <br /> `e4b88061`<br /><br />`INSERT INTO gbk_table VALUES('一a');`<br />`SELECT HEX(a) FROM gbk_table;`<br /> `e4b8` |
| TiDB  | `SELECT HEX('一a');` <br /> `Incorrect Error`<br /><br />`INSERT INTO gbk_table VALUES('一a');`<br /> `Incorrect Error` | `SELECT HEX('一a');` <br /> `e4b83f`<br /><br />`INSERT INTO gbk_table VALUES('一a');`<br />`SELECT HEX(a) FROM gbk_table;`<br /> `e4b83f`  |

在上表中，在 `utf8mb4` 字节集中 `SELECT HEX('a');` 的结果是 `e4b88061`。

### 其他 MySQL 兼容性

- 目前，TiDB 不支持使用 `ALTER TABLE` 语句将其他字符集类型转换为 `gbk` 或从 `gbk` 转换为其他字符集类型。

* TiDB 不支持使用 `_gbk`。例如：

  ```sql
  CREATE TABLE t(a CHAR(10) CHARSET BINARY);
  Query OK, 0 rows affected (0.00 sec)
  INSERT INTO t VALUES (_gbk'啊');
  ERROR 1115 (42000): Unsupported character introducer: 'gbk'
  ```

- 目前，对于 `ENUM` 和 `SET` 类型的二进制字符，TiDB 将其作为 `utf8mb4` 字符集处理。

## 组件兼容性

- 目前，TiFlash 不支持 GBK 字符集。

- TiDB Data Migration (DM) 不支持将 `charset=GBK` 的表迁移到 v5.4.0 之前的 TiDB 集群。

- TiDB Lightning 不支持将 `charset=GBK` 的表导入到 v5.4.0 之前的 TiDB 集群。

- v6.1.0 之前的 TiCDC 版本不支持复制 `charset=GBK` 的表。所有版本的 TiCDC 都不支持将 `charset=GBK` 的表复制到 v6.1.0 之前的 TiDB 集群。

- v5.4.0 之前的 Backup & Restore (BR) 版本不支持恢复 `charset=GBK` 的表。所有版本的 BR 都不支持将 `charset=GBK` 的表恢复到 v5.4.0 之前的 TiDB 集群。
