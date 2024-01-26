---
title: 从 MariaDB 文件迁移数据到 TiDB
summary: 介绍如何将数据从 MariaDB 文件迁移数据到 TiDB。
---

# 从 MariaDB 文件迁移数据到 TiDB

本文档介绍了如何将数据从 MariaDB 服务器迁移到 TiDB 集群。

## 前提条件

选择合适的迁移策略：

- 第一种策略是 [导出和恢复](#使用-dumpling-导出数据后使用-tidb-lightning-导入)。该策略适用于所有版本的 MariaDB。该策略的缺点是需要更多的停机时间。
- 第二种策略是使用 DM [迁移数据](#使用-dm-迁移数据) 从 MariaDB 到 TiDB。DM 不支持所有版本的 MariaDB。支持的版本请参考 [DM 兼容性目录](/dm/dm-compatibility-catalog.md#tidb-data-migration-兼容性目录) 。

除了以上两种策略，还有其他策略适用于特定的场景。例如：

- 使用 Object Relational Mapping (ORM) 工具重新部署和迁移数据。
- 修改应用程序，使其在迁移过程中同时读写 MariaDB 和 TiDB。

本文档仅介绍前两种策略。

根据你选择的策略，准备以下内容：

- 对于第一种策略：
    - 安装 [Dumpling](/dumpling-overview.md) 和 [TiDB Lightning](/tidb-lightning/tidb-lightning-overview.md)。
    - 确保你在 MariaDB 服务器上拥有[所需的权限](/dumpling-overview.md#required-privileges)，以便 Dumpling 导出数据。
- 对于第二种策略，设置 [DM](/dm/dm-overview.md)。

## 检查兼容性

TiDB 和 [MySQL 兼容](/mysql-compatibility.md)，而 MySQL 和 MariaDB 也有很多通用的特性。在迁移数据前需要注意，可能某些 MariaDB 特有的特性和 TiDB 并不兼容。

除了检查本小节介绍的事项之外，建议你参考 [MariaDB Compatibility & Differences](https://mariadb.com/kb/en/compatibility-differences/)检查相关配置。

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

```
+-----------------------+----------+
| plugin                | COUNT(*) |
+-----------------------+----------+
| mysql_native_password |       11 |
+-----------------------+----------+
1 row in set (0.002 sec)
```

### 系统版本表

TiDB does not support [system-versioned tables](https://mariadb.com/kb/en/system-versioned-tables/). However, TiDB does support [`AS OF TIMESTAMP`](/as-of-timestamp.md) which might replace some of the use cases of system-versioned tables.

TiDB 不支持[系统版本表 (System-Versioned Table)](https://mariadb.com/kb/en/system-versioned-tables/)。但是 TiDB 支持 [`AS OF TIMESTAMP`](/as-of-timestamp.md)，可以在某些场景下取代系统班报表。

你可以执行下列语句检查受影响的表格：

```sql
SELECT
  TABLE_SCHEMA,
  TABLE_NAME
FROM
  information_schema.tables
WHERE
  TABLE_TYPE='SYSTEM VERSIONED';
```

```
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | t          |
+--------------+------------+
1 row in set (0.005 sec)
```

要删除 `SYSTEM VERSIONING`，执行 `ALTER TABLE` 语句：

```
MariaDB [test]> ALTER TABLE t DROP SYSTEM VERSIONING;
Query OK, 0 rows affected (0.071 sec)
Records: 0  Duplicates: 0  Warnings: 0
```

### 序列

MariaDB 和 TiDB 都支持 [`CREATE SEQUENCE`](/sql-statements/sql-statement-create-sequence.md)，但是 DM 暂不支持。建议在迁移期间不要创建、修改或删除序列，尤其在迁移后不要进行相关测试。

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

```
+--------------+------------+
| TABLE_SCHEMA | TABLE_NAME |
+--------------+------------+
| test         | s1         |
+--------------+------------+
1 row in set (0.016 sec)
```

### 存储引擎

MariaDB 为本地数据提供了存储引擎，例如 `InnoDB`、`MyISAM` 和 `Aria`。虽然 TiDB 不直接支持这些数据格式，但是你仍可以迁移这些数据。但是，也有一些存储引擎将数据放在服务器之外，例如 `CONNECT` 存储引擎和 `Spider`。虽然你可以将这些表格迁移到 TiDB，但是 TiDB 没有将数据存储在 TiDB 集群之外的功能。

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

```
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

```
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

执行下列语句检查你正在使用的排序规则：

```sql
SHOW COLLATION;
```

```
+--------------------+---------+-----+---------+----------+---------+
| Collation          | Charset | Id  | Default | Compiled | Sortlen |
+--------------------+---------+-----+---------+----------+---------+
| ascii_bin          | ascii   |  65 | Yes     | Yes      |       1 |
| binary             | binary  |  63 | Yes     | Yes      |       1 |
| gbk_bin            | gbk     |  87 |         | Yes      |       1 |
| gbk_chinese_ci     | gbk     |  28 | Yes     | Yes      |       1 |
| latin1_bin         | latin1  |  47 | Yes     | Yes      |       1 |
| utf8_bin           | utf8    |  83 | Yes     | Yes      |       1 |
| utf8_general_ci    | utf8    |  33 |         | Yes      |       1 |
| utf8_unicode_ci    | utf8    | 192 |         | Yes      |       1 |
| utf8mb4_0900_ai_ci | utf8mb4 | 255 |         | Yes      |       1 |
| utf8mb4_0900_bin   | utf8mb4 | 309 |         | Yes      |       1 |
| utf8mb4_bin        | utf8mb4 |  46 | Yes     | Yes      |       1 |
| utf8mb4_general_ci | utf8mb4 |  45 |         | Yes      |       1 |
| utf8mb4_unicode_ci | utf8mb4 | 224 |         | Yes      |       1 |
+--------------------+---------+-----+---------+----------+---------+
13 rows in set (0.0012 sec)
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

```
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

## 使用 Dumpling 导出数据后使用 TiDB Lightning 导入

This method assumes that you take your application offline, migrate the data, and then re-configure your application to use the migrated data.

It is strongly recommended to first do this on a test or development instance of your application before doing it in production. This is both to check for possible compatibility issues as to get insight into how much time the migration will take.

1. Stop your application. Take your application offline. This ensures there are no modifications made to the data in MariaDB during or after the migration.

2. Dump the data. For this the first step is to dump data in MariaDB with the [`tiup dumpling`](/dumpling-overview.md#use-dumpling-to-export-data) command.

    ```shell
    tiup dumpling --port 3306 --host 127.0.0.1 --user root --password secret -F 256MB  -o /data/backup
    ```

3. Restore the data. For this step we will use the `tiup tidb-lightning` command. See [Get Started with TiDB Lightning](/get-started-with-tidb-lightning.md) for how to configure TiDB Lightning and how to run it.

4. Migrate user accounts and permissions. See [Export users and grants](#export-users-and-grants) for how to migrate your users and permissions.

5. Reconfigure your application. You need to change the application configuration so that it can connect to the TiDB server.

6. Clean up. Once you have verified that the migration is successful you can make a final backup of the data in MariaDB and stop the server. This also means you can remove tools such as TiUP, Dumpling, and TiDB Lightning.

## 使用 DM 迁移数据

This method assumes you would set up replication, stop your application and wait for the replication to catch up, and then re-configure your application to use TiDB.

It is strongly recommended to first test your application before doing this migration in production.

To use DM, you need to deploy a set of DM services either with a [TiUP cluster](/dm/deploy-a-dm-cluster-using-tiup.md) or with [TiDB Operator](/tidb-operator-overview.md). After that, use `dmctl` to configure the DM services.

### Step 1. Prepare

Make sure that binlogs are enabled on MariaDB and that the `binlog_format` is set to `ROW`. It is also recommended to set `binlog_annotate_row_events=OFF` and `log_bin_compress=OFF`.

You also need an account with the `SUPER` permission or with the `BINLOG MONITOR` and `REPLICATION MASTER ADMIN` permissions. This account also needs read permission for the schemas you are going to migrate.

If you are not using an account with the `SUPER` permission, then you might have to add the following to the DM configuration, because TiDB does not yet know how to check for MariaDB specific permissions.

```yaml
ignore-checking-items: ["replication_privilege"]
```

Before you use DM to migrate data from upstream to downstream, a precheck helps detect errors in the upstream database configurations and ensures that the migration goes smoothly. For more information, see [Migration Task Precheck](/dm/dm-precheck.md)

### Step 2. Replicate data

Note that it is not required to first copy the initial data as you would do with MariaDB to MariaDB replication, DM will do this for you.

Follow the [Quick Start Guide for TiDB Data Migration](/dm/quick-start-with-dm.md) to replicate your data from MariaDB to TiDB.

### Step 3. Migrate user accounts and permissions

See [Export users and grants](#export-users-and-grants) for how to migrate your users and permissions.

### Step 4. Test your data

Once your data is replicated, you can run read-only queries on it to validate it. For more information, see [Test your application](#test-your-application).

### Step 5. Switch over

To switch over to TiDB, you need to do the following:

1. Stop your application.
2. Monitor the replication delay, which should go to 0 seconds.
3. Change the configuration of your application so that it connects to TiDB and start it again.

To check for replication delay, run [`query-status <taskname>`](/dm/dm-query-status.md#detailed-query-result) via `dmctl` and check for `"synced: true"` in the `subTaskStatus`.

### Step 6. Clean up

Once you have verified that the migration is successful, you can make a final backup of the data in MariaDB and stop the server. It also means you can stop and remove the DM cluster.

## Export users and grants

You can use [`pt-show-grants`](https://docs.percona.com/percona-toolkit/pt-show-grants.html). It is part of the Percona Toolkit to export users and grants from MariaDB and load these into TiDB.

## Test your application

While it is possible to use generic tools such as `sysbench` for testing, it is highly recommended to test some specific features of your application. For example, run a copy of your application against a TiDB cluster with a temporary copy of your data.

Such a test makes sure your application compatibility and performance with TiDB is verified. You need to monitor the log files of your application and TiDB to see if there are any warnings that might need to be addressed. Make sure that the database driver that your application is using (for example MySQL Connector/J for Java based applications) is tested. You might want to use an application such as JMeter to put some load on your application if needed.

## Validate data

You can use [sync-diff-inspector](/sync-diff-inspector/sync-diff-inspector-overview.md) to validate if the data in MariaDB and TiDB are identical.
