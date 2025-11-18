---
title: GB18030 字符集
summary: 本文介绍 TiDB 对 GB18030 字符集的支持情况。
---

# GB18030 字符集

TiDB 从 v9.0.0 开始支持 GB18030-2022 字符集。本文档介绍 TiDB 对 GB18030 字符集的支持和兼容情况。

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gb18030';
```

```
+---------+---------------------------------+--------------------+--------+
| Charset | Description                     | Default collation  | Maxlen |
+---------+---------------------------------+--------------------+--------+
| gb18030 | China National Standard GB18030 | gb18030_chinese_ci |      4 |
+---------+---------------------------------+--------------------+--------+
1 row in set (0.01 sec)
```

```sql
SHOW COLLATION WHERE CHARSET = 'gb18030';
```

```
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| gb18030_bin        | gb18030 | 249 |         | Yes      |       1 | PAD SPACE     |
| gb18030_chinese_ci | gb18030 | 248 | Yes     | Yes      |       1 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
2 rows in set (0.001 sec)
```

## 与 MySQL 的兼容性

本节介绍 TiDB 中 GB18030 字符集与 MySQL 的兼容情况。

### 排序规则兼容性

MySQL 的 GB18030 字符集默认排序规则是 `gb18030_chinese_ci`。TiDB 的 GB18030 字符集的默认排序规则取决于 TiDB 配置项 [`new_collations_enabled_on_first_bootstrap`](/tidb-configuration-file.md#new_collations_enabled_on_first_bootstrap) 的值：

- 默认情况下，TiDB 配置项 `new_collations_enabled_on_first_bootstrap` 为 `true`，表示开启[新的排序规则框架](/character-set-and-collation.md#新框架下的排序规则支持)。此时，GB18030 字符集的默认排序规则是 `gb18030_chinese_ci`。
- 当 TiDB 配置项 `new_collations_enabled_on_first_bootstrap` 为 `false` 时，表示关闭新的排序规则框架，GB18030 字符集的默认排序规则是 `gb18030_bin`。

另外，TiDB 支持的 `gb18030_bin` 与 MySQL 支持的 `gb18030_bin` 排序规则也不一致，TiDB 是将 GB18030 转换成 `utf8mb4`，然后再进行二进制排序。

开启新的排序规则框架后，如果查看 GB18030 字符集对应的排序规则，你可以看到 TiDB GB18030 默认排序规则已经切换为 `gb18030_chinese_ci`：

```sql
SHOW CHARACTER SET WHERE CHARSET = 'gb18030';
```

```
+---------+---------------------------------+--------------------+--------+
| Charset | Description                     | Default collation  | Maxlen |
+---------+---------------------------------+--------------------+--------+
| gb18030 | China National Standard GB18030 | gb18030_chinese_ci |      4 |
+---------+---------------------------------+--------------------+--------+
1 row in set (0.01 sec)
```

```sql
SHOW COLLATION WHERE CHARSET = 'gb18030';
```

```
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| gb18030_bin        | gb18030 | 249 |         | Yes      |       1 | PAD SPACE     |
| gb18030_chinese_ci | gb18030 | 248 | Yes     | Yes      |       1 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
2 rows in set (0.00 sec)
```

### 字符兼容性

- TiDB 支持 GB18030-2022 的字符，MySQL 支持 GB18030-2005 的字符，因此部分字符的编解码结果不同。

- 对于非法的 GB18030 字符，比如 `0xFE39FE39`，MySQL 支持以 16 进制的方式写入数据库中，并保存为 `?`。TiDB 在严格模式下读写非法 GB18030 字符都会报错；在非严格模式下，TiDB 允许读写非法 GB18030 字符但会返回警告。

### 其它

* 目前 TiDB 不支持通过 `ALTER TABLE` 语句将其它字符集类型改成 `gb18030` 或者从 `gb18030` 转成其它字符集类型。

* TiDB 不支持使用 `_gb18030` 字符集引导符。例如：

    ```sql
    CREATE TABLE t(a CHAR(10) CHARSET BINARY);
    Query OK, 0 rows affected (0.00 sec)
    INSERT INTO t VALUES (_gb18030'啊');
    ERROR 1115 (42000): Unsupported character introducer: 'gb18030'
    ```

* 对于 `ENUM` 和 `SET` 类型中的二进制字符，TiDB 目前都会将其作为 `utf8mb4` 字符集处理。

## 组件兼容性

* TiFlash、TiDB Data Migration (DM) 和 TiCDC 目前不支持 GB18030 字符集。

* 在 v9.0.0 之前，Dumpling 不支持导出 `charset=GB18030` 的表，TiDB Lightning 不支持导入 `charset=GB18030` 的表。

* 在 v9.0.0 之前，TiDB Backup & Restore（BR）不支持备份恢复 `charset=GB18030` 的表。另外，任何版本的 BR 都不支持恢复 `charset=GB18030` 的表到 v9.0.0 之前的 TiDB 集群。

## 另请参阅

* [`SHOW CHARACTER SET`](/sql-statements/sql-statement-show-character-set.md)
* [字符集和排序规则](/character-set-and-collation.md)
