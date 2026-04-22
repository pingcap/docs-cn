---
title: 从 MariaDB 文件迁移数据到 TiDB
summary: 介绍如何将数据从 MariaDB 文件迁移数据到 TiDB。
---

# 从 MariaDB 文件迁移数据到 TiDB

本文档介绍了如何将数据从 MariaDB 服务器迁移到 TiDB 集群。

## 前提条件

选择合适的迁移策略：

- 第一种策略是[使用 Dumpling 导出数据然后使用 TiDB Lightning 恢复](#使用-dumpling-导出数据后使用-tidb-lightning-导入)。该策略适用于所有版本的 MariaDB，但缺点是需要更长的停机时间。
- 第二种策略是[使用 DM 迁移数据](#使用-dm-迁移数据)从 MariaDB 到 TiDB。注意 DM 不支持所有版本的 MariaDB。支持的版本请参考 [DM 兼容性目录](/dm/dm-compatibility-catalog.md#tidb-data-migration-兼容性目录)。

除了以上两种策略，还有其他策略适用于特定的场景，例如：

- 使用 Object Relational Mapping (ORM) 工具重新部署和迁移数据。
- 修改应用程序，使其在迁移过程中同时写入 MariaDB 和 TiDB。

本文档仅介绍前两种策略。

根据你选择的策略，准备以下内容：

- 对于第一种策略：
    - 安装 [Dumpling](/dumpling-overview.md) 和 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)。
    - 确保你在 MariaDB 服务器上拥有[所需的权限](/dumpling-overview.md#需要的权限)，以便 Dumpling 导出数据。
- 对于第二种策略，设置 [DM](/dm/dm-overview.md)。

## 检查兼容性

TiDB 和 [MySQL 兼容](/mysql-compatibility.md)，而 MySQL 和 MariaDB 也有很多通用的特性。在迁移数据前需要注意，可能某些 MariaDB 特有的特性和 TiDB 并不兼容。

除了检查本小节介绍的事项之外，建议你参考 [MariaDB Compatibility and Differences](https://mariadb.com/docs/release-notes/community-server/about/compatibility-and-differences) 检查相关配置。

### 认证

[与 MySQL 安全特性差异](/security-compatibility-with-mysql.md)文档列举了 TiDB 支持的认证方式。TiDB 不支持 MariaDB 中的某些认证方式，你可能需要为账号创建新的密码哈希，或采取其他相应措施。

你可以执行以下语句检查使用的认证方式：

```sql
SELECT
  plugin,
  COUNT(*)
FROM
  mysql.user
GROUP BY
  plugin;
```

```sql
+-----------------------+----------+
| plugin                | COUNT(*) |
+-----------------------+----------+
| mysql_native_password |       11 |
+-----------------------+----------+
1 row in set (0.002 sec)
```

### 系统版本表

TiDB 不支持[系统版本表 (System-Versioned Table)](https://mariadb.com/docs/server/reference/sql-structure/temporal-tables/system-versioned-tables)。但是 TiDB 支持 [`AS OF TIMESTAMP`](/as-of-timestamp.md)，可以在某些场景下取代系统版本表。

你可以执行下列语句检查受影响的表：

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SYSTEM VERSIONED';
```

```sql
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | t          |
+--------------+------------+
1 row in set (0.005 sec)
```

要删除 `SYSTEM VERSIONING`，执行 `ALTER TABLE` 语句：

```sql
MariaDB [test]> ALTER TABLE t DROP SYSTEM VERSIONING;
Query OK, 0 rows affected (0.071 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

### 序列

MariaDB 和 TiDB 均支持 [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)，但是 DM 暂不支持。建议在迁移期间不要创建、修改或删除序列，尤其在迁移后要进行相关测试。

执行下列语句检查你是否在使用序列：

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SEQUENCE';
```

```sql
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | s1         |
+--------------+------------+
1 row in set (0.016 sec)
```

### 存储引擎

MariaDB 为本地数据提供了存储引擎，例如 `InnoDB`、`MyISAM` 和 `Aria`。虽然 TiDB 不直接支持这些数据格式，但是你仍可以迁移这些数据。但是，也有一些存储引擎将数据放在服务器之外，例如 `CONNECT` 存储引擎和 `Spider`。虽然你可以将这些表迁移到 TiDB，但是 TiDB 无法将数据存储在 TiDB 集群外部。

执行下列语句检查你正在使用的存储引擎：

```sql
SELECT
  ENGINE,
  COUNT(*)
FROM
  information_schema.tables
GROUP BY
  ENGINE;
```

```sql
+--------------------+----------+
| ENGINE             | COUNT(*) |
+--------------------+----------+
| NULL               |      101 |
| Aria               |       38 |
| CSV                |        2 |
| InnoDB             |        6 |
| MEMORY             |       67 |
| MyISAM             |        1 |
| PERFORMANCE_SCHEMA |       81 |
+--------------------+----------+
7 rows in set (0.009 sec)
```

### 语法

MariaDB 支持 `DELETE`、`INSERT` 和 `REPLACE` 语句的 `RETURNING` 关键字。TiDB 不支持这些语句的关键字。你可能需要查看应用程序和查询日志，以检查它是否会影响数据迁移。

### 数据类型

MariaDB 支持的一些数据类型，例如 `UUID`、`INET4` 和 `INET6`，TiDB 并不支持。

执行下列语句检查你正在使用的数据类型：

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME,
  COLUMN_NAME,
  DATA_TYPE
FROM
  information_schema.columns
WHERE
  DATA_TYPE IN('INET4','INET6','UUID');
```

```sql
+--------------+------------+-------------+-----------+
| TABLE_SCHEMA | TABLE_NAME | COLUMN_NAME | DATA_TYPE |
+--------------+------------+-------------+-----------+
| test         | u1         | u           | uuid      |
| test         | u1         | i4          | inet4     |
| test         | u1         | i6          | inet6     |
+--------------+------------+-------------+-----------+
3 rows in set (0.026 sec)

```

### 字符集和排序规则

TiDB 不支持 MariaDB 中常用的 `latin1_swedish_ci` 排序规则。

TiDB 也不支持 `utf8mb4_uca1400_ai_ci`，该排序规则为 MariaDB 11.6 及之后版本默认使用的排序规则。请使用 `utf8mb4_0900_ai_ci`。这两个排序规则的区别在于所使用的 [Unicode Collation Algorithm (UCA)](http://www.unicode.org/reports/tr10/) 版本不同：`utf8mb4_0900_ai_ci` 使用的是 UCA 9.0.0，而 `utf8mb4_uca1400_ai_ci` 使用的是 UCA 14.0.0。

执行下列语句检查 TiDB 支持的排序规则：

```sql
SHOW COLLATION;
```

```sql
+--------------------+---------+-----+---------+----------+---------+---------------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen | Pad_attribute |
+--------------------+---------+-----+---------+----------+---------+---------------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 | PAD SPACE     |
| binary             | binary  |  63 | Yes     | Yes      |       1 | NO PAD        |
| gb18030_bin        | gb18030 | 249 |         | Yes      |       1 | PAD SPACE     |
| gb18030_chinese_ci | gb18030 | 248 | Yes     | Yes      |       1 | PAD SPACE     |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 | PAD SPACE     |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 | PAD SPACE     |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 | PAD SPACE     |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       8 | PAD SPACE     |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       0 | NO PAD        |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 | NO PAD        |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 | PAD SPACE     |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 | PAD SPACE     |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       8 | PAD SPACE     |
+--------------------+---------+-----+---------+----------+---------+---------------+
15 rows in set (0.000 sec)
```

执行下列语句检查当前表的列使用的排序规则：

```sql
SELECT
  TABLE_SCHEMA,
  COLLATION_NAME,
  COUNT(*)
FROM
  information_schema.columns
GROUP BY
  TABLE_SCHEMA, COLLATION_NAME
ORDER BY
  COLLATION_NAME;
```

```sql
+--------------------+--------------------+----------+
| TABLE_SCHEMA       | COLLATION_NAME     | COUNT(*) |
+--------------------+--------------------+----------+
| sys                | NULL               |      562 |
| test               | NULL               |       14 |
| mysql              | NULL               |       84 |
| performance_schema | NULL               |      892 |
| information_schema | NULL               |      421 |
| mysql              | latin1_swedish_ci  |       34 |
| performance_schema | utf8mb3_bin        |       38 |
| mysql              | utf8mb3_bin        |       61 |
| sys                | utf8mb3_bin        |       40 |
| information_schema | utf8mb3_general_ci |      375 |
| performance_schema | utf8mb3_general_ci |      244 |
| sys                | utf8mb3_general_ci |      386 |
| mysql              | utf8mb3_general_ci |       67 |
| mysql              | utf8mb4_bin        |        8 |
+--------------------+--------------------+----------+
14 rows in set (0.045 sec)
```

更多信息，请参考[字符集和排序规则](/character-set-and-collation.md)。

### 索引长度

如下例所示，如果索引超过最大键长度，MariaDB 会自动将其转换为前缀索引。TiDB 遵循 MySQL 的行为，不会执行这种自动转换，而是返回错误。因此，你需要修改脚本，在必要时显式创建前缀索引。

```
MariaDB> \W
Show warnings enabled.
MariaDB> CREATE TABLE t1(id SERIAL, c1 VARCHAR(800));
Query OK, 0 rows affected (0.024 sec)

MariaDB> ALTER TABLE t1 ADD INDEX(c1);
Query OK, 0 rows affected, 1 warning (0.031 sec)
Records: 0  Duplicates: 0  Warnings: 1

Note (Code 1071): Specified key was too long; max key length is 3072 bytes
MariaDB> SHOW CREATE TABLE t1\G
*************************** 1. row ***************************
       Table: t1
Create Table: CREATE TABLE `t1` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `c1` varchar(800) DEFAULT NULL,
  UNIQUE KEY `id` (`id`),
  KEY `c1` (`c1`(768))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci
1 row in set (0.001 sec)
```

MariaDB 对超过最大键长度的唯一索引也有特殊处理，如下所示。TiDB 不提供此功能。

```
MariaDB> CREATE TABLE t2 (id SERIAL PRIMARY KEY, c1 TEXT NOT NULL);
Query OK, 0 rows affected (0.015 sec)

MariaDB> ALTER TABLE t2 ADD INDEX regular_index_c1 (c1);
Query OK, 0 rows affected, 1 warning (0.034 sec)
Records: 0  Duplicates: 0  Warnings: 1

Note (Code 1071): Specified key was too long; max key length is 3072 bytes
MariaDB> ALTER TABLE t2 ADD UNIQUE INDEX unique_index_c1 (c1);
Query OK, 0 rows affected (0.048 sec)
Records: 0  Duplicates: 0  Warnings: 0

MariaDB> SHOW CREATE TABLE t2\G
*************************** 1. row ***************************
       Table: t2
Create Table: CREATE TABLE `t2` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `c1` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_index_c1` (`c1`) USING HASH,
  KEY `regular_index_c1` (`c1`(768))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_uca1400_ai_ci
1 row in set (0.001 sec)
```

要在 TiDB 中对长文本列强制唯一性，可以添加一个生成的哈希列，并在该生成的哈希列上创建唯一索引，如下所示：

```
tidb> CREATE TABLE t1 (id int PRIMARY KEY, c1 TEXT NOT NULL);
Query OK, 0 rows affected (0.102 sec)

tidb> ALTER TABLE t1 ADD COLUMN c1_hash BINARY(32) AS (UNHEX(SHA2(c1,256)));
Query OK, 0 rows affected (0.242 sec)

tidb> ALTER TABLE t1 ADD UNIQUE KEY (c1_hash);
Query OK, 0 rows affected (0.363 sec)

tidb> INSERT INTO t1(id,c1) VALUES (1,'aaa');
Query OK, 1 row affected (0.015 sec)

tidb> INSERT INTO t1(id,c1) VALUES (2,'bbb');
Query OK, 1 row affected (0.006 sec)

tidb> INSERT INTO t1(id,c1) VALUES (3,'aaa');
ERROR 1062 (23000): Duplicate entry '\x984\x87m\xCF\xB0\\xB1g\xA5\xC2IS\xEB\xA5\x8CJ\xC8\x9B\x1A\xDFW' for key 't1.c1_hash'
tidb>
```

## 使用 Dumpling 导出数据后使用 TiDB Lightning 导入

该迁移策略假定你将应用程序下线，迁移数据，然后重新配置应用程序以使用迁移后的数据。

> **注意：**
>
> 强烈建议你在生产环境操作之前，先在测试或开发环境中进行测试。这样既可以检查可能的兼容性问题，也可以了解迁移所需时长。

将数据从 MariaDB 迁移到 TiDB 的操作步骤如下：

1. 停止应用程序。将应用程序下线。这样可以确保在迁移过程中或迁移之后，MariaDB 中的数据不会被修改。

2. 导出数据。首先使用 [`tiup dumpling`](/dumpling-overview.md#使用-dumpling-导出数据) 命令从 MariaDB 导出数据。

    ```shell
    tiup dumpling --port 3306 --host 127.0.0.1 --user root --password secret -F 256MB  -o /data/backup
    ```

3. 使用 `tiup tidb-lightning` 命令恢复数据。请参考[TiDB Lightning 快速上手](/get-started-with-tidb-lightning.md)了解如何配置及运行 TiDB Lightning。

4. 迁移用户账号和权限。请参考[导出用户和授权](#导出用户和授权)了解如何迁移用户账号和权限。

5. 重新配置应用程序。你需要修改应用程序的配置，使其可以连接到 TiDB 服务器。

6. 清理环境。一旦确认迁移成功，你可以在 MariaDB 中做最后一次备份，然后停止 MariaDB 服务器。你可以删除 TiUP、Dumpling 和 TiDB Lightning 等工具。

## 使用 DM 迁移数据

该策略假定你将应用程序下线，等待复制数据，然后重新配置应用程序以使用 TiDB。

要使用 DM，你需要使用 [TiUP 集群](/dm/deploy-a-dm-cluster-using-tiup.md)或 [TiDB Operator](/tidb-operator-overview.md) 部署一组 DM 服务。之后，使用 `dmctl` 配置 DM 服务。

> **注意：**
>
> 强烈建议你在生产环境操作之前，先在测试或开发环境中进行测试。这样既可以检查可能的兼容性问题，也可以了解迁移所需时长。

### 第 1 步：准备工作

确保 MariaDB 上启用了 binlog，并且 `binlog_format` 设置为 `ROW`。建议设置 `binlog_annotate_row_events=OFF` 和 `log_bin_compress=OFF`。

你还需要一个拥有 `SUPER` 权限或 `BINLOG MONITOR` 和 `REPLICATION MASTER ADMIN` 权限的账号。该账号还需要对你要迁移的数据库有读权限。

如果你不使用拥有 `SUPER` 权限的账号，那么你可能需要在 DM 配置中添加以下内容，因为 TiDB 不知道如何检查 MariaDB 特有的权限。

```yaml
ignore-checking-items: ["replication_privilege"]
```

使用 DM 迁移数据前，可以使用预检查上游数据库配置是否正确，以确保迁移顺利进行。更多信息，请参考 [TiDB Data Migration 任务前置检查](/dm/dm-precheck.md)。

### 第 2 步：迁移数据

参考 [TiDB Data Migration 快速上手指南](/dm/quick-start-with-dm.md)了解如何从 MariaDB 迁移数据到 TiDB。

注意，与从 MariaDB 到 MariaDB 迁移数据时不同，你不需要先复制初始数据，因为 DM 会完成相关操作。

### 第 3 步：迁移用户账号和权限

参考[导出用户和授权](#导出用户和授权)了解如何迁移用户账号和权限。

### 第 4 步：测试数据

一旦数据开始迁移，你可以在其上运行只读查询来验证数据。更多信息，请参考[测试应用程序](#测试应用程序)。

### 第 5 步：切换系统

要将系统切换到 TiDB，你需要执行以下操作：

1. 停止应用程序。
2. 监控复制延迟，它应该变为 0 秒。
3. 修改应用程序的配置，使其连接到 TiDB，然后重新启动应用程序。

要检查复制延迟，使用 `dmctl` 运行 [`query-status <taskname>`](/dm/dm-query-status.md#详情查询结果)，并检查 `subTaskStatus` 中的 `"synced: true"`。

### 第 6 步：清理环境

一旦确认迁移成功，你可以在 MariaDB 中做最后一次备份，然后停止 MariaDB 服务器。这也意味着你可以停止并删除 DM 集群。

## 导出用户和授权

你可以使用 [`pt-show-grants`](https://docs.percona.com/percona-toolkit/pt-show-grants.html) 导出用户和授权。它是 Percona Toolkit 的一部分，用于从 MariaDB 导出用户和授权，并将其加载到 TiDB 中。

## 测试应用程序

虽然可以使用 `sysbench` 等通用工具进行测试，但是强烈建议你测试应用程序的某些特定功能。例如，使用临时数据副本，运行应用程序的副本，连接到 TiDB 集群。

这些测试可以确保应用程序与 TiDB 的兼容性和性能。你需要监控应用程序和 TiDB 的日志，以查看是否有任何需要解决的警告。确保测试应用程序使用的数据库驱动程序，例如 Java 应用程序的 MySQL Connector/J。如有必要，你可能需要使用 JMeter 等应用程序对应用程序进行负载测试。

## 验证数据

你可以使用 [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) 验证 MariaDB 和 TiDB 中的数据是否相同。